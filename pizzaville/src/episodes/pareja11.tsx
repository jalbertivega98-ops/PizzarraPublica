// COSAS DE PAREJA · EP. 11 (prueba del estilo nuevo) — «El GTA 6».
// Personajes toon de cuerpo entero, caras exageradas, 6 escenarios: sofá, súper, coche, cocina, baño y sofá por la mañana.
// T = pensamiento de Dani (voz con eco), D = Dani en voz alta, H = Lucía (voz de chica).
import { useMemo, useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { RoundedBox } from '@react-three/drei'
import * as THREE from 'three'
import { clock, seg } from '../engine/clock'
import { toon, Ol } from '../scene/Toon'
import { B, FX, Show, ToonEpisode, box, tp, type FP, type Shot, type ToonSpec } from './toon_kit'
import SCRIPT_JSON from '../../voz/pareja11.json'

const SCRIPT = (SCRIPT_JSON as any).lines.map((l: any) => ({ id: l.id, kind: l.kind, text: l.text })) as ToonSpec['script']

// ---------------------------------------------------------------- poses
type O = Parameters<typeof tp>[0]
const sit = (f: FP, o: O = {}) => tp({ ...B.sit, ...o, f })
const stand = (f: FP, o: O = {}) => tp({ ...o, f })

// ---------------------------------------------------------------- props
function Pad() {
  const m = useMemo(() => ({ b: toon('#2b2d3a'), r: toon('#ff4d6d'), g: toon('#3ddc97'), y: toon('#ffd23f'), c: toon('#4da3ff') }), [])
  return (
    <group position={[-0.1, 0.02, 0.06]} rotation={[0.9, 0, 0]}>
      <RoundedBox args={[0.26, 0.05, 0.11]} radius={0.022} smoothness={3} material={m.b}><Ol w={0.006} /></RoundedBox>
      {[-1, 1].map((s) => <mesh key={s} material={m.b} position={[s * 0.11, -0.005, -0.06]} rotation-x={0.4}><capsuleGeometry args={[0.035, 0.06, 4, 8]} /><Ol w={0.006} /></mesh>)}
      {[[0.07, 0.02, m.r], [0.09, -0.01, m.g], [0.05, -0.01, m.c], [0.07, -0.035, m.y]].map(([x, z, mm], i) => <mesh key={i} material={mm as THREE.Material} position={[x as number, 0.03, z as number]}><sphereGeometry args={[0.012, 8, 6]} /></mesh>)}
      <mesh material={m.b} position={[-0.07, 0.035, 0]}><boxGeometry args={[0.05, 0.012, 0.016]} /></mesh>
    </group>
  )
}
function Yogurt({ lid = '#2f7dff', label = '#ffffff' }: { lid?: string; label?: string }) {
  const m = useMemo(() => ({ c: toon(label), l: toon(lid) }), [lid, label])
  return (
    <group>
      <mesh material={m.c} position={[0, 0.045, 0]}><cylinderGeometry args={[0.04, 0.032, 0.09, 14]} /><Ol w={0.004} /></mesh>
      <mesh material={m.l} position={[0, 0.092, 0]}><cylinderGeometry args={[0.043, 0.043, 0.008, 14]} /></mesh>
    </group>
  )
}
function Headphones({ color = '#ff4d6d' }: { color?: string }) {
  const m = useMemo(() => toon(color), [color])
  return (
    <group>
      <mesh material={m} position={[0, 0.03, -0.02]} rotation={[0, 0, 0]}><torusGeometry args={[0.31, 0.025, 8, 24, Math.PI]} /><Ol w={0.005} /></mesh>
      {[-1, 1].map((s) => <mesh key={s} material={m} position={[s * 0.3, -0.01, -0.02]} rotation-z={Math.PI / 2}><cylinderGeometry args={[0.085, 0.085, 0.07, 16]} /><Ol w={0.006} /></mesh>)}
    </group>
  )
}
function Shades() {
  const m = useMemo(() => toon('#111111'), [])
  const f = useMemo(() => toon('#ff3fa4'), [])
  return (
    <group position={[0, 0.03, 0.262]}>
      {[-1, 1].map((s) => <mesh key={s} material={m} position={[s * 0.095, 0, 0]}><boxGeometry args={[0.15, 0.08, 0.02]} /></mesh>)}
      <mesh material={f} position={[0, 0.03, 0]}><boxGeometry args={[0.38, 0.025, 0.025]} /></mesh>
    </group>
  )
}

// ---------------------------------------------------------------- TV screen (generic neon game title / film / gameplay)
function screenTexture() {
  const cv = document.createElement('canvas'); cv.width = 512; cv.height = 288
  const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace
  const c = cv.getContext('2d')!
  const draw = (mode: string, t: number) => {
    if (mode === 'film') {
      const g = c.createLinearGradient(0, 0, 0, 288); g.addColorStop(0, '#f7b7c9'); g.addColorStop(1, '#a45d8c'); c.fillStyle = g; c.fillRect(0, 0, 512, 288)
      c.fillStyle = '#ffffff'; c.font = 'bold 34px sans-serif'; c.textAlign = 'center'; c.fillText('AMOR EN PARÍS 4', 256, 70)
      for (const [x, s] of [[200, 1], [312, -1]] as const) { c.fillStyle = '#3a1f35'; c.beginPath(); c.ellipse(x, 190, 30, 40, 0, 0, Math.PI * 2); c.fill(); c.beginPath(); c.ellipse(x, 130, 24, 26, 0, 0, Math.PI * 2); c.fill(); void s }
      c.fillStyle = '#ff2d55'; c.font = '48px sans-serif'; c.fillText('♥', 256, 120 + Math.sin(t * 4) * 6)
      return
    }
    // neon sunset city
    const g = c.createLinearGradient(0, 0, 0, 288); g.addColorStop(0, '#2b0f54'); g.addColorStop(0.55, '#ff4fa3'); g.addColorStop(1, '#ffb347'); c.fillStyle = g; c.fillRect(0, 0, 512, 288)
    c.fillStyle = '#ffe66d'; c.beginPath(); c.arc(256, 170, 70, Math.PI, 0); c.fill()
    c.fillStyle = '#ff4fa3'; for (let i = 0; i < 5; i++) c.fillRect(180, 120 + i * 10, 152, 3 + i)
    c.fillStyle = '#1a0b2e'
    for (let i = 0; i < 14; i++) { const h = 30 + ((i * 37) % 70); c.fillRect(i * 38 - 5, 200 - h, 30, h + 90) }
    const palm = (x: number, h: number) => { c.fillRect(x, 288 - h, 6, h); for (let k = 0; k < 6; k++) { const a = -Math.PI / 2 + (k - 2.5) * 0.55; c.beginPath(); c.moveTo(x + 3, 288 - h); c.quadraticCurveTo(x + 3 + Math.cos(a) * 40, 288 - h + Math.sin(a) * 30, x + 3 + Math.cos(a) * 60, 288 - h + 22); c.lineTo(x + 3 + Math.cos(a) * 56, 288 - h + 28); c.quadraticCurveTo(x + 3 + Math.cos(a) * 36, 288 - h + Math.sin(a) * 18, x + 3, 288 - h + 6); c.fill() } }
    palm(40, 150); palm(470, 170); palm(420, 110)
    if (mode === 'game') {
      c.fillStyle = 'rgba(0,0,0,0.35)'; c.fillRect(0, 230, 512, 58)
      c.fillStyle = '#ffffff'; c.font = 'bold 26px sans-serif'; c.textAlign = 'left'; c.fillText('MISIÓN 40', 16, 266)
      c.fillStyle = '#3ddc97'; c.textAlign = 'right'; c.fillText('★★★★★', 496, 266)
      for (let i = 0; i < 6; i++) { c.fillStyle = '#fff'; const x = (t * 400 + i * 90) % 560 - 20; c.fillRect(x, 215, 40, 4) }
      return
    }
    c.textAlign = 'center'; c.font = 'bold 30px sans-serif'
    if (Math.floor(t * 2) % 2 === 0) { c.fillStyle = '#ffffff'; c.fillText('PULSA START', 256, 262) }
  }
  return { tex, draw }
}
function TV({ st, z = 2.4 }: { st: Record<string, any>; z?: number }) {
  const s = useMemo(screenTexture, [])
  const light = useRef<THREE.PointLight>(null!)
  useFrame(() => { s.draw(st.tv ?? 'start', clock.t); s.tex.needsUpdate = true; light.current.color.set(st.tv === 'film' ? '#ffb0c8' : '#ff6fd0'); light.current.intensity = 2.2 + 0.4 * Math.sin(clock.t * 5) })
  const m = useMemo(() => ({ b: toon('#16141c'), w: toon('#7a4b2a') }), [])
  return (
    <group position={[0, 0, z]} rotation-y={Math.PI}>
      <mesh material={m.w} position={[0, 0.25, 0]}><boxGeometry args={[1.6, 0.5, 0.45]} /><Ol /></mesh>
      <mesh material={m.b} position={[0, 1.05, 0]}><boxGeometry args={[1.5, 0.88, 0.06]} /><Ol /></mesh>
      <mesh position={[0, 1.05, 0.035]}><planeGeometry args={[1.42, 0.8]} /><meshBasicMaterial map={s.tex} toneMapped={false} /></mesh>
      <pointLight ref={light} position={[0, 1.1, 0.8]} distance={5} decay={1.3} />
    </group>
  )
}

// ---------------------------------------------------------------- sets
function Lights({ key1 = '#fff2e0', amb = 0.9, sky = '#ffe6cc', ground = '#40304a', k = 1.4 }: { key1?: string; amb?: number; sky?: string; ground?: string; k?: number }) {
  return (
    <group>
      <hemisphereLight args={[sky, ground, amb]} />
      <directionalLight position={[2.5, 4, 4]} intensity={k} color={key1} castShadow shadow-mapSize={[1024, 1024]} shadow-bias={-0.0008}
        shadow-camera-left={-3} shadow-camera-right={3} shadow-camera-top={3} shadow-camera-bottom={-3} />
    </group>
  )
}

function SofaRoom({ st, morning = false }: { st: Record<string, any>; morning?: boolean }) {
  const m = useMemo(() => ({
    wall: toon(morning ? '#f3c9a1' : '#5b3d6b'), floor: toon(morning ? '#c98b5a' : '#6b4630'), rug: toon(morning ? '#7fd1c7' : '#3f8f88'),
    sofa: toon('#e9634b'), cush: toon('#f38b6c'), wood: toon('#8a5a34'), win: toon(morning ? '#9fdcff' : '#1b2550'), frame: toon('#f4efe6'),
    plant: toon('#3fae62'), pot: toon('#f2b33d'), bowl: toon('#4da3ff'), chip: toon('#ffd23f'), can: toon('#3ddc97'), moon: toon('#fff6c9'),
  }), [morning])
  return (
    <group>
      <Lights key1={morning ? '#fff4d6' : '#ffd9b8'} amb={morning ? 1.15 : 0.85} sky={morning ? '#fff1d6' : '#ffd6c2'} ground={morning ? '#40304a' : '#2a2040'} k={morning ? 1.6 : 1.0} />
      <mesh material={m.wall} position={[0, 1.7, -1.3]} receiveShadow><planeGeometry args={[9, 3.4]} /></mesh>
      <mesh material={m.floor} rotation-x={-Math.PI / 2} receiveShadow><planeGeometry args={[9, 9]} /></mesh>
      <mesh material={m.rug} rotation-x={-Math.PI / 2} position={[0, 0.005, 0.5]} receiveShadow><circleGeometry args={[1.4, 32]} /></mesh>
      {/* window */}
      <group position={[-1.3, 1.85, -1.28]}>
        <mesh material={m.frame}><boxGeometry args={[1.0, 0.8, 0.04]} /></mesh>
        <mesh material={m.win} position={[0, 0, 0.025]}><planeGeometry args={[0.88, 0.68]} /></mesh>
        <mesh material={m.moon} position={[morning ? 0.25 : -0.2, 0.15, 0.03]}><circleGeometry args={[morning ? 0.13 : 0.08, 20]} /></mesh>
        <mesh material={m.frame} position={[0, 0, 0.03]}><boxGeometry args={[0.03, 0.7, 0.01]} /></mesh>
      </group>
      {/* poster */}
      <group position={[1.25, 1.95, -1.28]}>
        <mesh material={m.frame}><boxGeometry args={[0.6, 0.8, 0.03]} /></mesh>
        <mesh position={[0, 0, 0.02]}><planeGeometry args={[0.5, 0.7]} /><meshToonMaterial color="#ff4fa3" /></mesh>
        <mesh material={m.chip} position={[0, 0.05, 0.025]}><circleGeometry args={[0.13, 20, 0, Math.PI]} /></mesh>
      </group>
      {/* sofa */}
      <group position={[0, 0, -0.55]}>
        <RoundedBox args={[2.3, 0.3, 0.95]} radius={0.06} smoothness={3} position={[0, 0.2, 0]} material={m.sofa} castShadow receiveShadow><Ol /></RoundedBox>
        <RoundedBox args={[2.3, 0.7, 0.25]} radius={0.08} smoothness={3} position={[0, 0.6, -0.38]} material={m.sofa} castShadow receiveShadow><Ol /></RoundedBox>
        {[-1.2, 1.2].map((x) => <RoundedBox key={x} args={[0.25, 0.58, 0.98]} radius={0.08} smoothness={3} position={[x, 0.4, 0]} material={m.sofa} castShadow><Ol /></RoundedBox>)}
        {[-0.53, 0.53].map((x) => <RoundedBox key={x} args={[1.04, 0.14, 0.78]} radius={0.06} smoothness={3} position={[x, 0.4, 0.06]} material={m.cush} castShadow receiveShadow><Ol w={0.008} /></RoundedBox>)}
      </group>
      {/* coffee table with snacks */}
      <group position={[0, 0, 0.75]}>
        <RoundedBox args={[1.2, 0.06, 0.55]} radius={0.02} smoothness={2} position={[0, 0.36, 0]} material={m.wood} castShadow receiveShadow><Ol w={0.008} /></RoundedBox>
        {[[-0.52, -0.22], [0.52, -0.22], [-0.52, 0.22], [0.52, 0.22]].map(([x, z], i) => <mesh key={i} material={m.wood} position={[x, 0.17, z]}><cylinderGeometry args={[0.03, 0.03, 0.34, 8]} /></mesh>)}
        <mesh material={m.bowl} position={[-0.25, 0.43, 0]}><sphereGeometry args={[0.14, 16, 8, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2]} /><Ol w={0.006} /></mesh>
        {[0, 1, 2, 3, 4, 5, 6].map((i) => <mesh key={i} material={m.chip} position={[-0.25 + Math.cos(i * 2.1) * 0.07, 0.44, Math.sin(i * 2.1) * 0.06]} rotation={[i, i * 2, 0]}><circleGeometry args={[0.04, 7]} /></mesh>)}
        {[0.2, 0.32].map((x) => <mesh key={x} material={m.can} position={[x, 0.45, 0.05]}><cylinderGeometry args={[0.035, 0.035, 0.13, 12]} /><Ol w={0.005} /></mesh>)}
      </group>
      {/* plant */}
      <group position={[1.7, 0, -0.9]}>
        <mesh material={m.pot} position={[0, 0.2, 0]}><cylinderGeometry args={[0.18, 0.13, 0.4, 14]} /><Ol /></mesh>
        {[0, 1, 2, 3, 4].map((i) => <mesh key={i} material={m.plant} position={[Math.cos(i * 1.3) * 0.13, 0.62 + (i % 2) * 0.17, Math.sin(i * 1.3) * 0.1]}><sphereGeometry args={[0.17, 10, 8]} /><Ol w={0.008} /></mesh>)}
      </group>
      <TV st={st} />
    </group>
  )
}

function checker(a: string, b: string, n = 8) {
  const cv = document.createElement('canvas'); cv.width = cv.height = 256
  const c = cv.getContext('2d')!
  for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) { c.fillStyle = (i + j) % 2 ? a : b; c.fillRect(i * 256 / n, j * 256 / n, 256 / n, 256 / n) }
  const t = new THREE.CanvasTexture(cv); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.colorSpace = THREE.SRGBColorSpace
  return t
}
function textPlane(txt: string, bg: string, fg: string, w = 512, h = 128) {
  const cv = document.createElement('canvas'); cv.width = w; cv.height = h
  const c = cv.getContext('2d')!
  c.fillStyle = bg; c.fillRect(0, 0, w, h); c.fillStyle = fg; c.font = `bold ${h * 0.55}px sans-serif`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(txt, w / 2, h / 2 + 4)
  const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace
  return t
}

