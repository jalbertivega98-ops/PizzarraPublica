// Kit común de COSAS DE PAREJA (low-poly): poses, pistas, lip-sync, cámara, salón y un episodio genérico.
// Cada episodio solo define guion (voz/<id>.json), poses por tiempo, cortes de cámara, sfx y rótulos.
import { useMemo, useRef, type ReactNode } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { RoundedBox } from '@react-three/drei'
import * as THREE from 'three'
import { clock, ease, seg } from '../engine/clock'
import { useLines, type Line } from '../engine/voice'
import { LowPolyChar, P0, mixPose, type LPLook, type LPPose } from '../scene/LowPoly'

export const DANI: LPLook = { skin: '#e9b48e', hair: '#1e1a1c', top: '#2f8f83', hairStyle: 'dani' }
export const LUCIA: LPLook = { skin: '#f1c3a0', hair: '#a4482a', top: '#f08aa6', hairStyle: 'lucia' }

export const pose = (o: Partial<LPPose>): LPPose => ({ ...P0, ...o })
export const endOf = (l: Line) => l.at + l.dur

export function track(keys: [number, LPPose][], t: number, blend = 0.3): LPPose {
  let i = 0
  while (i + 1 < keys.length && t >= keys[i + 1][0]) i++
  const cur = keys[i][1]
  const prev = i > 0 ? keys[i - 1][1] : cur
  const k = i > 0 ? ease.inOut(seg(t, keys[i][0], keys[i][0] + blend)) : 1
  return mixPose(prev, cur, k)
}

const VOW = /[aeiouáéíóúü]/gi
export function lip(l: Line | undefined, t: number) {
  if (!l) return 0
  const lt = t - l.at
  if (lt < 0 || lt > l.dur) return 0
  for (const w of l.words) if (lt >= w.t && lt <= w.t + w.d) {
    const syl = Math.max(1, (w.w.match(VOW) ?? []).length)
    return 0.15 + 0.85 * Math.pow(Math.abs(Math.sin(((lt - w.t) / w.d) * syl * Math.PI)), 0.7)
  }
  return 0
}
/** silent "talking" mouth for the one who doesn't have the voice */
export const flap = (t: number) => 0.12 + 0.45 * Math.abs(Math.sin(t * 9.3)) * (Math.sin(t * 2.1) > -0.4 ? 1 : 0)

export type Shot = { p: [number, number, number]; l: [number, number, number]; fov: number; push?: number }
export const POP = '\\t(0,180,\\fscx112\\fscy112)\\t(180,360,\\fscx100\\fscy100)'
export type Overlay = { a: number; b: number; st: string; tx: string }
export const box = (a: number, b: number, y: number, size: number, tx: string, an = 5): Overlay =>
  ({ a, b, st: 'Box', tx: `{\\an${an}\\pos(540,${y})\\fad(80,120)${POP}\\fs${size}}${tx}` })

