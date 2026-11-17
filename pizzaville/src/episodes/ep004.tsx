// EPISODIO 4 — «El puente se hunde»: 107 vecinos, el puente central cae, hacen falta 100 piedras
// (cada comentario = una piedra). Enfoque captación: primer comentario x2, etiquetas suman piedras.
// Mundo persistente: reutiliza el reparto del ep003 y añade a los nuevos detrás.
import { useMemo, useRef } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { Text } from '@react-three/drei'
import * as THREE from 'three'
import { clock, ease, seg } from '../engine/clock'
import { evalCam, world, type CamKey } from '../engine/director'
import { useLines, mouthAt, speakingAt } from '../engine/voice'
import { Character, PIZZ_LOOK, lookFromSeed, newState, type CharState, type Look } from '../scene/Character'
import { House, houseSpecFromSeed } from '../scene/House'
import { PizzHome, HOME_Y } from '../scene/PizzHome'
import { NameTag } from '../scene/Town'
import { mat } from '../scene/materials'
import { hashString, mulberry32 } from '../world/rng'
import { extraReserved } from '../world/plots'
import { heightAt, RIVER, WATER_LEVEL } from '../world/terrain'
import { type Lot } from './ep001layout'
import { Tag, BigLabel, Bridge, Fence, PlotMarker } from './parts'
import { LAYOUT as L2, ISO, ISLE, STADIUM, wishStyle, type Item, Castle, BellTower, Terrace, Dog, Stadium, Island, FlagPost } from './ep002'
import { LAY as L3, BULLRING, STADIUM_Y, BaseProps, Bullring } from './ep003'
import VECINOS from '../../episodios/ep004/vecinos.csv?raw'

export const EP004 = {
  id: 'ep004',
  duration: 63.6,
  script: [
    { id: 'l01', at: 0.3, text: '¿Nunca has comentado? ¡Hoy es tu día! Comenta y tu piedra hace crecer Pizzaville.' },
    { id: 'l02', at: 4.43, text: 'Ciento siete vecinos... y anoche, ¡CRAC! Se ha hundido el puente grande.' },
    { id: 'l03', at: 8.53, text: 'Europa y América, incomunicadas. ¡Y los patos de Ronaldy flotando río abajo!' },
    { id: 'l04', at: 12.96, text: 'Para levantarlo hacen falta cien piedras. Cada comentario es una piedra... ¡y si es tu primer comentario, vale doble!' },
    { id: 'l05', at: 19.53, text: 'La votación de la oposición quedó en empate, así que el presidente decide: ¡Thiago carga las piedras!' },
    { id: 'l06', at: 25.11, text: 'Mientras, el pueblo no para: Sergio abre el museo de Fernando Alonso... ¡y Romeo quiere su circuito de Fórmula 1!' },
    { id: 'l07', at: 31.38, text: 'Yeray monta un cine, Adry se apunta a la comisaría, y Carlos y Eric fundan un club de fútbol profesional.' },
    { id: 'l08', at: 36.48, text: 'Y Oliver cumple: ¡baja los impuestos y hace parques para niños y abuelos!' },
    { id: 'l09', at: 40.55, text: 'Pero ojo: siete vecinos aún no tienen bandera. Gisela, Fran, Romeo, Noel... ¡decidnos vuestro país!' },
    { id: 'l10', at: 46.17, text: 'Europa lleva cincuenta y ocho, América cuarenta. ¿Qué orilla pone más piedras?' },
    { id: 'l11', at: 50.3, text: 'Comenta EUROPA o AMÉRICA y tu piedra va a tu orilla. ¡Y por cada amigo que etiquetes, otra piedra más!' },
    { id: 'l12', at: 55.58, text: '¿Eres nuevo? Tu nombre, tu país y qué quieres ser... ¡y te construyo la casa en el próximo episodio!' },
  ],
}
const A = Object.fromEntries(EP004.script.map((l) => [l.id, l.at])) as Record<string, number>
const PZ = { x: 0.15, z: 5.3 }
const CRAC = 6.27
const EUROPE = new Set(['España', 'Bulgaria'])
const ISLAND = new Set(['Marruecos', 'Líbano'])
const CIRCUIT = { x: 35, z: -155, rx: 30, rz: 17 }
const PILE_EU = { x: 29, z: -37 }, PILE_AM = { x: 29, z: -86 }

function csvRows(src: string): string[][] {
  const out: string[][] = []
  for (const line of src.split(/\r?\n/).slice(1)) {
    if (!line.trim()) continue
    const row: string[] = []; let cur = '', q = false
    for (let i = 0; i < line.length; i++) {
      const c = line[i]
      if (q) { if (c === '"' && line[i + 1] === '"') { cur += '"'; i++ } else if (c === '"') q = false; else cur += c }
      else if (c === '"') q = true
      else if (c === ',') { row.push(cur); cur = '' } else cur += c
    }
    row.push(cur); out.push(row)
  }
  return out
}

