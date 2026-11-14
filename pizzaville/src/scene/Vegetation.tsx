import { useLayoutEffect, useMemo, useRef } from 'react'
import * as THREE from 'three'
import { heightAt, slopeAt, waterDist, forestDensity, ROAD, HOME_PATH, WATER_LEVEL } from '../world/terrain'
import { mulberry32, smoothstep } from '../world/rng'
import { blob, merge, paint, rockGeo, T } from './geom'
import { useFrame } from '@react-three/fiber'
import { mergeVertices } from 'three/examples/jsm/utils/BufferGeometryUtils.js'
import { addWind } from './glsl'
import { clock } from '../engine/clock'
import { reservedAt } from '../world/plots'

// ----------------------------------------------------------- tree models
function pine(seed: number) {
  const parts = [paint(T(new THREE.CylinderGeometry(0.12, 0.22, 2.4, 7), 0, 1.2, 0), '#6b4a32', { jitter: 0.05 })]
  const tiers = [[1.75, 1.5, 2.6], [1.4, 2.6, 2.3], [1.05, 3.6, 2.0], [0.62, 4.5, 1.6]]
  tiers.forEach(([r, y, h], i) => {
    const c = new THREE.ConeGeometry(r, h, 9, 2)
    const p = c.getAttribute('position') as THREE.BufferAttribute
    for (let k = 0; k < p.count; k++) {
      const a = Math.atan2(p.getZ(k), p.getX(k))
      const w = 1 + 0.09 * Math.sin(a * 5 + seed + i)
      p.setX(k, p.getX(k) * w); p.setZ(k, p.getZ(k) * w)
      if (p.getY(k) < -h / 2 + 0.01) p.setY(k, p.getY(k) + 0.25 * Math.sin(a * 3 + i))
    }
    c.computeVertexNormals()
    parts.push(paint(T(c, 0, y + h / 2 - 0.2, 0, 0, i * 0.7), new THREE.Color('#2f6a3c').offsetHSL(0, 0, i * 0.03), { ao: [y - 0.2, y + h, 0.62], jitter: 0.03, seed }))
  })
  return merge(parts)
}
function oak(seed: number) {
  const r = mulberry32(seed)
  const parts = [paint(T(new THREE.CylinderGeometry(0.16, 0.3, 2.6, 7), 0, 1.3, 0), '#6e4c33', { jitter: 0.05 })]
  parts.push(paint(T(new THREE.CylinderGeometry(0.06, 0.12, 1.4, 5), 0.45, 2.4, 0, 0, 0, -0.7), '#6e4c33'))
  parts.push(paint(T(new THREE.CylinderGeometry(0.06, 0.12, 1.2, 5), -0.4, 2.5, 0.2, 0.3, 0, 0.8), '#6e4c33'))
  const blobs = [[0, 3.6, 0, 1.75], [1.0, 3.2, 0.3, 1.25], [-0.9, 3.3, -0.3, 1.3], [0.2, 4.4, -0.4, 1.2], [-0.3, 3.0, 0.9, 1.05]]
  blobs.forEach(([x, y, z, rad], i) => {
    parts.push(paint(T(blob(rad * (0.9 + r() * 0.2), 1, 0.14, seed + i), x, y, z), new THREE.Color('#5c9b3f').offsetHSL(0.01 * (r() - 0.5), 0, (r() - 0.5) * 0.06), { ao: [2.0, 5.6, 0.55], jitter: 0.05, seed: i }))
  })
  return merge(parts)
}
function birch(seed: number) {
  const parts = [paint(T(new THREE.CylinderGeometry(0.09, 0.15, 3.6, 7), 0, 1.8, 0), '#ece8dc', { jitter: 0.25, seed })]
  ;[[0, 4.2, 0, 1.15, 1.35], [0.4, 3.4, 0.2, 0.85, 1.2], [-0.35, 3.6, -0.2, 0.8, 1.2]].forEach(([x, y, z, rad, sq], i) =>
    parts.push(paint(T(blob(rad, 1, 0.16, seed + i * 3, sq), x, y, z), '#93bf55', { ao: [2.6, 5.6, 0.6], jitter: 0.05, seed: i })),
  )
  return merge(parts)
}
function cypress(seed: number) {
  return merge([
    paint(T(new THREE.CylinderGeometry(0.1, 0.16, 1, 6), 0, 0.5, 0), '#5d4130'),
    paint(T(blob(0.85, 2, 0.1, seed, 3.4), 0, 3.2, 0), '#3b6a33', { ao: [0.6, 6.2, 0.55], jitter: 0.04, seed }),
  ])
}
function bush(seed: number) {
  const r = mulberry32(seed)
  const parts: THREE.BufferGeometry[] = []
  for (let i = 0; i < 4; i++) {
    parts.push(paint(T(blob(0.5 + r() * 0.35, 1, 0.18, seed + i, 0.85), (r() - 0.5) * 0.9, 0.45 + r() * 0.2, (r() - 0.5) * 0.9), '#5a9842', { ao: [0, 1.2, 0.55], jitter: 0.06, seed: i }))
  }
  return merge(parts)
}
function farPine() {
  return merge([
    paint(T(new THREE.CylinderGeometry(0.15, 0.2, 1.4, 4), 0, 0.7, 0), '#5a3f2c'),
    paint(T(new THREE.ConeGeometry(1.8, 5.5, 5), 0, 3.6, 0), '#2f6338', { ao: [0.8, 6.3, 0.6] }),
  ])
}
function farRound() {
  return merge([
    paint(T(new THREE.CylinderGeometry(0.15, 0.2, 1.8, 4), 0, 0.9, 0), '#5a3f2c'),
    paint(T(new THREE.IcosahedronGeometry(1.7, 0), 0, 3.0, 0), '#4f8a3c', { ao: [1.5, 4.7, 0.6] }),
  ])
}

