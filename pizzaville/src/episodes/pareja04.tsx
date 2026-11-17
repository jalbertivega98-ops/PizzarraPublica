// COSAS DE PAREJA · EP. 4 — «Los pies fríos». En la cama, antes de dormir.
import { Bedroom, Clock } from './pareja01v2'
import { PairEpisode, box, coupleShots, endOf, flap, pose, track, type PairSpec } from './pareja_kit'

const SCRIPT = [
  { id: 'l01', text: "Por fin en la cama. Calentito. Has tardado veinte minutos en coger la postura perfecta." },
  { id: 'l02', text: "Y entonces lo notas. Bajo las sábanas." },
  { id: 'l03', text: "Dos cubitos de hielo. Sus pies." },
  { id: 'l04', text: "«Ay, perdona, es que tengo los pies helados.»" },
  { id: 'l05', text: "Helados. Esos pies vienen de Siberia." },
  { id: 'l06', text: "«¿Me los calientas un poquito?»" },
  { id: 'l07', text: "Y tú, como eres un caballero, dices que sí." },
  { id: 'l08', text: "Tu cuerpo pierde cinco grados en un segundo." },
  { id: 'l09', text: "«Ay, qué gustito. Buenas noches, amor.»" },
  { id: 'l10', text: "Ella se duerme en dos minutos. Calentita." },
  { id: 'l11', text: "Tú te quedas despierto. Congelado. Y sin manta." },
  { id: 'l12', text: "Etiqueta a la de los pies helados." },
]

const D = {
  cozy: pose({ lids: 0.75, smile: 0.7, roll: -0.1, pitch: 0.06, sink: 0.04 }),
  alert: pose({ lids: 0, brows: 0.7, browTilt: -0.2, yaw: 0.1 }),
  shocked: pose({ lids: 0, brows: 1, browTilt: -0.3, mouth: 0.45, lean: -0.06, sink: -0.06 }),
  toHer: pose({ yaw: -0.5, lids: 0.15, brows: 0.2, browTilt: 0.3, smile: -0.3 }),
  sarcastic: pose({ yaw: -0.1, lids: 0.45, brows: 0.35, browTilt: 0.5, smile: 0.35 }),
  forced: pose({ yaw: -0.45, smile: 0.55, brows: 0.65, browTilt: -0.8, lids: 0.1 }),
  pain: pose({ lids: 0.85, brows: 0.9, browTilt: -1, smile: -0.7, pitch: -0.08, lSh: [0.3, -0.25], lEl: -1.7, rSh: [0.3, 0.25], rEl: -1.7 }),
  awake: pose({ lids: 0, brows: 0.25, browTilt: -0.4, smile: -0.4, lSh: [0.3, -0.25], lEl: -1.7, rSh: [0.3, 0.25], rEl: -1.7 }),
}
const L_ = {
  sleepy: pose({ lids: 0.5, yaw: 0.25, smile: 0.2 }),
  innocent: pose({ yaw: 0.6, brows: 0.7, browTilt: -0.4, smile: 0.5, lids: 0.05, roll: 0.12 }),
  puppy: pose({ yaw: 0.6, brows: 0.9, browTilt: -0.7, smile: 0.25, lean: 0.08, side: 0.1, roll: 0.1 }),
  cuddle: pose({ side: 0.17, roll: 0.25, yaw: 0.4, lids: 0.6, smile: 0.85, lean: 0.08 }),
  asleep: pose({ lids: 1, smile: 0.55, side: 0.2, roll: 0.3, sink: 0.1, yaw: 0.3 }),
}

