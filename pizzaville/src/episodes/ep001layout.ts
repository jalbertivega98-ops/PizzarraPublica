// Episodio 1: Europa en la orilla de Pizz (junto al camino), América al otro lado del río.
import { plotSlots, valid, footprintHeight } from '../world/plots'
import { RIVER } from '../world/terrain'

export type Lot = { x: number; z: number; y: number; rot: number }

export function europeLots(n: number): Lot[] {
  return plotSlots().slice(0, n).map((s) => ({ x: s.x, z: s.z, y: s.y, rot: s.rot }))
}

/** plots on the far bank of the river (north), houses facing the river */
export function americaLots(n: number): Lot[] {
  const out: Lot[] = []
  const s0 = RIVER.query(0, -58, 50).s
  for (let m = 0; m < 80 && out.length < n; m++) {
    for (const dir of m === 0 ? [0] : [1, -1]) {
      const p = RIVER.at(s0 + dir * m * 15)
      // north normal (away from Pizz's house)
      let nx = p.tz, nz = -p.tx
      if (nz > 0) { nx = -nx; nz = -nz }
      for (const off of [24, 42]) {
        const x = p.x + nx * off, z = p.z + nz * off
        if (!valid(x, z)) continue
        if (out.some((o) => Math.hypot(o.x - x, o.z - z) < 12)) continue
        out.push({ x, z, y: footprintHeight(x, z), rot: Math.atan2(-nx, -nz) })
        if (out.length >= n) break
      }
    }
  }
  return out
}
