import { useMemo, useRef, type ReactNode } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'
import { clock, ease, seg } from '../engine/clock'
import { mulberry32, pick } from '../world/rng'
import { mat, nightMat } from './materials'
import { blob, merge, paint, T } from './geom'
import { Flag } from './Flag'

export type HouseSpec = {
  w: number; d: number; floors: number; wallH: number
  roofType: 'gable' | 'hip'
  wall: string; roof: string; trim: string; door: string; shutter: string | null; plinth: string
  chimney: boolean; porch: boolean; balcony: boolean
  pitch: number
}

export const PIZZ_SPEC: HouseSpec = {
  w: 6.2, d: 5, floors: 1, wallH: 2.9, roofType: 'gable',
  wall: '#f4e8d0', roof: '#c9663f', trim: '#fffaf1', door: '#8b5a3a', shutter: '#5f9273', plinth: '#b8ab95',
  chimney: true, porch: false, balcony: false, pitch: 0.62,
}

const WALLS = ['#f4e8d0', '#fbf6ec', '#f6dfb5', '#f3cdb4', '#cfe0e6', '#dfe6cf', '#f2d6d0', '#e9e1f2']
const ROOFS = ['#c9663f', '#b85a35', '#a84d33', '#5f6670', '#8a5a44', '#c47a45']
const SHUTTERS = ['#5f9273', '#4f7fa8', '#b8574a', '#d8a542', '#6f6aa8', null]
const DOORS = ['#8b5a3a', '#4f7fa8', '#b8574a', '#3f6b4f', '#6d4a7a']

export function houseSpecFromSeed(seed: number): HouseSpec {
  const r = mulberry32(seed)
  const floors = r() < 0.35 ? 2 : 1
  return {
    w: 5.2 + r() * 1.8, d: 4.4 + r() * 1.4, floors, wallH: 2.7 + r() * 0.3,
    roofType: r() < 0.6 ? 'gable' : 'hip',
    wall: pick(r, WALLS), roof: pick(r, ROOFS), trim: '#fffaf1', door: pick(r, DOORS), shutter: pick(r, SHUTTERS), plinth: '#b8ab95',
    chimney: r() < 0.6, porch: r() < 0.4, balcony: floors === 2 && r() < 0.6, pitch: 0.5 + r() * 0.2,
  }
}

// ---------------------------------------------------------------- stages
// progress windows (0..1) of the construction sequence
export const STAGES = {
  plot: [0.0, 0.05], materials: [0.05, 0.14], foundation: [0.14, 0.22], walls: [0.22, 0.5], roof: [0.5, 0.64],
  openings: [0.64, 0.74], decor: [0.74, 0.82], plants: [0.82, 0.89], flag: [0.89, 0.96], movein: [0.96, 1.0],
} as const

type Kind = 'pop' | 'rise' | 'drop' | 'during' | 'grow'
type Part = { o: THREE.Object3D; k: Kind; a: number; b: number; base: THREE.Vector3; baseS: THREE.Vector3 }

/** returns the construction progress getter + a ref factory for animated parts */
export function useBuildAnim(getP: () => number) {
  const parts = useRef<Part[]>([])
  const reg = (k: Kind, a: number, b: number) => (o: THREE.Object3D | null) => {
    if (!o || parts.current.some((p) => p.o === o)) return
    parts.current.push({ o, k, a, b, base: o.position.clone(), baseS: o.scale.clone() })
  }
  useFrame(() => {
    const p = getP()
    for (const part of parts.current) {
      const s = seg(p, part.a, part.b)
      const { o } = part
      switch (part.k) {
        case 'pop': {
          o.visible = p >= part.a
          const k = Math.max(0.0001, ease.outBack(s))
          o.scale.copy(part.baseS).multiplyScalar(k)
          break
        }
        case 'grow': {
          o.visible = p >= part.a
          o.scale.copy(part.baseS).multiplyScalar(Math.max(0.0001, ease.out(s)))
          break
        }
        case 'rise': {
          o.visible = p >= part.a
          o.scale.set(part.baseS.x, part.baseS.y * Math.max(0.0001, ease.out(s)), part.baseS.z)
          break
        }
        case 'drop': {
          o.visible = p >= part.a
          const e = s < 1 ? 1 - ease.outBack(s) : 0
          o.position.set(part.base.x, part.base.y + e * 5, part.base.z)
          break
        }
        case 'during':
          o.visible = p >= part.a && p < part.b
          break
      }
    }
  })
  return reg
}

