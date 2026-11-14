// Pure terrain model (no three.js). Shared by the browser scene and the
// Node API (plot allocation), so both always agree on the same world.
import { makeNoise, smoothstep, lerp, clamp } from './rng'

export const WORLD_SEED = 20261114
export const WATER_LEVEL = -0.6
export const TERRAIN_SIZE = 14000

const n1 = makeNoise(WORLD_SEED)
const n2 = makeNoise(WORLD_SEED + 1)
const n3 = makeNoise(WORLD_SEED + 2)
const n4 = makeNoise(WORLD_SEED + 3)

function fbm(noise: (x: number, y: number) => number, x: number, y: number, oct: number) {
  let a = 1, f = 1, s = 0, norm = 0
  for (let i = 0; i < oct; i++) {
    s += a * noise(x * f, y * f)
    norm += a
    a *= 0.5
    f *= 2.03
  }
  return s / norm
}
function ridged(x: number, y: number, oct: number) {
  let a = 1, f = 1, s = 0, norm = 0
  for (let i = 0; i < oct; i++) {
    const v = 1 - Math.abs(n3(x * f, y * f))
    s += a * v * v
    norm += a
    a *= 0.42
    f *= 1.9
  }
  return s / norm
}

// ---------------------------------------------------------------- polylines
type P = [number, number]
function catmull(points: P[], step = 3): P[] {
  const out: P[] = []
  for (let i = 0; i < points.length - 1; i++) {
    const p0 = points[Math.max(0, i - 1)], p1 = points[i], p2 = points[i + 1], p3 = points[Math.min(points.length - 1, i + 2)]
    const len = Math.hypot(p2[0] - p1[0], p2[1] - p1[1])
    const n = Math.max(2, Math.ceil(len / step))
    for (let j = 0; j < n; j++) {
      const t = j / n, t2 = t * t, t3 = t2 * t
      const f = (a: number, b: number, c: number, d: number) =>
        0.5 * (2 * b + (-a + c) * t + (2 * a - 5 * b + 4 * c - d) * t2 + (-a + 3 * b - 3 * c + d) * t3)
      out.push([f(p0[0], p1[0], p2[0], p3[0]), f(p0[1], p1[1], p2[1], p3[1])])
    }
  }
  out.push(points[points.length - 1])
  return out
}

class Polyline {
  pts: P[]
  cum: number[] = [0]
  private buckets = new Map<number, number[]>()
  private minX = Infinity; private maxX = -Infinity; private minZ = Infinity; private maxZ = -Infinity
  private cell = 40
  constructor(ctrl: P[], step = 3) {
    this.pts = catmull(ctrl, step)
    for (let i = 1; i < this.pts.length; i++) {
      this.cum.push(this.cum[i - 1] + Math.hypot(this.pts[i][0] - this.pts[i - 1][0], this.pts[i][1] - this.pts[i - 1][1]))
    }
    for (let i = 0; i < this.pts.length - 1; i++) {
      const [ax, az] = this.pts[i], [bx, bz] = this.pts[i + 1]
      const k = Math.floor((ax + bx) / 2 / this.cell) * 100003 + Math.floor((az + bz) / 2 / this.cell)
      this.minX = Math.min(this.minX, ax, bx); this.maxX = Math.max(this.maxX, ax, bx); this.minZ = Math.min(this.minZ, az, bz); this.maxZ = Math.max(this.maxZ, az, bz)
      let arr = this.buckets.get(k)
      if (!arr) this.buckets.set(k, (arr = []))
      arr.push(i)
    }
  }
  get length() { return this.cum[this.cum.length - 1] }
  /** distance to the line (exact within `range`, else returns range) and arc position */
  query(x: number, z: number, range = 120): { d: number; s: number } {
    if (x < this.minX - range || x > this.maxX + range || z < this.minZ - range || z > this.maxZ + range) return { d: range, s: 0 }
    const cx = Math.floor(x / this.cell), cz = Math.floor(z / this.cell)
    const r = Math.ceil(range / this.cell)
    let best = range, bs = 0
    for (let i = -r; i <= r; i++) for (let j = -r; j <= r; j++) {
      const arr = this.buckets.get((cx + i) * 100003 + cz + j)
      if (!arr) continue
      for (const k of arr) {
        const [ax, az] = this.pts[k], [bx, bz] = this.pts[k + 1]
        const dx = bx - ax, dz = bz - az
        const l2 = dx * dx + dz * dz || 1
        const t = clamp(((x - ax) * dx + (z - az) * dz) / l2)
        const px = ax + dx * t, pz = az + dz * t
        const d = Math.hypot(x - px, z - pz)
        if (d < best) { best = d; bs = this.cum[k] + t * Math.sqrt(l2) }
      }
    }
    return { d: best, s: bs }
  }
  /** point + tangent at arc length s */
  at(s: number): { x: number; z: number; tx: number; tz: number } {
    s = clamp(s, 0, this.length)
    let lo = 0, hi = this.cum.length - 1
    while (hi - lo > 1) { const m = (lo + hi) >> 1; if (this.cum[m] <= s) lo = m; else hi = m }
    const a = this.pts[lo], b = this.pts[hi]
    const seg = this.cum[hi] - this.cum[lo] || 1
    const t = (s - this.cum[lo]) / seg
    const tx = (b[0] - a[0]) / seg, tz = (b[1] - a[1]) / seg
    return { x: lerp(a[0], b[0], t), z: lerp(a[1], b[1], t), tx, tz }
  }
}

