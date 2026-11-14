import { Canvas, useFrame, useThree, advance } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'
import * as THREE from 'three'
import { useMemo } from 'react'
import { NatureWorld } from './scene/World'
import { PizzHome, Sign, HOME_Y } from './scene/PizzHome'
import { Character, PIZZ_LOOK, newState } from './scene/Character'
import { params, tickLive, clock, RECORD, setTime, whenReady } from './engine/clock'
import { nightMats } from './scene/materials'
import { world } from './engine/director'
import { skyAt } from './scene/Atmosphere'
import { Ep000 } from './episodes/ep000'

const EPISODE = params.get('episode')

function Ticker() {
  useFrame((_, d) => {
    tickLive(d)
    const n = skyAt(world.hour).night
    for (const nm of nightMats) nm.m.emissiveIntensity = nm.day + (nm.night - nm.day) * n
  })
  return null
}

function DebugCam() {
  const { camera } = useThree()
  const shot = params.get('cam')
  useMemo(() => {
    if (RECORD) (window as any).__pv.setCam = (c: number[]) => {
      camera.position.set(c[0], c[1], c[2]); camera.lookAt(c[3], c[4], c[5]); world.focus.set(c[3], 0, c[5])
      ;(camera as THREE.PerspectiveCamera).fov = c[6] ?? 45; camera.updateProjectionMatrix()
    }
    const [px, py, pz, lx, ly, lz] = (shot ?? '9,3.2,16,0,1.6,3').split(',').map(Number)
    camera.position.set(px, py, pz)
    camera.lookAt(lx, ly, lz)
    world.focus.set(lx, 0, lz)
    ;(camera as THREE.PerspectiveCamera).fov = Number(params.get('fov') ?? 45)
    camera.updateProjectionMatrix()
  }, [])
  const [lx, ly, lz] = (shot ?? '9,3.2,16,0,1.6,3').split(',').map(Number).slice(3)
  return params.get('orbit') === '0' ? null : <OrbitControls target={[lx, ly, lz]} makeDefault />
}

// exporter hook: deterministic single-frame rendering
if (RECORD) {
  ;(window as any).__pv = {
    ready: () => whenReady(),
    renderAt: (t: number) => { setTime(t); advance(performance.now()); return true },
  }
}

function EpisodeHooks() {
  useMemo(() => { if (RECORD) (window as any).__pv.setCam = () => {} }, [])
  return null
}

export default function App() {
  const pizz = useMemo(() => { const s = newState(); s.x = 0.4; s.z = 5.6; s.y = HOME_Y; s.ry = 0.25; return s }, [])
  if (params.get('hour')) world.hour = Number(params.get('hour'))
  if (params.get('t')) clock.t = Number(params.get('t'))
  return (
    <Canvas shadows={{ type: THREE.PCFShadowMap }} frameloop={RECORD ? 'never' : 'always'} gl={{ antialias: true, preserveDrawingBuffer: true }} dpr={1} camera={{ fov: 45, near: 0.1, far: 20000 }}>
      <Ticker />
      {EPISODE ? <EpisodeHooks /> : <DebugCam />}
      <NatureWorld />
      <Sign />
      {EPISODE === 'ep000' ? (
        <Ep000 />
      ) : (
        <>
          <PizzHome />
          <Character look={PIZZ_LOOK} state={pizz} />
        </>
      )}
    </Canvas>
  )
}
