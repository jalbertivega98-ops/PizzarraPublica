// COSAS DE PAREJA · EP. 2 — «¿Qué te pasa? Nada». Sofá, viendo una serie.
import { LivingRoom, PairEpisode, box, coupleShots, endOf, flap, pose, track, type PairSpec } from './pareja_kit'

const SCRIPT = [
  { id: 'l01', text: "Estáis en el sofá viendo una serie. Todo tranquilo." },
  { id: 'l02', text: "Hasta que notas que lleva diez minutos sin decir nada." },
  { id: 'l03', text: "Le preguntas qué le pasa." },
  { id: 'l04', text: "«Nada.»" },
  { id: 'l05', text: "Nada. Ese «nada» pesa más que tu hipoteca." },
  { id: 'l06', text: "Le preguntas si ha pasado algo." },
  { id: 'l07', text: "«Que no me pasa nada. Ya está.»" },
  { id: 'l08', text: "Repasas la última semana. Aniversario no es. Cumpleaños tampoco." },
  { id: 'l09', text: "«Tú sabrás lo que has hecho.»" },
  { id: 'l10', text: "No sabes lo que has hecho. Pero ya estás pidiendo perdón." },
  { id: 'l11', text: "«Ah, por cierto. Mañana viene mi madre a comer.»" },
  { id: 'l12', text: "Ahí estaba." },
  { id: 'l13', text: "Etiqueta a la que dice «nada» cuando es todo." },
]

const D = {
  watch: pose({ lids: 0.2, smile: 0.25 }),
  glance: pose({ yaw: -0.35, brows: 0.3, lids: 0.1 }),
  ask: pose({ yaw: -0.5, brows: 0.5, browTilt: -0.3, lSh: [0.6, 0.3], lEl: -1.1 }),
  worried: pose({ yaw: -0.3, brows: 0.8, browTilt: -0.9, lids: 0 }),
  think: pose({ yaw: 0.25, pitch: -0.15, brows: 0.5, browTilt: -0.6, lSh: [1.25, 0.25], lEl: -1.75 }),
  panic: pose({ yaw: -0.5, brows: 1, browTilt: -1, lids: 0, mouth: 0.3, lean: -0.04 }),
  sorry: pose({ lids: 0.35, yaw: -0.4, pitch: 0.15, brows: 0.6, browTilt: -1, lSh: [0.9, -0.12], lEl: -1.2, rSh: [0.9, 0.12], rEl: -1.2 }),
  defeated: pose({ pitch: 0.25, lids: 0.6, brows: 0.4, browTilt: -0.8, sink: 0.07, smile: -0.4, roll: -0.06 }),
}
const L_ = {
  watch: pose({ smile: 0.15 }),
  cold: pose({ yaw: -0.3, pitch: -0.12, brows: -0.2, browTilt: 0.7, lids: 0.35, smile: -0.4 }),
  coldSide: pose({ yaw: 0.15, pitch: -0.1, brows: -0.25, browTilt: 0.8, lids: 0.4, smile: -0.4 }),
  stare: pose({ yaw: 0.55, brows: -0.3, browTilt: 1, lids: 0.2, lean: 0.06 }),
  sweet: pose({ yaw: 0.55, brows: 0.6, browTilt: -0.3, smile: 0.9, lids: 0, roll: 0.12, lean: 0.05 }),
  happy: pose({ yaw: 0.1, smile: 0.8, brows: 0.3 }),
}

const spec: PairSpec = {
  id: 'pareja02',
  script: SCRIPT,
  gap: { l02: 0.3, l03: 0.5, l04: 0.6, l05: 0.5, l06: 0.4, l07: 0.4, l08: 0.5, l09: 0.5, l10: 0.4, l11: 0.8, l12: 0.6, l13: 0.9 },
  her: ['l04', 'l07', 'l09', 'l11'],
  bg: '#1a1420',
  Set: () => <LivingRoom />,
  pos: { lucia: [-0.42, 0.5, -0.35], dani: [0.42, 0.5, -0.35] },
  shots: coupleShots(1.52, -0.35),
  frame: (t, a, l, st) => {
    const dani = track([
      [0, D.watch], [a('l02') + 0.5, D.glance], [a('l03'), D.ask], [a('l04') + 0.3, D.glance], [a('l05'), D.worried],
      [a('l06'), D.ask], [a('l07') + 0.4, D.worried], [a('l08'), D.think], [a('l09') + 0.3, D.panic], [a('l10') + 0.9, D.sorry],
      [a('l11') + 0.3, D.glance], [a('l12') - 0.1, D.defeated],
    ], t)
    if ((t > a('l03') + 0.2 && t < endOf(l('l03'))) || (t > a('l06') + 0.2 && t < endOf(l('l06'))) || (t > a('l10') + 0.8 && t < endOf(l('l10')) + 0.3)) dani.mouth = flap(t)
    if (t > a('l08') && t < a('l09')) dani.yaw += Math.sin(t * 1.8) * 0.18 // looking around, thinking
    const lucia = track([
      [0, L_.watch], [a('l02'), L_.cold], [a('l04') - 0.2, L_.coldSide], [a('l05') + 0.2, L_.cold], [a('l07') - 0.2, L_.stare],
      [a('l08'), L_.cold], [a('l09') - 0.2, L_.stare], [a('l10') + 0.5, L_.cold], [a('l11') - 0.2, L_.sweet], [a('l12') + 0.6, L_.happy],
    ], t, 0.35)
    st.noBlink = t > a('l09') && t < a('l10') + 0.6
    return {
      dani, lucia,
      cuts: [
        [0, 'wide'], [a('l02') - 0.1, 'luciaTight'], [a('l03') - 0.1, 'two'], [a('l04') - 0.15, 'luciaTight'], [a('l05') - 0.1, 'daniTight'],
        [a('l06') - 0.1, 'two'], [a('l07') - 0.1, 'lucia'], [a('l08') - 0.1, 'daniTight'], [a('l09') - 0.1, 'luciaTight'],
        [a('l10') - 0.1, 'dani'], [a('l11') - 0.1, 'lucia'], [a('l12') - 0.1, 'daniTight'], [a('l13') - 0.1, 'two'],
      ],
    }
  },
  sfx: (l) => [
    { type: 'hit', at: l('l04').at - 0.05, g: 0.4 },
    { type: 'tick', at: l('l08').at + 0.2, g: 0.5 }, { type: 'tick', at: l('l08').at + 0.9, g: 0.5 }, { type: 'tick', at: l('l08').at + 1.6, g: 0.5 },
    { type: 'whoosh', at: l('l10').at - 0.2, g: 0.35 },
    { type: 'scratch', at: l('l11').at - 0.3, g: 0.45 },
    { type: 'hit', at: l('l12').at - 0.05, g: 0.4 },
  ],
  overlays: (l, dur) => [
    box(l('l05').at + 0.6, endOf(l('l05')) + 0.3, 250, 64, 'NIVEL DE PELIGRO\\N{\\fs92}MÁXIMO', 8),
    box(l('l08').at, endOf(l('l08')) + 0.2, 250, 80, 'MODO DETECTIVE', 8),
    box(l('l12').at + 0.3, l('l13').at - 0.1, 250, 64, 'TRADUCCIÓN\\N{\\fs92}«NADA» = TODO', 8),
    box(l('l13').at, dur, 250, 70, 'COSAS DE PAREJA\\N{\\fs56}SÍGUENOS PARA EL EP. 3', 8),
  ],
}

export function Pareja02() { return <PairEpisode spec={spec} /> }
