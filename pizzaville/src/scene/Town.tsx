// The persistent town: every approved/built inhabitant with their house, flag and character.
import { useMemo, useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { Billboard, Text } from '@react-three/drei'
import * as THREE from 'three'
import { useStore, BUILD_SECONDS, type Inhabitant } from '../state/store'
import { House, houseSpecFromSeed, STAGES, timedProgress } from './House'
import { ConstructionSite } from './Construction'
import { Character, lookFromSeed, newState, WORKER_LOOK } from './Character'
import { flagTexture } from './Flag'
import { clock, seg } from '../engine/clock'
import { mat } from './materials'
import { heightAt } from '../world/terrain'

function Lot({ h }: { h: Inhabitant }) {
  const start = useStore((s) => s.builds[h.id])
  const spec = useMemo(() => houseSpecFromSeed(h.house_seed), [h.house_seed])
  const look = useMemo(() => lookFromSeed(h.look_seed), [h.look_seed])
  const built = h.status === 'built'
  const getP = useMemo(() => (built ? () => 1 : start !== undefined ? timedProgress(start, BUILD_SECONDS) : () => 0), [built, start])
  const person = useMemo(newState, [])
  const workers = useMemo(() => [newState(), newState()], [])
  const label = useRef<THREE.Group>(null!)
  const c = Math.cos(h.rot), s = Math.sin(h.rot)
  const local = (lx: number, lz: number): [number, number] => [h.x + lx * c + lz * s, h.z - lx * s + lz * c]

  useFrame(() => {
    const p = getP()
    // the inhabitant: waits on the plot during works, then strolls by the door
    const t = clock.t + h.house_seed % 100
    const [dx, dz] = local(Math.sin(t * 0.21) * 2.2 + (p < 1 ? spec.w / 2 + 2 : 0), spec.d / 2 + 2.2 + Math.sin(t * 0.13) * 0.6)
    person.x = dx; person.z = dz; person.y = heightAt(dx, dz)
    const moving = Math.abs(Math.cos(t * 0.21)) > 0.25
    person.speed = moving ? 1.1 : 0
    person.phase = t * 5.2
    person.ry = h.rot + (Math.cos(t * 0.21) > 0 ? Math.PI / 2 : -Math.PI / 2) * (moving ? 1 : 0)
    person.action = p > 0.9 && p < 1 ? 'celebrate' : 'none'; person.actionT = t; person.actionW = person.action === 'none' ? 0 : 1
    person.visible = p > 0 || built || h.status === 'approved'
    workers.forEach((w, i) => {
      const [wx, wz] = local(i ? -spec.w / 2 - 1 : spec.w / 2 + 1, i ? -1 : 1.5)
      w.x = wx; w.z = wz; w.y = heightAt(wx, wz)
      w.ry = Math.atan2(h.x - wx, h.z - wz)
      w.visible = p > STAGES.materials[0] && p < STAGES.decor[1]
      w.action = 'hammer'; w.actionT = clock.t + i; w.actionW = 1
    })
    label.current.visible = (p >= 1 || built) && !!h.display_name
    label.current.scale.setScalar(Math.max(0.001, seg(p, 0.97, 1)))
  })
  return (
    <group>
      <group position={[h.x, h.y, h.z]} rotation-y={h.rot}>
        <House spec={spec} getProgress={getP} flag={h.country} />
        {!built && <ConstructionSite spec={spec} getProgress={getP} />}
        <group ref={label} position={[0, spec.wallH * spec.floors + 3.6, 0]}>
          <NameTag name={h.display_name ?? ''} iso={h.country} />
        </group>
      </group>
      <Character look={look} state={person} />
      {!built && workers.map((w, i) => <Character key={i} look={WORKER_LOOK(h.house_seed + i)} state={w} scale={0.78} />)}
    </group>
  )
}

export function NameTag({ name, iso }: { name: string; iso: string }) {
  const fm = useMemo(() => new THREE.MeshBasicMaterial({ map: flagTexture(iso), toneMapped: false }), [iso])
  const w = 0.75 + name.length * 0.17
  return (
    <Billboard>
      <mesh position={[0, 0, -0.01]} material={mat('#1a2233', { transparent: true, opacity: 0.78 })}>
        <planeGeometry args={[w, 0.5]} />
      </mesh>
      <mesh position={[-w / 2 + 0.3, 0, 0]} material={fm}>
        <planeGeometry args={[0.4, 0.3]} />
      </mesh>
      <Text font="/fonts/fredoka600.woff" fontSize={0.27} color="#ffffff" anchorX="left" anchorY="middle" position={[-w / 2 + 0.58, 0, 0]}>
        {name}
      </Text>
    </Billboard>
  )
}

export function Town() {
  const data = useStore((s) => s.data)
  const lots = (data?.inhabitants ?? []).filter((h) => (h.status === 'approved' || h.status === 'built') && h.plot_id)
  return <group>{lots.map((h) => <Lot key={h.id} h={h} />)}</group>
}
