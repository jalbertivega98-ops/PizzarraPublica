// COSAS DE PAREJA · EP. 6 — La guerra del termostato. Sofá, termostato en la pared.
import { Clock } from './pareja01v2'
import { LivingRoom, PairEpisode, Show, beatFrame, box, coupleShots, type PairSpec } from './pareja_kit'
import { D, Lx } from './pareja_poses'

const SCRIPT = [
  { id: 'l01', text: "Invierno. Pones la calefacción a veintiún grados. Temperatura perfecta." },
  { id: 'l02', text: "Te das la vuelta un momento... y está a veinticinco." },
  { id: 'l03', text: "Nadie ha dicho nada. Nadie ha visto nada." },
  { id: 'l04', text: "La bajas a veintidós. En silencio. Como un ninja." },
  { id: 'l05', text: "Diez minutos después: veinticuatro." },
  { id: 'l06', text: "Veintiuno." },
  { id: 'l07', text: "Veintiséis." },
  { id: 'l08', text: "Esto ya no es una casa. Es una guerra fría. Bueno, caliente." },
  { id: 'l09', text: "Ella pasa por el pasillo. Silbando. Mirando al techo." },
  { id: 'l10', text: "Tú vuelves. Veintiocho grados. Esto ya es Sevilla en agosto." },
  { id: 'l11', text: "«Amor, ¿tú has tocado la calefacción? Es que tengo un frío...»" },
  { id: 'l12', text: "Frío. En una casa a veintiocho grados. Con tu sudadera puesta." },
  { id: 'l13', text: "Y dos mantas. Y calcetines de lana." },
  { id: 'l14', text: "Tú, mientras, te abanicas con la factura del gas." },
  { id: 'l15', text: "La factura llega a final de mes. Ciento ochenta euros." },
  { id: 'l16', text: "«¡Uf, qué caro está el gas! Tenemos que ahorrar, ¿eh?»" },
  { id: 'l17', text: "Etiqueta a la que tiene frío hasta en agosto." },
]

const ORDER = SCRIPT.map((s) => s.id)
const frame = beatFrame(ORDER, {
  l01: { d: D.idle, cut: 'wide', l: Lx.idle },
  l02: { d: D.stunned, dAt: 0.8, cut: 'thermo', cutAt: 1.0 },
  l03: { d: D.sneaky, cut: 'two', l: Lx.whistle },
  l04: { d: D.sneaky, cut: 'thermo', cutAt: 0.6, l: Lx.idle },
  l05: { d: D.stunned, cut: 'thermo' },
  l06: { d: D.sneaky, cut: 'daniTight', l: Lx.idle },
  l07: { l: Lx.smug, cut: 'luciaTight' },
  l08: { d: D.camera, cut: 'two' },
  l09: { l: Lx.whistle, cut: 'lucia', d: D.stare, dAt: 0.3 },
  l10: { d: D.hot, cut: 'thermo', cutAt: 1.2 },
  l11: { l: Lx.shiver, cut: 'luciaTight', d: D.hot },
  l12: { d: D.camera, cut: 'daniTight' },
  l13: { l: Lx.shiver, cut: 'lucia' },
  l14: { d: D.hot, cut: 'dani' },
  l15: { d: D.stunned, cut: 'two', dAt: 0.5 },
  l16: { l: Lx.annoyed, cut: 'luciaTight', d: D.defeated, dAt: 0.4 },
  l17: { d: D.idle, l: Lx.shiver, cut: 'wide' },
}, D.idle, Lx.idle)

