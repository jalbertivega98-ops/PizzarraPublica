// COSAS DE PAREJA · EP. 1 «Las llaves» (versión larga, 4 sitios): recibidor → rellano → coche → calle.
// Un solo audio continuo (Martín e Inés) con silencios entre escenas, sin música ni efectos.
// Él mueve la boca al hablar, no al murmurar (l06). Remate visual: las llaves estaban en el bolsillo de su abrigo.
import { useMemo, useRef, type ReactNode } from 'react'
import { useFrame } from '@react-three/fiber'
import { RoundedBox } from '@react-three/drei'
import * as THREE from 'three'
import { CONV } from './pareja13_data'
import { Hallway, Mug, PairEpisode, Show, box, pose, track, type Overlay, type PairSpec } from './pareja_kit'
import { clock } from '../engine/clock'

const fm = (c: string, r = 0.8) => new THREE.MeshStandardMaterial({ color: c, roughness: r, flatShading: true })
const METAL = fm('#d9d2c2', 0.3), RING = fm('#c9a43a', 0.35), FOB = fm('#2f7f83'), DARK = fm('#2b2224')

const at = Object.fromEntries(CONV.map((c) => [c.id, c.at])) as Record<string, number>
const S2 = 10.45, S3 = 18.35, S4 = 30.55
const KEYS_OUT = at.l15 - 0.75 // the keys come out of her coat pocket
const sc = (t: number) => (t < S2 ? 1 : t < S3 ? 2 : t < S4 ? 3 : 4)
const inS = (n: number) => () => sc(clock.t) === n
const LX = -0.42, Z = 0.2, HY = 1.66

function Keys({ s = 1 }: { s?: number }) {
  return (
    <group rotation={[0.2, 0.4, 0.3]} scale={s}>
      <mesh material={RING}><torusGeometry args={[0.03, 0.006, 5, 12]} /></mesh>
      <mesh position={[0.01, -0.06, 0.005]} rotation-z={0.2} material={METAL}><boxGeometry args={[0.018, 0.07, 0.004]} /></mesh>
      <mesh position={[-0.03, -0.055, 0]} rotation-z={-0.4} material={METAL}><boxGeometry args={[0.018, 0.065, 0.004]} /></mesh>
      <mesh position={[0.03, 0.035, 0]} material={FOB}><boxGeometry args={[0.035, 0.05, 0.015]} /></mesh>
    </group>
  )
}

/** canvas screen for the phone insert */
function useScreen(draw: (c: CanvasRenderingContext2D, w: number, h: number) => void) {
  return useMemo(() => {
    const cv = document.createElement('canvas'); cv.width = 540; cv.height = 1100
    const c = cv.getContext('2d')!
    draw(c, cv.width, cv.height)
    const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace
    return tex
  }, [])
}
const rr = (c: CanvasRenderingContext2D, x: number, y: number, w: number, h: number, r: number) => { c.beginPath(); c.roundRect(x, y, w, h, r); c.fill() }
function ChatScreen() {
  const tex = useScreen((c, w, h) => {
    c.fillStyle = '#0f1a1f'; c.fillRect(0, 0, w, h)
    c.fillStyle = '#1f2c33'; c.fillRect(0, 0, w, 170)
    c.fillStyle = '#e9edef'; c.font = '600 30px sans-serif'; c.textAlign = 'left'; c.fillText('21:14', 34, 52)
    c.fillStyle = '#c7a27a'; c.beginPath(); c.arc(84, 118, 34, 0, Math.PI * 2); c.fill()
    c.fillStyle = '#e9edef'; c.font = '700 40px sans-serif'; c.fillText('Mamá', 136, 116)
    c.fillStyle = '#8696a0'; c.font = '28px sans-serif'; c.fillText('en línea', 136, 152)
    const bub = (y: number, txt: string, hr: string) => {
      c.font = '38px sans-serif'; const tw = c.measureText(txt).width
      c.fillStyle = '#202c33'; rr(c, 34, y, tw + 120, 86, 20)
      c.fillStyle = '#e9edef'; c.fillText(txt, 58, y + 56)
      c.fillStyle = '#8696a0'; c.font = '24px sans-serif'; c.fillText(hr, tw + 70, y + 72)
    }
    bub(560, 'La cena está lista', '20:58')
    bub(670, '¿Venís ya? 🙂', '21:14')
  })
  return <mesh position={[0, 0, 0.0065]}><planeGeometry args={[0.072, 0.146]} /><meshBasicMaterial map={tex} toneMapped={false} /></mesh>
}
function PhoneProp({ screen }: { screen?: ReactNode }) {
  return (
    <group>
      <RoundedBox args={[0.08, 0.16, 0.012]} radius={0.008} smoothness={2}><meshStandardMaterial color="#1a1a22" roughness={0.35} /></RoundedBox>
      {screen ?? <mesh position={[0, 0, 0.0065]}><planeGeometry args={[0.072, 0.146]} /><meshBasicMaterial color="#9fd0ff" toneMapped={false} /></mesh>}
    </group>
  )
}

