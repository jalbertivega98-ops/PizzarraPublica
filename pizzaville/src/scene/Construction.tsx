// Construction-site dressing around a House in progress: stakes & string,
// material piles that get used up, dust puffs on every stage, sparkles at the end.
import { useMemo, useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'
import { STAGES, type HouseSpec } from './House'
import { mat } from './materials'
import { seg, ease } from '../engine/clock'
import { mulberry32 } from '../world/rng'

const EVENTS = [STAGES.plot[0], STAGES.foundation[0], STAGES.walls[0], (STAGES.walls[0] + STAGES.walls[1]) / 2, STAGES.roof[0], STAGES.openings[0], STAGES.flag[1]]

export function ConstructionSite({ spec, getProgress }: { spec: HouseSpec; getProgress: () => number }) {
  const { w, d } = spec
  const stakes = useRef<THREE.Group>(null!)
  const planks = useRef<THREE.Group>(null!)
  const bricks = useRef<THREE.Group>(null!)
  const dust = useRef<THREE.InstancedMesh>(null!)
  const sparkle = useRef<THREE.InstancedMesh>(null!)
  const N = 70
  const SP = 40
  const seeds = useMemo(() => {
    const r = mulberry32(5)
    return Array.from({ length: N }, () => [r() * 6.28, r(), r(), r()])
  }, [])
  const o = useMemo(() => new THREE.Object3D(), [])
  const corners: [number, number][] = [[-w / 2 - 0.4, -d / 2 - 0.4], [w / 2 + 0.4, -d / 2 - 0.4], [w / 2 + 0.4, d / 2 + 0.4], [-w / 2 - 0.4, d / 2 + 0.4]]

  useFrame(() => {
    const p = getProgress()
    // stakes visible from plot until roof
    stakes.current.visible = p > 0 && p < STAGES.openings[0]
    stakes.current.scale.setScalar(Math.max(0.001, ease.outBack(seg(p, 0, 0.04))))
    // material piles drop in, then shrink as they are used
    const inP = ease.outBack(seg(p, STAGES.materials[0], STAGES.materials[1]))
    planks.current.visible = p > STAGES.materials[0] && p < STAGES.roof[1]
    planks.current.scale.set(1, Math.max(0.05, inP * (1 - seg(p, STAGES.roof[0], STAGES.roof[1]) * 0.9)), 1)
    bricks.current.visible = p > STAGES.materials[0] + 0.02 && p < STAGES.walls[1]
    bricks.current.scale.set(1, Math.max(0.05, ease.outBack(seg(p, STAGES.materials[0] + 0.02, STAGES.materials[1])) * (1 - seg(p, STAGES.walls[0], STAGES.walls[1]) * 0.9)), 1)
    // dust: puffs born at each event, ~0.06 progress long
    let k = 0
    for (let e = 0; e < EVENTS.length - 1; e++) {
      const age = (p - EVENTS[e]) / 0.07
      for (let j = 0; j < N / (EVENTS.length - 1) && k < N; j++, k++) {
        const [a, r1, r2, r3] = seeds[k]
        if (age < 0 || age > 1 || p >= 1) { o.scale.setScalar(0.0001) }
        else {
          const R = Math.max(w, d) * 0.55 + r1 * 1.2
          o.position.set(Math.cos(a) * R * (0.4 + age * 0.6), 0.2 + age * (1 + r2 * 1.5) + (e >= 4 ? spec.wallH * spec.floors * 0.9 : 0), Math.sin(a) * R * (0.4 + age * 0.6))
          o.scale.setScalar((0.25 + r3 * 0.35) * Math.sin(age * Math.PI))
        }
        o.updateMatrix()
        dust.current.setMatrixAt(k, o.matrix)
      }
    }
    dust.current.instanceMatrix.needsUpdate = true
    // sparkles when finished (flag raised)
    const sa = (p - STAGES.flag[1]) / 0.06
    for (let i = 0; i < SP; i++) {
      const [a, r1, r2] = seeds[i]
      if (sa < 0 || sa > 1) o.scale.setScalar(0.0001)
      else {
        o.position.set(Math.cos(a) * (1 + sa * 5 * r1), 1 + spec.wallH + sa * (3 + r2 * 4) - sa * sa * 3, Math.sin(a) * (1 + sa * 5 * r1))
        o.rotation.set(a * 3 + sa * 8, a, 0)
        o.scale.setScalar(0.22 * (1 - sa))
      }
      o.updateMatrix()
      sparkle.current.setMatrixAt(i, o.matrix)
    }
    sparkle.current.instanceMatrix.needsUpdate = true
  })

  const wood = mat('#c9a06a', { rough: 0.8 })
  return (
    <group>
      <group ref={stakes}>
        {corners.map(([x, z], i) => (
          <mesh key={i} position={[x, 0.35, z]} material={wood} castShadow>
            <boxGeometry args={[0.08, 0.8, 0.08]} />
          </mesh>
        ))}
        {corners.map(([x, z], i) => {
          const [x2, z2] = corners[(i + 1) % 4]
          const len = Math.hypot(x2 - x, z2 - z)
          return (
            <mesh key={'s' + i} position={[(x + x2) / 2, 0.6, (z + z2) / 2]} rotation-y={Math.atan2(x2 - x, z2 - z)} material={mat('#ff6a2b', { emissive: '#ff6a2b', ei: 0.3 })}>
              <boxGeometry args={[0.02, 0.02, len]} />
            </mesh>
          )
        })}
      </group>
      <group ref={planks} position={[w / 2 + 2.0, 0, 0.8]}>
        {Array.from({ length: 6 }, (_, i) => (
          <mesh key={i} position={[0, 0.08 + i * 0.13, 0]} rotation-y={(i % 2) * 0.08} material={wood} castShadow>
            <boxGeometry args={[0.9, 0.11, 2.4]} />
          </mesh>
        ))}
      </group>
      <group ref={bricks} position={[-w / 2 - 2.0, 0, -0.6]}>
        <mesh position={[0, 0.06, 0]} material={mat('#8f6b45')} castShadow><boxGeometry args={[1.3, 0.12, 1.3]} /></mesh>
        {Array.from({ length: 12 }, (_, i) => (
          <mesh key={i} position={[((i % 3) - 1) * 0.4, 0.22 + Math.floor(i / 6) * 0.2, (Math.floor(i / 3) % 2 - 0.5) * 0.55]} material={mat('#c26a4a', { rough: 0.9 })} castShadow>
            <boxGeometry args={[0.38, 0.18, 0.5]} />
          </mesh>
        ))}
      </group>
      <instancedMesh ref={dust} args={[new THREE.IcosahedronGeometry(0.5, 1), mat('#f6f1e8', { rough: 1, transparent: true, opacity: 0.5 }), N]} frustumCulled={false} />
      <instancedMesh ref={sparkle} args={[new THREE.OctahedronGeometry(0.5, 0), mat('#ffd34d', { emissive: '#ffb020', ei: 1.2 }), SP]} frustumCulled={false} />
    </group>
  )
}
