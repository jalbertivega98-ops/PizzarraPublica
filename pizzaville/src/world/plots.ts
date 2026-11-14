// Deterministic urban layout: plot slots along the main road, ordered by
// distance to Pizz's house. Shared by the scene and the persistence API.
import { ROAD, heightAt, waterDist, slopeAt, WATER_LEVEL } from './terrain'

export type PlotSlot = { index: number; id: string; x: number; z: number; y: number; rot: number; side: number; s: number }

export const PIZZ_HOUSE = { x: 0, z: 0, rot: 0 }
export const SIGN_POS = { x: 4.6, z: 16.2 }
const SPACING = 15
const OFFSET = 12.5

let cache: PlotSlot[] | null = null

export function plotSlots(): PlotSlot[] {
  if (cache) return cache
  const s0 = ROAD.query(0, 0, 60).s
  const out: PlotSlot[] = []
  for (let m = 0; m < 160 && out.length < 400; m++) {
    for (const dir of m === 0 ? [0] : [1, -1]) {
      const s = s0 + dir * m * SPACING
      if (s < 10 || s > ROAD.length - 10) continue
      const p = ROAD.at(s)
      // normal pointing "north" side (towards -z-ish) and south side
      const nx = p.tz, nz = -p.tx
      for (const side of [1, -1]) {
        if (m === 0 && side === 1) continue // that's Pizz's own house
        const x = p.x + nx * OFFSET * side, z = p.z + nz * OFFSET * side
        if (!valid(x, z)) continue
        if (Math.hypot(x - PIZZ_HOUSE.x, z - PIZZ_HOUSE.z) < 13) continue
        if (Math.hypot(x - SIGN_POS.x, z - SIGN_POS.z) < 8) continue
        // house front faces the road
        const rot = Math.atan2(-nx * side, -nz * side)
        const id = `p${m}${dir < 0 ? 'w' : 'e'}${side > 0 ? 'n' : 's'}`
        out.push({ index: out.length, id, x, z, y: footprintHeight(x, z), rot, side, s })
      }
    }
  }
  cache = out
  return out
}

function valid(x: number, z: number) {
  if (waterDist(x, z) < 7) return false
  let lo = Infinity, hi = -Infinity
  for (const [dx, dz] of [[-4, -4], [4, -4], [-4, 4], [4, 4], [0, 0]]) {
    const h = heightAt(x + dx, z + dz)
    lo = Math.min(lo, h); hi = Math.max(hi, h)
  }
  if (lo < WATER_LEVEL + 0.8) return false
  if (hi - lo > 2.2) return false
  if (slopeAt(x, z, 3) > 0.35) return false
  return true
}

export function footprintHeight(x: number, z: number) {
  let lo = Infinity
  for (const [dx, dz] of [[-3, -3], [3, -3], [-3, 3], [3, 3], [0, 0]]) lo = Math.min(lo, heightAt(x + dx, z + dz))
  return lo
}

/** keep the first slots free of trees and rocks */
export function reservedAt(x: number, z: number, n = 70) {
  const slots = plotSlots()
  for (let i = 0; i < Math.min(n, slots.length); i++) {
    const s = slots[i]
    if (Math.abs(s.x - x) < 9 && Math.abs(s.z - z) < 9) return true
  }
  if (Math.hypot(x - SIGN_POS.x, z - SIGN_POS.z) < 3) return true
  return false
}