// ---------------- 2 · landing outside the flat: their door (3ºB), lift, stair rail, cold ceiling light
function Landing() {
  const key = useRef<THREE.Group>(null!)
  useFrame(() => {
    // the key turns twice in the lock during the scene change
    const k = THREE.MathUtils.clamp((clock.t - (S2 + 0.25)) / 0.9, 0, 1)
    key.current.rotation.z = -Math.PI * 2 * (k * k * (3 - 2 * k))
  })
  const wall = fm('#bfc7c2'), floor = fm('#8d8a84', 0.6), door = fm('#6b4a33', 0.6)
  return (
    <group>
      <hemisphereLight args={['#e8f1ff', '#2a2a30', 0.85]} />
      <directionalLight position={[-1.5, 3.2, 3]} intensity={0.8} color="#eef4ff" castShadow shadow-mapSize={[2048, 2048]} shadow-bias={-0.0005}
        shadow-camera-left={-3} shadow-camera-right={3} shadow-camera-top={3} shadow-camera-bottom={-3} />
      <pointLight position={[0, 2.5, 0.3]} intensity={3.5} distance={6} decay={1.5} color="#f2f7ff" />
      <pointLight position={[0, 1.7, 2.6]} intensity={1.2} distance={6} color="#fff0e0" />
      <mesh rotation-x={-Math.PI / 2} material={floor} receiveShadow><planeGeometry args={[8, 8]} /></mesh>
      {/* checker tiles */}
      {Array.from({ length: 30 }, (_, i) => <mesh key={i} rotation-x={-Math.PI / 2} position={[-2.25 + (i % 6) * 0.9 + ((i / 6 | 0) % 2) * 0.45, 0.004, -0.9 + (i / 6 | 0) * 0.45]} material={fm('#a8a49c', 0.6)}><planeGeometry args={[0.45, 0.45]} /></mesh>)}
      <mesh position={[0, 1.5, -1.1]} material={wall} receiveShadow><planeGeometry args={[8, 3]} /></mesh>
      <mesh position={[0, 0.5, -1.095]} material={fm('#7e8a86')}><planeGeometry args={[8, 1.0]} /></mesh>
      <mesh position={[0, 2.68, 0.3]}><boxGeometry args={[0.9, 0.05, 0.16]} /><meshStandardMaterial color="#ffffff" emissive="#eaf2ff" emissiveIntensity={1.4} /></mesh>
      {/* their door, behind them in the middle, with number plate and the lock */}
      <group position={[0, 0, -1.08]}>
        <mesh position={[0, 1.1, 0.01]} material={fm('#e9e4da')}><boxGeometry args={[1.08, 2.3, 0.04]} /></mesh>
        <mesh position={[0, 1.07, 0.035]} material={door} castShadow><boxGeometry args={[0.92, 2.14, 0.05]} /></mesh>
        {[0.5, 1.1, 1.7].map((y) => <mesh key={y} position={[0, y, 0.064]} material={fm('#5c3f2b', 0.6)}><boxGeometry args={[0.7, 0.42, 0.01]} /></mesh>)}
        <mesh position={[0, 1.95, 0.07]} material={fm('#d4b15a', 0.3)}><boxGeometry args={[0.16, 0.08, 0.01]} /></mesh>
        <mesh position={[0.36, 1.0, 0.08]} material={fm('#d4b15a', 0.3)}><boxGeometry args={[0.05, 0.2, 0.03]} /></mesh>
        <group position={[0.36, 1.16, 0.1]}>
          <mesh rotation-x={Math.PI / 2} material={fm('#d4b15a', 0.3)}><cylinderGeometry args={[0.025, 0.025, 0.02, 10]} /></mesh>
          <group ref={key} position={[0, 0, 0.02]}><group rotation-x={-1.2}><Keys s={0.9} /></group></group>
        </group>
        <mesh rotation-x={-Math.PI / 2} position={[0, 0.01, 0.45]} material={fm('#5a4a3a')}><planeGeometry args={[0.8, 0.5]} /></mesh>
      </group>
      {/* lift on the right */}
      <group position={[1.6, 0, -1.08]}>
        <mesh position={[0, 1.1, 0.01]} material={fm('#6f767a', 0.4)}><boxGeometry args={[1.0, 2.2, 0.04]} /></mesh>
        <mesh position={[-0.22, 1.05, 0.035]} material={fm('#a9b0b4', 0.3)}><boxGeometry args={[0.43, 2.0, 0.02]} /></mesh>
        <mesh position={[0.22, 1.05, 0.035]} material={fm('#a9b0b4', 0.3)}><boxGeometry args={[0.43, 2.0, 0.02]} /></mesh>
        <mesh position={[0.62, 1.15, 0.03]} material={DARK}><boxGeometry args={[0.1, 0.22, 0.02]} /></mesh>
        <mesh position={[0.62, 1.2, 0.045]}><circleGeometry args={[0.02, 8]} /><meshBasicMaterial color="#ffb36b" toneMapped={false} /></mesh>
      </group>
      {/* stairs going down on the left with a rail */}
      <group position={[-1.85, 0, -0.2]}>
        {[0, 1, 2, 3].map((i) => <mesh key={i} position={[0, -0.09 - i * 0.18, 0.3 + i * 0.28]} material={fm('#9a958c', 0.6)} receiveShadow><boxGeometry args={[0.9, 0.18, 0.28]} /></mesh>)}
        <mesh position={[0.5, 0.95, 0.5]} rotation-x={0.55} material={DARK}><boxGeometry args={[0.05, 0.05, 1.6]} /></mesh>
        {[0, 1, 2, 3, 4].map((i) => <mesh key={i} position={[0.5, 0.5 - i * 0.16, -0.1 + i * 0.3]} material={DARK}><boxGeometry args={[0.02, 0.9, 0.02]} /></mesh>)}
      </group>
      <mesh position={[-1.0, 1.5, -1.07]} material={fm('#e9e4da')}><boxGeometry args={[0.18, 0.12, 0.01]} /></mesh>
    </group>
  )
}

