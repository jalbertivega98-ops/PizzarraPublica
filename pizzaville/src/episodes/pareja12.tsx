// COSAS DE PAREJA · episodio 1 (nueva etapa) — «Las llaves». En la entrada de casa, de pie. Conversación natural
// (Martín e Inés, un solo audio continuo), sin música ni efectos. Él mueve la boca al hablar, no al murmurar (l08).
import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { RoundedBox } from '@react-three/drei'
import * as THREE from 'three'
import { CONV } from './pareja12_data'
import { Hallway, Mug, PairEpisode, coupleShots, pose, track, type PairSpec } from './pareja_kit'
import { clock } from '../engine/clock'

const fm = (c: string, r = 0.8) => new THREE.MeshStandardMaterial({ color: c, roughness: r, flatShading: true })
const LEATHER = fm('#8c4b2b', 0.6), STRAP = fm('#5a2e1a', 0.6), METAL = fm('#d9d2c2', 0.3), RING = fm('#c9a43a', 0.35), FOB = fm('#2f7f83')

function Bag() {
  // open tote bag: body, dark inside, two straps
  return (
    <group>
      <RoundedBox args={[0.42, 0.26, 0.16]} radius={0.03} smoothness={2} material={LEATHER} castShadow receiveShadow />
      <mesh position={[0, 0.131, 0]} rotation-x={-Math.PI / 2} material={fm('#2a1610')}><planeGeometry args={[0.38, 0.12]} /></mesh>
      {[-0.05, 0.05].map((z) => <mesh key={z} position={[0, 0.13, z]} material={STRAP}><torusGeometry args={[0.12, 0.012, 5, 12, Math.PI]} /></mesh>)}
      <mesh position={[0, 0.02, 0.082]} material={METAL}><boxGeometry args={[0.05, 0.035, 0.01]} /></mesh>
    </group>
  )
}
function Keys() {
  return (
    <group rotation={[0.2, 0.4, 0.3]}>
      <mesh material={RING}><torusGeometry args={[0.03, 0.006, 5, 12]} /></mesh>
      <mesh position={[0.01, -0.06, 0.005]} rotation-z={0.2} material={METAL}><boxGeometry args={[0.018, 0.07, 0.004]} /></mesh>
      <mesh position={[-0.03, -0.055, 0]} rotation-z={-0.4} material={METAL}><boxGeometry args={[0.018, 0.065, 0.004]} /></mesh>
      <mesh position={[0.03, 0.035, 0]} material={FOB}><boxGeometry args={[0.035, 0.05, 0.015]} /></mesh>
    </group>
  )
}

/** the keys come up out of the bag, held between two fingers */
function RisingKeys({ t0 }: { t0: number }) {
  const g = useRef<THREE.Group>(null!)
  useFrame(() => {
    const k = Math.min(1, Math.max(0, (clock.t - t0) / 0.9))
    const e = k * k * (3 - 2 * k)
    g.current.visible = clock.t > t0
    g.current.position.set(0.02, 0.05 + e * 0.2, 0.01)
    g.current.rotation.z = Math.sin(clock.t * 3.1) * 0.12 * e
  })
  return <group ref={g}><Keys /></group>
}

const at = Object.fromEntries(CONV.map((c) => [c.id, c.at]))
const LX = -0.42, Z = 0.2, HY = 1.66

