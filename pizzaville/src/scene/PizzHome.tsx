import { useMemo } from 'react'
import * as THREE from 'three'
import { Text } from '@react-three/drei'
import { House, PIZZ_SPEC, Mailbox } from './House'
import { mat } from './materials'
import { heightAt, HOME_PATH } from '../world/terrain'
import { SIGN_POS } from '../world/plots'
import { holdReady } from '../engine/clock'
import { blob, merge, paint, rockGeo, T } from './geom'
import { mulberry32 } from '../world/rng'
import { Smoke } from './Ambient'

export const HOME_Y = heightAt(0, 0) - 0.05

function heroTree() {
  const parts: THREE.BufferGeometry[] = []
  const trunk = new THREE.CylinderGeometry(0.22, 0.42, 3.2, 9)
  parts.push(paint(T(trunk, 0, 1.6, 0), '#6e4c33', { jitter: 0.06 }))
  parts.push(paint(T(new THREE.CylinderGeometry(0.09, 0.18, 1.9, 6), 0.6, 3.1, 0.1, 0, 0, -0.75), '#6e4c33'))
  parts.push(paint(T(new THREE.CylinderGeometry(0.08, 0.16, 1.7, 6), -0.55, 3.2, -0.2, 0.2, 0, 0.8), '#6e4c33'))
  const r = mulberry32(17)
  const blobs = [[0, 4.6, 0, 2.2], [1.4, 4.1, 0.3, 1.6], [-1.3, 4.3, -0.2, 1.7], [0.3, 5.6, -0.4, 1.6], [-0.4, 4.0, 1.2, 1.4], [0.6, 4.2, -1.3, 1.4], [-0.9, 5.3, 0.6, 1.2]]
  blobs.forEach(([x, y, z, rad], i) => parts.push(paint(T(blob(rad, 2, 0.14, 40 + i), x, y, z), new THREE.Color('#5fa040').offsetHSL(0, 0, (r() - 0.5) * 0.08), { ao: [2.6, 7.2, 0.5], jitter: 0.05, seed: i })))
  // a few apples
  for (let i = 0; i < 9; i++) {
    const a = r() * 6.28, el = r() * 1.2 - 0.3
    parts.push(paint(T(new THREE.SphereGeometry(0.09, 8, 6), Math.cos(a) * 2.0 * Math.cos(el), 4.6 + Math.sin(el) * 1.8, Math.sin(a) * 2.0 * Math.cos(el)), '#d8423a'))
  }
  return merge(parts)
}

function fenceGeo() {
  const parts: THREE.BufferGeometry[] = []
  const add = (x0: number, z0: number, x1: number, z1: number) => {
    const len = Math.hypot(x1 - x0, z1 - z0)
    const n = Math.max(2, Math.round(len / 0.45))
    const ang = Math.atan2(x1 - x0, z1 - z0)
    for (let i = 0; i <= n; i++) {
      const x = x0 + (x1 - x0) * (i / n), z = z0 + (z1 - z0) * (i / n)
      const picket = new THREE.BoxGeometry(0.09, 0.75, 0.04)
      T(picket, 0, 0.375, 0)
      const tip = new THREE.ConeGeometry(0.065, 0.12, 4)
      T(tip, 0, 0.8, 0, 0, Math.PI / 4, 0)
      const g = merge([paint(picket, '#fbf7ee'), paint(tip, '#fbf7ee')])
      T(g, x, 0, z, 0, ang + Math.PI / 2, 0)
      parts.push(g)
    }
    for (const y of [0.25, 0.55]) {
      const rail = new THREE.BoxGeometry(0.05, 0.07, len)
      T(rail, (x0 + x1) / 2, y, (z0 + z1) / 2, 0, ang, 0)
      parts.push(paint(rail, '#efe9dc'))
    }
  }
  // front garden fence with a gap for the path
  add(-5.2, 3.2, -5.2, 8.6); add(-5.2, 8.6, -1.1, 8.6); add(1.1, 8.6, 5.2, 8.6); add(5.2, 8.6, 5.2, 3.2)
  return merge(parts)
}

function gardenBeds() {
  const parts: THREE.BufferGeometry[] = []
  const r = mulberry32(3)
  const cols = ['#f05a7e', '#ffd04a', '#ffffff', '#b38be8', '#ff8a4b']
  for (const [cx, cz] of [[-3.3, 5.2], [3.3, 5.2], [-3.6, 7.4], [3.6, 7.4]]) {
    parts.push(paint(T(new THREE.CylinderGeometry(1.0, 1.1, 0.16, 18), cx, 0.05, cz, 0, 0, 0, [1.25, 1, 0.75]), '#6b4a33'))
    for (let i = 0; i < 16; i++) {
      const a = r() * 6.28, d = Math.sqrt(r()) * 0.95
      const x = cx + Math.cos(a) * d * 1.2, z = cz + Math.sin(a) * d * 0.7
      parts.push(paint(T(blob(0.11, 1, 0.2, i), x, 0.2 + r() * 0.08, z), '#4f8f3a'))
      parts.push(paint(T(new THREE.SphereGeometry(0.07, 7, 5), x + 0.03, 0.32 + r() * 0.1, z), cols[Math.floor(r() * cols.length)]))
    }
  }
  return merge(parts)
}