// ---------------- 3 · in the car at night: seen from the front, dashboard hides their legs. He drives (left seat = +x).
function CarNight() {
  const pass = useRef<THREE.PointLight>(null!)
  const lights = useRef<THREE.Group>(null!)
  useFrame(() => {
    const t = clock.t
    const ph = (t * 0.55) % 1
    pass.current.intensity = 2.6 * Math.pow(Math.max(0, Math.sin(ph * Math.PI)), 6)
    pass.current.position.set(-1.6 + ph * 3.2, 2.3, 0.4)
    lights.current.position.x = ((t * 1.6) % 4) - 2
  })
  const body = fm('#20242c', 0.5), seat = fm('#33363e', 0.9), dash = fm('#1b1d22', 0.7)
  return (
    <group>
      <hemisphereLight args={['#5a6d9a', '#0c0c12', 0.55]} />
      <pointLight position={[0, 1.45, 1.2]} intensity={1.6} distance={3} decay={1.6} color="#a9c6ff" />
      <pointLight position={[0.3, 1.9, 2.4]} intensity={1.1} distance={5} color="#ffe6c8" />
      <pointLight ref={pass} distance={4} decay={1.5} color="#ffb05a" />
      <directionalLight position={[0, 3, 3]} intensity={0.35} color="#9fb6ff" />
      {/* street lights blurred behind the rear window */}
      <group ref={lights} position={[0, 1.6, -3.5]}>
        {[-3, -1.5, 0, 1.5, 3, 4.5].map((x, i) => <mesh key={x} position={[x, (i % 2) * 0.25, 0]}><sphereGeometry args={[0.09, 8, 6]} /><meshBasicMaterial color={i % 3 ? '#ffb05a' : '#ffe2a0'} toneMapped={false} /></mesh>)}
      </group>
      {/* seats + headrests */}
      {[LX, 0.42].map((x) => (
        <group key={x} position={[x, 0, Z - 0.32]}>
          <RoundedBox args={[0.6, 1.05, 0.2]} radius={0.06} smoothness={2} position={[0, 0.95, 0]} rotation-x={-0.12} material={seat} />
          <RoundedBox args={[0.32, 0.22, 0.14]} radius={0.05} smoothness={2} position={[0, 1.72, -0.08]} material={seat} />
          <mesh position={[0, 1.55, -0.05]} material={METAL}><boxGeometry args={[0.2, 0.12, 0.02]} /></mesh>
        </group>
      ))}
      {/* roof, pillars, doors */}
      <mesh position={[0, 2.12, 0.15]} material={body}><boxGeometry args={[1.9, 0.06, 1.6]} /></mesh>
      {[-0.95, 0.95].map((x) => <mesh key={x} position={[x, 1.65, 0.9]} rotation-x={-0.5} material={body}><boxGeometry args={[0.07, 1.05, 0.07]} /></mesh>)}
      {[-1.0, 1.0].map((x) => <mesh key={x} position={[x, 0.9, 0.2]} material={body}><boxGeometry args={[0.06, 0.9, 1.6]} /></mesh>)}
      <mesh position={[0, 2.05, 0.8]} rotation-x={0.1} material={DARK}><boxGeometry args={[0.24, 0.05, 0.05]} /></mesh>
      {/* dashboard and steering wheel (his side) */}
      <mesh position={[0, 1.02, 0.92]} rotation-x={-0.35} material={dash}><boxGeometry args={[1.95, 0.22, 0.6]} /></mesh>
      <mesh position={[0, 0.7, 1.0]} material={dash}><boxGeometry args={[1.95, 0.6, 0.4]} /></mesh>
      <group position={[0.42, 1.2, 0.66]} rotation-x={-0.5}>
        <mesh material={fm('#111216', 0.6)}><torusGeometry args={[0.17, 0.022, 6, 16]} /></mesh>
        <mesh material={fm('#111216', 0.6)}><boxGeometry args={[0.3, 0.035, 0.02]} /></mesh>
      </group>
      <mesh position={[-0.05, 1.16, 0.82]} rotation-x={-0.35}><planeGeometry args={[0.18, 0.07]} /><meshBasicMaterial color="#5fd0c0" toneMapped={false} /></mesh>
    </group>
  )
}

