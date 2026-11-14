import { useMemo, useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'
import { mulberry32 } from '../world/rng'
import { blob, merge, paint, T } from './geom'
import { clock } from '../engine/clock'

// ------------------------------------------------------------- clouds
function cloudGeo(seed: number) {
  const r = mulberry32(seed)
  const parts: THREE.BufferGeometry[] = []
  const n = 7 + Math.floor(r() * 5)
  for (let i = 0; i < n; i++) {
    const x = (i / (n - 1) - 0.5) * 70 + (r() - 0.5) * 10
    const rad = 10 + r() * 12 * (1 - Math.abs(i / (n - 1) - 0.5))
    const y = rad * 0.35 + r() * 4
    parts.push(paint(T(blob(rad, 2, 0.08, seed + i, 0.72), x, y, (r() - 0.5) * 18), '#ffffff', { ao: [-4, 18, 0.78] }))
  }
  const g = merge(parts)
  const p = g.getAttribute('position') as THREE.BufferAttribute
  for (let i = 0; i < p.count; i++) if (p.getY(i) < 0) p.setY(i, p.getY(i) * 0.25) // flat bottoms
  g.computeVertexNormals()
  return g
}

export function Clouds() {
  const geos = useMemo(() => [cloudGeo(1), cloudGeo(2), cloudGeo(3)], [])
  const mat = useMemo(() => new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 1, emissive: new THREE.Color('#dfe8f2'), emissiveIntensity: 0.45, fog: true }), [])
  const items = useMemo(() => {
    const r = mulberry32(55)
    return Array.from({ length: 38 }, (_, i) => ({
      g: i % 3, x: (r() - 0.5) * 7000, z: (r() - 0.5) * 7000, y: 260 + r() * 260, s: 0.8 + r() * 1.6, ry: r() * 6.28,
    }))
  }, [])
  const refs = useRef<THREE.Mesh[]>([])
  useFrame(() => {
    const t = clock.t
    items.forEach((c, i) => {
      const m = refs.current[i]
      if (!m) return
      let x = c.x + t * 2.2
      x = ((x + 3500) % 7000 + 7000) % 7000 - 3500
      m.position.set(x, c.y, c.z)
    })
  })
  return (
    <group>
      {items.map((c, i) => (
        <mesh key={i} ref={(m) => { if (m) refs.current[i] = m }} geometry={geos[c.g]} material={mat} scale={c.s} rotation-y={c.ry} />
      ))}
    </group>
  )
}

// ------------------------------------------------------------- birds
function birdGeo() {
  const g = new THREE.BufferGeometry()
  // body + two wings (wings flap in the vertex shader via |x|)
  const v = [
    0, 0, -0.25, 0, 0.04, 0.3, 0.08, 0, 0,
    0, 0, -0.25, -0.08, 0, 0, 0, 0.04, 0.3,
    0.05, 0.02, 0.05, 0.75, 0.0, -0.05, 0.05, 0.02, -0.15,
    -0.05, 0.02, 0.05, -0.05, 0.02, -0.15, -0.75, 0.0, -0.05,
  ]
  g.setAttribute('position', new THREE.Float32BufferAttribute(v, 3))
  g.computeVertexNormals()
  return g
}
export function Birds() {
  const geo = useMemo(birdGeo, [])
  const mat = useMemo(() => {
    const m = new THREE.MeshStandardMaterial({ color: '#2d3440', side: THREE.DoubleSide, roughness: 1 })
    m.onBeforeCompile = (s) => {
      s.uniforms.uTime = clock.uTime
      s.vertexShader = s.vertexShader.replace('#include <common>', '#include <common>\nuniform float uTime;').replace(
        '#include <begin_vertex>',
        `#include <begin_vertex>
        float ph = 0.;
        #ifdef USE_INSTANCING
        ph = instanceMatrix[3].x*0.3 + instanceMatrix[3].z*0.2;
        #endif
        transformed.y += abs(position.x) * sin(uTime*9. + ph) * 0.9;`,
      )
    }
    return m
  }, [])
  const N = 22
  const ref = useRef<THREE.InstancedMesh>(null!)
  const flocks = useMemo(() => {
    const r = mulberry32(9)
    return Array.from({ length: N }, (_, i) => ({ f: i % 3, ox: (r() - 0.5) * 8, oy: (r() - 0.5) * 3, oz: (r() - 0.5) * 8, sp: 0.9 + r() * 0.2 }))
  }, [])
  const o = useMemo(() => new THREE.Object3D(), [])
  useFrame(() => {
    const t = clock.t
    flocks.forEach((b, i) => {
      const cx = [40, -120, 160][b.f], cz = [-30, 60, 90][b.f], R = [70, 110, 90][b.f], y = [38, 55, 46][b.f]
      const a = t * 0.12 * b.sp + b.f * 2
      const x = cx + Math.cos(a) * R + b.ox, z = cz + Math.sin(a) * R + b.oz
      o.position.set(x, y + b.oy + Math.sin(t + i) * 1.2, z)
      o.rotation.set(0, -a, 0)
      o.scale.setScalar(1.6)
      o.updateMatrix()
      ref.current.setMatrixAt(i, o.matrix)
    })
    ref.current.instanceMatrix.needsUpdate = true
  })
  return <instancedMesh ref={ref} args={[geo, mat, N]} frustumCulled={false} />
}

// ------------------------------------------------------------- chimney smoke
export function Smoke({ position }: { position: [number, number, number] }) {
  const N = 14
  const ref = useRef<THREE.InstancedMesh>(null!)
  const geo = useMemo(() => new THREE.IcosahedronGeometry(0.35, 1), [])
  const mat = useMemo(() => new THREE.MeshStandardMaterial({ color: '#e9edf2', transparent: true, opacity: 0.55, roughness: 1, depthWrite: false }), [])
  const o = useMemo(() => new THREE.Object3D(), [])
  useFrame(() => {
    const t = clock.t
    for (let i = 0; i < N; i++) {
      const life = ((t * 0.25 + i / N) % 1 + 1) % 1
      o.position.set(position[0] + Math.sin(life * 5 + i) * 0.25 + life * 1.8, position[1] + life * 5.5, position[2] + Math.cos(life * 4 + i) * 0.2)
      o.scale.setScalar((0.35 + life * 1.6) * (life < 0.1 ? life / 0.1 : 1) * (1 - Math.max(0, life - 0.75) / 0.25))
      o.updateMatrix()
      ref.current.setMatrixAt(i, o.matrix)
    }
    ref.current.instanceMatrix.needsUpdate = true
  })
  return <instancedMesh ref={ref} args={[geo, mat, N]} frustumCulled={false} />
}
