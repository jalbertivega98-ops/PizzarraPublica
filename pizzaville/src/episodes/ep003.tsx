// EPISODIO 3 — «La fiesta de la victoria»: Oliver gana 31-4, fiesta en casa de Joaquín con DJ Gisela,
// la oposición la asalta (tartas), llega el ejército, Elena lo apunta en el libro de historia.
// Mundo persistente: reutiliza el reparto del ep002 y añade a los vecinos nuevos detrás.
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
import { heightAt } from '../world/terrain'
import { type Lot } from './ep001layout'
import { Tag, BigLabel, Bridge, Fence, PlotMarker } from './parts'
import {
  LAYOUT as L2, ISO, ISLE, STADIUM, POSTER, DECK, wishStyle, type Item,
  Poster, Castle, BellTower, Terrace, Dog, Stadium, Island, FlagPost,
} from './ep002'
import VECINOS from '../../episodios/ep003/vecinos.csv?raw'

export const EP003 = {
  id: 'ep003',
  duration: 57.6,
  script: [
    { id: 'l01', at: 0.3, text: '¡Noventa y un vecinos... y por fin, un presidente!' },
    { id: 'l02', at: 3.32, text: 'Oliver arrasa: ¡treinta y uno a cuatro! Y como ha ganado... ¡la fiesta la paga él!' },
    { id: 'l03', at: 8.22, text: '¿Dónde? En la casa de Joaquín, que pidió una piscina para dar fiestas a todo el pueblo.' },
    { id: 'l04', at: 13.11, text: 'A los platos, ¡DJ Gisela! Quentin trae el pan, Nicolás pone las luces... y Álvaro viene con India y Nala.' },
    { id: 'l05', at: 18.73, text: 'Pero... la oposición de Thiago no se lo ha tomado nada bien.' },
    { id: 'l06', at: 22.12, text: '¡Asaltan la fiesta! ¡Tartas por los aires!' },
    { id: 'l07', at: 24.52, text: '¡Llamad al ejército! Sale la base militar de Fran, con el general Esteban al frente.' },
    { id: 'l08', at: 28.84, text: 'Gian, SoyAngelix y el sheriff Ezequiel ponen orden. ¡Paz en Pizzaville!' },
    { id: 'l09', at: 33.45, text: 'Y Elena, desde el ayuntamiento, lo apunta todo en el libro de historia del pueblo.' },
    { id: 'l10', at: 37.57, text: 'Mientras, Hugo, Rafael y Joakin estrenan el estadio... ¡y Cayetano abre su plaza de toros!' },
    { id: 'l11', at: 42.46, text: 'Europa sigue ganando, cincuenta y uno a treinta y ocho. Ahora decidís vosotros: ¿qué hacemos con la oposición? Comenta MULTA o PERDÓN.' },
    { id: 'l12', at: 50.11, text: 'Y si eres nuevo: tu nombre, tu país y qué quieres ser. ¿Tu casa aquí? ¡Etiqueta a alguien de tu país!' },
  ],
}
const A = Object.fromEntries(EP003.script.map((l) => [l.id, l.at])) as Record<string, number>
const PZ = { x: 0.15, z: 5.3 }
const BRIDGES = [-45, 20, 85]
const EUROPE = new Set(['España', 'Bulgaria'])
export const BULLRING = { x: 70, z: 110, r: 15 }
function topOf(x: number, z: number, rx: number, rz: number) { let hi = -1e9; for (let a = 0; a < 24; a++) for (const k of [0, 0.6, 1.15]) hi = Math.max(hi, heightAt(x + Math.cos(a / 24 * 6.283) * rx * k, z + Math.sin(a / 24 * 6.283) * rz * k)); return hi }
export const STADIUM_Y = topOf(STADIUM.x, STADIUM.z, STADIUM.rx, STADIUM.rz) + 0.15
const RING_Y = (() => { let hi = -1e9; for (let a = 0; a < 16; a++) hi = Math.max(hi, heightAt(BULLRING.x + Math.cos(a) * BULLRING.r, BULLRING.z + Math.sin(a) * BULLRING.r)); return hi })()

