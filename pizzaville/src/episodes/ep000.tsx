// EPISODIO 0 — «Bienvenido a Pizzaville». Everything is a pure function of the
// episode time `t`, so the exporter can render any frame in any order.
import { useMemo, useRef } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { Billboard, Text } from '@react-three/drei'
import * as THREE from 'three'
import { clock, ease, seg } from '../engine/clock'
import { evalCam, world, type CamKey } from '../engine/director'
import { useLines, mouthAt, speakingAt } from '../engine/voice'
import { walk, turnTo, type Pt } from '../engine/motion'
import { Character, PIZZ_LOOK, WORKER_LOOK, lookFromSeed, newState, type CharState } from '../scene/Character'
import { House, houseSpecFromSeed } from '../scene/House'
import { PizzHome, HOME_Y } from '../scene/PizzHome'
import { ConstructionSite } from '../scene/Construction'
import { plotSlots } from '../world/plots'
import { ROAD, heightAt } from '../world/terrain'
import { mat } from '../scene/materials'

export const EP000 = {
  id: 'ep000',
  duration: 60,
  script: [
    { id: 'l01', at: 4.9, text: '¡Eh, tú! ¡Sí, tú! ¡Ven, que te enseño una cosa!' },
    { id: 'l02', at: 11.0, text: 'Soy Pizz, y bienvenido a Pizzaville.' },
    { id: 'l03', at: 14.2, text: 'Ahora mismo vivo aquí completamente solo. Tengo mi casita, un montón de terreno... y absolutamente ningún vecino.' },
    { id: 'l04', at: 22.0, text: 'Pero quiero convertir todo esto en una ciudad enorme. ¡Y necesito vuestra ayuda!' },
    { id: 'l05', at: 27.8, text: 'Cada persona que comente su nombre y su país podrá convertirse en un nuevo habitante.' },
    { id: 'l06', at: 32.8, text: 'Lo veremos llegar, construir su casa... ¡y colocar su bandera!' },
    { id: 'l07', at: 40.3, text: 'Vamos a actualizar Pizzaville dos veces al día, para que veáis cómo crece.' },
    { id: 'l08', at: 45.1, text: 'Empezaremos con unas pocas casas. Después, calles, tiendas, parques... ¡y barrios enteros!' },
    { id: 'l09', at: 52.9, text: 'Así que dime de dónde eres, y ayúdame a construir Pizzaville.' },
    { id: 'l10', at: 57.0, text: '¡Nos vemos en la próxima actualización!' },
  ],
}

// ---------------------------------------------------------------- layout
const PZ = { x: 0.15, z: 5.3 } // Pizz's mark in front of his door
const headY = HOME_Y + 1.62
const slot = () => plotSlots()[0]
const DEMO_SEED = 7711
const BUILD = { start: 29.4, dur: 9.0 }

function doorOf(s: { x: number; z: number; rot: number }, dist: number): Pt {
  return [s.x + Math.sin(s.rot) * dist, s.z + Math.cos(s.rot) * dist]
}