// ---------------- 4 · street at night, outside her parents' building: portal, intercom, street lamp, parked car, cold
function StreetNight() {
  const fac = fm('#7c6a5d'), stone = fm('#6c665e', 0.7)
  return (
    <group>
      <hemisphereLight args={['#6f86b8', '#14121a', 0.7]} />
      <pointLight position={[1.6, 2.9, 0.4]} intensity={6} distance={6} decay={1.4} color="#ffbf73" castShadow />
      <pointLight position={[0, 1.8, 2.6]} intensity={1.0} distance={6} color="#cfdcff" />
      <directionalLight position={[-2, 3.5, 2]} intensity={0.4} color="#a8bcff" />
      {/* pavement + kerb + road */}
      <mesh rotation-x={-Math.PI / 2} material={stone} receiveShadow><planeGeometry args={[8, 3.2]} /></mesh>
      {Array.from({ length: 16 }, (_, i) => <mesh key={i} rotation-x={-Math.PI / 2} position={[-3.75 + i * 0.5, 0.003, 0.3]} material={fm('#5d5850', 0.7)}><planeGeometry args={[0.02, 3]} /></mesh>)}
      <mesh position={[0, 0.06, 1.62]} material={fm('#8a857c')}><boxGeometry args={[8, 0.12, 0.12]} /></mesh>
      <mesh rotation-x={-Math.PI / 2} position={[0, -0.05, 3.5]} material={fm('#2a2a30', 0.9)}><planeGeometry args={[8, 4]} /></mesh>
      {/* facade with the portal */}
      <mesh position={[0, 2, -1.1]} material={fac} receiveShadow><planeGeometry args={[8, 4]} /></mesh>
      <mesh position={[0, 0.3, -1.09]} material={fm('#5e5049')}><planeGeometry args={[8, 0.6]} /></mesh>
      <group position={[0, 0, -1.08]}>
        <mesh position={[0, 1.25, 0.01]} material={fm('#3a3330')}><boxGeometry args={[1.3, 2.6, 0.05]} /></mesh>
        <mesh position={[0, 1.18, 0.04]}><boxGeometry args={[1.1, 2.3, 0.02]} /><meshStandardMaterial color="#e6c58f" emissive="#d9a865" emissiveIntensity={0.55} roughness={0.2} /></mesh>
        {[0.55, 1.18, 1.8].map((y) => <mesh key={y} position={[0, y, 0.055]} material={DARK}><boxGeometry args={[1.1, 0.04, 0.02]} /></mesh>)}
        <mesh position={[0, 1.18, 0.055]} material={DARK}><boxGeometry args={[0.04, 2.3, 0.02]} /></mesh>
        <mesh position={[0, 2.62, 0.06]} material={fm('#d4b15a', 0.3)}><boxGeometry args={[0.3, 0.12, 0.02]} /></mesh>
      </group>
      {/* intercom */}
      <group position={[0.95, 1.3, -1.06]}>
        <mesh material={fm('#a9a49a', 0.4)}><boxGeometry args={[0.2, 0.38, 0.03]} /></mesh>
        {[0, 1, 2, 3, 4].map((i) => <mesh key={i} position={[0, 0.1 - i * 0.055, 0.02]} material={DARK}><boxGeometry args={[0.12, 0.03, 0.01]} /></mesh>)}
        <mesh position={[0, 0.16, 0.02]} material={DARK}><circleGeometry args={[0.035, 10]} /></mesh>
      </group>
      {/* street lamp + its glow */}
      <group position={[1.9, 0, 1.3]}>
        <mesh position={[0, 1.6, 0]} material={DARK}><cylinderGeometry args={[0.035, 0.05, 3.2, 6]} /></mesh>
        <mesh position={[-0.2, 3.15, 0]} rotation-z={Math.PI / 2} material={DARK}><cylinderGeometry args={[0.025, 0.025, 0.45, 6]} /></mesh>
        <mesh position={[-0.4, 3.05, 0]}><coneGeometry args={[0.16, 0.18, 6]} /><meshBasicMaterial color="#ffd08a" toneMapped={false} /></mesh>
      </group>
      {/* parked car on the left (side) + small tree pit */}
      <group position={[-2.3, 0, 2.3]}>
        <RoundedBox args={[1.8, 0.55, 0.9]} radius={0.12} smoothness={2} position={[0, 0.45, 0]} material={fm('#7d2f2f', 0.4)} />
        <RoundedBox args={[1.0, 0.4, 0.82]} radius={0.12} smoothness={2} position={[-0.1, 0.88, 0]} material={fm('#7d2f2f', 0.4)} />
        <mesh position={[-0.1, 0.9, 0.42]}><planeGeometry args={[0.85, 0.3]} /><meshStandardMaterial color="#2a3240" roughness={0.1} /></mesh>
        {[-0.6, 0.6].map((x) => <mesh key={x} position={[x, 0.2, 0.42]} rotation-x={Math.PI / 2} material={DARK}><cylinderGeometry args={[0.2, 0.2, 0.12, 10]} /></mesh>)}
      </group>
      <group position={[-1.6, 0, -0.6]}>
        <mesh position={[0, 0.01, 0]} rotation-x={-Math.PI / 2} material={fm('#3b2f27')}><planeGeometry args={[0.6, 0.6]} /></mesh>
        <mesh position={[0, 1.1, 0]} material={fm('#4a3526')}><cylinderGeometry args={[0.05, 0.07, 2.2, 6]} /></mesh>
        {[0, 1, 2].map((i) => <mesh key={i} position={[Math.cos(i * 2.1) * 0.2, 2.3 + i * 0.1, Math.sin(i * 2.1) * 0.15]} material={fm('#5b4a33')}><icosahedronGeometry args={[0.28, 0]} /></mesh>)}
      </group>
    </group>
  )
}

