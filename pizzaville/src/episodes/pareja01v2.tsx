// COSAS DE PAREJA · EP. 1 (v2) — «Ha soñado que le ponías los cuernos».
// Estilo low-poly, de noche en la cama, narrador cansado que habla en «tú».
// Todo cuelga de los tiempos reales de cada frase de voz.
import { useMemo, useRef } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { RoundedBox } from '@react-three/drei'
import * as THREE from 'three'
import { clock, ease, seg } from '../engine/clock'
import { useLines, type Line } from '../engine/voice'
import { LowPolyChar, P0, mixPose, type LPLook, type LPPose } from '../scene/LowPoly'

export const DANI: LPLook = { skin: '#e9b48e', hair: '#1e1a1c', top: '#2f8f83', hairStyle: 'dani' }
export const LUCIA: LPLook = { skin: '#f1c3a0', hair: '#a4482a', top: '#f08aa6', hairStyle: 'lucia' }

export const EP = {
  id: 'pareja01v2',
  script: [
    { id: 'l01', at: 0.4, text: 'Son las tres de la mañana. Por fin te estás quedando dormido.' },
    { id: 'l02', at: 5, text: 'Y entonces notas que te está mirando.' },
    { id: 'l03', at: 8, text: '«¿Estás despierto?»' },
    { id: 'l04', at: 10, text: 'No. Evidentemente no.' },
    { id: 'l05', at: 12, text: '«Es que he soñado una cosa... y estoy muy enfadada contigo.»' },
    { id: 'l06', at: 16, text: 'Contigo. Que estabas aquí. Durmiendo.' },
    { id: 'l07', at: 19, text: '«En el sueño te ibas a cenar con otra. Y ni me avisabas.»' },
    { id: 'l08', at: 23, text: 'Le intentas explicar que eso no ha pasado. Que era un sueño.' },
    { id: 'l09', at: 27, text: '«Ya, pero lo habrías hecho. Se te veía muy feliz.»' },
    { id: 'l10', at: 31, text: 'Veinte minutos después, estás pidiendo perdón por algo que no has hecho.' },
    { id: 'l11', at: 36, text: 'Ella ya se ha dormido. Tú no vas a dormir en tu vida.' },
    { id: 'l12', at: 40, text: 'Etiqueta a la que se enfada contigo por sus sueños.' },
  ],
}
// pauses before a line (deadpan timing)
const GAP: Record<string, number> = { l02: 0.3, l03: 0.9, l04: 0.7, l05: 0.3, l06: 0.5, l07: 0.4, l08: 0.5, l09: 0.4, l10: 1.0, l11: 0.6, l12: 0.9 }

const VOW = /[aeiouáéíóúü]/gi
function lip(l: Line | undefined, t: number) {
  if (!l) return 0
  const lt = t - l.at
  if (lt < 0 || lt > l.dur) return 0
  for (const w of l.words) if (lt >= w.t && lt <= w.t + w.d) {
    const syl = Math.max(1, (w.w.match(VOW) ?? []).length)
    return 0.15 + 0.85 * Math.pow(Math.abs(Math.sin(((lt - w.t) / w.d) * syl * Math.PI)), 0.7)
  }
  return 0
}
const endOf = (l: Line) => l.at + l.dur

