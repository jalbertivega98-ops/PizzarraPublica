// COSAS DE PAREJA · «Elige tú» — formato narrador: Martín cuenta por dentro («Mi novia me dice…»), sin mover la boca;
// Inés solo dice sus frases. Un solo tema. Salón (sofá) → baño → recibidor (ella con abrigo) → el italiano de la esquina.
// Un solo audio continuo, sin música ni efectos. Cortes tranquilos: solo cuando pasa algo.
import { useMemo, useRef, type ReactNode } from 'react'
import { useFrame } from '@react-three/fiber'
import { RoundedBox } from '@react-three/drei'
import * as THREE from 'three'
import { CONV } from './pareja14_data'
import { Hallway, LivingRoom, PairEpisode, Show, pose, track, type Overlay, type PairSpec } from './pareja_kit'
import { clock } from '../engine/clock'

const fm = (c: string, r = 0.8) => new THREE.MeshStandardMaterial({ color: c, roughness: r, flatShading: true })
const DARK = fm('#2b2224')

const at = Object.fromEntries(CONV.map((c) => [c.id, c.at])) as Record<string, number>
/** id of the first line that starts with this text */
const L = (s: string) => CONV.find((c) => c.text.toLowerCase().startsWith(s.toLowerCase()))!.id
const A = (s: string) => at[L(s)]
const S2 = A('Me encierro') - 0.35, S3 = A('Salgo') - 0.3, S4 = A('Pido pasta') - 0.35
const sc = (t: number) => (t < S2 ? 1 : t < S3 ? 2 : t < S4 ? 3 : 4)
const inS = (n: number) => () => sc(clock.t) === n
const LX = -0.42, DX = 0.42, Z = -0.35, HY = 1.52

