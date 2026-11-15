// EPISODIO 1 — «62 vecinos»: Europa en la orilla de Pizz, América al otro lado del río.
// Todo es función pura del tiempt `t` del episodio (render determinista).
import { useMemo, useRef } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import * as THREE from 'three'
import { clock, ease, seg } from '../engine/clock'
import { evalCam, world, type CamKey } from '../engine/director'
import { useLines, mouthAt, speakingAt } from '../engine/voice'
import { Character, PIZZ_LOOK, lookFromSeed, newState, type CharState } from '../scene/Character'
import { House, houseSpecFromSeed, type HouseSpec } from '../scene/House'
import { PizzHome, HOME_Y } from '../scene/PizzHome'
import { NameTag } from '../scene/Town'
import { mat } from '../scene/materials'
import { hashString } from '../world/rng'
import { extraReserved, footprintHeight, valid } from '../world/plots'
import { europeLots, americaLots, type Lot } from './ep001layout'
import VECINOS from '../../episodios/ep001/vecinos.csv?raw'
import { Tag, BigLabel, Bridge, Fence, PlotMarker } from './parts'

export const EP001 = {
  id: 'ep001',
  duration: 54.5,
  script: [
    { id: 'l01', at: 0.3, text: '¡Eh! ¡Que ayer vivía SOLO aquí!' },
    { id: 'l02', at: 2.2, text: 'Y mirad esto: ¡sesenta y dos vecinos! ¡De trece países!' },
    { id: 'l03', at: 5.3, text: 'Sois tantos que he tenido que partir el valle en dos: Europa a este lado del río... ¡y América al otro!' },
    { id: 'l04', at: 11.4, text: 'Supermercado, escuela, centro de salud... ¡y tres puentes! Esto ya es una ciudad.' },
    { id: 'l05', at: 16.2, text: 'Marina, fuiste la primera. ¡Tu casa ya está!' },
    { id: 'l06', at: 18.7, text: 'Gabriel, tu granja de gallinas. Manuel, tu huerto con tractor. Y Rodrigo... tu furgo, tus perros, y el río al ladito.' },
    { id: 'l07', at: 25.0, text: '¡Y Aleky quería ser el peluquero! Peluquería abierta.' },
    { id: 'l08', at: 28.15, text: 'Cruzamos a América: Fernando, tu rancho. Kiker, tu casa de dos pisos. ¡Y Thiago, mansión con piscina!' },
    { id: 'l09', at: 34.05, text: '¡Atención! Matheus trae la primera bandera nueva: ¡Brasil! Premio: barrio propio.' },
    { id: 'l10', at: 38.65, text: 'Y ahora mismo... ¡Europa gana treinta y siete a veinticinco!' },
    { id: 'l11', at: 42.2, text: 'América, ¿os vais a dejar ganar?' },
    { id: 'l12', at: 44.4, text: 'Comenta tu nombre, tu país y qué casa quieres. ¡Y etiqueta a alguien de tu país!' },
    { id: 'l13', at: 49.35, text: '¿Tu casa aquí? ¡Te la construyo en el próximo episodio!' },
  ],
}
const A = Object.fromEntries(EP001.script.map((l) => [l.id, l.at])) as Record<string, number>

// ---------------------------------------------------------------- data & layout
const ISO: Record<string, string> = { España: 'es', México: 'mx', Argentina: 'ar', Colombia: 'co', Chile: 'cl', Bulgaria: 'bg', Perú: 'pe', Venezuela: 've', Bolivia: 'bo', Cuba: 'cu', 'República Dominicana': 'do', Uruguay: 'uy', Brasil: 'br' }
const EUROPE = new Set(['España', 'Bulgaria'])
type Person = { name: string; country: string; iso: string; wish: string }
function people(): Person[] {
  return VECINOS.split(/\r?\n/).slice(1).filter((l) => l.trim()).map((l) => {
    const c = l.split(',')
    return { name: c[0], country: c[1], iso: ISO[c[1]] ?? 'es', wish: c[4] ?? '' }
  })
}

type Item = { key: string; lot: Lot; spec: HouseSpec; iso: string; name?: string; label?: string; sign?: string; signColor?: string; pool?: boolean; fence?: boolean; delay: number; person?: Person }

const PZ = { x: 0.15, z: 5.3 }