function Super() {
  const floor = useMemo(() => { const t = checker('#e9eef2', '#cfd8de'); t.repeat.set(6, 6); return t }, [])
  const sign = useMemo(() => textPlane('YOGURES', '#2f7dff', '#ffffff'), [])
  const m = useMemo(() => ({ shelf: toon('#d9dde3'), wall: toon('#fff3d6'), fridge: toon('#f4f7fb'), glass: toon('#bfe6ff', { transparent: true, opacity: 0.35 }), cart: toon('#8d99a6'), red: toon('#e8423f') }), [])
  const boxes = useMemo(() => {
    const cols = ['#ff4d6d', '#ffd23f', '#3ddc97', '#4da3ff', '#ff9f1c', '#b388ff', '#ffffff']
    const out: { p: [number, number, number]; s: [number, number, number]; c: THREE.Material }[] = []
    const mats = cols.map((c) => toon(c))
    let k = 3
    for (let lvl = 0; lvl < 4; lvl++) for (let i = 0; i < 16; i++) {
      k = (k * 7 + 3) % 97
      const h = 0.18 + (k % 5) * 0.03
      out.push({ p: [-1.9 + i * 0.25, 0.3 + lvl * 0.48 + h / 2, -1.05], s: [0.2, h, 0.22], c: mats[k % mats.length] })
    }
    return out
  }, [])
  return (
    <group>
      <Lights key1="#ffffff" amb={1.2} sky="#ffffff" ground="#b9c3cc" k={1.0} />
      <mesh rotation-x={-Math.PI / 2} receiveShadow><planeGeometry args={[9, 9]} /><meshToonMaterial map={floor} /></mesh>
      <mesh material={m.wall} position={[0, 1.8, -1.4]}><planeGeometry args={[9, 3.6]} /></mesh>
      {/* shelves */}
      {[0, 1, 2, 3].map((l) => <mesh key={l} material={m.shelf} position={[0, 0.28 + l * 0.48, -1.05]}><boxGeometry args={[4.2, 0.04, 0.4]} /><Ol w={0.006} /></mesh>)}
      {boxes.map((b, i) => <mesh key={i} material={b.c} position={b.p}><boxGeometry args={b.s} /><Ol w={0.005} /></mesh>)}
      {/* yogurt fridge on the left */}
      <group position={[-1.25, 0, 0.1]} rotation-y={Math.PI / 2}>
        <mesh material={m.fridge} position={[0, 0.9, -0.3]}><boxGeometry args={[1.6, 1.8, 0.5]} /><Ol /></mesh>
        {[0, 1, 2].map((l) => Array.from({ length: 9 }).map((_, i) => <group key={l + '-' + i} position={[-0.64 + i * 0.16, 0.42 + l * 0.42, -0.1]}><Yogurt lid={['#2f7dff', '#ff4d6d', '#3ddc97', '#ffd23f'][(i + l) % 4]} /></group>))}
      </group>
      {/* hanging sign */}
      <mesh position={[-0.6, 2.25, -0.5]}><planeGeometry args={[0.9, 0.22]} /><meshBasicMaterial map={sign} toneMapped={false} /></mesh>
      {/* cart in front of Dani */}
      <group position={[0.55, 0, 0.5]} rotation-y={-0.2}>
        <mesh material={m.cart} position={[0, 0.62, 0]}><boxGeometry args={[0.5, 0.32, 0.7]} /><meshToonMaterial color="#8d99a6" transparent opacity={0.5} /></mesh>
        {[[-0.25, -0.35], [0.25, -0.35], [-0.25, 0.35], [0.25, 0.35]].map(([x, z], i) => <mesh key={i} material={m.cart} position={[x, 0.4, z]}><cylinderGeometry args={[0.012, 0.012, 0.8, 6]} /></mesh>)}
        {[[-0.25, -0.35], [0.25, -0.35], [-0.25, 0.35], [0.25, 0.35]].map(([x, z], i) => <mesh key={'w' + i} material={m.red} position={[x, 0.04, z]} rotation-z={Math.PI / 2}><cylinderGeometry args={[0.04, 0.04, 0.03, 10]} /></mesh>)}
        <mesh material={m.red} position={[0, 0.85, -0.38]} rotation-z={Math.PI / 2}><cylinderGeometry args={[0.02, 0.02, 0.56, 8]} /><Ol w={0.005} /></mesh>
        {[[-0.1, 0.1, '#ffd23f'], [0.1, -0.1, '#ff4d6d'], [0.05, 0.15, '#3ddc97']].map(([x, z, c], i) => <mesh key={'p' + i} position={[x as number, 0.6, z as number]}><boxGeometry args={[0.16, 0.2, 0.12]} /><meshToonMaterial color={c as string} /></mesh>)}
      </group>
    </group>
  )
}

