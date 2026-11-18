// COSAS DE PAREJA · EP. 7 — «Elige tú la peli». Sofá, luz de la tele.
import { LivingRoom, PairEpisode, beatFrame, box, coupleShots, type PairSpec } from './pareja_kit'
import { D, Lx } from './pareja_poses'

const SCRIPT = [
  { id: 'l01', text: "Noche de peli. Le dices que elija ella." },
  { id: 'l02', text: "«No, no, elige tú, que siempre elijo yo.»" },
  { id: 'l03', text: "Vale. Propones una de acción." },
  { id: 'l04', text: "«Uf, tiros no, porfa.»" },
  { id: 'l05', text: "Una comedia." },
  { id: 'l06', text: "«Esa ya la vi en el dos mil catorce.»" },
  { id: 'l07', text: "Una de miedo." },
  { id: 'l08', text: "«¿Quieres que no duerma en un mes?»" },
  { id: 'l09', text: "Una romántica." },
  { id: 'l10', text: "«¿Esa no es la que muere el chico al final? No, que lloro.»" },
  { id: 'l11', text: "Un documental de animales." },
  { id: 'l12', text: "«¿Un documental? ¿Tienes ochenta años?»" },
  { id: 'l13', text: "Cincuenta minutos de tráiler en tráiler. Has visto más tráilers que películas este año." },
  { id: 'l14', text: "«¡Esta! Esta tiene buena pinta.»" },
  { id: 'l15', text: "Por fin. Le das al play." },
  { id: 'l16', text: "Minuto diez. Está dormida." },
  { id: 'l17', text: "«Mañana la seguimos, ¿eh? No la veas sin mí.»" },
  { id: 'l18', text: "Etiqueta a la que se duerme en todas las pelis." },
]

const ORDER = SCRIPT.map((s) => s.id)
const frame = beatFrame(ORDER, {
  l01: { d: D.idle, cut: 'wide', l: Lx.idle },
  l02: { l: Lx.sweet, cut: 'luciaTight', d: D.ask, dAt: 0.3 },
  l03: { d: D.hopeful, cut: 'dani', flap: true },
  l04: { l: Lx.disgust, cut: 'lucia', d: D.tired, dAt: 0.4 },
  l05: { d: D.trying, cut: 'daniTight', flap: true },
  l06: { l: Lx.meh, cut: 'luciaTight', d: D.tired, dAt: 0.4 },
  l07: { d: D.trying, cut: 'dani', flap: true },
  l08: { l: Lx.annoyed, cut: 'lucia', d: D.tired, dAt: 0.4 },
  l09: { d: D.trying, cut: 'daniTight', flap: true },
  l10: { l: Lx.sad, cut: 'luciaTight', d: D.tired, dAt: 0.4 },
  l11: { d: D.hopeful, cut: 'dani', flap: true },
  l12: { l: Lx.disgust, cut: 'lucia', d: D.stunned, dAt: 0.4 },
  l13: { d: D.slump, cut: 'wide', l: Lx.idle },
  l14: { l: Lx.excited, cut: 'luciaTight', d: D.stunned, dAt: 0.3 },
  l15: { d: D.nod, cut: 'two', l: Lx.happy },
  l16: { l: Lx.sleep, lAt: 0.6, cut: 'two', d: D.stare, dAt: 1.2, dMid: D.camera },
  l17: { l: Lx.sleep, cut: 'luciaTight', d: D.defeated, dAt: 0.3 },
  l18: { d: D.idle, cut: 'wide', l: Lx.sleep },
}, D.idle, Lx.idle)

const spec: PairSpec = {
  id: 'pareja07',
  script: SCRIPT,
  gap: { l02: 0.3, l03: 0.4, l04: 0.3, l05: 0.3, l06: 0.3, l07: 0.3, l08: 0.3, l09: 0.3, l10: 0.3, l11: 0.3, l12: 0.3, l13: 0.8, l14: 0.4, l15: 0.4, l16: 0.8, l17: 0.5, l18: 0.8 },
  her: ['l02', 'l04', 'l06', 'l08', 'l10', 'l12', 'l14', 'l17'],
  bg: '#141018',
  Set: () => <LivingRoom tv={() => 1.25} />,
  pos: { lucia: [-0.42, 0.5, -0.35], dani: [0.42, 0.5, -0.35] },
  shots: coupleShots(1.52, -0.35),
  frame: (t, a, l, st) => {
    const f = frame(t, a, l)
    // she mumbles l17 while asleep: keep eyes shut, mouth still moves (lip-sync)
    st.noBlink = t > a('l16') + 1.5
    if (t > a('l17') - 0.3) f.lucia.lids = 1
    return f
  },
  sfx: (l) => [
    { type: 'buzz', at: l('l04').at - 0.1, g: 0.35 },
    { type: 'buzz', at: l('l06').at - 0.1, g: 0.35 },
    { type: 'buzz', at: l('l08').at - 0.1, g: 0.35 },
    { type: 'buzz', at: l('l10').at - 0.1, g: 0.35 },
    { type: 'buzz', at: l('l12').at - 0.1, g: 0.35 },
    { type: 'whoosh', at: l('l13').at - 0.4, g: 0.35 },
    { type: 'ding', at: l('l14').at - 0.1, g: 0.45 },
    { type: 'pop', at: l('l15').at + 0.8, g: 0.4 },
    { type: 'scratch', at: l('l16').at + 0.9, g: 0.4 },
  ],
  overlays: (l, dur) => {
    const n = (k: number) => `PELIS DESCARTADAS\\N{\\fs110}${k}`
    return [
      box(l('l04').at, l('l06').at - 0.05, 250, 56, n(1), 8),
      box(l('l06').at, l('l08').at - 0.05, 250, 56, n(2), 8),
      box(l('l08').at, l('l10').at - 0.05, 250, 56, n(3), 8),
      box(l('l10').at, l('l12').at - 0.05, 250, 56, n(4), 8),
      box(l('l12').at, l('l13').at - 0.4, 250, 56, n(5), 8),
      box(l('l13').at - 0.4, l('l14').at - 0.1, 760, 86, '50 MINUTOS DESPUÉS\\N{\\fs56}TRÁILERS VISTOS: 38'),
      box(l('l16').at + 0.9, l('l17').at - 0.1, 250, 64, 'MINUTO 10\\N{\\fs92}KO', 8),
      box(l('l18').at, dur, 250, 70, 'COSAS DE PAREJA\\N{\\fs56}SÍGUENOS PARA EL EP. 8', 8),
    ]
  },
}

export function Pareja07() { return <PairEpisode spec={spec} /> }