// ---------------- living room (sofa + blanket, TV light from the camera side)
export function LivingRoom({ tv }: { tv?: () => number }) {
  const tvL = useRef<THREE.PointLight>(null!)
  useFrame(() => {
    const t = clock.t
    const k = tv ? tv() : 1
    tvL.current.intensity = k * (2.2 + 0.5 * Math.sin(t * 7.3) * Math.sin(t * 2.9 + 1) + 0.25 * Math.sin(t * 13.1))
  })
  const fm = (c: string, r = 0.9) => new THREE.MeshStandardMaterial({ color: c, roughness: r, flatShading: true })
  const wall = fm('#6e4a63'), sofa = fm('#3e5f8f'), cush = fm('#4b6ea3'), wood = fm('#8a5a34', 0.7), blanket = fm('#e0a63c')
  return (
    <group>
      <hemisphereLight args={['#ffe6cc', '#2c2230', 0.95]} />
      <directionalLight position={[-2, 3.5, 3]} intensity={1.1} color="#ffe2c2" castShadow shadow-mapSize={[2048, 2048]} shadow-bias={-0.0005}
        shadow-camera-left={-3} shadow-camera-right={3} shadow-camera-top={3} shadow-camera-bottom={-3} />
      <pointLight position={[0, 1.9, 2.4]} intensity={1.6} distance={6} color="#ffe6d2" />
      <pointLight ref={tvL} position={[0.2, 1.1, 2.0]} distance={5} decay={1.4} color="#8fb6ff" />
      <pointLight position={[-1.55, 1.65, -0.7]} intensity={3} distance={3.5} decay={1.6} color="#ffb766" />
      {/* walls & floor */}
      <mesh position={[0, 1.6, -1.05]} material={wall} receiveShadow><planeGeometry args={[8, 3.4]} /></mesh>
      <mesh rotation-x={-Math.PI / 2} material={fm('#7a5538', 0.8)} receiveShadow><planeGeometry args={[8, 8]} /></mesh>
      <mesh rotation-x={-Math.PI / 2} position={[0, 0.005, 0.6]} material={fm('#c9b8a3')} receiveShadow><circleGeometry args={[1.5, 10]} /></mesh>
      {/* framed pictures */}
      <group position={[0.15, 1.95, -1.03]}>
        <mesh material={fm('#2b2224')}><boxGeometry args={[0.95, 0.62, 0.04]} /></mesh>
        <mesh position={[0, 0, 0.025]} material={fm('#f2d7a6')}><planeGeometry args={[0.85, 0.52]} /></mesh>
        <mesh position={[-0.15, -0.05, 0.03]} material={fm('#e2725b')}><circleGeometry args={[0.15, 7]} /></mesh>
        <mesh position={[0.18, 0.06, 0.031]} rotation-z={0.4} material={fm('#3b7f8c')}><planeGeometry args={[0.28, 0.2]} /></mesh>
      </group>
      <group position={[1.15, 1.75, -1.03]}>
        <mesh material={fm('#2b2224')}><boxGeometry args={[0.38, 0.48, 0.04]} /></mesh>
        <mesh position={[0, 0, 0.025]} material={fm('#bfe0d0')}><planeGeometry args={[0.3, 0.4]} /></mesh>
      </group>
      {/* sofa */}
      <group position={[0, 0, -0.45]}>
        <mesh position={[0, 0.2, 0]} material={sofa} castShadow receiveShadow><boxGeometry args={[2.3, 0.4, 0.95]} /></mesh>
        <mesh position={[0, 0.72, -0.38]} material={sofa} castShadow receiveShadow><boxGeometry args={[2.3, 0.65, 0.22]} /></mesh>
        {[-1.17, 1.17].map((x) => <RoundedBox key={x} args={[0.26, 0.62, 0.98]} radius={0.06} smoothness={2} position={[x, 0.4, 0.01]} material={sofa} castShadow receiveShadow />)}
        {[-0.52, 0.52].map((x) => <RoundedBox key={x} args={[1.02, 0.17, 0.78]} radius={0.06} smoothness={2} position={[x, 0.48, 0.06]} material={cush} castShadow receiveShadow />)}
        {[-0.52, 0.52].map((x) => <RoundedBox key={x} args={[0.98, 0.5, 0.16]} radius={0.07} smoothness={2} position={[x, 0.82, -0.22]} rotation-x={-0.12} material={cush} castShadow />)}
        <RoundedBox args={[0.34, 0.34, 0.12]} radius={0.06} smoothness={2} position={[-0.95, 0.72, -0.1]} rotation={[-0.2, 0.3, 0.2]} material={fm('#f2d7a6')} castShadow />
      </group>
      {/* blanket over both laps */}
      <RoundedBox args={[1.95, 0.2, 0.8]} radius={0.08} smoothness={2} position={[0, 0.66, -0.05]} material={blanket} castShadow receiveShadow />
      <RoundedBox args={[1.9, 0.12, 0.42]} radius={0.05} smoothness={2} position={[0, 0.6, 0.38]} rotation-x={0.25} material={blanket} castShadow receiveShadow />
      {[-0.42, 0.42].map((x) => <RoundedBox key={x} args={[0.5, 0.08, 0.6]} radius={0.04} smoothness={2} position={[x, 0.75, 0.25]} material={blanket} />)}
      {/* floor lamp + plant */}
      <group position={[-1.6, 0, -0.75]}>
        <mesh position={[0, 0.8, 0]} material={fm('#2b2224')}><cylinderGeometry args={[0.02, 0.02, 1.6, 6]} /></mesh>
        <mesh position={[0, 0.02, 0]} material={fm('#2b2224')}><cylinderGeometry args={[0.16, 0.18, 0.04, 8]} /></mesh>
        <mesh position={[0, 1.66, 0]}><cylinderGeometry args={[0.13, 0.2, 0.26, 8, 1, true]} /><meshStandardMaterial color="#fbe9c8" emissive="#ffb766" emissiveIntensity={1.1} side={THREE.DoubleSide} flatShading /></mesh>
      </group>
      <group position={[1.65, 0, -0.7]}>
        <mesh position={[0, 0.2, 0]} material={fm('#c46a4a')}><cylinderGeometry args={[0.16, 0.12, 0.4, 8]} /></mesh>
        {[0, 1, 2, 3, 4].map((i) => <mesh key={i} position={[Math.cos(i * 1.3) * 0.12, 0.62 + (i % 2) * 0.15, Math.sin(i * 1.3) * 0.1]} material={fm('#3f8a4f')}><icosahedronGeometry args={[0.17, 0]} /></mesh>)}
      </group>
      {/* coffee table with a bowl */}
      <group position={[0, 0, 1.25]}>
        <mesh position={[0, 0.36, 0]} material={wood} castShadow receiveShadow><boxGeometry args={[1.3, 0.06, 0.6]} /></mesh>
        {[[-0.58, -0.25], [0.58, -0.25], [-0.58, 0.25], [0.58, 0.25]].map(([x, z], i) => <mesh key={i} position={[x, 0.17, z]} material={wood}><boxGeometry args={[0.06, 0.34, 0.06]} /></mesh>)}
        <mesh position={[-0.3, 0.45, 0]} material={fm('#e8e2d8')}><sphereGeometry args={[0.13, 9, 5, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2]} /></mesh>
        {[0, 1, 2, 3, 4, 5].map((i) => <mesh key={i} position={[-0.3 + Math.cos(i) * 0.07, 0.46, Math.sin(i) * 0.06]} material={fm('#fff3c4')}><icosahedronGeometry args={[0.035, 0]} /></mesh>)}
        <mesh position={[0.3, 0.4, 0.05]} rotation={[-Math.PI / 2, 0, 0.4]} material={fm('#1a1a22', 0.4)}><boxGeometry args={[0.1, 0.22, 0.02]} /></mesh>
      </group>
    </group>
  )
}

