import { Terrain } from './Terrain'
import { WaterSurface } from './Water'
import { Atmosphere } from './Atmosphere'
import { Trees, Grass, Rocks } from './Vegetation'
import { Roads } from './Roads'
import { Clouds, Birds } from './Ambient'
import { params } from '../engine/clock'

const off = new Set((params.get('off') ?? '').split(','))

/** the static natural world (deterministic from WORLD_SEED) */
export function NatureWorld() {
  return (
    <>
      <Atmosphere />
      {!off.has('terrain') && <Terrain />}
      {!off.has('water') && <WaterSurface />}
      {!off.has('roads') && <Roads />}
      {!off.has('trees') && <Trees />}
      {!off.has('grass') && <Grass />}
      {!off.has('rocks') && <Rocks />}
      {!off.has('clouds') && <Clouds />}
      {!off.has('birds') && <Birds />}
    </>
  )
}