/** the phone insert (staged far from the sets, with its own light) */
const PH: [number, number, number] = [20, 1, 0]
function PhoneInsert() {
  const g = useRef<THREE.Group>(null!)
  useFrame(() => { g.current.rotation.z = Math.sin(clock.t * 1.3) * 0.02 })
  return (
    <group position={PH}>
      <pointLight position={[0.1, 0.3, 0.5]} intensity={1.2} distance={2} color="#b9c9ff" />
      <mesh position={[0, -0.12, -0.05]} rotation-x={-0.2}><boxGeometry args={[0.4, 0.05, 0.3]} /><meshStandardMaterial color="#c98b3a" roughness={0.9} flatShading /></mesh>
      <group ref={g}><PhoneProp screen={<ChatScreen />} /></group>
    </group>
  )
}
/** close-up of the keys coming out of the coat pocket */
const KP: [number, number, number] = [-20, 1, 0]
function KeysInsert() {
  const k = useRef<THREE.Group>(null!)
  useFrame(() => {
    const e = THREE.MathUtils.clamp((clock.t - (KEYS_OUT - 0.1)) / 0.8, 0, 1)
    const s = e * e * (3 - 2 * e)
    k.current.position.set(0.02, -0.12 + s * 0.2, 0.09)
    k.current.rotation.z = Math.sin(clock.t * 3.2) * 0.15 * s
  })
  return (
    <group position={KP}>
      <hemisphereLight args={['#6f86b8', '#14121a', 0.4]} />
      <pointLight position={[0.4, 0.5, 0.6]} intensity={2.2} distance={3} color="#ffbf73" />
      {/* camel coat panel with a pocket */}
      <mesh position={[0, 0, 0]} material={fm('#c98b3a', 0.95)}><boxGeometry args={[0.6, 0.6, 0.1]} /></mesh>
      <mesh position={[0, -0.12, 0.055]} material={fm('#b47a2f', 0.95)}><boxGeometry args={[0.24, 0.02, 0.02]} /></mesh>
      <mesh position={[-0.2, 0.15, 0.056]} material={fm('#5a3d1f')}><circleGeometry args={[0.022, 8]} /></mesh>
      <group ref={k}><Keys s={2.2} /></group>
      {/* her hand */}
      <mesh position={[0.03, -0.02, 0.07]} material={fm('#f1c3a0', 0.75)}><icosahedronGeometry args={[0.045, 1]} /></mesh>
    </group>
  )
}

