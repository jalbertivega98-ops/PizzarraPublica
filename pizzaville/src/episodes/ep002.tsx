// EPISODIO 2 — «87 vecinos»: elecciones (Oliver vs Thiago), oficios, estadio en obras,
// castillo de Toni y una isla nueva en el lago para África y Asia.
// El mundo es persistente: los 62 vecinos del ep001 siguen en las mismas parcelas.
import { useMemo, useRef } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { Text } from '@react-three/drei'
import * as THREE from 'three'
import { clock, ease, seg } from '../engine/clock'
import { evalCam, world, type CamKey } from '../engine/director'
import { useLines, mouthAt, speakingAt } from '../engine/voice'
import { Character, PIZZ_LOOK, WORKER_LOOK, lookFromSeed, newState, type CharState, type Look } from '../scene/Character'
import { House, houseSpecFromSeed, type HouseSpec } from '../scene/House'
import { ConstructionSite } from '../scene/Construction'
import { Flag, flagTexture } from '../scene/Flag'
import { PizzHome, HOME_Y } from '../scene/PizzHome'
import { NameTag } from '../scene/Town'
import { mat } from '../scene/materials'
import { hashString } from '../world/rng'
import { extraReserved, footprintHeight, valid } from '../world/plots'
import { heightAt, LAKE } from '../world/terrain'
import { europeLots, americaLots, type Lot } from './ep001layout'
import VECINOS from '../../episodios/ep002/vecinos.csv?raw'
import { Tag, BigLabel, Bridge, Fence, PlotMarker } from './parts'

export const EP002 = {
  id: 'ep002',
  duration: 61.0,
  script: [
    { id: 'l01', at: 0.3, text: '¡Ochenta y siete vecinos! ¡Y diecinueve países!' },
    { id: 'l02', at: 3.52, text: 'Pero tenemos un problema... ¡todos queréis mandar!' },
    { id: 'l03', at: 6.82, text: 'Oliver, desde España, quiere ser presidente. Y Thiago, desde Argentina... ¡también!' },
    { id: 'l04', at: 12.19, text: 'Así que... ¡elecciones en Pizzaville! Europa contra América.' },
    { id: 'l05', at: 16.3, text: 'Mientras, la ciudad se pone a trabajar: Gian y SoyAngelix, policías. Ezequiel, sheriff. Y Álvaro, el cura del pueblo.' },
    { id: 'l06', at: 23.78, text: 'Gerard y Gerardo abren restaurante... y Matheus también, ¡con su perrito Marley!' },
    { id: 'l07', at: 28.39, text: 'Hugo quiere ser futbolista y Rafael, desde Chile, monta el club. ¡Toca construir un estadio!' },
    { id: 'l08', at: 33.83, text: '¿Y Toni Castillo? Pidió un castillo... ¡y aquí lo tiene!' },
    { id: 'l09', at: 37.34, text: '¡Y atención! Llegan Marruecos y Líbano: ¡África y Asia! Y no tienen orilla... así que les estamos haciendo una isla nueva.' },
    { id: 'l10', at: 45.24, text: 'Europa sigue ganando: ¡cuarenta y nueve a treinta y seis!' },
    { id: 'l11', at: 48.46, text: 'Ahora vota: comenta OLIVER o THIAGO. Quien tenga más votos será el primer presidente de Pizzaville.' },
    { id: 'l12', at: 54.37, text: 'Y si eres nuevo: tu nombre, tu país y qué quieres ser. ¡Etiqueta a alguien de tu país!' },
  ],
}
const A = Object.fromEntries(EP002.script.map((l) => [l.id, l.at])) as Record<string, number>

// ---------------------------------------------------------------- data & layout
const ISO: Record<string, string> = {
  España: 'es', México: 'mx', Argentina: 'ar', Colombia: 'co', Chile: 'cl', Bulgaria: 'bg', Perú: 'pe', Venezuela: 've', Bolivia: 'bo', Cuba: 'cu',
  'República Dominicana': 'do', Uruguay: 'uy', Brasil: 'br', Líbano: 'lb', Guatemala: 'gt', 'Costa Rica': 'cr', Marruecos: 'ma', Ecuador: 'ec', 'El Salvador': 'sv',
}
const EUROPE = new Set(['España', 'Bulgaria'])
const ISLAND = new Set(['Marruecos', 'Líbano'])
type Person = { name: string; country: string; iso: string; wish: string; job: string; handle: string }
function people(): Person[] {
  return VECINOS.split(/\r?\n/).slice(1).filter((l) => l.trim()).map((l) => {
    const c = l.split(',')
    return { name: c[0], country: c[1], iso: ISO[c[1]] ?? 'es', handle: c[3] ?? '', wish: c[4] ?? '', job: (c[c.length - 1] ?? '').trim() }
  })
}

type Item = {
  key: string; lot: Lot; spec: HouseSpec; iso: string; name?: string; label?: string; sign?: string; signColor?: string
  pool?: boolean; fence?: boolean; castle?: boolean; isNew?: boolean; delay: number; person?: Person
}

const PZ = { x: 0.15, z: 5.3 }
const OLD = 62 // vecinos del ep001: ya construidos, mismas parcelas

function riverSpot(x0: number): Lot {
  for (let z = -36; z < -10; z += 2) if (valid(x0, z)) return { x: x0, z, y: footprintHeight(x0, z), rot: Math.PI }
  return { x: x0, z: -30, y: footprintHeight(x0, -30), rot: Math.PI }
}

// island in the lake for Africa & Asia
export const ISLE = { x: LAKE.x - 6, z: LAKE.z + 4, r: 17, y: 0.55 }
export const STADIUM = { x: -95, z: 85, rx: 26, rz: 18 }

const spec = (seed: number, o: Partial<HouseSpec> = {}) => ({ ...houseSpecFromSeed(seed), ...o })