// ---------------------------------------------------------------- layout: ep003 + new neighbours
function build() {
  const rows = csvRows(VECINOS)
  const items: Item[] = L3.items.map((it) => ({ ...it, isNew: false, delay: -9 }))
  let k = 0
  const extra: Record<string, Item> = {}
  for (const c of rows.slice(91)) {
    const p = { name: c[0], country: c[1], iso: ISO[c[1]] ?? (c[1] ? 'es' : 'xx'), handle: c[3] ?? '', wish: c[4] ?? '', job: (c[6] ?? '').trim() }
    const lot = !p.country || EUROPE.has(p.country) ? L2.nextEu() : L2.nextAm()
    let { o, label, pool } = wishStyle(p.wish.toLowerCase())
    let sign: string | undefined, signColor: string | undefined
    if (/museo/.test(p.wish)) { sign = 'MUSEO FERNANDO ALONSO'; signColor = '#0f7a6b'; o = { w: 10.5, d: 7.5, floors: 2, wall: '#e8f1ef', roof: '#0f7a6b', roofType: 'hip', balcony: false } }
    if (/estanco/.test(p.job)) { sign = 'ESTANCO Y BAR JOEL'; signColor = '#a0522d' }
    if (/tractores/.test(p.wish)) label = 'GARAJE DE TRACTORES'
    if (/barrio propio/.test(p.wish)) label = 'BARRIO MÉXICO'
    if (/patos/.test(p.wish)) label = 'PATOS Y GALLINAS'
    if (/husky/.test(p.wish)) { pool = true; label = 'PISCINA + HUSKY Y BULLDOG' }
    if (/akron/i.test(p.wish)) label = 'QUIERE EL ESTADIO AKRON'
    if (/circuito/.test(p.wish)) label = 'PILOTO DE F1'
    if (/futbol|fútbol/.test(p.job)) label = 'FUTBOLISTA'
    if (/DJ/.test(p.job)) label = 'DJ'
    if (/militar/.test(p.job)) label = 'MILITAR'
    if (/comisar/.test(p.job)) label = 'OFICIAL DE POLICÍA'
    const it: Item = { key: 'n4_' + p.name + '_' + p.handle, lot, spec: { ...houseSpecFromSeed(hashString(p.name + p.country)), ...o }, iso: p.iso, name: p.name, label, sign, signColor, pool,
      isNew: true, delay: 0.35 + (k++) * 0.09, person: p as any }
    items.push(it); extra[p.name] = it
  }
  const cine: Item = { key: 'CINE YERAY', lot: L2.nextEu(), spec: { ...houseSpecFromSeed(401), w: 10, d: 8, floors: 2, wall: '#3a2b4f', roof: '#1a1426', roofType: 'hip', balcony: false, porch: false },
    iso: '', sign: 'CINE YERAY', signColor: '#c2185b', isNew: true, delay: 0.35 + (k++) * 0.09 }
  const parkLot = L2.nextEu()
  items.push(cine)
  for (const it of items) extraReserved.push({ x: it.lot.x, z: it.lot.z, r: 9 })
  extraReserved.push({ x: CIRCUIT.x, z: CIRCUIT.z, r: 36 }, { x: PILE_EU.x, z: PILE_EU.z, r: 5 }, { x: PILE_AM.x, z: PILE_AM.z, r: 5 })
  const free = L2.nextEu()
  const by = (n: string) => items.find((i) => i.name === n || i.key === n)!
  return { items, extra, cine, parkLot, free, by }
}
export const LAY4 = build()
;(globalThis as any).__ep4 = LAY4

const F = (l: Lot) => [Math.sin(l.rot), Math.cos(l.rot)]
function at(l: Lot, f: number, r: number, y: number): [number, number, number] {
  const [fx, fz] = F(l)
  return [l.x + fx * f + fz * r, l.y + y, l.z + fz * f - fx * r]
}
const look = (l: Lot, y = 2.6): [number, number, number] => [l.x, l.y + y, l.z]
const pileY = (p: { x: number; z: number }) => heightAt(p.x, p.z)
const CIRC_Y = (() => { let hi = -1e9; for (let a = 0; a < 24; a++) for (const k of [0, 0.7, 1.1]) hi = Math.max(hi, heightAt(CIRCUIT.x + Math.cos(a / 24 * 6.283) * CIRCUIT.rx * k, CIRCUIT.z + Math.sin(a / 24 * 6.283) * CIRCUIT.rz * k)); return hi + 0.15 })()

// ducks drifting down the river past the broken bridge
const S0 = RIVER.query(0, -60, 60).s
const duckAt = (i: number, t: number) => {
  const p = RIVER.at(S0 - 20 + i * 2.2 + t * 2.2)
  const side = ((i % 3) - 1) * 2.2
  return [p.x + p.tz * side, WATER_LEVEL + 0.12, p.z - p.tx * side, Math.atan2(p.tx, p.tz)] as const
}