// ---------------------------------------------------------------- layout: ep002 + new neighbours
function build() {
  const rows = VECINOS.split(/\r?\n/).slice(1).filter((l) => l.trim()).map((l) => l.split(','))
  const items: Item[] = L2.items.map((it) => ({ ...it, isNew: false, delay: -9 }))
  let k = 0
  for (const c of rows.slice(87)) {
    const p = { name: c[0], country: c[1], iso: ISO[c[1]] ?? 'es', handle: c[3] ?? '', wish: c[4] ?? '', job: (c[c.length - 1] ?? '').trim() }
    if (/armer/i.test(p.job)) continue // not shown (joel)
    if (/toros/.test(p.wish)) continue // Cayetano gets the bullring instead of a house
    const lot = EUROPE.has(p.country) ? L2.nextEu() : L2.nextAm()
    const { o, label } = wishStyle(p.wish.toLowerCase())
    const jl = /futbol/.test(p.job) ? 'FUTBOLISTA' : /electric/.test(p.job) ? 'ELECTRICISTA' : label
    items.push({ key: p.name + '_' + p.handle, lot, spec: { ...houseSpecFromSeed(hashString(p.name + p.country)), ...o }, iso: p.iso, name: p.name, label: jl,
      isNew: true, delay: 0.35 + (k++) * 0.12, person: p as any })
  }
  const ayto: Item = { key: 'AYUNTAMIENTO', lot: L2.nextEu(), spec: { ...houseSpecFromSeed(301), w: 11, d: 8, floors: 2, wall: '#f3e6c8', roof: '#8a3b2a', roofType: 'hip', balcony: true, porch: true },
    iso: 'es', sign: 'AYUNTAMIENTO', signColor: '#7a5a3a', isNew: true, delay: 0.35 + (k++) * 0.12 }
  const base: Item = { key: 'BASE MILITAR', lot: L2.nextAm(), spec: { ...houseSpecFromSeed(302), w: 11, d: 7.5, floors: 1, wall: '#6b7a4a', roof: '#4a5535', roofType: 'hip', balcony: false, porch: false },
    iso: '', sign: 'BASE MILITAR DE FRAN', signColor: '#4a5535', isNew: true, delay: 0.35 + (k++) * 0.12 }
  items.push(ayto, base)
  for (const it of items) extraReserved.push({ x: it.lot.x, z: it.lot.z, r: 9 })
  extraReserved.push({ x: BULLRING.x, z: BULLRING.z, r: 24 })
  const free = L2.nextEu()
  const by = (n: string) => items.find((i) => i.name === n || i.key === n || (i.person && n === i.name + '@' + i.person.handle))!
  return { items, ayto, base, free, by, joaquin: by('Joaquín@joaquinzamora99') }
}
export const LAY = build()
;(globalThis as any).__ep3 = LAY
const ISLAND = new Set(['Marruecos', 'Líbano'])

const F = (l: Lot) => [Math.sin(l.rot), Math.cos(l.rot)]
function at(l: Lot, f: number, r: number, y: number): [number, number, number] {
  const [fx, fz] = F(l)
  return [l.x + fx * f + fz * r, l.y + y, l.z + fz * f - fx * r]
}
const look = (l: Lot, y = 2.6): [number, number, number] => [l.x, l.y + y, l.z]
const JQ = LAY.joaquin.lot
const party = (f: number, r: number, y = 0) => at(JQ, f, r, y)
const posterLot = (p: { x: number; z: number }): Lot => ({ x: p.x, z: p.z, y: DECK, rot: Math.PI / 2 })