function Car({ st }: { st: Record<string, any> }) {
  const m = useMemo(() => ({ body: toon('#e8423f'), seat: toon('#2b2d3a'), dash: toon('#6b7087'), road: toon('#4b4f5c'), line: toon('#fff6c9'), lamp: toon('#2b2d3a'), bulb: toon('#fff6c9', { emissive: new THREE.Color('#fff2a8'), emissiveIntensity: 1 }), bld: ['#6c7a99', '#8a6c99', '#5d8a8a', '#99826c'].map((c) => toon(c)), palm: toon('#1a0b2e'), sun: toon('#ffe66d', { emissive: new THREE.Color('#ffb347'), emissiveIntensity: 0.6 }), glass: toon('#bfe6ff', { transparent: true, opacity: 0.15 }) }), [])
  const world = useRef<THREE.Group>(null!), miami = useRef<THREE.Group>(null!), city = useRef<THREE.Group>(null!)
  useFrame(() => {
    const sp = st.miami ? 38 : 22
    world.current.children.forEach((c, i) => { const base = (c.userData.z0 as number); c.position.z = -(((clock.t * sp + base) % 40)) - 1.5 })
    miami.current.visible = !!st.miami; city.current.visible = !st.miami
  })
  const items = useMemo(() => Array.from({ length: 16 }).map((_, i) => ({ z0: i * 2.5, side: i % 2 ? 1 : -1, k: i })), [])
  return (
    <group>
      <Lights key1="#fff2e0" amb={1.0} k={1.3} />
      <mesh material={m.road} rotation-x={-Math.PI / 2} position={[0, -0.25, -15]}><planeGeometry args={[8, 40]} /></mesh>
      <group ref={world}>
        {items.map((it) => (
          <group key={it.k} userData={{ z0: it.z0 }}>
            <mesh material={m.line} rotation-x={-Math.PI / 2} position={[0, -0.24, 0]}><planeGeometry args={[0.12, 1.0]} /></mesh>
            {it.k % 2 === 0 && <group position={[it.side * 2.3, -0.25, 0]}>
              <mesh material={m.lamp} position={[0, 1.4, 0]}><cylinderGeometry args={[0.04, 0.05, 2.8, 8]} /></mesh>
              <mesh material={m.bulb} position={[-it.side * 0.3, 2.8, 0]}><boxGeometry args={[0.6, 0.08, 0.16]} /></mesh>
            </group>}
          </group>
        ))}
      </group>
      <group ref={city}>
        {Array.from({ length: 12 }).map((_, i) => <mesh key={i} material={m.bld[i % 4]} position={[(i % 2 ? 1 : -1) * (4 + (i % 3)), 1.5 + (i % 4) * 0.6, -6 - i * 2.5]}><boxGeometry args={[2, 3 + (i % 4) * 1.2, 2]} /><Ol w={0.02} /></mesh>)}
      </group>
      <group ref={miami}>
        <mesh material={m.sun} position={[0, 2.2, -30]}><circleGeometry args={[3.2, 40]} /></mesh>
        {[-1, 1].flatMap((s) => [0, 1, 2, 3].map((i) => (
          <group key={s + '-' + i} position={[s * (3.2 + i * 0.6), -0.25, -6 - i * 5]}>
            <mesh material={m.palm} position={[0, 1.6, 0]} rotation-z={s * 0.12}><cylinderGeometry args={[0.07, 0.11, 3.2, 6]} /></mesh>
            {[0, 1, 2, 3, 4, 5].map((k) => <mesh key={k} material={m.palm} position={[s * 0.2 + Math.cos(k) * 0.5, 3.2, Math.sin(k) * 0.5]} rotation={[Math.sin(k) * 0.6, k, Math.cos(k) * 0.6]}><boxGeometry args={[1.3, 0.05, 0.25]} /></mesh>)}
          </group>
        )))}
      </group>
      {/* car body (open cabin, camera on the hood) */}
      <group>
        <RoundedBox args={[1.8, 0.4, 2.6]} radius={0.1} smoothness={3} position={[0, 0.25, 0.2]} material={m.body} castShadow><Ol w={0.015} /></RoundedBox>
        <RoundedBox args={[1.8, 0.2, 1.0]} radius={0.08} smoothness={3} position={[0, 0.5, 1.15]} material={m.body}><Ol w={0.012} /></RoundedBox>
        {[-1, 1].map((s) => <RoundedBox key={s} args={[0.12, 0.45, 1.5]} radius={0.04} smoothness={2} position={[s * 0.86, 0.62, -0.05]} material={m.body}><Ol w={0.01} /></RoundedBox>)}
        {/* pillars + roof */}
        {[-1, 1].map((s) => <mesh key={'a' + s} material={m.body} position={[s * 0.82, 1.2, 0.5]} rotation-x={-0.45}><boxGeometry args={[0.08, 0.9, 0.08]} /><Ol w={0.008} /></mesh>)}
        <RoundedBox args={[1.72, 0.08, 1.0]} radius={0.03} smoothness={2} position={[0, 1.6, -0.1]} material={m.body}><Ol w={0.01} /></RoundedBox>
        {/* seats */}
        {[-0.36, 0.36].map((x) => <group key={x} position={[x, 0, -0.1]}>
          <RoundedBox args={[0.55, 0.14, 0.5]} radius={0.04} smoothness={2} position={[0, 0.42, 0]} material={m.seat}><Ol w={0.006} /></RoundedBox>
          <RoundedBox args={[0.55, 0.75, 0.14]} radius={0.05} smoothness={2} position={[0, 0.82, -0.3]} rotation-x={-0.12} material={m.seat}><Ol w={0.006} /></RoundedBox>
        </group>)}
        {/* dashboard + wheel */}
        <RoundedBox args={[1.6, 0.16, 0.3]} radius={0.05} smoothness={2} position={[0, 0.66, 0.7]} material={m.dash}><Ol w={0.008} /></RoundedBox>
        <group position={[0.36, 0.84, 0.4]} rotation-x={-1.15}>
          <mesh material={m.dash}><torusGeometry args={[0.14, 0.022, 8, 24]} /><Ol w={0.005} /></mesh>
          <mesh material={m.dash} rotation-x={Math.PI / 2}><cylinderGeometry args={[0.035, 0.035, 0.05, 10]} /></mesh>
        </group>
      </group>
    </group>
  )
}