// ---------------------------------------------------------------- camera
function cameraKeys(): CamKey[] {
  const H = HOME_Y + 1.6
  const shot = (t0: number, t1: number, l: Lot, d = 13, r = 4, y = 4.5): CamKey[] => [
    { t: t0, p: at(l, d + 9, r * 1.6, y + 3.5), l: look(l, 3.2), fov: 44, cut: true },
    { t: t1, p: at(l, d + 5, r * 1.2, y + 2.5), l: look(l, 3.0), fov: 42, e: 'linear' },
  ]
  const fl = LAY4.free, pk = LAY4.parkLot, C = CIRCUIT
  const ey = pileY(PILE_EU)
  const com = L2.job['COMISARÍA'].lot
  const q = LAY4.extra
  const qMid: Lot = { ...q.Gisela.lot, x: (q.Gisela.lot.x + q.Noel.lot.x) / 2, z: (q.Gisela.lot.z + q.Noel.lot.z) / 2 }
  const d1 = duckAt(4, 10.5), d2 = duckAt(4, 12.9)
  return [
    // S1 hook: Pizz talks straight to the newcomer
    { t: 0, p: [1.3, 2.62, 9.6], l: [PZ.x, H - 0.05, PZ.z], fov: 36 },
    { t: 4.33, p: [0.55, 2.52, 8.4], l: [PZ.x, H - 0.05, PZ.z], fov: 32, e: 'linear' },
    // S2 aerial towards the bridge… CRAC
    { t: A.l02, p: [-40, 70, 60], l: [20, 0, -60], fov: 50, cut: true },
    { t: CRAC - 0.06, p: [-5, 40, 10], l: [20, 0, -61], fov: 50, e: 'inOut' },
    { t: CRAC, p: [44, 9, -50], l: [20, 0.5, -61], fov: 50, cut: true },
    { t: A.l03 - 0.1, p: [40, 7.5, -52], l: [20, 0.5, -61], fov: 50, e: 'linear' },
    // S3 the two banks cut off, then the ducks
    { t: A.l03, p: [20, 45, -10], l: [20, 0, -62], fov: 50, cut: true },
    { t: 10.45, p: [20, 48, -18], l: [20, 0, -64], fov: 50, e: 'linear' },
    { t: 10.53, p: [d1[0] + 7, 3.2, d1[2] + 6], l: [d1[0], 0, d1[2]], fov: 42, cut: true },
    { t: A.l04 - 0.1, p: [d2[0] + 7, 3.2, d2[2] + 6], l: [d2[0], 0, d2[2]], fov: 42, e: 'linear' },
    // S4 the stone piles and the counter
    { t: A.l04, p: [PILE_EU.x + 14, ey + 8, PILE_EU.z + 12], l: [PILE_EU.x - 2, ey + 1, PILE_EU.z - 6], fov: 46, cut: true },
    { t: A.l05 - 0.1, p: [PILE_EU.x + 9, ey + 5, PILE_EU.z + 7], l: [PILE_EU.x - 2, ey + 1, PILE_EU.z - 6], fov: 46, e: 'linear' },
    // S5 Thiago carries stones while Oliver points
    { t: A.l05, p: [PILE_EU.x - 5, ey + 3.8, PILE_EU.z + 11], l: [PILE_EU.x - 3.5, ey + 1.2, PILE_EU.z - 2.5], fov: 46, cut: true },
    { t: A.l06 - 0.1, p: [PILE_EU.x - 4.5, ey + 3.2, PILE_EU.z + 8.5], l: [PILE_EU.x - 3.5, ey + 1.2, PILE_EU.z - 2.5], fov: 44, e: 'linear' },
    // S6 museum, then the F1 circuit
    { t: A.l06, p: [-60, 50, 80], l: [0, 0, 10], fov: 50, cut: true },
    { t: 26.65, p: [30, 50, 85], l: [0, 0, 10], fov: 50, e: 'linear' },
    ...shot(26.73, 29.25, q.Sergio.lot, 14, 4, 4),
    { t: 29.32, p: [C.x - 50, CIRC_Y + 32, C.z + 40], l: [C.x, CIRC_Y, C.z], fov: 48, cut: true },
    { t: A.l07 - 0.1, p: [C.x + 30, CIRC_Y + 28, C.z + 45], l: [C.x, CIRC_Y, C.z], fov: 48, e: 'linear' },
    // S7 cinema, Adry at the police station, the pro football club
    ...shot(A.l07, 32.4, LAY4.cine.lot, 13, -4, 4),
    ...shot(32.47, 33.85, com, 11, 3, 3),
    { t: 33.92, p: [STADIUM.x - 22, STADIUM_Y + 14, STADIUM.z + 26], l: [STADIUM.x, STADIUM_Y + 1, STADIUM.z], fov: 46, cut: true },
    { t: A.l08 - 0.1, p: [STADIUM.x - 10, STADIUM_Y + 10, STADIUM.z + 22], l: [STADIUM.x, STADIUM_Y + 1, STADIUM.z], fov: 46, e: 'linear' },
    // S8 Oliver's park
    ...shot(A.l08, A.l09 - 0.1, pk, 10, 3, 4),
    // S9 neighbours still without a flag
    { t: A.l09, p: at(qMid, 34, -14, 22), l: look(qMid, 2), fov: 50, cut: true },
    { t: A.l10 - 0.1, p: at(qMid, 26, 10, 16), l: look(qMid, 2), fov: 50, e: 'linear' },
    // S10 continents: high aerial
    { t: A.l10, p: [-70, 170, 170], l: [60, 0, -30], fov: 52, cut: true },
    { t: A.l11 - 0.1, p: [120, 170, 170], l: [110, 0, -25], fov: 52, e: 'linear' },
    // S11 both banks with their piles: comment EUROPA or AMÉRICA
    { t: A.l11, p: [62, 22, -61], l: [24, 0, -61], fov: 50, cut: true },
    { t: A.l12 - 0.1, p: [52, 17, -61], l: [24, 0, -61], fov: 50, e: 'linear' },
    // S12 Pizz, the free plot, up and away
    { t: A.l12, p: [1.4, 2.6, 10.0], l: [PZ.x, H - 0.05, PZ.z], fov: 38, cut: true },
    { t: 58.38, p: [0.5, 2.5, 8.6], l: [PZ.x, H - 0.05, PZ.z], fov: 34, e: 'linear' },
    { t: 58.45, p: [fl.x + 6, fl.y + 16, fl.z - 22], l: [fl.x, fl.y + 2, fl.z], fov: 48, cut: true },
    { t: 61.3, p: [fl.x + 4, fl.y + 12, fl.z - 17], l: [fl.x, fl.y + 2, fl.z], fov: 48, e: 'linear' },
    { t: 61.9, p: [fl.x + 3.6, fl.y + 11.5, fl.z - 16], l: [fl.x, fl.y + 2.2, fl.z], fov: 48, e: 'linear' },
    { t: EP004.duration, p: [80, 170, 220], l: [40, 0, -25], fov: 52, e: 'inOut' },
  ]
}