const darkInterior = new THREE.MeshBasicMaterial({ color: '#1c1512' })

// ---------------------------------------------------------------- pieces
function Box({ s, p, m, cast = true, r }: { s: [number, number, number]; p: [number, number, number]; m: THREE.Material; cast?: boolean; r?: [number, number, number] }) {
  return (
    <mesh position={p} rotation={r} material={m} castShadow={cast} receiveShadow>
      <boxGeometry args={s} />
    </mesh>
  )
}

function roofGeometry(spec: HouseSpec) {
  const { w, d, pitch, roof } = spec
  const oh = 0.45
  const parts: THREE.BufferGeometry[] = []
  const base = new THREE.Color(roof)
  if (spec.roofType === 'gable') {
    const half = d / 2 + oh
    const L = half / Math.cos(pitch)
    const rise = Math.tan(pitch) * (d / 2)
    for (const side of [1, -1]) {
      const slab = new THREE.BoxGeometry(w + oh * 2, 0.16, L)
      T(slab, 0, 0, side * L / 2, 0, 0, 0)
      const rows = Math.floor(L / 0.32)
      const tiles: THREE.BufferGeometry[] = [paint(slab, base.clone().multiplyScalar(0.85))]
      for (let i = 0; i < rows; i++) {
        const t = new THREE.CylinderGeometry(0.11, 0.11, w + oh * 2, 6, 1, false, 0, Math.PI)
        T(t, 0, 0.08, side * (0.16 + i * 0.32), 0, 0, Math.PI / 2)
        tiles.push(paint(t, base.clone().offsetHSL(0, 0, ((i * 7919) % 5) * 0.012 - 0.02), { jitter: 0.06, seed: i }))
      }
      const g = merge(tiles)
      T(g, 0, 0, 0, side * pitch, 0, 0)
      T(g, 0, rise + 0.1, 0)
      parts.push(g)
    }
    // ridge cap
    parts.push(paint(T(new THREE.CylinderGeometry(0.16, 0.16, w + oh * 2 + 0.1, 8), 0, rise + 0.2, 0, 0, 0, Math.PI / 2), base.clone().multiplyScalar(0.8)))
    // gable triangles
    const shape = new THREE.Shape()
    shape.moveTo(-d / 2, 0); shape.lineTo(d / 2, 0); shape.lineTo(0, rise); shape.lineTo(-d / 2, 0)
    for (const sx of [1, -1]) {
      const tri = new THREE.ExtrudeGeometry(shape, { depth: 0.2, bevelEnabled: false })
      T(tri, sx * (w / 2 - 0.1) - (sx > 0 ? 0 : 0.0), 0, 0, 0, Math.PI / 2 * sx, 0)
      parts.push(paint(tri, spec.wall))
    }
  } else {
    const rise = Math.tan(pitch) * (Math.min(w, d) / 2) * 0.95
    const cone = new THREE.ConeGeometry(Math.SQRT1_2 * 2, 1, 4, 3)
    T(cone, 0, 0.5, 0, 0, Math.PI / 4, 0)
    T(cone, 0, 0, 0, 0, 0, 0, [(w + oh * 2) / 2, rise, (d + oh * 2) / 2])
    const g = paint(cone, base, { jitter: 0.04 })
    const p = g.getAttribute('position') as THREE.BufferAttribute
    const c = g.getAttribute('color') as THREE.BufferAttribute
    for (let i = 0; i < p.count; i++) {
      const band = Math.sin(p.getY(i) / rise * 26) * 0.06
      c.setXYZ(i, c.getX(i) * (1 + band), c.getY(i) * (1 + band), c.getZ(i) * (1 + band))
    }
    parts.push(g)
  }
  return merge(parts)
}