function Kitchen({ st }: { st: Record<string, any> }) {
  const tiles = useMemo(() => { const t = checker('#ffffff', '#cde9e4', 6); t.repeat.set(3, 1.5); return t }, [])
  const m = useMemo(() => ({ floor: toon('#e0a96d'), cab: toon('#3ddc97'), top: toon('#f4efe6'), fridge: toon('#f4f7fb'), inside: toon('#d6f1ff'), handle: toon('#8d99a6') }), [])
  const stack = useRef<THREE.Group>(null!)
  useFrame(() => { const n = Math.round(st.yogs ?? 0); stack.current.children.forEach((c, i) => { c.visible = i < n }) })
  const pos = useMemo(() => {
    const p: [number, number, number][] = []
    // pyramid of 37 yogurts on the counter
    let y = 0.92, row = 9, z = -0.75
    while (p.length < 37 && row > 0) { for (let i = 0; i < row && p.length < 37; i++) p.push([-0.1 + (i - row / 2) * 0.085 + 0.45, y, z]); y += 0.095; row-- }
    return p
  }, [])
  return (
    <group>
      <Lights key1="#fff6e0" amb={1.1} k={1.3} />
      <mesh material={m.floor} rotation-x={-Math.PI / 2} receiveShadow><planeGeometry args={[9, 9]} /></mesh>
      <mesh position={[0, 1.7, -1.1]}><planeGeometry args={[9, 3.4]} /><meshToonMaterial map={tiles} /></mesh>
      <RoundedBox args={[3.2, 0.86, 0.6]} radius={0.03} smoothness={2} position={[0.4, 0.43, -0.78]} material={m.cab} castShadow><Ol /></RoundedBox>
      <mesh material={m.top} position={[0.4, 0.88, -0.78]}><boxGeometry args={[3.3, 0.05, 0.66]} /><Ol w={0.006} /></mesh>
      {[-0.6, 0.2, 1.0, 1.8].map((x) => <mesh key={x} material={m.handle} position={[x, 0.65, -0.47]}><boxGeometry args={[0.2, 0.025, 0.02]} /></mesh>)}
      {/* open fridge on the left */}
      <group position={[-1.6, 0, -0.6]}>
        <RoundedBox args={[0.8, 1.9, 0.7]} radius={0.05} smoothness={2} position={[0, 0.95, 0]} material={m.fridge} castShadow><Ol /></RoundedBox>
        <mesh material={m.inside} position={[0, 0.95, 0.31]}><planeGeometry args={[0.66, 1.7]} /></mesh>
        <group position={[0.42, 0.95, 0.4]} rotation-y={-1.9}><RoundedBox args={[0.8, 1.9, 0.06]} radius={0.02} smoothness={2} position={[0.4, 0, 0]} material={m.fridge}><Ol /></RoundedBox></group>
      </group>
      <group ref={stack}>{pos.map((p, i) => <group key={i} position={p}><Yogurt /></group>)}</group>
    </group>
  )
}