// ---------------------------------------------------------------- camera
function cameraKeys(): CamKey[] {
  const H = HOME_Y + 1.6
  const shot = (t0: number, t1: number, l: Lot, d = 13, r = 4, y = 4.5): CamKey[] => [
    { t: t0, p: at(l, d + 9, r * 1.6, y + 3.5), l: look(l, 3.2), fov: 44, cut: true },
    { t: t1, p: at(l, d + 5, r * 1.2, y + 2.5), l: look(l, 3.0), fov: 42, e: 'linear' },
  ]
  const po = posterLot(POSTER.oliver), pt = posterLot(POSTER.thiago)
  const S = STADIUM, fl = LAY.free, B = BULLRING
  const pc = party(11, 0, 1.2) // centre of the dance floor
  return [
    // S1 hook: aerial dive
    { t: 0, p: [-60, 190, 230], l: [0, 0, -25], fov: 50 },
    { t: 3.22, p: [25, 55, 85], l: [0, 2, -10], fov: 48, e: 'inOut' },
    // S2 Oliver wins, at his poster
    { t: A.l02, p: [po.x + 15, po.y + 3.6, po.z + 6], l: [po.x + 2, po.y + 2.6, po.z], fov: 44, cut: true },
    { t: A.l03 - 0.1, p: [po.x + 10, po.y + 3.0, po.z + 3], l: [po.x + 2, po.y + 2.6, po.z], fov: 42, e: 'linear' },
    // S3 Joaquín's house: crane over the pool party
    { t: A.l03, p: party(40, 18, 26), l: party(6, 0, 1), fov: 48, cut: true },
    { t: A.l04 - 0.1, p: party(26, 10, 12), l: party(8, 0, 1.5), fov: 48, e: 'inOut' },
    // S4 DJ Gisela, Quentin, Nicolás, Álvaro & dogs
    { t: A.l04, p: party(14, 4.5, 3.2), l: party(7.5, 3.2, 2.2), fov: 42, cut: true },
    { t: 14.68, p: party(12.5, 4, 2.8), l: party(7.5, 3.2, 2.0), fov: 40, e: 'linear' },
    { t: 14.72, p: party(13.5, -10.5, 2.6), l: party(12, -5.2, 1.3), fov: 46, cut: true },
    { t: 17.07, p: party(15, -8.5, 2.6), l: party(12.3, -3, 1.4), fov: 46, e: 'linear' },
    { t: 17.11, p: party(21, 2, 2.6), l: party(15.5, 0, 0.9), fov: 42, cut: true },
    { t: A.l05 - 0.1, p: party(19.5, 1.5, 2.3), l: party(15.5, 0, 0.9), fov: 42, e: 'linear' },
    // S5 Thiago and the opposition, angry at their poster
    { t: A.l05, p: [pt.x + 15, pt.y + 3.6, pt.z - 6], l: [pt.x + 2, pt.y + 2.4, pt.z], fov: 44, cut: true },
    { t: A.l06 - 0.1, p: [pt.x + 10, pt.y + 3.0, pt.z - 3], l: [pt.x + 2, pt.y + 2.4, pt.z], fov: 42, e: 'linear' },
    // S6 the raid: cakes in the air
    { t: A.l06, p: party(24, -12, 7), l: pc, fov: 50, cut: true },
    { t: A.l07 - 0.1, p: party(22, -6, 5.5), l: pc, fov: 50, e: 'linear' },
    // S7 the army base, then the troops arriving
    ...shot(A.l07, 26.38, LAY.base.lot, 14, -4, 5),
    { t: 26.42, p: at(LAY.base.lot, 17, 6, 3.5), l: at(LAY.base.lot, 8, 0, 1.6), fov: 46, cut: true },
    { t: A.l08 - 0.1, p: at(LAY.base.lot, 14.5, 4, 3.0), l: at(LAY.base.lot, 8, 0, 1.6), fov: 44, e: 'linear' },
    // S8 police put things in order: wide on the calmed party
    { t: A.l08, p: party(8, -13, 6), l: party(16, 0, 1.3), fov: 48, cut: true },
    { t: A.l09 - 0.1, p: party(8, -20, 12), l: party(14, 0, 1.3), fov: 48, e: 'inOut' },
    // S9 Elena at the town hall with the history book
    ...shot(A.l09, A.l10 - 0.1, LAY.ayto.lot, 11, 3, 3),
    // S10 stadium with the three players, then the bullring
    { t: A.l10, p: [S.x - 30, heightAt(S.x, S.z) + 22, S.z + 40], l: [S.x, heightAt(S.x, S.z) + 1, S.z], fov: 48, cut: true },
    { t: 40.35, p: [S.x + 20, heightAt(S.x, S.z) + 18, S.z + 38], l: [S.x, heightAt(S.x, S.z) + 1, S.z], fov: 48, e: 'linear' },
    { t: 40.39, p: [B.x - 30, heightAt(B.x, B.z) + 24, B.z + 32], l: [B.x, heightAt(B.x, B.z) + 2, B.z], fov: 46, cut: true },
    { t: A.l11 - 0.1, p: [B.x + 10, heightAt(B.x, B.z) + 20, B.z + 34], l: [B.x, heightAt(B.x, B.z) + 2, B.z], fov: 46, e: 'linear' },
    // S11 score + vote MULTA / PERDÓN: aerial, then the opposition at the poster
    { t: A.l11, p: [-70, 170, 170], l: [60, 0, -30], fov: 52, cut: true },
    { t: 45.7, p: [120, 170, 170], l: [110, 0, -25], fov: 52, e: 'linear' },
    { t: 45.75, p: [pt.x + 15, pt.y + 3.4, pt.z + 7], l: [pt.x + 2, pt.y + 2.4, pt.z], fov: 46, cut: true },
    { t: A.l12 - 0.1, p: [pt.x + 11, pt.y + 3.0, pt.z + 4], l: [pt.x + 2, pt.y + 2.4, pt.z], fov: 44, e: 'linear' },
    // S12 Pizz, the free plot, then up and away
    { t: A.l12, p: [1.4, 2.6, 10.0], l: [PZ.x, H - 0.05, PZ.z], fov: 38, cut: true },
    { t: 52.68, p: [0.5, 2.5, 8.6], l: [PZ.x, H - 0.05, PZ.z], fov: 34, e: 'linear' },
    { t: 52.73, p: [fl.x + 6, fl.y + 16, fl.z - 22], l: [fl.x, fl.y + 2, fl.z], fov: 48, cut: true },
    { t: 55.0, p: [fl.x + 4, fl.y + 12, fl.z - 17], l: [fl.x, fl.y + 2, fl.z], fov: 48, e: 'linear' },
    { t: 55.6, p: [fl.x + 3.6, fl.y + 11.5, fl.z - 16], l: [fl.x, fl.y + 2.2, fl.z], fov: 48, e: 'linear' },
    { t: EP003.duration, p: [80, 170, 220], l: [40, 0, -25], fov: 52, e: 'inOut' },
  ]
}