// ---------------------------------------------------------------- cast
const tint = (seed: number, top: string, extra: Partial<Look> = {}): Look => {
  const c = new THREE.Color(top)
  return { ...lookFromSeed(seed), top, topDark: '#' + c.multiplyScalar(0.78).getHexString(), ...extra }
}
type Act = 'wave' | 'celebrate' | 'hammer' | 'point' | 'shrug' | 'surprise' | 'talk' | 'none'
type Cast = { key: string; tag?: string; look: Look; pos: (t: number) => [number, number, number]; ry: number | ((t: number) => number); act: (t: number) => Act; moving?: (t: number) => boolean; carry?: boolean }

function cast(): Cast[] {
  const q = LAY4.extra
  const front = (l: Lot, f: number, r: number) => () => at(l, f, r, 0)
  const S = STADIUM
  const com = L2.job['COMISARÍA'].lot
  const pk = LAY4.parkLot
  // Thiago walks between the pile and the bridge end carrying a stone
  const thiago = (t: number): [number, number, number] => {
    const u = (Math.sin(t * 0.9) + 1) / 2
    const x = PILE_EU.x - 1 - u * 6, z = PILE_EU.z - 1.5 - u * 3.5
    return [x, heightAt(x, z), z]
  }
  const out: Cast[] = [
    { key: 'Thiago', tag: 'THIAGO', look: tint(12, '#3fa9f5'), pos: thiago, ry: (t) => (Math.cos(t * 0.9) > 0 ? 0.6 + Math.PI : 0.6), act: () => 'none', moving: () => true, carry: true },
    { key: 'Oliver', tag: 'PRESIDENTE OLIVER', look: tint(11, '#ffd23d'), pos: () => [PILE_EU.x + 1.5, heightAt(PILE_EU.x + 1.5, PILE_EU.z + 2.5), PILE_EU.z + 2.5], ry: Math.PI + 0.5, act: (t) => (t < A.l06 ? 'point' : 'wave') },
    { key: 'OliverPark', tag: 'OLIVER', look: tint(11, '#ffd23d'), pos: front(pk, 4.5, 1.5), ry: pk.rot, act: () => 'celebrate' },
    { key: 'Sergio', look: tint(41, '#0f7a6b'), pos: front(q.Sergio.lot, q.Sergio.spec.d / 2 + 3, -2), ry: q.Sergio.lot.rot, act: () => 'wave' },
    { key: 'Romeo', tag: 'ROMEO', look: tint(42, '#d23c3c'), pos: () => [CIRCUIT.x, CIRC_Y, CIRCUIT.z + CIRCUIT.rz + 3], ry: 0, act: () => 'celebrate' },
    { key: 'Yeray', look: tint(43, '#c2185b'), pos: front(LAY4.cine.lot, LAY4.cine.spec.d / 2 + 2.6, 1), ry: LAY4.cine.lot.rot, act: () => 'wave' },
    { key: 'Adry', tag: 'ADRY · OFICIAL', look: tint(44, '#1f3a6b', { pants: '#1c2533' }), pos: front(com, 6.2, 0), ry: com.rot, act: () => 'wave' },
    ...['Carlos', 'Eric'].map((n, i): Cast => ({ key: n, tag: n.toUpperCase(), look: tint(45 + i, i ? '#111111' : '#ffffff', { pants: '#111111' }),
      pos: () => [S.x - 2 + i * 4, STADIUM_Y, S.z + 2], ry: 0, act: () => 'celebrate' })),
  ]
  // kids and grandparents in the park
  const r = mulberry32(44)
  for (let i = 0; i < 6; i++) out.push({ key: 'park' + i, look: lookFromSeed(2000 + i), pos: front(pk, 1 + r() * 4, -4 + r() * 8), ry: pk.rot + (r() - 0.5) * 2, act: () => (i % 2 ? 'celebrate' : 'wave') })
  return out
}