// House of Pizz is the world origin. Its door faces +Z (south).
export const RIVER = new Polyline([
  [-2600, -2300], [-1500, -1150], [-820, -560], [-420, -230], [-210, -110], [-95, -62], [0, -58], [70, -66], [140, -52], [205, -30],
])
export const RIVER2 = new Polyline([
  [300, 10], [420, 120], [620, 300], [980, 640], [1700, 1300], [2600, 2200],
])
export const LAKE = { x: 255, z: -5, r: 62 }

export const ROAD = new Polyline([
  [-1400, 260], [-760, 120], [-380, 52], [-170, 30], [-60, 22], [0, 20], [70, 24], [150, 44], [230, 88], [330, 150], [520, 250], [900, 420], [1500, 700],
])
export const HOME_PATH = new Polyline([[0, 3.2], [0.6, 9], [-0.4, 14.5], [0, 20]], 1)

// ---------------------------------------------------------------- height
function riverHalfWidth(s: number, which: number) {
  return which === 0 ? 6.5 + 2.5 * n4(s / 90, 3.3) : 7.5 + 2 * n4(s / 90, 9.1)
}

export function rawHeight(x: number, z: number) {
  const r = Math.hypot(x, z)
  const wx = x + 70 * n1(x / 500, z / 500)
  const wz = z + 70 * n2(x / 500, z / 500)
  const hills = 3.2 * fbm(n1, wx / 210, wz / 210, 3) + 0.9 * n2(x / 48, z / 48)
  const ang = Math.atan2(z, x)
  const rw = r * (1 + 0.28 * n2(Math.cos(ang) * 1.3 + 7, Math.sin(ang) * 1.3 + 7)) + 90 * n1(wx / 260, wz / 260)
  const vm = smoothstep(620, 2000, rw)
  const ridge = ridged(wx / 1150, wz / 1150, 4)
  const far = smoothstep(2400, 5500, r)
  const massif = Math.max(0, fbm(n1, wx / 1500 + 20, wz / 1500 - 20, 4) * 0.5 + 0.55)
  const mountains = Math.pow(vm, 1.3) * (120 + 820 * massif * massif * (0.75 + 0.35 * ridge) + 300 * far * massif) + vm * 50 * fbm(n4, x / 300, z / 300, 3)
  let h = 1.6 + hills + mountains
  // gentle rolling meadows inside the valley
  h += (1 - vm) * 2.2 * Math.max(0, n4(wx / 120, wz / 120))
  h += smoothstep(260, 700, rw) * 26 * Math.max(0, fbm(n2, wx / 260 + 3, wz / 260, 3) + 0.15)
  // keep a calm clearing around the founder's house
  h = lerp(h, 1.25 + 0.25 * hills, smoothstep(78, 22, r))
  return h
}