// ---------------- named poses
const pose = (o: Partial<LPPose>): LPPose => ({ ...P0, ...o })
const D = {
  sleep: pose({ lids: 1, roll: -0.14, pitch: 0.12, lean: 0.02 }),
  stir: pose({ lids: 1, roll: -0.1, pitch: 0.08, brows: 0.35, browTilt: -0.3 }),
  tired: pose({ lids: 0.55, yaw: 0.05, pitch: 0.02, brows: -0.1 }),
  toHer: pose({ lids: 0.45, yaw: -0.55, brows: 0.25 }),
  shocked: pose({ lids: 0, yaw: -0.5, brows: 0.9, browTilt: -0.2, mouth: 0.25 }),
  explain: pose({ lids: 0.2, yaw: -0.45, brows: 0.6, browTilt: -0.5, lSh: [0.95, 0.35], lEl: -1.0, rSh: [0.95, -0.35], rEl: -1.0 }),
  frozen: pose({ lids: 0.1, yaw: -0.4, brows: 0.5, browTilt: -0.8, lSh: [0.8, 0.3], lEl: -1.1, rSh: [0.8, -0.3], rEl: -1.1 }),
  sorry: pose({ lids: 0.35, yaw: -0.35, pitch: 0.15, brows: 0.6, browTilt: -1, lSh: [0.9, -0.12], lEl: -1.2, rSh: [0.9, 0.12], rEl: -1.2 }),
  stare: pose({ lids: 0, yaw: 0, brows: 0, browTilt: 0 }),
}
const L_ = {
  stare: pose({ yaw: 0.6, brows: -0.1, browTilt: 0.2, lean: 0.05 }),
  closer: pose({ yaw: 0.65, lean: 0.12, side: 0.07, roll: 0.06, brows: 0.1 }),
  angry: pose({ yaw: 0.5, brows: -0.3, browTilt: 1, lean: 0.1, side: 0.04, lSh: [0.35, 0.25], lEl: -0.7, rSh: [0.35, -0.25], rEl: -0.7 }),
  point: pose({ yaw: 0.5, brows: -0.2, browTilt: 0.9, rSh: [1.1, -0.1], rEl: -0.5, lSh: [0.3, 0.1], lEl: -0.9 }),
  smug: pose({ yaw: 0.35, brows: 0.15, browTilt: 0.5, smile: 0.6, lids: 0.3, rSh: [0.6, -0.1], rEl: -1.2 }),
  offended: pose({ yaw: -0.35, pitch: -0.12, brows: 0.2, browTilt: 0.6, lids: 0.35, smile: -0.3 }),
  asleep: pose({ lids: 1, sink: 0.16, roll: 0.22, yaw: 0.2, pitch: 0.05, smile: 0.5, side: 0.03 }),
}

/** keyed pose track: [time, pose][] with 0.3 s blends */
function track(keys: [number, LPPose][], t: number, blend = 0.3): LPPose {
  let i = 0
  while (i + 1 < keys.length && t >= keys[i + 1][0]) i++
  const cur = keys[i][1]
  const prev = i > 0 ? keys[i - 1][1] : cur
  const k = i > 0 ? ease.inOut(seg(t, keys[i][0], keys[i][0] + blend)) : 1
  return mixPose(prev, cur, k)
}

// ---------------- props
function Clock({ text }: { text: () => string }) {
  const { tex, cv } = useMemo(() => {
    const cv = document.createElement('canvas'); cv.width = 256; cv.height = 96
    const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace
    return { tex, cv }
  }, [])
  const last = useRef('')
  useFrame(() => {
    const s = text()
    if (s === last.current) return
    last.current = s
    const c = cv.getContext('2d')!
    c.fillStyle = '#0c0c10'; c.fillRect(0, 0, 256, 96)
    c.fillStyle = '#ff3b30'; c.font = 'bold 74px monospace'; c.textAlign = 'center'; c.textBaseline = 'middle'
    c.fillText(s, 128, 52)
    tex.needsUpdate = true
  })
  return (
    <group>
      <RoundedBox args={[0.3, 0.13, 0.12]} radius={0.02} material={new THREE.MeshStandardMaterial({ color: '#26242c', roughness: 0.5 })} />
      <mesh position={[0, 0, 0.061]}><planeGeometry args={[0.26, 0.098]} /><meshBasicMaterial map={tex} toneMapped={false} /></mesh>
    </group>
  )
}

