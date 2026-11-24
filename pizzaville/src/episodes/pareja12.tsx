// COSAS DE PAREJA · prueba 12 — «Las llaves». Conversación natural (Martín e Inés, un solo audio continuo):
// sin música ni efectos, cortes cortos, primeros planos e insertos del bolso, una imitación sin cambiar la voz.
import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { RoundedBox } from '@react-three/drei'
import * as THREE from 'three'
import { CONV } from './pareja12_data'
import { LivingRoom, PairEpisode, coupleShots, pose, track, type PairSpec } from './pareja_kit'
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
const LX = -0.42, Z = -0.35

const D = {
  tv: pose({ yaw: 0.05, lids: 0.35, smile: 0.05 }),
  flat: pose({ yaw: -0.2, lids: 0.4, brows: 0.05, smile: 0 }),
  smug: pose({ yaw: -0.3, lids: 0.35, brows: 0.25, browTilt: 0.2, smile: 0.35 }),
  turn: pose({ yaw: -0.5, lids: 0.15, brows: 0.3 }),
  mock: pose({ yaw: 0.25, pitch: -0.05, roll: 0.12, lids: 0.45, brows: 0.6, browTilt: -0.3, smile: 0.2 }),
  caught: pose({ yaw: -0.45, lids: 0, brows: 0.8, browTilt: -0.2, smile: 0 }),
  innocent: pose({ yaw: -0.45, lids: 0.1, brows: 0.55, browTilt: -0.5, smile: 0.55 }),
  look: pose({ yaw: -0.5, lids: 0.3, brows: 0.15, smile: -0.05 }),
  deadpan: pose({ yaw: 0, lids: 0.45, brows: 0.05, smile: -0.1 }),
}
const dig = { lSh: [0.75, 0.05] as [number, number], lEl: -0.95, rSh: [0.75, -0.05] as [number, number], rEl: -0.95 }
const L_ = {
  search: pose({ yaw: 0.1, pitch: 0.35, lids: 0.2, brows: 0.3, browTilt: -0.3, ...dig }),
  ask: pose({ yaw: 0.45, pitch: 0.05, lids: 0.05, brows: 0.35, ...dig }),
  no: pose({ yaw: 0.5, lids: 0.25, brows: 0.1, browTilt: 0.2, smile: -0.25, ...dig }),
  unamused: pose({ yaw: 0.55, lids: 0.5, brows: -0.1, browTilt: 0.5, smile: -0.35, ...dig }),
  obvious: pose({ yaw: 0.5, pitch: -0.05, lids: 0.35, brows: 0.5, browTilt: 0.1, smile: -0.2, roll: -0.08, ...dig }),
  sharp: pose({ yaw: 0.6, lids: 0, brows: -0.3, browTilt: 0.9, smile: -0.4, lean: 0.04 }),
  stare: pose({ yaw: 0.55, lids: 0.3, brows: -0.2, browTilt: 0.7, smile: -0.3 }),
  find: pose({ yaw: 0.05, pitch: 0.3, lids: 0.15, brows: 0.8, browTilt: -0.4, smile: 0, ...dig }),
  keys: pose({ yaw: 0.35, pitch: 0.1, lids: 0.35, brows: 0.4, browTilt: -0.6, smile: 0.15, lSh: [0.6, 0.05], lEl: -0.9, rSh: [1.25, -0.15], rEl: -1.35 }),
}

const shots = {
  ...coupleShots(1.52, Z),
  bag: { p: [LX + 0.22, 1.38, 0.85] as [number, number, number], l: [LX, 0.9, -0.02] as [number, number, number], fov: 38, push: 0.12 },
  keys: { p: [LX + 0.15, 1.3, 0.75] as [number, number, number], l: [LX + 0.02, 1.02, -0.02] as [number, number, number], fov: 34, push: 0.1 },
  daniClose: { p: [0.25, 1.62, Z + 1.75] as [number, number, number], l: [0.42, 1.48, Z] as [number, number, number], fov: 36, push: 0.1 },
}

const spec: PairSpec = {
  id: 'pareja12',
  script: CONV.map((c) => ({ id: c.id, text: c.text })),
  fixedAt: at,
  gap: {},
  her: CONV.filter((c) => c.her).map((c) => c.id),
  bg: '#1a1420',
  tail: 1.8,
  keyColor: '&H8A6A1E&',
  Set: () => (
    <group>
      <LivingRoom tv={() => 0.6} />
      <group position={[LX + 0.02, 0.88, -0.02]} rotation={[-0.1, 0.15, 0]}>
        <Bag />
        <RisingKeys t0={at.l11 - 0.45} />
      </group>
    </group>
  ),
  pos: { lucia: [LX, 0.5, Z], dani: [0.42, 0.5, Z] },
  shots,
  frame: (t, a, l) => {
    const dani = track([
      [0, D.tv], [a('l02') - 0.1, D.flat], [a('l04') + 0.3, D.smug], [a('l05') + 0.5, D.flat], [a('l06') - 0.2, D.turn],
      [a('l07') + 0.4, D.look], [a('l08') - 0.15, D.mock], [a('l09') + 0.05, D.caught], [a('l10') + 0.35, D.innocent],
      [a('l11') - 0.9, D.look], [a('l11') + 1.0, D.deadpan],
    ], t, 0.22)
    const lucia = track([
      [0, L_.search], [a('l01') + 0.1, L_.ask], [a('l02') + 0.6, L_.search], [a('l03') - 0.1, L_.no], [a('l04') + 0.5, L_.unamused],
      [a('l06') + 0.4, L_.search], [a('l07') - 0.1, L_.obvious], [a('l08') + 0.3, L_.search], [a('l09') - 0.15, L_.sharp], [a('l10') + 0.4, L_.stare],
      [a('l11') - 0.5, L_.find], [a('l11') + 0.35, L_.keys],
    ], t, 0.25)
    // rummaging in the bag while she searches
    if ((t < a('l09') - 0.2 || (t > a('l11') - 0.5 && t < a('l11') + 0.35))) {
      const k = Math.sin(t * 6.1) * 0.08
      lucia.lSh = [lucia.lSh[0] + k, lucia.lSh[1]]; lucia.rSh = [lucia.rSh[0] - k, lucia.rSh[1]]
    }
    return {
      dani, lucia,
      cuts: [
        [0, 'two'], [a('l02') - 0.08, 'dani'], [a('l03') - 0.08, 'lucia'], [a('l04') - 0.08, 'dani'], [a('l05') - 0.08, 'lucia'],
        [a('l06') - 0.08, 'two'], [a('l07') - 0.08, 'lucia'], [a('l07') + l('l07').dur * 0.45, 'bag'], [a('l08') - 0.1, 'daniClose'],
        [a('l09') - 0.1, 'lucia'], [a('l10') - 0.08, 'dani'], [a('l11') - 0.55, 'keys'],
        [a('l12') - 0.1, 'dani'],
      ],
    }
  },
  sfx: () => [],
  overlays: () => [],
}

export function Pareja12() { return <PairEpisode spec={spec} /> }