function Bath({ st }: { st: Record<string, any> }) {
  const tiles = useMemo(() => { const t = checker('#7fb7d9', '#9fcbe6', 8); t.repeat.set(2, 1.2); return t }, [])
  const m = useMemo(() => ({ floor: toon('#e8e8ee'), wc: toon('#ffffff'), door: toon('#c98b5a'), light: toon('#ffe9a8', { emissive: new THREE.Color('#ffd36b'), emissiveIntensity: 1.2 }), sink: toon('#ffffff'), cab: toon('#8a5a34'), mon: toon('#16141c') }), [])
  const door = useRef<THREE.Group>(null!), doorLight = useRef<THREE.PointLight>(null!)
  const scr = useMemo(screenTexture, [])
  useFrame(() => { const k = st.door ?? 0; door.current.rotation.y = -k * 1.6; doorLight.current.intensity = k * 5; scr.draw('game', clock.t); scr.tex.needsUpdate = true })
  return (
    <group>
      <hemisphereLight args={['#6f86ff', '#1b1630', 0.55]} />
      <pointLight position={[0.9, 1.2, 0.2]} intensity={3.2} distance={4} color="#6fb6ff" />
      <pointLight ref={doorLight} position={[-1.3, 1.6, 0.4]} distance={4} color="#ffd36b" />
      <mesh material={m.floor} rotation-x={-Math.PI / 2}><planeGeometry args={[6, 6]} /></mesh>
      <mesh position={[0, 1.6, -0.95]}><planeGeometry args={[6, 3.2]} /><meshToonMaterial map={tiles} /></mesh>
      <mesh position={[-1.15, 1.6, 0]} rotation-y={Math.PI / 2}><planeGeometry args={[4, 3.2]} /><meshToonMaterial map={tiles} /></mesh>
      {/* doorway with warm light behind */}
      <mesh material={m.light} position={[-1.14, 1.0, 0.35]} rotation-y={Math.PI / 2}><planeGeometry args={[0.8, 2.0]} /></mesh>
      <group ref={door} position={[-1.12, 0, -0.05]}>
        <mesh material={m.door} position={[0, 1.0, 0.4]}><boxGeometry args={[0.05, 2.0, 0.8]} /><Ol /></mesh>
      </group>
      {/* toilet */}
      <group position={[0, 0, -0.55]}>
        <RoundedBox args={[0.42, 0.4, 0.55]} radius={0.12} smoothness={3} position={[0, 0.2, 0.08]} material={m.wc}><Ol /></RoundedBox>
        <RoundedBox args={[0.46, 0.06, 0.58]} radius={0.03} smoothness={2} position={[0, 0.42, 0.1]} material={m.wc}><Ol w={0.008} /></RoundedBox>
        <RoundedBox args={[0.5, 0.45, 0.2]} radius={0.05} smoothness={2} position={[0, 0.65, -0.26]} material={m.wc}><Ol /></RoundedBox>
      </group>
      {/* sink cabinet with the console's monitor */}
      <group position={[0.95, 0, -0.55]}>
        <RoundedBox args={[0.6, 0.8, 0.5]} radius={0.03} smoothness={2} position={[0, 0.4, 0]} material={m.cab}><Ol /></RoundedBox>
        <group position={[-0.05, 1.1, 0]} rotation-y={-0.7}>
          <mesh material={m.mon}><boxGeometry args={[0.6, 0.38, 0.04]} /><Ol w={0.008} /></mesh>
          <mesh position={[0, 0, 0.022]}><planeGeometry args={[0.55, 0.32]} /><meshBasicMaterial map={scr.tex} toneMapped={false} /></mesh>
        </group>
      </group>
      {/* towel */}
      <mesh position={[-0.6, 1.3, -0.92]}><boxGeometry args={[0.35, 0.55, 0.03]} /><meshToonMaterial color="#ff4fa3" /></mesh>
    </group>
  )
}