function roofRise(spec: HouseSpec) {
  return spec.roofType === 'gable' ? Math.tan(spec.pitch) * (spec.d / 2) : Math.tan(spec.pitch) * (Math.min(spec.w, spec.d) / 2) * 0.95
}

function Window({ x, y, z, ry = 0, spec, reg, a, b, flowers = false }: { x: number; y: number; z: number; ry?: number; spec: HouseSpec; reg: ReturnType<typeof useBuildAnim>; a: number; b: number; flowers?: boolean }) {
  const trim = mat(spec.trim, { rough: 0.6 })
  const glass = nightMat('#9fc1dc', '#ffc46b', 0.04, 1.7)
  const sh = spec.shutter ? mat(spec.shutter, { rough: 0.7 }) : null
  return (
    <group position={[x, y, z]} rotation-y={ry} ref={reg('pop', a, b)}>
      <Box s={[0.98, 1.18, 0.1]} p={[0, 0, 0]} m={trim} />
      <Box s={[0.8, 1.0, 0.06]} p={[0, 0, 0.04]} m={glass} cast={false} />
      <Box s={[0.05, 1.0, 0.06]} p={[0, 0, 0.08]} m={trim} cast={false} />
      <Box s={[0.8, 0.05, 0.06]} p={[0, 0.08, 0.08]} m={trim} cast={false} />
      <Box s={[1.1, 0.08, 0.22]} p={[0, -0.62, 0.08]} m={trim} />
      {sh && (
        <>
          <Box s={[0.42, 1.12, 0.06]} p={[-0.74, 0, 0.05]} m={sh} />
          <Box s={[0.42, 1.12, 0.06]} p={[0.74, 0, 0.05]} m={sh} />
        </>
      )}
      {flowers && <FlowerBox reg={reg} a={STAGES.decor[0]} b={STAGES.decor[1]} />}
    </group>
  )
}

const flowerBoxGeo = (() => {
  const parts: THREE.BufferGeometry[] = [paint(T(new THREE.BoxGeometry(0.95, 0.2, 0.22), 0, 0, 0), '#8b5a3a')]
  const cols = ['#e8506a', '#f4c430', '#ffffff', '#e8506a', '#ff8a4b']
  for (let i = 0; i < 7; i++) {
    parts.push(paint(T(blob(0.09, 1, 0.2, i), -0.39 + i * 0.13, 0.13, 0.02), i % 2 ? '#4f8f3a' : cols[i % cols.length]))
  }
  return merge(parts)
})()
function FlowerBox({ reg, a, b }: { reg: ReturnType<typeof useBuildAnim>; a: number; b: number }) {
  return <mesh geometry={flowerBoxGeo} material={mat('#ffffff', { vc: true })} position={[0, -0.76, 0.2]} ref={reg('pop', a, b)} castShadow />
}