// ----------------------------------------------------------- placement
type Inst = { x: number; y: number; z: number; s: number; ry: number; c: THREE.Color }

function blocked(x: number, z: number, clear = 7) {
  if (ROAD.query(x, z, clear).d < clear) return true
  if (HOME_PATH.query(x, z, 3.5).d < 3.5) return true
  if (reservedAt(x, z)) return true
  return false
}

function placeTrees() {
  const rnd = mulberry32(4242)
  const near: Inst[][] = [[], [], [], [], []] // pine, oak, birch, cypress, bush
  const far: Inst[][] = [[], []]
  const cell = 6.5
  const R = 820
  for (let gz = -R; gz < R; gz += cell) for (let gx = -R; gx < R; gx += cell) {
    const x = gx + rnd() * cell, z = gz + rnd() * cell
    const r = Math.hypot(x, z)
    const fd = forestDensity(x, z)
    const roadD = ROAD.query(x, z, 80).d
    const valley = smoothstep(150, 380, r)
    let dens = fd * (0.15 + 0.85 * valley) * (0.25 + 0.75 * smoothstep(18, 90, roadD))
    dens = Math.max(dens, 0.025 * smoothstep(45, 70, r)) // scattered meadow trees
    if (r < 40) dens = 0
    if (rnd() > dens * 0.92) continue
    const h = heightAt(x, z)
    if (h < WATER_LEVEL + 0.6 || h > 420) continue
    if (waterDist(x, z) < 3) continue
    if (slopeAt(x, z) > 0.95) continue
    if (blocked(x, z)) continue
    const alt = smoothstep(40, 220, h)
    let type: number
    const q = rnd()
    if (q < 0.18 + alt * 0.6) type = 0
    else if (q < 0.58) type = 1
    else if (q < 0.74) type = 2
    else if (q < 0.82) type = 3
    else type = 4
    const s = (type === 4 ? 0.8 : 0.75) + rnd() * 0.6 + (type === 0 ? alt * 0.3 : 0)
    const c = new THREE.Color(1, 1, 1).offsetHSL((rnd() - 0.5) * 0.04, (rnd() - 0.5) * 0.12, (rnd() - 0.5) * 0.12)
    near[type].push({ x, y: h - 0.15, z, s, ry: rnd() * Math.PI * 2, c })
  }
  const cellF = 34
  const RF = 4600
  for (let gz = -RF; gz < RF; gz += cellF) for (let gx = -RF; gx < RF; gx += cellF) {
    const x = gx + rnd() * cellF, z = gz + rnd() * cellF
    const r = Math.hypot(x, z)
    if (r < R - 30) continue
    const fd = forestDensity(x, z)
    if (rnd() > fd * 1.1 + 0.05) continue
    const h = heightAt(x, z)
    if (h < WATER_LEVEL + 0.8 || h > 460) continue
    if (slopeAt(x, z, 8) > 1.15) continue
    const n = 1 + Math.floor(rnd() * 3)
    for (let k = 0; k < n; k++) {
      const xx = x + (rnd() - 0.5) * 22, zz = z + (rnd() - 0.5) * 22
      const hh = heightAt(xx, zz)
      if (hh < WATER_LEVEL + 0.8 || hh > 460) continue
      const type = rnd() < 0.35 + smoothstep(60, 260, hh) * 0.55 ? 0 : 1
      far[type].push({ x: xx, y: hh - 0.3, z: zz, s: 1.4 + rnd() * 1.4, ry: rnd() * 6.28, c: new THREE.Color(1, 1, 1).offsetHSL(0, 0, (rnd() - 0.5) * 0.15) })
    }
  }
  return { near, far }
}