// ---------------------------------------------------------------- cast
const tint = (seed: number, top: string, extra: Partial<Look> = {}): Look => {
  const c = new THREE.Color(top)
  return { ...lookFromSeed(seed), top, topDark: '#' + c.multiplyScalar(0.78).getHexString(), ...extra }
}
type Act = 'wave' | 'celebrate' | 'hammer' | 'point' | 'shrug' | 'surprise' | 'talk' | 'none'
type Cast = { key: string; look: Look; pos: (t: number) => [number, number, number]; ry: number; act: (t: number) => Act; vis?: (t: number) => boolean; moving?: (t: number) => boolean }
const lerp3 = (a: number[], b: number[], k: number): [number, number, number] => [a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k, a[2] + (b[2] - a[2]) * k]

function cast(): Cast[] {
  const po = posterLot(POSTER.oliver), pt = posterLot(POSTER.thiago)
  const S = STADIUM, sy = (x: number, z: number) => heightAt(x, z)
  const fixed = (p: [number, number, number]) => () => p
  const ry = JQ.rot
  const calm = (t: number): Act => (t > A.l06 && t < A.l08 + 1 ? 'surprise' : 'celebrate')
const bf = (f: number, r: number) => at(LAY.base.lot, f, r, 0)
  const sw = (a: [number, number, number], b: [number, number, number]) => (t: number) => (t < A.l08 ? a : b)
  const out: Cast[] = [
    // Oliver: winner at his poster early, then at the party
    { key: 'Oliver', look: tint(11, '#ffd23d'), pos: (t) => (t < A.l03 ? [19.4, DECK, po.z + 1.6] : party(12, 0.5)), ry: Math.PI / 2, act: () => 'celebrate' },
    { key: 'Thiago', look: tint(12, '#3fa9f5'), pos: fixed([19.4, DECK, pt.z - 1.6]), ry: Math.PI / 2, act: (t) => (t < A.l06 ? 'shrug' : 'point') },
    { key: 'Gisela', look: tint(31, '#e040a0', { hair: '#2a1d16' }), pos: fixed(party(6.2, 3.2)), ry, act: () => 'celebrate' },
    { key: 'Quentin', look: tint(32, '#f2efe6', { pants: '#c9a46b' }), pos: fixed(party(12, -5.2)), ry: ry + 0.4, act: (t) => (t > A.l06 && t < A.l08 ? 'surprise' : 'wave') },
    { key: 'Nicolás', look: tint(33, '#f2b81e', { hardhat: true }), pos: fixed(party(12.5, -1.2)), ry: ry - 0.4, act: (t) => (t > A.l06 && t < A.l08 ? 'surprise' : 'hammer') },
    { key: 'Álvaro', look: tint(16, '#1c1c1f', { pants: '#1c1c1f' }), pos: fixed(party(15.5, 1.0)), ry, act: (t) => (t > A.l06 && t < A.l08 ? 'surprise' : 'wave') },
    { key: 'Joaquín', look: tint(34, '#47a5a5'), pos: fixed(party(10, 4.5)), ry, act: calm },
    // army + police arrive during l07–l08
    { key: 'Esteban', look: tint(35, '#4a5535', { pants: '#3a4228' }), pos: sw(bf(6.5, -1), party(18.5, 0)), ry: LAY.base.lot.rot, act: () => 'point' },
    { key: 'Fran', look: tint(36, '#4a5535', { pants: '#3a4228' }), pos: sw(bf(6.5, 1.5), party(19.5, 2.4)), ry: LAY.base.lot.rot, act: () => 'wave' },
    { key: 'Gian', look: tint(13, '#1f3a6b', { pants: '#1c2533' }), pos: fixed(party(17, -3.5)), ry: ry + Math.PI, act: () => 'point', vis: (t) => t > A.l08 - 0.1 },
    { key: 'SoyAngelix', look: tint(14, '#1f3a6b', { pants: '#1c2533' }), pos: fixed(party(17.5, -6)), ry: ry + Math.PI, act: () => 'point', vis: (t) => t > A.l08 - 0.1 },
    { key: 'Ezequiel', look: tint(15, '#8a5a2b'), pos: fixed(party(17.5, 5.5)), ry: ry + Math.PI, act: () => 'point', vis: (t) => t > A.l08 - 0.1 },
    // Elena at the town hall with the history book
    { key: 'Elena', look: tint(37, '#a368c2'), pos: fixed(at(LAY.ayto.lot, LAY.ayto.spec.d / 2 + 2.4, 0.8, 0)), ry: LAY.ayto.lot.rot, act: () => 'talk' },
    // footballers in the stadium
    ...['Hugo', 'Rafael', 'Joakin'].map((n, i): Cast => ({ key: n, look: tint(20 + i * 7, ['#d23c3c', '#2d6cdf', '#d23c3c'][i], { pants: '#f2efe6' }),
      pos: (t) => { const a = t * 1.4 + i * 2.1; const x = S.x + Math.cos(a) * (5 + i * 2), z = S.z + Math.sin(a) * (3 + i); return [x, STADIUM_Y, z] },
      ry: 0, act: () => 'none', moving: () => true })),
    // Cayetano in his bullring
    { key: 'Cayetano', look: tint(38, '#c1272d', { pants: '#e8c547' }), pos: fixed([BULLRING.x + 2, RING_Y + 0.17, BULLRING.z + 1]), ry: 0.6, act: () => 'celebrate' },
  ]
  // dancing crowd around the pool
  const r = mulberry32(77)
  for (let i = 0; i < 16; i++) {
    const f = 9 + r() * 7, rr = -6 + r() * 12
    if (Math.hypot(f - 12, rr - 0.5) < 1.2) continue
    out.push({ key: 'crowd' + i, look: lookFromSeed(1000 + i), pos: fixed(party(f, rr)), ry: ry + (r() - 0.5) * 2, act: calm })
  }
  // the opposition: blue shirts storming in from the side during l06
  for (let i = 0; i < 6; i++) {
    const r0 = -18 - i * 1.3, f0 = 9 + i * 1.6
    out.push({ key: 'opo' + i, look: tint(500 + i, '#3fa9f5'), pos: (t) => lerp3(party(f0, r0), party(f0 + 0.5, -8.5 - (i % 3) * 0.8), seg(t, A.l06 - 0.4, A.l06 + 1.2)),
      ry: ry - Math.PI / 2, act: (t) => (t > A.l08 + 0.5 ? 'shrug' : t > A.l06 + 1.2 ? 'point' : 'none'), vis: (t) => t > A.l06 - 0.5, moving: (t) => t > A.l06 - 0.4 && t < A.l06 + 1.2 })
  }
  // soldiers following the general
  for (let i = 0; i < 6; i++) {
    const rr = -4 + (i % 3) * 4, ff = 37 + Math.floor(i / 3) * 2
    out.push({ key: 'sol' + i, look: tint(600 + i, '#4a5535', { pants: '#3a4228', hardhat: true }), pos: sw(bf(9 + Math.floor(i / 3) * 1.6, -3 + (i % 3) * 3), party(ff - 15, rr * 1.4)),
      ry: LAY.base.lot.rot, act: () => (i % 2 ? 'none' : 'wave') })
  }
  return out
}

