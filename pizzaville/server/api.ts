// Pizzaville persistence API (Vite plugin, works in `vite` dev and `vite preview`).
// SQLite (node:sqlite, no extra deps) + JSON snapshot after every write + rotating backups.
// Two separate worlds: "official" (the real series) and "sandbox" (tests / demos).
import type { Plugin, Connect } from 'vite'
import { DatabaseSync } from 'node:sqlite'
import fs from 'node:fs'
import path from 'node:path'
import crypto from 'node:crypto'
import { plotSlots } from '../src/world/plots'
import { WORLD_SEED } from '../src/world/terrain'
import { ISO_CODES, parseComment, countryName } from '../src/world/countries'
import { hashString } from '../src/world/rng'

const ENVS = ['official', 'sandbox'] as const
type Env = (typeof ENVS)[number]
const DATA = path.resolve(process.cwd(), 'data')
const dbs = new Map<Env, DatabaseSync>()

const SCHEMA = `
CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE IF NOT EXISTS inhabitants (
  id TEXT PRIMARY KEY, comment_id TEXT UNIQUE, account_id TEXT, platform TEXT, public_name TEXT, show_name INTEGER DEFAULT 1,
  country TEXT NOT NULL, joined_at TEXT NOT NULL, episode INTEGER, plot_id TEXT UNIQUE, x REAL, z REAL, y REAL, rot REAL,
  house_seed INTEGER, look_seed INTEGER, status TEXT NOT NULL, built_at TEXT, source_text TEXT
);
CREATE UNIQUE INDEX IF NOT EXISTS one_house_per_account ON inhabitants(platform, account_id) WHERE account_id IS NOT NULL AND status NOT IN ('removed','rejected');
CREATE TABLE IF NOT EXISTS events (seq INTEGER PRIMARY KEY AUTOINCREMENT, key TEXT UNIQUE, type TEXT, payload TEXT, created_at TEXT);
`

function db(env: Env) {
  let d = dbs.get(env)
  if (d) return d
  fs.mkdirSync(path.join(DATA, env, 'backups'), { recursive: true })
  const file = path.join(DATA, env, 'pizzaville.sqlite')
  const fresh = !fs.existsSync(file)
  d = new DatabaseSync(file)
  d.exec('PRAGMA journal_mode=WAL;' + SCHEMA)
  d.prepare('INSERT OR IGNORE INTO meta(key,value) VALUES (?,?)').run('seed', String(WORLD_SEED))
  dbs.set(env, d)
  // a fresh container: restore from the committed JSON snapshot
  const snap = path.join(DATA, env, 'world.json')
  if (fresh && fs.existsSync(snap)) importSnapshot(env, JSON.parse(fs.readFileSync(snap, 'utf8')))
  return d
}

type Row = Record<string, unknown>
function all(env: Env) {
  return db(env).prepare('SELECT * FROM inhabitants ORDER BY joined_at, id').all() as Row[]
}

function snapshot(env: Env) {
  const d = db(env)
  const data = {
    version: 1, env, seed: WORLD_SEED, saved_at: new Date().toISOString(),
    meta: Object.fromEntries((d.prepare('SELECT key,value FROM meta').all() as Row[]).map((r) => [r.key, r.value])),
    inhabitants: all(env),
    events: d.prepare('SELECT * FROM events ORDER BY seq').all(),
  }
  return data
}

function persist(env: Env) {
  const data = JSON.stringify(snapshot(env), null, 1)
  const dir = path.join(DATA, env)
  const tmp = path.join(dir, 'world.json.tmp')
  fs.writeFileSync(tmp, data)
  fs.renameSync(tmp, path.join(dir, 'world.json')) // atomic replace: a crash never leaves a half file
  const bdir = path.join(dir, 'backups')
  fs.writeFileSync(path.join(bdir, `world-${Date.now()}.json`), data)
  const files = fs.readdirSync(bdir).filter((f) => f.endsWith('.json')).sort()
  for (const f of files.slice(0, Math.max(0, files.length - 30))) fs.unlinkSync(path.join(bdir, f))
}