// ---------------------------------------------------------------- shots (head ≈ 1.21 sitting, 1.43 standing)
const HS = 1.2, HU = 1.42
const X = 0.34
const sofaShots = (z = -0.35): Record<string, Shot> => ({
  tv: { p: [1.45, 1.8, -1.0], l: [0.1, 0.9, 2.4], fov: 40, push: 0.35 },
  two: { p: [0, HS + 0.15, z + 2.9], l: [0, HS - 0.25, z], fov: 46, push: 0.3 },
  wide: { p: [1.9, 1.75, 1.7], l: [0, 0.85, -0.3], fov: 46, push: 0.2 },
  dani: { p: [0.05, HS + 0.08, z + 1.6], l: [X, HS - 0.1, z], fov: 42, push: 0.15 },
  lucia: { p: [-0.05, HS + 0.08, z + 1.6], l: [-X, HS - 0.12, z], fov: 42, push: 0.15 },
  rage: { p: [X - 0.1, HS + 0.4, z + 2.1], l: [X, HS + 0.18, z], fov: 44, push: 0.3 },
  daniTight: { p: [X - 0.05, HS + 0.06, z + 1.3], l: [X, HS - 0.02, z], fov: 46, push: 0.2 },
  luciaTight: { p: [-X + 0.08, HS + 0.04, z + 1.3], l: [-X, HS - 0.05, z], fov: 46, push: 0.2 },
})
const SH: Record<string, Record<string, Shot>> = {
  sofa: sofaShots(),
  super: {
    wide: { p: [0.5, 1.8, 2.9], l: [-0.05, 1.0, -0.2], fov: 46, push: 0.3 },
    two: { p: [0.05, HU + 0.1, 2.8], l: [0.05, HU - 0.3, 0], fov: 46, push: 0.25 },
    lucia: { p: [0.15, HU + 0.05, 1.5], l: [-0.35, HU - 0.12, 0], fov: 42, push: 0.15 },
    daniTight: { p: [0.4, HU + 0.06, 1.35], l: [0.5, HU - 0.02, 0], fov: 46, push: 0.2 },
    rage: { p: [0.35, HU + 0.4, 2.1], l: [0.5, HU + 0.18, 0], fov: 44, push: 0.3 },
    dani: { p: [0.3, HU + 0.1, 1.7], l: [0.5, HU - 0.1, 0], fov: 42, push: 0.2 },
  },
  car: {
    front: { p: [0, 1.4, 2.75], l: [0, 1.0, -0.1], fov: 46, push: 0.3 },
    dani: { p: [0.15, 1.3, 1.5], l: [0.36, HS - 0.1, -0.1], fov: 42, push: 0.15 },
    lucia: { p: [-0.1, 1.3, 1.5], l: [-0.36, HS - 0.12, -0.1], fov: 42, push: 0.15 },
    rage: { p: [0.28, HS + 0.12, 2.0], l: [0.36, HS + 0.14, -0.1], fov: 44, push: 0.3 },
    daniTight: { p: [0.33, 1.3, 1.2], l: [0.36, HS, -0.1], fov: 46, push: 0.15 },
  },
  kitchen: {
    wide: { p: [0.55, 1.65, 2.6], l: [0, 1.05, -0.4], fov: 46, push: 0.4 },
    daniTight: { p: [0.3, HU + 0.05, 1.3], l: [0.1, HU - 0.05, 0], fov: 46, push: 0.15 },
  },
  bath: {
    two: { p: [0.2, 1.4, 2.3], l: [-0.25, 0.95, -0.4], fov: 46, push: 0.3 },
    daniTight: { p: [0.08, HS + 0.06, 0.95], l: [0, HS - 0.04, -0.45], fov: 46, push: 0.15 },
    door: { p: [0.75, 1.5, 1.7], l: [-0.95, HU - 0.15, 0.3], fov: 40, push: 0.15 },
  },
  morning: sofaShots(),
}

