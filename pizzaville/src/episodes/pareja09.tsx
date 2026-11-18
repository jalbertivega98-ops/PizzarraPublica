// COSAS DE PAREJA · EP. 9 — «¿Me queda bien?». Sofá; ella se prueba vestidos (cambia el color de la ropa).
import { LivingRoom, PairEpisode, beatFrame, box, coupleShots, type PairSpec } from './pareja_kit'
import { D, Lx } from './pareja_poses'

const SCRIPT = [
  { id: 'l01', text: "Hay preguntas que no tienen respuesta correcta. Y esta es la peor." },
  { id: 'l02', text: "«¿Me queda bien este vestido?»" },
  { id: 'l03', text: "Opción uno: dices que sí." },
  { id: 'l04', text: "«Lo dices por decir. Ni lo has mirado.»" },
  { id: 'l05', text: "Opción dos: dices que no." },
  { id: 'l06', text: "«¿Ah, sí? ¿Y qué es lo que me queda mal, a ver?»" },
  { id: 'l07', text: "Opción tres: dices que normal." },
  { id: 'l08', text: "Nunca digas normal. Nadie ha sobrevivido a un normal." },
  { id: 'l09', text: "Opción cuatro: fingir un desmayo." },
  { id: 'l10', text: "Lo valoras. Lo valoras en serio." },
  { id: 'l11', text: "Así que respiras hondo y dices: te queda increíble, amor." },
  { id: 'l12', text: "«¿Mejor que el negro?»" },
  { id: 'l13', text: "El negro. ¿Qué negro? Nadie te había hablado del negro." },
  { id: 'l14', text: "Ella vuelve al probador. Con el negro. Y con un tercero que tampoco conocías." },
  { id: 'l15', text: "«Bueno, ¿y cuál me llevo?»" },
  { id: 'l16', text: "Respuestas correctas posibles: cero." },
  { id: 'l17', text: "Etiqueta a la que te hace la pregunta trampa." },
]

const ORDER = SCRIPT.map((s) => s.id)
const frame = beatFrame(ORDER, {
  l01: { d: D.camera, cut: 'daniTight', l: Lx.mirror },
  l02: { l: Lx.pose1, cut: 'lucia', d: D.panic, dAt: 0.5 },
  l03: { d: D.nod, cut: 'dani', flap: false },
  l04: { l: Lx.annoyed, cut: 'luciaTight', d: D.stunned, dAt: 0.3 },
  l05: { d: D.sorry, cut: 'dani' },
  l06: { l: Lx.cross, cut: 'lucia', d: D.panic, dAt: 0.3 },
  l07: { d: D.think, cut: 'daniTight' },
  l08: { d: D.camera, cut: 'two', l: Lx.stare },
  l09: { d: D.think, cut: 'dani', dMid: D.faint },
  l10: { d: D.think, cut: 'daniTight' },
  l11: { d: D.breathe, cut: 'two', dMid: D.hopeful, l: Lx.mirror },
  l12: { l: Lx.doubt, cut: 'luciaTight', d: D.stunned, dAt: 0.3 },
  l13: { d: D.panic, cut: 'daniTight' },
  l14: { l: Lx.pose2, cut: 'lucia', lMid: Lx.pose1, d: D.stunned },
  l15: { l: Lx.sweet, cut: 'luciaTight', d: D.panic, dAt: 0.3 },
  l16: { d: D.defeated, cut: 'two' },
  l17: { d: D.idle, cut: 'wide', l: Lx.happy },
}, D.idle, Lx.mirror)

const spec: PairSpec = {
  id: 'pareja09',
  script: SCRIPT,
  gap: { l02: 0.6, l03: 0.6, l04: 0.2, l05: 0.5, l06: 0.2, l07: 0.5, l08: 0.3, l09: 0.5, l10: 0.4, l11: 0.6, l12: 0.4, l13: 0.4, l14: 0.6, l15: 0.4, l16: 0.6, l17: 0.8 },
  her: ['l02', 'l04', 'l06', 'l12', 'l15'],
  bg: '#1a1420',
  Set: () => <LivingRoom />,
  pos: { lucia: [-0.42, 0.5, -0.35], dani: [0.42, 0.5, -0.35] },
  shots: coupleShots(1.52, -0.35),
  frame: (t, a, l, st) => {
    const f = frame(t, a, l)
    let c = '#f08aa6'
    if (t > a('l02') - 0.3) c = '#c8324a' // the dress
    if (t > a('l14') - 0.2) c = '#22202a' // the black one
    if (t > a('l14') + l('l14').dur * 0.5) c = '#2f8a5a' // and a third one
    if (t > a('l15') - 0.2) c = '#c8324a'
    st.luciaTop = c
    return f
  },
  sfx: (l) => [
    { type: 'riser', at: l('l01').at + 0.5, g: 0.3 },
    { type: 'hit', at: l('l02').at + l('l02').dur, g: 0.4 },
    { type: 'buzz', at: l('l04').at - 0.1, g: 0.4 },
    { type: 'buzz', at: l('l06').at - 0.1, g: 0.4 },
    { type: 'buzz', at: l('l08').at, g: 0.4 },
    { type: 'thud', at: l('l09').at + l('l09').dur * 0.55, g: 0.45 },
    { type: 'ding', at: l('l11').at + l('l11').dur * 0.6, g: 0.4 },
    { type: 'scratch', at: l('l13').at - 0.1, g: 0.45 },
    { type: 'whoosh', at: l('l14').at - 0.2, g: 0.35 },
    { type: 'whoosh', at: l('l14').at + l('l14').dur * 0.5, g: 0.35 },
    { type: 'buzz', at: l('l16').at, g: 0.4 },
  ],
  overlays: (l, dur) => [
    box(l('l02').at + 0.2, l('l03').at - 0.1, 250, 64, 'PREGUNTA TRAMPA\\N{\\fs50}NIVEL: MÁXIMO', 8),
    box(l('l03').at, l('l05').at - 0.05, 250, 56, 'OPCIÓN 1: «SÍ»\\N{\\fs80}MAL', 8),
    box(l('l05').at, l('l07').at - 0.05, 250, 56, 'OPCIÓN 2: «NO»\\N{\\fs80}FATAL', 8),
    box(l('l07').at, l('l09').at - 0.05, 250, 56, 'OPCIÓN 3: «NORMAL»\\N{\\fs80}GAME OVER', 8),
    box(l('l09').at, l('l11').at - 0.05, 250, 56, 'OPCIÓN 4: DESMAYO\\N{\\fs80}¿...?', 8),
    box(l('l13').at, l('l14').at - 0.1, 760, 80, '¿¿QUÉ NEGRO??'),
    box(l('l16').at, l('l17').at - 0.1, 250, 56, 'RESPUESTAS CORRECTAS\\N{\\fs110}0', 8),
    box(l('l17').at, dur, 250, 70, 'COSAS DE PAREJA\\N{\\fs56}SÍGUENOS PARA EL EP. 10', 8),
  ],
}

export function Pareja09() { return <PairEpisode spec={spec} /> }