function useInstances(ref: React.RefObject<THREE.InstancedMesh | null>, list: Inst[]) {
  useLayoutEffect(() => {
    const m = ref.current
    if (!m) return
    const o = new THREE.Object3D()
    list.forEach((it, i) => {
      o.position.set(it.x, it.y, it.z)
      o.rotation.set(0, it.ry, 0)
      o.scale.setScalar(it.s)
      o.updateMatrix()
      m.setMatrixAt(i, o.matrix)
      m.setColorAt(i, it.c)
    })
    m.instanceMatrix.needsUpdate = true
    if (m.instanceColor) m.instanceColor.needsUpdate = true
    m.computeBoundingSphere()
  }, [list, ref])
}

function Instanced({ geo, list, mat, shadow = true, cull = false }: { geo: THREE.BufferGeometry; list: Inst[]; mat: THREE.Material; shadow?: boolean; cull?: boolean }) {
  const ref = useRef<THREE.InstancedMesh>(null)
  useInstances(ref, list)
  if (!list.length) return null
  return <instancedMesh ref={ref} args={[geo, mat, list.length]} castShadow={shadow} receiveShadow frustumCulled={cull} />
}

function windMat(strength: number, height: number) {
  const m = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.85 })
  addWind(m, clock.uTime, strength, height)
  return m
}

// low-poly LOD versions (≈20–60 triangles)
function loPine() {
  return merge([
    paint(T(new THREE.CylinderGeometry(0.15, 0.22, 1.6, 5), 0, 0.8, 0), '#6b4a32'),
    paint(T(new THREE.ConeGeometry(1.7, 3.0, 7), 0, 2.6, 0), '#2f6a3c', { ao: [1.1, 4.1, 0.62] }),
    paint(T(new THREE.ConeGeometry(1.15, 2.4, 7), 0, 4.2, 0), '#357544', { ao: [3.0, 5.4, 0.7] }),
  ])
}
function loBlob(color: string, y: number, r: number, sq = 1) {
  return merge([
    paint(T(new THREE.CylinderGeometry(0.14, 0.25, y, 5), 0, y / 2, 0), '#6e4c33'),
    paint(T(new THREE.IcosahedronGeometry(r, 1), 0, y + r * 0.6 * sq, 0, 0, 0, 0, [1, sq, 1]), color, { ao: [y - r * 0.4, y + r * 1.8 * sq, 0.55] }),
  ])
}
const LO = () => [loPine(), loBlob('#5c9b3f', 2.4, 1.9), loBlob('#93bf55', 3.0, 1.2, 1.4), loBlob('#3b6a33', 0.6, 0.9, 3.0), loBlob('#5a9842', 0.2, 0.8, 0.8)]

const CHUNK = 110
const HI_DIST = 230

type Chunk = { cx: number; cz: number; hi: Inst[][]; lo: Inst[][] }

function chunkify(near: Inst[][], far: Inst[][]): Chunk[] {
  const map = new Map<string, Chunk>()
  const get = (x: number, z: number) => {
    const cx = Math.floor(x / CHUNK), cz = Math.floor(z / CHUNK)
    const k = cx + ',' + cz
    let c = map.get(k)
    if (!c) map.set(k, (c = { cx: (cx + 0.5) * CHUNK, cz: (cz + 0.5) * CHUNK, hi: [[], [], [], [], []], lo: [[], [], [], [], []] }))
    return c
  }
  near.forEach((list, t) => list.forEach((it) => get(it.x, it.z).hi[t].push(it)))
  // far trees map onto lo pine (0) and lo round (1)
  far.forEach((list, t) => list.forEach((it) => get(it.x, it.z).lo[t].push(it)))
  return [...map.values()]
}

