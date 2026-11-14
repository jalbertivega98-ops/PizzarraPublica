import { useEffect, useMemo, useState } from 'react'
import { useStore, type Inhabitant } from '../state/store'
import { ISO_CODES, countryName, parseComment } from '../world/countries'
import { clock } from '../engine/clock'
import { world } from '../engine/director'

const flag = (iso: string) => <img className="flag" src={`/flags/${iso}.svg`} alt={iso} />
const STATUS: Record<string, string> = { pending: 'Pendiente', approved: 'Aprobado', built: 'Con casa', rejected: 'Rechazado', removed: 'Retirado' }

function parseCsv(text: string) {
  // columns: comment_id, platform, account_id, text   (header optional)
  const rows: Record<string, string>[] = []
  for (const line of text.split(/\r?\n/)) {
    if (!line.trim()) continue
    const cells: string[] = []
    let cur = '', q = false
    for (let i = 0; i < line.length; i++) {
      const ch = line[i]
      if (ch === '"') { if (q && line[i + 1] === '"') { cur += '"'; i++ } else q = !q }
      else if ((ch === ',' || ch === ';') && !q) { cells.push(cur); cur = '' }
      else cur += ch
    }
    cells.push(cur)
    if (/comment_id/i.test(cells[0])) continue
    rows.push({ comment_id: cells[0], platform: cells[1] || 'csv', account_id: cells[2], text: cells.slice(3).join(',') })
  }
  return rows
}