function riverSpot(x0: number): Lot {
  for (let z = -36; z < -10; z += 2) {
    if (valid(x0, z)) return { x: x0, z, y: footprintHeight(x0, z), rot: Math.PI }
  }
  return { x: x0, z: -30, y: footprintHeight(x0, -30), rot: Math.PI }
}

function build(): { items: Item[]; byName: Record<string, Item>; free: Lot; brazil: Lot } {
  const ps = people()
  const eu = europeLots(44), am = americaLots(31)
  const items: Item[] = []
  const spec = (seed: number, o: Partial<HouseSpec> = {}) => ({ ...houseSpecFromSeed(seed), ...o })
  // infrastructure next to Pizz
  const infra: [number, string, string, Partial<HouseSpec>][] = [
    [1, 'SUPERMERCADO', '#2e8b57', { w: 10, d: 7, floors: 1, wall: '#f2f0e6', roof: '#2e8b57', roofType: 'hip' }],
    [3, 'ESCUELA', '#d9822b', { w: 10.5, d: 7, floors: 2, wall: '#f3d9a4', roof: '#a94b32', roofType: 'gable', balcony: false }],
    [5, 'CENTRO DE SALUD', '#d23c3c', { w: 9.5, d: 7, floors: 2, wall: '#ffffff', roof: '#7a8a99', roofType: 'hip', balcony: false }],
  ]
  for (const [i, sign, col, o] of infra) items.push({ key: sign, lot: eu[i], spec: spec(900 + i, o), iso: '', sign, signColor: col, delay: 0.1 * i })
  const used = new Set(infra.map((x) => x[0]))
  let ei = 0, ai = 0
  const nextEu = () => { while (used.has(ei)) ei++; return eu[ei++] }
  // America featured lots near the central bridge
  const amFixed: Record<string, number> = { Fernando: 0, Kiker: 2, Thiago: 5 }
  const amUsed = new Set(Object.values(amFixed).concat([am.length - 1]))
  const nextAm = () => { while (amUsed.has(ai)) ai++; return am[ai++] }
  let k = 0
  for (const p of ps) {
    const seed = hashString(p.name + p.country)
    let lot: Lot, o: Partial<HouseSpec> = {}, label: string | undefined, sign: string | undefined, pool = false, fence = false
    const w = p.wish.toLowerCase()
    if (p.name === 'Rodrigo') lot = riverSpot(-78)
    else if (p.name === 'Aleky') { lot = eu[7]; used.add(7); sign = 'PELUQUERÍA ALEKY'; o = { wall: '#f7c6d9', roof: '#7d4e9e' } }
    else if (p.country === 'Brasil') lot = am[am.length - 1]
    else if (amFixed[p.name] !== undefined) lot = am[amFixed[p.name]]
    else lot = EUROPE.has(p.country) ? nextEu() : nextAm()
    if (/rancho/.test(w)) { o = { w: 9, d: 6, floors: 1, wall: '#d9a066', roof: '#8a4b2a' }; fence = true; label = 'RANCHO' }
    if (/2 pisos|dos plantas/.test(w)) { o = { ...o, floors: 2 }; label = /pueblo/.test(w) ? 'CASA DE PUEBLO' : '2 PISOS' }
    if (/mansi/.test(w)) { o = { w: 9.5, d: 7, floors: 2, wall: '#ffffff', roof: '#3b3f4a', roofType: 'hip', balcony: true, porch: true }; pool = true; label = 'MANSIÓN + PISCINA' }
    else if (/piscina/.test(w)) { pool = true; label = 'CON PISCINA' }
    if (/moderna/.test(w)) { o = { floors: 2, wall: '#f5f5f5', roof: '#2f3540', roofType: 'hip' }; label = 'CASA MODERNA' }
    if (/granja/.test(w)) { o = { wall: '#b5432f', roof: '#5a3a2a' }; fence = true; label = 'GRANJA DE GALLINAS' }
    if (/huerto/.test(w)) { fence = true; label = 'HUERTO + TRACTOR' }
    if (/furgo/.test(w)) label = 'FURGO + PERROS'
    if (/tecnolog/.test(w)) { o = { wall: '#dfe8f2', roof: '#2d6cdf' }; label = 'CASA TECNOLÓGICA' }
    if (/chalet/.test(w) && !pool) label = 'CHALET'
    if (/batall/.test(w)) label = '¡UN BATALLÓN!'
    if (p.country === 'Brasil') label = 'BARRIO BRASIL'
    items.push({ key: p.name, lot, spec: spec(seed, o), iso: p.iso, name: p.name, label, sign, signColor: '#c2185b', pool, fence, delay: 0.25 + (k++) * 0.035, person: p })
  }
  const byName = Object.fromEntries(items.map((i) => [i.key, i]))
  const free = eu[ei + 1] ?? eu[eu.length - 1]
  for (const it of items) extraReserved.push({ x: it.lot.x, z: it.lot.z, r: 9 })
  for (const bx of BRIDGES) extraReserved.push({ x: bx, z: -60, r: 8 })
  return { items, byName, free, brazil: am[am.length - 1] }
}
const BRIDGES = [-45, 20, 85]
const LAYOUT = build() // at import time, so trees avoid every plot
;(globalThis as any).__ep1 = LAYOUT