// ---------------------------------------------------------------- camera
function cameraKeys(): CamKey[] {
  const s = slot()
  const H = headY
  const F = [Math.sin(s.rot), Math.cos(s.rot)], R = [Math.cos(s.rot), -Math.sin(s.rot)]
  const at = (f: number, r: number, y: number): [number, number, number] => [s.x + F[0] * f + R[0] * r, s.y + y, s.z + F[1] * f + R[1] * r]
  const spec = houseSpecFromSeed(DEMO_SEED)
  const fl = [s.x - R[0] * (spec.w / 2 + 1.1) + F[0] * (spec.d / 2 + 1.6), s.z - R[1] * (spec.w / 2 + 1.1) + F[1] * (spec.d / 2 + 1.6)]
  return [
    // 0–3 s: aerial → house, fast and smooth
    { t: 0, p: [-520, 330, 760], l: [0, 20, 0], fov: 46 },
    { t: 1.2, p: [-160, 95, 260], l: [0, 6, 2], fov: 44, e: 'linear' },
    { t: 2.25, p: [-22, 14, 38], l: [0, 2.8, 2], fov: 42, e: 'linear' },
    { t: 3.0, p: [3.2, 3.6, 13.5], l: [0.2, 2.4, 2.5], fov: 40, e: 'out' },
    // 3–8: door opens, Pizz walks out, looks up and waves
    { t: 4.6, p: [2.0, 3.0, 11.4], l: [0.2, 2.2, 4.5], fov: 38 },
    { t: 8.0, p: [0.9, 2.55, 9.2], l: [PZ.x, H - 0.1, PZ.z], fov: 36 },
    { t: 11.5, p: [-0.4, 2.45, 8.8], l: [PZ.x, H - 0.1, PZ.z], fov: 34 },
    // over-the-shoulder panorama of the valley (east)
    { t: 11.6, p: [-2.6, 3.2, 4.3], l: [40, 4, 12], fov: 52, cut: true },
    { t: 16.0, p: [-3.6, 4.4, 3.8], l: [50, 8, 16], fov: 52 },
    // crane around the lonely house
    { t: 16.1, p: [22, 9, 26], l: [0, 2.5, 0], fov: 45, cut: true },
    { t: 19.5, p: [-16, 15, 26], l: [0, 2.5, 0], fov: 45, e: 'linear' },
    // back to Pizz, he asks for help
    { t: 19.6, p: [1.4, 2.5, 10.2], l: [PZ.x, H - 0.05, PZ.z], fov: 38, cut: true },
    { t: 25.0, p: [0.6, 2.4, 9.2], l: [PZ.x, H, PZ.z], fov: 36 },
    // 25.1–29.4: follow the newcomer (handled in code), then the works
    { t: 29.4, p: at(12, 8, 4.5), l: [s.x, s.y + 1.5, s.z], fov: 46, cut: true },
    { t: 33.5, p: at(12, -9, 7), l: [s.x, s.y + 2.5, s.z], fov: 44 },
    { t: 38.6, p: at(10, -6, 4.5), l: [fl[0], s.y + 2.6, fl[1]], fov: 44 },
    { t: 40.2, p: at(8.5, -3.5, 3.8), l: [fl[0], s.y + 3.6, fl[1]], fov: 40 },
    // valley flyover with free plots
    { t: 40.3, p: [-34, 34, 66], l: [24, 0, 24], fov: 50, cut: true },
    { t: 50.2, p: [62, 28, 74], l: [0, 0, 22], fov: 50, e: 'linear' },
    // Pizz close, asks for comments
    { t: 50.3, p: [0.8, 2.5, 9.0], l: [PZ.x, H - 0.05, PZ.z], fov: 36, cut: true },
    { t: 55.0, p: [0.3, 2.45, 8.4], l: [PZ.x, H - 0.05, PZ.z], fov: 34 },
    // pull back to the single house in the huge valley
    { t: 56.4, p: [3, 6, 19], l: [0, 2, 2], fov: 40, e: 'in' },
    { t: 60, p: [110, 210, 420], l: [0, 0, 0], fov: 46, e: 'out' },
  ]
}