function Bedroom({ lamp }: { lamp: () => number }) {
  const lampLight = useRef<THREE.PointLight>(null!)
  const shade = useRef<THREE.MeshStandardMaterial>(null!)
  const fill = useRef<THREE.HemisphereLight>(null!)
  useFrame(() => {
    const k = lamp()
    lampLight.current.intensity = 4.2 * k
    shade.current.emissiveIntensity = 0.15 + 1.2 * k
    fill.current.intensity = 0.9 + 0.2 * k
  })
  const fm = (c: string, r = 0.9) => new THREE.MeshStandardMaterial({ color: c, roughness: r, flatShading: true })
  const wall = fm('#2b3a6e'), wood = fm('#8a5a34', 0.7), sheet = fm('#e9e4f2'), duvet = fm('#3d5fb0'), pillow = fm('#f4f1fa')
  return (
    <group>
      <hemisphereLight ref={fill} args={['#d3d9ff', '#3a2c40', 0.9]} />
      {/* moonlight from the window, cold */}
      <directionalLight position={[2.5, 3.5, 2.5]} intensity={1.5} color="#d2d9ff" castShadow shadow-mapSize={[2048, 2048]} shadow-bias={-0.0005}
        shadow-camera-left={-3} shadow-camera-right={3} shadow-camera-top={3} shadow-camera-bottom={-3} />
      <pointLight position={[0, 1.9, 2.4]} intensity={2.2} distance={6} color="#ffe6d2" />
      <pointLight ref={lampLight} position={[-1.15, 1.25, -0.25]} distance={4.5} decay={1.6} color="#ffb766" castShadow />
      {/* walls & floor */}
      <mesh position={[0, 1.6, -0.95]} material={wall} receiveShadow><planeGeometry args={[8, 3.4]} /></mesh>
      <mesh rotation-x={-Math.PI / 2} material={fm('#5b3f2e', 0.8)} receiveShadow><planeGeometry args={[8, 8]} /></mesh>
      {/* window with moon */}
      <group position={[1.35, 2.15, -0.93]}>
        <mesh material={fm('#cfd6ee')}><boxGeometry args={[0.9, 0.9, 0.04]} /></mesh>
        <mesh position={[0, 0, 0.025]}><planeGeometry args={[0.8, 0.8]} /><meshBasicMaterial color="#0e1638" /></mesh>
        <mesh position={[0.18, 0.18, 0.03]}><circleGeometry args={[0.09, 14]} /><meshBasicMaterial color="#f6f1d0" /></mesh>
        {[[-0.25, -0.1], [0.05, -0.28], [-0.1, 0.25], [0.28, -0.05], [-0.3, 0.3]].map(([x, y], i) => (
          <mesh key={i} position={[x, y, 0.03]}><circleGeometry args={[0.01, 5]} /><meshBasicMaterial color="#ffffff" /></mesh>
        ))}
        <mesh position={[0, 0, 0.04]} material={fm('#cfd6ee')}><boxGeometry args={[0.03, 0.8, 0.02]} /></mesh>
        <mesh position={[0, 0, 0.04]} material={fm('#cfd6ee')}><boxGeometry args={[0.8, 0.03, 0.02]} /></mesh>
      </group>
      {/* headboard */}
      <mesh position={[0, 0.95, -0.82]} material={wood} castShadow receiveShadow><boxGeometry args={[2.0, 1.1, 0.1]} /></mesh>
      <mesh position={[0, 1.52, -0.82]} material={fm('#734828', 0.7)}><boxGeometry args={[2.08, 0.08, 0.14]} /></mesh>
      {/* bed */}
      <mesh position={[0, 0.27, 0.3]} material={wood} castShadow receiveShadow><boxGeometry args={[1.95, 0.32, 2.4]} /></mesh>
      <mesh position={[0, 0.5, 0.3]} material={sheet} receiveShadow><boxGeometry args={[1.88, 0.16, 2.34]} /></mesh>
      {[-0.42, 0.42].map((x) => (
        <RoundedBox key={x} args={[0.72, 0.22, 0.42]} radius={0.08} smoothness={2} position={[x, 0.72, -0.6]} rotation={[-0.5, 0, 0]} material={pillow} castShadow receiveShadow />
      ))}
      {/* duvet up to the waist, with folds */}
      <RoundedBox args={[1.96, 0.32, 1.75]} radius={0.12} smoothness={2} position={[0, 0.66, 0.6]} material={duvet} castShadow receiveShadow />
      <RoundedBox args={[1.98, 0.14, 0.36]} radius={0.06} smoothness={2} position={[0, 0.83, -0.08]} material={fm('#e9e4f2')} castShadow />
      {[-0.4, 0.4].map((x) => <RoundedBox key={x} args={[0.62, 0.1, 0.7]} radius={0.05} smoothness={2} position={[x, 0.84, 0.5]} material={duvet} />)}
      {/* nightstands */}
      {[-1.25, 1.25].map((x) => (
        <group key={x} position={[x, 0, -0.5]}>
          <mesh position={[0, 0.3, 0]} material={wood} castShadow receiveShadow><boxGeometry args={[0.45, 0.6, 0.42]} /></mesh>
          <mesh position={[0, 0.42, 0.212]} material={fm('#734828')}><boxGeometry args={[0.36, 0.14, 0.01]} /></mesh>
        </group>
      ))}
      {/* her lamp (left) */}
      <group position={[-1.25, 0.6, -0.55]}>
        <mesh position={[0, 0.12, 0]} material={fm('#e7d9c3')}><cylinderGeometry args={[0.05, 0.08, 0.24, 7]} /></mesh>
        <mesh position={[0, 0.36, 0]}><cylinderGeometry args={[0.1, 0.17, 0.22, 8, 1, true]} /><meshStandardMaterial ref={shade} color="#fbe9c8" emissive="#ffb766" side={THREE.DoubleSide} flatShading /></mesh>
      </group>
      {/* phone + glass on his side */}
      <mesh position={[1.12, 0.61, -0.4]} rotation={[-Math.PI / 2, 0, 0.3]} material={fm('#1a1a22', 0.4)}><boxGeometry args={[0.08, 0.16, 0.012]} /></mesh>
      <mesh position={[1.4, 0.66, -0.55]} material={new THREE.MeshStandardMaterial({ color: '#cfe8ff', roughness: 0.1, transparent: true, opacity: 0.55 })}><cylinderGeometry args={[0.04, 0.035, 0.12, 9]} /></mesh>
    </group>
  )
}