// cakes: thrown by the opposition at the dancers
const CAKES = Array.from({ length: 10 }, (_, i) => {
  const r = mulberry32(900 + i)
  const from = party(10 + (i % 6) * 1.6, -8.8, 1.6), to = party(9 + r() * 7, -4 + r() * 9, 0.4)
  const t0 = A.l06 + 0.9 + i * 0.22
  return { from, to, t0, t1: t0 + 0.9, col: i % 2 ? '#ff8fb8' : '#fff1e0' }
})

// ---------------------------------------------------------------- component
export function Ep003() {
  const { camera } = useThree()
  const lines = useMemo(() => useLines(EP003.id, EP003.script), [])
  const keys = useMemo(cameraKeys, [])
  const pizz = useMemo(newState, [])
  const P = useMemo(() => new THREE.Vector3(), [])
  const L = useMemo(() => new THREE.Vector3(), [])
  const camPos = useMemo(() => new THREE.Vector3(), [])
  const labels = useRef<THREE.Group>(null!)
  const marker = useRef<THREE.Group>(null!)
  const cakes = useRef<THREE.Group>(null!)
  const splats = useRef<THREE.Group>(null!)
  const lights = useRef<THREE.Group>(null!)
  const ball = useRef<THREE.Mesh>(null!)
  const book = useRef<THREE.Group>(null!)
  const people = useMemo(cast, [])
  const states = useMemo(() => people.map(() => newState()), [])
  const T = () => clock.t

  useMemo(() => {
    const pv = (window as any).__pv
    if (!pv) return
    pv.info = () => {
      const sfx: { type: string; at: number; g?: number }[] = [{ type: 'whoosh', at: 0.0, g: 0.6 }]
      LAY.items.forEach((it, i) => { if (it.isNew) sfx.push({ type: 'pop', at: 0.4 + it.delay + 0.3, g: 0.22 }) })
      for (const k of keys) if (k.cut && k.t > 3) sfx.push({ type: 'whoosh', at: k.t - 0.05, g: 0.3 })
      for (const c of CAKES) sfx.push({ type: 'pop', at: c.t1, g: 0.35 })
      sfx.push({ type: 'chime', at: A.l02 + 1.0, g: 0.6 }, { type: 'chime', at: A.l08 + 3.2, g: 0.6 }, { type: 'chime', at: A.l10 + 3.0, g: 0.5 }, { type: 'chime', at: A.l11 + 6.4, g: 0.6 })
      return { id: EP003.id, duration: EP003.duration, lines: lines.map((l) => ({ id: l.id, at: l.at, dur: l.dur, text: l.text, words: l.words, hasAudio: l.hasAudio })), sfx }
    }
  }, [])

  useFrame(() => {
    const t = T()
    const fov = evalCam(keys, t, P, L)
    camera.position.copy(P); camera.lookAt(L)
    const pc = camera as THREE.PerspectiveCamera
    if (Math.abs(pc.fov - fov) > 0.01) { pc.fov = fov; pc.updateProjectionMatrix() }
    camPos.copy(P); (globalThis as any).__cam3 = [P.toArray(), L.toArray(), marker.current?.visible]
    world.focus.set(L.x, 0, L.z)
    world.shadowSpan = THREE.MathUtils.clamp(P.distanceTo(L) * 0.9, 18, 120)

    pizz.x = PZ.x; pizz.z = PZ.z; pizz.y = HOME_Y; pizz.ry = 0.15; pizz.speed = 0
    pizz.lookAt = camPos; pizz.action = 'none'; pizz.actionW = 0; pizz.smile = 0.8
    if (t > A.l12 && t < A.l12 + 1.8) { pizz.action = 'point'; pizz.actionT = t; pizz.actionW = seg(t, A.l12, A.l12 + 0.3) * (1 - seg(t, A.l12 + 1.5, A.l12 + 1.8)) }
    else if (speakingAt(lines, t)) { pizz.action = 'talk'; pizz.actionT = t; pizz.actionW = 0.85 }
    pizz.mouth = mouthAt(lines, t)

    people.forEach((c, i) => {
      const st = states[i]
      const [x, y, z] = c.pos(t)
      st.x = x; st.z = z; st.y = y || heightAt(x, z)
      const mv = c.moving?.(t) ?? false
      st.speed = mv ? 3.2 : 0
      st.ry = c.ry
      st.lookAt = mv || c.act(t) === 'hammer' ? null : camPos
      st.visible = c.vis ? c.vis(t) : true
      const a = c.act(t)
      st.action = a === 'none' ? 'none' : a; st.actionT = t + i * 0.31; st.actionW = a === 'none' ? 0 : 1
    })

    // cakes in flight and splats on the ground
    cakes.current.children.forEach((m, i) => {
      const c = CAKES[i], k = seg(t, c.t0, c.t1)
      m.visible = t > c.t0 && t < c.t1
      if (m.visible) m.position.set(c.from[0] + (c.to[0] - c.from[0]) * k, c.from[1] + (c.to[1] - c.from[1]) * k + Math.sin(k * Math.PI) * 4, c.from[2] + (c.to[2] - c.from[2]) * k)
      m.rotation.set(t * 7 + i, t * 5, 0)
    })
    splats.current.children.forEach((m, i) => {
      const c = CAKES[i]
      m.visible = t > c.t1 && t < A.l09
      m.scale.setScalar(Math.max(0.01, ease.outBack(seg(t, c.t1, c.t1 + 0.25))))
    })
    // party lights pulse with the beat
    lights.current.children.forEach((m, i) => {
      const s = 0.7 + 0.5 * Math.max(0, Math.sin(t * 8 + i * 1.7));
      (m as THREE.Mesh).scale.setScalar(s)
    })
    // football bouncing between the players
    const S = STADIUM
    ball.current.position.set(S.x + Math.cos(t * 2.2) * 7, STADIUM_Y + 0.35 + Math.abs(Math.sin(t * 6)) * 1.2, S.z + Math.sin(t * 1.7) * 4)
    book.current.rotation.y = Math.sin(t * 2) * 0.15

    labels.current.visible = t > A.l11 && t < 45.7
    marker.current.visible = t > 52.7
    marker.current.scale.setScalar(Math.max(0.001, ease.outBack(seg(t, 52.8, 53.3))) * 1.5)
  }, -1)

  const prog = (it: Item) => (it.isNew ? () => seg(T(), 0.4 + it.delay, 1.1 + it.delay) : () => 1)
  const fl = LAY.free
  const el = at(LAY.ayto.lot, LAY.ayto.spec.d / 2 + 2.9, 0.8, 1.3)
  return (
    <group>
      <PizzHome />
      <Character look={PIZZ_LOOK} state={pizz} />
      {people.map((c, i) => <Character key={c.key} look={c.look} state={states[i] as CharState} />)}
      {LAY.items.filter((it) => !ISLAND.has(it.person?.country ?? '')).map((it) => (
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
        </group>
      ))}
      {LAY.items.map((it) => (
        <group key={'t' + it.key} position={[it.lot.x, it.lot.y + (it.castle ? 12.5 : it.spec.wallH * it.spec.floors + 3.8), it.lot.z]} scale={1.6}>
          {it.name && <NameTag name={it.name} iso={it.iso} />}
          {it.label && <Tag text={it.label} y={-0.62} color="#ffd23d" />}
          {it.sign && <Tag text={it.sign} y={it.name ? 0.75 : 0} color="#ffffff" bg={it.signColor} big />}
        </group>
      ))}
      {BRIDGES.map((bx) => <Bridge key={bx} x={bx} />)}
      <Poster {...POSTER.oliver} />
      <Poster {...POSTER.thiago} />
      <group position={[16.5, DECK + 6.9, POSTER.oliver.z]} scale={1.8}><Tag text="¡GANADOR! 31 VOTOS" y={0} color="#1a2233" bg="#ffd23d" big /></group>
      <Stadium progress={() => 1} label="ESTADIO PIZZAVILLE · ¡INAUGURADO!" />
      <mesh ref={ball} material={mat('#ffffff', { rough: 0.5 })} castShadow><sphereGeometry args={[0.35, 12, 10]} /></mesh>
      <Bullring />
      <Island getProgress={() => 0.66} items={LAY.items.filter((it) => ISLAND.has(it.person?.country ?? ''))} />
      <PartySet lights={lights} />
      {/* Álvaro's dogs: India (black border collie) and Nala (light brown mastiff) */}
      <group position={party(15.8, 2.3)} rotation-y={JQ.rot + 0.6}><Dog color="#1f1f22" ear="#1f1f22" scale={1.2} /></group>
      <group position={party(16.2, -0.6)} rotation-y={JQ.rot - 0.5}><Dog color="#d9b98a" ear="#b8935e" scale={1.55} /></group>
      {/* Quentin's bread basket */}
      <group position={party(12.6, -5.9, 0)}>
        <mesh position={[0, 0.45, 0]} material={mat('#a0703f')}><cylinderGeometry args={[0.55, 0.4, 0.4, 10]} /></mesh>
        {[0, 1, 2].map((i) => <mesh key={i} position={[-0.25 + i * 0.25, 0.75, 0]} rotation-z={0.5 - i * 0.5} material={mat('#e0a95a')}><capsuleGeometry args={[0.09, 0.8, 4, 8]} /></mesh>)}
      </group>
      {/* Elena's history book */}
      <group ref={book} position={el}>
        <mesh material={mat('#7a1f2b')}><boxGeometry args={[0.7, 0.5, 0.12]} /></mesh>
        <Text font="/fonts/lilita.woff" fontSize={0.09} color="#e8c547" position={[0, 0.05, 0.07]} anchorX="center">HISTORIA DE</Text>
        <Text font="/fonts/lilita.woff" fontSize={0.1} color="#e8c547" position={[0, -0.08, 0.07]} anchorX="center">PIZZAVILLE</Text>
      </group>
      <group ref={cakes}>
        {CAKES.map((c, i) => (
          <group key={i}>
            <mesh material={mat(c.col, { rough: 0.6 })}><cylinderGeometry args={[0.35, 0.35, 0.25, 12]} /></mesh>
            <mesh position={[0, 0.16, 0]} material={mat('#d23c3c')}><sphereGeometry args={[0.09, 8, 6]} /></mesh>
          </group>
        ))}
      </group>
      <group ref={splats}>
        {CAKES.map((c, i) => (
          <mesh key={i} position={[c.to[0], c.to[1] - 0.36, c.to[2]]} rotation-x={-Math.PI / 2} material={mat(c.col, { rough: 0.7 })}><circleGeometry args={[0.7, 10]} /></mesh>
        ))}
      </group>
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
/** DJ booth, speakers, light poles and string lights in front of Joaquín's house */
export function PartySet({ lights }: { lights: React.RefObject<THREE.Group> }) {
  const cols = ['#ff3d7f', '#3dd9ff', '#ffd23d', '#7dff6a', '#b06aff', '#ff8a3d']
  const poles: [number, number][] = [[7, -7], [7, 7], [17, -7], [17, 7]]
  return (
    <group>
      <group position={party(7.0, 3.2)} rotation-y={JQ.rot + Math.PI}>
        <mesh position={[0, 0.55, 0]} material={mat('#1a2233')} castShadow><boxGeometry args={[2.6, 1.1, 1.0]} /></mesh>
        <mesh position={[0, 1.12, 0]} material={mat('#2d2d33')}><boxGeometry args={[2.4, 0.06, 0.8]} /></mesh>
        {[-0.6, 0.6].map((x) => <mesh key={x} position={[x, 1.17, 0]} material={mat('#888888', { emissive: '#3dd9ff', ei: 0.4 })}><cylinderGeometry args={[0.3, 0.3, 0.04, 16]} /></mesh>)}
        <Text font="/fonts/lilita.woff" fontSize={0.32} color="#ff3d7f" position={[0, 0.55, -0.51]} rotation-y={Math.PI} anchorX="center">DJ GISELA</Text>
        {[-2, 2].map((x) => <mesh key={'s' + x} position={[x, 0.9, 0]} material={mat('#111111')} castShadow><boxGeometry args={[0.9, 1.8, 0.8]} /></mesh>)}
      </group>
      {poles.map(([f, r], i) => (
        <group key={i} position={party(f, r)}>
          <mesh position={[0, 2, 0]} material={mat('#333333')}><cylinderGeometry args={[0.07, 0.07, 4, 6]} /></mesh>
        </group>
      ))}
      <group ref={lights}>
        {poles.map(([f, r], i) => (
          <mesh key={i} position={party(f, r, 4.1)} material={mat(cols[i], { emissive: cols[i], ei: 1.2 })}><sphereGeometry args={[0.35, 12, 10]} /></mesh>
        ))}
        {Array.from({ length: 18 }, (_, i) => {
          const k = i / 17, side = i < 9 ? -7 : 7, kk = i < 9 ? k * 2 : (k - 0.5) * 2
          return <mesh key={'b' + i} position={party(7 + kk * 10, side, 3.6 - Math.sin(kk * Math.PI) * 0.5)} material={mat(cols[i % 6], { emissive: cols[i % 6], ei: 1.2 })}><sphereGeometry args={[0.13, 8, 6]} /></mesh>
        })}
      </group>
      <group position={party(12, 0, 6.5)} scale={2}><Tag text="FIESTA DE LA VICTORIA · INVITA OLIVER" y={0} color="#1a2233" bg="#ffd23d" big /></group>
    </group>
  )
}

export function BaseProps({ w, d }: { w: number; d: number }) {
  return (
    <group>
      {/* sandbags and a jeep */}
      {[-1, 1].map((s) => <mesh key={s} position={[s * (w / 2 - 0.5), 0.35, d / 2 + 2.4]} material={mat('#c9b07a')}><boxGeometry args={[2.2, 0.7, 0.8]} /></mesh>)}
      <group position={[w / 2 + 3, 0, 1]}>
        <mesh position={[0, 0.9, 0]} material={mat('#5d6b3e')} castShadow><boxGeometry args={[1.8, 1, 3.2]} /></mesh>
        <mesh position={[0, 1.6, -0.4]} material={mat('#4a5535')}><boxGeometry args={[1.6, 0.5, 1.4]} /></mesh>
        {[[-0.9, -1], [0.9, -1], [-0.9, 1], [0.9, 1]].map(([x, z], i) => <mesh key={i} position={[x, 0.4, z]} rotation-z={Math.PI / 2} material={mat('#222222')}><cylinderGeometry args={[0.4, 0.4, 0.3, 12]} /></mesh>)}
      </group>
    </group>
  )
}

/** Cayetano's bullring: round sand arena with tiered white walls and red barrier */
export function Bullring() {
  const B = BULLRING
  const y = useMemo(() => { let hi = -1e9; for (let a = 0; a < 16; a++) hi = Math.max(hi, heightAt(B.x + Math.cos(a) * B.r, B.z + Math.sin(a) * B.r)); return hi }, [])
  return (
    <group position={[B.x, y, B.z]}>
      <mesh position={[0, -1.5, 0]} material={mat('#b59a72', { rough: 1 })} receiveShadow><cylinderGeometry args={[B.r + 3, B.r + 3, 3.2, 40]} /></mesh>
      <mesh position={[0, 0.12, 0]} material={mat('#e3c27a', { rough: 1 })} receiveShadow><cylinderGeometry args={[B.r - 3.5, B.r - 3.5, 0.1, 40]} /></mesh>
      <mesh position={[0, 0.6, 0]} material={mat('#c0392b', { rough: 0.8 })}><cylinderGeometry args={[B.r - 3.4, B.r - 3.4, 1.0, 40, 1, true]} /></mesh>
      {[0, 1, 2].map((i) => (
        <mesh key={i} position={[0, 1.2 + i * 1.1, 0]} material={mat(i === 2 ? '#f4ecd8' : '#e9e2d0', { rough: 0.9 })} castShadow>
          <cylinderGeometry args={[B.r - 2.6 + i * 1.3, B.r - 2.6 + i * 1.3, 1.1 + i * 0.1, 40, 1, true]} />
        </mesh>
      ))}
      <mesh position={[0, 4.6, 0]} material={mat('#c0392b', { rough: 0.8 })}><cylinderGeometry args={[B.r + 0.3, B.r + 0.3, 0.6, 40, 1, true]} /></mesh>
      <group position={[0, 9.5, 0]} scale={2.2}><Tag text="PLAZA DE TOROS DE CAYETANO" y={0} color="#ffffff" bg="#c0392b" big /></group>
    </group>
  )
}
