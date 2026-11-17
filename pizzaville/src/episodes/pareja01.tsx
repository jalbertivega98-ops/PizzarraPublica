// COSAS DE PAREJA · EP. 1 — «No tengo hambre».
// Narrador en off que le habla al novio («tú»). Pizz = el novio; Lía = su novia.
// Todo el guion visual va colgado de los tiempos reales de cada frase de voz,
// así que si la voz cambia de duración, los planos y gags se recolocan solos.
import { useMemo, useRef, type ReactNode, type MutableRefObject } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { RoundedBox } from '@react-three/drei'
import * as THREE from 'three'
import { clock, ease, seg } from '../engine/clock'
import { world } from '../engine/director'
import { useLines, type Line } from '../engine/voice'
import { Character, PIZZ_LOOK, newState, type Look, type Action, type CharState } from '../scene/Character'
import { mat } from '../scene/materials'

export const LIA_LOOK: Look = {
  skin: '#f3c7a6', hair: '#3a2219', hairStyle: 3, top: '#a85bd6', topDark: '#8a45b8', pants: '#2b3b55', shoes: '#f6f4ee', accent: '#a85bd6',
  logo: null, eye: '#3f5a33', lashes: true, lip: '#c4566a',
}

export const PAREJA01 = {
  id: 'pareja01',
  script: [
    { id: 'l01', at: 0.35, text: 'Le preguntas a tu novia si tiene hambre.' },
    { id: 'l02', at: 2.9, text: '«No, no, que he merendado.»' },
    { id: 'l03', at: 5.3, text: 'Perfecto. Te pides una hamburguesa doble... solo para ti.' },
    { id: 'l04', at: 9.4, text: 'Error. Error de novato.' },
    { id: 'l05', at: 12.2, text: 'Llega el repartidor, abres la bolsa y, de repente: «¿Me das una patatita?»' },
    { id: 'l06', at: 18.0, text: 'Una. Dos. Cinco. A los dos minutos lleva más patatas que tú.' },
    { id: 'l07', at: 23.4, text: 'Vas a darle el último mordisco a tu hamburguesa...' },
    { id: 'l08', at: 26.8, text: '«Uy, ¿me dejas probar? Un bocadito.»' },
    { id: 'l09', at: 29.8, text: 'Un bocadito, dice. Media hamburguesa.' },
    { id: 'l10', at: 33.0, text: 'Resultado: tú, muerto de hambre. Ella, que no tenía hambre, cenada.' },
    { id: 'l11', at: 38.0, text: 'Y encima te mira y te suelta: «Oye... ¿y de postre qué hay?»' },
    { id: 'l12', at: 43.6, text: 'Etiqueta a esa novia que nunca tiene hambre.' },
  ],
}

// extra pauses (s) inserted BEFORE a line, for gags to breathe
const GAP: Record<string, number> = { l04: 0.25, l05: 0.5, l06: 0.35, l08: 0.45, l09: 0.5, l10: 0.35, l11: 0.6, l12: 0.9 }

// ---------------------------------------------------------------- helpers
const VOW = /[aeiouáéíóúü]/gi
/** mouth openness for the words of line l from word index k on */
function mouthFrom(l: Line | undefined, t: number, k = 0, k1 = 999) {
  if (!l) return 0
  const lt = t - l.at
  if (lt < 0 || lt > l.dur) return 0
  for (let i = k; i < Math.min(k1, l.words.length); i++) {
    const w = l.words[i]
    if (lt >= w.t && lt <= w.t + w.d) {
      const syl = Math.max(1, (w.w.match(VOW) ?? []).length)
      return 0.18 + 0.7 * Math.pow(Math.abs(Math.sin(((lt - w.t) / w.d) * syl * Math.PI)), 0.7)
    }
  }
  return 0.04
}
/** index of the first word inside «…» */
function quoteStart(l: Line) {
  const toks = l.text.split(/\s+/)
  const q = toks.findIndex((x) => x.includes('«'))
  return Math.max(0, q)
}
const wordT = (l: Line | undefined, i: number) => (l ? l.at + (l.words[Math.min(i, l.words.length - 1)]?.t ?? 0) : 0)
const endOf = (l: Line | undefined) => (l ? l.at + l.dur : 0)

function act(st: CharState, a: Action, t: number, t0: number, t1: number, fade = 0.18, w = 1) {
  if (t < t0 - fade || t > t1 + fade) return
  st.action = a; st.actionT = t - t0
  st.actionW = w * Math.min(seg(t, t0 - fade, t0), 1 - seg(t, t1, t1 + fade))
}