function Door({ spec, z, reg, getDoor }: { spec: HouseSpec; z: number; reg: ReturnType<typeof useBuildAnim>; getDoor?: () => number }) {
  const panel = useRef<THREE.Group>(null!)
  useFrame(() => { if (getDoor && panel.current) panel.current.rotation.y = -ease.inOut(getDoor()) * 1.75 })
  const wood = mat(spec.door, { rough: 0.6 })
  const trim = mat(spec.trim, { rough: 0.6 })
  const [a, b] = STAGES.openings
  return (
    <group position={[0, 0, z]} ref={reg('pop', a, b)}>
      <Box s={[1.3, 2.25, 0.12]} p={[0, 1.12, 0]} m={trim} />
      <mesh position={[0, 1.03, 0.066]} material={darkInterior}><boxGeometry args={[1.0, 2.05, 0.04]} /></mesh>
      <group ref={panel} position={[-0.5, 0, 0.1]}>
        <Box s={[1.0, 2.05, 0.08]} p={[0.5, 1.03, 0]} m={wood} />
        <Box s={[0.36, 0.7, 0.04]} p={[0.28, 1.45, 0.05]} m={mat(spec.door, { rough: 0.5 })} cast={false} />
        <Box s={[0.36, 0.7, 0.04]} p={[0.72, 1.45, 0.05]} m={mat(spec.door, { rough: 0.5 })} cast={false} />
        <Box s={[0.8, 0.55, 0.04]} p={[0.5, 0.55, 0.05]} m={mat(spec.door, { rough: 0.5 })} cast={false} />
        <mesh position={[0.85, 1.05, 0.08]} material={mat('#d9b04a', { metal: 0.8, rough: 0.3 })}>
          <sphereGeometry args={[0.05, 10, 8]} />
        </mesh>
      </group>
      <Box s={[1.6, 0.16, 0.7]} p={[0, 0.0, 0.35]} m={mat(spec.plinth)} />
      {/* door lamp */}
      <mesh position={[0.9, 2.05, 0.12]} material={nightMat('#fff2c8', '#ffcf7a', 0.2, 3)}>
        <sphereGeometry args={[0.1, 10, 8]} />
      </mesh>
    </group>
  )
}