// ---------------- phone screens (canvas)
const rr = (c: CanvasRenderingContext2D, x: number, y: number, w: number, h: number, r: number) => { c.beginPath(); c.roundRect(x, y, w, h, r); c.fill() }
function useScreen(draw: (c: CanvasRenderingContext2D, w: number, h: number) => void) {
  return useMemo(() => {
    const cv = document.createElement('canvas'); cv.width = 540; cv.height = 1100
    draw(cv.getContext('2d')!, cv.width, cv.height)
    const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace
    return tex
  }, [])
}
function MapsScreen() {
  const tex = useScreen((c, w, h) => {
    c.fillStyle = '#f4f4f2'; c.fillRect(0, 0, w, h)
    c.fillStyle = '#ffffff'; rr(c, 24, 40, w - 48, 84, 42)
    c.fillStyle = '#6b6b6b'; c.font = '34px sans-serif'; c.fillText('Restaurantes cerca', 60, 94)
    const items: [string, string, string][] = [['Mexicano La Lupe', '4,3 ★ · 300 m', '#d4553b'], ['Taberna griega Ítaca', '4,5 ★ · 450 m', '#2f6db5'], ['Thai Garden', '4,1 ★ · 600 m', '#e0a63c'], ['Burger Brothers', '4,0 ★ · 700 m', '#7a4f2e']]
    items.forEach(([n, s, col], i) => {
      const y = 170 + i * 220
      c.fillStyle = '#ffffff'; rr(c, 24, y, w - 48, 196, 18)
      c.fillStyle = col; rr(c, 44, y + 22, 150, 150, 14)
      if (i === 2) { // the thai place with a cat photo
        c.fillStyle = '#f3c27a'; c.beginPath(); c.arc(119, y + 112, 46, 0, Math.PI * 2); c.fill()
        c.beginPath(); c.moveTo(80, y + 84); c.lineTo(92, y + 44); c.lineTo(108, y + 72); c.fill()
        c.beginPath(); c.moveTo(158, y + 84); c.lineTo(146, y + 44); c.lineTo(130, y + 72); c.fill()
        c.fillStyle = '#2b2224'; c.beginPath(); c.arc(103, y + 106, 6, 0, 7); c.arc(135, y + 106, 6, 0, 7); c.fill()
      }
      c.fillStyle = '#1d1d1f'; c.font = '600 34px sans-serif'; c.fillText(n, 216, y + 78)
      c.fillStyle = '#6b6b6b'; c.font = '28px sans-serif'; c.fillText(s, 216, y + 124)
    })
  })
  return <mesh position={[0, 0, 0.0065]}><planeGeometry args={[0.072, 0.146]} /><meshBasicMaterial map={tex} toneMapped={false} /></mesh>
}
function GroupScreen() {
  const tex = useScreen((c, w, h) => {
    c.fillStyle = '#0b141a'; c.fillRect(0, 0, w, h)
    c.fillStyle = '#1f2c33'; c.fillRect(0, 0, w, 150)
    c.fillStyle = '#e9edef'; c.font = '700 38px sans-serif'; c.fillText('Los de siempre 🍻', 40, 90)
    c.fillStyle = '#8696a0'; c.font = '26px sans-serif'; c.fillText('Álex, Rubén, Sergio, tú', 40, 128)
    // my message
    c.font = '40px sans-serif'; const tw = c.measureText('Emergencia').width
    c.fillStyle = '#005c4b'; rr(c, w - tw - 110, 230, tw + 80, 86, 20)
    c.fillStyle = '#e9edef'; c.fillText('Emergencia', w - tw - 70, 287)
    // three voice notes + one text
    for (let i = 0; i < 3; i++) {
      const y = 360 + i * 120
      c.fillStyle = '#202c33'; rr(c, 34, y, 380, 96, 20)
      c.fillStyle = '#53bdeb'; c.beginPath(); c.moveTo(70, y + 30); c.lineTo(70, y + 66); c.lineTo(100, y + 48); c.fill()
      c.fillStyle = '#8696a0'; for (let k = 0; k < 20; k++) { const hh = 8 + ((k * 37 + i * 11) % 30); c.fillRect(120 + k * 12, y + 48 - hh / 2, 6, hh) }
      c.fillStyle = '#8696a0'; c.font = '24px sans-serif'; c.fillText(['0:07', '0:12', '0:04'][i], 360, y + 82)
    }
    c.font = '38px sans-serif'; const t2 = 'suerte, campeón'; const w2 = c.measureText(t2).width
    c.fillStyle = '#202c33'; rr(c, 34, 740, w2 + 60, 86, 20); c.fillStyle = '#e9edef'; c.fillText(t2, 64, 797)
  })
  return <mesh position={[0, 0, 0.0065]}><planeGeometry args={[0.072, 0.146]} /><meshBasicMaterial map={tex} toneMapped={false} /></mesh>
}
function ClockScreen() {
  const tex = useScreen((c, w, h) => {
    const g = c.createLinearGradient(0, 0, 0, h); g.addColorStop(0, '#2d3a5c'); g.addColorStop(1, '#141a2b'); c.fillStyle = g; c.fillRect(0, 0, w, h)
    c.fillStyle = '#ffffff'; c.textAlign = 'center'; c.font = '30px sans-serif'; c.fillText('jueves, 26 de noviembre', w / 2, 210)
    c.font = '200 190px sans-serif'; c.fillText('21:45', w / 2, 390)
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
/** phone inserts, each staged far from the sets with its own light */
const INS: Record<string, [number, number, number]> = { maps: [20, 1, 0], group: [24, 1, 0], clock: [28, 1, 0] }
function PhoneInsert({ p, screen }: { p: [number, number, number]; screen: ReactNode }) {
  const g = useRef<THREE.Group>(null!)
  useFrame(() => { g.current.rotation.z = Math.sin(clock.t * 1.3) * 0.02; g.current.rotation.x = Math.sin(clock.t * 0.9) * 0.02 })
  return (
    <group position={p}>
      <pointLight position={[0.1, 0.3, 0.5]} intensity={1.2} distance={2} color="#cfd9ff" />
      <mesh position={[0, -0.02, -0.06]}><planeGeometry args={[0.6, 0.6]} /><meshStandardMaterial color="#3e5f8f" roughness={0.95} /></mesh>
      <group ref={g}><PhoneProp screen={screen} /></group>
    </group>
  )
}

// ---------------- bathroom (he sits on the closed lid at DX, Z)
function Bathroom() {
  const tile = fm('#cfe0e3', 0.5), tile2 = fm('#b9cfd3', 0.5), white = fm('#f3f1ec', 0.4)
  return (
    <group>
      <hemisphereLight args={['#f1f7ff', '#30363a', 0.9]} />
      <pointLight position={[0.2, 2.4, 0.4]} intensity={3.2} distance={5} decay={1.5} color="#f4f8ff" />
      <pointLight position={[0, 1.6, 2.4]} intensity={1.1} distance={5} color="#fff0e0" />
      <directionalLight position={[1.5, 3, 2.5]} intensity={0.6} castShadow shadow-mapSize={[1024, 1024]} />
      <mesh rotation-x={-Math.PI / 2} material={fm('#8a9a9c', 0.5)} receiveShadow><planeGeometry args={[6, 6]} /></mesh>
      <mesh position={[0, 1.5, -1.05]} material={tile} receiveShadow><planeGeometry args={[6, 3]} /></mesh>
      {Array.from({ length: 12 }, (_, i) => <mesh key={i} position={[-2.75 + i * 0.5, 1.5, -1.045]} material={tile2}><planeGeometry args={[0.015, 3]} /></mesh>)}
      {Array.from({ length: 6 }, (_, i) => <mesh key={i} position={[0, 0.25 + i * 0.5, -1.044]} material={tile2}><planeGeometry args={[6, 0.015]} /></mesh>)}
      {/* toilet under him */}
      <group position={[DX, 0, Z - 0.05]}>
        <mesh position={[0, 0.22, 0]} material={white} castShadow><cylinderGeometry args={[0.2, 0.16, 0.44, 10]} /></mesh>
        <mesh position={[0, 0.46, 0.02]} material={white}><cylinderGeometry args={[0.23, 0.23, 0.04, 12]} /></mesh>
        <RoundedBox args={[0.5, 0.42, 0.2]} radius={0.04} smoothness={2} position={[0, 0.75, -0.45]} material={white} castShadow />
      </group>
      {/* sink + mirror on the left, towel, small shelf with bottles */}
      <group position={[-0.55, 0, -0.85]}>
        <mesh position={[0, 0.42, 0]} material={white}><cylinderGeometry args={[0.07, 0.09, 0.84, 8]} /></mesh>
        <RoundedBox args={[0.6, 0.12, 0.38]} radius={0.04} smoothness={2} position={[0, 0.9, 0.04]} material={white} />
        <mesh position={[0, 1.02, -0.1]} material={fm('#c9cdd0', 0.2)}><cylinderGeometry args={[0.015, 0.015, 0.14, 6]} /></mesh>
        <mesh position={[0, 1.55, -0.17]}><boxGeometry args={[0.55, 0.7, 0.02]} /><meshStandardMaterial color="#a9c3cc" roughness={0.1} metalness={0.3} /></mesh>
        {[-0.15, 0, 0.13].map((x, i) => <mesh key={x} position={[x, 1.28, -0.12]} material={fm(['#e2725b', '#6fb3a8', '#f2d7a6'][i])}><cylinderGeometry args={[0.03, 0.03, 0.12 + i * 0.03, 6]} /></mesh>)}
      </group>
      <group position={[1.25, 1.2, -1.0]}>
        <mesh material={DARK}><boxGeometry args={[0.5, 0.03, 0.04]} /></mesh>
        <mesh position={[0, -0.28, 0.03]} material={fm('#e0a63c', 0.95)}><boxGeometry args={[0.4, 0.55, 0.03]} /></mesh>
      </group>
    </group>
  )
}

// ---------------- the italian place on the corner: they sit side by side at a table facing camera
function Italiano() {
  const flame = useRef<THREE.PointLight>(null!)
  useFrame(() => { flame.current.intensity = 1.6 + 0.25 * Math.sin(clock.t * 9.1) * Math.sin(clock.t * 3.3) })
  return (
    <group>
      <hemisphereLight args={['#ffe2c2', '#2a1a14', 0.8]} />
      <pointLight position={[0, 2.3, 0.5]} intensity={2.6} distance={5} decay={1.5} color="#ffcf8a" />
      <pointLight position={[0, 1.6, 2.4]} intensity={1.0} distance={5} color="#fff0e0" />
      <pointLight ref={flame} position={[0, 1.05, 0.15]} distance={2} decay={1.6} color="#ffb05a" />
      <mesh rotation-x={-Math.PI / 2} material={fm('#6b3f2a', 0.7)} receiveShadow><planeGeometry args={[6, 6]} /></mesh>
      <mesh position={[0, 1.5, -1.05]} material={fm('#c9a36b')} receiveShadow><planeGeometry args={[6, 3]} /></mesh>
      <mesh position={[0, 0.5, -1.04]} material={fm('#7a2f2f')}><planeGeometry args={[6, 1.0]} /></mesh>
      {/* framed picture: hills + sun, and a little italian flag */}
      <group position={[0, 2.05, -1.03]}>
        <mesh material={DARK}><boxGeometry args={[0.9, 0.55, 0.03]} /></mesh>
        <mesh position={[0, 0, 0.02]} material={fm('#f2d7a6')}><planeGeometry args={[0.8, 0.45]} /></mesh>
        <mesh position={[-0.15, -0.12, 0.025]} material={fm('#6f8f4a')}><circleGeometry args={[0.25, 8, 0, Math.PI]} /></mesh>
        <mesh position={[0.2, -0.14, 0.026]} material={fm('#58753c')}><circleGeometry args={[0.2, 8, 0, Math.PI]} /></mesh>
        <mesh position={[0.22, 0.1, 0.025]} material={fm('#e9a23b')}><circleGeometry args={[0.06, 8]} /></mesh>
      </group>
      {[['#2e8b57', -0.1], ['#f4f1ea', 0], ['#c8372d', 0.1]].map(([c, x]) => <mesh key={x as number} position={[1.3 + (x as number), 2.15, -1.03]} material={fm(c as string)}><planeGeometry args={[0.1, 0.24]} /></mesh>)}
      {/* bench behind them */}
      <RoundedBox args={[2.0, 0.5, 0.3]} radius={0.05} smoothness={2} position={[0, 0.8, Z - 0.3]} material={fm('#5a2e1a', 0.7)} />
      {/* table with checkered cloth, two plates of pasta, candle in a bottle, bread */}
      <group position={[0, 0, Z + 0.55]}>
        <mesh position={[0, 0.88, 0]} material={fm('#f4f1ea')} receiveShadow><boxGeometry args={[1.6, 0.04, 0.6]} /></mesh>
        {Array.from({ length: 8 }, (_, i) => <mesh key={i} position={[-0.7 + i * 0.2, 0.902, 0]} rotation-x={-Math.PI / 2} material={fm('#c8372d')}><planeGeometry args={[0.1, 0.6]} /></mesh>)}
        <mesh position={[0, 0.6, 0.29]} material={fm('#f4f1ea')}><boxGeometry args={[1.6, 0.55, 0.02]} /></mesh>
        {[LX, DX].map((x) => (
          <group key={x} position={[x, 0.91, 0.05]}>
            <mesh material={fm('#ffffff', 0.4)}><cylinderGeometry args={[0.15, 0.12, 0.03, 12]} /></mesh>
            {[0, 1, 2, 3, 4, 5].map((i) => <mesh key={i} position={[Math.cos(i * 1.1) * 0.05, 0.035, Math.sin(i * 1.1) * 0.04]} material={fm('#e9b44c')}><torusGeometry args={[0.035, 0.012, 4, 8]} /></mesh>)}
            <mesh position={[0, 0.05, 0]} material={fm('#c8372d')}><icosahedronGeometry args={[0.04, 0]} /></mesh>
          </group>
        ))}
        <group position={[0, 0.9, -0.05]}>
          <mesh position={[0, 0.1, 0]} material={fm('#2f6a3a', 0.3)}><cylinderGeometry args={[0.04, 0.05, 0.2, 8]} /></mesh>
          <mesh position={[0, 0.25, 0]} material={fm('#f4ecd8')}><cylinderGeometry args={[0.012, 0.012, 0.1, 6]} /></mesh>
          <mesh position={[0, 0.315, 0]}><coneGeometry args={[0.012, 0.035, 6]} /><meshBasicMaterial color="#ffcf6a" toneMapped={false} /></mesh>
        </group>
      </group>
    </group>
  )
}

// ---------------- acting (seated on the sofa: her left, him right)
const sofaArms = { rSh: [0.35, -0.12] as [number, number], rEl: -1.2, lSh: [0.35, 0.12] as [number, number], lEl: -1.2 }
const phoneArms = { rSh: [0.75, -0.05] as [number, number], rEl: -1.6 }
const D = {
  calm: pose({ yaw: -0.15, lids: 0.3, brows: 0.05, ...sofaArms }),
  her: pose({ yaw: -0.45, lids: 0.25, brows: 0.15, ...sofaArms }),
  cam: pose({ yaw: 0.05, lids: 0.45, brows: 0.05, smile: -0.1, ...sofaArms }),
  camBrow: pose({ yaw: 0.05, lids: 0.35, brows: 0.45, browTilt: -0.4, smile: -0.15, ...sofaArms }),
  doubt: pose({ yaw: -0.4, lids: 0.2, brows: 0.5, browTilt: -0.5, smile: 0.05, ...sofaArms }),
  small: pose({ yaw: -0.4, pitch: 0.12, lids: 0.35, brows: 0.3, browTilt: -0.6, smile: -0.2, ...sofaArms }),
  phone: pose({ yaw: 0.05, pitch: 0.35, lids: 0.25, brows: 0.2, ...sofaArms, ...phoneArms }),
  show: pose({ yaw: -0.4, lids: 0.15, brows: 0.45, smile: 0.25, ...sofaArms, rSh: [0.8, 0.35], rEl: -1.3 }),
  tired: pose({ yaw: -0.1, pitch: 0.08, lids: 0.6, brows: -0.1, smile: -0.15, lean: 0.05, ...sofaArms }),
  loo: pose({ yaw: 0, pitch: 0.4, lids: 0.3, brows: 0.35, browTilt: -0.4, lean: 0.1, ...sofaArms, rSh: [0.95, -0.05], rEl: -1.7, lSh: [0.9, 0.05], lEl: -1.7 }),
  looCam: pose({ yaw: 0.05, pitch: 0.05, lids: 0.45, brows: 0.1, smile: -0.1, lean: 0.05, ...sofaArms, rSh: [0.95, -0.05], rEl: -1.7, lSh: [0.9, 0.05], lEl: -1.7 }),
  ask: pose({ yaw: -0.45, lids: 0.1, brows: 0.6, ...sofaArms }),
  stunned: pose({ yaw: -0.45, lids: 0, brows: 0.95, browTilt: -0.2, smile: -0.1, ...sofaArms }),
  dead: pose({ yaw: 0.05, lids: 0.55, brows: -0.1, smile: -0.2, ...sofaArms }),
  fork: pose({ yaw: 0, pitch: 0.25, lids: 0.4, brows: 0, ...sofaArms, rSh: [0.6, -0.1], rEl: -1.5 }),
  last: pose({ yaw: 0.08, pitch: 0.02, lids: 0.55, brows: 0.15, browTilt: -0.3, smile: -0.25, ...sofaArms }),
}
const herArms = { rSh: [0.35, -0.12] as [number, number], rEl: -1.2, lSh: [0.35, 0.12] as [number, number], lEl: -1.2 }
const I = {
  smile: pose({ yaw: 0.45, lids: 0.15, brows: 0.3, smile: 0.6, ...herArms }),
  sweet: pose({ yaw: 0.45, lids: 0.2, brows: 0.35, browTilt: -0.3, smile: 0.45, roll: -0.06, ...herArms }),
  meh: pose({ yaw: 0.45, lids: 0.45, brows: -0.1, browTilt: 0.4, smile: -0.3, ...herArms }),
  flat: pose({ yaw: 0.45, lids: 0.35, brows: 0.05, smile: -0.1, ...herArms }),
  stare: pose({ yaw: 0.5, lids: 0.5, brows: -0.25, browTilt: 0.7, smile: -0.35, ...herArms }),
  cold: pose({ yaw: 0.2, pitch: -0.05, lids: 0.45, brows: -0.15, browTilt: 0.5, smile: -0.3, ...herArms, lSh: [0.6, 0.6], lEl: -1.9, rSh: [0.6, -0.6], rEl: -1.9 }),
  eyes: pose({ yaw: 0.5, lids: 0.15, brows: 0.2, smile: 0, ...herArms }),
  innocent: pose({ yaw: 0.45, lids: 0.05, brows: 0.6, browTilt: -0.4, smile: 0.35, ...herArms }),
  ready: pose({ yaw: 0.4, lids: 0.1, brows: 0.4, smile: 0.55, ...herArms, rSh: [0.5, -0.4], rEl: -1.0 }),
  shrug: pose({ yaw: 0.45, lids: 0.2, brows: 0.5, browTilt: -0.3, smile: 0.4, roll: -0.08, ...herArms, lSh: [0.5, 0.5], lEl: -1.2, rSh: [0.5, -0.5], rEl: -1.2 }),
  eat: pose({ yaw: 0.1, pitch: 0.25, lids: 0.3, brows: 0.1, smile: 0.2, ...herArms, rSh: [0.6, -0.1], rEl: -1.5 }),
  surprised: pose({ yaw: 0.45, lids: 0, brows: 0.8, browTilt: -0.2, smile: 0.1, ...herArms }),
}

const DaniHand = () => (
  <group>
    <Show show={() => (clock.t > A('Abro el móvil') - 0.3 && clock.t < A('¿Y a ti') - 0.2) || inS(2)()}><group rotation={[0.3, 0, 0]} position={[0, -0.02, 0.05]}><PhoneProp /></group></Show>
    <Show show={inS(4)}><mesh position={[0, -0.03, 0.06]} rotation-x={0.4} material={fm('#c9cdd0', 0.25)}><boxGeometry args={[0.012, 0.16, 0.008]} /></mesh></Show>
  </group>
)
const LuciaHand = () => <Show show={inS(4)}><mesh position={[0, -0.03, 0.06]} rotation-x={0.4} material={fm('#c9cdd0', 0.25)}><boxGeometry args={[0.012, 0.16, 0.008]} /></mesh></Show>

const V = (x: number, y: number, z: number) => [x, y, z] as [number, number, number]
const ins = (k: string) => ({ p: V(INS[k][0], INS[k][1] + 0.01, INS[k][2] + 0.27), l: V(INS[k][0], INS[k][1], INS[k][2]), fov: 36, push: 0.03 })
const shots = {
  // sofa
  two: { p: V(0, HY + 0.22, Z + 2.75), l: V(0, HY - 0.15, Z), fov: 44, push: 0.3 },
  lucia: { p: V(-0.1, HY + 0.12, Z + 2.25), l: V(LX, HY - 0.1, Z), fov: 36, push: 0.1 },
  dani: { p: V(0.1, HY + 0.12, Z + 2.25), l: V(DX, HY - 0.1, Z), fov: 36, push: 0.1 },
  daniCam: { p: V(DX - 0.02, HY + 0.06, Z + 1.95), l: V(DX, HY - 0.06, Z), fov: 34, push: 0.06 },
  maps: ins('maps'), group: ins('group'), clock: ins('clock'),
  // bathroom
  loo: { p: V(DX - 0.2, HY + 0.3, Z + 2.5), l: V(DX - 0.15, HY - 0.3, Z), fov: 44, push: 0.15 },
  // hallway (standing: sink -0.12)
  door: { p: V(-0.25, HY + 0.2, Z + 2.5), l: V(-0.15, HY - 0.05, Z), fov: 42, push: 0.15 },
  doorL: { p: V(-0.12, HY + 0.2, Z + 2.25), l: V(LX, HY + 0.04, Z), fov: 36, push: 0.08 },
  doorD: { p: V(0.12, HY + 0.2, Z + 2.25), l: V(DX, HY + 0.04, Z), fov: 36, push: 0.08 },
  doorCam: { p: V(DX - 0.02, HY + 0.16, Z + 1.95), l: V(DX, HY + 0.08, Z), fov: 34, push: 0.06 },
  // restaurant
  table: { p: V(0, HY + 0.15, Z + 3.0), l: V(0, HY - 0.32, Z + 0.2), fov: 44, push: 0.25 },
  tableL: { p: V(-0.1, HY + 0.14, Z + 2.35), l: V(LX, HY - 0.12, Z), fov: 36, push: 0.08 },
  tableCam: { p: V(DX - 0.02, HY + 0.08, Z + 2.0), l: V(DX, HY - 0.05, Z), fov: 34, push: 0.06 },
}

const herIds = CONV.filter((c) => c.her).map((c) => c.id)
const donde = L('¿Dónde')
const W = '{\\an8\\pos(540,70)\\fs34\\bord2\\shad0\\alpha&H50&}@pizarrapublica'
const spec: PairSpec = {
  id: 'pareja14',
  script: CONV.map((c) => ({ id: c.id, text: c.text })),
  fixedAt: at,
  gap: {},
  her: herIds,
  talk: true,
  // the narrator is inside his head: only «¿Dónde?» is said aloud
  quiet: CONV.filter((c) => !c.her && c.id !== donde).map((c) => c.id),
  bg: '#1a1420',
  tail: 2.4,
  keyColor: '&H8A6A1E&',
  Set: ({ st }) => {
    return (
      <group>
        <Show show={inS(1)}><LivingRoom tv={() => 0.6} /></Show>
        <Show show={inS(2)}><Bathroom /></Show>
        <Show show={inS(3)}><Hallway /></Show>
        <Show show={inS(4)}><Italiano /></Show>
        <PhoneInsert p={INS.maps} screen={<MapsScreen />} />
        <PhoneInsert p={INS.group} screen={<GroupScreen />} />
        <PhoneInsert p={INS.clock} screen={<ClockScreen />} />
        {void st}
      </group>
    )
  },
  pos: { lucia: [LX, 0.5, Z], dani: [DX, 0.5, Z] },
  shots,
  luciaHand: <LuciaHand />,
  daniHand: <DaniHand />,
  frame: (t, a, l, st) => {
    const s = sc(t)
    st.luciaTop = s >= 3 ? '#c98b3a' : undefined // her coat on to go out
    const g = (txt: string) => A(txt)
    const lastQ = CONV.filter((c) => c.text.startsWith('¿Otra vez pasta')).slice(-1)[0].at
    const dani = track([
      [0, D.calm], [g('Y me lo dice') - 0.1, D.her], [g('Siempre elige') + 0.1, D.cam], [g('Digo el italiano') - 0.1, D.her],
      [g('Vale. El japonés') - 0.1, D.doubt], [g('No comió') - 0.1, D.camBrow], [g('Pero no digo') + 0.2, D.small], [g('Digo hamburguesa') - 0.1, D.her],
      [g('Me mira como') + 0.3, D.small], [g('En mi casa') - 0.1, D.cam], [g('Abro el móvil') - 0.2, D.phone], [g('Se lo enseño') - 0.1, D.show],
      [g('¿Y a ti') + 0.4, D.her], [g('A mí me apetece') - 0.1, D.cam], [g('Las cocinas') + 0.1, D.tired],
      [S2, D.loo], [g('Me contestan') + 1.2, D.looCam],
      [S3, D.her], [g('¿Dónde') - 0.15, D.ask], [g('En el italiano') + 0.5, D.stunned], [g('El italiano de la') - 0.1, D.dead], [g('Es que de repente') + 0.4, D.her],
      [S4, D.fork], [lastQ + 0.3, D.her], [CONV[CONV.length - 1].at - 0.1, D.last],
    ], t, 0.3)
    const lucia = track([
      [0, I.flat], [g('Y me lo dice') - 0.2, I.smile], [g('Elige tú') + 0.8, I.sweet], [g('¿Otra vez pasta') - 0.15, I.meh], [g('Ayer comí') - 0.1, I.flat],
      [g('Me mira como') - 0.15, I.stare], [g('Tú verás') + 0.6, I.cold], [g('Se lo enseño') + 0.3, I.eyes], [g('¿Y a ti') + 0.8, I.stare],
      [S3, I.ready], [g('En el italiano') - 0.1, I.sweet], [g('Es que de repente') - 0.1, I.shrug],
      [S4, I.eat], [lastQ - 0.15, I.surprised],
    ], t, 0.3)
    // the moment she shows/looks: shift his eyes to the phone, hers to him
    if (s === 2) lucia.side = -30 // she is not in the bathroom
    if (s === 3) { dani.sink = -0.12; lucia.sink = -0.12 } // standing in the hallway
    // fork to mouth every now and then at the restaurant
    if (s === 4) { const k = Math.max(0, Math.sin(t * 1.4)); dani.rEl -= 0.25 * k; lucia.rEl -= 0.25 * Math.max(0, Math.sin(t * 1.2 + 1)) }
    return {
      dani, lucia,
      cuts: [
        [0, 'two'], [g('Y me lo dice') - 0.1, 'lucia'], [g('Siempre elige') - 0.1, 'daniCam'], [g('Digo el italiano') - 0.1, 'two'],
        [g('¿Otra vez pasta') - 0.08, 'lucia'], [g('Vale. El japonés') - 0.1, 'dani'], [g('Ayer comí') - 0.08, 'lucia'], [g('No comió') - 0.1, 'daniCam'],
        [g('Digo hamburguesa') - 0.1, 'two'], [g('Tú verás') - 0.08, 'lucia'], [g('En mi casa') - 0.1, 'daniCam'],
        [g('Abro el móvil') + 0.4, 'maps'], [g('Se lo enseño') - 0.1, 'two'], [g('¿Y a ti') - 0.08, 'lucia'], [g('A mí me apetece') - 0.1, 'daniCam'],
        [g('Las cocinas') - 0.1, 'clock'],
        [S2, 'loo'], [g('Me encierro') + 1.3, 'group'], [g('Me contestan') + 1.4, 'loo'],
        [S3, 'door'], [g('Venga, que') - 0.08, 'doorL'], [g('¿Dónde') - 0.1, 'doorD'], [g('En el italiano') - 0.08, 'doorL'], [g('El italiano de la') - 0.1, 'doorCam'],
        [g('Es que de repente') - 0.08, 'doorL'],
        [S4, 'table'], [lastQ - 0.08, 'tableL'], [CONV[CONV.length - 1].at - 0.1, 'tableCam'],
      ],
    }
  },
  sfx: () => [],
  overlays: (_l, dur): Overlay[] => [{ a: 0, b: dur, st: 'Mid', tx: W }],
}

export function Pareja14() { return <PairEpisode spec={spec} /> }