/** low-frequency height used to smooth roads */
function smoothHeight(x: number, z: number) {
  return rawHeight(x, z) * 0.0 + rawHeightLow(x, z)
}
function rawHeightLow(x: number, z: number) {
  const r = Math.hypot(x, z)
  const wx = x + 70 * n1(x / 500, z / 500)
  const wz = z + 70 * n2(x / 500, z / 500)
  const hills = 3.2 * fbm(n1, wx / 210, wz / 210, 3)
  const ang = Math.atan2(z, x)
  const rw = r * (1 + 0.28 * n2(Math.cos(ang) * 1.3 + 7, Math.sin(ang) * 1.3 + 7)) + 90 * n1(wx / 260, wz / 260)
  const vm = smoothstep(620, 2000, rw)
  let h = 1.6 + hills + Math.pow(vm, 1.25) * 160 + smoothstep(260, 700, rw) * 26 * Math.max(0, fbm(n2, wx / 260 + 3, wz / 260, 3) + 0.15)
  h = lerp(h, 1.25 + 0.25 * hills, smoothstep(78, 22, r))
  return h
}

export function heightAt(x: number, z: number) {
  let h = rawHeight(x, z)
  // roads & home path: flatten towards a smooth profile
  const rd = ROAD.query(x, z, 14).d
  if (rd < 14) h = lerp(h, smoothHeight(x, z), smoothstep(12, 3.5, rd))
  const hp = HOME_PATH.query(x, z, 6).d
  if (hp < 6) h = lerp(h, 1.25, smoothstep(5, 1.5, hp) * 0.6)
  // rivers
  for (let w = 0; w < 2; w++) {
    const line = w === 0 ? RIVER : RIVER2
    const q = line.query(x, z, 160)
    if (q.d < 160) {
      const hw = riverHalfWidth(q.s, w)
      const bankW = 14 + Math.max(0, h) * 0.9
      if (q.d < hw + bankW) {
        const target = q.d < hw ? WATER_LEVEL - 1.9 * (1 - (q.d / hw) ** 2) : WATER_LEVEL + (q.d - hw) * 0.22
        const t = smoothstep(hw + bankW, hw * 0.7, q.d)
        h = Math.min(h, lerp(h, target, t))
      }
    }
  }
  // lake
  const ld = Math.hypot(x - LAKE.x, (z - LAKE.z) * 1.25)
  const lr = LAKE.r * (1 + 0.18 * n4(x / 40, z / 40))
  if (ld < lr + 40) {
    const target = ld < lr ? WATER_LEVEL - 2.6 * (1 - (ld / lr) ** 2) : WATER_LEVEL + (ld - lr) * 0.12
    h = Math.min(h, lerp(h, target, smoothstep(lr + 40, lr * 0.8, ld)))
  }
  return h
}

export function slopeAt(x: number, z: number, e = 1.5) {
  const hx = heightAt(x + e, z) - heightAt(x - e, z)
  const hz = heightAt(x, z + e) - heightAt(x, z - e)
  return Math.hypot(hx, hz) / (2 * e)
}

export function waterDist(x: number, z: number) {
  const a = RIVER.query(x, z, 60).d - 8
  const b = RIVER2.query(x, z, 60).d - 8
  const c = Math.hypot(x - LAKE.x, (z - LAKE.z) * 1.25) - LAKE.r * 1.15
  return Math.min(a, b, c)
}

/** forest density 0..1 (deterministic) */
export function forestDensity(x: number, z: number) {
  const v = fbm(n2, x / 260 + 11, z / 260 - 4, 3)
  return smoothstep(-0.05, 0.45, v)
}

export function detailNoise(x: number, z: number) {
  return n3(x / 9, z / 9)
}

/** smooth "world warp": grid coordinate u∈[-1,1] → world meters, dense in the centre */
const WARP_K = 5.5
export function warp(u: number) {
  return (Math.sinh(WARP_K * u) / Math.sinh(WARP_K)) * (TERRAIN_SIZE / 2)
}