// ---------------- acting
const mugArms = { rSh: [0.55, -0.05] as [number, number], rEl: -1.75, lSh: [0.2, 0.18] as [number, number], lEl: -0.5 }
const relArms = { rSh: [0.25, -0.12] as [number, number], rEl: -0.6, lSh: [0.2, 0.12] as [number, number], lEl: -0.5 }
const wheel = { rSh: [1.05, -0.08] as [number, number], rEl: -0.55, lSh: [1.05, 0.08] as [number, number], lEl: -0.55 }
const D = {
  sip: pose({ yaw: -0.1, lids: 0.3, smile: 0.1, ...mugArms, rSh: [0.85, -0.05], rEl: -2.0, pitch: -0.05 }),
  flat: pose({ yaw: -0.35, lids: 0.4, brows: 0.05, ...mugArms }),
  helpful: pose({ yaw: -0.4, lids: 0.2, brows: 0.3, smile: 0.15, ...mugArms, lSh: [0.6, 0.35], lEl: -1.1 }),
  mutter: pose({ yaw: 0.25, pitch: 0.12, roll: 0.06, lids: 0.6, brows: -0.25, browTilt: 0.5, smile: -0.3, ...mugArms }),
  hurry: pose({ yaw: -0.4, lids: 0.15, brows: 0.25, smile: 0, ...relArms, rSh: [0.7, -0.2], rEl: -1.3 }),
  calm: pose({ yaw: -0.4, lids: 0.3, brows: 0.15, smile: 0.25, ...relArms, lSh: [0.45, 0.4], lEl: -1.0 }),
  blank: pose({ yaw: -0.3, lids: 0.45, brows: -0.05, smile: -0.15, ...relArms }),
  drive: pose({ yaw: 0, lids: 0.25, brows: 0, ...wheel }),
  driveSide: pose({ yaw: -0.4, lids: 0.35, brows: 0.15, smile: 0.05, ...wheel }),
  driveDry: pose({ yaw: -0.05, lids: 0.5, brows: -0.1, smile: -0.1, ...wheel }),
  wise: pose({ yaw: -0.35, lids: 0.45, brows: 0.35, browTilt: -0.3, smile: 0.35, ...wheel }),
  cold: pose({ yaw: -0.2, lids: 0.3, brows: 0.1, smile: -0.05, lean: 0.03, ...relArms, rSh: [0.35, -0.02], lSh: [0.35, 0.02], rEl: -1.6, lEl: -1.6 }),
  look: pose({ yaw: -0.5, pitch: 0.2, lids: 0.15, brows: 0.5, ...relArms }),
  stunned: pose({ yaw: -0.5, lids: 0, brows: 0.95, browTilt: -0.2, smile: -0.1, ...relArms }),
  sure: pose({ yaw: -0.45, lids: 0.35, brows: 0.6, browTilt: -0.5, smile: -0.2, ...relArms }),
  camera: pose({ yaw: 0.25, pitch: 0.02, lids: 0.5, brows: 0.05, smile: -0.2, ...relArms }),
}
const herArms = { rSh: [0.25, -0.12] as [number, number], rEl: -0.7, lSh: [0.25, 0.12] as [number, number], lEl: -0.7 }
const phone = { rSh: [0.8, -0.05] as [number, number], rEl: -1.55 }
const L_ = {
  look: pose({ yaw: -0.2, pitch: 0.15, lids: 0.15, brows: 0.35, browTilt: -0.35, smile: -0.1, ...herArms }),
  ask: pose({ yaw: 0.45, lids: 0.05, brows: 0.5, ...herArms, lSh: [0.5, 0.35], lEl: -1.1 }),
  unamused: pose({ yaw: 0.55, lids: 0.55, brows: -0.2, browTilt: 0.6, smile: -0.4, ...herArms, rSh: [0.45, -0.4], rEl: -1.2 }),
  already: pose({ yaw: 0.5, pitch: -0.05, lids: 0.4, brows: 0.4, browTilt: 0.2, smile: -0.25, roll: -0.08, ...herArms }),
  pat: pose({ yaw: 0.1, pitch: 0.3, lids: 0.2, brows: 0.3, ...herArms, rSh: [0.15, -0.3], rEl: -0.4, lSh: [0.15, 0.3], lEl: -0.4 }),
  worried: pose({ yaw: 0.45, lids: 0.1, brows: 0.6, browTilt: -0.6, smile: -0.2, ...herArms, lSh: [0.6, 0.2], lEl: -1.5 }),
  pout: pose({ yaw: 0.5, lids: 0.35, brows: 0.2, browTilt: -0.4, smile: -0.35, roll: 0.06, ...herArms }),
  phone: pose({ yaw: 0.15, pitch: 0.35, lids: 0.25, brows: 0.2, ...herArms, ...phone }),
  phoneTell: pose({ yaw: 0.45, pitch: 0.1, lids: 0.2, brows: 0.35, ...herArms, ...phone }),
  defend: pose({ yaw: 0.5, lids: 0.3, brows: -0.1, browTilt: 0.5, smile: -0.3, ...herArms, ...phone, lSh: [0.55, 0.4], lEl: -1.2 }),
  glare: pose({ yaw: 0.55, lids: 0.55, brows: -0.35, browTilt: 0.8, smile: -0.4, ...herArms, ...phone }),
  cold: pose({ yaw: 0.2, lids: 0.3, brows: 0.2, smile: -0.1, lean: 0.03, ...herArms, rSh: [0.35, -0.02], lSh: [0.35, 0.02], rEl: -1.6, lEl: -1.6 }),
  pocket: pose({ yaw: 0.05, pitch: 0.3, lids: 0.2, brows: 0.4, ...herArms, rSh: [0.05, -0.35], rEl: -0.25 }),
  found: pose({ yaw: 0.15, pitch: 0.2, lids: 0, brows: 0.9, browTilt: -0.3, smile: 0.05, ...herArms, rSh: [0.95, -0.05], rEl: -1.35 }),
  mira: pose({ yaw: 0.45, lids: 0.1, brows: 0.6, browTilt: -0.5, smile: 0.35, ...herArms, rSh: [0.95, -0.05], rEl: -1.35 }),
  excuse: pose({ yaw: 0.5, lids: 0.2, brows: 0.4, browTilt: -0.4, smile: 0.2, roll: -0.07, ...herArms, rSh: [0.7, -0.1], rEl: -1.2, lSh: [0.5, 0.4], lEl: -1.2 }),
  logic: pose({ yaw: 0.5, pitch: -0.06, lids: 0.35, brows: 0.5, browTilt: 0.1, smile: 0.1, ...herArms, rSh: [0.7, -0.1], rEl: -1.2 }),
}

