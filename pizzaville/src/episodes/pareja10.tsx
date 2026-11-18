// COSAS DE PAREJA · EP. 10 — El último trozo de pizza. Sofá, caja de pizza en la mesa.
import { LivingRoom, PairEpisode, Show, beatFrame, box, coupleShots, type PairSpec } from './pareja_kit'
import { D, Lx } from './pareja_poses'

const SCRIPT = [
  { id: 'l01', text: "Pizza familiar. Viernes. Felicidad." },
  { id: 'l02', text: "Queda un trozo. El último." },
  { id: 'l03', text: "Le preguntas si lo quiere." },
  { id: 'l04', text: "«No, no, cógelo tú, yo estoy llena.»" },
  { id: 'l05', text: "Estoy llena. Eso es lo que dijo." },
  { id: 'l06', text: "Lo coges. Despacio. Como quien desactiva una bomba." },
  { id: 'l07', text: "Primer mordisco... y notas su mirada." },
  { id: 'l08', text: "Te mira como si te estuvieras comiendo a su perro." },
  { id: 'l09', text: "«Nada, nada, cómetelo. Si yo no quería.»" },
  { id: 'l10', text: "Ya no sabe igual. Sabe a culpa." },
  { id: 'l11', text: "«No, de verdad, disfrútalo. Yo ya me comeré un yogur.»" },
  { id: 'l12', text: "Un yogur. Ha dicho un yogur. Esto es peor que una bronca." },
  { id: 'l13', text: "Le ofreces la mitad del trozo. Mordido." },
  { id: 'l14', text: "«¿Mordido? Qué asco, no.»" },
  { id: 'l15', text: "Media hora después suena el timbre." },
  { id: 'l16', text: "«¡He pedido otra pizza! Como tú te comiste el último trozo...»" },
  { id: 'l17', text: "Etiqueta a la que está llena... hasta que te ve comiendo." },
]

const ORDER = SCRIPT.map((s) => s.id)
const frame = beatFrame(ORDER, {
  l01: { d: D.chew, cut: 'wide', l: Lx.happy },
  l02: { d: D.idle, cut: 'table' },
  l03: { d: D.ask, cut: 'dani', flap: true },
  l04: { l: Lx.sweet, cut: 'luciaTight', d: D.nod, dAt: 0.4 },
  l05: { d: D.camera, cut: 'daniTight' },
  l06: { d: D.sneaky, cut: 'two', dMid: D.chew },
  l07: { d: D.chew, cut: 'dani', l: Lx.stareFood, lAt: 1.0 },
  l08: { l: Lx.stareFood, cut: 'luciaTight', d: D.guilty },
  l09: { l: Lx.sad, cut: 'lucia', d: D.guilty },
  l10: { d: D.guilty, cut: 'daniTight' },
  l11: { l: Lx.sad, cut: 'luciaTight' },
  l12: { d: D.camera, cut: 'daniTight' },
  l13: { d: D.sorry, cut: 'two' },
  l14: { l: Lx.disgust, cut: 'luciaTight', d: D.stunned, dAt: 0.3 },
  l15: { d: D.stunned, cut: 'wide', l: Lx.smug },
  l16: { l: Lx.excited, cut: 'lucia', d: D.defeated, dAt: 0.6 },
  l17: { d: D.idle, cut: 'wide', l: Lx.happy },
}, D.idle, Lx.happy)

function Slice({ bite = false }: { bite?: boolean }) {
  return (
    <group>
      <mesh rotation-x={-Math.PI / 2}><circleGeometry args={[0.2, 6, 0, bite ? Math.PI / 6 : Math.PI / 4]} /><meshStandardMaterial color="#f2b33d" flatShading side={2} /></mesh>
      {[[0.11, 0.03], [0.15, 0.06], [0.08, 0.06]].map(([x, z], i) => <mesh key={i} position={[x, 0.006, -z]}><cylinderGeometry args={[0.018, 0.018, 0.006, 7]} /><meshStandardMaterial color="#b8332a" flatShading /></mesh>)}
    </group>
  )
}
function PizzaBox({ slices, open = true }: { slices: number; open?: boolean }) {
  return (
    <group>
      <mesh position={[0, 0.02, 0]}><boxGeometry args={[0.5, 0.04, 0.5]} /><meshStandardMaterial color="#d9b88a" flatShading /></mesh>
      {open && <mesh position={[0, 0.25, -0.25]} rotation-x={-0.25}><boxGeometry args={[0.5, 0.5, 0.01]} /><meshStandardMaterial color="#cfae80" flatShading /></mesh>}
      {Array.from({ length: slices }).map((_, i) => <group key={i} position={[0, 0.045, 0]} rotation-y={(i * Math.PI) / 4}><Slice /></group>)}
    </group>
  )
}