function wishStyle(w: string) {
  let o: Partial<HouseSpec> = {}, label: string | undefined, pool = false, fence = false
  if (/rancho/.test(w)) { o = { w: 9, d: 6, floors: 1, wall: '#d9a066', roof: '#8a4b2a' }; fence = true; label = 'RANCHO' }
  if (/2 pisos|dos plantas/.test(w)) { o = { ...o, floors: 2 }; label = /pueblo/.test(w) ? 'CASA DE PUEBLO' : '2 PISOS' }
  if (/mansi/.test(w)) { o = { w: 9.5, d: 7, floors: 2, wall: '#ffffff', roof: '#3b3f4a', roofType: 'hip', balcony: true, porch: true }; pool = true; label = 'MANSIÓN + PISCINA' }
  else if (/piscina/.test(w)) { pool = true; label = 'CON PISCINA' }
  if (/moderna/.test(w)) { o = { floors: 2, wall: '#f5f5f5', roof: '#2f3540', roofType: 'hip' }; label = 'CASA MODERNA' }
  if (/lujosa/.test(w)) { o = { floors: 2, wall: '#fff8e8', roof: '#3b3f4a', roofType: 'hip', balcony: true, porch: true }; label = 'CASA DE LUJO' }
  if (/granja/.test(w)) { o = { wall: '#b5432f', roof: '#5a3a2a' }; fence = true; label = 'GRANJA DE GALLINAS' }
  if (/huerto/.test(w)) { fence = true; label = 'HUERTO + TRACTOR' }
  if (/furgo/.test(w)) label = 'FURGO + PERROS'
  if (/tecnolog/.test(w)) { o = { wall: '#dfe8f2', roof: '#2d6cdf' }; label = 'CASA TECNOLÓGICA' }
  if (/chalet/.test(w) && !pool) label = 'CHALET'
  if (/batall/.test(w)) label = '¡UN BATALLÓN!'
  if (/caballo/.test(w)) { fence = true; label = 'CASA + CABALLO' }
  return { o, label, pool, fence }
}

const JOB_LABEL: Record<string, string> = {
  granjero: 'GRANJERO', informático: 'INFORMÁTICO', cocinero: 'COCINERO', general: 'GENERAL', quiosco: 'QUIOSCO', futbolista: 'FUTBOLISTA', 'club de fútbol': 'PRESIDENTE DEL CLUB',
}

function build() {
  const ps = people()
  const eu = europeLots(80), am = americaLots(52)
  const items: Item[] = []
  const infra: [number, string, string, Partial<HouseSpec>][] = [
    [1, 'SUPERMERCADO', '#2e8b57', { w: 10, d: 7, floors: 1, wall: '#f2f0e6', roof: '#2e8b57', roofType: 'hip' }],
    [3, 'ESCUELA', '#d9822b', { w: 10.5, d: 7, floors: 2, wall: '#f3d9a4', roof: '#a94b32', roofType: 'gable', balcony: false }],
    [5, 'CENTRO DE SALUD', '#d23c3c', { w: 9.5, d: 7, floors: 2, wall: '#ffffff', roof: '#7a8a99', roofType: 'hip', balcony: false }],
  ]
  for (const [i, sign, col, o] of infra) items.push({ key: sign, lot: eu[i], spec: spec(900 + i, o), iso: '', sign, signColor: col, delay: -9 })
  const used = new Set(infra.map((x) => x[0]))
  let ei = 0, ai = 0
  const nextEu = () => { while (used.has(ei)) ei++; used.add(ei); return eu[ei++] }
  const amFixed: Record<string, number> = { Fernando: 0, Kiker: 2, Thiago: 5 }
  const amUsed = new Set(Object.values(amFixed).concat([30]))
  const nextAm = () => { while (amUsed.has(ai)) ai++; amUsed.add(ai); return am[ai++] }
  let k = 0, isle = 0
  ps.forEach((p, idx) => {
    const isNew = idx >= OLD
    const seed = hashString(p.name + p.country)
    let lot: Lot
    let { o, label, pool, fence } = wishStyle(p.wish.toLowerCase())
    let sign: string | undefined, castle = false
    if (p.name === 'Rodrigo') lot = riverSpot(-78)
    else if (p.name === 'Aleky') { lot = eu[7]; used.add(7); sign = 'PELUQUERÍA ALEKY'; o = { wall: '#f7c6d9', roof: '#7d4e9e' } }
    else if (p.country === 'Brasil') lot = am[30]
    else if (amFixed[p.name] !== undefined) lot = am[amFixed[p.name]]
    else if (ISLAND.has(p.country)) {
      const a = isle++ * Math.PI - 0.5
      const x = ISLE.x + Math.cos(a) * 6.5, z = ISLE.z + Math.sin(a) * 6.5
      lot = { x, z, y: ISLE.y, rot: Math.atan2(Math.cos(a), Math.sin(a)) }
    } else lot = EUROPE.has(p.country) ? nextEu() : nextAm()
    if (p.country === 'Brasil') label = 'BARRIO BRASIL'
    if (/castillo/.test(p.wish)) { castle = true; label = 'CASTILLO DE TONI' }
    if (isNew && JOB_LABEL[p.job]) label = JOB_LABEL[p.job]
    if (p.job === 'granjero') { fence = true; o = { wall: '#b5432f', roof: '#5a3a2a' } }
    items.push({ key: p.name + '_' + p.handle, lot, spec: spec(seed, o), iso: p.iso, name: p.name, label, sign, signColor: '#c2185b', pool, fence, castle, isNew,
      delay: isNew ? 0.35 + (k++) * 0.07 : -9, person: p })
  })
  // job buildings (new this episode)
  const jobs: [string, string, Partial<HouseSpec>][] = [
    ['COMISARÍA', '#1f4fa8', { w: 10, d: 7, floors: 2, wall: '#e9eef7', roof: '#1f3a6b', roofType: 'hip', balcony: false }],
    ['IGLESIA', '#7a5a3a', { w: 7.5, d: 9, floors: 2, wall: '#f4ecd8', roof: '#8a3b2a', roofType: 'gable', balcony: false, porch: false }],
    ['RESTAURANTE GERARD', '#d23c3c', { w: 9, d: 7, floors: 1, wall: '#fff3d6', roof: '#c0392b', porch: true }],
    ['RESTAURANTE GERARDO', '#e07b1f', { w: 9, d: 7, floors: 1, wall: '#fbe3c2', roof: '#2e7d4f', porch: true }],
  ]
  const job: Record<string, Item> = {}
  // the two restaurants face each other across the road: take the first free pair at the same road point
  const pair = (() => { for (let i = 0; i + 1 < eu.length; i++) if (!used.has(i) && !used.has(i + 1) && Math.abs(eu[i].x - eu[i + 1].x) < 6 && i > ei) return i; return ei + 4 })()
  const jobLot: Record<string, Lot> = {}
  used.add(pair); used.add(pair + 1)
  jobLot['RESTAURANTE GERARD'] = eu[pair]; jobLot['RESTAURANTE GERARDO'] = eu[pair + 1]
  jobLot['COMISARÍA'] = nextEu(); jobLot['IGLESIA'] = nextEu()
  for (const [s, col, o] of jobs) {
    const it: Item = { key: s, lot: jobLot[s], spec: spec(hashString(s), o), iso: '', sign: s, signColor: col, isNew: true, delay: 0.5 + (k++) * 0.07 }
    items.push(it); job[s] = it
  }
  const sheriff: Item = { key: 'SHERIFF', lot: nextAm(), spec: spec(77, { w: 8.5, d: 6.5, floors: 1, wall: '#c98b55', roof: '#6b3f22', porch: true }), iso: '', sign: 'OFICINA DEL SHERIFF', signColor: '#8a5a2b', isNew: true, delay: 0.5 + (k++) * 0.07 }
  // Matheus' restaurant: the free American lot closest to Barrio Brasil
  let bi = -1, bd = 1e9
  am.forEach((l, i) => { if (!amUsed.has(i)) { const d = Math.hypot(l.x - am[30].x, l.z - am[30].z); if (d < bd) { bd = d; bi = i } } })
  amUsed.add(bi)
  const resBr: Item = { key: 'RESTAURANTE MATHEUS', lot: am[bi], spec: spec(55, { w: 9, d: 7, floors: 1, wall: '#e8f5e0', roof: '#2a9d4b', porch: true }), iso: '', sign: 'RESTAURANTE MATHEUS', signColor: '#2a9d4b', isNew: true, delay: 0.5 + (k++) * 0.07 }
  items.push(sheriff, resBr)
  job['SHERIFF'] = sheriff; job['RESTAURANTE MATHEUS'] = resBr
  const byName: Record<string, Item> = {}
  for (const it of items) if (it.name && !byName[it.name]) byName[it.name] = it
  for (const it of items) if (it.name) byName[it.name + '@' + it.person!.handle] = it
  let fi = ei; while (used.has(fi)) fi++
  const free = eu[fi + 2] ?? eu[eu.length - 1]
  for (const it of items) extraReserved.push({ x: it.lot.x, z: it.lot.z, r: 9 })
  for (const bx of BRIDGES) extraReserved.push({ x: bx, z: -60, r: 8 })
  extraReserved.push({ x: STADIUM.x, z: STADIUM.z, r: 36 })
    return { items, byName, job, free }
}
const BRIDGES = [-45, 20, 85]
const LAYOUT = build()
;(globalThis as any).__ep2 = LAYOUT