// ---------------------------------------------------------------- component
export function Ep004() {
  const { camera } = useThree()
  const lines = useMemo(() => useLines(EP004.id, EP004.script), [])
  const keys = useMemo(cameraKeys, [])
  const pizz = useMemo(newState, [])
  const P = useMemo(() => new THREE.Vector3(), [])
  const L = useMemo(() => new THREE.Vector3(), [])
  const camPos = useMemo(() => new THREE.Vector3(), [])
  const labels = useRef<THREE.Group>(null!)
  const marker = useRef<THREE.Group>(null!)
  const ducks = useRef<THREE.Group>(null!)
  const halfS = useRef<THREE.Group>(null!)
  const halfN = useRef<THREE.Group>(null!)
  const splash = useRef<THREE.Group>(null!)
  const stone = useRef<THREE.Mesh>(null!)
  const cars = useRef<THREE.Group>(null!)
  const people = useMemo(cast, [])
  const states = useMemo(() => people.map(() => newState()), [])
  const T = () => clock.t

  useMemo(() => {
    const pv = (window as any).__pv
    if (!pv) return
    pv.info = () => {
      const sfx: { type: string; at: number; g?: number }[] = [{ type: 'whoosh', at: 0.0, g: 0.5 }]
      for (const k of keys) if (k.cut && k.t > 3) sfx.push({ type: 'whoosh', at: k.t - 0.05, g: 0.3 })
      sfx.push({ type: 'thud', at: CRAC, g: 1.0 }, { type: 'thud', at: CRAC + 0.35, g: 0.8 }, { type: 'pop', at: CRAC + 0.5, g: 0.4 })
      sfx.push({ type: 'chime', at: A.l04 + 1.6, g: 0.5 }, { type: 'chime', at: A.l04 + 5.8, g: 0.6 }, { type: 'chime', at: A.l08 + 1.0, g: 0.5 }, { type: 'chime', at: A.l11 + 0.6, g: 0.6 })
      return { id: EP004.id, duration: EP004.duration, lines: lines.map((l) => ({ id: l.id, at: l.at, dur: l.dur, text: l.text, words: l.words, hasAudio: l.hasAudio })), sfx }
    }
  }, [])

  useFrame(() => {
    const t = T()
    const fov = evalCam(keys, t, P, L)
    camera.position.copy(P); camera.lookAt(L)
    const pc = camera as THREE.PerspectiveCamera
    if (Math.abs(pc.fov - fov) > 0.01) { pc.fov = fov; pc.updateProjectionMatrix() }
    camPos.copy(P)
    world.focus.set(L.x, 0, L.z)
    world.shadowSpan = THREE.MathUtils.clamp(P.distanceTo(L) * 0.9, 18, 120)

    pizz.x = PZ.x; pizz.z = PZ.z; pizz.y = HOME_Y; pizz.ry = 0.15; pizz.speed = 0
    pizz.lookAt = camPos; pizz.action = 'none'; pizz.actionW = 0; pizz.smile = 0.8
    if (t < 1.2) { pizz.action = 'point'; pizz.actionT = t; pizz.actionW = seg(t, 0, 0.25) * (1 - seg(t, 1.0, 1.2)) }
    else if (t > A.l12 && t < A.l12 + 1.8) { pizz.action = 'point'; pizz.actionT = t; pizz.actionW = seg(t, A.l12, A.l12 + 0.3) * (1 - seg(t, A.l12 + 1.5, A.l12 + 1.8)) }
    else if (speakingAt(lines, t)) { pizz.action = 'talk'; pizz.actionT = t; pizz.actionW = 0.85 }
    pizz.mouth = mouthAt(lines, t)

    people.forEach((c, i) => {
      const st = states[i]
      const [x, y, z] = c.pos(t)
      st.x = x; st.y = y; st.z = z
      const mv = c.moving?.(t) ?? false
      st.speed = mv ? 1.6 : 0
      st.ry = typeof c.ry === 'function' ? c.ry(t) : c.ry
      st.lookAt = mv ? null : camPos
      const a = c.act(t)
      st.action = a; st.actionT = t + i * 0.31; st.actionW = a === 'none' ? 0 : 1
    })
    // the stone Thiago carries
    const th = states[0]
    stone.current.position.set(th.x + Math.sin(th.ry) * 0.45, th.y + 1.25, th.z + Math.cos(th.ry) * 0.45)

    // the bridge collapses at CRAC
    const k = ease.outBack(seg(t, CRAC, CRAC + 0.55))
    halfS.current.rotation.x = -0.24 * k
    halfN.current.rotation.x = 0.22 * k
    splash.current.visible = t > CRAC + 0.2 && t < CRAC + 1.6
    splash.current.children.forEach((m, i) => {
      const u = seg(t, CRAC + 0.2, CRAC + 1.6)
      m.position.y = Math.sin(u * Math.PI) * (1.5 + (i % 3)) - 0.2
      m.scale.setScalar(Math.max(0.01, 1 - u))
    })
    ducks.current.children.forEach((m, i) => {
      const [x, y, z, ry] = duckAt(i, t)
      m.position.set(x, y + Math.sin(t * 3 + i) * 0.05, z); m.rotation.y = ry + Math.sin(t * 2 + i) * 0.4
    })
    cars.current.children.forEach((m, i) => {
      const a = t * (1.1 + i * 0.12) + i * 1.3
      m.position.set(CIRCUIT.x + Math.cos(a) * CIRCUIT.rx * 0.82, CIRC_Y + 0.05, CIRCUIT.z + Math.sin(a) * CIRCUIT.rz * 0.75)
      m.rotation.y = -a
    })

    labels.current.visible = t > A.l10 && t < A.l11
    marker.current.visible = t > 58.4
    marker.current.scale.setScalar(Math.max(0.001, ease.outBack(seg(t, 58.5, 59.0))) * 1.5)
  }, -1)

  const prog = (it: Item) => (it.isNew ? () => seg(T(), 0.4 + it.delay, 1.1 + it.delay) : () => 1)
  const fl = LAY4.free
  const pk = LAY4.parkLot
  return (
    <group>
      <PizzHome />
      <Character look={PIZZ_LOOK} state={pizz} />
      {people.map((c, i) => <Character key={c.key} look={c.look} state={states[i] as CharState} />)}
      {people.map((c, i) => c.tag ? <CharTag key={'tag' + c.key} text={c.tag} st={states[i]} /> : null)}
      <mesh ref={stone} material={mat('#8a8f96', { rough: 1 })} castShadow><dodecahedronGeometry args={[0.42, 0]} /></mesh>
      {LAY4.items.filter((it) => !ISLAND.has(it.person?.country ?? '')).map((it) => (
        <group key={it.key} position={[it.lot.x, it.lot.y, it.lot.z]} rotation-y={it.lot.rot}>
          {it.castle ? <Castle getProgress={prog(it)} /> : <House spec={it.spec} getProgress={prog(it)} flag={it.iso || null} />}
          {it.castle && <group position={[3.4, 0, 6.2]}><FlagPost iso={it.iso} h={3.5} /></group>}
          {it.pool && (
            <mesh position={[it.spec.w / 2 + 2.6, 0.08, 0.5]} material={mat('#3fb6e8', { rough: 0.15, emissive: '#1d8fc4', ei: 0.25 })}>
              <boxGeometry args={[3.2, 0.12, 4.4]} />
            </mesh>
          )}
          {it.fence && <Fence w={it.spec.w + 5} d={it.spec.d + 5} />}
          {it.key === 'IGLESIA' && <BellTower h={it.spec.wallH * 2} d={it.spec.d} />}
          {it.key.startsWith('RESTAURANTE') && <Terrace w={it.spec.w} d={it.spec.d} />}
          {it.key === 'RESTAURANTE MATHEUS' && <group position={[0.4, 0, it.spec.d / 2 + 2.0]} rotation-y={0.5}><Dog /></group>}
          {it.key === 'BASE MILITAR' && <BaseProps w={it.spec.w} d={it.spec.d} />}
          {it.sign === 'MUSEO FERNANDO ALONSO' && <group position={[-1.5, 0, it.spec.d / 2 + 2.6]} rotation-y={0.4}><F1Car color="#0f7a6b" /></group>}
          {it.key === 'CINE YERAY' && <Marquee w={it.spec.w} d={it.spec.d} />}
          {/husky/.test(it.person?.wish ?? '') && <group position={[it.spec.w / 2 + 1.2, 0, it.spec.d / 2 + 2]}><Dog color="#d9dde3" ear="#5a6068" scale={1.4} /><group position={[1.2, 0, 0.6]}><Dog color="#c9a27a" ear="#8a6a4a" scale={1.1} /></group></group>}
          {/patos/.test(it.person?.wish ?? '') && <Fence w={it.spec.w + 5} d={it.spec.d + 5} />}
        </group>
      ))}
      {LAY4.items.map((it) => (
        <group key={'t' + it.key} position={[it.lot.x, it.lot.y + (it.castle ? 12.5 : it.spec.wallH * it.spec.floors + 3.8), it.lot.z]} scale={1.6}>
          {it.name && <NameTag name={it.name} iso={it.iso} />}
          {it.label && <Tag text={it.label} y={-0.62} color="#ffd23d" />}
          {it.sign && <Tag text={it.sign} y={it.name ? 0.75 : 0} color="#ffffff" bg={it.signColor} big />}
        </group>
      ))}
      <Bridge x={-45} />
      <Bridge x={85} />
      <BrokenBridge halfS={halfS} halfN={halfN} splash={splash} />
      <StonePile p={PILE_EU} label="EUROPA · 0 PIEDRAS" color="#ffd23d" />
      <StonePile p={PILE_AM} label="AMÉRICA · 0 PIEDRAS" color="#7fe0ff" />
      <group position={[24, 9, -61]} scale={2.6}><Tag text="PUENTE: 0 / 100 PIEDRAS" y={0} color="#1a2233" bg="#ffd23d" big /></group>
      <group ref={ducks}>{Array.from({ length: 9 }, (_, i) => <Duck key={i} />)}</group>
      <Stadium progress={() => 1} label="CLUB PROFESIONAL DE CARLOS Y ERIC" />
      <Bullring />
      <Island getProgress={() => 0.72} items={LAY4.items.filter((it) => ISLAND.has(it.person?.country ?? ''))} />
      <Circuit />
      <group ref={cars}>{[0, 1, 2].map((i) => <F1Car key={i} color={['#d23c3c', '#0f7a6b', '#f2b81e'][i]} />)}</group>
      <Park lot={pk} />
      <group ref={labels}>
        <BigLabel text="EUROPA 58" position={[0, 22, 22]} color="#ffd23d" />
        <BigLabel text="AMÉRICA 40" position={[10, 26, -100]} color="#7fe0ff" />
        <BigLabel text="ÁFRICA · ASIA" position={[ISLE.x, 24, ISLE.z]} color="#7dffa8" />
      </group>
      <group ref={marker} position={[fl.x, fl.y + 4, fl.z]}>
        <PlotMarker />
      </group>
    </group>
  )
}