// ---------------- shots
type Shot = { p: [number, number, number]; l: [number, number, number]; fov: number; push?: number }
const HY = 1.58
const SH: Record<string, Shot> = {
  two: { p: [0, 1.78, 2.35], l: [0, 1.45, -0.3], fov: 44, push: 0.2 },
  lucia: { p: [-0.1, 1.7, 1.55], l: [-0.42, HY - 0.08, -0.3], fov: 38, push: 0.12 },
  dani: { p: [0.1, 1.7, 1.55], l: [0.42, HY - 0.08, -0.3], fov: 38, push: 0.12 },
  daniTight: { p: [0.36, 1.66, 1.2], l: [0.42, HY - 0.02, -0.3], fov: 36, push: 0.08 },
  clock: { p: [1.05, 0.95, 0.35], l: [1.2, 0.68, -0.4], fov: 34, push: 0.06 },
}

export function Pareja01v2() {
  const { camera, scene } = useThree()
  const lines = useMemo(() => useLines(EP.id, EP.script), [])
  const L = (id: string) => lines.find((l) => l.id === id)!
  const P = useMemo(() => new THREE.Vector3(), [])
  const LK = useMemo(() => new THREE.Vector3(), [])
  const poses = useRef({ dani: P0, lucia: P0 })
  const state = useRef({ lamp: 0, clock: '03:00' })
  useMemo(() => { scene.background = new THREE.Color('#0d1022'); scene.fog = null }, [])

  const layout = () => {
    for (let i = 0; i < lines.length; i++) lines[i].at = i === 0 ? 0.6 : lines[i - 1].at + lines[i - 1].dur + 0.35 + (GAP[lines[i].id] ?? 0)
  }
  const duration = () => { layout(); return Math.ceil((endOf(lines[lines.length - 1]) + 2.8) * 10) / 10 }

  useMemo(() => {
    const pv = (window as any).__pv
    if (!pv) return
    pv.info = () => {
      layout()
      const l = L
      const sfx = [
        { type: 'tick', at: l('l03').at - 0.45, g: 0.6 }, // lamp click on
        { type: 'whoosh', at: l('l10').at - 0.5, g: 0.35 },
        { type: 'tick', at: l('l11').at - 0.2, g: 0.6 }, // lamp click off
        { type: 'hit', at: l('l07').at + l('l07').dur * 0.45, g: 0.35 },
      ]
      return { id: EP.id, duration: duration(), music: 'night', subStyle: 'box', overlays: overlays(lines, duration()), lines: lines.map((x) => ({ id: x.id, at: x.at, dur: x.dur, text: x.text, words: x.words, hasAudio: x.hasAudio })), sfx }
    }
  }, [])

  useFrame(() => {
    layout()
    const t = clock.t, l = L, s = state.current
    const a = (id: string) => l(id).at
    // ---------------- poses
    const dani = track([
      [0, D.sleep], [a('l02') + 0.6, D.stir], [a('l03') + 0.3, D.sleep], [a('l04') - 0.1, D.tired], [a('l05') + 0.2, D.toHer],
      [a('l06') - 0.1, D.tired], [a('l07') + l('l07').dur * 0.45, D.shocked], [a('l08'), D.explain], [a('l09') + 0.4, D.frozen],
      [a('l10') - 0.2, D.sorry], [a('l11') + 0.5, D.stare],
    ], t)
    // his explaining has silent mouth flaps
    if (t > a('l08') && t < endOf(l('l08'))) dani.mouth = 0.15 + 0.5 * Math.abs(Math.sin(t * 9.3)) * (Math.sin(t * 2.1) > -0.4 ? 1 : 0)
    if (t > a('l10') + 0.3 && t < endOf(l('l10'))) dani.mouth = 0.12 + 0.35 * Math.abs(Math.sin(t * 8.1))
    // pleading bob
    if (t > a('l10') && t < a('l11')) { dani.pitch += Math.sin(t * 5) * 0.04; dani.lSh = [dani.lSh[0] + Math.sin(t * 5) * 0.05, dani.lSh[1]] }
    const lucia = track([
      [0, L_.stare], [a('l02'), L_.closer], [a('l05'), L_.angry], [a('l07'), L_.point], [a('l08') + 0.3, L_.angry],
      [a('l09'), L_.smug], [a('l10') - 0.2, L_.offended], [a('l11') - 0.3, L_.asleep],
    ], t, 0.4)
    lucia.mouth = Math.max(lip(l('l03'), t), lip(l('l05'), t), lip(l('l07'), t), lip(l('l09'), t))
    // blinking
    const blink = (off: number) => ((t + off) % 4.1) < 0.12 ? 1 : 0
    lucia.lids = Math.max(lucia.lids, blink(1.3))
    if (dani.lids < 0.6) dani.lids = Math.max(dani.lids, blink(0.2))
    // final stare: no blinking at all, eyes wide
    if (t > a('l11') + 0.5) dani.lids = 0
    poses.current.dani = dani; poses.current.lucia = lucia
    s.lamp = t < a('l03') - 0.45 ? 0 : t < a('l11') - 0.2 ? 1 : 0
    s.clock = t < a('l10') - 0.5 ? '03:00' : t < a('l11') - 0.2 ? '03:20' : '03:47'

    // ---------------- camera
    const cuts: [number, string][] = [
      [0, 'two'], [a('l02') - 0.15, 'lucia'], [a('l03') - 0.5, 'two'], [a('l04') - 0.1, 'daniTight'], [a('l05') - 0.1, 'lucia'],
      [a('l06') - 0.1, 'daniTight'], [a('l07') - 0.1, 'lucia'], [a('l07') + l('l07').dur * 0.42, 'dani'], [a('l08') - 0.1, 'two'],
      [a('l09') - 0.1, 'lucia'], [a('l09') + l('l09').dur * 0.7, 'dani'], [a('l10') - 0.6, 'clock'], [a('l10') + 1.0, 'two'],
      [a('l11') - 0.25, 'two'], [a('l11') + l('l11').dur * 0.45, 'daniTight'], [a('l12') - 0.1, 'two'],
    ]
    let ci = 0
    while (ci + 1 < cuts.length && t >= cuts[ci + 1][0]) ci++
    const [c0, name] = cuts[ci]
    const c1 = ci + 1 < cuts.length ? cuts[ci + 1][0] : c0 + 5
    const sh = SH[name]
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
      <Bedroom lamp={() => state.current.lamp} />
      <LowPolyChar look={LUCIA} pose={() => poses.current.lucia} position={[-0.42, 0.56, -0.3]} />
      <LowPolyChar look={DANI} pose={() => poses.current.dani} position={[0.42, 0.56, -0.3]} />
      <group position={[1.2, 0.665, -0.5]} rotation={[0, -0.35, 0]}><Clock text={() => state.current.clock} /></group>
    </group>
  )
}

function overlays(lines: Line[], Dur: number) {
  const l = (id: string) => lines.find((x) => x.id === id)!
  const o: { a: number; b: number; st: string; tx: string }[] = []
  const POP = '\\t(0,180,\\fscx112\\fscy112)\\t(180,360,\\fscx100\\fscy100)'
  o.push({ a: l('l10').at - 0.6, b: l('l10').at + 1.0, st: 'Box', tx: `{\\an5\\pos(540,760)\\fad(80,120)${POP}\\fs96}20 MINUTOS DESPUÉS` })
  o.push({ a: l('l11').at + l('l11').dur * 0.45, b: l('l12').at - 0.1, st: 'Box', tx: `{\\an8\\pos(540,250)\\fad(120,120)${POP}\\fs64}HORAS DE SUEÑO\\N{\\fs92}ELLA 8 · TÚ 0` })
  o.push({ a: l('l12').at, b: Dur, st: 'Box', tx: `{\\an8\\pos(540,250)\\fad(150,0)${POP}\\fs70}COSAS DE PAREJA\\N{\\fs56}SÍGUENOS PARA EL EP. 2` })
  return o
}