const spec: PairSpec = {
  id: 'pareja04',
  script: SCRIPT,
  gap: { l02: 0.4, l03: 0.3, l04: 0.6, l05: 0.4, l06: 0.4, l07: 0.4, l08: 0.4, l09: 0.5, l10: 0.6, l11: 0.6, l12: 0.9 },
  her: ['l04', 'l06', 'l09'],
  bg: '#0d1022',
  Set: ({ st }) => <Bedroom lamp={() => st.lamp ?? 1} />,
  pos: { lucia: [-0.42, 0.56, -0.3], dani: [0.42, 0.56, -0.3] },
  shots: { ...coupleShots(1.58, -0.3), feet: { p: [0.2, 1.25, 1.9], l: [0, 0.75, 0.5], fov: 40, push: 0.1 } },
  extras: (st) => <group position={[1.2, 0.665, -0.5]} rotation={[0, -0.35, 0]}><Clock text={() => st.clock ?? '00:30'} /></group>,
  frame: (t, a, l, st) => {
    const dani = track([
      [0, D.cozy], [a('l02') + 0.4, D.alert], [a('l03') - 0.05, D.shocked], [a('l04') + 0.2, D.toHer], [a('l05'), D.sarcastic],
      [a('l06') + 0.3, D.toHer], [a('l07') + l('l07').dur * 0.6, D.forced], [a('l08'), D.pain], [a('l09') + 0.5, D.forced],
      [a('l10') + 0.4, D.pain], [a('l11'), D.awake],
    ], t, 0.2)
    if (t > a('l07') + l('l07').dur * 0.75 && t < endOf(l('l07')) + 0.2) dani.mouth = flap(t)
    // shivering from the moment the feet arrive
    if (t > a('l03')) { const k = t > a('l08') ? 1 : 0.5; dani.side += Math.sin(t * 47) * 0.006 * k; dani.roll += Math.sin(t * 39) * 0.02 * k }
    const lucia = track([
      [0, L_.sleepy], [a('l03') + 0.3, L_.cuddle], [a('l04') - 0.2, L_.innocent], [a('l05') + 0.3, L_.cuddle], [a('l06') - 0.2, L_.puppy],
      [a('l07') + 0.6, L_.cuddle], [a('l10') + 0.4, L_.asleep],
    ], t, 0.35)
    st.lamp = t < endOf(l('l10')) - 0.3 ? 1 : 0
    st.clock = t < a('l10') ? '00:30' : t < a('l11') ? '00:32' : '03:15'
    st.noBlink = t > a('l11')
    return {
      dani, lucia,
      cuts: [
        [0, 'two'], [a('l02') - 0.1, 'daniTight'], [a('l03') - 0.1, 'feet'], [a('l03') + l('l03').dur * 0.45, 'daniTight'],
        [a('l04') - 0.1, 'lucia'], [a('l05') - 0.1, 'daniTight'], [a('l06') - 0.1, 'luciaTight'], [a('l07') - 0.1, 'two'],
        [a('l08') - 0.1, 'daniTight'], [a('l09') - 0.1, 'lucia'], [a('l10') - 0.1, 'two'], [a('l11') - 0.1, 'daniTight'], [a('l12') - 0.1, 'two'],
      ],
    }
  },
  sfx: (l) => [
    { type: 'riser', at: l('l02').at, g: 0.3 },
    { type: 'hit', at: l('l03').at - 0.05, g: 0.45 },
    { type: 'boing', at: l('l03').at + l('l03').dur * 0.5, g: 0.3 },
    { type: 'whoosh', at: l('l08').at - 0.1, g: 0.35 },
    { type: 'tick', at: endOf(l('l10')) - 0.3, g: 0.6 },
  ],
  overlays: (l, dur) => [
    box(l('l03').at + 0.2, l('l04').at - 0.1, 250, 64, 'TEMPERATURA DE SUS PIES\\N{\\fs110}-5 °C', 8),
    box(l('l08').at, endOf(l('l08')) + 0.4, 250, 64, 'TU TEMPERATURA\\N{\\fs96}36,5 → 31,5 °C', 8),
    box(l('l11').at + l('l11').dur * 0.4, l('l12').at - 0.1, 250, 64, 'CALOR\\N{\\fs92}ELLA 10 · TÚ 0', 8),
    box(l('l12').at, dur, 250, 70, 'COSAS DE PAREJA\\N{\\fs56}SÍGUENOS PARA EL EP. 5', 8),
  ],
}

export function Pareja04() { return <PairEpisode spec={spec} /> }