const F = (l: Lot) => [Math.sin(l.rot), Math.cos(l.rot)]
/** point in front of a lot: f metres forward, r metres to the right, y height */
function at(l: Lot, f: number, r: number, y: number): [number, number, number] {
  const [fx, fz] = F(l)
  return [l.x + fx * f + fz * r, l.y + y, l.z + fz * f - fx * r]
}
const look = (l: Lot, y = 2.6): [number, number, number] => [l.x, l.y + y, l.z]

// ---------------------------------------------------------------- camera
function cameraKeys(): CamKey[] {
  const H = HOME_Y + 1.6
  const b = LAYOUT.byName
  const shot = (t0: number, t1: number, l: Lot, d = 13, r = 4, y = 4.5, cut = true): CamKey[] => [
    { t: t0, p: at(l, d + 9, r * 1.6, y + 3.5), l: look(l, 3.2), fov: 44, cut },
    { t: t1, p: at(l, d + 5, r * 1.2, y + 2.5), l: look(l, 3.0), fov: 42, e: 'linear' },
  ]
  const sup = LAYOUT.items.find((i) => i.sign === 'SUPERMERCADO')!.lot
  return [
    // S1 hook: Pizz at his door
    { t: 0, p: [1.6, 2.7, 10.4], l: [PZ.x, H - 0.05, PZ.z], fov: 38 },
    { t: 2.1, p: [0.7, 2.55, 8.9], l: [PZ.x, H - 0.05, PZ.z], fov: 35, e: 'linear' },
    // S2 reveal: crane up, houses pop
    { t: 2.2, p: [0, 3.6, 14], l: [0, 2.5, 0], fov: 45, cut: true },
    { t: 5.2, p: [70, 120, 175], l: [0, 0, -15], fov: 50, e: 'inOut' },
    // S3 the river splits the valley
    { t: 5.3, p: [-120, 60, 95], l: [-10, 0, -40], fov: 52, cut: true },
    { t: 11.3, p: [110, 60, 95], l: [10, 0, -40], fov: 52, e: 'linear' },
    // S4 infrastructure, then bridges
    { t: 11.4, p: at(sup, 20, -14, 7), l: look(sup, 3), fov: 46, cut: true },
    { t: A.l04 + 2.3, p: at(sup, 20, 14, 7), l: [sup.x - 15, sup.y + 3, sup.z], fov: 50, e: 'linear' },
    { t: A.l04 + 2.4, p: [-70, 22, -20], l: [20, 0, -62], fov: 50, cut: true },
    { t: 16.1, p: [-30, 18, -12], l: [40, 0, -62], fov: 50, e: 'linear' },
    // S5 Marina
    ...shot(16.2, 18.6, b.Marina.lot),
    // S6 Gabriel / Manuel / Rodrigo
    ...shot(18.7, A.l06 + 1.55, b.Gabriel.lot),
    ...shot(A.l06 + 1.6, A.l06 + 3.05, b.Manuel.lot),
    { t: A.l06 + 3.1, p: at(b.Rodrigo.lot, 24, -12, 9), l: look(b.Rodrigo.lot, 3), fov: 48, cut: true },
    { t: 24.9, p: at(b.Rodrigo.lot, 20, -6, 7.5), l: look(b.Rodrigo.lot, 3), fov: 46, e: 'linear' },
    // S7 Aleky
    ...shot(25.0, 28.05, b.Aleky.lot, 14, -3),
    // S8 cross to America over the central bridge, then the three wishes
    { t: 28.15, p: [20, 7, -30], l: [20, 2, -75], fov: 50, cut: true },
    { t: A.l08 + 1.05, p: [20, 7, -55], l: [15, 3, -90], fov: 50, e: 'linear' },
    ...shot(A.l08 + 1.1, A.l08 + 2.25, b.Fernando.lot, 15, 3, 5.5),
    ...shot(A.l08 + 2.3, A.l08 + 4.1, b.Kiker.lot, 15, -3, 5.5),
    ...shot(A.l08 + 4.15, 33.95, b.Thiago.lot, 17, 6, 7),
    // S9 Brasil
    ...shot(34.05, 38.55, b.Matheus.lot, 15, -4, 5),
    // S10 the score: high aerial
    { t: 38.65, p: [-150, 140, 120], l: [0, 0, -30], fov: 50, cut: true },
    { t: 44.3, p: [150, 150, 130], l: [0, 0, -30], fov: 50, e: 'linear' },
    // S11 Pizz asks for comments, then the free plot
    { t: 44.4, p: [1.4, 2.6, 10.0], l: [PZ.x, H - 0.05, PZ.z], fov: 38, cut: true },
    { t: 49.25, p: [0.5, 2.5, 8.6], l: [PZ.x, H - 0.05, PZ.z], fov: 34, e: 'linear' },
    { t: 49.35, p: [LAYOUT.free.x - 30, LAYOUT.free.y + 13, LAYOUT.free.z + 14], l: [LAYOUT.free.x + 8, LAYOUT.free.y + 3, LAYOUT.free.z - 2], fov: 50, cut: true },
    { t: 51.8, p: [LAYOUT.free.x - 24, LAYOUT.free.y + 11, LAYOUT.free.z + 11], l: [LAYOUT.free.x + 8, LAYOUT.free.y + 3, LAYOUT.free.z - 2], fov: 50, e: 'linear' },
    { t: 54.5, p: [60, 150, 200], l: [0, 0, -20], fov: 50, e: 'inOut' },
  ]
}