// ---------------------------------------------------------------- house
export function House({ spec, getProgress, flag, decorations, children, getDoor }: { spec: HouseSpec; getProgress: () => number; flag?: string | null; decorations?: boolean; children?: ReactNode; getDoor?: () => number }) {
  const reg = useBuildAnim(getProgress)
  const roofGeo = useMemo(() => roofGeometry(spec), [spec])
  const { w, d, floors, wallH } = spec
  const H = wallH * floors
  const rise = roofRise(spec)
  const wallM = mat(spec.wall, { rough: 0.9 })
  const trimM = mat(spec.trim, { rough: 0.6 })
  const [wa, wb] = STAGES.walls
  const slices = 5 * floors
  const sliceH = H / slices
  // window layout
  const front: [number, number][] = []
  const cols = w > 6 ? [-1.9, 1.9] : [-1.65, 1.65]
  for (let f = 0; f < floors; f++) {
    const y = f * wallH + 1.55
    if (f === 0) cols.forEach((x) => front.push([x, y]))
    else [-1.65, 0, 1.65].forEach((x) => front.push([x * (w / 6), y]))
  }
  const [oa, ob] = STAGES.openings
  const lotRnd = mulberry32(Math.floor(w * 1000 + d * 10))
  return (
    <group>
      {/* foundation */}
      <group ref={reg('rise', ...STAGES.foundation)} position={[0, -1.2, 0]}>
        <Box s={[w + 0.5, 1.45, d + 0.5]} p={[0, 0.72, 0]} m={mat(spec.plinth, { rough: 0.95 })} />
      </group>
      {/* walls in courses */}
      {Array.from({ length: slices }, (_, i) => {
        const a = wa + (wb - wa) * (i / slices), b = a + (wb - wa) / slices * 1.6
        return (
          <group key={i} position={[0, 0.25 + i * sliceH, 0]} ref={reg('rise', a, Math.min(b, wb))}>
            <Box s={[w, sliceH + 0.002, d]} p={[0, sliceH / 2, 0]} m={wallM} />
          </group>
        )
      })}
      {/* corner trims & floor belt */}
      <group ref={reg('rise', wa + 0.05, wb)} position={[0, 0.25, 0]}>
        {[[-1, -1], [1, -1], [-1, 1], [1, 1]].map(([sx, sz], i) => (
          <Box key={i} s={[0.18, H, 0.18]} p={[sx * (w / 2), H / 2, sz * (d / 2)]} m={trimM} />
        ))}
        {floors > 1 && <Box s={[w + 0.12, 0.14, d + 0.12]} p={[0, wallH, 0]} m={trimM} />}
        <Box s={[w + 0.2, 0.16, d + 0.2]} p={[0, H, 0]} m={trimM} />
      </group>
      {/* roof */}
      <group position={[0, H + 0.25, 0]}>
        <group ref={reg('drop', ...STAGES.roof)}>
          <mesh geometry={roofGeo} material={mat('#ffffff', { vc: true, rough: 0.75 })} castShadow receiveShadow />
          {spec.chimney && (
            <group position={[w * 0.28, rise * 0.55, -d * 0.18]}>
              <Box s={[0.6, 1.6, 0.6]} p={[0, 0.5, 0]} m={mat('#c4b49c', { rough: 0.95 })} />
              <Box s={[0.75, 0.14, 0.75]} p={[0, 1.33, 0]} m={mat('#8d8170')} />
            </group>
          )}
        </group>
      </group>
      {/* openings */}
      <group position={[0, 0.25, 0]}>
        <Door spec={spec} z={d / 2 + 0.02} reg={reg} getDoor={getDoor} />
        {front.map(([x, y], i) => (
          <Window key={i} x={x} y={y} z={d / 2 + 0.04} spec={spec} reg={reg} a={oa + i * 0.012} b={ob} flowers={i < 2 || decorations} />
        ))}
        {Array.from({ length: floors }, (_, f) => (
          <group key={f}>
            <Window x={w / 2 + 0.04} y={f * wallH + 1.55} z={0} ry={Math.PI / 2} spec={spec} reg={reg} a={oa + 0.03} b={ob} />
            <Window x={-w / 2 - 0.04} y={f * wallH + 1.55} z={0} ry={-Math.PI / 2} spec={spec} reg={reg} a={oa + 0.03} b={ob} />
            <Window x={-w / 4} y={f * wallH + 1.55} z={-d / 2 - 0.04} ry={Math.PI} spec={spec} reg={reg} a={oa + 0.04} b={ob} />
          </group>
        ))}
        {spec.porch && (
          <group ref={reg('drop', STAGES.decor[0], STAGES.decor[1])}>
            <Box s={[2.3, 0.14, 1.5]} p={[0, 2.55, d / 2 + 0.75]} m={mat(spec.roof, { rough: 0.7 })} r={[-0.18, 0, 0]} />
            <Box s={[0.12, 2.5, 0.12]} p={[-1.0, 1.25, d / 2 + 1.35]} m={trimM} />
            <Box s={[0.12, 2.5, 0.12]} p={[1.0, 1.25, d / 2 + 1.35]} m={trimM} />
          </group>
        )}
        {spec.balcony && (
          <group ref={reg('pop', STAGES.decor[0], STAGES.decor[1])} position={[0, wallH, d / 2 + 0.45]}>
            <Box s={[1.9, 0.12, 0.9]} p={[0, 0, 0]} m={mat(spec.plinth)} />
            {Array.from({ length: 9 }, (_, i) => <Box key={i} s={[0.04, 0.8, 0.04]} p={[-0.88 + i * 0.22, 0.42, 0.4]} m={mat('#3b3f46', { metal: 0.6, rough: 0.4 })} cast={false} />)}
            <Box s={[1.9, 0.05, 0.06]} p={[0, 0.84, 0.4]} m={mat('#3b3f46', { metal: 0.6, rough: 0.4 })} />
          </group>
        )}
      </group>
      {/* plants around the house */}
      <group ref={reg('grow', ...STAGES.plants)}>
        {[-1, 1].map((sx) => (
          <mesh key={sx} geometry={bushGeo} material={mat('#ffffff', { vc: true, rough: 0.85 })} position={[sx * (w / 2 - 0.4), 0.05, d / 2 + 0.7]} scale={0.7 + lotRnd() * 0.3} castShadow />
        ))}
      </group>
      {/* mailbox */}
      <group ref={reg('pop', ...STAGES.decor)} position={[w / 2 + 0.8, 0, d / 2 + 2.6]}>
        <Mailbox color={spec.door} />
      </group>
      {flag && (
        <group position={[-w / 2 - 1.1, 0, d / 2 + 1.6]}>
          <FlagPole iso={flag} getProgress={getProgress} reg={reg} />
        </group>
      )}
      {children}
    </group>
  )
}

