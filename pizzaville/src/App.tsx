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
import { Ep001 } from './episodes/ep001'
import { Ep002 } from './episodes/ep002'
import { Ep003 } from './episodes/ep003'
import { Ep004 } from './episodes/ep004'
import { Pareja01 } from './episodes/pareja01'
import { Pareja01v2 } from './episodes/pareja01v2'
import { Pareja02 } from './episodes/pareja02'
import { Pareja03 } from './episodes/pareja03'
import { Pareja04 } from './episodes/pareja04'
import { Pareja05 } from './episodes/pareja05'
import { Pareja06 } from './episodes/pareja06'
import { Pareja07 } from './episodes/pareja07'
import { Pareja08 } from './episodes/pareja08'
import { Pareja09 } from './episodes/pareja09'
import { Pareja10 } from './episodes/pareja10'
import { Pareja11 } from './episodes/pareja11'
import { Pareja12 } from './episodes/pareja12'
import { Pareja13 } from './episodes/pareja13'
import { Pareja14 } from './episodes/pareja14'
import { Pareja15 } from './episodes/pareja15'
import { Town } from './scene/Town'
import { Panel } from './ui/Panel'
import { useStore } from './state/store'
import { walk } from './engine/motion'
import { seg } from './engine/clock'

const EPISODE = params.get('episode')

function Ticker() {
  useFrame((_, d) => {
    tickLive(d)
    const n = skyAt(world.hour).night
    for (const nm of nightMats) nm.m.emissiveIntensity = nm.day + (nm.night - nm.day) * n
  })
  return null
}

function LivePizz() {
  const st = useMemo(newState, [])
  useFrame(() => {
    const t = clock.t
    // a calm loop in his garden: walk, stop, wave now and then
    const cyc = t % 24
    const pts: [number, number][] = [[0.2, 5.3], [3.2, 6.2], [-2.6, 6.6], [0.2, 5.3]]
    walk(st, pts, Math.floor(t / 24) * 24 + 4, 1.1, t)
    if (st.y < HOME_Y) st.y = HOME_Y
    if (cyc < 4) { st.ry = 0; st.action = 'wave'; st.actionT = t; st.actionW = seg(cyc, 0.5, 0.8) * (1 - seg(cyc, 2.8, 3.2)) }
    else { st.action = 'none'; st.actionW = 0 }
  })
  return <Character look={PIZZ_LOOK} state={st} />
}

function CameraFly() {
  const { camera, controls } = useThree() as unknown as { camera: THREE.PerspectiveCamera; controls: { target: THREE.Vector3; update: () => void } | null }
  const focus = useStore((s) => s.focus)
  const from = useMemo(() => ({ p: new THREE.Vector3(), t: new THREE.Vector3() }), [])
  useMemo(() => { if (controls) { from.p.copy(camera.position); from.t.copy(controls.target) } }, [focus])
  useFrame(() => {
    if (!focus || !controls) { if (controls) world.focus.copy(controls.target); return }
    const k = Math.min(1, (performance.now() - focus.at) / 1600)
    const e = k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2
    const tgt = new THREE.Vector3(focus.x, focus.y + 2, focus.z)
    const pos = tgt.clone().add(new THREE.Vector3(14, 10, 18))
    controls.target.lerpVectors(from.t, tgt, e)
    camera.position.lerpVectors(from.p, pos, e)
    controls.update()
    world.focus.copy(controls.target)
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
    const [px, py, pz, lx, ly, lz] = (shot ?? '22,14,34,0,2,8').split(',').map(Number)
    camera.position.set(px, py, pz)
    camera.lookAt(lx, ly, lz)
    world.focus.set(lx, 0, lz)
    ;(camera as THREE.PerspectiveCamera).fov = Number(params.get('fov') ?? 45)
    camera.updateProjectionMatrix()
  }, [])
  const [lx, ly, lz] = (shot ?? '22,14,34,0,2,8').split(',').map(Number).slice(3)
  return params.get('orbit') === '0' ? null : <OrbitControls target={[lx, ly, lz]} makeDefault maxPolarAngle={1.45} minDistance={3} maxDistance={1500} enableDamping />
}

// exporter hook: deterministic single-frame rendering
if (RECORD) {
  ;(window as any).__store = useStore
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
    <>
    <Canvas shadows={{ type: THREE.PCFShadowMap }} frameloop={RECORD ? 'never' : 'always'} gl={{ antialias: true, preserveDrawingBuffer: true }} dpr={1} camera={{ fov: 45, near: 0.1, far: 20000 }}>
      <Ticker />
      {EPISODE ? <EpisodeHooks /> : <DebugCam />}
      {!EPISODE?.startsWith('pareja') && <NatureWorld />}
      {!EPISODE?.startsWith('pareja') && <Sign />}
      {EPISODE === 'pareja15' ? <Pareja15 /> : EPISODE === 'pareja14' ? <Pareja14 /> : EPISODE === 'pareja13' ? <Pareja13 /> : EPISODE === 'pareja12' ? <Pareja12 /> : EPISODE === 'pareja11' ? <Pareja11 /> : EPISODE === 'pareja05' ? <Pareja05 /> : EPISODE === 'pareja06' ? <Pareja06 /> : EPISODE === 'pareja07' ? <Pareja07 /> : EPISODE === 'pareja08' ? <Pareja08 /> : EPISODE === 'pareja09' ? <Pareja09 /> : EPISODE === 'pareja10' ? <Pareja10 /> : EPISODE === 'pareja02' ? (
        <Pareja02 />
      ) : EPISODE === 'pareja03' ? (
        <Pareja03 />
      ) : EPISODE === 'pareja04' ? (
        <Pareja04 />
      ) : EPISODE === 'pareja01v2' ? (
        <Pareja01v2 />
      ) : EPISODE === 'pareja01' ? (
        <Pareja01 />
      ) : EPISODE === 'ep000' ? (
        <Ep000 />
      ) : EPISODE === 'ep004' ? (
        <Ep004 />
      ) : EPISODE === 'ep003' ? (
        <Ep003 />
      ) : EPISODE === 'ep002' ? (
        <Ep002 />
      ) : EPISODE === 'ep001' ? (
        <Ep001 />
      ) : (
        <>
          <PizzHome />
          {RECORD ? <Character look={PIZZ_LOOK} state={pizz} /> : <LivePizz />}
          <Town />
          <CameraFly />
        </>
      )}
    </Canvas>
    {!RECORD && !EPISODE && <Panel />}
    </>
  )
}