// ---------------------------------------------------------------- props
function Burger({ half = false }: { half?: boolean }) {
  const th = half ? Math.PI : Math.PI * 2
  const L = (y: number, r: number, h: number, c: string, rough = 0.7) => (
    <mesh position={[0, y, 0]} material={mat(c, { rough })} castShadow>
      <cylinderGeometry args={[r, r * 0.96, h, 24, 1, false, 0, th]} />
    </mesh>
  )
  return (
    <group rotation={[Math.PI / 2, 0, 0]} scale={0.95}>
      {L(0, 0.085, 0.03, '#e3a457')}
      {L(0.024, 0.09, 0.022, '#5a3220', 0.9)}
      {L(0.04, 0.094, 0.008, '#f5c33b', 0.5)}
      {L(0.052, 0.09, 0.02, '#5a3220', 0.9)}
      {L(0.066, 0.096, 0.008, '#6cbf4a', 0.6)}
      <mesh position={[0, 0.072, 0]} material={mat('#e3a457', { rough: 0.6 })} castShadow scale={[1, 0.55, 1]}>
        <sphereGeometry args={[0.088, 24, 12, 0, th, 0, Math.PI / 2]} />
      </mesh>
      {!half && [0, 1, 2, 3, 4].map((i) => (
        <mesh key={i} position={[Math.cos(i * 1.3) * 0.045, 0.12, Math.sin(i * 1.3) * 0.045]} material={mat('#fff3d6')}>
          <sphereGeometry args={[0.006, 6, 4]} />
        </mesh>
      ))}
    </group>
  )
}

function Fries({ left }: { left: () => number }) {
  const g = useRef<THREE.Group>(null!)
  const sticks = useMemo(() => Array.from({ length: 14 }, (_, i) => ({ x: ((i * 37) % 9) / 9 - 0.5, z: ((i * 53) % 7) / 7 - 0.5, h: 0.12 + ((i * 29) % 5) * 0.012, r: ((i * 17) % 7) / 7 - 0.5 })), [])
  useFrame(() => { const n = left(); g.current.children.forEach((c, i) => (c.visible = i < n)) })
  return (
    <group>
      <mesh position={[0, 0.07, 0]} material={mat('#d8342c', { rough: 0.5 })} castShadow>
        <cylinderGeometry args={[0.085, 0.06, 0.14, 4, 1, false, Math.PI / 4]} />
      </mesh>
      <mesh position={[0, 0.09, 0.062]} material={mat('#ffd34d', { rough: 0.5 })}>
        <circleGeometry args={[0.022, 12]} />
      </mesh>
      <group ref={g}>
        {sticks.map((s, i) => (
          <mesh key={i} position={[s.x * 0.09, 0.13 + s.h * 0.3, s.z * 0.06]} rotation={[s.z * 0.4, 0, s.r * 0.35]} material={mat('#f3c449', { rough: 0.6 })}>
            <boxGeometry args={[0.014, s.h, 0.014]} />
          </mesh>
        ))}
      </group>
    </group>
  )
}

const Fry = () => (
  <mesh rotation={[0.3, 0, 0.2]} material={mat('#f3c449', { rough: 0.6 })}><boxGeometry args={[0.014, 0.12, 0.014]} /></mesh>
)
const Phone = () => (
  <group rotation={[-0.2, 0, 0]}>
    <RoundedBox args={[0.075, 0.15, 0.012]} radius={0.008} smoothness={2} material={mat('#1d1f27', { rough: 0.3 })} />
    <mesh position={[0, 0, 0.007]} material={mat('#7fc8ff', { emissive: '#7fc8ff', ei: 0.9, rough: 0.2 })}><planeGeometry args={[0.064, 0.13]} /></mesh>
  </group>
)

function Bag() {
  return (
    <group>
      <mesh position={[0, 0.13, 0]} material={mat('#c9a06b', { rough: 0.95 })} castShadow><boxGeometry args={[0.24, 0.26, 0.15]} /></mesh>
      <mesh position={[0, 0.27, 0]} material={mat('#b58c58', { rough: 0.95 })}><boxGeometry args={[0.24, 0.03, 0.15]} /></mesh>
      <mesh position={[0, 0.14, 0.076]} material={mat('#ec6a3f', { rough: 0.6 })}><circleGeometry args={[0.055, 20]} /></mesh>
    </group>
  )
}