function importSnapshot(env: Env, snap: { inhabitants: Row[]; events?: Row[]; meta?: Record<string, string> }) {
  const d = db(env)
  d.exec('BEGIN')
  try {
    d.exec('DELETE FROM inhabitants; DELETE FROM events;')
    const cols = ['id', 'comment_id', 'account_id', 'platform', 'public_name', 'show_name', 'country', 'joined_at', 'episode', 'plot_id', 'x', 'z', 'y', 'rot', 'house_seed', 'look_seed', 'status', 'built_at', 'source_text']
    const ins = d.prepare(`INSERT INTO inhabitants(${cols.join(',')}) VALUES (${cols.map(() => '?').join(',')})`)
    for (const r of snap.inhabitants) ins.run(...cols.map((c) => (r[c] ?? null) as never))
    const ev = d.prepare('INSERT INTO events(seq,key,type,payload,created_at) VALUES (?,?,?,?,?)')
    for (const e of snap.events ?? []) ev.run(e.seq as never, e.key as never, e.type as never, e.payload as never, e.created_at as never)
    for (const [k, v] of Object.entries(snap.meta ?? {})) d.prepare('INSERT OR REPLACE INTO meta(key,value) VALUES (?,?)').run(k, String(v))
    d.exec('COMMIT')
  } catch (e) {
    d.exec('ROLLBACK')
    throw e
  }
}

function event(env: Env, key: string | null, type: string, payload: unknown) {
  db(env).prepare('INSERT OR IGNORE INTO events(key,type,payload,created_at) VALUES (?,?,?,?)').run(key, type, JSON.stringify(payload), new Date().toISOString())
}

// ------------------------------------------------------------------ domain
export function addInhabitant(env: Env, body: Row) {
  const d = db(env)
  const comment_id = (body.comment_id as string) || null
  const platform = (body.platform as string) || 'manual'
  const account_id = (body.account_id as string) || null
  if (comment_id) {
    const ex = d.prepare('SELECT * FROM inhabitants WHERE comment_id = ?').get(comment_id) as Row | undefined
    if (ex) return { ok: true, duplicate: 'comment', inhabitant: ex }
  }
  if (account_id) {
    const ex = d.prepare("SELECT * FROM inhabitants WHERE platform = ? AND account_id = ? AND status NOT IN ('removed','rejected')").get(platform, account_id) as Row | undefined
    if (ex) return { ok: true, duplicate: 'account', inhabitant: ex }
  }
  let country = String(body.country ?? '').toLowerCase()
  let name = (body.name as string) || null
  if (body.text && (!country || !name)) {
    const p = parseComment(String(body.text))
    country ||= p.iso ?? ''
    name ||= p.name
  }
  if (!ISO_CODES.includes(country)) return { ok: false, error: 'País no reconocido' }
  const taken = new Set((d.prepare('SELECT plot_id FROM inhabitants WHERE plot_id IS NOT NULL').all() as Row[]).map((r) => r.plot_id))
  const slot = plotSlots().find((s) => !taken.has(s.id))
  if (!slot) return { ok: false, error: 'No quedan parcelas en esta región' }
  const id = 'h_' + crypto.randomBytes(5).toString('hex')
  const status = (body.status as string) || 'approved'
  const row = {
    id, comment_id, account_id, platform, public_name: name ? String(name).slice(0, 24) : null, show_name: body.show_name === false ? 0 : 1,
    country, joined_at: new Date().toISOString(), episode: (body.episode as number) ?? null, plot_id: slot.id, x: slot.x, z: slot.z, y: slot.y, rot: slot.rot,
    house_seed: hashString(id + ':house'), look_seed: hashString(id + ':look'), status, built_at: null, source_text: (body.text as string) ?? null,
  }
  const cols = Object.keys(row)
  d.prepare(`INSERT INTO inhabitants(${cols.join(',')}) VALUES (${cols.map(() => '?').join(',')})`).run(...(Object.values(row) as never[]))
  event(env, comment_id ? 'add:' + comment_id : null, 'inhabitant.added', { id, country, plot: slot.id })
  persist(env)
  return { ok: true, inhabitant: row }
}