function TreeChunk({ c, geos, lo, mat, loMat }: { c: Chunk; geos: THREE.BufferGeometry[]; lo: THREE.BufferGeometry[]; mat: THREE.Material; loMat: THREE.Material }) {
  const hiG = useRef<THREE.Group>(null!)
  const loG = useRef<THREE.Group>(null!)
  const hasHi = c.hi.some((l) => l.length)
  // near trees also exist as lo versions when far away
  const loLists = useMemo(() => c.lo.map((l, i) => [...l, ...c.hi[i]]), [c])
  useFrame(({ camera }) => {
    const d = Math.hypot(camera.position.x - c.cx, camera.position.z - c.cz) - CHUNK * 0.7
    const useHi = hasHi && d < HI_DIST + camera.position.y * 0.3
    hiG.current.visible = useHi
    loG.current.visible = !useHi
  })
  return (
    <group>
      <group ref={hiG}>{geos.map((g, i) => <Instanced key={i} geo={g} list={c.hi[i]} mat={mat} cull />)}</group>
      <group ref={loG}>{lo.map((g, i) => <Instanced key={i} geo={g} list={loLists[i]} mat={loMat} shadow={false} cull />)}</group>
    </group>
  )
}

export function Trees() {
  const data = useMemo(placeTrees, [])
  const chunks = useMemo(() => chunkify(data.near, data.far), [data])
  const geos = useMemo(() => [pine(1), oak(2), birch(3), cypress(4), bush(5)].map(indexed), [])
  const lo = useMemo(() => LO().map(indexed), [])
  const mat = useMemo(() => windMat(0.1, 6), [])
  const loMat = useMemo(() => new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.95, flatShading: true }), [])
  return <group>{chunks.map((c, i) => <TreeChunk key={i} c={c} geos={geos} lo={lo} mat={mat} loMat={loMat} />)}</group>
}

function indexed(g: THREE.BufferGeometry) {
  const m = mergeVertices(g, 1e-4)
  m.computeBoundingSphere()
  return m
}

// ----------------------------------------------------------- grass & flowers
function grassTuft() {
  const parts: THREE.BufferGeometry[] = []
  const rnd = mulberry32(99)
  for (let b = 0; b < 5; b++) {
    const h = 0.16 + rnd() * 0.2, w = 0.035
    const g = new THREE.BufferGeometry()
    const lean = (rnd() - 0.5) * 0.25
    const v = [-w, 0, 0, w, 0, 0, -w * 0.6, h * 0.55, lean * 0.4, w * 0.6, h * 0.55, lean * 0.4, 0, h, lean]
    g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(v), 3))
    g.setIndex([0, 1, 2, 1, 3, 2, 2, 3, 4])
    g.computeVertexNormals()
    const n = g.getAttribute('normal') as THREE.BufferAttribute
    for (let i = 0; i < n.count; i++) n.setXYZ(i, 0, 1, 0) // up-facing normals → soft, uniform lighting
    T(g, (rnd() - 0.5) * 0.25, 0, (rnd() - 0.5) * 0.25, 0, rnd() * Math.PI, 0)
    const col = new Float32Array(15)
    const base = new THREE.Color('#4f8a35'), tip = new THREE.Color('#b4d86e')
    for (let i = 0; i < 5; i++) {
      const c = base.clone().lerp(tip, i < 2 ? 0 : i < 4 ? 0.55 : 1)
      col.set([c.r, c.g, c.b], i * 3)
    }
    g.setAttribute('color', new THREE.BufferAttribute(col, 3))
    parts.push(g.toNonIndexed())
    // back side with reversed winding but the same up-facing normals
    const back = g.clone()
    back.setIndex([2, 1, 0, 2, 3, 1, 4, 3, 2])
    parts.push(back.toNonIndexed())
  }
  return merge(parts)
}

function placeGrass() {
  const rnd = mulberry32(5150)
  const out: Inst[] = []
  const R = 95, cell = 0.95
  for (let gz = -R; gz < R; gz += cell) for (let gx = -R; gx < R; gx += cell) {
    const x = gx + rnd() * cell, z = gz + rnd() * cell
    const r = Math.hypot(x, z)
    if (r > R) continue
    if (rnd() > 0.55 * (1 - smoothstep(60, R, r))) continue
    if (Math.abs(x) < 4.6 && z > -4.6 && z < 4.2) continue // house footprint
    if (ROAD.query(x, z, 3.2).d < 3.2 || HOME_PATH.query(x, z, 1.3).d < 1.3) continue
    const h = heightAt(x, z)
    if (h < WATER_LEVEL + 0.25) continue
    out.push({ x, y: h - 0.02, z, s: 0.8 + rnd() * 0.6, ry: rnd() * 6.28, c: new THREE.Color(1, 1, 1).offsetHSL((rnd() - 0.5) * 0.05, 0, (rnd() - 0.5) * 0.18) })
  }
  return out
}

