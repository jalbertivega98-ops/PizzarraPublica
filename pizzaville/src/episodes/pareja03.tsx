// COSAS DE PAREJA · EP. 3 — «¿Dónde cenamos? Me da igual». Sofá, ella con el móvil.
import { LivingRoom, PairEpisode, Phone, box, coupleShots, endOf, flap, pose, track, type PairSpec } from './pareja_kit'

const SCRIPT = [
  { id: 'l01', text: "Viernes por la noche. Le preguntas qué le apetece cenar." },
  { id: 'l02', text: "«Me da igual, lo que tú quieras.»" },
  { id: 'l03', text: "Perfecto. Propones pizza." },
  { id: 'l04', text: "«Uf, pizza no, que la comimos el martes.»" },
  { id: 'l05', text: "Vale. ¿Un japonés?" },
  { id: 'l06', text: "«Mmm... no me apetece nada crudo.»" },
  { id: 'l07', text: "¿Hamburguesa?" },
  { id: 'l08', text: "«¿Otra vez? Siempre lo mismo contigo.»" },
  { id: 'l09', text: "Cuarenta minutos después, sigues con hambre y sin ideas." },
  { id: 'l10', text: "«¡Ya sé! ¿Pedimos pizza?»" },
  { id: 'l11', text: "Pizza. La del martes." },
  { id: 'l12', text: "Etiqueta a la que «le da igual» pero nunca le da igual." },
]

const PH = { rSh: [0.95, -0.15] as [number, number], rEl: -1.35 } // phone held in front of the chest
const D = {
  bored: pose({ lids: 0.35, yaw: 0.05, smile: -0.1 }),
  ask: pose({ yaw: -0.45, brows: 0.35, lids: 0.1 }),
  hopeful: pose({ yaw: -0.45, brows: 0.6, smile: 0.6, lids: 0, lSh: [0.7, 0.3], lEl: -1.1 }),
  trying: pose({ yaw: -0.45, brows: 0.45, browTilt: -0.3, smile: 0.25, lSh: [0.85, 0.35], lEl: -1.0 }),
  tired: pose({ yaw: -0.3, lids: 0.5, brows: 0.25, browTilt: -0.5, smile: -0.2 }),
  slump: pose({ sink: 0.1, pitch: 0.22, lids: 0.6, yaw: 0, brows: 0.3, browTilt: -0.7, roll: -0.08, smile: -0.4 }),
  stunned: pose({ yaw: -0.5, lids: 0, brows: 1, browTilt: -0.2, mouth: 0.3 }),
  stare: pose({ yaw: 0, lids: 0, brows: 0.2, smile: -0.3 }),
}
const L_ = {
  phone: pose({ ...PH, pitch: 0.28, yaw: 0.05, brows: 0.1 }),
  carefree: pose({ ...PH, yaw: 0.45, smile: 0.55, brows: 0.35, pitch: 0.05 }),
  disgust: pose({ ...PH, yaw: 0.45, smile: -0.7, brows: -0.15, browTilt: 0.4, lids: 0.35, roll: -0.12 }),
  meh: pose({ ...PH, yaw: 0.3, smile: -0.35, lids: 0.45, brows: 0.1, roll: 0.08 }),
  annoyed: pose({ ...PH, yaw: 0.55, browTilt: 1, brows: -0.3, lean: 0.08, smile: -0.3 }),
  excited: pose({ yaw: 0.55, brows: 0.9, smile: 1, lids: 0, rSh: [1.6, -0.3], rEl: -0.5, lean: 0.06 }),
}