// ---------------------------------------------------------------- beats
const pad = B.pad
const beats: ToonSpec['beats'] = {
  l01: { cut: 'tv', cut2: [2.6, 'dani'], d: sit({ eye: 1.2, sparkle: 1, smile: 0.6, tears: 0.25, brow: 0.6, ang: -0.5, open: 1 }, { ...pad, pitch: 0.05 }), l: sit(FX.calm, { yaw: 0.2, pitch: 0.3 }) },
  l02: { cut: 'daniTight', zoom: 0.8, d: sit(FX.cry, { ...pad, shake: 0.6, pitch: -0.1 }), shake: 0.3 },
  l03: { cut: 'lucia', l: sit(FX.sweet, { yaw: 0.55, tilt: -0.15, lean: 0.05, roll: -0.08 }), d: sit(FX.cryOpen, { ...pad }) },
  l04: { cut: 'daniTight', zoom: 0.7, lines: 1, flash: '#ff3b30', shake: 0.6, d: sit(FX.angry, { ...pad, head: 1.15, shake: 0.5, yaw: -0.3 }), dMid: sit({ ...FX.scream, rage: 0.4 }, { ...pad, head: 1.25, shake: 0.8, yaw: -0.2 }) },
  l05: { cut: 'two', d: sit(FX.fake, { lSh: [2.7, 0.4], lEl: -0.3, rSh: [1.0, -0.3], rEl: -1.1, head: 1.05 }), l: sit(FX.joy, { yaw: 0.4, ...B.armsUp }) },
  l06: { cut: 'wide', d: stand(FX.dead, { lean: 0.3, pitch: 0.25, squash: -0.1, lSh: [0.05, 0.05], lEl: 0, rSh: [0.05, 0.05], rEl: 0 }), l: stand(FX.doubt, { ...B.hold2, yaw: -0.15, pitch: 0.25 }) },
  l07: { cut: 'lucia', l: stand({ ...FX.doubt, lx: 0.7 }, { ...B.hold2, lSh: [1.6, 0.2], lEl: -0.6, yaw: 0.55, tilt: 0.2 }), lMid: stand({ ...FX.sweet, lx: 0.7 }, { ...B.hold2, yaw: 0.55, tilt: -0.2 }) },
  l08: { cut: 'rage', zoom: 0.65, lines: 1, flash: '#ffd400', shake: 0.9, d: stand({ ...FX.scream, rage: 0.6 }, { ...B.fists, head: 1.3, shake: 0.9, squash: 0.08 }) },
  l09: { cut: 'two', d: stand(FX.fake, { ...B.point, yaw: -0.4, head: 1.05 }), l: stand(FX.hearts, { ...B.hold2, yaw: 0.5 }) },
  l10: { cut: 'front', flash: '#ff4fa3', d: sit({ ...FX.smug, lx: 0, ang: 0.5 }, { ...B.wheel, lean: 0.12, shake: 0.2 }), l: sit(FX.calm, { yaw: 0.1, pitch: 0.2 }), shake: 0.35 },
  l11: { cut: 'lucia', l: sit(FX.suspicious, { yaw: 0.6, tilt: 0.12, ...B.hips }), d: sit(FX.focus, { ...B.wheel }) },
  l12: { cut: 'dani', d: sit({ open: 1, eye: 1.2, smile: 0.5, brow: 0.7, ang: -0.5, ly: -0.7, lx: 0.4, sweat: 1 }, { ...B.wheel, yaw: -0.25 }) },
  l13: { cut: 'rage', zoom: 0.6, lines: 1, flash: '#ff2d2d', shake: 1, d: sit(FX.rage, { ...B.wheel, head: 1.4, shake: 1 }) },
  l14: { cut: 'wide', d: stand({ open: 0.45, smile: 0.2, ang: 0.35, bags: 0.7, vein: 0.5, lx: -0.6 }, { ...B.hold, yaw: -0.4, lean: 0.05 }), dMid: stand({ open: 0.5, smile: 0.5, teeth: 1, ang: 0.4, bags: 0.7, vein: 0.8 }, { ...B.hold, yaw: 0.1 }) },
  l15: { cut: 'dani', d: sit(FX.joy, { ...pad, shake: 0.4, head: 1.08 }), l: sit(FX.calm, { yaw: 0.2 }) },
  l16: { cut: 'lucia', l: sit({ ...FX.sweet, blush: 1 }, { yaw: 0.5, roll: -0.12, lean: 0.06, tilt: -0.25, lSh: [1.0, -0.6], lEl: -1.2 }), d: sit({ ...FX.joy, mouth: 0.3 }, { ...pad }), dAt: 0, lAt: 0 },
  l17: { cut: 'rage', zoom: 0.6, lines: 1, flash: '#ff0000', shake: 1, d: sit({ ...FX.angry, rage: 0.8 }, { ...pad, head: 1.25, shake: 0.8 }), dMid: sit(FX.rage, { ...pad, head: 1.45, shake: 1.2, squash: 0.06 }) },
  l18: { cut: 'two', d: sit({ ...FX.fake, tears: 0.6, vein: 0 }, { head: 1.0, yaw: -0.3 }), l: sit(FX.hearts, { yaw: 0.45, roll: -0.12, tilt: -0.2 }) },
  l19: { cut: 'two', d: sit(FX.sneaky, { ...pad, lean: 0.12, yaw: 0.35, pitch: 0.1 }) },
  l20: { cut: 'door', l: stand(FX.sleepy, { yaw: 0.2, tilt: 0.1, ...B.hips }) },
  l21: { cut: 'daniTight', zoom: 0.7, flash: '#ffffff', d: sit(FX.nervous, { ...pad, yaw: -0.5, head: 1.15, shake: 0.6 }), shake: 0.4 },
  l22: { cut: 'door', l: stand({ ...FX.suspicious, lx: -0.3 }, { ...B.point, yaw: 0.2 }), lMid: stand({ ...FX.joy, sparkle: 1, eye: 1.2 }, { ...B.armsUp, yaw: 0.2 }) },
  l23: { cut: 'two', d: sit({ ...FX.dead, open: 0.22 }, { lean: 0.15, roll: 0.0, tilt: -0.35, pitch: 0.2, squash: -0.08, lSh: [0.1, 0.05], lEl: 0, rSh: [0.1, 0.05], rEl: 0 }), l: sit(FX.gamer, { ...pad, lean: 0.12, shake: 0.25 }) },
  l24: { cut: 'daniTight', d: sit(FX.camera, { tilt: -0.1 }), l: sit(FX.gamer, { ...pad, lean: 0.12, shake: 0.25 }) },
}

// ---------------------------------------------------------------- scenes
const scenes: ToonSpec['scenes'] = [
  { id: 'sofa', from: 'l01', bg: '#1b1230', Set: ({ st }) => <SofaRoom st={st} />, dani: { p: [X, 0, -0.35], ry: 0 }, lucia: { p: [-X, 0, -0.35], ry: 0 }, shots: SH.sofa },
  { id: 'super', from: 'l06', bg: '#fff3d6', Set: () => <Super />, dani: { p: [0.5, 0, 0], ry: -0.2 }, lucia: { p: [-0.35, 0, 0], ry: -0.45 }, shots: SH.super },
  { id: 'car', from: 'l10', bg: '#8fc6ff', Set: ({ st }) => <Car st={st} />, dani: { p: [0.36, 0.02, -0.1], ry: 0 }, lucia: { p: [-0.36, 0.02, -0.1], ry: 0 }, shots: SH.car },
  { id: 'kitchen', from: 'l14', bg: '#fff3d6', Set: ({ st }) => <Kitchen st={st} />, dani: { p: [0.1, 0, 0], ry: -0.3 }, shots: SH.kitchen },
  { id: 'sofa2', from: 'l15', bg: '#1b1230', Set: ({ st }) => <SofaRoom st={st} />, dani: { p: [X, 0, -0.35], ry: 0 }, lucia: { p: [-X, 0, -0.35], ry: 0 }, shots: SH.sofa },
  { id: 'bath', from: 'l19', bg: '#10142a', Set: ({ st }) => <Bath st={st} />, dani: { p: [0, 0.0, -0.45], ry: 0 }, lucia: { p: [-0.95, 0, 0.3], ry: Math.PI / 2 }, shots: SH.bath },
  { id: 'morning', from: 'l23', bg: '#ffe0b8', Set: ({ st }) => <SofaRoom st={st} morning />, dani: { p: [X, 0, -0.35], ry: 0 }, lucia: { p: [-X, 0, -0.35], ry: 0 }, shots: SH.morning },
]