// hands: he has the mug at home, nothing in the car; she has the phone in the car and the keys after the pocket
const DaniHand = () => <Show show={inS(1)}><Mug color="#2f7f83" /></Show>
const LuciaHand = () => (
  <group>
    <Show show={() => sc(clock.t) === 3 && clock.t > at.l11 - 0.8}><group rotation={[0.3, 0, 0]} position={[0, -0.02, 0.05]}><PhoneProp /></group></Show>
    <Show show={() => clock.t > KEYS_OUT + 0.4}><group position={[0, -0.04, 0.05]}><Keys s={1.3} /></group></Show>
  </group>
)

const V = (x: number, y: number, z: number) => [x, y, z] as [number, number, number]
const shots = {
  // 1 hallway
  wide: { p: V(0.35, 1.75, 3.7), l: V(-0.25, 1.15, -0.6), fov: 50, push: 0.3 },
  two: { p: V(0, HY + 0.15, Z + 3.0), l: V(0, HY - 0.4, Z), fov: 44, push: 0.2 },
  lucia: { p: V(-0.12, HY + 0.05, Z + 2.3), l: V(LX, HY - 0.22, Z), fov: 38, push: 0.12 },
  dani: { p: V(0.12, HY + 0.05, Z + 2.3), l: V(0.42, HY - 0.22, Z), fov: 38, push: 0.12 },
  daniClose: { p: V(0.3, HY + 0.02, Z + 1.9), l: V(0.42, HY - 0.12, Z), fov: 36, push: 0.1 },
  bowl: { p: V(0.6, 1.3, -0.3), l: V(0.47, 0.86, -0.83), fov: 36, push: 0.06 },
  // 2 landing
  lock: { p: V(0.62, 1.32, -0.05), l: V(0.36, 1.12, -0.97), fov: 32, push: 0.08 },
  landing: { p: V(-0.3, 1.8, 3.4), l: V(0.1, 1.15, -0.5), fov: 48, push: 0.25 },
  // 3 car (from outside the windscreen)
  car: { p: V(0, 1.72, 3.3), l: V(0, 1.52, Z), fov: 38, push: 0.15 },
  carL: { p: V(-0.1, 1.66, 2.75), l: V(LX + 0.05, 1.5, Z), fov: 30, push: 0.08 },
  carD: { p: V(0.1, 1.66, 2.75), l: V(0.37, 1.5, Z), fov: 30, push: 0.08 },
  phone: { p: V(PH[0], PH[1] + 0.02, PH[2] + 0.26), l: V(PH[0], PH[1], PH[2]), fov: 36, push: 0.04 },
  // 4 street
  street: { p: V(0.6, 1.7, 3.9), l: V(-0.1, 1.3, -0.6), fov: 50, push: 0.35 },
  keys: { p: V(KP[0] + 0.08, KP[1] + 0.06, KP[2] + 0.95), l: V(KP[0], KP[1] - 0.02, KP[2]), fov: 36, push: 0.06 },
  cam: { p: V(0.38, HY + 0.0, Z + 1.75), l: V(0.42, HY - 0.08, Z), fov: 34, push: 0.06 },
}