const bushGeo = (() => {
  const parts: THREE.BufferGeometry[] = []
  for (let i = 0; i < 4; i++) parts.push(paint(T(blob(0.45 + (i % 2) * 0.15, 1, 0.18, i * 3, 0.85), Math.cos(i * 2.1) * 0.35, 0.4, Math.sin(i * 2.1) * 0.3), i === 3 ? '#68a84a' : '#559641', { ao: [0, 1, 0.55], jitter: 0.05 }))
  parts.push(paint(T(blob(0.12, 1, 0.2, 9), 0.2, 0.85, 0.3), '#f06b8a'))
  parts.push(paint(T(blob(0.1, 1, 0.2, 10), -0.25, 0.75, 0.35), '#ffffff'))
  return merge(parts)
})()

export function Mailbox({ color }: { color: string }) {
  return (
    <group>
      <Box s={[0.1, 1.05, 0.1]} p={[0, 0.52, 0]} m={mat('#6e4c33')} />
      <mesh position={[0, 1.15, 0]} rotation-z={Math.PI / 2} material={mat(color, { rough: 0.5 })} castShadow>
        <cylinderGeometry args={[0.17, 0.17, 0.5, 14, 1, false, 0, Math.PI]} />
      </mesh>
      <Box s={[0.34, 0.06, 0.5]} p={[0, 1.15, 0]} m={mat(color, { rough: 0.5 })} r={[Math.PI / 2, 0, 0]} />
      <Box s={[0.5, 0.18, 0.34]} p={[0, 1.07, 0]} m={mat(color, { rough: 0.5 })} />
      <Box s={[0.03, 0.22, 0.05]} p={[0.27, 1.27, 0.0]} m={mat('#d8423a')} />
    </group>
  )
}

function FlagPole({ iso, getProgress, reg }: { iso: string; getProgress: () => number; reg: ReturnType<typeof useBuildAnim> }) {
  const flagRef = useRef<THREE.Group>(null!)
  const [a, b] = STAGES.flag
  useFrame(() => {
    const p = getProgress()
    const s = seg(p, a + (b - a) * 0.35, b)
    flagRef.current.position.y = 1.1 + ease.inOut(s) * 3.0
    flagRef.current.visible = p >= a + (b - a) * 0.35
  })
  return (
    <group>
      <group ref={reg('rise', a, a + (b - a) * 0.35)}>
        <mesh position={[0, 2.2, 0]} material={mat('#d9dde2', { metal: 0.7, rough: 0.3 })} castShadow>
          <cylinderGeometry args={[0.045, 0.06, 4.4, 8]} />
        </mesh>
        <mesh position={[0, 4.45, 0]} material={mat('#d9b04a', { metal: 0.8, rough: 0.3 })}>
          <sphereGeometry args={[0.09, 10, 8]} />
        </mesh>
      </group>
      <group ref={flagRef}>
        <Flag iso={iso} />
      </group>
    </group>
  )
}

/** progress getter for a construction that started at `start` (world seconds) and lasts `dur` */
export function timedProgress(start: number, dur: number) {
  return () => (dur <= 0 ? 1 : Math.min(1, Math.max(0, (clock.t - start) / dur)))
}
