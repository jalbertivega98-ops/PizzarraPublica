// Small procedural-geometry toolkit: everything is merged into a few
// vertex-coloured BufferGeometries so it can be instanced cheaply.
import * as THREE from 'three'
import { mergeGeometries, mergeVertices } from 'three/examples/jsm/utils/BufferGeometryUtils.js'
import { makeNoise } from '../world/rng'

const gn = makeNoise(777)

export function paint(g: THREE.BufferGeometry, color: THREE.ColorRepresentation, opts: { ao?: [number, number, number]; jitter?: number; seed?: number } = {}) {
  let geo = g.index ? g.toNonIndexed() : g
  geo.deleteAttribute('uv')
  const pos = geo.getAttribute('position') as THREE.BufferAttribute
  const col = new Float32Array(pos.count * 3)
  const c = new THREE.Color(color)
  const tmp = new THREE.Color()
  let ymin = Infinity, ymax = -Infinity
  if (opts.ao) { ymin = opts.ao[0]; ymax = opts.ao[1] }
  for (let i = 0; i < pos.count; i++) {
    tmp.copy(c)
    if (opts.jitter) {
      const n = gn(pos.getX(i) * 3 + (opts.seed ?? 0), pos.getZ(i) * 3 + pos.getY(i) * 2)
      tmp.offsetHSL(0, 0, n * opts.jitter)
    }
    if (opts.ao) {
      const t = THREE.MathUtils.clamp((pos.getY(i) - ymin) / (ymax - ymin), 0, 1)
      tmp.multiplyScalar(opts.ao[2] + (1 - opts.ao[2]) * t)
    }
    col[i * 3] = tmp.r; col[i * 3 + 1] = tmp.g; col[i * 3 + 2] = tmp.b
  }
  geo.setAttribute('color', new THREE.BufferAttribute(col, 3))
  if (!geo.getAttribute('normal')) geo.computeVertexNormals()
  return geo
}

export function merge(geos: THREE.BufferGeometry[]) {
  const g = mergeGeometries(geos.map((x) => (x.index ? x.toNonIndexed() : x)), false)!
  g.computeBoundingSphere()
  g.computeBoundingBox()
  return g
}

/** noisy blob (smooth normals) */
export function blob(radius: number, detail: number, amp: number, seed: number, squashY = 1) {
  let g: THREE.BufferGeometry = new THREE.IcosahedronGeometry(radius, detail)
  g.deleteAttribute('normal'); g.deleteAttribute('uv')
  g = mergeVertices(g)
  const p = g.getAttribute('position') as THREE.BufferAttribute
  const v = new THREE.Vector3()
  for (let i = 0; i < p.count; i++) {
    v.fromBufferAttribute(p, i)
    const d = 1 + amp * gn(v.x * 1.3 + seed, v.y * 1.3 + v.z * 0.7 - seed)
    v.multiplyScalar(d)
    v.y *= squashY
    p.setXYZ(i, v.x, v.y, v.z)
  }
  g.computeVertexNormals()
  return g
}

/** faceted rock */
export function rockGeo(radius: number, seed: number) {
  let g: THREE.BufferGeometry = new THREE.IcosahedronGeometry(radius, 1)
  g.deleteAttribute('normal'); g.deleteAttribute('uv')
  g = mergeVertices(g)
  const p = g.getAttribute('position') as THREE.BufferAttribute
  const v = new THREE.Vector3()
  for (let i = 0; i < p.count; i++) {
    v.fromBufferAttribute(p, i)
    v.multiplyScalar(1 + 0.32 * gn(v.x * 1.7 + seed, v.z * 1.7 + v.y))
    v.y *= 0.62
    if (v.y < -radius * 0.25) v.y = -radius * 0.25
    p.setXYZ(i, v.x, v.y, v.z)
  }
  const ng = g.toNonIndexed()
  ng.computeVertexNormals()
  return ng
}

export const T = (g: THREE.BufferGeometry, x = 0, y = 0, z = 0, rx = 0, ry = 0, rz = 0, s: number | [number, number, number] = 1) => {
  const m = new THREE.Matrix4().compose(
    new THREE.Vector3(x, y, z),
    new THREE.Quaternion().setFromEuler(new THREE.Euler(rx, ry, rz)),
    Array.isArray(s) ? new THREE.Vector3(...s) : new THREE.Vector3(s, s, s),
  )
  g.applyMatrix4(m)
  return g
}