const F = (l: Lot) => [Math.sin(l.rot), Math.cos(l.rot)]
function at(l: Lot, f: number, r: number, y: number): [number, number, number] {
  const [fx, fz] = F(l)
  return [l.x + fx * f + fz * r, l.y + y, l.z + fz * f - fx * r]
}
const look = (l: Lot, y = 2.6): [number, number, number] => [l.x, l.y + y, l.z]

// campaign posters at both ends of the central bridge, facing east
const POSTER = {
  oliver: { x: 16.5, z: -47, name: 'OLIVER', iso: 'es', bg: '#ffd23d', fg: '#1a2233' },
  thiago: { x: 16.5, z: -75, name: 'THIAGO', iso: 'ar', bg: '#3fa9f5', fg: '#ffffff' },
}
const DECK = 2.53 // top of the bridge deck
const posterLot = (p: { x: number; z: number }): Lot => ({ x: p.x, z: p.z, y: DECK, rot: Math.PI / 2 })

// ---------------------------------------------------------------- camera
function cameraKeys(): CamKey[] {
  const H = HOME_Y + 1.6
  const b = LAYOUT.byName, j = LAYOUT.job
  const shot = (t0: number, t1: number, l: Lot, d = 13, r = 4, y = 4.5, cut = true): CamKey[] => [
    { t: t0, p: at(l, d + 9, r * 1.6, y + 3.5), l: look(l, 3.2), fov: 44, cut },
    { t: t1, p: at(l, d + 5, r * 1.2, y + 2.5), l: look(l, 3.0), fov: 42, e: 'linear' },
  ]
  const po = posterLot(POSTER.oliver), pt = posterLot(POSTER.thiago)
  const pshot = (t0: number, t1: number, l: Lot, side: number): CamKey[] => [
    { t: t0, p: [l.x + 15, l.y + 3.6, l.z + side * 6], l: [l.x + 2, l.y + 2.6, l.z], fov: 44, cut: true },
    { t: t1, p: [l.x + 11, l.y + 3.0, l.z + side * 3.5], l: [l.x + 2, l.y + 2.5, l.z], fov: 42, e: 'linear' },
  ]
  const S = STADIUM, I = ISLE, fl = LAYOUT.free
  const rg = j['RESTAURANTE GERARD'].lot
  return [
    // S1 hook: high aerial dives over the grown town while the new houses pop
    { t: 0, p: [-60, 190, 230], l: [0, 0, -25], fov: 50 },
    { t: 3.42, p: [25, 55, 85], l: [0, 2, -10], fov: 48, e: 'inOut' },
    // S2 «todos queréis mandar»: Pizz at his door
    { t: A.l02, p: [1.6, 2.7, 10.4], l: [PZ.x, H - 0.05, PZ.z], fov: 38, cut: true },
    { t: A.l03 - 0.1, p: [0.7, 2.55, 8.9], l: [PZ.x, H - 0.05, PZ.z], fov: 34, e: 'linear' },
    // S3 the two candidates at their posters
    ...pshot(A.l03, A.l03 + 2.58, po, 1),
    ...pshot(A.l03 + 2.63, A.l04 - 0.1, pt, -1),
    // S4 elections: the central bridge with both posters
    { t: A.l04, p: [44, 12, -16], l: [16.5, 4, -61], fov: 46, cut: true },
    { t: A.l05 - 0.1, p: [38, 9, -24], l: [16.5, 4, -61], fov: 46, e: 'linear' },
    // S5 the town gets to work
    { t: A.l05, p: [-70, 48, 85], l: [0, 0, 5], fov: 50, cut: true },
    { t: A.l05 + 2.15, p: [40, 48, 90], l: [0, 0, 5], fov: 50, e: 'linear' },
    ...shot(A.l05 + 2.2, A.l05 + 3.9, j['COMISARÍA'].lot, 13, 4),
    ...shot(A.l05 + 3.95, A.l05 + 5.38, j['SHERIFF'].lot, 13, -4),
    ...shot(A.l05 + 5.43, A.l06 - 0.1, j['IGLESIA'].lot, 19, 4, 6),
    // S6 restaurants, Matheus and Marley
    { t: A.l06, p: at(rg, -12, 9, 24), l: at(rg, 13, 0, 1), fov: 48, cut: true },
    { t: A.l06 + 1.95, p: at(rg, -8, 5, 19), l: at(rg, 13, 0, 1), fov: 48, e: 'linear' },
    ...shot(A.l06 + 2.0, A.l07 - 0.1, j['RESTAURANTE MATHEUS'].lot, 9, 1, 3),
    // S7 Hugo & Rafael at the stadium works, then the stadium
    { t: A.l07, p: [S.x + 2, heightAt(S.x, S.z + S.rz + 26) + 4.5, S.z + S.rz + 27], l: [S.x + 0.5, heightAt(S.x, S.z + S.rz + 13) + 3.5, S.z + S.rz + 10], fov: 44, cut: true },
    { t: A.l07 + 3.28, p: [S.x + 0.6, heightAt(S.x, S.z + S.rz + 22) + 3.8, S.z + S.rz + 22], l: [S.x + 0.5, heightAt(S.x, S.z + S.rz + 13) + 3.5, S.z + S.rz + 8], fov: 44, e: 'linear' },
    { t: A.l07 + 3.33, p: [S.x - 55, 42, S.z + 50], l: [S.x, 2, S.z], fov: 48, cut: true },
    { t: A.l08 - 0.1, p: [S.x + 45, 38, S.z + 55], l: [S.x, 2, S.z], fov: 48, e: 'linear' },
    // S8 Toni's castle
    ...shot(A.l08, A.l09 - 0.1, b.Toni.lot, 16, 6, 7),
    // S9 «¡atención!» Pizz, then the island in the lake
    { t: A.l09, p: [1.2, 2.6, 9.6], l: [PZ.x, H - 0.05, PZ.z], fov: 36, cut: true },
    { t: A.l09 + 1.15, p: [0.6, 2.5, 8.6], l: [PZ.x, H - 0.05, PZ.z], fov: 33, e: 'linear' },
    { t: A.l09 + 1.21, p: [I.x - 70, 30, I.z + 55], l: [I.x, 2, I.z], fov: 46, cut: true },
    { t: A.l09 + 4.5, p: [I.x - 28, 14, I.z + 26], l: [I.x, 2.5, I.z], fov: 46, e: 'inOut' },
    { t: A.l10 - 0.1, p: [I.x + 6, 11, I.z + 30], l: [I.x, 2.5, I.z], fov: 46, e: 'linear' },
    // S10 the score: high aerial over the three regions
    { t: A.l10, p: [-70, 170, 170], l: [60, 0, -30], fov: 52, cut: true },
    { t: A.l11 - 0.1, p: [230, 170, 170], l: [150, 0, -20], fov: 52, e: 'linear' },
    // S11 vote: back to the bridge, low between the posters
    { t: A.l11, p: [42, 32, -104], l: [16.5, 3.5, -61], fov: 46, cut: true },
    { t: A.l12 - 0.1, p: [35, 25, -95], l: [16.5, 3.5, -61], fov: 46, e: 'linear' },
    // S12 Pizz asks, then the free plot, then up and away
    { t: A.l12, p: [1.4, 2.6, 10.0], l: [PZ.x, H - 0.05, PZ.z], fov: 38, cut: true },
    { t: A.l12 + 3.1, p: [0.5, 2.5, 8.6], l: [PZ.x, H - 0.05, PZ.z], fov: 34, e: 'linear' },
    { t: A.l12 + 3.15, p: [fl.x - 30, fl.y + 13, fl.z + 14], l: [fl.x + 8, fl.y + 3, fl.z - 2], fov: 50, cut: true },
    { t: A.l12 + 5.3, p: [fl.x - 24, fl.y + 11, fl.z + 11], l: [fl.x + 8, fl.y + 3, fl.z - 2], fov: 50, e: 'linear' },
    { t: EP002.duration, p: [80, 170, 220], l: [40, 0, -25], fov: 52, e: 'inOut' },
  ]
}