// ---------------------------------------------------------------- room
function Room() {
  const wall = mat('#f1d7b0', { rough: 0.95 })
  const wood = mat('#b98758', { rough: 0.75 })
  const sofa = mat('#3e8f8b', { rough: 0.9 }), sofaD = mat('#2f7470', { rough: 0.9 })
  return (
    <group>
      <hemisphereLight args={['#fff1dc', '#6a4a3a', 0.9]} />
      <directionalLight position={[-2.2, 4.2, 4.5]} intensity={2.2} color="#fff0db" castShadow shadow-mapSize={[2048, 2048]} shadow-bias={-0.0004}
        shadow-camera-left={-3} shadow-camera-right={3} shadow-camera-top={3} shadow-camera-bottom={-3} />
      <pointLight position={[1.75, 1.75, -0.6]} intensity={3.2} distance={5} color="#ffbf73" />
      <pointLight position={[0, 2.2, 2.4]} intensity={1.2} distance={6} color="#ffe7c8" />
      {/* floor + rug */}
      <mesh rotation-x={-Math.PI / 2} material={wood} receiveShadow><planeGeometry args={[10, 10]} /></mesh>
      {Array.from({ length: 24 }, (_, i) => (
        <mesh key={i} rotation-x={-Math.PI / 2} position={[-5 + i * 0.42, 0.001, 0]} material={mat('#a77649', { rough: 0.8 })}><planeGeometry args={[0.012, 10]} /></mesh>
      ))}
      <mesh rotation-x={-Math.PI / 2} position={[0, 0.004, 0.9]} material={mat('#e9e2d0', { rough: 1 })} receiveShadow><circleGeometry args={[1.35, 40]} /></mesh>
      <mesh rotation-x={-Math.PI / 2} position={[0, 0.005, 0.9]} material={mat('#d9653f', { rough: 1 })}><ringGeometry args={[1.15, 1.22, 40]} /></mesh>
      {/* back wall with window, poster and skirting */}
      <mesh position={[0, 1.6, -0.75]} material={wall} receiveShadow><planeGeometry args={[10, 3.2]} /></mesh>
      <mesh position={[0, 0.06, -0.74]} material={mat('#fffaf0')}><boxGeometry args={[10, 0.12, 0.02]} /></mesh>
      <mesh position={[-4.2, 1.6, 0.8]} rotation-y={Math.PI / 2} material={mat('#e9cba1', { rough: 0.95 })}><planeGeometry args={[5, 3.2]} /></mesh>
      <group position={[-1.55, 1.75, -0.73]}>
        <mesh material={mat('#ffffff')}><boxGeometry args={[1.0, 1.15, 0.05]} /></mesh>
        <mesh position={[0, 0, 0.03]} material={mat('#1b2550', { emissive: '#1b2550', ei: 0.6 })}><planeGeometry args={[0.88, 1.03]} /></mesh>
        {Array.from({ length: 26 }, (_, i) => (
          <mesh key={i} position={[((i * 37) % 23) / 23 * 0.8 - 0.4, -0.45 + ((i * 13) % 9) / 9 * 0.45, 0.035]} material={mat('#ffd98a', { emissive: '#ffd98a', ei: 1.4 })}>
            <planeGeometry args={[0.04, 0.05]} />
          </mesh>
        ))}
        <mesh position={[0.25, 0.32, 0.035]} material={mat('#fff6d8', { emissive: '#fff6d8', ei: 1.2 })}><circleGeometry args={[0.07, 20]} /></mesh>
        <mesh position={[0, 0, 0.04]} material={mat('#ffffff')}><boxGeometry args={[0.04, 1.03, 0.02]} /></mesh>
      </group>
      {/* pizza poster */}
      <group position={[0.95, 1.85, -0.73]}>
        <mesh material={mat('#2e2a3a')}><boxGeometry args={[0.62, 0.8, 0.03]} /></mesh>
        <mesh position={[0, 0, 0.02]} material={mat('#ffcf5a')}><planeGeometry args={[0.54, 0.72]} /></mesh>
        <mesh position={[0, 0.03, 0.025]} rotation-z={Math.PI} material={mat('#ec6a3f')}><circleGeometry args={[0.2, 3]} /></mesh>
        {[[-0.05, 0.05], [0.06, 0.0], [0.0, -0.08]].map(([x, y], i) => (
          <mesh key={i} position={[x, y, 0.03]} material={mat('#c62f2f')}><circleGeometry args={[0.03, 12]} /></mesh>
        ))}
      </group>
      {/* floor lamp */}
      <group position={[1.75, 0, -0.45]}>
        <mesh position={[0, 0.8, 0]} material={mat('#2d2a33', { metal: 0.4, rough: 0.4 })}><cylinderGeometry args={[0.015, 0.015, 1.6, 8]} /></mesh>
        <mesh position={[0, 0.02, 0]} material={mat('#2d2a33')}><cylinderGeometry args={[0.16, 0.18, 0.04, 20]} /></mesh>
        <mesh position={[0, 1.68, 0]} material={mat('#fff2d6', { emissive: '#ffc77a', ei: 0.9, side: THREE.DoubleSide })}><cylinderGeometry args={[0.15, 0.24, 0.3, 24, 1, true]} /></mesh>
      </group>
      {/* plant */}
      <group position={[-1.5, 0, -0.35]}>
        <mesh position={[0, 0.17, 0]} material={mat('#e7e1d6')} castShadow><cylinderGeometry args={[0.15, 0.12, 0.34, 18]} /></mesh>
        {Array.from({ length: 9 }, (_, i) => (
          <mesh key={i} position={[Math.cos(i * 2.4) * 0.12, 0.55 + (i % 3) * 0.12, Math.sin(i * 2.4) * 0.1]} rotation={[Math.sin(i) * 0.6, i, Math.cos(i * 2.4) * 0.7]} material={mat('#4f9a52', { rough: 0.8 })} castShadow>
            <sphereGeometry args={[0.13, 10, 6]} />
          </mesh>
        ))}
      </group>
      {/* sofa */}
      <group position={[0, 0, 0]}>
        <RoundedBox args={[2.1, 0.28, 0.82]} radius={0.05} position={[0, 0.16, -0.02]} material={sofaD} castShadow receiveShadow />
        {[-0.5, 0.5].map((x) => (
          <RoundedBox key={x} args={[0.98, 0.14, 0.74]} radius={0.06} smoothness={3} position={[x, 0.36, 0.0]} material={sofa} castShadow receiveShadow />
        ))}
        <RoundedBox args={[2.1, 0.62, 0.22]} radius={0.08} smoothness={3} position={[0, 0.66, -0.36]} material={sofa} castShadow receiveShadow />
        {[-1.1, 1.1].map((x) => (
          <RoundedBox key={x} args={[0.2, 0.5, 0.84]} radius={0.08} smoothness={3} position={[x, 0.42, -0.02]} material={sofaD} castShadow />
        ))}
        <RoundedBox args={[0.42, 0.36, 0.14]} radius={0.06} smoothness={3} position={[0.82, 0.62, -0.2]} rotation={[-0.25, -0.3, 0.12]} material={mat('#f3b33d', { rough: 0.95 })} castShadow />
        <RoundedBox args={[0.4, 0.34, 0.14]} radius={0.06} smoothness={3} position={[-0.84, 0.62, -0.2]} rotation={[-0.25, 0.3, -0.1]} material={mat('#e86f8a', { rough: 0.95 })} castShadow />
      </group>
      {/* coffee table */}
      <group position={[0, 0, 0.98]}>
        <RoundedBox args={[1.1, 0.06, 0.55]} radius={0.02} position={[0, 0.4, 0]} material={mat('#8a5a36', { rough: 0.6 })} castShadow receiveShadow />
        {[[-0.48, -0.22], [0.48, -0.22], [-0.48, 0.22], [0.48, 0.22]].map(([x, z], i) => (
          <mesh key={i} position={[x, 0.19, z]} material={mat('#6b4428')} castShadow><cylinderGeometry args={[0.025, 0.02, 0.38, 8]} /></mesh>
        ))}
      </group>
    </group>
  )
}