const spec: PairSpec = {
  id: 'pareja03',
  script: SCRIPT,
  gap: { l02: 0.4, l03: 0.4, l04: 0.4, l05: 0.4, l06: 0.4, l07: 0.4, l08: 0.3, l09: 0.9, l10: 0.6, l11: 0.7, l12: 0.9 },
  her: ['l02', 'l04', 'l06', 'l08', 'l10'],
  bg: '#1a1420',
  Set: () => <LivingRoom />,
  pos: { lucia: [-0.42, 0.5, -0.35], dani: [0.42, 0.5, -0.35] },
  shots: coupleShots(1.52, -0.35),
  luciaHand: <Phone />,
  frame: (t, a, l, st) => {
    const dani = track([
      [0, D.bored], [a('l01') + 1.2, D.ask], [a('l02') + 0.3, D.ask], [a('l03'), D.hopeful], [a('l04') + 0.5, D.tired],
      [a('l05'), D.trying], [a('l06') + 0.4, D.tired], [a('l07'), D.trying], [a('l08') + 0.4, D.tired], [a('l09'), D.slump],
      [a('l10') + 0.3, D.stunned], [a('l11') + l('l11').dur * 0.5, D.stare],
    ], t)
    for (const id of ['l01', 'l03', 'l05', 'l07']) if (t > a(id) + l(id).dur * 0.55 && t < endOf(l(id)) + 0.2) dani.mouth = flap(t)
    const lucia = track([
      [0, L_.phone], [a('l02') - 0.2, L_.carefree], [a('l03') + 0.4, L_.phone], [a('l04') - 0.2, L_.disgust], [a('l05') + 0.4, L_.phone],
      [a('l06') - 0.2, L_.meh], [a('l07') + 0.3, L_.phone], [a('l08') - 0.2, L_.annoyed], [a('l09') + 0.3, L_.phone],
      [a('l10') - 0.2, L_.excited], [a('l11') + 0.5, L_.carefree],
    ], t, 0.3)
    st.noBlink = t > a('l11')
    return {
      dani, lucia,
      cuts: [
        [0, 'wide'], [a('l02') - 0.1, 'luciaTight'], [a('l03') - 0.1, 'daniTight'], [a('l04') - 0.1, 'lucia'], [a('l05') - 0.1, 'dani'],
        [a('l06') - 0.1, 'luciaTight'], [a('l07') - 0.1, 'daniTight'], [a('l08') - 0.1, 'lucia'], [a('l09') - 0.5, 'wide'],
        [a('l10') - 0.1, 'luciaTight'], [a('l11') - 0.1, 'daniTight'], [a('l12') - 0.1, 'two'],
      ],
    }
  },
  sfx: (l) => [
    { type: 'buzz', at: l('l04').at - 0.1, g: 0.4 },
    { type: 'buzz', at: l('l06').at - 0.1, g: 0.4 },
    { type: 'buzz', at: l('l08').at - 0.1, g: 0.4 },
    { type: 'whoosh', at: l('l09').at - 0.5, g: 0.35 },
    { type: 'ding', at: l('l10').at - 0.1, g: 0.45 },
    { type: 'scratch', at: l('l11').at - 0.2, g: 0.45 },
  ],
  overlays: (l, dur) => {
    const n = (k: number) => `PROPUESTAS RECHAZADAS\\N{\\fs110}${k}`
    return [
      box(l('l04').at, l('l06').at - 0.05, 250, 56, n(1), 8),
      box(l('l06').at, l('l08').at - 0.05, 250, 56, n(2), 8),
      box(l('l08').at, l('l09').at - 0.6, 250, 56, n(3), 8),
      box(l('l09').at - 0.6, l('l09').at + 1.4, 760, 96, '40 MINUTOS DESPUÉS'),
      box(l('l11').at + 0.4, l('l12').at - 0.1, 250, 64, 'PROPUESTA GANADORA\\N{\\fs92}LA TUYA (HACE 40 MIN)', 8),
      box(l('l12').at, dur, 250, 70, 'COSAS DE PAREJA\\N{\\fs56}SÍGUENOS PARA EL EP. 4', 8),
    ]
  },
}

export function Pareja03() { return <PairEpisode spec={spec} /> }