// ---------------------------------------------------------------- characters
const tint = (seed: number, top: string, extra: Partial<Look> = {}): Look => {
  const c = new THREE.Color(top)
  return { ...lookFromSeed(seed), top, topDark: '#' + c.multiplyScalar(0.78).getHexString(), ...extra }
}
type Cast = { key: string; look: Look; pos: () => [number, number, number]; ry: number; action: 'wave' | 'celebrate' | 'hammer' | 'point'; from: number }
function cast(): Cast[] {
  const b = LAYOUT.byName, j = LAYOUT.job
  const front = (l: Lot, f: number, r: number) => () => at(l, f, r, 0)
  const po = posterLot(POSTER.oliver), pt = posterLot(POSTER.thiago)
  const S = STADIUM, sy = (x: number, z: number) => heightAt(x, z)
  const out: Cast[] = [
    { key: 'Oliver', look: tint(11, '#ffd23d'), pos: () => [19.4, DECK, po.z + 1.6], ry: Math.PI / 2, action: 'celebrate', from: 0 },
    { key: 'Thiago', look: tint(12, '#3fa9f5'), pos: () => [19.4, DECK, pt.z - 1.6], ry: Math.PI / 2, action: 'celebrate', from: 0 },
    { key: 'Gian', look: tint(13, '#1f3a6b', { pants: '#1c2533' }), pos: front(j['COMISARÍA'].lot, 6.2, -2), ry: j['COMISARÍA'].lot.rot, action: 'wave', from: 0 },
    { key: 'SoyAngelix', look: tint(14, '#1f3a6b', { pants: '#1c2533' }), pos: front(j['COMISARÍA'].lot, 6.2, 2), ry: j['COMISARÍA'].lot.rot, action: 'wave', from: 0 },
    { key: 'Ezequiel', look: tint(15, '#8a5a2b'), pos: front(j['SHERIFF'].lot, 5.6, 0), ry: j['SHERIFF'].lot.rot, action: 'wave', from: 0 },
    { key: 'Álvaro', look: tint(16, '#1c1c1f', { pants: '#1c1c1f' }), pos: front(j['IGLESIA'].lot, 6.8, 0), ry: j['IGLESIA'].lot.rot, action: 'wave', from: 0 },
    { key: 'Gerard', look: tint(17, '#ffffff'), pos: front(j['RESTAURANTE GERARD'].lot, 5.8, 0), ry: j['RESTAURANTE GERARD'].lot.rot, action: 'wave', from: 0 },
    { key: 'Gerardo', look: tint(18, '#ffffff'), pos: front(j['RESTAURANTE GERARDO'].lot, 5.8, 0), ry: j['RESTAURANTE GERARDO'].lot.rot, action: 'wave', from: 0 },
    { key: 'Matheus', look: tint(19, '#2a9d4b'), pos: front(j['RESTAURANTE MATHEUS'].lot, 5.6, -1), ry: j['RESTAURANTE MATHEUS'].lot.rot, action: 'wave', from: 0 },
    { key: 'Hugo', look: tint(20, '#d23c3c', { pants: '#f2efe6' }), pos: () => [S.x - 0.9, sy(S.x - 0.9, S.z + S.rz + 13), S.z + S.rz + 13], ry: 0, action: 'celebrate', from: 0 },
    { key: 'Rafael', look: tint(21, '#2d6cdf'), pos: () => [S.x + 1.3, sy(S.x + 1.3, S.z + S.rz + 13), S.z + S.rz + 13], ry: 0, action: 'wave', from: 0 },
    { key: 'Toni', look: tint(22, '#7d4e9e'), pos: front(b.Toni.lot, 8.5, 0), ry: b.Toni.lot.rot, action: 'wave', from: 0 },
    { key: 'Sofian', look: tint(23, '#c1272d'), pos: () => [ISLE.x - 3, ISLE.y, ISLE.z + 9], ry: 0, action: 'wave', from: 0 },
    { key: 'Youssef', look: tint(24, '#00a651'), pos: () => [ISLE.x + 3, ISLE.y, ISLE.z + 9], ry: 0, action: 'wave', from: 0 },
  ]
  // workers on the island and at the stadium
  const W = (key: string, x: number, z: number, ry: number) => out.push({ key, look: WORKER_LOOK(hashString(key)), pos: () => [x, key.startsWith('wi') ? ISLE.y : sy(x, z), z], ry, action: 'hammer', from: 0 })
  W('wi1', ISLE.x - 9, ISLE.z - 1, 1.2); W('wi2', ISLE.x + 8, ISLE.z + 3, -1.4); W('wi3', ISLE.x + 1, ISLE.z - 9, 0.3)
  W('ws1', S.x - 18, S.z + 8, 2.2); W('ws2', S.x + 16, S.z + 10, -2.3); W('ws3', S.x + 6, S.z - 14, 0.4)
  return out
}