// ---------------------------------------------------------------- props
function CharTag({ text, st }: { text: string; st: CharState }) {
  const g = useRef<THREE.Group>(null!)
  useFrame(() => { g.current.position.set(st.x, st.y + 2.55, st.z); g.current.visible = st.visible }, -2)
  return <group ref={g} scale={1.1}><Tag text={text} y={0} color="#ffffff" bg="#ec6a3f" /></group>
}

function BrokenBridge({ halfS, halfN, splash }: { halfS: React.RefObject<THREE.Group>; halfN: React.RefObject<THREE.Group>; splash: React.RefObject<THREE.Group> }) {
  const x = 20, z0 = -42, z1 = -80, y = 2.3, half = (z0 - z1) / 2
  const deck = mat('#9a6a43', { rough: 0.85 }), rail = mat('#6e4a2f', { rough: 0.9 })
  const Half = ({ dir }: { dir: number }) => (
    <group>
      <mesh position={[0, 0, dir * half / 2]} material={deck} castShadow><boxGeometry args={[4.2, 0.45, half]} /></mesh>
      {[-2, 2].map((s) => <mesh key={s} position={[s, 0.75, dir * half / 2]} material={rail}><boxGeometry args={[0.18, 0.18, half]} /></mesh>)}
      {Array.from({ length: 5 }, (_, i) => [-2, 2].map((s) => <mesh key={i + '_' + s} position={[s, 0.4, dir * (1 + i * (half - 2) / 4)]} material={rail}><boxGeometry args={[0.16, 0.8, 0.16]} /></mesh>))}
    </group>
  )
  return (
    <group>
      <group ref={halfS} position={[x, y, z0]}><Half dir={-1} /></group>
      <group ref={halfN} position={[x, y, z1]}><Half dir={1} /></group>
      <group ref={splash} position={[x, WATER_LEVEL, (z0 + z1) / 2]}>
        {Array.from({ length: 10 }, (_, i) => (
          <mesh key={i} position={[Math.cos(i * 0.63) * 2.5, 0, Math.sin(i * 0.63) * 2.5]} material={mat('#e8f6ff', { rough: 0.3, transparent: true, opacity: 0.85 })}><sphereGeometry args={[0.5, 8, 6]} /></mesh>
        ))}
      </group>
      {/* planks drifting */}
      {[[-3, 2, 0.4], [3, -4, -0.6], [1, 6, 1.1]].map(([dx, dz, r], i) => (
        <mesh key={i} position={[x + dx, WATER_LEVEL + 0.1, (z0 + z1) / 2 + dz]} rotation-y={r} material={deck}><boxGeometry args={[0.6, 0.15, 3]} /></mesh>
      ))}
    </group>
  )
}

