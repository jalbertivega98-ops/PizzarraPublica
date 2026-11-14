// Path walking for characters: position/heading/gait as a pure function of time.
import { heightAt } from '../world/terrain'
import type { CharState } from '../scene/Character'

export type Pt = [number, number]

export function pathLength(pts: Pt[]) {
  let L = 0
  for (let i = 1; i < pts.length; i++) L += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1])
  return L
}

export function pointAt(pts: Pt[], d: number): { x: number; z: number; hx: number; hz: number } {
  for (let i = 1; i < pts.length; i++) {
    const [ax, az] = pts[i - 1], [bx, bz] = pts[i]
    const l = Math.hypot(bx - ax, bz - az)
    if (d <= l || i === pts.length - 1) {
      const t = Math.min(1, Math.max(0, d / (l || 1)))
      return { x: ax + (bx - ax) * t, z: az + (bz - az) * t, hx: (bx - ax) / (l || 1), hz: (bz - az) / (l || 1) }
    }
    d -= l
  }
  const p = pts[pts.length - 1]
  return { x: p[0], z: p[1], hx: 0, hz: 1 }
}

/** walk along pts starting at t0 with speed (m/s), with ease-in/out of 0.4 s. Writes into st. Returns true while moving. */
export function walk(st: CharState, pts: Pt[], t0: number, speed: number, t: number, yOffset = 0) {
  const L = pathLength(pts)
  const dur = L / speed + 0.4
  const lt = Math.min(Math.max(t - t0, 0), dur)
  // distance with smooth accel/decel
  const acc = 0.4
  let d: number
  if (lt < acc) d = (speed * lt * lt) / (2 * acc)
  else if (lt > dur - acc) { const r = dur - lt; d = L - (speed * r * r) / (2 * acc) }
  else d = speed * (lt - acc / 2)
  d = Math.min(L, Math.max(0, d))
  const p = pointAt(pts, d)
  st.x = p.x; st.z = p.z; st.y = heightAt(p.x, p.z) + yOffset
  st.ry = Math.atan2(p.hx, p.hz)
  const moving = t > t0 && t < t0 + dur
  const v = !moving ? 0 : lt < acc ? speed * lt / acc : lt > dur - acc ? speed * (dur - lt) / acc : speed
  st.speed = v
  const stride = speed > 2.2 ? 2.3 : 1.35
  st.phase = (d / stride) * Math.PI * 2
  return moving
}

/** smoothly turn heading towards a target angle */
export function turnTo(from: number, to: number, k: number) {
  let d = to - from
  while (d > Math.PI) d -= Math.PI * 2
  while (d < -Math.PI) d += Math.PI * 2
  return from + d * Math.min(1, Math.max(0, k))
}