// ---------------------------------------------------------------- component
export function Ep000({ startAt = 0 }: { startAt?: number }) {
  const { camera } = useThree()
  const lines = useMemo(() => useLines(EP000.id, EP000.script), [])
  const keys = useMemo(cameraKeys, [])
  const pizz = useMemo(newState, [])
  const guest = useMemo(newState, [])
  const workers = useMemo(() => [newState(), newState(), newState()], [])
  const P = useMemo(() => new THREE.Vector3(), [])
  const L = useMemo(() => new THREE.Vector3(), [])
  const s = slot()
  const spec = useMemo(() => houseSpecFromSeed(DEMO_SEED), [])
  const demoRef = useRef<THREE.Group>(null!)
  const markers = useRef<THREE.Group>(null!)
  const guestLabel = useRef<THREE.Group>(null!)
  const camPos = useMemo(() => new THREE.Vector3(), [])

  const T = () => clock.t - startAt
  const progress = () => Math.min(1, Math.max(0, (T() - BUILD.start) / BUILD.dur))
  const door = () => {
    const t = T()
    return t < 3.0 ? 0 : t < 5.6 ? ease.out(seg(t, 3.0, 3.6)) : 1 - ease.inOut(seg(t, 5.6, 6.4))
  }
  const sRoad = ROAD.query(s.x, s.z, 40).s
  const guestPath: Pt[] = useMemo(() => {
    const pts: Pt[] = []
    for (let d = 70; d >= 0; d -= 5) { const p = ROAD.at(sRoad + d); pts.push([p.x, p.z]) }
    pts.push(doorOf(s, 3.2 + spec.d / 2 + 2.5))
    pts.push(doorOf(s, spec.d / 2 + 1.6))
    return pts
  }, [])

  useMemo(() => {
    const pv = (window as any).__pv
    if (!pv) return
    pv.info = () => {
      const b = BUILD.start, d = BUILD.dur
      const sfx: { type: string; at: number; g?: number }[] = [
        { type: 'whoosh', at: 0.0, g: 0.7 }, { type: 'door', at: 3.0 }, { type: 'pop', at: 5.0, g: 0.35 },
        { type: 'whoosh', at: 11.45, g: 0.35 }, { type: 'whoosh', at: 15.95, g: 0.35 }, { type: 'chime', at: 22.7, g: 0.35 },
        { type: 'pop', at: b, g: 0.5 }, { type: 'thud', at: b + d * 0.06 }, { type: 'thud', at: b + d * 0.09 },
        { type: 'thud', at: b + d * 0.14 }, { type: 'thud', at: b + d * 0.5, g: 0.7 }, { type: 'thud', at: b + d * 0.57, g: 0.7 },
        { type: 'chime', at: b + d * 0.95, g: 0.6 }, { type: 'whoosh', at: 40.2, g: 0.6 }, { type: 'whoosh', at: 50.2, g: 0.4 }, { type: 'whoosh', at: 56.3, g: 0.6 },
      ]
      for (let k = 0; k < 10; k++) sfx.push({ type: 'pop', at: b + d * (0.64 + k * 0.012), g: 0.25 })
      for (let k = 0; k < 8; k++) sfx.push({ type: 'pop', at: 41 + k * 0.35, g: 0.3 })
      for (let tt = b + d * 0.2; tt < b + d * 0.62; tt += 0.27) sfx.push({ type: 'hammer', at: tt, g: 0.35 })
      return { id: EP000.id, duration: EP000.duration, lines: lines.map((l) => ({ id: l.id, at: l.at, dur: l.dur, text: l.text, words: l.words, hasAudio: l.hasAudio })), sfx }
    }
  }, [])
  useFrame(() => {
    const t = T()
    // ---------- camera
    const fov = evalCam(keys, t, P, L)

    camera.position.copy(P)
    camera.lookAt(L)
    const pc = camera as THREE.PerspectiveCamera
    if (Math.abs(pc.fov - fov) > 0.01) { pc.fov = fov; pc.updateProjectionMatrix() }
    camPos.copy(P)
    world.focus.set(L.x, 0, L.z)
    world.shadowSpan = THREE.MathUtils.clamp(P.distanceTo(L) * 0.9, 18, 90)

    // ---------- Pizz
    pizz.visible = true
    pizz.action = 'none'; pizz.actionW = 0; pizz.lookAt = null; pizz.brows = 0; pizz.smile = 0.7
    if (t < 3.3) { pizz.visible = t > 3.05; walk(pizz, [[PZ.x, 1.2], [PZ.x, PZ.z]], 99, 1, t) }
    else if (t < 5.4) walk(pizz, [[PZ.x, 1.2], [PZ.x, 2.9], [PZ.x, PZ.z]], 3.35, 2.3, t)
    else walk(pizz, [[PZ.x, 1.2], [PZ.x, PZ.z]], -10, 2, t)
    if (t >= 4.9 && t < 5.5) { pizz.action = 'surprise'; pizz.actionT = t - 4.9; pizz.actionW = ease.out(seg(t, 4.9, 5.05)) * (1 - seg(t, 5.35, 5.5)) }
    if (t >= 5.4 && t < 7.4) { pizz.action = 'wave'; pizz.actionT = t; pizz.actionW = seg(t, 5.4, 5.6) * (1 - seg(t, 7.2, 7.4)) }
    if (t >= 4.8 && t < 11.6) pizz.lookAt = camPos
    // talk gestures while speaking
    const sp = speakingAt(lines, t)
    if (sp && pizz.action === 'none' && pizz.speed < 0.2) { pizz.action = 'talk'; pizz.actionT = t; pizz.actionW = 0.85 }
    // pointing to the valley (east) while saying «un montón de terreno»
    if (t >= 11.6 && t < 19.5) {
      const k = ease.inOut(seg(t, 11.6, 12.4))
      pizz.ry = turnTo(0, Math.PI * 0.42, k)
      if (t > 13.2 && t < 16.4) { pizz.action = 'point'; pizz.actionT = t; pizz.actionW = seg(t, 13.2, 13.6) * (1 - seg(t, 16.0, 16.4)) }
      if (t > 17.0) { pizz.action = 'shrug'; pizz.actionW = seg(t, 17.0, 17.4) * (1 - seg(t, 18.6, 19.0)) }
    }
    if (t >= 19.5 && t < 25) {
      pizz.ry = 0.12
      pizz.lookAt = camPos
      if (t > 22.6 && t < 24.6) { pizz.action = 'celebrate'; pizz.actionT = t - 22.6; pizz.actionW = seg(t, 22.6, 22.8) * (1 - seg(t, 24.3, 24.6)) }
    }
    // 25–40: Pizz goes to the road to welcome the newcomer
    if (t >= 25 && t < 40.3) {
      walk(pizz, [[PZ.x, PZ.z], [0.4, 12], [-0.6, 17.4], [s.x - 3.4, 19.4]], 25.4, 1.6, t)
      if (t > 29.0 && t < 30.6) { pizz.action = 'wave'; pizz.actionT = t; pizz.actionW = seg(t, 29.0, 29.2) * (1 - seg(t, 30.4, 30.6)) }
      if (t > 30.6) { pizz.ry = turnTo(pizz.ry, Math.atan2(s.x - pizz.x, s.z - pizz.z), seg(t, 30.6, 31.2)); pizz.lookAt = new THREE.Vector3(s.x, s.y + 2.5, s.z) }
      if (t > 38.0) { pizz.action = 'celebrate'; pizz.actionT = t - 38; pizz.actionW = seg(t, 38.0, 38.2) }
    }
    if (t >= 40.3) {
      walk(pizz, [[PZ.x, 1.2], [PZ.x, PZ.z]], -10, 2, t)
      pizz.lookAt = t > 50 ? camPos : null
      if (t > 53.1 && t < 54.7) { pizz.action = 'point'; pizz.actionT = t; pizz.actionW = seg(t, 53.1, 53.4) * (1 - seg(t, 54.4, 54.7)); pizz.ry = 0.2 }
      if (t > 56.6) { pizz.action = 'wave'; pizz.actionT = t; pizz.actionW = seg(t, 56.6, 56.9) }
    }
    pizz.mouth = mouthAt(lines, t)
    if (pizz.y < HOME_Y) pizz.y = HOME_Y

    // ---------- guest (demo inhabitant)
    guest.visible = t > 25 && t < 40.2
    guest.action = 'none'; guest.actionW = 0; guest.lookAt = null; guest.mouth = 0
    if (guest.visible) {
      const moving = walk(guest, guestPath, 25.3, 1.9, t)
      if (!moving && t > 28 && t < 38.7) {
        // waits next to the plot, turned towards the works
        guest.ry = turnTo(guest.ry, Math.atan2(s.x - guest.x, s.z - guest.z), seg(t, 28.5, 29.5))
        if (t > 29 && t < 30.4) { guest.action = 'wave'; guest.actionT = t; guest.actionW = seg(t, 29, 29.2) * (1 - seg(t, 30.2, 30.4)) }
        if (t > 37.6) { guest.action = 'celebrate'; guest.actionT = t - 37.6; guest.actionW = seg(t, 37.6, 37.8) }
      }
      if (t >= 38.7) {
        const [dx, dz] = doorOf(s, spec.d / 2 + 1.6), [ix, iz] = doorOf(s, spec.d / 2 - 1.0)
        walk(guest, [[dx, dz], [ix, iz]], 38.8, 1.4, t)
        guest.visible = t < 40.0
      }
    }
    if (t >= 25.1 && t < 29.4) {
      // tracking shot alongside the newcomer
      L.set(guest.x, guest.y + 1.2, guest.z)
      const side = 0.9 - (t - 25.1) * 0.06
      P.set(guest.x + Math.cos(side) * 6.5, guest.y + 2.6, guest.z + Math.sin(side) * 6.5)
      camera.position.copy(P); camera.lookAt(L); world.focus.set(L.x, 0, L.z)
      const pc2 = camera as THREE.PerspectiveCamera
      if (pc2.fov !== 42) { pc2.fov = 42; pc2.updateProjectionMatrix() }
    }
    guestLabel.current.visible = t > 26 && t < 40.2
    guestLabel.current.position.set(guest.x, guest.y + 2.25, guest.z)

    // ---------- workers
    workers.forEach((w, i) => {
      const a = BUILD.start - 3.0 + i * 0.3
      const spot: Pt[] = [[-2.6, 3.2], [2.8, 2.6], [0.4, -3.6]]
      const c = Math.cos(s.rot), sn = Math.sin(s.rot)
      const [lx, lz] = spot[i]
      const wx = s.x + lx * c + lz * sn, wz = s.z - lx * sn + lz * c
      const from: Pt = [ROAD.at(sRoad - 9 - i * 2).x, ROAD.at(sRoad - 9 - i * 2).z]
      w.visible = t > a && t < BUILD.start + BUILD.dur * 0.9
      w.action = 'none'; w.actionW = 0
      if (!w.visible) return
      const moving = walk(w, [from, [wx, wz]], a, 3.2, t)
      if (!moving) {
        w.ry = Math.atan2(s.x - w.x, s.z - w.z)
        w.action = 'hammer'; w.actionT = t + i; w.actionW = 1
      }
    })

    // ---------- demo house & markers
    demoRef.current.visible = t > BUILD.start - 0.5 && t < 40.25
    markers.current.visible = t > 40.25 && t < 50.25
    markers.current.children.forEach((m, i) => {
      const k = ease.outBack(seg(t, 41 + i * 0.35, 41.6 + i * 0.35))
      m.scale.setScalar(Math.max(0.001, k))
      m.position.y = m.userData.y + Math.sin(clock.t * 2 + i) * 0.3
    })
  })

  const free = plotSlots().slice(1, 9)
  return (
    <group>
      <PizzHome getDoor={door} />
      <Character look={PIZZ_LOOK} state={pizz} />
      <Character look={lookFromSeed(DEMO_SEED)} state={guest} />
      {workers.map((w, i) => <Character key={i} look={WORKER_LOOK(90 + i)} state={w} scale={0.78} />)}
      <group ref={guestLabel}>
        <Billboard>
          <mesh position={[0, 0, -0.01]} material={mat('#1a2233', { transparent: true, opacity: 0.78 })}>
            <planeGeometry args={[1.5, 0.42]} />
          </mesh>
          <Text font="/fonts/fredoka600.woff" fontSize={0.24} color="#ffffff" anchorX="center" anchorY="middle" position={[0.18, 0, 0]}>
            Sofía
          </Text>
          <FlagChip iso="mx" position={[-0.45, 0, 0.005]} />
        </Billboard>
      </group>
      <group ref={demoRef} position={[s.x, s.y, s.z]} rotation-y={s.rot}>
        <House spec={spec} getProgress={progress} flag="mx" />
        <ConstructionSite spec={spec} getProgress={progress} />
      </group>
      <group ref={markers}>
        {free.map((f, i) => (
          <group key={f.id} position={[f.x, f.y + 9, f.z]} userData={{ y: f.y + 9 }}>
            <group scale={2.2}><PlotMarker /></group>
          </group>
        ))}
      </group>
    </group>
  )
}