function StonePile({ p, label, color }: { p: { x: number; z: number }; label: string; color: string }) {
  const y = heightAt(p.x, p.z)
  const r = mulberry32(Math.round(p.z))
  return (
    <group position={[p.x, y, p.z]}>
      {Array.from({ length: 4 }, (_, i) => (
        <mesh key={i} position={[(r() - 0.5) * 1.2, 0.3, (r() - 0.5) * 1.2]} rotation={[r() * 3, r() * 3, 0]} material={mat('#8a8f96', { rough: 1 })} castShadow><dodecahedronGeometry args={[0.4, 0]} /></mesh>
      ))}
      <mesh position={[1.8, 1.0, 0]} material={mat('#6e4a2f')}><boxGeometry args={[0.15, 2, 0.15]} /></mesh>
      <group position={[1.8, 3.0, 0]} scale={1.5}><Tag text={label} y={0} color="#1a2233" bg={color} big /></group>
    </group>
  )
}

function Duck() {
  return (
    <group scale={0.9}>
      <mesh position={[0, 0.15, 0]} material={mat('#fff6d6', { rough: 0.8 })}><boxGeometry args={[0.45, 0.3, 0.6]} /></mesh>
      <mesh position={[0, 0.42, 0.25]} material={mat('#fff6d6', { rough: 0.8 })}><boxGeometry args={[0.28, 0.28, 0.28]} /></mesh>
      <mesh position={[0, 0.38, 0.45]} material={mat('#f29a1e')}><boxGeometry args={[0.16, 0.08, 0.16]} /></mesh>
      {[-0.08, 0.08].map((x) => <mesh key={x} position={[x, 0.48, 0.39]} material={mat('#111111')}><boxGeometry args={[0.04, 0.04, 0.02]} /></mesh>)}
    </group>
  )
}

function F1Car({ color }: { color: string }) {
  const k = mat('#1b1b1f'), c = mat(color, { rough: 0.35 })
  return (
    <group scale={1.3}>
      <mesh position={[0, 0.3, 0]} material={c} castShadow><boxGeometry args={[0.7, 0.3, 2.6]} /></mesh>
      <mesh position={[0, 0.5, -0.2]} material={k}><boxGeometry args={[0.4, 0.25, 0.6]} /></mesh>
      <mesh position={[0, 0.3, 1.45]} material={c}><boxGeometry args={[1.3, 0.08, 0.35]} /></mesh>
      <mesh position={[0, 0.65, -1.25]} material={c}><boxGeometry args={[1.1, 0.08, 0.3]} /></mesh>
      {[[-0.6, 0.8], [0.6, 0.8], [-0.6, -0.9], [0.6, -0.9]].map(([x, z], i) => (
        <mesh key={i} position={[x, 0.25, z]} rotation-z={Math.PI / 2} material={k}><cylinderGeometry args={[0.25, 0.25, 0.3, 12]} /></mesh>
      ))}
    </group>
  )
}