const spec: PairSpec = {
  id: 'pareja06',
  script: SCRIPT,
  gap: { l02: 0.6, l03: 0.4, l04: 0.4, l05: 0.6, l06: 0.3, l07: 0.3, l08: 0.5, l09: 0.5, l10: 0.5, l11: 0.4, l12: 0.4, l13: 0.2, l14: 0.4, l15: 0.6, l16: 0.4, l17: 0.8 },
  her: ['l11', 'l16'],
  bg: '#1a1420',
  Set: () => <LivingRoom />,
  pos: { lucia: [-0.42, 0.5, -0.35], dani: [0.42, 0.5, -0.35] },
  shots: { ...coupleShots(1.52, -0.35), thermo: { p: [-0.95, 1.5, 0.05], l: [-0.95, 1.5, -1.03], fov: 30, push: 0.12 } },
  daniHand: null,
  frame: (t, a, l, st) => {
    const f = frame(t, a, l)
    let g = 21
    if (t > a('l02') + 1.2) g = 25
    if (t > a('l04') + 1.4) g = 22
    if (t > a('l05') + 1.0) g = 24
    if (t > a('l06')) g = 21
    if (t > a('l07')) g = 26
    if (t > a('l10') + 1.2) g = 28
    st.temp = `${g}°`
    st.hot = g >= 25 ? 1 : 0
    st.fan = t > a('l14') && t < a('l16')
    if (st.fan) { f.dani.rSh = [1.4, -0.1 + 0.25 * Math.sin(t * 14)]; f.dani.rEl = -1.5 }
    if (t > a('l11') && t < a('l14')) f.lucia.roll += 0.02 * Math.sin(t * 40) // shiver
    st.luciaTop = t > a('l11') - 0.3 ? '#5a6370' : undefined // his grey hoodie
    st.bill = t > a('l15') - 0.2 && t < a('l16')
    return f
  },
  extras: (st) => (
    <group>
      <group position={[-0.95, 1.5, -1.0]} scale={1.5}><Clock text={() => st.temp ?? '21°'} /></group>
      {/* paper fan (the gas bill) in front of Dani's face */}
      <Show show={() => st.fan || st.bill}>
        <mesh position={[0.62, 1.42, 0.0]} rotation={[0, -0.3, 0.2]}>
          <planeGeometry args={[0.2, 0.27]} />
          <meshStandardMaterial color="#f4f1e8" side={2} />
        </mesh>
      </Show>
    </group>
  ),
  sfx: (l) => [
    { type: 'tick', at: l('l02').at + 1.2, g: 0.5 },
    { type: 'tick', at: l('l04').at + 1.4, g: 0.5 },
    { type: 'tick', at: l('l05').at + 1.0, g: 0.5 },
    { type: 'tick', at: l('l06').at, g: 0.5 },
    { type: 'tick', at: l('l07').at, g: 0.5 },
    { type: 'riser', at: l('l08').at, g: 0.3 },
    { type: 'tick', at: l('l10').at + 1.2, g: 0.5 },
    { type: 'hit', at: l('l10').at + 1.25, g: 0.35 },
    { type: 'buzz', at: l('l12').at, g: 0.35 },
    { type: 'paper', at: l('l14').at, g: 0.5 },
    { type: 'scratch', at: l('l16').at + 0.2, g: 0.4 },
  ],
  overlays: (l, dur) => [
    box(l('l05').at, l('l08').at - 0.05, 250, 60, 'GUERRA DEL TERMOSTATO\\N{\\fs50}EN DIRECTO', 8),
    box(l('l08').at, l('l09').at - 0.1, 760, 70, 'GUERRA FRÍA (CALIENTE)'),
    box(l('l10').at + 1.2, l('l11').at - 0.1, 250, 70, 'SEVILLA, AGOSTO', 8),
    box(l('l12').at, l('l14').at - 0.1, 250, 54, 'ELLA: 28° + SUDADERA\\N+ 2 MANTAS + CALCETINES', 8),
    box(l('l15').at + 0.3, l('l16').at - 0.1, 760, 92, 'GAS: 180 €'),
    box(l('l17').at, dur, 250, 70, 'COSAS DE PAREJA\\N{\\fs56}SÍGUENOS PARA EL EP. 7', 8),
  ],
}

export function Pareja06() { return <PairEpisode spec={spec} /> }
