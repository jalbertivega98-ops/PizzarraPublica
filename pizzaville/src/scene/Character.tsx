import { useMemo, useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'
import { RoundedBox } from '@react-three/drei'
import { mat } from './materials'
import { blob, merge, paint, T } from './geom'
import { mulberry32, pick } from '../world/rng'
import { clock } from '../engine/clock'

// ============================================================ look
export type Look = {
  skin: string; hair: string; hairStyle: number; top: string; topDark: string; pants: string; shoes: string; accent: string
  logo?: 'pizza' | null; hardhat?: boolean; vest?: boolean; eye?: string
}

/** Master model of Pizz — never change these values (identity of the series). */
export const PIZZ_LOOK: Look = {
  skin: '#f1c39f', hair: '#5b3622', hairStyle: 0, top: '#ec6a3f', topDark: '#c9502c', pants: '#3d5170', shoes: '#f6f4ee', accent: '#ec6a3f', logo: 'pizza', eye: '#4a3020',
}

const SKINS = ['#f6d3b8', '#f1c39f', '#e2a97e', '#c98b61', '#a86c45', '#8a5636', '#6b3f27']
const HAIRS = ['#2a1d16', '#4a2f1f', '#6e4a2c', '#a5733f', '#d9b36c', '#1c1c1f', '#8c3f22', '#b8b2a8']
const TOPS = ['#4f86c6', '#58a776', '#e0b440', '#a368c2', '#e57373', '#47a5a5', '#f08c4b', '#6c7a89', '#d65a84', '#f2efe6']
const PANTS = ['#3d5170', '#2f3640', '#6b5843', '#4c6b4a', '#7a7f8a', '#2b3b55']

/** appearance from an internal seed only (never from comment data) */
export function lookFromSeed(seed: number): Look {
  const r = mulberry32(seed ^ 0x9e3779b9)
  const top = new THREE.Color(pick(r, TOPS))
  return {
    skin: pick(r, SKINS), hair: pick(r, HAIRS), hairStyle: 1 + Math.floor(r() * 3),
    top: '#' + top.getHexString(), topDark: '#' + top.clone().multiplyScalar(0.8).getHexString(),
    pants: pick(r, PANTS), shoes: pick(r, ['#f6f4ee', '#2f2f35', '#b5543c', '#4f7fa8']), accent: pick(r, TOPS), logo: null, eye: pick(r, ['#3b2a20', '#2f4a6a', '#3f5a33', '#5a3a22']),
  }
}

export const WORKER_LOOK = (seed: number): Look => ({ ...lookFromSeed(seed), top: '#f08a24', topDark: '#d06f12', pants: '#3a4a63', hardhat: true, vest: true })

// ============================================================ state
export type Action = 'none' | 'wave' | 'point' | 'surprise' | 'celebrate' | 'talk' | 'hammer' | 'shrug'
export type CharState = {
  x: number; y: number; z: number; ry: number
  speed: number // m/s → walk/run blend
  phase: number // locomotion phase (radians)
  action: Action; actionT: number; actionW: number
  lookAt: THREE.Vector3 | null
  mouth: number; smile: number; brows: number // brows: -1 angry .. 0 .. 1 surprised
  visible: boolean
}
export const newState = (): CharState => ({ x: 0, y: 0, z: 0, ry: 0, speed: 0, phase: 0, action: 'none', actionT: 0, actionW: 0, lookAt: null, mouth: 0, smile: 0.6, brows: 0, visible: true })

// ============================================================ geometry
function pizzaLogo() {
  const parts: THREE.BufferGeometry[] = []
  const sh = new THREE.Shape()
  sh.moveTo(-0.055, 0.035); sh.lineTo(0.055, 0.035); sh.lineTo(0, -0.07); sh.lineTo(-0.055, 0.035)
  parts.push(paint(new THREE.ShapeGeometry(sh), '#ffd34d'))
  parts.push(paint(T(new THREE.BoxGeometry(0.13, 0.03, 0.01), 0, 0.045, 0.003), '#e0a95a'))
  ;[[-0.018, 0.012], [0.02, 0.0], [0.0, -0.035]].forEach(([x, y]) => parts.push(paint(T(new THREE.CircleGeometry(0.013, 10), x, y, 0.002), '#d23b2f')))
  return merge(parts)
}

function hairGeo(style: number, color: string) {
  const parts: THREE.BufferGeometry[] = []
  const c = new THREE.Color(color)
  const cap = new THREE.SphereGeometry(0.214, 26, 16, 0, Math.PI * 2, 0, Math.PI * 0.56)
  T(cap, 0, 0.012, -0.012, -0.32, 0, 0)
  parts.push(paint(cap, c, { jitter: 0.04 }))
  const r = mulberry32(style * 101 + 7)
  if (style === 0) {
    // Pizz: short, slightly messy — tufts swept up and to the side
    const tufts: [number, number, number, number, number, number][] = [
      [0.0, 0.2, 0.1, 0.08, -0.5, 0.2], [0.07, 0.19, 0.09, 0.07, -0.4, -0.5], [-0.08, 0.18, 0.1, 0.07, -0.6, 0.6],
      [0.03, 0.22, 0.02, 0.08, 0.2, 0.1], [-0.05, 0.215, -0.04, 0.075, 0.3, 0.4], [0.1, 0.17, -0.02, 0.07, 0.1, -0.7],
      [-0.12, 0.15, 0.03, 0.065, -0.2, 0.9], [0.13, 0.13, 0.06, 0.06, -0.3, -0.9], [0.0, 0.17, -0.12, 0.08, 0.6, 0.0],
      [0.15, 0.08, -0.06, 0.055, 0, -1.2], [-0.15, 0.08, -0.06, 0.055, 0, 1.2], [0.05, 0.16, 0.14, 0.05, -1.0, -0.2],
    ]
    tufts.forEach(([x, y, z, s, rx, rz], i) => {
      const g = new THREE.ConeGeometry(s * 0.75, s * 2.1, 7)
      T(g, 0, s * 0.6, 0)
      T(g, x, y, z, rx, 0, rz)
      parts.push(paint(g, c.clone().offsetHSL(0, 0, (i % 3) * 0.02 - 0.02), { jitter: 0.04 }))
      parts.push(paint(T(blob(s * 0.8, 1, 0.15, i), x * 0.98, y * 0.96, z * 0.96), c, { jitter: 0.03 }))
    })
    // fringe
    parts.push(paint(T(blob(0.09, 1, 0.2, 3, 0.6), 0.04, 0.155, 0.135, 0.3, 0, -0.3), c))
  } else {
    const n = style === 1 ? 10 : style === 2 ? 16 : 6
    for (let i = 0; i < n; i++) {
      const a = r() * Math.PI * 2, el = 0.35 + r() * 0.9
      const x = Math.cos(a) * Math.cos(el) * 0.19, y = Math.sin(el) * 0.19 + 0.02, z = Math.sin(a) * Math.cos(el) * 0.19 - 0.02
      parts.push(paint(T(blob(0.06 + r() * 0.04, 1, 0.2, i, 0.8), x, y, z), c, { jitter: 0.04 }))
    }
    if (style === 2) {
      // longer hair at the back
      parts.push(paint(T(blob(0.17, 2, 0.08, 4, 1.35), 0, -0.05, -0.07), c, { jitter: 0.04 }))
    }
  }
  return merge(parts)
}

// ============================================================ poses
type J = 'hips' | 'chest' | 'neck' | 'head' | 'lSh' | 'lEl' | 'rSh' | 'rEl' | 'lHip' | 'lKn' | 'rHip' | 'rKn' | 'lFt' | 'rFt'
type Pose = Record<J, [number, number, number]> & { lift: number }
const JOINTS: J[] = ['hips', 'chest', 'neck', 'head', 'lSh', 'lEl', 'rSh', 'rEl', 'lHip', 'lKn', 'rHip', 'rKn', 'lFt', 'rFt']
const zero = (): Pose => Object.assign(Object.fromEntries(JOINTS.map((j) => [j, [0, 0, 0]])) as Record<J, [number, number, number]>, { lift: 0 })

function locomotion(st: CharState, t: number): Pose {
  const p = zero()
  const sp = st.speed
  const walkW = Math.min(1, sp / 1.2)
  const runW = Math.min(1, Math.max(0, (sp - 2) / 2))
  const A = 0.55 * walkW + 0.35 * runW
  const ph = st.phase
  // idle breathing & weight shift
  const br = Math.sin(t * 1.9) * 0.025 * (1 - walkW)
  p.chest[0] = br + 0.25 * runW
  p.hips[2] = Math.sin(t * 0.7) * 0.025 * (1 - walkW)
  p.lSh[2] = 0.09; p.rSh[2] = -0.09
  p.lEl[0] = -0.12; p.rEl[0] = -0.12
  // legs
  p.lHip[0] = -Math.sin(ph) * A
  p.rHip[0] = Math.sin(ph) * A
  p.lKn[0] = Math.max(0, Math.sin(ph + 1.4)) * (0.7 * walkW + 0.7 * runW)
  p.rKn[0] = Math.max(0, Math.sin(ph + 1.4 + Math.PI)) * (0.7 * walkW + 0.7 * runW)
  p.lFt[0] = -p.lKn[0] * 0.3; p.rFt[0] = -p.rKn[0] * 0.3
  // arms swing opposite
  p.lSh[0] = Math.sin(ph) * A * 0.85
  p.rSh[0] = -Math.sin(ph) * A * 0.85
  p.lEl[0] -= 0.25 * walkW + 0.9 * runW
  p.rEl[0] -= 0.25 * walkW + 0.9 * runW
  p.hips[1] = Math.sin(ph) * 0.08 * walkW
  p.chest[1] = -Math.sin(ph) * 0.12 * walkW
  p.lift = Math.abs(Math.cos(ph)) * (0.035 * walkW + 0.07 * runW) - 0.02 * walkW
  return p
}

function actionPose(a: Action, t: number, p: Pose) {
  const o = zero()
  const copy = (j: J) => (o[j] = [...p[j]] as [number, number, number])
  JOINTS.forEach(copy)
  o.lift = p.lift
  switch (a) {
    case 'wave':
      o.rSh = [-0.25, 0.1, -2.55]
      o.rEl = [0, 0, -0.55 + Math.sin(t * 10) * 0.55]
      o.head = [-0.05, 0, 0.12 + Math.sin(t * 5) * 0.04]
      o.chest[2] = 0.05
      break
    case 'point':
      o.rSh = [-1.45, -0.2, -0.25]
      o.rEl = [-0.05, 0, 0]
      o.lSh = [0.1, 0, 0.25]
      o.chest[1] = -0.15
      break
    case 'surprise': {
      const k = Math.min(1, t * 6)
      o.lSh = [-0.6 * k, 0, 1.0 * k]; o.rSh = [-0.6 * k, 0, -1.0 * k]
      o.lEl = [-1.3 * k, 0, 0]; o.rEl = [-1.3 * k, 0, 0]
      o.chest[0] = -0.12 * k
      o.head = [-0.12 * k, 0, 0]
      o.lift = Math.max(0, Math.sin(Math.min(1, t * 3) * Math.PI)) * 0.12
      break
    }
    case 'celebrate': {
      const j = Math.max(0, Math.sin(t * 7.5))
      o.lift = j * 0.32
      o.lSh = [-0.2, 0, 2.6 + Math.sin(t * 15) * 0.15]; o.rSh = [-0.2, 0, -2.6 - Math.sin(t * 15) * 0.15]
      o.lEl = [0, 0, 0.3]; o.rEl = [0, 0, -0.3]
      o.lKn = [j * 0.6, 0, 0]; o.rKn = [j * 0.6, 0, 0]
      o.lHip = [-j * 0.3, 0, 0]; o.rHip = [-j * 0.3, 0, 0]
      o.head = [-0.15, 0, 0]
      break
    }
    case 'talk': {
      const g1 = Math.sin(t * 2.3), g2 = Math.sin(t * 1.7 + 1)
      o.rSh = [-0.55 + g1 * 0.2, 0, -0.35 - g2 * 0.1]
      o.rEl = [-0.9 - g1 * 0.3, 0, 0]
      o.lSh = [-0.4 + g2 * 0.18, 0, 0.3 + g1 * 0.08]
      o.lEl = [-0.8 + g2 * 0.25, 0, 0]
      o.head = [Math.sin(t * 3.1) * 0.06, Math.sin(t * 1.3) * 0.1, Math.sin(t * 2.1) * 0.04]
      o.chest[1] = Math.sin(t * 1.1) * 0.06
      break
    }
    case 'hammer': {
      const h = Math.sin(t * 9)
      o.rSh = [-1.2 - h * 0.6, 0, -0.2]
      o.rEl = [-0.8 + h * 0.5, 0, 0]
      o.chest[0] = 0.35
      o.lKn = [0.5, 0, 0]; o.rKn = [0.5, 0, 0]; o.lHip = [-0.4, 0, 0]; o.rHip = [-0.4, 0, 0]
      o.lift = -0.08
      break
    }
    case 'shrug':
      o.lSh = [-0.3, 0, 0.7]; o.rSh = [-0.3, 0, -0.7]; o.lEl = [-1.4, 0, 0]; o.rEl = [-1.4, 0, 0]; o.head = [0, 0, 0.18]
      break
  }
  return o
}

// ============================================================ component
export function Character({ look, state, scale = 1, shadow = true }: { look: Look; state: CharState; scale?: number; shadow?: boolean }) {
  const refs = useRef<Partial<Record<J, THREE.Group>>>({})
  const root = useRef<THREE.Group>(null!)
  const mouthOpen = useRef<THREE.Mesh>(null!)
  const smile = useRef<THREE.Mesh>(null!)
  const eyes = useRef<THREE.Group>(null!)
  const browL = useRef<THREE.Mesh>(null!)
  const browR = useRef<THREE.Mesh>(null!)
  const finger = useRef<THREE.Mesh>(null!)
  const hair = useMemo(() => hairGeo(look.hairStyle, look.hair), [look.hairStyle, look.hair])
  const logo = useMemo(() => (look.logo === 'pizza' ? pizzaLogo() : null), [look.logo])
  const tmpV = useMemo(() => new THREE.Vector3(), [])
  const seed = useMemo(() => Math.random() * 10, [])

  const M = {
    skin: mat(look.skin, { rough: 0.65 }), hair: mat('#ffffff', { vc: true, rough: 0.8 }), top: mat(look.top, { rough: 0.85 }), topD: mat(look.topDark, { rough: 0.85 }),
    pants: mat(look.pants, { rough: 0.9 }), shoes: mat(look.shoes, { rough: 0.6 }), accent: mat(look.accent, { rough: 0.6 }), sole: mat('#e9e6df', { rough: 0.7 }),
    white: mat('#ffffff', { rough: 0.3 }), iris: mat(look.eye ?? '#3b2a20', { rough: 0.3 }), pupil: mat('#111111', { rough: 0.2 }), brow: mat(new THREE.Color(look.hair).multiplyScalar(0.7).getStyle(), { rough: 0.8 }),
    mouth: mat('#6d2a2c', { rough: 0.6 }), lip: mat(new THREE.Color(look.skin).multiplyScalar(0.72).getStyle(), { rough: 0.6 }), cheek: mat('#f08f86', { rough: 0.9, transparent: true, opacity: 0.35 }),
    hat: mat('#f4c430', { rough: 0.45 }), vest: mat('#d9f24a', { rough: 0.6 }), vc: mat('#ffffff', { vc: true, rough: 0.6 }),
  }
  const r = (j: J) => (g: THREE.Group | null) => { if (g) refs.current[j] = g }
  const C = shadow

  useFrame(() => {
    const st = state
    const t = clock.t + seed
    root.current.visible = st.visible
    if (!st.visible) return
    root.current.position.set(st.x, st.y, st.z)
    root.current.rotation.y = st.ry
    let pose = locomotion(st, t)
    if (st.action !== 'none' && st.actionW > 0) {
      const ap = actionPose(st.action, st.actionT, pose)
      const w = st.actionW
      const out = zero()
      JOINTS.forEach((j) => { out[j] = [0, 1, 2].map((k) => pose[j][k] + (ap[j][k] - pose[j][k]) * w) as [number, number, number] })
      out.lift = pose.lift + (ap.lift - pose.lift) * w
      pose = out
    }
    // head look-at (yaw/pitch in local space)
    if (st.lookAt) {
      tmpV.copy(st.lookAt)
      root.current.worldToLocal(tmpV)
      tmpV.y -= 1.55
      const yaw = THREE.MathUtils.clamp(Math.atan2(tmpV.x, tmpV.z), -1.1, 1.1)
      const pitch = THREE.MathUtils.clamp(-Math.atan2(tmpV.y, Math.hypot(tmpV.x, tmpV.z)), -0.7, 0.45)
      pose.neck[1] += yaw * 0.45; pose.head[1] += yaw * 0.55
      pose.neck[0] += pitch * 0.4; pose.head[0] += pitch * 0.6
    }
    JOINTS.forEach((j) => { const g = refs.current[j]; if (g) g.rotation.set(pose[j][0], pose[j][1], pose[j][2]) })
    refs.current.hips!.position.y = 0.86 + pose.lift
    // face
    const m = THREE.MathUtils.clamp(st.mouth, 0, 1)
    const surprised = st.action === 'surprise' ? Math.min(1, st.actionT * 5) * st.actionW : 0
    const open = Math.max(m, surprised * 0.8)
    mouthOpen.current.visible = open > 0.06
    mouthOpen.current.scale.set(1 - surprised * 0.35 + m * 0.1, 0.25 + open * 0.95, 1)
    smile.current.visible = open <= 0.06
    smile.current.scale.set(1, 0.6 + st.smile * 0.6, 1)
    const blinkPhase = (t * 0.31) % 1
    const blink = blinkPhase < 0.035 ? 0.12 : 1
    eyes.current.scale.y = blink * (1 + surprised * 0.15)
    const bu = st.brows + surprised
    browL.current.position.y = 0.105 + bu * 0.025; browR.current.position.y = 0.105 + bu * 0.025
    browL.current.rotation.z = Math.PI / 2 - 0.12 - bu * 0.14; browR.current.rotation.z = Math.PI / 2 + 0.12 + bu * 0.14
    finger.current.visible = st.action === 'point' && st.actionW > 0.5
  })

  return (
    <group ref={root} scale={scale}>
      <group ref={r('hips')} position={[0, 0.86, 0]}>
        {/* pelvis */}
        <mesh material={M.pants} castShadow={C} position={[0, 0.0, 0]} scale={[1, 0.7, 0.8]}>
          <sphereGeometry args={[0.165, 16, 12]} />
        </mesh>
        {/* legs */}
        {(['l', 'r'] as const).map((s) => {
          const sx = s === 'l' ? 1 : -1
          return (
            <group key={s} ref={r(s === 'l' ? 'lHip' : 'rHip')} position={[sx * 0.09, -0.02, 0]}>
              <mesh material={M.pants} castShadow={C} position={[0, -0.2, 0]}>
                <capsuleGeometry args={[0.078, 0.26, 4, 10]} />
              </mesh>
              <group ref={r(s === 'l' ? 'lKn' : 'rKn')} position={[0, -0.42, 0]}>
                <mesh material={M.pants} castShadow={C}>
                  <sphereGeometry args={[0.074, 12, 10]} />
                </mesh>
                <mesh material={M.pants} castShadow={C} position={[0, -0.18, 0]}>
                  <capsuleGeometry args={[0.07, 0.24, 4, 10]} />
                </mesh>
                <group ref={r(s === 'l' ? 'lFt' : 'rFt')} position={[0, -0.38, 0]}>
                  <RoundedBox args={[0.13, 0.085, 0.27]} radius={0.04} smoothness={3} position={[0, -0.02, 0.045]} material={M.shoes} castShadow={C} />
                  <mesh material={M.sole} position={[0, -0.06, 0.045]}>
                    <boxGeometry args={[0.135, 0.022, 0.275]} />
                  </mesh>
                  <mesh material={M.accent} position={[sx * 0.066, -0.015, 0.03]}>
                    <boxGeometry args={[0.006, 0.03, 0.14]} />
                  </mesh>
                </group>
              </group>
            </group>
          )
        })}
        {/* torso */}
        <group ref={r('chest')} position={[0, 0.06, 0]}>
          <mesh material={M.top} castShadow={C} position={[0, 0.2, 0]} scale={[1.08, 1, 0.78]}>
            <capsuleGeometry args={[0.175, 0.24, 6, 16]} />
          </mesh>

          {/* hoodie hem & pocket */}
          <mesh material={M.topD} position={[0, 0.02, 0]} scale={[1, 1, 0.8]}>
            <cylinderGeometry args={[0.18, 0.175, 0.06, 16]} />
          </mesh>
          {!look.vest && (
            <RoundedBox args={[0.2, 0.09, 0.03]} radius={0.012} smoothness={2} position={[0, 0.08, 0.142]} material={M.topD} />
          )}
          {logo && <mesh geometry={logo} material={M.vc} position={[0.0, 0.25, 0.152]} scale={1.15} />}
          {/* hood + strings */}
          {!look.hardhat && (
            <>
              <mesh material={M.topD} position={[0, 0.43, -0.07]} rotation={[1.25, 0, 0]} castShadow={C}>
                <torusGeometry args={[0.105, 0.05, 8, 16]} />
              </mesh>
              {[-0.04, 0.04].map((x) => (
                <mesh key={x} material={M.white} position={[x * 1.6, 0.38, 0.15]}>
                  <cylinderGeometry args={[0.006, 0.006, 0.08, 4]} />
                </mesh>
              ))}
            </>
          )}
          {look.vest && (
            <mesh material={M.vest} position={[0, 0.22, 0]} scale={[1.04, 1, 0.84]}>
              <cylinderGeometry args={[0.19, 0.19, 0.3, 16, 1, true]} />
            </mesh>
          )}
          {/* arms */}
          {(['l', 'r'] as const).map((s) => {
            const sx = s === 'l' ? 1 : -1
            return (
              <group key={s} ref={r(s === 'l' ? 'lSh' : 'rSh')} position={[sx * 0.2, 0.37, 0]}>
                <mesh material={M.top} castShadow={C}>
                  <sphereGeometry args={[0.066, 12, 10]} />
                </mesh>
                <mesh material={M.top} castShadow={C} position={[0, -0.13, 0]}>
                  <capsuleGeometry args={[0.064, 0.18, 4, 10]} />
                </mesh>
                <group ref={r(s === 'l' ? 'lEl' : 'rEl')} position={[0, -0.27, 0]}>
                  <mesh material={M.top} castShadow={C}>
                    <sphereGeometry args={[0.06, 10, 8]} />
                  </mesh>
                  <mesh material={M.top} castShadow={C} position={[0, -0.1, 0]}>
                    <capsuleGeometry args={[0.058, 0.15, 4, 10]} />
                  </mesh>
                  <mesh material={M.topD} position={[0, -0.2, 0]}>
                    <cylinderGeometry args={[0.06, 0.06, 0.04, 10]} />
                  </mesh>
                  <mesh material={M.skin} castShadow={C} position={[0, -0.27, 0.0]} scale={[0.9, 1.1, 0.75]}>
                    <sphereGeometry args={[0.062, 12, 10]} />
                  </mesh>
                  {s === 'r' && (
                    <mesh ref={finger} material={M.skin} position={[0, -0.36, 0.0]}>
                      <capsuleGeometry args={[0.017, 0.07, 3, 6]} />
                    </mesh>
                  )}
                </group>
              </group>
            )
          })}
          {/* neck + head */}
          <group ref={r('neck')} position={[0, 0.44, 0]}>
            <mesh material={M.skin} position={[0, 0.04, 0]}>
              <cylinderGeometry args={[0.06, 0.07, 0.1, 10]} />
            </mesh>
            <group ref={r('head')} position={[0, 0.1, 0]}>
              <group position={[0, 0.17, 0]}>
                <mesh material={M.skin} castShadow={C} scale={[1, 1.03, 0.95]}>
                  <sphereGeometry args={[0.2, 28, 20]} />
                </mesh>
                <mesh geometry={hair} material={M.hair} castShadow={C} />
                {/* ears */}
                {[1, -1].map((sx) => (
                  <mesh key={sx} material={M.skin} position={[sx * 0.195, -0.005, -0.01]} scale={[0.5, 1, 0.8]}>
                    <sphereGeometry args={[0.05, 10, 8]} />
                  </mesh>
                ))}
                {/* nose */}
                <mesh material={M.skin} position={[0, -0.025, 0.192]} scale={[1, 0.9, 0.8]}>
                  <sphereGeometry args={[0.032, 10, 8]} />
                </mesh>
                {/* cheeks */}
                {[1, -1].map((sx) => (
                  <mesh key={'c' + sx} material={M.cheek} position={[sx * 0.11, -0.05, 0.155]} scale={[1, 0.6, 0.4]}>
                    <sphereGeometry args={[0.035, 10, 8]} />
                  </mesh>
                ))}
                {/* eyes */}
                <group ref={eyes} position={[0, 0.03, 0]}>
                  {[1, -1].map((sx) => (
                    <group key={sx} position={[sx * 0.074, 0, 0.17]}>
                      <mesh material={M.white} scale={[0.82, 1.08, 0.6]}>
                        <sphereGeometry args={[0.054, 16, 12]} />
                      </mesh>
                      <mesh material={M.iris} position={[0, -0.004, 0.026]} scale={[1, 1, 0.5]}>
                        <sphereGeometry args={[0.031, 14, 10]} />
                      </mesh>
                      <mesh material={M.pupil} position={[0, -0.004, 0.039]} scale={[1, 1, 0.4]}>
                        <sphereGeometry args={[0.016, 10, 8]} />
                      </mesh>
                      <mesh material={M.white} position={[0.011, 0.012, 0.045]}>
                        <sphereGeometry args={[0.008, 6, 6]} />
                      </mesh>
                    </group>
                  ))}
                </group>
                {/* brows */}
                <mesh ref={browL} material={M.brow} position={[0.075, 0.105, 0.178]} rotation={[0, 0, 0.12]}>
                  <capsuleGeometry args={[0.012, 0.06, 3, 6]} />
                </mesh>
                <mesh ref={browR} material={M.brow} position={[-0.075, 0.105, 0.178]} rotation={[0, 0, -0.12]}>
                  <capsuleGeometry args={[0.012, 0.06, 3, 6]} />
                </mesh>
                {/* brow capsules lie horizontally */}
                {/* mouth */}
                <mesh ref={smile} material={M.lip} position={[0, -0.085, 0.178]} rotation={[0.25, 0, Math.PI]}>
                  <torusGeometry args={[0.045, 0.011, 6, 14, Math.PI]} />
                </mesh>
                <mesh ref={mouthOpen} material={M.mouth} position={[0, -0.095, 0.172]} scale={[1, 0.5, 1]}>
                  <sphereGeometry args={[0.045, 14, 10]} />
                </mesh>
                {look.hardhat && (
                  <group position={[0, 0.07, 0]}>
                    <mesh material={M.hat} castShadow={C}>
                      <sphereGeometry args={[0.225, 20, 12, 0, Math.PI * 2, 0, Math.PI / 2]} />
                    </mesh>
                    <mesh material={M.hat} position={[0, 0.0, 0.03]}>
                      <cylinderGeometry args={[0.26, 0.26, 0.02, 20]} />
                    </mesh>
                  </group>
                )}
              </group>
            </group>
          </group>
        </group>
      </group>
    </group>
  )
}
