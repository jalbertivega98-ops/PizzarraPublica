// Shared mutable world/scene state read by components every frame,
// plus the camera-path machinery used by episodes.
import * as THREE from 'three'
import { ease } from './clock'

export const world = {
  hour: 15.6,
  cycle: false, // live day/night cycle
  focus: new THREE.Vector3(0, 0, 0),
  shadowSpan: 45,
  fogColor: new THREE.Color('#cfe0ee'),
  sunDir: new THREE.Vector3(0, 1, 0),
}

// ------------------------------------------------------------ camera paths
export type CamKey = { t: number; p: [number, number, number]; l: [number, number, number]; fov?: number; e?: keyof typeof ease | 'linear' }

const v3 = new THREE.Vector3()
function catmull(p0: number, p1: number, p2: number, p3: number, t: number) {
  const t2 = t * t, t3 = t2 * t
  return 0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3)
}

/** evaluates a keyframed camera at time t. Segments use their end key's easing. */
export function evalCam(keys: CamKey[], t: number, outP: THREE.Vector3, outL: THREE.Vector3): number {
  if (t <= keys[0].t) { outP.set(...keys[0].p); outL.set(...keys[0].l); return keys[0].fov ?? 45 }
  const last = keys[keys.length - 1]
  if (t >= last.t) { outP.set(...last.p); outL.set(...last.l); return last.fov ?? 45 }
  let i = 0
  while (keys[i + 1].t < t) i++
  const a = keys[i], b = keys[i + 1]
  const k0 = keys[Math.max(0, i - 1)], k3 = keys[Math.min(keys.length - 1, i + 2)]
  let u = (t - a.t) / (b.t - a.t)
  const e = b.e ?? 'inOut'
  u = e === 'linear' ? u : ease[e](u)
  // smooth when the neighbour keys are part of the same "move"
  for (let c = 0; c < 3; c++) {
    outP.setComponent(c, catmull(k0.p[c], a.p[c], b.p[c], k3.p[c], u))
    outL.setComponent(c, catmull(k0.l[c], a.l[c], b.l[c], k3.l[c], u))
  }
  return THREE.MathUtils.lerp(a.fov ?? 45, b.fov ?? 45, u)
}

/** point-in-time helpers for timelines */
export const between = (t: number, a: number, b: number) => t >= a && t < b
export const vec = (x: number, y: number, z: number) => v3.set(x, y, z)