// ---------------------------------------------------------------- camera shots
type Shot = { p: [number, number, number]; l: [number, number, number]; fov: number; push?: number }
const HY = 1.27
const SH: Record<string, Shot> = {
  two: { p: [0, 1.3, 3.7], l: [0, 0.95, 0.1], fov: 38, push: 0.35 },
  twoTable: { p: [0, 1.5, 3.6], l: [0, 0.8, 0.5], fov: 38, push: 0.3 },
  liaCU: { p: [-0.05, 1.32, 2.1], l: [0.42, HY - 0.12, 0], fov: 32, push: 0.25 },
  pizzCU: { p: [0.05, 1.32, 2.1], l: [-0.42, HY - 0.12, 0], fov: 32, push: 0.25 },
  pizzECU: { p: [-0.25, 1.3, 1.55], l: [-0.42, HY - 0.04, 0], fov: 30, push: 0.15 },
  pizzBurger: { p: [-0.9, 1.22, 1.95], l: [-0.42, HY - 0.15, 0.1], fov: 34, push: 0.35 },
  table: { p: [0.35, 1.7, 2.0], l: [0.15, 0.5, 0.7], fov: 36, push: 0.2 },
}

// ---------------------------------------------------------------- component
export function Pareja01() {
  const { camera, scene } = useThree()
  const lines = useMemo(() => {
    const ls = useLines(PAREJA01.id, PAREJA01.script)
    return ls
  }, [])
  const L = (id: string) => lines.find((l) => l.id === id)!
  const pizz = useMemo(newState, [])
  const lia = useMemo(newState, [])
  const st = useRef({ friesLeft: 14, pizzBurger: 0 as 0 | 1 | 2, liaBurger: false, liaFry: false, pizzPhone: false, liaPhone: false, bag: false, table: false })
  const P = useMemo(() => new THREE.Vector3(), [])
  const LK = useMemo(() => new THREE.Vector3(), [])
  const headP = useMemo(() => new THREE.Vector3(-0.42, HY, 1.1), []) // cheated towards camera
  const headL = useMemo(() => new THREE.Vector3(0.42, HY, 1.1), [])
  const camV = useMemo(() => new THREE.Vector3(), [])

  useMemo(() => { scene.background = new THREE.Color('#1c1626'); scene.fog = null }, [])

  // spread lines with gag pauses once real timings are known (useLines already de-overlapped them)
  const layout = () => {
    // back-to-back with a short breath + gag pauses; recomputed every call, so it follows the real audio timings
    for (let i = 0; i < lines.length; i++) {
      lines[i].at = i === 0 ? 0.35 : lines[i - 1].at + lines[i - 1].dur + 0.55 + (GAP[lines[i].id] ?? 0)
    }
  }
  const duration = () => { layout(); return Math.ceil((endOf(lines[lines.length - 1]) + 3.2) * 10) / 10 }

  useMemo(() => {
    const pv = (window as any).__pv
    if (!pv) return
    pv.info = () => {
      layout()
      const l = L, D = duration()
      const q5 = wordT(l('l05'), quoteStart(l('l05')))
      const sfx: { type: string; at: number; g?: number }[] = [
        { type: 'whoosh', at: 0, g: 0.35 },
        { type: 'ding', at: l('l03').at + 0.2, g: 0.45 },
        { type: 'buzz', at: l('l04').at - 0.05, g: 0.55 },
        { type: 'doorbell', at: l('l05').at - 0.35, g: 0.55 },
        { type: 'paper', at: wordT(l('l05'), 4), g: 0.5 },
        { type: 'boing', at: q5 - 0.1, g: 0.35 },
        { type: 'riser', at: l('l07').at, g: 0.4 },
        { type: 'scratch', at: l('l08').at - 0.12, g: 0.55 },
        { type: 'munch', at: l('l08').at + l('l08').dur * 0.75, g: 0.6 },
        { type: 'growl', at: wordT(l('l10'), 3), g: 0.6 },
        { type: 'scratch', at: wordT(l('l11'), quoteStart(l('l11'))) - 0.1, g: 0.5 },
        { type: 'hit', at: wordT(l('l11'), quoteStart(l('l11')) + 2), g: 0.5 },
        { type: 'pop', at: l('l12').at, g: 0.35 },
      ]
      for (let k = 0; k < 3; k++) sfx.push({ type: 'munch', at: wordT(l('l06'), k) + 0.15, g: 0.35 })
      for (let k = 0; k < 4; k++) sfx.push({ type: 'tick', at: wordT(l('l06'), 3) + 0.2 + k * 0.35, g: 0.3 })
      const ov = overlays(lines, D)
      return { id: PAREJA01.id, duration: D, music: 'comedy', overlays: ov, lines: lines.map((x) => ({ id: x.id, at: x.at, dur: x.dur, text: x.text, words: x.words, hasAudio: x.hasAudio })), sfx }
    }
  }, [])

  useFrame(() => {
    layout()
    const t = clock.t
    const l = L
    const s = st.current
    // ---------------- base: both seated, idle
    for (const c of [pizz, lia]) { c.sit = 1; c.speed = 0; c.action = 'none'; c.actionW = 0; c.mouth = 0; c.brows = 0; c.smile = 0.6; c.visible = true; c.y = 0.02; c.z = 0.0 }
    pizz.x = -0.42; lia.x = 0.42
    pizz.ry = 0.12; lia.ry = -0.12
    pizz.lookAt = camV.set(0, 1.2, 3.5).clone()
    lia.lookAt = null
    s.pizzPhone = false; s.liaPhone = false; s.liaFry = false; s.liaBurger = false
    s.bag = t > l('l05').at - 0.2; s.table = t > wordT(l('l05'), 4)

    // l01: Pizz asks her (mouths the question), Lía scrolls her phone
    const a1 = l('l01').at, e1 = endOf(l('l01'))
    pizz.lookAt = headL; pizz.mouth = mouthFrom(l('l01'), t, 0) * 0.85
    act(pizz, 'talk', t, a1, e1, 0.2, 0.8)
    s.liaPhone = t < l('l02').at - 0.1
    if (s.liaPhone) act(lia, 'phone', t, -1, l('l02').at - 0.2, 0.25)
    // l02: «No, no, que he merendado» — Lía shakes head, sure of herself
    const a2 = l('l02').at, e2 = endOf(l('l02'))
    if (t > a2 - 0.3 && t < e2 + 0.4) {
      lia.lookAt = headP
      act(lia, 'no', t, a2, a2 + 0.7, 0.15)
      lia.mouth = mouthFrom(l('l02'), t, 0)
      lia.smile = 1; lia.brows = 0.3
    }
    // l03: he orders on his phone, smug
    const a3 = l('l03').at, e3 = endOf(l('l03'))
    if (t > a3 - 0.2 && t < l('l04').at) {
      s.pizzPhone = true
      act(pizz, 'phone', t, a3, l('l04').at - 0.1, 0.2)
      pizz.smile = 1; pizz.brows = 0.2; pizz.lookAt = null
    }
    // l04: ERROR. Pizz freezes, looks at camera
    const a4 = l('l04').at
    if (t > a4 && t < l('l05').at) { pizz.lookAt = camV.set(-0.4, 1.3, 3).clone(); pizz.brows = 0.9; pizz.smile = 0.2; act(pizz, 'surprise', t, a4, endOf(l('l04')), 0.1, 0.6) }
    // l05: delivery arrives; burger in his hand, fries on the table; then her puppy question
    const a5 = l('l05').at, q5 = wordT(l('l05'), quoteStart(l('l05'))), e5 = endOf(l('l05'))
    if (t > wordT(l('l05'), 5)) s.pizzBurger = 1
    else s.pizzBurger = 0
    if (t > a5 && t < q5) { pizz.smile = 1.1; pizz.lookAt = new THREE.Vector3(0.1, 0.5, 0.95); act(pizz, 'celebrate', t, a5 + 0.2, a5 + 0.9, 0.15, 0.35) }
    if (t > q5 - 0.2 && t < l('l06').at) {
      lia.lookAt = headP; lia.brows = 1; lia.smile = 1.1
      lia.mouth = mouthFrom(l('l05'), t, quoteStart(l('l05')))
      pizz.lookAt = headL; pizz.brows = 0.4
    }
    // l06: «Una. Dos. Cinco.» — she keeps stealing fries
    const a6 = l('l06').at, e6 = endOf(l('l06'))
    const steals = [wordT(l('l06'), 0), wordT(l('l06'), 1), wordT(l('l06'), 2), wordT(l('l06'), 2) + 0.35, wordT(l('l06'), 2) + 0.7, wordT(l('l06'), 3) + 0.3, wordT(l('l06'), 3) + 0.65, wordT(l('l06'), 3) + 1.0, wordT(l('l06'), 5) + 0.2, wordT(l('l06'), 6)]
    const stolen = steals.filter((x) => t > x).length
    s.friesLeft = Math.max(1, 14 - stolen - (t > a6 + 0.4 ? 1 : 0))
    if (t > a6 - 0.3 && t < e6 + 0.3) {
      // cycle: reach → eat for every steal
      const last = [...steals].reverse().find((x) => t > x - 0.25) ?? a6
      const ph = t - last
      if (ph < 0.25 || t < steals[0]) act(lia, 'reach', t, last - 0.25, last + 0.1, 0.12)
      else { act(lia, 'eat', t, last + 0.1, last + 0.6, 0.15); s.liaFry = ph < 0.6 }
      lia.lookAt = new THREE.Vector3(0.15, 0.55, 0.98); lia.smile = 1
      pizz.lookAt = headL; pizz.brows = -0.4; pizz.smile = 0.3
    }
    // l07: he goes for the last big bite
    const a7 = l('l07').at, e7 = endOf(l('l07'))
    if (t > a7 - 0.2 && t < l('l08').at + 0.3) {
      const k = seg(t, a7, e7 + 0.3)
      act(pizz, 'eat', t, a7, l('l08').at + 0.2, 0.6, 0.55 + 0.45 * k)
      pizz.lookAt = null; pizz.smile = 0.9; pizz.brows = 0.2
    }
    // l08: «Uy, ¿me dejas probar? Un bocadito.» → she takes it and bites
    const a8 = l('l08').at, e8 = endOf(l('l08'))
    const grab = a8 + l('l08').dur * 0.62
    if (t > a8 - 0.2 && t < l('l09').at + 0.2) {
      lia.lookAt = headP; lia.brows = 1; lia.smile = 1
      lia.mouth = mouthFrom(l('l08'), t, 0)
      pizz.lookAt = headL; pizz.brows = 0.8; pizz.smile = 0.2
      if (t < grab) act(lia, 'reach', t, grab - 0.5, grab, 0.25)
      else { act(lia, 'eat', t, grab + 0.05, l('l09').at + 0.1, 0.15); s.liaBurger = true; s.pizzBurger = 0 }
    }
    // l09: half burger back in his hand, deadpan stare at camera
    const a9 = l('l09').at
    if (t > a9 - 0.15) s.pizzBurger = t < l('l11').at ? 2 : 0
    if (t > a9 && t < l('l10').at) {
      pizz.lookAt = camV.set(-0.4, 1.3, 3).clone(); pizz.brows = -0.8; pizz.smile = 0
      act(pizz, 'reach', t, a9 + 0.05, l('l10').at, 0.2, 0.0)
      lia.lookAt = null; lia.smile = 1.1; act(lia, 'eat', t, a9, a9 + 0.8, 0.2, 0.6)
    }
    // l10: she relaxes, he is starving
    const a10 = l('l10').at
    if (t > a10 && t < l('l11').at) {
      pizz.lookAt = headL; pizz.brows = -0.6; pizz.smile = 0.1
      act(pizz, 'cross', t, a10 + 0.2, l('l11').at - 0.1, 0.25)
      lia.lookAt = camV.set(0.4, 1.3, 3).clone(); lia.smile = 1.2; lia.brows = 0.4
      lia.ry = -0.12 + 0.1 * ease.inOut(seg(t, a10, a10 + 0.6))
    }
    // l11: «Oye... ¿y de postre qué hay?»
    const a11 = l('l11').at, q11 = wordT(l('l11'), quoteStart(l('l11')))
    if (t > a11 && t < l('l12').at) {
      lia.lookAt = headP; lia.brows = 1; lia.smile = 1.1
      lia.mouth = mouthFrom(l('l11'), t, quoteStart(l('l11')))
      pizz.lookAt = headL
      if (t > q11) { act(pizz, 'surprise', t, q11 + 0.6, l('l12').at, 0.1); pizz.brows = 1; pizz.smile = 0; if (t > q11 + 0.5) pizz.lookAt = camV.set(-0.3, 1.3, 3).clone() }
    }
    // l12: CTA — he facepalms, she waves to camera
    const a12 = l('l12').at
    if (t > a12) {
      act(pizz, 'facepalm', t, a12 + 0.1, 99, 0.25); pizz.lookAt = null
      lia.lookAt = camV.set(0, 1.2, 3.8).clone(); lia.smile = 1.2
      act(lia, 'wave', t, a12 + 0.4, 99, 0.2, 0.8)
      lia.sit = 1
    }
    // blink-proof: when not their turn, keep mouths shut
    if (lia.action === 'eat' && lia.actionW > 0.5) lia.mouth = Math.max(lia.mouth, 0.25 + 0.2 * Math.abs(Math.sin(t * 9)))
    if (pizz.action === 'eat' && pizz.actionW > 0.9) pizz.mouth = 0.5

    // ---------------- camera: one shot per beat
    const cuts: [number, string][] = [
      [0, 'two'], [l('l02').at - 0.12, 'liaCU'], [l('l03').at - 0.1, 'pizzCU'], [l('l04').at - 0.08, 'pizzECU'],
      [l('l05').at - 0.4, 'twoTable'], [q5 - 0.12, 'liaCU'], [l('l06').at - 0.1, 'table'], [wordT(l('l06'), 3) - 0.05, 'two'],
      [l('l07').at - 0.1, 'pizzBurger'], [l('l08').at - 0.1, 'two'], [l('l09').at - 0.1, 'pizzECU'], [l('l10').at - 0.1, 'two'],
      [l('l11').at - 0.1, 'liaCU'], [q11 + 0.55, 'pizzECU'], [l('l12').at - 0.1, 'two'],
    ]
    let ci = 0
    while (ci + 1 < cuts.length && t >= cuts[ci + 1][0]) ci++
    const [c0, name] = cuts[ci]
    const c1 = ci + 1 < cuts.length ? cuts[ci + 1][0] : c0 + 6
    const sh = SH[name]
    const k = ease.out(seg(t, c0, c1 + 0.5))
    P.set(...sh.p); LK.set(...sh.l)
    const dir = LK.clone().sub(P).normalize()
    P.addScaledVector(dir, (sh.push ?? 0) * k)
    // snap-zoom punch on the ECU shots
    let fov = sh.fov
    if (name === 'pizzECU') fov = sh.fov + 10 * (1 - ease.out(seg(t, c0, c0 + 0.25)))
    // handheld feel
    P.x += Math.sin(t * 0.9) * 0.008; P.y += Math.sin(t * 1.3 + 1) * 0.006
    camera.position.copy(P); camera.lookAt(LK)
    const pc = camera as THREE.PerspectiveCamera
    if (Math.abs(pc.fov - fov) > 0.01) { pc.fov = fov; pc.updateProjectionMatrix() }
    world.focus.set(0, 0, 0)
  }, -1)

  const s = st.current
  return (
    <group>
      <Room />
      <Character look={PIZZ_LOOK} state={pizz} rightHand={<PizzHand st={st} />} />
      <Character look={LIA_LOOK} state={lia} rightHand={<LiaHand st={st} />} />
      <Vis on={() => st.current.bag} position={[-0.25, 0.43, 1.0]} rotation={[0, 0.3, 0]}><Bag /></Vis>
      <Vis on={() => st.current.table} position={[0.2, 0.43, 0.95]} rotation={[0, -0.2, 0]}><Fries left={() => st.current.friesLeft} /></Vis>
      {void s}
    </group>
  )
}

