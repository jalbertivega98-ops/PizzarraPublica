// COSAS DE PAREJA · EP. 5 — «Cinco minutos y salgo». Sofá; ella va cambiando de conjunto, reloj en la pared.
import { Clock } from './pareja01v2'
import { LivingRoom, PairEpisode, beatFrame, box, coupleShots, type PairSpec } from './pareja_kit'
import { D, Lx } from './pareja_poses'

const SCRIPT = [
  { id: 'l01', text: "Habéis quedado a cenar a las nueve. Son menos cuarto. Tú llevas listo desde las ocho." },
  { id: 'l02', text: "«¡Cinco minutos y salgo!»" },
  { id: 'l03', text: "Cinco minutos. Apúntalo." },
  { id: 'l04', text: "Tú te sientas en el sofá. Con los zapatos puestos. Con las llaves en la mano." },
  { id: 'l05', text: "Primer conjunto. A ti te parece perfecto." },
  { id: 'l06', text: "«Mmm... no, que me hace rara.»" },
  { id: 'l07', text: "Segundo conjunto. También perfecto." },
  { id: 'l08', text: "«¡Es que no tengo nada que ponerme!»" },
  { id: 'l09', text: "Tiene un armario entero. Tú tienes dos cajones. Y uno es suyo." },
  { id: 'l10', text: "«Amor, ¿este o este?»" },
  { id: 'l11', text: "Son iguales. Son exactamente iguales. Pero tú dices que el de la derecha." },
  { id: 'l12', text: "«¿Ves? Por eso no te pregunto.»" },
  { id: 'l13', text: "Nueve y media. Tercer conjunto. Cuarto. Quinto." },
  { id: 'l14', text: "«¡Ya está! Al final me pongo el primero.»" },
  { id: 'l15', text: "El primero. El de hace cuarenta y cinco minutos." },
  { id: 'l16', text: "Llegáis a las diez menos diez. Y adivina qué." },
  { id: 'l17', text: "Los demás tampoco han llegado." },
  { id: 'l18', text: "«¿Ves? Si es que te agobias por nada.»" },
  { id: 'l19', text: "Etiqueta a la de los cinco minutos que son cincuenta." },
]

const ORDER = SCRIPT.map((s) => s.id)
const frame = beatFrame(ORDER, {
  l01: { d: D.wait, cut: 'wide', l: Lx.mirror },
  l02: { l: Lx.rush, cut: 'luciaTight', d: D.nod, dAt: 0.3 },
  l03: { d: D.camera, cut: 'daniTight', l: Lx.mirror },
  l04: { d: D.wait, cut: 'two', dMid: D.bored },
  l05: { d: D.hopeful, cut: 'lucia', l: Lx.pose1 },
  l06: { l: Lx.doubt, cut: 'luciaTight', d: D.tired, dAt: 0.4 },
  l07: { d: D.trying, cut: 'two', l: Lx.pose2 },
  l08: { l: Lx.annoyed, cut: 'lucia', d: D.stunned, dAt: 0.3 },
  l09: { d: D.camera, cut: 'daniTight', l: Lx.mirror },
  l10: { l: Lx.pose1, cut: 'luciaTight', d: D.ask, dAt: 0.3 },
  l11: { d: D.think, cut: 'dani', dMid: D.point, flap: false },
  l12: { l: Lx.smug, cut: 'luciaTight', d: D.stunned, dAt: 0.3 },
  l13: { d: D.slump, cut: 'wide', l: Lx.pose2, lMid: Lx.pose1 },
  l14: { l: Lx.happy, cut: 'lucia', d: D.stare, dAt: 0.4 },
  l15: { d: D.camera, cut: 'daniTight' },
  l16: { d: D.tired, cut: 'clock', l: Lx.rush },
  l17: { d: D.stunned, cut: 'two' },
  l18: { l: Lx.smug, cut: 'luciaTight', d: D.defeated, dAt: 0.4 },
  l19: { d: D.idle, l: Lx.happy, cut: 'wide' },
}, D.wait, Lx.mirror)