export function Phone() {
  return (
    <group rotation={[0.3, 0, 0]}>
      <mesh position={[0, -0.02, 0.06]} rotation={[-0.2, 0, 0]}><boxGeometry args={[0.085, 0.16, 0.012]} /><meshStandardMaterial color="#1a1a22" roughness={0.4} /></mesh>
      <mesh position={[0, -0.02, 0.067]} rotation={[-0.2, 0, 0]}><planeGeometry args={[0.072, 0.14]} /><meshBasicMaterial color="#9fd0ff" toneMapped={false} /></mesh>
    </group>
  )
}

// ---------------- generic episode
export type PairFrame = { dani: LPPose; lucia: LPPose; cuts: [number, string][] }
export type PairSpec = {
  id: string
  script: { id: string; text: string }[]
  gap: Record<string, number>
  her: string[] // lines spoken by Lucía (narrator imitating her)
  bg: string
  Set: (p: { st: Record<string, any> }) => ReactNode
  pos: { lucia: [number, number, number]; dani: [number, number, number] }
  shots: Record<string, Shot>
  frame: (t: number, a: (id: string) => number, l: (id: string) => Line, st: Record<string, any>) => PairFrame
  sfx: (l: (id: string) => Line) => { type: string; at: number; g?: number }[]
  overlays: (l: (id: string) => Line, dur: number) => Overlay[]
  music?: string
  tail?: number
  luciaHand?: ReactNode
  daniHand?: ReactNode
  extras?: (st: Record<string, any>) => ReactNode
}

export function PairEpisode({ spec }: { spec: PairSpec }) {
  const { camera, scene } = useThree()
  const lines = useMemo(() => useLines(spec.id, spec.script.map((s, i) => ({ ...s, at: i * 3 }))), [])
  const L = (id: string) => lines.find((l) => l.id === id)!
  const P = useMemo(() => new THREE.Vector3(), [])
  const LK = useMemo(() => new THREE.Vector3(), [])
  const poses = useRef({ dani: P0, lucia: P0 })
  const st = useRef<Record<string, any>>({}).current
  useMemo(() => { scene.background = new THREE.Color(spec.bg); scene.fog = null }, [])

  const layout = () => {
    for (let i = 0; i < lines.length; i++) lines[i].at = i === 0 ? 0.6 : lines[i - 1].at + lines[i - 1].dur + 0.12 + 0.55 * (spec.gap[lines[i].id] ?? 0)
  }
  const duration = () => { layout(); return Math.ceil((endOf(lines[lines.length - 1]) + (spec.tail ?? 2.2)) * 10) / 10 }

  useMemo(() => {
    const pv = (window as any).__pv
    if (!pv) return
    pv.info = () => {
      layout()
      const d = duration()
      return { id: spec.id, duration: d, music: spec.music ?? 'night', subStyle: 'box', overlays: spec.overlays(L, d), lines: lines.map((x) => ({ id: x.id, at: x.at, dur: x.dur, text: x.text, words: x.words, hasAudio: x.hasAudio })), sfx: spec.sfx(L) }
    }
  }, [])

  useFrame(() => {
    layout()
    const t = clock.t
    const a = (id: string) => L(id).at
    const f = spec.frame(t, a, L, st)
    const lucia = f.lucia, dani = f.dani
    const m = Math.max(...spec.her.map((id) => lip(L(id), t)))
    lucia.mouth = Math.max(lucia.mouth, m)
    const blink = (off: number) => ((t + off) % 4.1) < 0.12 ? 1 : 0
    if (lucia.lids < 0.6) lucia.lids = Math.max(lucia.lids, blink(1.3))
    if (dani.lids < 0.6 && !st.noBlink) dani.lids = Math.max(dani.lids, blink(0.2))
    poses.current.dani = dani; poses.current.lucia = lucia

    let ci = 0
    while (ci + 1 < f.cuts.length && t >= f.cuts[ci + 1][0]) ci++
    const [c0, name] = f.cuts[ci]
    const c1 = ci + 1 < f.cuts.length ? f.cuts[ci + 1][0] : c0 + 5
    const sh = spec.shots[name]
    P.set(...sh.p); LK.set(...sh.l)
    const dir = LK.clone().sub(P).normalize()
    P.addScaledVector(dir, (sh.push ?? 0) * ease.out(seg(t, c0, c1 + 0.5)))
    P.x += Math.sin(t * 0.7) * 0.006; P.y += Math.sin(t * 1.1 + 1) * 0.005
    camera.position.copy(P); camera.lookAt(LK)
    const pc = camera as THREE.PerspectiveCamera
    if (Math.abs(pc.fov - sh.fov) > 0.01) { pc.fov = sh.fov; pc.updateProjectionMatrix() }
  }, -1)

  return (
    <group>
      {spec.Set({ st })}
      <LowPolyChar look={LUCIA} pose={() => poses.current.lucia} position={spec.pos.lucia} hand={spec.luciaHand} topColor={() => st.luciaTop} />
      <LowPolyChar look={DANI} pose={() => poses.current.dani} position={spec.pos.dani} hand={spec.daniHand} topColor={() => st.daniTop} />
      {spec.extras?.(st)}
    </group>
  )
}