// ---------------------------------------------------------------- component
export function Ep001() {
  const { camera } = useThree()
  const lines = useMemo(() => useLines(EP001.id, EP001.script), [])
  const keys = useMemo(cameraKeys, [])
  const pizz = useMemo(newState, [])
  const P = useMemo(() => new THREE.Vector3(), [])
  const L = useMemo(() => new THREE.Vector3(), [])
  const camPos = useMemo(() => new THREE.Vector3(), [])
  const labels = useRef<THREE.Group>(null!)
  const marker = useRef<THREE.Group>(null!)
  const featured = ['Marina', 'Gabriel', 'Manuel', 'Rodrigo', 'Aleky', 'Fernando', 'Kiker', 'Thiago', 'Matheus']
  const fstates = useMemo(() => featured.map(() => newState()), [])
  const T = () => clock.t

  useMemo(() => {
    const pv = (window as any).__pv
    if (!pv) return
    pv.info = () => {
      const sfx: { type: string; at: number; g?: number }[] = [{ type: 'whoosh', at: 0.0, g: 0.5 }, { type: 'whoosh', at: 2.2, g: 0.6 }]
      LAYOUT.items.forEach((it, i) => { if (i % 2 === 0) sfx.push({ type: 'pop', at: 2.6 + it.delay + 0.3, g: 0.22 }) })
      for (const k of keys) if (k.cut && k.t > 3) sfx.push({ type: 'whoosh', at: k.t - 0.05, g: 0.3 })
      sfx.push({ type: 'chime', at: A.l05 + 0.2, g: 0.4 }, { type: 'chime', at: A.l07 + 1.6, g: 0.4 }, { type: 'chime', at: A.l09 + 2.4, g: 0.6 }, { type: 'chime', at: A.l10 + 1.2, g: 0.6 })
      return { id: EP001.id, duration: EP001.duration, lines: lines.map((l) => ({ id: l.id, at: l.at, dur: l.dur, text: l.text, words: l.words, hasAudio: l.hasAudio })), sfx }
    }
  }, [])

  useFrame(() => {
    const t = T()
    const fov = evalCam(keys, t, P, L)
    camera.position.copy(P); camera.lookAt(L)
    const pc = camera as THREE.PerspectiveCamera
    if (Math.abs(pc.fov - fov) > 0.01) { pc.fov = fov; pc.updateProjectionMatrix() }
    camPos.copy(P); (globalThis as any).__cam = [P.toArray(), L.toArray(), marker.current?.getWorldPosition(new THREE.Vector3()).toArray()]
    world.focus.set(L.x, 0, L.z)
    world.shadowSpan = THREE.MathUtils.clamp(P.distanceTo(L) * 0.9, 18, 120)

    // Pizz at his door
    pizz.x = PZ.x; pizz.z = PZ.z; pizz.y = HOME_Y; pizz.ry = 0.15; pizz.speed = 0
    pizz.lookAt = camPos; pizz.action = 'none'; pizz.actionW = 0; pizz.smile = 0.8
    if (t < 0.9) { pizz.action = 'surprise'; pizz.actionT = t; pizz.actionW = 1 - seg(t, 0.7, 0.9) }
    else if (t < 2.2) { pizz.action = 'celebrate'; pizz.actionT = t - 0.9; pizz.actionW = seg(t, 0.9, 1.05) }
    else if (t > 44.4 && t < 46.2) { pizz.action = 'point'; pizz.actionT = t; pizz.actionW = seg(t, 44.4, 44.7) * (1 - seg(t, 45.9, 46.2)) }
    else if (speakingAt(lines, t)) { pizz.action = 'talk'; pizz.actionT = t; pizz.actionW = 0.85 }
    pizz.mouth = mouthAt(lines, t)

    // featured inhabitants wave in front of their homes
    featured.forEach((n, i) => {
      const it = LAYOUT.byName[n], st = fstates[i]
      const [x, y, z] = at(it.lot, it.spec.d / 2 + 2.2, it.spec.w / 2 - 0.6, 0)
      st.x = x; st.z = z; st.y = y; st.speed = 0
      st.ry = it.lot.rot; st.lookAt = camPos; st.visible = t > 2.4 + it.delay + 0.6
      st.action = 'wave'; st.actionT = t + i; st.actionW = 1
    })

    labels.current.visible = (t > 5.3 && t < 11.4) || (t > 38.65 && t < 44.4)
    marker.current.visible = t > 49.3
    marker.current.scale.setScalar(Math.max(0.001, ease.outBack(seg(t, 49.4, 49.9))) * 1.5)
  }, -1)

  const pop = (d: number) => () => seg(T(), 2.6 + d, 3.3 + d)
  const fl = LAYOUT.free
  return (
    <group>
      <PizzHome />
      <Character look={PIZZ_LOOK} state={pizz} />
      {featured.map((n, i) => <Character key={n} look={lookFromSeed(hashString(n + 'look'))} state={fstates[i] as CharState} />)}
      {LAYOUT.items.map((it) => (
        <group key={it.key} position={[it.lot.x, it.lot.y, it.lot.z]} rotation-y={it.lot.rot}>
          <House spec={it.spec} getProgress={pop(it.delay)} flag={it.iso || null} />
          {it.pool && (
            <mesh position={[it.spec.w / 2 + 2.6, 0.08, 0.5]} material={mat('#3fb6e8', { rough: 0.15, emissive: '#1d8fc4', ei: 0.25 })}>
              <boxGeometry args={[3.2, 0.12, 4.4]} />
            </mesh>
          )}
          {it.fence && <Fence w={it.spec.w + 5} d={it.spec.d + 5} />}
        </group>
      ))}
      {LAYOUT.items.map((it) => (
        <group key={'t' + it.key}>
            <group position={[it.lot.x, it.lot.y + it.spec.wallH * it.spec.floors + 3.8, it.lot.z]} scale={1.6}>
            {it.name && <NameTag name={it.name} iso={it.iso} />}
            {it.label && <Tag text={it.label} y={-0.62} color="#ffd23d" />}
            {it.sign && <Tag text={it.sign} y={it.name ? 0.75 : 0} color="#ffffff" bg={it.signColor} big />}
          </group>
        </group>
      ))}
      {BRIDGES.map((bx) => <Bridge key={bx} x={bx} />)}
      <group ref={labels}>
        <BigLabel text="EUROPA" position={[0, 22, 22]} color="#ffd23d" />
        <BigLabel text="AMÉRICA" position={[10, 26, -100]} color="#7fe0ff" />
      </group>
      <group ref={marker} position={[fl.x, fl.y + 4, fl.z]}>
        <PlotMarker />
      </group>
    </group>
  )
}