// ---------------------------------------------------------------- component
export function Ep002() {
  const { camera } = useThree()
  const lines = useMemo(() => useLines(EP002.id, EP002.script), [])
  const keys = useMemo(cameraKeys, [])
  const pizz = useMemo(newState, [])
  const P = useMemo(() => new THREE.Vector3(), [])
  const L = useMemo(() => new THREE.Vector3(), [])
  const camPos = useMemo(() => new THREE.Vector3(), [])
  const labels = useRef<THREE.Group>(null!)
  const marker = useRef<THREE.Group>(null!)
  const people = useMemo(cast, [])
  const states = useMemo(() => people.map(() => newState()), [])
  const T = () => clock.t

  useMemo(() => {
    const pv = (window as any).__pv
    if (!pv) return
    pv.info = () => {
      const sfx: { type: string; at: number; g?: number }[] = [{ type: 'whoosh', at: 0.0, g: 0.6 }]
      LAYOUT.items.forEach((it, i) => { if (it.isNew && i % 2 === 0) sfx.push({ type: 'pop', at: 0.4 + it.delay + 0.3, g: 0.22 }) })
      for (const k of keys) if (k.cut && k.t > 3) sfx.push({ type: 'whoosh', at: k.t - 0.05, g: 0.3 })
      sfx.push(
        { type: 'chime', at: A.l04 + 0.9, g: 0.6 }, { type: 'chime', at: A.l08 + 2.3, g: 0.5 }, { type: 'chime', at: A.l09 + 0.2, g: 0.6 },
        { type: 'chime', at: A.l10 + 1.0, g: 0.6 }, { type: 'chime', at: A.l11 + 1.2, g: 0.6 },
      )
      return { id: EP002.id, duration: EP002.duration, lines: lines.map((l) => ({ id: l.id, at: l.at, dur: l.dur, text: l.text, words: l.words, hasAudio: l.hasAudio })), sfx }
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
    pizz.lookAt = camPos; pizz.action = 'none'; pizz.actionW = 0; pizz.smile = 0.8; pizz.brows = 0
    const l02 = A.l02, l09 = A.l09, l12 = A.l12
    if (t > l02 && t < l02 + 1.4) { pizz.action = 'shrug'; pizz.actionT = t - l02; pizz.actionW = seg(t, l02, l02 + 0.2) * (1 - seg(t, l02 + 1.2, l02 + 1.4)) }
    else if (t > l02 + 1.4 && t < A.l03) { pizz.action = 'surprise'; pizz.actionT = t - l02 - 1.4; pizz.actionW = seg(t, l02 + 1.4, l02 + 1.6) }
    else if (t > l09 && t < l09 + 1.2) { pizz.action = 'surprise'; pizz.actionT = t - l09; pizz.actionW = 1 }
    else if (t > l12 && t < l12 + 1.8) { pizz.action = 'point'; pizz.actionT = t; pizz.actionW = seg(t, l12, l12 + 0.3) * (1 - seg(t, l12 + 1.5, l12 + 1.8)) }
    else if (speakingAt(lines, t)) { pizz.action = 'talk'; pizz.actionT = t; pizz.actionW = 0.85 }
    pizz.mouth = mouthAt(lines, t)

    people.forEach((c, i) => {
      const st = states[i]
      const [x, y, z] = c.pos()
      st.x = x; st.y = y; st.z = z; st.speed = 0; st.ry = c.ry
      st.lookAt = c.action === 'hammer' ? null : camPos
      st.visible = t >= c.from
      st.action = c.action; st.actionT = t + i * 0.37; st.actionW = 1
    })

    labels.current.visible = (t > A.l10 && t < A.l11)
    marker.current.visible = t > A.l12 + 3.1
    marker.current.scale.setScalar(Math.max(0.001, ease.outBack(seg(t, A.l12 + 3.2, A.l12 + 3.7))) * 1.5)
  }, -1)

  const prog = (it: Item) => it.isNew ? () => seg(T(), 0.4 + it.delay, 1.1 + it.delay) : () => 1
  const fl = LAYOUT.free
  const isleProg = () => 0.3 + 0.32 * seg(T(), A.l09 + 1.2, A.l10)
  return (
    <group>
      <PizzHome />
      <Character look={PIZZ_LOOK} state={pizz} />
      {people.map((c, i) => <Character key={c.key} look={c.look} state={states[i] as CharState} />)}
      {LAYOUT.items.filter((it) => !ISLAND.has(it.person?.country ?? '')).map((it) => (
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
        </group>
      ))}
      {LAYOUT.items.map((it) => (
        <group key={'t' + it.key} position={[it.lot.x, it.lot.y + (it.castle ? 12.5 : it.spec.wallH * it.spec.floors + 3.8), it.lot.z]} scale={1.6}>
          {it.name && <NameTag name={it.name} iso={it.iso} />}
          {it.label && <Tag text={it.label} y={-0.62} color="#ffd23d" />}
          {it.sign && <Tag text={it.sign} y={it.name ? 0.75 : 0} color="#ffffff" bg={it.signColor} big />}
        </group>
      ))}
      {BRIDGES.map((bx) => <Bridge key={bx} x={bx} />)}
      <Poster {...POSTER.oliver} />
      <Poster {...POSTER.thiago} />
      <Stadium />
      <Island getProgress={isleProg} items={LAYOUT.items.filter((it) => ISLAND.has(it.person?.country ?? ''))} />
      <group ref={labels}>
        <BigLabel text="EUROPA" position={[0, 22, 22]} color="#ffd23d" />
        <BigLabel text="AMÉRICA" position={[10, 26, -100]} color="#7fe0ff" />
        <BigLabel text="ÁFRICA · ASIA" position={[ISLE.x, 24, ISLE.z]} color="#7dffa8" />
      </group>
      <group ref={marker} position={[fl.x, fl.y + 4, fl.z]}>
        <PlotMarker />
      </group>
    </group>
  )
}

// ---------------------------------------------------------------- props
function FlagPost({ iso, h = 4 }: { iso: string; h?: number }) {
  return (
    <group>
      <mesh position={[0, h / 2, 0]} material={mat('#d9d9d9', { rough: 0.4 })}><cylinderGeometry args={[0.06, 0.06, h, 6]} /></mesh>
      <group position={[0, h - 0.05, 0]}><Flag iso={iso} /></group>
    </group>
  )
}

function Poster({ x, z, name, iso, bg, fg }: { x: number; z: number; name: string; iso: string; bg: string; fg: string }) {
  const y = DECK
  const fm = useMemo(() => new THREE.MeshBasicMaterial({ map: flagTexture(iso), toneMapped: false }), [iso])
  return (
    <group position={[x, y, z]} rotation-y={Math.PI / 2}>
      {[-2.6, 2.6].map((s) => (
        <mesh key={s} position={[s, 1.6, -0.1]} material={mat('#6e4a2f')} castShadow><boxGeometry args={[0.22, 3.2, 0.22]} /></mesh>
      ))}
      <mesh position={[0, 4.2, -0.05]} material={mat('#1a2233')} castShadow><boxGeometry args={[6.4, 3.6, 0.15]} /></mesh>
      <mesh position={[0, 4.2, 0.04]} material={mat(bg, { rough: 0.6, emissive: bg, ei: 0.25 })}><planeGeometry args={[6.1, 3.3]} /></mesh>
      <mesh position={[-2.0, 4.95, 0.06]} material={fm}><planeGeometry args={[1.5, 1.1]} /></mesh>
      <Text font="/fonts/lilita.woff" fontSize={0.62} color={fg} anchorX="left" anchorY="middle" position={[-1.05, 5.0, 0.07]}>VOTA A</Text>
      <Text font="/fonts/lilita.woff" fontSize={1.25} color={fg} outlineWidth={0.05} outlineColor="#1a2233" anchorX="center" anchorY="middle" position={[0, 3.75, 0.07]}>{name}</Text>
      <Text font="/fonts/fredoka600.woff" fontSize={0.36} color={fg} anchorX="center" anchorY="middle" position={[0, 2.85, 0.07]}>PRESIDENTE DE PIZZAVILLE</Text>
    </group>
  )
}

function Castle({ getProgress }: { getProgress: () => number }) {
  const g = useRef<THREE.Group>(null!)
  useFrame(() => { const p = getProgress(); g.current.visible = p > 0.01; g.current.scale.set(1, Math.max(0.01, ease.outBack(p)), 1) })
  const stone = mat('#c9c2b4', { rough: 0.95 }), dark = mat('#9b9384', { rough: 0.95 }), roof = mat('#7d4e9e', { rough: 0.7 })
  const towers: [number, number][] = [[-4.5, -4.5], [4.5, -4.5], [-4.5, 4.5], [4.5, 4.5]]
  return (
    <group ref={g}>
      {/* walls */}
      {[[0, -4.5, 9, 0.8], [0, 4.5, 9, 0.8], [-4.5, 0, 0.8, 9], [4.5, 0, 0.8, 9]].map(([x, z, w, d], i) => (
        <mesh key={i} position={[x, 2, z]} material={stone} castShadow receiveShadow><boxGeometry args={[w, 4, d]} /></mesh>
      ))}
      {/* battlements */}
      {Array.from({ length: 8 }, (_, i) => -3.5 + i).flatMap((v) => [[v, -4.5], [v, 4.5], [-4.5, v], [4.5, v]]).filter((_, i) => i % 2 === 0).map(([x, z], i) => (
        <mesh key={'b' + i} position={[x, 4.35, z]} material={stone}><boxGeometry args={[0.6, 0.7, 0.9]} /></mesh>
      ))}
      {/* keep */}
      <mesh position={[0, 4, 0]} material={stone} castShadow><boxGeometry args={[4.4, 8, 4.4]} /></mesh>
      <mesh position={[0, 9.2, 0]} material={roof} castShadow><coneGeometry args={[3.4, 2.6, 4]} /></mesh>
      {towers.map(([x, z], i) => (
        <group key={'t' + i} position={[x, 0, z]}>
          <mesh position={[0, 3.2, 0]} material={stone} castShadow><cylinderGeometry args={[1.3, 1.4, 6.4, 12]} /></mesh>
          <mesh position={[0, 7.4, 0]} material={roof} castShadow><coneGeometry args={[1.7, 2.2, 12]} /></mesh>
        </group>
      ))}
      {/* gate */}
      <mesh position={[0, 1.3, 4.95]} material={mat('#5a3a22')}><boxGeometry args={[2, 2.6, 0.1]} /></mesh>
      <mesh position={[0, 2.6, 4.96]} rotation-x={Math.PI / 2} material={mat('#5a3a22')}><cylinderGeometry args={[1, 1, 0.1, 16, 1, false, 0, Math.PI]} /></mesh>
      {[-1.6, 1.6].map((x) => <mesh key={x} position={[x, 5.5, 2.25]} material={dark}><boxGeometry args={[0.5, 0.9, 0.1]} /></mesh>)}
    </group>
  )
}

function BellTower({ h, d }: { h: number; d: number }) {
  return (
    <group position={[0, 0, d / 2 - 1.2]}>
      <mesh position={[0, h + 1.6, 0]} material={mat('#f4ecd8', { rough: 0.9 })} castShadow><boxGeometry args={[2.2, 3.4, 2.2]} /></mesh>
      <mesh position={[0, h + 1.9, 1.11]} material={mat('#3a2a1a')}><planeGeometry args={[0.9, 1.2]} /></mesh>
      <mesh position={[0, h + 4.4, 0]} rotation-y={Math.PI / 4} material={mat('#8a3b2a')} castShadow><coneGeometry args={[1.8, 2.4, 4]} /></mesh>
      <mesh position={[0, h + 6.1, 0]} material={mat('#e8c547', { emissive: '#e8c547', ei: 0.3 })}><boxGeometry args={[0.14, 1.1, 0.14]} /></mesh>
      <mesh position={[0, h + 6.3, 0]} material={mat('#e8c547', { emissive: '#e8c547', ei: 0.3 })}><boxGeometry args={[0.6, 0.14, 0.14]} /></mesh>
    </group>
  )
}

function Terrace({ w, d }: { w: number; d: number }) {
  const cloth = mat('#ffffff', { rough: 0.7 }), leg = mat('#5a3a22')
  return (
    <group position={[0, 0, d / 2 + 2.6]}>
      {[-w / 2 + 1.2, w / 2 - 1.2].map((x) => (
        <group key={x} position={[x, 0, 0]}>
          <mesh position={[0, 0.75, 0]} material={cloth}><cylinderGeometry args={[0.65, 0.65, 0.06, 14]} /></mesh>
          <mesh position={[0, 0.37, 0]} material={leg}><cylinderGeometry args={[0.06, 0.06, 0.74, 6]} /></mesh>
          <mesh position={[0, 2.1, 0]} material={mat('#d23c3c', { rough: 0.7 })}><coneGeometry args={[1.3, 0.6, 8]} /></mesh>
          <mesh position={[0, 1.2, 0]} material={leg}><cylinderGeometry args={[0.04, 0.04, 1.8, 6]} /></mesh>
        </group>
      ))}
    </group>
  )
}

/** Marley, Matheus' small white dog: wags its tail and hops */
function Dog() {
  const g = useRef<THREE.Group>(null!)
  const tail = useRef<THREE.Mesh>(null!)
  useFrame(() => {
    const t = clock.t
    tail.current.rotation.y = Math.sin(t * 18) * 0.7
    g.current.position.y = Math.abs(Math.sin(t * 5)) * 0.12
  })
  const w = mat('#fbfbf7', { rough: 0.9 }), k = mat('#222222')
  return (
    <group ref={g} scale={1.2}>
      <mesh position={[0, 0.42, 0]} material={w} castShadow><boxGeometry args={[0.45, 0.36, 0.8]} /></mesh>
      <mesh position={[0, 0.72, 0.45]} material={w} castShadow><boxGeometry args={[0.38, 0.36, 0.36]} /></mesh>
      <mesh position={[0, 0.66, 0.66]} material={w}><boxGeometry args={[0.2, 0.16, 0.16]} /></mesh>
      <mesh position={[0, 0.7, 0.75]} material={k}><boxGeometry args={[0.08, 0.07, 0.04]} /></mesh>
      {[-0.1, 0.1].map((x) => <mesh key={x} position={[x, 0.8, 0.64]} material={k}><boxGeometry args={[0.05, 0.05, 0.02]} /></mesh>)}
      {[-0.15, 0.15].map((x) => <mesh key={'e' + x} position={[x, 0.92, 0.42]} material={mat('#eadfc8')}><boxGeometry args={[0.1, 0.2, 0.12]} /></mesh>)}
      {[[-0.15, 0.28], [0.15, 0.28], [-0.15, -0.28], [0.15, -0.28]].map(([x, z], i) => (
        <mesh key={'l' + i} position={[x, 0.13, z]} material={w}><boxGeometry args={[0.1, 0.26, 0.1]} /></mesh>
      ))}
      <mesh ref={tail} position={[0, 0.58, -0.42]} material={w}><boxGeometry args={[0.07, 0.07, 0.3]} /></mesh>
      <mesh position={[0, 0.6, 0.3]} material={mat('#d23c3c')}><boxGeometry args={[0.4, 0.06, 0.06]} /></mesh>
    </group>
  )
}

/** stadium under construction: platform, pitch, stands rising section by section, crane */
function Stadium() {
  const S = STADIUM
  const base = useMemo(() => {
    let lo = 1e9, hi = -1e9
    for (let a = 0; a < 24; a++) for (const r of [0, 0.6, 1.15]) {
      const h = heightAt(S.x + Math.cos(a / 24 * 6.283) * S.rx * r, S.z + Math.sin(a / 24 * 6.283) * S.rz * r)
      lo = Math.min(lo, h); hi = Math.max(hi, h)
    }
    return { lo, hi }
  }, [])
  const N = 20
  const stands = useRef<THREE.Group>(null!)
  const hook = useRef<THREE.Group>(null!)
  useFrame(() => {
    const t = clock.t
    // 60 % built at the start, rising to ~85 % during the stadium shot
    const p = 0.55 + 0.3 * seg(t, A.l07 + 3.3, A.l08)
    stands.current.children.forEach((c, i) => {
      const s = THREE.MathUtils.clamp(p * N - i, 0, 1)
      c.visible = s > 0.02
      c.scale.y = Math.max(0.02, ease.outBack(s))
    })
    hook.current.rotation.y = 0.6 + Math.sin(t * 0.5) * 0.5
  })
  const y0 = base.hi + 0.15
  return (
    <group position={[S.x, 0, S.z]}>
      <mesh position={[0, (base.lo - 1 + y0) / 2, 0]} scale={[S.rx + 4, 1, S.rz + 4]} material={mat('#b59a72', { rough: 1 })} receiveShadow>
        <cylinderGeometry args={[1, 1, y0 - base.lo + 1, 32]} />
      </mesh>
      <mesh position={[0, y0 + 0.02, 0]} rotation-x={-Math.PI / 2} material={mat('#4caf50', { rough: 0.9 })} receiveShadow><planeGeometry args={[S.rx * 1.3, S.rz * 1.25]} /></mesh>
      {/* pitch lines */}
      <mesh position={[0, y0 + 0.04, 0]} rotation-x={-Math.PI / 2} material={mat('#ffffff')}><ringGeometry args={[2.6, 2.85, 32]} /></mesh>
      <mesh position={[0, y0 + 0.04, 0]} rotation-x={-Math.PI / 2} material={mat('#ffffff')}><planeGeometry args={[0.25, S.rz * 1.25]} /></mesh>
      {[-1, 1].map((s) => (
        <group key={s} position={[s * S.rx * 0.62, y0, 0]}>
          {[-1.8, 1.8].map((z) => <mesh key={z} position={[0, 1, z]} material={mat('#ffffff')}><boxGeometry args={[0.15, 2, 0.15]} /></mesh>)}
          <mesh position={[0, 2, 0]} material={mat('#ffffff')}><boxGeometry args={[0.15, 0.15, 3.75]} /></mesh>
        </group>
      ))}
      {/* stands */}
      <group ref={stands} position={[0, y0, 0]}>
        {Array.from({ length: N }, (_, i) => {
          const a = (i / N) * Math.PI * 2
          const x = Math.cos(a) * (S.rx * 0.9 + 3), z = Math.sin(a) * (S.rz * 0.95 + 3)
          const col = i % 2 ? '#ec6a3f' : '#f2efe6'
          return (
            <group key={i} position={[x, 0, z]} rotation-y={-a + Math.PI / 2}>
              {[0, 1, 2].map((r) => (
                <mesh key={r} position={[0, 0.7 + r * 1.2, -r * 1.3]} material={mat(r === 2 ? '#c9c2b4' : col, { rough: 0.8 })} castShadow>
                  <boxGeometry args={[8.5, 1.3 + r * 1.2, 1.5]} />
                </mesh>
              ))}
            </group>
          )
        })}
      </group>
      {/* tower crane */}
      <group position={[S.rx + 6, y0, -S.rz + 2]}>
        <mesh position={[0, 11, 0]} material={mat('#f2b81e', { rough: 0.6 })} castShadow><boxGeometry args={[0.9, 22, 0.9]} /></mesh>
        <group ref={hook} position={[0, 22, 0]}>
          <mesh position={[-8, 0, 0]} material={mat('#f2b81e', { rough: 0.6 })} castShadow><boxGeometry args={[22, 0.7, 0.7]} /></mesh>
          <mesh position={[3, -0.6, 0]} material={mat('#555b66')}><boxGeometry args={[2.4, 1.4, 1.4]} /></mesh>
          <mesh position={[-15, -4, 0]} material={mat('#333333')}><boxGeometry args={[0.05, 8, 0.05]} /></mesh>
          <mesh position={[-15, -8.4, 0]} material={mat('#9a6a43')}><boxGeometry args={[2.5, 0.6, 1.2]} /></mesh>
        </group>
      </group>
      <group position={[0, y0 + 15, 0]} scale={2.4}>
        <Tag text="ESTADIO PIZZAVILLE · EN OBRAS" y={0} color="#ffffff" bg="#ec6a3f" big />
      </group>
      {/* site fence */}
      <group position={[0, y0, 0]}><Fence w={S.rx * 2 + 16} d={S.rz * 2 + 16} /></group>
    </group>
  )
}

/** new island in the lake: sand, grass, two houses being built, flags, crane */
function Island({ getProgress, items }: { getProgress: () => number; items: Item[] }) {
  const I = ISLE
  const hook = useRef<THREE.Group>(null!)
  useFrame(() => { hook.current.rotation.y = -0.4 + Math.sin(clock.t * 0.6) * 0.6 })
  return (
    <group>
      <group position={[I.x, 0, I.z]}>
        <mesh position={[0, (I.y - 4) / 2, 0]} material={mat('#e3cf9a', { rough: 1 })} receiveShadow><cylinderGeometry args={[I.r, I.r + 2, I.y + 4, 40]} /></mesh>
        <mesh position={[0, I.y + 0.05, 0]} material={mat('#7dbb4f', { rough: 0.95 })} receiveShadow><cylinderGeometry args={[I.r - 3, I.r - 2.5, 0.12, 40]} /></mesh>
        {[[-6, -6], [7, -5]].map(([x, z], i) => (
          <group key={i} position={[x, I.y, z]}>
            <mesh position={[0, 2.4, 0]} material={mat('#8a5a3a')}><cylinderGeometry args={[0.18, 0.25, 4.8, 6]} /></mesh>
            {[0, 1, 2, 3, 4].map((k) => (
              <mesh key={k} position={[Math.cos(k * 1.26) * 1.2, 4.8, Math.sin(k * 1.26) * 1.2]} rotation={[Math.sin(k * 1.26) * 0.6, 0, -Math.cos(k * 1.26) * 0.6]} material={mat('#3f9a3a')}>
                <boxGeometry args={[2.6, 0.08, 0.7]} />
              </mesh>
            ))}
          </group>
        ))}
        <group position={[-2.5, I.y, 11]}><FlagPost iso="ma" h={4.5} /></group>
        <group position={[2.5, I.y, 11]}><FlagPost iso="lb" h={4.5} /></group>
        <group position={[-I.r + 4, I.y, 2]}>
          <mesh position={[0, 8, 0]} material={mat('#f2b81e', { rough: 0.6 })} castShadow><boxGeometry args={[0.7, 16, 0.7]} /></mesh>
          <group ref={hook} position={[0, 16, 0]}>
            <mesh position={[6, 0, 0]} material={mat('#f2b81e', { rough: 0.6 })}><boxGeometry args={[16, 0.55, 0.55]} /></mesh>
            <mesh position={[11, -3, 0]} material={mat('#333333')}><boxGeometry args={[0.05, 6, 0.05]} /></mesh>
            <mesh position={[11, -6.2, 0]} material={mat('#c0392b')}><boxGeometry args={[1.6, 0.5, 1]} /></mesh>
          </group>
        </group>
        <group position={[0, I.y + 13, 0]} scale={2}>
          <Tag text="ÁFRICA · ASIA — EN OBRAS" y={0} color="#ffffff" bg="#2a9d4b" big />
        </group>
      </group>
      {items.map((it) => (
        <group key={it.key} position={[it.lot.x, it.lot.y, it.lot.z]} rotation-y={it.lot.rot}>
          <House spec={it.spec} getProgress={getProgress} flag={null} />
          <ConstructionSite spec={it.spec} getProgress={getProgress} />
        </group>
      ))}
    </group>
  )
}