function Vis({ on, children, ...rest }: { on: () => boolean; children: ReactNode; position?: [number, number, number]; rotation?: [number, number, number] }) {
  const g = useRef<THREE.Group>(null!)
  useFrame(() => { g.current.visible = on() })
  return <group ref={g} {...rest}>{children}</group>
}

type St = MutableRefObject<{ friesLeft: number; pizzBurger: 0 | 1 | 2; liaBurger: boolean; liaFry: boolean; pizzPhone: boolean; liaPhone: boolean }>
function PizzHand({ st }: { st: St }) {
  return (
    <>
      <Vis on={() => st.current.pizzBurger === 1}><Burger /></Vis>
      <Vis on={() => st.current.pizzBurger === 2}><group rotation={[0, 0, Math.PI / 2]}><Burger half /></group></Vis>
      <Vis on={() => st.current.pizzPhone}><Phone /></Vis>
    </>
  )
}
function LiaHand({ st }: { st: St }) {
  return (
    <>
      <Vis on={() => st.current.liaBurger}><Burger /></Vis>
      <Vis on={() => st.current.liaFry}><Fry /></Vis>
      <Vis on={() => st.current.liaPhone}><Phone /></Vis>
    </>
  )
}

// ---------------------------------------------------------------- on-screen text (ASS), built from real line times
function overlays(lines: Line[], D: number) {
  const l = (id: string) => lines.find((x) => x.id === id)!
  const POP = '\\t(0,180,\\fscx114\\fscy114)\\t(180,360,\\fscx100\\fscy100)'
  const o: { a: number; b: number; st: string; tx: string }[] = []
  const add = (a: number, b: number, st: string, tx: string) => o.push({ a, b, st, tx })
  // series badge
  add(0, l('l02').at, 'Tag', '{\\an8\\pos(540,150)\\fad(0,200)}COSAS DE PAREJA · EP. 1')
  add(l('l03').at + 0.15, endOf(l('l03')) + 0.2, 'Mid', `{\\an5\\pos(540,430)\\fad(80,120)${POP}}HAMBURGUESA DOBLE\\N{\\c&H004DD3FF&\\fs70}SOLO PARA TI`)
  add(l('l04').at, l('l05').at - 0.3, 'Big', `{\\an5\\pos(540,420)\\fad(0,120)${POP}\\fs210\\bord11\\3c&H00201810&\\c&H003C3CD2&\\frz-6}ERROR\\N{\\fs100\\c&H00FFFFFF&\\frz-6}DE NOVATO`)
  // fries scoreboard
  const l6 = l('l06')
  const sc = (a: number, b: number, ella: number, tu: number) =>
    add(a, b, 'Mid', `{\\an8\\pos(540,240)\\fad(60,60)}{\\c&H0035C8F4&\\fs62}PATATAS\\N{\\fs110\\c&H00D65BA8&}ELLA ${ella}{\\c&H00FFFFFF&} – {\\c&H003F6AEC&}${tu} TÚ`)
  const w = (i: number) => l6.at + (l6.words[Math.min(i, l6.words.length - 1)]?.t ?? 0)
  sc(l6.at - 0.1, w(1), 1, 2)
  sc(w(1), w(2), 2, 2)
  sc(w(2), w(3), 5, 2)
  sc(w(3), endOf(l6) + 0.3, 9, 2)
  add(l('l09').at + 0.1, endOf(l('l09')) + 0.25, 'Mid', `{\\an5\\pos(540,420)\\fad(80,120)${POP}}«UN BOCADITO»\\N{\\c&H003C3CD2&\\fs86}= MEDIA HAMBURGUESA`)
  add(l('l10').at + 0.1, l('l11').at - 0.15, 'Mid', `{\\an8\\pos(540,240)\\fad(80,120)${POP}}{\\fs62}CENA DE HOY\\N{\\fs110\\c&H00D65BA8&}ELLA 1{\\c&H00FFFFFF&} – {\\c&H003F6AEC&}0 TÚ`)
  add(l('l12').at, D, 'Big', `{\\an5\\pos(540,380)\\fad(150,0)${POP}\\fs96}ETIQUETA A\\N{\\c&H004DD3FF&\\fs120}TU NOVIA`)
  add(l('l12').at + 0.6, D, 'Tag', '{\\an8\\pos(540,150)\\fad(200,0)}COSAS DE PAREJA · SÍGUENOS PARA EL EP. 2')
  return o
}