function Circuit() {
  const C = CIRCUIT
  const lo = useMemo(() => { let l = 1e9; for (let a = 0; a < 24; a++) l = Math.min(l, heightAt(C.x + Math.cos(a / 24 * 6.283) * C.rx * 1.2, C.z + Math.sin(a / 24 * 6.283) * C.rz * 1.2)); return l }, [])
  return (
    <group position={[C.x, 0, C.z]}>
      <mesh position={[0, (lo - 1 + CIRC_Y) / 2, 0]} scale={[C.rx + 5, 1, C.rz + 5]} material={mat('#7dbb4f', { rough: 1 })} receiveShadow><cylinderGeometry args={[1, 1, CIRC_Y - lo + 1, 40]} /></mesh>
      <group scale={[C.rx * 0.82, 1, C.rz * 0.75]}>
        <mesh position={[0, CIRC_Y + 0.02, 0]} rotation-x={-Math.PI / 2} material={mat('#3a3d44', { rough: 0.9 })} receiveShadow><ringGeometry args={[0.86, 1.14, 64]} /></mesh>
        <mesh position={[0, CIRC_Y + 0.03, 0]} rotation-x={-Math.PI / 2} material={mat('#d23c3c')}><ringGeometry args={[1.14, 1.17, 64]} /></mesh>
        <mesh position={[0, CIRC_Y + 0.03, 0]} rotation-x={-Math.PI / 2} material={mat('#ffffff')}><ringGeometry args={[0.83, 0.86, 64]} /></mesh>
      </group>
      {/* start line + grandstand */}
      <mesh position={[0, CIRC_Y + 0.04, C.rz * 0.75]} rotation-x={-Math.PI / 2} material={mat('#ffffff')}><planeGeometry args={[0.6, 5]} /></mesh>
      <mesh position={[0, CIRC_Y + 1.2, C.rz * 0.75 + 5.5]} material={mat('#ec6a3f', { rough: 0.8 })} castShadow><boxGeometry args={[16, 2.4, 2.5]} /></mesh>
      <group position={[0, CIRC_Y + 8, 0]} scale={2.4}><Tag text="CIRCUITO F1 DE ROMEO" y={0} color="#ffffff" bg="#d23c3c" big /></group>
    </group>
  )
}

function Marquee({ w, d }: { w: number; d: number }) {
  const g = useRef<THREE.Group>(null!)
  useFrame(() => { g.current.children.forEach((m, i) => { m.visible = Math.floor(clock.t * 6 + i) % 2 === 0 }) })
  return (
    <group position={[0, 3.2, d / 2 + 0.6]}>
      <mesh material={mat('#c2185b', { emissive: '#c2185b', ei: 0.4 })}><boxGeometry args={[w * 0.8, 1.1, 0.5]} /></mesh>
      <Text font="/fonts/lilita.woff" fontSize={0.55} color="#fff6d6" position={[0, 0, 0.27]} anchorX="center" anchorY="middle">ESTRENO HOY</Text>
      <group ref={g}>
        {Array.from({ length: 12 }, (_, i) => <mesh key={i} position={[-w * 0.38 + i * (w * 0.76 / 11), -0.62, 0.27]} material={mat('#ffd23d', { emissive: '#ffd23d', ei: 1.2 })}><sphereGeometry args={[0.1, 6, 5]} /></mesh>)}
      </group>
    </group>
  )
}

function Park({ lot }: { lot: Lot }) {
  const grass = mat('#6fbf4a', { rough: 1 }), wood = mat('#8a5a3a'), metal = mat('#d23c3c', { rough: 0.5 })
  return (
    <group position={[lot.x, lot.y, lot.z]} rotation-y={lot.rot}>
      <mesh position={[0, 0.06, 0]} material={grass} receiveShadow><boxGeometry args={[12, 0.12, 9]} /></mesh>
      {/* swings */}
      <group position={[-3, 0, -1.5]}>
        {[-1.4, 1.4].map((x) => <mesh key={x} position={[x, 1.3, 0]} material={metal}><boxGeometry args={[0.12, 2.6, 0.12]} /></mesh>)}
        <mesh position={[0, 2.6, 0]} material={metal}><boxGeometry args={[3, 0.12, 0.12]} /></mesh>
        {[-0.6, 0.6].map((x) => <mesh key={'s' + x} position={[x, 0.6, 0]} material={wood}><boxGeometry args={[0.5, 0.06, 0.25]} /></mesh>)}
      </group>
      {/* slide */}
      <group position={[3, 0, -1.5]}>
        <mesh position={[0, 0.9, -0.8]} material={mat('#2d6cdf')}><boxGeometry args={[0.8, 1.8, 0.8]} /></mesh>
        <mesh position={[0, 0.85, 0.6]} rotation-x={0.75} material={mat('#f2b81e')}><boxGeometry args={[0.7, 0.08, 2.4]} /></mesh>
      </group>
      {/* benches for the grandparents */}
      {[-3.5, 3.5].map((x) => (
        <group key={x} position={[x, 0, 3]}>
          <mesh position={[0, 0.45, 0]} material={wood}><boxGeometry args={[1.8, 0.1, 0.5]} /></mesh>
          <mesh position={[0, 0.8, -0.22]} material={wood}><boxGeometry args={[1.8, 0.5, 0.08]} /></mesh>
        </group>
      ))}
      {[[-5.2, -3.6], [5.2, -3.6], [0, -3.8]].map(([x, z], i) => (
        <group key={'tr' + i} position={[x, 0, z]}>
          <mesh position={[0, 1, 0]} material={mat('#7a5230')}><cylinderGeometry args={[0.15, 0.2, 2, 6]} /></mesh>
          <mesh position={[0, 2.6, 0]} material={mat('#3f9a3a')}><icosahedronGeometry args={[1.2, 0]} /></mesh>
        </group>
      ))}
      <group position={[0, 6.2, 0]} scale={1.7}>
        <Tag text="PARQUE PARA NIÑOS Y ABUELOS" y={0.6} color="#ffffff" bg="#2a9d4b" big />
        <Tag text="IMPUESTOS BAJADOS" y={-0.2} color="#1a2233" bg="#ffd23d" big />
      </group>
    </group>
  )
}