function flowerParts() {
  const stem = paint(T(new THREE.CylinderGeometry(0.01, 0.014, 0.2, 3), 0, 0.1, 0), '#4d8a35')
  const center = paint(T(new THREE.SphereGeometry(0.035, 6, 4), 0, 0.21, 0), '#f2c230')
  const petals: THREE.BufferGeometry[] = []
  for (let i = 0; i < 5; i++) {
    const a = (i / 5) * Math.PI * 2
    petals.push(paint(T(new THREE.SphereGeometry(0.05, 6, 4), Math.cos(a) * 0.065, 0.21, Math.sin(a) * 0.065, 0, 0, 0, [1.25, 0.45, 1.25]), '#ffffff'))
  }
  return { base: merge([stem, center]), petals: merge(petals) }
}
const FLOWER_COLORS = ['#ffffff', '#f4d24a', '#e86a8c', '#9b7be0', '#f08a4b', '#ffffff', '#e4e9ff']
function placeFlowers() {
  const rnd = mulberry32(808)
  const out: Inst[] = []
  const R = 110
  for (let i = 0; i < 9000; i++) {
    const a = rnd() * Math.PI * 2, r = Math.sqrt(rnd()) * R
    const x = Math.cos(a) * r, z = Math.sin(a) * r
    const patch = Math.sin(x * 0.11) * Math.cos(z * 0.13) + Math.sin(x * 0.031 + z * 0.05)
    if (patch < 0.55 && rnd() > 0.06) continue
    if (Math.abs(x) < 4.8 && z > -4.8 && z < 4.4) continue
    if (ROAD.query(x, z, 3.2).d < 3.2 || HOME_PATH.query(x, z, 1.3).d < 1.3) continue
    const h = heightAt(x, z)
    if (h < WATER_LEVEL + 0.4) continue
    const ci = Math.floor((Math.sin(x * 0.05) * 0.5 + 0.5) * 3 + rnd() * 4) % FLOWER_COLORS.length
    out.push({ x, y: h - 0.02, z, s: 0.8 + rnd() * 0.7, ry: rnd() * 6.28, c: new THREE.Color(FLOWER_COLORS[ci]) })
  }
  return out
}

export function Grass() {
  const geo = useMemo(grassTuft, [])
  const list = useMemo(placeGrass, [])
  const mat = useMemo(() => {
    return windMat(0.9, 0.6)
  }, [])
  const fl = useMemo(flowerParts, [])
  const flowers = useMemo(placeFlowers, [])
  const white = useMemo(() => flowers.map((f) => ({ ...f, c: new THREE.Color(1, 1, 1) })), [flowers])
  const fmat = useMemo(() => windMat(0.6, 0.4), [])
  return (
    <group>
      <Instanced geo={geo} list={list} mat={mat} shadow={false} />
      <Instanced geo={fl.base} list={white} mat={fmat} shadow={false} />
      <Instanced geo={fl.petals} list={flowers} mat={fmat} shadow={false} />
    </group>
  )
}

// ----------------------------------------------------------- rocks
export function Rocks() {
  const geos = useMemo(() => [0, 1, 2].map((i) => paint(rockGeo(1, i * 13.7), '#9a958b', { ao: [-0.3, 0.7, 0.6], jitter: 0.06, seed: i })), [])
  const lists = useMemo(() => {
    const rnd = mulberry32(31337)
    const L: Inst[][] = [[], [], []]
    for (let i = 0; i < 2600; i++) {
      const a = rnd() * Math.PI * 2, r = 30 + Math.pow(rnd(), 0.7) * 900
      const x = Math.cos(a) * r, z = Math.sin(a) * r
      const wd = waterDist(x, z)
      const h = heightAt(x, z)
      const nearWater = wd < 6 && wd > -6
      if (!nearWater && rnd() > 0.35) continue
      if (h < WATER_LEVEL - 0.4) continue
      if (blocked(x, z, 5)) continue
      const big = !nearWater && rnd() < 0.25
      const s = big ? 1.2 + rnd() * 2.2 : 0.25 + rnd() * 0.6
      L[i % 3].push({ x, y: h - s * 0.15, z, s, ry: rnd() * 6.28, c: new THREE.Color(1, 1, 1).offsetHSL(0.02 * (rnd() - 0.5), 0, (rnd() - 0.5) * 0.12) })
    }
    return L
  }, [])
  const mat = useMemo(() => new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.9, flatShading: true }), [])
  return <group>{geos.map((g, i) => <Instanced key={i} geo={g} list={lists[i]} mat={mat} />)}</group>
}