const ACTIONS: Record<string, (d: DatabaseSync, id: string) => void> = {
  approve: (d, id) => d.prepare("UPDATE inhabitants SET status='approved' WHERE id=? AND status IN ('pending','rejected')").run(id),
  reject: (d, id) => d.prepare("UPDATE inhabitants SET status='rejected', plot_id=NULL WHERE id=? AND status='pending'").run(id),
  remove: (d, id) => d.prepare("UPDATE inhabitants SET status='removed', public_name=NULL, plot_id=NULL WHERE id=?").run(id),
  hide_name: (d, id) => d.prepare('UPDATE inhabitants SET show_name=0 WHERE id=?').run(id),
  show_name: (d, id) => d.prepare('UPDATE inhabitants SET show_name=1 WHERE id=?').run(id),
  built: (d, id) => d.prepare("UPDATE inhabitants SET status='built', built_at=? WHERE id=? AND status='approved'").run(new Date().toISOString(), id),
}

function world(env: Env) {
  const rows = all(env)
  const live = rows.filter((r) => r.status === 'approved' || r.status === 'built')
  const countries = new Map<string, number>()
  for (const r of live) countries.set(r.country as string, (countries.get(r.country as string) ?? 0) + 1)
  return {
    env, seed: WORLD_SEED,
    inhabitants: rows.map((r) => ({ ...r, display_name: r.show_name ? r.public_name : null })),
    stats: {
      population: live.length + 1, // + Pizz
      houses: rows.filter((r) => r.status === 'built').length + 1,
      pending: rows.filter((r) => r.status === 'pending').length,
      countries: [...countries.entries()].sort((a, b) => b[1] - a[1]).map(([iso, n]) => ({ iso, name: countryName(iso), n })),
    },
  }
}

// ------------------------------------------------------------------ http
function readBody(req: Connect.IncomingMessage): Promise<Row> {
  return new Promise((res) => {
    let s = ''
    req.on('data', (c) => (s += c))
    req.on('end', () => { try { res(s ? JSON.parse(s) : {}) } catch { res({}) } })
  })
}

const handler: Connect.NextHandleFunction = async (req, res, next) => {
  if (!req.url?.startsWith('/api/')) return next()
  const url = new URL(req.url, 'http://x')
  const env = (url.searchParams.get('env') ?? 'sandbox') as Env
  const send = (code: number, obj: unknown) => { res.statusCode = code; res.setHeader('content-type', 'application/json'); res.end(JSON.stringify(obj)) }
  if (!ENVS.includes(env)) return send(400, { error: 'env' })
  try {
    if (req.method === 'GET' && url.pathname === '/api/world') return send(200, world(env))
    if (req.method === 'POST' && url.pathname === '/api/inhabitants') {
      const r = addInhabitant(env, await readBody(req))
      return send(r.ok ? 200 : 400, r)
    }
    if (req.method === 'POST' && url.pathname === '/api/import') {
      // CSV rows already parsed client-side: [{comment_id, platform, account_id, text}]
      const body = await readBody(req)
      const out = (body.rows as Row[]).map((r) => addInhabitant(env, { ...r, status: 'pending' }))
      return send(200, { results: out })
    }
    const m = url.pathname.match(/^\/api\/inhabitants\/([\w-]+)$/)
    if (req.method === 'POST' && m) {
      const { action } = await readBody(req)
      const f = ACTIONS[action as string]
      if (!f) return send(400, { error: 'acción desconocida' })
      f(db(env), m[1])
      event(env, null, 'inhabitant.' + action, { id: m[1] })
      persist(env)
      return send(200, world(env))
    }
    if (req.method === 'GET' && url.pathname === '/api/backup') return send(200, snapshot(env))
    if (req.method === 'POST' && url.pathname === '/api/restore') {
      const body = await readBody(req)
      if (env === 'official' && body.confirm !== 'RESTAURAR') return send(400, { error: 'Escribe RESTAURAR para confirmar' })
      persist(env) // keep a backup of the current state first
      importSnapshot(env, body.snapshot as never)
      persist(env)
      return send(200, world(env))
    }
    if (req.method === 'POST' && url.pathname === '/api/reset') {
      if (env !== 'sandbox') return send(403, { error: 'Solo el entorno de pruebas se puede vaciar' })
      db(env).exec('DELETE FROM inhabitants; DELETE FROM events;')
      persist(env)
      return send(200, world(env))
    }
    send(404, { error: 'not found' })
  } catch (e) {
    send(500, { error: String(e) })
  }
}

export function pizzavilleApi(): Plugin {
  return {
    name: 'pizzaville-api',
    configureServer(s) { s.middlewares.use(handler) },
    configurePreviewServer(s) { s.middlewares.use(handler) },
  }
}