function stepStones() {
  const parts: THREE.BufferGeometry[] = []
  const r = mulberry32(8)
  for (let s = 1.2; s < HOME_PATH.length - 1; s += 0.85) {
    const p = HOME_PATH.at(s)
    const x = p.x + (r() - 0.5) * 0.25, z = p.z
    const g = paint(rockGeo(0.3, s * 3), '#c9c1b2', { jitter: 0.05 })
    T(g, x, heightAt(x, z) - HOME_Y - 0.02, z, 0, r() * 3, 0, [1.1, 0.12, 0.85])
    parts.push(g)
  }
  return merge(parts)
}

export function Sign() {
  const y = heightAt(SIGN_POS.x, SIGN_POS.z)
  const done = useMemo(() => holdReady(), [])
  const wood = mat('#8a5a36', { rough: 0.8 })
  const plank = mat('#b77d4b', { rough: 0.75 })
  return (
    <group position={[SIGN_POS.x, y - 0.1, SIGN_POS.z]} rotation-y={-0.35}>
      {[-1.25, 1.25].map((x) => (
        <mesh key={x} material={wood} position={[x, 1.0, 0]} castShadow>
          <boxGeometry args={[0.16, 2.0, 0.16]} />
        </mesh>
      ))}
      <mesh material={plank} position={[0, 1.55, 0.05]} castShadow receiveShadow>
        <boxGeometry args={[3.0, 0.8, 0.12]} />
      </mesh>
      <mesh material={mat('#9b6a3e', { rough: 0.8 })} position={[0, 1.55, 0.02]} rotation-z={0.03}>
        <boxGeometry args={[3.15, 0.86, 0.06]} />
      </mesh>
      <Text font="/fonts/lilita.woff" fontSize={0.48} position={[0, 1.57, 0.115]} color="#fff3dc" outlineWidth={0.025} outlineColor="#5a3418" anchorX="center" anchorY="middle" onSync={done} letterSpacing={0.02}>
        PIZZAVILLE
      </Text>
      <Text font="/fonts/fredoka600.woff" fontSize={0.13} position={[0, 1.24, 0.115]} color="#5a3418" anchorX="center" anchorY="middle">
        POBLACIÓN 1 · FUNDADA EN 2026
      </Text>
      {/* little pizza slice on top */}
      <group position={[0, 2.05, 0.05]} rotation-z={Math.PI}>
        <mesh material={mat('#ffcf4a', { rough: 0.6 })} castShadow>
          <coneGeometry args={[0.28, 0.5, 3]} />
        </mesh>
        <mesh material={mat('#d9a35a')} position={[0, -0.27, 0]}>
          <cylinderGeometry args={[0.3, 0.3, 0.1, 3]} />
        </mesh>
      </group>
    </group>
  )
}

export function PizzHome({ getDoor }: { getDoor?: () => number }) {
  const tree = useMemo(heroTree, [])
  const fence = useMemo(fenceGeo, [])
  const beds = useMemo(gardenBeds, [])
  const stones = useMemo(stepStones, [])
  const vc = mat('#ffffff', { vc: true, rough: 0.8 })
  const one = () => 1
  return (
    <group position={[0, HOME_Y, 0]}>
      <House spec={PIZZ_SPEC} getProgress={one} decorations getDoor={getDoor} />
      <mesh geometry={tree} material={vc} position={[-7.6, 0, 1.5]} castShadow receiveShadow />
      <mesh geometry={fence} material={vc} castShadow receiveShadow />
      <mesh geometry={beds} material={vc} castShadow receiveShadow />
      <mesh geometry={stones} material={vc} receiveShadow />
      {/* bench + lantern */}
      <group position={[-3.6, 0, 3.4]}>
        <mesh material={mat('#9b6a3e')} position={[0, 0.45, 0]} castShadow><boxGeometry args={[1.5, 0.08, 0.45]} /></mesh>
        <mesh material={mat('#9b6a3e')} position={[0, 0.75, -0.2]} castShadow><boxGeometry args={[1.5, 0.35, 0.06]} /></mesh>
        {[-0.65, 0.65].map((x) => <mesh key={x} material={mat('#5d4130')} position={[x, 0.22, 0]}><boxGeometry args={[0.08, 0.45, 0.4]} /></mesh>)}
      </group>
      <Smoke position={[PIZZ_SPEC.w * 0.28, 2.9 + 0.25 + Math.tan(PIZZ_SPEC.pitch) * PIZZ_SPEC.d / 2 * 0.55 + 1.9, -PIZZ_SPEC.d * 0.18]} />
    </group>
  )
}