// arms: she holds the open bag in front of her (right hand) and digs in it (left hand)
const bagArms = { lSh: [0.7, 0.05] as [number, number], lEl: -0.9, rSh: [0.6, -0.05] as [number, number], rEl: -0.95 }
const mugArms = { rSh: [0.55, -0.05] as [number, number], rEl: -1.75, lSh: [0.2, 0.18] as [number, number], lEl: -0.5 }
const D = {
  sip: pose({ yaw: -0.1, lids: 0.3, smile: 0.1, ...mugArms, rSh: [0.85, -0.05], rEl: -2.0, pitch: -0.05 }),
  flat: pose({ yaw: -0.35, lids: 0.4, brows: 0.05, smile: 0, ...mugArms }),
  smug: pose({ yaw: -0.3, lids: 0.35, brows: 0.35, browTilt: 0.25, smile: 0.5, roll: 0.05, ...mugArms }),
  shrug: pose({ yaw: -0.35, lids: 0.2, brows: 0.6, browTilt: -0.2, smile: 0.2, ...mugArms, lSh: [0.5, 0.55], lEl: -1.2 }),
  turn: pose({ yaw: -0.5, lids: 0.15, brows: 0.35, ...mugArms }),
  mock: pose({ yaw: 0.35, pitch: 0.06, roll: 0.14, lids: 0.55, brows: 0.75, browTilt: -0.5, smile: 0.3, ...mugArms }),
  caught: pose({ yaw: -0.5, lids: 0, brows: 1, browTilt: -0.2, smile: -0.1, lean: -0.04, ...mugArms }),
  innocent: pose({ yaw: -0.45, lids: 0.05, brows: 0.7, browTilt: -0.6, smile: 0.7, ...mugArms }),
  look: pose({ yaw: -0.45, lids: 0.3, brows: 0.2, smile: -0.05, ...mugArms }),
  deadpan: pose({ yaw: 0, lids: 0.5, brows: 0.05, smile: -0.15, ...mugArms }),
}
const L_ = {
  search: pose({ yaw: 0.05, pitch: 0.4, lids: 0.15, brows: 0.35, browTilt: -0.35, smile: -0.1, ...bagArms }),
  ask: pose({ yaw: 0.45, pitch: 0.05, lids: 0.05, brows: 0.5, ...bagArms }),
  no: pose({ yaw: 0.5, lids: 0.25, brows: 0.1, browTilt: 0.3, smile: -0.3, ...bagArms }),
  unamused: pose({ yaw: 0.55, lids: 0.55, brows: -0.2, browTilt: 0.6, smile: -0.4, ...bagArms }),
  obvious: pose({ yaw: 0.5, pitch: -0.08, lids: 0.4, brows: 0.6, browTilt: 0.1, smile: -0.25, roll: -0.1, ...bagArms }),
  sharp: pose({ yaw: 0.65, lids: 0, brows: -0.4, browTilt: 1, smile: -0.5, lean: 0.05, ...bagArms }),
  stare: pose({ yaw: 0.6, lids: 0.35, brows: -0.3, browTilt: 0.8, smile: -0.35, ...bagArms }),
  find: pose({ yaw: 0.05, pitch: 0.35, lids: 0, brows: 0.9, browTilt: -0.4, smile: 0, ...bagArms }),
  keys: pose({ yaw: 0.3, pitch: 0.08, lids: 0.4, brows: 0.5, browTilt: -0.7, smile: 0.2, ...bagArms }),
}

const shots = {
  ...coupleShots(HY, Z),
  two: { p: [0, HY + 0.15, Z + 3.0] as [number, number, number], l: [0, HY - 0.4, Z] as [number, number, number], fov: 44, push: 0.2 },
  lucia: { p: [-0.12, HY + 0.05, Z + 2.3] as [number, number, number], l: [LX, HY - 0.22, Z] as [number, number, number], fov: 38, push: 0.12 },
  dani: { p: [0.12, HY + 0.05, Z + 2.3] as [number, number, number], l: [0.42, HY - 0.22, Z] as [number, number, number], fov: 38, push: 0.12 },
  wide: { p: [0.35, 1.75, 3.7] as [number, number, number], l: [-0.25, 1.15, -0.6] as [number, number, number], fov: 50, push: 0.3 },
  bowl: { p: [0.6, 1.3, -0.3] as [number, number, number], l: [0.47, 0.86, -0.83] as [number, number, number], fov: 36, push: 0.06 },
  bag: { p: [LX + 0.3, 1.5, Z + 1.25] as [number, number, number], l: [LX + 0.08, 1.02, Z + 0.38] as [number, number, number], fov: 36, push: 0.1 },
  daniClose: { p: [0.3, HY + 0.02, Z + 1.9] as [number, number, number], l: [0.42, HY - 0.12, Z] as [number, number, number], fov: 36, push: 0.1 },
}