const spec: PairSpec = {
  id: 'pareja10',
  script: SCRIPT,
  gap: { l02: 0.5, l03: 0.4, l04: 0.3, l05: 0.4, l06: 0.5, l07: 0.4, l08: 0.3, l09: 0.4, l10: 0.4, l11: 0.3, l12: 0.4, l13: 0.5, l14: 0.3, l15: 0.8, l16: 0.3, l17: 0.8 },
  her: ['l04', 'l09', 'l11', 'l14', 'l16'],
  bg: '#1a1420',
  Set: () => <LivingRoom />,
  pos: { lucia: [-0.42, 0.5, -0.35], dani: [0.42, 0.5, -0.35] },
  shots: { ...coupleShots(1.52, -0.35), table: { p: [0.15, 1.25, 2.25], l: [0.15, 0.42, 1.2], fov: 34, push: 0.15 } },
  daniHand: null,
  frame: (t, a, l, st) => {
    const f = frame(t, a, l)
    st.inBox = t < a('l06') + l('l06').dur * 0.45
    st.inHand = !st.inBox && t < a('l15')
    st.newPizza = t > a('l16') + 0.3
    if (st.inHand) { f.dani.rSh = [1.25, -0.1]; f.dani.rEl = -1.55 }
    return f
  },
  extras: (st) => (
    <group>
      <group position={[0.18, 0.39, 1.22]}><PizzaBox slices={0} /></group>
      <Show show={() => st.inBox}><group position={[0.18, 0.39, 1.22]}><group position={[0, 0.045, 0]}><Slice /></group></group></Show>
      <Show show={() => st.inHand}><group position={[0.55, 1.32, 0.05]} rotation={[0.9, 0.6, 0]}><Slice bite /></group></Show>
      <Show show={() => st.newPizza}><group position={[-0.25, 0.47, 1.22]}><PizzaBox slices={8} /></group></Show>
    </group>
  ),
  sfx: (l) => [
    { type: 'munch', at: l('l01').at + 0.4, g: 0.4 },
    { type: 'riser', at: l('l02').at, g: 0.25 },
    { type: 'ding', at: l('l04').at + l('l04').dur, g: 0.35 },
    { type: 'tick', at: l('l06').at + 0.6, g: 0.4 }, { type: 'tick', at: l('l06').at + 1.2, g: 0.4 },
    { type: 'munch', at: l('l07').at + 1.0, g: 0.5 },
    { type: 'hit', at: l('l08').at, g: 0.35 },
    { type: 'buzz', at: l('l12').at, g: 0.35 },
    { type: 'buzz', at: l('l14').at - 0.1, g: 0.4 },
    { type: 'doorbell', at: l('l15').at + l('l15').dur * 0.6, g: 0.55 },
    { type: 'scratch', at: l('l16').at + 0.3, g: 0.4 },
  ],
  overlays: (l, dur) => [
    box(l('l02').at, l('l03').at - 0.1, 250, 60, 'TROZOS RESTANTES\\N{\\fs110}1', 8),
    box(l('l05').at, l('l06').at - 0.1, 250, 56, '«ESTOY LLENA»\\N{\\fs50}(DECLARACIÓN JURADA)', 8),
    box(l('l08').at, l('l10').at - 0.1, 250, 56, 'NIVEL DE CULPA\\N{\\fs96}87%', 8),
    box(l('l10').at, l('l12').at - 0.1, 250, 56, 'NIVEL DE CULPA\\N{\\fs96}100%', 8),
    box(l('l15').at + 0.2, l('l16').at - 0.1, 760, 80, 'MEDIA HORA DESPUÉS'),
    box(l('l16').at + 0.3, l('l17').at - 0.1, 250, 56, 'PIZZAS\\N{\\fs80}TÚ 1 · ELLA 1,9', 8),
    box(l('l17').at, dur, 250, 70, 'COSAS DE PAREJA\\N{\\fs56}SÍGUENOS PARA MÁS', 8),
  ],
}

export function Pareja10() { return <PairEpisode spec={spec} /> }
