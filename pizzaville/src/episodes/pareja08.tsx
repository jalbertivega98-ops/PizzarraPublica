// COSAS DE PAREJA · EP. 8 — «Hazme una foto». Sofá, él con el móvil, flashes.
import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'
import { clock } from '../engine/clock'
import { LivingRoom, PairEpisode, Phone, beatFrame, box, coupleShots, type PairSpec } from './pareja_kit'
import { D, Lx } from './pareja_poses'

const SCRIPT = [
  { id: 'l01', text: "Le dices que está guapa. Error." },
  { id: 'l02', text: "«¡Ay, pues hazme una foto!»" },
  { id: 'l03', text: "Una foto. Fácil. Clic." },
  { id: 'l04', text: "«¡No, que salgo bizca!»" },
  { id: 'l05', text: "Otra. Clic." },
  { id: 'l06', text: "«¿Desde abajo? ¿Tú estás loco?»" },
  { id: 'l07', text: "Te agachas. Te subes al sofá. Contienes la respiración." },
  { id: 'l08', text: "«Haz muchas seguidas, en ráfaga.»" },
  { id: 'l09', text: "Ráfaga. Treinta fotos. Todas iguales. Todas preciosas." },
  { id: 'l10', text: "«En esta tengo papada. En esta el pelo raro. En esta salgo gorda.»" },
  { id: 'l11', text: "Cuarenta y siete fotos después, te duele un músculo que no sabías que tenías." },
  { id: 'l12', text: "«Ninguna vale. Es que no sabes hacer fotos.»" },
  { id: 'l13', text: "Al día siguiente la ves en Instagram." },
  { id: 'l14', text: "Es la primera foto. La de «salgo bizca»." },
  { id: 'l15', text: "Con cuatro filtros. Y la frase «foto random, sin pensar»." },
  { id: 'l16', text: "Etiqueta a la que te hace repetir cuarenta fotos." },
]

const ORDER = SCRIPT.map((s) => s.id)
const frame = beatFrame(ORDER, {
  l01: { d: D.nod, cut: 'wide', l: Lx.idle },
  l02: { l: Lx.excited, cut: 'luciaTight', d: D.stunned, dAt: 0.3 },
  l03: { d: D.photo, cut: 'two', l: Lx.pose1 },
  l04: { l: Lx.annoyed, cut: 'lucia', d: D.tired, dAt: 0.5 },
  l05: { d: D.photo, cut: 'dani', l: Lx.pose2 },
  l06: { l: Lx.disgust, cut: 'luciaTight', d: D.stunned, dAt: 0.3 },
  l07: { d: D.photoLow, cut: 'two', dMid: D.photo },
  l08: { l: Lx.pose1, cut: 'lucia' },
  l09: { d: D.photo, cut: 'wide', l: Lx.pose2, lMid: Lx.pose1 },
  l10: { l: Lx.stare, cut: 'luciaTight', lMid: Lx.disgust, d: D.tired, dAt: 0.4 },
  l11: { d: D.pain, cut: 'daniTight' },
  l12: { l: Lx.cross, cut: 'lucia', d: D.defeated, dAt: 0.4 },
  l13: { d: D.photo, cut: 'dani', l: Lx.idle },
  l14: { d: D.stunned, cut: 'daniTight' },
  l15: { d: D.camera, cut: 'two', l: Lx.smug },
  l16: { d: D.idle, cut: 'wide', l: Lx.happy },
}, D.idle, Lx.idle)

// shutter times are filled by frame() (needs line timings), then read by Flash/sfx
const shots: number[] = []
function shutterTimes(a: (id: string) => number, l: (id: string) => { dur: number }) {
  const s = [a('l03') + l('l03').dur * 0.75, a('l05') + l('l05').dur * 0.6, a('l08') + l('l08').dur + 0.15]
  for (let i = 0; i < 9; i++) s.push(a('l09') + 0.9 + i * 0.13)
  return s
}
function Flash() {
  const r = useRef<THREE.PointLight>(null!)
  useFrame(() => {
    const t = clock.t
    let k = 0
    for (const s of shots) if (t >= s && t < s + 0.12) k = 1 - (t - s) / 0.12
    r.current.intensity = 14 * k
  })
  return <pointLight ref={r} position={[0.2, 1.6, 0.8]} distance={4} color="#ffffff" />
}

const spec: PairSpec = {
  id: 'pareja08',
  script: SCRIPT,
  gap: { l02: 0.3, l03: 0.4, l04: 0.2, l05: 0.4, l06: 0.2, l07: 0.5, l08: 0.3, l09: 0.4, l10: 0.4, l11: 0.5, l12: 0.4, l13: 0.9, l14: 0.4, l15: 0.3, l16: 0.8 },
  her: ['l02', 'l04', 'l06', 'l08', 'l10', 'l12'],
  bg: '#1a1420',
  Set: () => <LivingRoom />,
  pos: { lucia: [-0.42, 0.5, -0.35], dani: [0.42, 0.5, -0.35] },
  shots: coupleShots(1.52, -0.35),
  daniHand: <Phone />,
  frame: (t, a, l, st) => {
    if (!shots.length) shots.push(...shutterTimes(a, l))
    const f = frame(t, a, l)
    if (t > a('l07') + l('l07').dur * 0.35 && t < a('l08')) f.dani.sink = -0.18 // stands on the sofa
    if (t > a('l13') - 0.2) st.luciaTop = undefined
    return f
  },
  extras: () => <Flash />,
  sfx: (l) => {
    const s = [l('l03').at + l('l03').dur * 0.75, l('l05').at + l('l05').dur * 0.6, l('l08').at + l('l08').dur + 0.15]
    for (let i = 0; i < 9; i++) s.push(l('l09').at + 0.9 + i * 0.13)
    return [
      ...s.map((at) => ({ type: 'tick', at, g: 0.6 })),
      { type: 'buzz', at: l('l04').at - 0.1, g: 0.35 },
      { type: 'buzz', at: l('l06').at - 0.1, g: 0.35 },
      { type: 'thud', at: l('l11').at + 0.3, g: 0.4 },
      { type: 'whoosh', at: l('l13').at - 0.5, g: 0.35 },
      { type: 'scratch', at: l('l14').at + 0.2, g: 0.45 },
      { type: 'ding', at: l('l15').at + 0.4, g: 0.4 },
    ]
  },
  overlays: (l, dur) => [
    box(l('l03').at, l('l05').at - 0.1, 250, 56, 'FOTOS HECHAS\\N{\\fs110}1', 8),
    box(l('l05').at, l('l09').at - 0.1, 250, 56, 'FOTOS HECHAS\\N{\\fs110}2', 8),
    box(l('l09').at + 0.9, l('l11').at - 0.1, 250, 56, 'FOTOS HECHAS\\N{\\fs110}32', 8),
    box(l('l11').at, l('l12').at - 0.1, 250, 56, 'FOTOS HECHAS\\N{\\fs110}47', 8),
    box(l('l12').at + 0.2, l('l13').at - 0.5, 760, 80, 'FOTOS VÁLIDAS: 0'),
    box(l('l13').at - 0.5, l('l14').at - 0.1, 760, 80, 'AL DÍA SIGUIENTE'),
    box(l('l14').at, l('l16').at - 0.1, 250, 54, 'FOTO PUBLICADA\\N{\\fs80}LA Nº 1 (BIZCA)', 8),
    box(l('l16').at, dur, 250, 70, 'COSAS DE PAREJA\\N{\\fs56}SÍGUENOS PARA EL EP. 9', 8),
  ],
}

export function Pareja08() { return <PairEpisode spec={spec} /> }