const spec: PairSpec = {
  id: 'pareja12',
  script: CONV.map((c) => ({ id: c.id, text: c.text })),
  fixedAt: at,
  gap: {},
  her: CONV.filter((c) => c.her).map((c) => c.id),
  talk: true,
  quiet: ['l08'],
  legs: { lucia: { pants: '#3b3550', shoes: '#2a1d1a' }, dani: { pants: '#2b3a5c', shoes: '#e8e2d8' } },
  ry: { lucia: 0.25, dani: -0.25 },
  bg: '#1a1420',
  tail: 1.8,
  keyColor: '&H8A6A1E&',
  Set: ({ st }) => {
    st.luciaTop = '#c98b3a'
    return (
      <group>
        <Hallway />
        {/* the open bag she holds in front of her */}
        <group position={[LX + 0.08, 1.0, Z + 0.38]} rotation={[0.15, 0.25, 0]}>
          <Bag />
          <RisingKeys t0={at.l11 - 0.45} />
        </group>
      </group>
    )
  },
  pos: { lucia: [LX, 0.62, Z], dani: [0.42, 0.62, Z] },
  shots,
  daniHand: <Mug color="#2f7f83" />,
  frame: (t, a, l) => {
    const dani = track([
      [0, D.sip], [a('l02') - 0.2, D.flat], [a('l04') + 0.3, D.smug], [a('l04') + 1.4, D.shrug], [a('l05') + 0.5, D.flat], [a('l06') - 0.2, D.turn],
      [a('l07') + 0.4, D.look], [a('l08') - 0.15, D.mock], [a('l09') + 0.05, D.caught], [a('l10') + 0.35, D.innocent],
      [a('l11') - 0.3, D.look], [a('l11') + 1.0, D.deadpan],
    ], t, 0.22)
    const lucia = track([
      [0, L_.search], [a('l01') + 0.1, L_.ask], [a('l02') + 0.6, L_.search], [a('l03') - 0.1, L_.no], [a('l04') + 0.5, L_.unamused],
      [a('l06') + 0.4, L_.search], [a('l07') - 0.1, L_.obvious], [a('l08') + 0.3, L_.search], [a('l09') - 0.15, L_.sharp], [a('l10') + 0.4, L_.stare],
      [a('l11') - 0.5, L_.find], [a('l11') + 0.35, L_.keys],
    ], t, 0.25)
    // digging in the bag while she searches
    if (t < a('l09') - 0.2 || (t > a('l11') - 0.5 && t < a('l11') + 0.35)) {
      const k = Math.sin(t * 6.1) * 0.1
      lucia.lSh = [lucia.lSh[0] + k, lucia.lSh[1]]; lucia.lEl += k * 0.6
    }
    return {
      dani, lucia,
      cuts: [
        [0, 'wide'], [a('l02') - 0.08, 'dani'], [a('l02') + 0.55, 'bowl'], [a('l03') - 0.08, 'lucia'], [a('l04') - 0.08, 'dani'], [a('l05') - 0.08, 'lucia'],
        [a('l06') - 0.08, 'two'], [a('l07') - 0.08, 'lucia'], [a('l07') + l('l07').dur * 0.5, 'bag'], [a('l08') - 0.1, 'daniClose'],
        [a('l09') - 0.1, 'lucia'], [a('l10') - 0.08, 'dani'], [a('l11') - 0.55, 'bag'],
        [a('l12') - 0.1, 'dani'],
      ],
    }
  },
  sfx: () => [],
  overlays: () => [],
}

export function Pareja12() { return <PairEpisode spec={spec} /> }