const spec: ToonSpec = {
  id: 'pareja11',
  script: SCRIPT,
  gap: { l03: 0.3, l05: 0.2, l06: 1.0, l07: 0.3, l09: 0.2, l10: 1.0, l11: 0.3, l13: 0.1, l14: 1.0, l15: 1.0, l16: 0.3, l17: 0.2, l18: 0.3, l19: 1.0, l20: 0.4, l21: 0.1, l22: 0.3, l23: 1.0, l24: 0.6 },
  scenes,
  beats,
  d0: sit({ eye: 1.2, sparkle: 1, smile: 0.6, open: 1 }, { ...pad }),
  l0: sit(FX.calm, { yaw: 0.2, pitch: 0.3 }),
  cut0: 'tv',
  music: 'comedy',
  hands: (st) => ({
    dani: <Show show={() => ['sofa', 'sofa2', 'bath'].includes(st.scene)}><Pad /></Show>,
    danil: <Show show={() => st.scene === 'kitchen'}><group position={[0, -0.04, 0]}><Yogurt /></group></Show>,
    lucia: <Show show={() => st.scene === 'super' || st.scene === 'morning'}><Show show={() => st.scene === 'super'}><group position={[0, -0.04, 0]}><Yogurt lid="#2f7dff" /></group></Show><Show show={() => st.scene === 'morning'}><Pad /></Show></Show>,
    lucial: <Show show={() => st.scene === 'super'}><group position={[0, -0.04, 0]}><Yogurt lid="#ffd23f" /></group></Show>,
    daniHead: <group><Show show={() => !!st.miami}><Shades /></Show><Show show={() => st.scene === 'bath'}><Headphones color="#4da3ff" /></Show></group>,
    luciaHead: <Show show={() => st.scene === 'morning'}><Headphones /></Show>,
  }),
  frame: (t, a, l, st, f) => {
    st.miami = t >= a('l10') - 0.1 && t < a('l11') - 0.1
    st.bg = st.miami ? '#ff8fb8' : undefined
    st.tv = t >= a('l18') && t < a('l19') ? 'film' : st.scene === 'morning' ? 'game' : 'start'
    st.yogs = 37 * seg(t, a('l14'), a('l14') + l('l14').dur * 0.85)
    st.door = seg(t, a('l20') - 0.4, a('l20') + 0.1)
    // Dani in the kitchen is the one holding a yogurt with the left hand
    if (st.scene === 'kitchen') { f.dani.lSh = [1.2, 0.1]; f.dani.lEl = -1.0 }
    // morning: Dani's head drops onto her shoulder
    if (st.scene === 'morning' && t < a('l24')) f.dani.tilt = -0.35 + 0.05 * Math.sin(t * 1.3)
  },
  sfx: (l) => [
    { type: 'chime', at: l('l01').at + 0.2, g: 0.35 },
    { type: 'ding', at: l('l03').at + 0.1, g: 0.3 },
    { type: 'scratch', at: l('l04').at, g: 0.45 },
    { type: 'hit', at: l('l04').at + 0.05, g: 0.4 },
    { type: 'boing', at: l('l05').at + 0.1, g: 0.4 },
    { type: 'whoosh', at: l('l06').at - 0.6, g: 0.5 },
    { type: 'tick', at: l('l06').at + 0.8, g: 0.35 }, { type: 'tick', at: l('l06').at + 1.6, g: 0.35 },
    { type: 'hit', at: l('l08').at, g: 0.5 },
    { type: 'boing', at: l('l09').at + 0.2, g: 0.3 },
    { type: 'whoosh', at: l('l10').at - 0.6, g: 0.5 },
    { type: 'riser', at: l('l10').at, g: 0.3 },
    { type: 'scratch', at: l('l11').at, g: 0.45 },
    { type: 'hit', at: l('l13').at, g: 0.55 },
    { type: 'whoosh', at: l('l14').at - 0.6, g: 0.5 },
    ...Array.from({ length: 10 }).map((_, i) => ({ type: 'pop', at: l('l14').at + 0.2 + i * l('l14').dur * 0.085, g: 0.25 })),
    { type: 'whoosh', at: l('l15').at - 0.6, g: 0.5 },
    { type: 'chime', at: l('l15').at + 0.3, g: 0.35 },
    { type: 'ding', at: l('l16').at, g: 0.3 },
    { type: 'growl', at: l('l17').at, g: 0.5 }, { type: 'hit', at: l('l17').at, g: 0.5 },
    { type: 'whoosh', at: l('l19').at - 0.6, g: 0.5 },
    { type: 'door', at: l('l20').at - 0.45, g: 0.6 },
    { type: 'buzz', at: l('l21').at - 0.05, g: 0.4 },
    { type: 'boing', at: l('l22').at + l('l22').dur * 0.5, g: 0.4 },
    { type: 'whoosh', at: l('l23').at - 0.6, g: 0.5 },
  ],
  overlays: (l, dur) => [
    box(l('l01').at + 0.3, l('l03').at - 0.1, 250, 56, 'ESPERANDO EL GTA 6\\N{\\fs110}13 AÑOS', 8),
    box(l('l04').at + 0.2, l('l05').at - 0.1, 250, 54, '«UN MOMENTITO»\\N{\\fs50}DURACIÓN REAL: 2 H 14 MIN', 8),
    box(l('l06').at, l('l08').at - 0.1, 250, 56, 'TIEMPO EN EL SÚPER\\N{\\fs110}2:14:07', 8),
    box(l('l10').at + 0.2, l('l11').at - 0.1, 250, 56, 'VELOCIDAD MENTAL\\N{\\fs110}240 KM/H', 8),
    box(l('l14').at + 0.2, l('l15').at - 0.2, 250, 56, 'YOGURES GRIEGOS\\N{\\fs110}37', 8),
    box(l('l17').at + 0.2, l('l18').at - 0.1, 250, 56, 'PACIENCIA\\N{\\fs110}0 %', 8),
    box(l('l19').at, l('l20').at - 0.5, 250, 90, '03:00', 8),
    box(l('l23').at, l('l24').at - 0.1, 250, 56, '09:00\\N{\\fs50}ELLA: MISIÓN 40 · TÚ: 0', 8),
    box(l('l24').at + l('l24').dur * 0.6, dur, 250, 70, 'COSAS DE PAREJA\\N{\\fs56}SÍGUENOS PARA MÁS', 8),
  ],
}

export function Pareja11() { return <ToonEpisode spec={spec} /> }