import { flagTexture } from '../scene/Flag'
function FlagChip({ iso, position }: { iso: string; position: [number, number, number] }) {
  const m = useMemo(() => new THREE.MeshBasicMaterial({ map: flagTexture(iso), toneMapped: false }), [iso])
  return (
    <mesh position={position} material={m}>
      <planeGeometry args={[0.36, 0.27]} />
    </mesh>
  )
}

function PlotMarker() {
  return (
    <group>
      <Billboard>
        <mesh material={mat('#ffffff', { rough: 0.4 })} position={[0, 0, -0.02]}>
          <circleGeometry args={[1.5, 32]} />
        </mesh>
        <mesh material={mat('#ff7a3d', { rough: 0.4, emissive: '#ff7a3d', ei: 0.25 })} position={[0, 0, -0.01]}>
          <ringGeometry args={[1.25, 1.5, 32]} />
        </mesh>
        <Text font="/fonts/lilita.woff" fontSize={1.1} color="#ff7a3d" anchorX="center" anchorY="middle" position={[0, 0.08, 0]}>
          +
        </Text>
        <Text font="/fonts/fredoka600.woff" fontSize={0.55} color="#ffffff" outlineWidth={0.05} outlineColor="#1a2233" anchorX="center" anchorY="top" position={[0, -1.7, 0]}>
          ¿TU CASA?
        </Text>
      </Billboard>
      <mesh position={[0, -3.2, 0]} material={mat('#ffffff', { transparent: true, opacity: 0.5 })}>
        <cylinderGeometry args={[0.05, 0.05, 3.2, 6]} />
      </mesh>
    </group>
  )
}