// outfit colour by time
const OUT = ['#f08aa6', '#d9483b', '#3f7fd6', '#3f9a6a', '#e0b84a', '#7a4fc9', '#2b2b33']
const spec: PairSpec = {
  id: 'pareja05',
  script: SCRIPT,
  gap: { l02: 0.3, l03: 0.4, l04: 0.4, l05: 0.6, l06: 0.3, l07: 0.5, l08: 0.3, l09: 0.4, l10: 0.5, l11: 0.3, l12: 0.3, l13: 0.7, l14: 0.4, l15: 0.4, l16: 0.8, l17: 0.5, l18: 0.4, l19: 0.8 },
  her: ['l02', 'l06', 'l08', 'l10', 'l12', 'l14', 'l18'],
  bg: '#1a1420',
  Set: () => <LivingRoom />,
  pos: { lucia: [-0.42, 0.5, -0.35], dani: [0.42, 0.5, -0.35] },
  shots: { ...coupleShots(1.52, -0.35), clock: { p: [-0.95, 1.6, 0.15], l: [-0.95, 1.58, -1.03], fov: 32, push: 0.1 } },
  frame: (t, a, l, st) => {
    const f = frame(t, a, l)
    let o = 0
    if (t > a('l05') - 0.2) o = 1
    if (t > a('l07') - 0.2) o = 2
    if (t > a('l10') - 0.2) o = 3
    if (t > a('l13') - 0.2) o = 4 + Math.floor((t - a('l13')) / 1.1) % 3
    if (t > a('l14') - 0.2) o = 1
    st.luciaTop = OUT[o]
    // clock: 20:45 → 21:30 (l13) → 21:50 (l16)
    const mins = t < a('l13') ? 20 * 60 + 45 + Math.floor((t / a('l13')) * 30) : t < a('l16') ? 21 * 60 + 30 + Math.floor(((t - a('l13')) / (a('l16') - a('l13'))) * 15) : 21 * 60 + 50
    st.clock = `${Math.floor(mins / 60)}:${String(mins % 60).padStart(2, '0')}`
    return f
  },
  extras: (st) => (
    <group position={[-0.95, 1.58, -1.0]} scale={1.6}>
      <Clock text={() => st.clock ?? '20:45'} />
    </group>
  ),
  sfx: (l) => [
    { type: 'ding', at: l('l02').at - 0.1, g: 0.4 },
    { type: 'whoosh', at: l('l05').at - 0.2, g: 0.35 },
    { type: 'buzz', at: l('l06').at - 0.1, g: 0.4 },
    { type: 'whoosh', at: l('l07').at - 0.2, g: 0.35 },
    { type: 'buzz', at: l('l08').at, g: 0.35 },
    { type: 'whoosh', at: l('l10').at - 0.2, g: 0.35 },
    { type: 'scratch', at: l('l12').at - 0.1, g: 0.4 },
    { type: 'whoosh', at: l('l13').at, g: 0.3 }, { type: 'whoosh', at: l('l13').at + 1.1, g: 0.3 }, { type: 'whoosh', at: l('l13').at + 2.2, g: 0.3 },
    { type: 'ding', at: l('l14').at - 0.1, g: 0.45 },
    { type: 'tick', at: l('l16').at - 0.3, g: 0.5 },
    { type: 'boing', at: l('l17').at + 0.2, g: 0.4 },
  ],
  overlays: (l, dur) => [
    box(l('l02').at, l('l03').at + l('l03').dur, 250, 64, '«5 MINUTOS»\\N{\\fs50}(ESTIMACIÓN OFICIAL)', 8),
    box(l('l05').at, l('l06').at + l('l06').dur, 250, 56, 'CONJUNTO Nº 1', 8),
    box(l('l07').at, l('l08').at + l('l08').dur, 250, 56, 'CONJUNTO Nº 2', 8),
    box(l('l09').at + 0.2, l('l10').at - 0.1, 250, 54, 'ARMARIO\\N{\\fs80}ELLA 95% · TÚ 5%', 8),
    box(l('l11').at + 0.3, l('l12').at - 0.1, 250, 54, 'DIFERENCIAS ENCONTRADAS\\N{\\fs110}0', 8),
    box(l('l13').at, l('l14').at - 0.1, 250, 56, 'CONJUNTOS PROBADOS\\N{\\fs110}5', 8),
    box(l('l15').at, l('l16').at - 0.1, 250, 56, 'GANADOR\\N{\\fs80}EL PRIMERO', 8),
    box(l('l17').at, l('l18').at - 0.1, 760, 64, 'LOS DEMÁS: TAMPOCO HAN LLEGADO'),
    box(l('l19').at, dur, 250, 70, 'COSAS DE PAREJA\\N{\\fs56}SÍGUENOS PARA EL EP. 6', 8),
  ],
}

export function Pareja05() { return <PairEpisode spec={spec} /> }