const W = '{\\an8\\pos(540,70)\\fs34\\bord2\\shad0\\alpha&H50&}@pizarrapublica'
const spec: PairSpec = {
  id: 'pareja13',
  script: CONV.map((c) => ({ id: c.id, text: c.text })),
  fixedAt: at,
  gap: {},
  her: CONV.filter((c) => c.her).map((c) => c.id),
  talk: true,
  quiet: ['l06'],
  legs: { lucia: { pants: '#3b3550', shoes: '#2a1d1a' }, dani: { pants: '#2b3a5c', shoes: '#e8e2d8' } },
  ry: { lucia: 0.25, dani: -0.25 },
  bg: '#141420',
  tail: 2.4,
  keyColor: '&H8A6A1E&',
  Set: ({ st }) => {
    st.luciaTop = '#c98b3a'
    return (
      <group>
        <Show show={inS(1)}><Hallway /></Show>
        <Show show={inS(2)}><Landing /></Show>
        <Show show={inS(3)}><CarNight /></Show>
        <Show show={inS(4)}><StreetNight /></Show>
        <PhoneInsert />
        <KeysInsert />
      </group>
    )
  },
  pos: { lucia: [LX, 0.62, Z], dani: [0.42, 0.62, Z] },
  shots,
  luciaHand: <LuciaHand />,
  daniHand: <DaniHand />,
  frame: (t, a, l, st) => {
    // he puts the navy jacket on to leave
    st.daniTop = t < S2 ? '#2f8f83' : '#2e3346'
    const dani = track([
      [0, D.sip], [a('l02') - 0.2, D.flat], [a('l04') - 0.15, D.helpful], [a('l05') + 0.6, D.flat], [a('l06') - 0.2, D.mutter],
      [S2, D.hurry], [a('l08') + 0.2, D.blank], [a('l09') - 0.15, D.calm], [a('l10') + 0.4, D.blank],
      [S3, D.drive], [a('l11') + 0.6, D.driveSide], [a('l12') + 0.3, D.driveDry], [a('l13') + 0.5, D.drive], [a('l14') - 0.1, D.wise], [a('l14') + 2.0, D.drive],
      [S4, D.cold], [KEYS_OUT + 0.3, D.look], [a('l15') + 0.2, D.stunned], [a('l16') + 0.8, D.blank], [a('l18') - 0.15, D.sure], [a('l19') + 1.6, D.camera],
    ], t, 0.24)
    const lucia = track([
      [0, L_.look], [a('l01') + 0.05, L_.ask], [a('l02') + 0.5, L_.look], [a('l03') - 0.1, L_.unamused], [a('l04') + 0.5, L_.look], [a('l05') - 0.1, L_.already],
      [a('l06'), L_.pat],
      [S2, L_.pat], [a('l08') - 0.15, L_.worried], [a('l09') + 0.5, L_.look], [a('l10') - 0.1, L_.pout],
      [S3, L_.look], [a('l11') - 0.8, L_.phone], [a('l11') + 0.3, L_.phoneTell], [a('l12') + 0.8, L_.phone], [a('l13') - 0.12, L_.defend], [a('l14') + 0.6, L_.glare],
      [S4, L_.cold], [KEYS_OUT - 0.9, L_.pocket], [KEYS_OUT + 0.4, L_.found], [a('l15') + 0.1, L_.mira], [a('l17') - 0.12, L_.excuse], [a('l18') + 0.5, L_.look], [a('l19') - 0.1, L_.logic],
    ], t, 0.26)
    // patting her pockets while she thinks
    if ((t > a('l06') && t < S2 + 0.9) || (t > KEYS_OUT - 0.9 && t < KEYS_OUT)) {
      const k = Math.sin(t * 7.3) * 0.08
      lucia.rSh = [lucia.rSh[0] + k, lucia.rSh[1]]; lucia.lSh = [lucia.lSh[0] - k, lucia.lSh[1]]
    }
    // shivering a bit in the street
    if (t > S4 && t < KEYS_OUT - 0.9) { const s = Math.sin(t * 31) * 0.01; lucia.side += s; dani.side -= s }
    // in the car they sit a bit lower
    if (sc(t) === 3) { dani.sink += 0.08; lucia.sink += 0.08; dani.yaw *= 0.7 }
    return {
      dani, lucia,
      cuts: [
        [0, 'wide'], [a('l02') - 0.08, 'dani'], [a('l03') - 0.08, 'lucia'], [a('l04') - 0.08, 'dani'], [a('l04') + 0.5, 'bowl'], [a('l05') + 0.35, 'lucia'],
        [a('l06') - 0.1, 'daniClose'],
        [S2, 'lock'], [S2 + 1.15, 'landing'], [a('l08') - 0.1, 'lucia'], [a('l09') - 0.08, 'dani'], [a('l10') - 0.08, 'lucia'],
        [S3, 'car'], [a('l11') - 1.3, 'phone'], [a('l11') + 0.7, 'carL'], [a('l12') - 0.08, 'carD'], [a('l13') - 0.08, 'carL'], [a('l14') - 0.08, 'carD'], [a('l14') + 2.0, 'car'],
        [S4, 'street'], [KEYS_OUT - 0.2, 'keys'], [a('l15') - 0.05, 'lucia'], [a('l16') - 0.08, 'dani'], [a('l17') - 0.08, 'lucia'], [a('l18') - 0.08, 'dani'],
        [a('l19') - 0.08, 'lucia'], [a('l19') + 1.55, 'cam'],
      ],
    }
  },
  sfx: () => [],
  overlays: (_l, dur): Overlay[] => [
    { a: 0, b: dur, st: 'Mid', tx: W },
    box(0.05, 2.3, 330, 58, 'Cuando ya llegáis tarde\\Ny ella te dice…'),
  ],
}

export function Pareja13() { return <PairEpisode spec={spec} /> }