export function Panel() {
  const { env, data, error, cinema, setEnv, load, add, act, build, setCinema, locate, builds } = useStore()
  const [tab, setTab] = useState<'add' | 'people' | 'countries'>('add')
  const [text, setText] = useState('')
  const [name, setName] = useState('')
  const [iso, setIso] = useState('es')
  const [msg, setMsg] = useState<string | null>(null)
  const [hour, setHour] = useState(world.hour)
  const countries = useMemo(() => ISO_CODES.map((c) => [c, countryName(c)] as const).sort((a, b) => a[1].localeCompare(b[1], 'es')), [])
  useEffect(() => { load() }, [])
  useEffect(() => {
    if (!text) return
    const p = parseComment(text)
    if (p.iso) setIso(p.iso)
    if (p.name) setName(p.name)
  }, [text])
  useEffect(() => { world.hour = hour }, [hour])

  if (cinema) return <button className="cine-exit" onClick={() => setCinema(false)}>Salir del modo cine</button>

  const submit = async () => {
    const r = await add({ name: name || null, country: iso, text: text || null, comment_id: text ? 'manual-' + Date.now() : null })
    setMsg(r.ok ? (r.duplicate ? 'Ya existía: no se crea otra casa.' : '¡Nuevo habitante! Pulsa «Construir» para ver la obra.') : r.error ?? 'Error')
    if (r.ok) { setText(''); setName(''); setTab('people') }
  }
  const importCsv = async (f: File) => {
    const rows = parseCsv(await f.text())
    const r = await fetch(`/api/import?env=${env}`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ rows }) }).then((x) => x.json())
    const okN = r.results.filter((x: { ok: boolean; duplicate?: string }) => x.ok && !x.duplicate).length
    setMsg(`CSV: ${rows.length} filas, ${okN} nuevas pendientes de revisión.`)
    await load()
    setTab('people')
  }
  const backup = async () => {
    const snap = await fetch(`/api/backup?env=${env}`).then((r) => r.json())
    const a = document.createElement('a')
    a.href = URL.createObjectURL(new Blob([JSON.stringify(snap, null, 1)], { type: 'application/json' }))
    a.download = `pizzaville-${env}-${new Date().toISOString().slice(0, 16).replace(':', '')}.json`
    a.click()
  }
  const restore = async (f: File) => {
    const snapshot = JSON.parse(await f.text())
    const confirm = env === 'official' ? prompt('Esto sustituye el mundo OFICIAL. Escribe RESTAURAR') : 'RESTAURAR'
    const r = await fetch(`/api/restore?env=${env}`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ snapshot, confirm }) }).then((x) => x.json())
    setMsg(r.error ?? 'Mundo restaurado.')
    load()
  }
  const st = data?.stats
  const people = (data?.inhabitants ?? []).filter((h) => h.status !== 'removed')

  return (
    <>
      <div className="hud">
        <div className="brand">PIZZAVILLE<span>🍕</span></div>
        <div className="stats">
          <div><b>{st?.population ?? '–'}</b><small>habitantes</small></div>
          <div><b>{st?.houses ?? '–'}</b><small>casas</small></div>
          <div><b>{st?.countries.length ?? 0}</b><small>países</small></div>
        </div>
        <div className="env">
          <button className={env === 'sandbox' ? 'on' : ''} onClick={() => setEnv('sandbox')}>Pruebas</button>
          <button className={env === 'official' ? 'on official' : ''} onClick={() => setEnv('official')}>Mundo oficial</button>
        </div>
      </div>

      <aside className="panel">
        {error && <div className="err">{error}</div>}
        {msg && <p className="msg" onClick={() => setMsg(null)}>{msg}</p>}
        <nav>
          <button className={tab === 'add' ? 'on' : ''} onClick={() => setTab('add')}>Añadir</button>
          <button className={tab === 'people' ? 'on' : ''} onClick={() => setTab('people')}>Habitantes{st?.pending ? <i>{st.pending}</i> : null}</button>
          <button className={tab === 'countries' ? 'on' : ''} onClick={() => setTab('countries')}>Países</button>
        </nav>
        {tab === 'add' && (
          <section>
            <label>Comentario (opcional)</label>
            <textarea value={text} onChange={(e) => setText(e.target.value)} placeholder="Soy Marta de España 🇪🇸" rows={2} />
            <label>Nombre público</label>
            <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Marta" maxLength={24} />
            <label>País</label>
            <div className="row">
              {flag(iso)}
              <select value={iso} onChange={(e) => setIso(e.target.value)}>{countries.map(([c, n]) => <option key={c} value={c}>{n}</option>)}</select>
            </div>
            <button className="primary" onClick={submit}>Añadir habitante</button>
            <label className="file">Importar comentarios CSV<input type="file" accept=".csv,text/csv" onChange={(e) => e.target.files?.[0] && importCsv(e.target.files[0])} /></label>
          </section>
        )}
        {tab === 'people' && (
          <section className="list">
            {!people.length && <p className="muted">Pizz vive solo. Añade el primer habitante.</p>}
            {people.map((h: Inhabitant) => (
              <div className="person" key={h.id}>
                {flag(h.country)}
                <div className="who">
                  <b>{h.public_name ?? 'Anónimo'}{!h.show_name && h.public_name ? ' (oculto)' : ''}</b>
                  <small>{countryName(h.country)} · {STATUS[h.status]}{builds[h.id] !== undefined && h.status === 'approved' ? ' · en obras' : ''}</small>
                </div>
                <div className="acts">
                  {h.status === 'pending' && <><button onClick={() => act(h.id, 'approve')}>Aprobar</button><button onClick={() => act(h.id, 'reject')}>Rechazar</button></>}
                  {h.status === 'approved' && builds[h.id] === undefined && <button className="primary" onClick={() => { build(h.id); locate(h.x, h.y, h.z) }}>Construir</button>}
                  {(h.status === 'approved' || h.status === 'built') && <button onClick={() => locate(h.x, h.y, h.z)}>Ver</button>}
                  {h.public_name && <button onClick={() => act(h.id, h.show_name ? 'hide_name' : 'show_name')}>{h.show_name ? 'Ocultar nombre' : 'Mostrar'}</button>}
                  <button className="danger" onClick={() => confirm('¿Retirar a este habitante? Su casa desaparece.') && act(h.id, 'remove')}>Retirar</button>
                </div>
              </div>
            ))}
          </section>
        )}
        {tab === 'countries' && (
          <section className="list">
            {!st?.countries.length && <p className="muted">Todavía no hay países.</p>}
            {st?.countries.map((c, i) => (
              <div className="person" key={c.iso}><span className="pos">{i + 1}</span>{flag(c.iso)}<div className="who"><b>{c.name}</b></div><b>{c.n}</b></div>
            ))}
          </section>
        )}
        <footer>
          <label>Hora del día <input type="range" min={5} max={22} step={0.1} value={hour} onChange={(e) => setHour(+e.target.value)} /></label>
          <div className="row wrap">
            <button onClick={() => setCinema(true)}>Modo cine</button>
            <button onClick={() => locate(0, 1.2, 0)}>Casa de Pizz</button>
            <a className="btn" href="/?episode=ep000">Ver episodio 0</a>
            <button onClick={backup}>Descargar copia</button>
            <label className="btn file">Restaurar<input type="file" accept=".json" onChange={(e) => e.target.files?.[0] && restore(e.target.files[0])} /></label>
            <button onClick={() => (clock.speed = clock.speed === 1 ? 3 : 1)}>Velocidad x1/x3</button>
          </div>
        </footer>
      </aside>
    </>
  )
}