/** standard shots for a couple sitting side by side (she left, he right) with head height hy and depth z */
export function coupleShots(hy: number, z: number): Record<string, Shot> {
  return {
    two: { p: [0, hy + 0.2, z + 2.65], l: [0, hy - 0.13, z], fov: 44, push: 0.2 },
    wide: { p: [0, hy + 0.55, z + 3.6], l: [0, hy - 0.3, z], fov: 48, push: 0.25 },
    lucia: { p: [-0.1, hy + 0.12, z + 1.85], l: [-0.42, hy - 0.08, z], fov: 38, push: 0.12 },
    dani: { p: [0.1, hy + 0.12, z + 1.85], l: [0.42, hy - 0.08, z], fov: 38, push: 0.12 },
    luciaTight: { p: [-0.36, hy + 0.08, z + 1.5], l: [-0.42, hy - 0.02, z], fov: 36, push: 0.08 },
    daniTight: { p: [0.36, hy + 0.08, z + 1.5], l: [0.42, hy - 0.02, z], fov: 36, push: 0.08 },
  }
}

/** Beat-driven frame: one entry per line id → Dani pose, Lucía pose, camera shot (keys at line start + offsets). */
export type Beat = { d?: LPPose; l?: LPPose; cut?: string; dAt?: number; lAt?: number; cutAt?: number; flap?: boolean; dMid?: LPPose; lMid?: LPPose }
export function beatFrame(order: string[], beats: Record<string, Beat>, d0: LPPose, l0: LPPose, cut0 = 'wide', blend = 0.3) {
  return (t: number, a: (id: string) => number, l: (id: string) => Line) => {
    const dk: [number, LPPose][] = [[0, d0]], lk: [number, LPPose][] = [[0, l0]], cuts: [number, string][] = [[0, cut0]]
    for (const id of order) {
      const b = beats[id]; if (!b) continue
      const s = a(id), du = l(id).dur
      if (b.d) dk.push([s + (b.dAt ?? 0), b.d])
      if (b.dMid) dk.push([s + du * 0.5, b.dMid])
      if (b.l) lk.push([s - 0.15 + (b.lAt ?? 0), b.l])
      if (b.lMid) lk.push([s + du * 0.5, b.lMid])
      if (b.cut) cuts.push([s - 0.1 + (b.cutAt ?? 0), b.cut])
    }
    const by = (x: [number, any], y: [number, any]) => x[0] - y[0]
    dk.sort(by); lk.sort(by); cuts.sort(by)
    const dani = track(dk, t, blend), lucia = track(lk, t, blend)
    for (const id of order) { const b = beats[id]; if (b?.flap && t > a(id) + 0.1 && t < endOf(l(id))) dani.mouth = flap(t) }
    return { dani, lucia, cuts }
  }
}

/** a thing that is visible only while show() is true */
export function Show({ show, children }: { show: () => boolean; children: ReactNode }) {
  const g = useRef<THREE.Group>(null!)
  useFrame(() => { g.current.visible = show() })
  return <group ref={g}>{children}</group>
}
