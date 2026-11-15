// PIZZ 2050 — EPISODIO 0 «El baúl del tiempo». Pizz se mete en un baúl, se entierra
// y saldrá en 2050: lo que comente la gente será lo que se encuentre.
// Todo es función pura del tiempo `t` (render determinista).
import { useMemo, useRef } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { Text } from '@react-three/drei'
import * as THREE from 'three'
import { clock, ease, seg } from '../engine/clock'
import { evalCam, world, type CamKey } from '../engine/director'
import { useLines, mouthAt, speakingAt } from '../engine/voice'
import { Character, PIZZ_LOOK, newState, type Action } from '../scene/Character'
import { PizzHome } from '../scene/PizzHome'
import { heightAt } from '../world/terrain'
import { mat } from '../scene/materials'

export const FUT000 = {
  id: 'futuro000',
  duration: 47.6,
  script: [
    { id: 'l01', at: 0.25, text: '¡Cada comentario que dejes aquí... será algo que me encuentre en el año dos mil cincuenta!' },
    { id: 'l02', at: 4.75, text: 'Soy Pizz. Y voy a hacer la mayor locura de internet.' },
    { id: 'l03', at: 8.0, text: 'Me meto en este baúl, me entierro... ¡y no salgo hasta dos mil cincuenta!' },
    { id: 'l04', at: 12.0, text: 'Veinticuatro años bajo tierra. Cuando se abra la tapa... el mundo será otro.' },
    { id: 'l05', at: 16.35, text: '¿Y qué habrá ahí fuera? ¡Eso lo decidís vosotros!' },
    { id: 'l06', at: 19.45, text: 'Comenta qué me voy a encontrar: coches voladores, robots, ¿pizza gratis?... ¡Lo que quieras!' },
    { id: 'l07', at: 25.0, text: 'Tú lo comentas... ¡y yo me lo encuentro!' },
    { id: 'l08', at: 27.45, text: 'Y etiqueta a alguien que tenga que venirse al futuro conmigo.' },
    { id: 'l09', at: 30.55, text: '¿Listos? ¡Nos vemos en dos mil cincuenta!' },
    { id: 'l10', at: 42.0, text: '¿Hola?... ¿Ya es dos mil cincuenta?' },
  ],
}
const A = Object.fromEntries(FUT000.script.map((l) => [l.id, l.at])) as Record<string, number>

// ---------------------------------------------------------------- layout & timeline
const TR = { x: 2.6, z: 11.3 }
const GY = heightAt(TR.x, TR.z)
const P0 = { x: 1.15, z: 11.5 }
const TW = 1.55, TD = 0.95, TH = 0.8 // trunk size
const FLOOR = GY + 0.12
const JUMP = [9.05, 9.75]
const B = { duck: 32.7, lid: 32.85, sink: 33.6, sign: 34.9, lapse: 35.3, lapseEnd: 41.1, shake: 41.2, burst: 44.35, end: 47.6 }
export const FUT_TIMES = { ...B }


const c = (x: number, y: number, z: number): [number, number, number] => [TR.x + x, GY + y, TR.z + z]
function cameraKeys(): CamKey[] {
  return [
    // S1 hook: lid bursts open, fast push-in
    { t: 0, p: c(-0.4, 2.9, 11), l: c(-0.6, 1.1, 0), fov: 42 },
    { t: 1.1, p: c(-0.5, 1.9, 6.0), l: c(-0.6, 1.2, 0), fov: 40, e: 'out' },
    { t: 4.6, p: c(-0.6, 1.8, 5.2), l: c(-0.6, 1.25, 0), fov: 38, e: 'linear' },
    // S2 low hero dolly
    { t: 4.7, p: c(-2.2, 0.6, 5.0), l: c(-0.9, 1.4, 0), fov: 42, cut: true },
    { t: 7.9, p: c(1.0, 0.6, 5.2), l: c(-0.9, 1.4, 0), fov: 42, e: 'linear' },
    // S3 wide: he jumps in
    { t: 7.95, p: c(-0.6, 2.6, 8.5), l: c(-0.3, 0.9, 0), fov: 42, cut: true },
    { t: 11.9, p: c(-0.2, 2.3, 6.8), l: c(-0.1, 1.0, 0), fov: 42, e: 'linear' },
    // S4 high angle into the trunk
    { t: 11.95, p: c(0, 4.2, 3.2), l: c(0, 1.0, 0), fov: 44, cut: true },
    { t: 16.25, p: c(0.5, 3.8, 3.0), l: c(0, 1.05, 0), fov: 44, e: 'linear' },
    // S5 close-up
    { t: 16.3, p: c(0.05, 1.95, 2.9), l: c(0, 1.6, 0), fov: 38, cut: true },
    { t: 19.35, p: c(0, 1.92, 2.6), l: c(0, 1.62, 0), fov: 38, e: 'linear' },
    // S6 slow orbit while he lists ideas
    { t: 19.4, p: c(-1.8, 2.2, 4.4), l: c(0, 1.4, 0), fov: 42, cut: true },
    { t: 24.9, p: c(1.9, 2.2, 4.3), l: c(0, 1.4, 0), fov: 42, e: 'linear' },
    // S7 punch-in on the slogan
    { t: 24.95, p: c(0, 1.9, 2.4), l: c(0, 1.62, 0), fov: 36, cut: true },
    { t: 27.35, p: c(0, 1.85, 2.1), l: c(0, 1.62, 0), fov: 33, e: 'linear' },
    // S8 tag a friend
    { t: 27.4, p: c(1.3, 2.3, 4.0), l: c(0, 1.4, 0), fov: 40, cut: true },
    { t: 30.45, p: c(1.0, 2.2, 3.6), l: c(0, 1.42, 0), fov: 40, e: 'linear' },
    // S9 goodbye, then burial seen from a little further
    { t: 30.5, p: c(0, 2.4, 4.6), l: c(0, 1.3, 0), fov: 42, cut: true },
    { t: 32.6, p: c(0, 2.3, 4.2), l: c(0, 1.3, 0), fov: 42, e: 'linear' },
    { t: 32.65, p: c(-2.9, 3.4, 6.6), l: c(0, 0.3, 0), fov: 44, cut: true },
    { t: B.lapse, p: c(-2.4, 3.0, 5.9), l: c(-0.8, 0.3, 0), fov: 44, e: 'linear' },
    // timelapse: crane up over the spot
    { t: B.lapseEnd, p: c(12, 15, 20), l: c(0, 0.4, 0), fov: 46, e: 'inOut' },
    // the ground shakes: low and close
    { t: B.shake, p: c(-1.6, 0.9, 3.8), l: c(0, 0.35, 0), fov: 46, cut: true },
    { t: B.burst, p: c(-1.2, 0.85, 3.3), l: c(0, 0.5, 0), fov: 46, e: 'linear' },
    // light explodes: pull back
    { t: B.burst + 0.05, p: c(-1.2, 0.85, 3.3), l: c(0, 0.6, 0), fov: 46, cut: true },
    { t: B.end, p: c(-4.2, 3.6, 9.5), l: c(0, 1.8, 0), fov: 48, e: 'out' },
  ]
}

// ---------------------------------------------------------------- component
export function Fut000() {
  const { camera } = useThree()
  const lines = useMemo(() => useLines(FUT000.id, FUT000.script), [])
  const keys = useMemo(cameraKeys, [])
  const pizz = useMemo(newState, [])
  const P = useMemo(() => new THREE.Vector3(), [])
  const L = useMemo(() => new THREE.Vector3(), [])
  const camPos = useMemo(() => new THREE.Vector3(), [])
  const trunk = useRef<THREE.Group>(null!)
  const lid = useRef<THREE.Group>(null!)
  const beam = useRef<THREE.Mesh>(null!)
  const mound = useRef<THREE.Mesh>(null!)
  const cap = useRef<THREE.Mesh>(null!)
  const sign = useRef<THREE.Group>(null!)
  const sprouts = useRef<THREE.Group>(null!)
  const cracks = useRef<THREE.Group>(null!)
  const beams = useRef<THREE.Group>(null!)
  const dust = useRef<THREE.Group>(null!)
  const flash = useRef<THREE.Mesh>(null!)
  const T = () => clock.t

  const grad = useMemo(() => { const cv = document.createElement('canvas'); cv.width = 4; cv.height = 64; const g = cv.getContext('2d')!; const lg = g.createLinearGradient(0, 0, 0, 64); lg.addColorStop(0, 'rgba(255,255,255,0)'); lg.addColorStop(1, 'rgba(255,255,255,1)'); g.fillStyle = lg; g.fillRect(0, 0, 4, 64); return new THREE.CanvasTexture(cv) }, [])
  const glow = useMemo(() => new THREE.MeshBasicMaterial({ color: '#6ff3ff', alphaMap: grad, transparent: true, opacity: 0.35, blending: THREE.AdditiveBlending, depthWrite: false, toneMapped: false, side: THREE.DoubleSide }), [])
  const glow2 = useMemo(() => new THREE.MeshBasicMaterial({ color: '#7ff8ff', alphaMap: grad, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false, toneMapped: false, side: THREE.DoubleSide }), [])
  const crackM = useMemo(() => new THREE.MeshBasicMaterial({ color: '#9ffcff', transparent: true, opacity: 0, toneMapped: false }), [])
  const dustM = useMemo(() => new THREE.MeshStandardMaterial({ color: '#c9a27a', transparent: true, opacity: 0, roughness: 1, depthWrite: false }), [])
  const flashM = useMemo(() => new THREE.MeshBasicMaterial({ color: '#ffffff', transparent: true, opacity: 0, toneMapped: false, depthTest: false }), [])

  const sproutData = useMemo(() => Array.from({ length: 26 }, (_, i) => {
    const a = i * 2.39996, r = 0.9 + ((i * 37) % 11) / 11 * 1.3
    return { x: Math.cos(a) * r, z: Math.sin(a) * r * 0.8, s: 0.6 + ((i * 53) % 7) / 7 * 0.7, d: (i % 9) / 9, flower: i % 4 === 0 ? ['#ffd23d', '#ff6fa8', '#ffffff', '#b98cff'][i % 4 === 0 ? (i / 4) % 4 : 0] : null }
  }), [])
  const crackData = useMemo(() => Array.from({ length: 9 }, (_, i) => ({ a: (i / 9) * Math.PI * 2 + 0.3 * Math.sin(i * 7), len: 0.9 + (i % 3) * 0.45 })), [])

  useMemo(() => {
    const pv = (window as any).__pv
    if (!pv) return
    pv.info = () => {
      const sfx: { type: string; at: number; g?: number }[] = [
        { type: 'hit', at: 0.12, g: 0.9 }, { type: 'whoosh', at: 0.0, g: 0.6 },
        { type: 'whoosh', at: JUMP[0] - 0.1, g: 0.5 }, { type: 'thud', at: JUMP[1], g: 0.7 },
        { type: 'thud', at: B.lid + 0.38, g: 1.0 }, { type: 'hit', at: B.lid + 0.38, g: 0.6 },
        { type: 'rumble', at: B.sink - 0.2, g: 0.7 }, { type: 'pop', at: B.sign + 0.1, g: 0.4 },
        { type: 'riser', at: B.lapseEnd - 1.9, g: 0.5 },
        { type: 'rumble', at: B.shake, g: 0.9 }, { type: 'rumble', at: B.shake + 1.6, g: 0.9 },
        { type: 'riser', at: B.burst - 2.0, g: 0.7 }, { type: 'hit', at: B.burst, g: 1.0 }, { type: 'chime', at: B.burst + 0.1, g: 0.5 },
      ]
      for (const k of keys) if (k.cut && k.t > 1) sfx.push({ type: 'whoosh', at: k.t - 0.05, g: 0.3 })
      for (let i = 0; i <= 24; i++) sfx.push({ type: 'tick', at: B.lapse + 0.2 + i * ((B.lapseEnd - B.lapse - 0.6) / 24), g: 0.5 })
      return {
        id: FUT000.id, duration: FUT000.duration, music: 'epic', mute: [[B.shake, B.burst]],
        lines: lines.map((l) => ({ id: l.id, at: l.at, dur: l.dur, text: l.text, words: l.words, hasAudio: l.hasAudio })), sfx,
      }
    }
  }, [])

  useFrame(() => {
    const t = T()
    const fov = evalCam(keys, t, P, L)
    // ground shake
    const sh = t > B.shake && t < B.burst + 0.6 ? (0.025 + 0.06 * seg(t, B.shake, B.burst)) * (1 - seg(t, B.burst, B.burst + 0.6)) : t > B.lid + 0.35 && t < B.lid + 0.7 ? 0.04 : 0
    if (sh) { P.x += Math.sin(t * 71) * sh; P.y += Math.sin(t * 97 + 1) * sh; L.x += Math.sin(t * 53) * sh * 0.6 }
    camera.position.copy(P); camera.lookAt(L)
    const pc = camera as THREE.PerspectiveCamera
    if (Math.abs(pc.fov - fov) > 0.01) { pc.fov = fov; pc.updateProjectionMatrix() }
    camPos.copy(P)
    world.focus.set(L.x, 0, L.z)
    world.shadowSpan = THREE.MathUtils.clamp(P.distanceTo(L) * 0.9, 14, 60)

    // time of day: golden afternoon → timelapse → night
    if (t < B.lapse) world.hour = 17.2
    else if (t < B.lapseEnd) world.hour = 17.2 + Math.pow(seg(t, B.lapse, B.lapseEnd), 1.15) * (24 * 5 + 3.6)
    else world.hour = 20.8

    // ---- Pizz
    pizz.lookAt = camPos; pizz.smile = 0.8; pizz.speed = 0; pizz.visible = t < B.lid + 0.3
    pizz.action = 'none'; pizz.actionW = 0
    if (t < JUMP[0]) { pizz.x = P0.x; pizz.z = P0.z; pizz.y = heightAt(P0.x, P0.z); pizz.ry = 0.25 }
    else if (t < JUMP[1]) {
      const u = seg(t, JUMP[0], JUMP[1])
      pizz.x = THREE.MathUtils.lerp(P0.x, TR.x, u); pizz.z = THREE.MathUtils.lerp(P0.z, TR.z, u)
      pizz.y = THREE.MathUtils.lerp(heightAt(P0.x, P0.z), FLOOR, u) + Math.sin(u * Math.PI) * 1.0
      pizz.ry = 0.25 - u * 0.25
      pizz.action = 'celebrate'; pizz.actionT = 0.21; pizz.actionW = 1
    } else {
      pizz.x = TR.x; pizz.z = TR.z; pizz.ry = 0
      pizz.y = FLOOR - Math.pow(seg(t, B.duck, B.duck + 0.3), 2) * 1.5
    }
    const act = (a: Action, t0: number, t1: number, tt = t) => { if (t >= t0 && t < t1) { pizz.action = a; pizz.actionT = tt; pizz.actionW = seg(t, t0, t0 + 0.15) * (1 - seg(t, t1 - 0.15, t1)); return true } return false }
    if (!(t >= JUMP[0] && t < JUMP[1])) {
      act('surprise', 0, 0.9, t) ||
      act('celebrate', A.l02 + 1.5, A.l02 + 2.9, t - A.l02 - 1.5) ||
      act('shrug', A.l05, A.l05 + 1.4) ||
      act('point', A.l05 + 1.5, A.l05 + 2.7) ||
      act('celebrate', A.l07 + 0.9, A.l07 + 2.2, t - A.l07 - 0.9) ||
      act('point', A.l08 + 0.2, A.l08 + 2.6) ||
      act('wave', A.l09 + 0.6, B.duck) ||
      (speakingAt(lines, t) && act('talk', 0, 99))
    }
    pizz.mouth = mouthAt(lines, t)

    // ---- trunk: lid bursts open at the start, slams shut at the end
    const open = t < B.lid ? ease.outBack(seg(t, 0.1, 0.42)) : 1 - ease.in(seg(t, B.lid, B.lid + 0.38))
    lid.current.rotation.x = -open * 1.95
    const sink = ease.inOut(seg(t, B.sink, B.sink + 1.3))
    trunk.current.position.y = GY - sink * (TH + 0.6)
    trunk.current.visible = sink < 0.999
    const bo = t < B.lid ? 0.4 * (1 - seg(t, 2.2, 3.4)) * (0.85 + 0.15 * Math.sin(t * 9)) * seg(t, 0.1, 0.3) : 0
    glow.opacity = bo; beam.current.visible = bo > 0.01
    // dirt: mound shrinks into the hole, cap appears
    const fill = seg(t, B.sink + 0.2, B.sink + 1.5)
    mound.current.scale.set(1, Math.max(0.02, 1 - fill * 0.9), 1)
    cap.current.visible = fill > 0.02
    cap.current.scale.setScalar(Math.max(0.01, fill))
    dustM.opacity = 0.3 * Math.sin(seg(t, B.sink, B.sink + 1.9) * Math.PI)
    dust.current.children.forEach((c, i) => { const u = seg(t, B.sink + i * 0.08, B.sink + 1.9); c.scale.setScalar(0.2 + u * (0.6 + (i % 3) * 0.2)); c.position.y = 0.2 + u * 0.8 })
    dust.current.visible = dustM.opacity > 0.01
    // sign + sprouts during the years
    sign.current.scale.setScalar(Math.max(0.001, ease.outBack(seg(t, B.sign, B.sign + 0.4))))
    sprouts.current.children.forEach((c, i) => { const d = sproutData[i]; c.scale.setScalar(Math.max(0.001, ease.out(seg(t, B.lapse + 0.5 + d.d * 3, B.lapse + 2.5 + d.d * 3)) * d.s)) })
    // cracks + beams: something is coming out
    const cr = seg(t, B.shake + 0.4, B.burst)
    crackM.opacity = cr * (0.75 + 0.25 * Math.sin(t * 30))
    cracks.current.visible = cr > 0.01
    cracks.current.children.forEach((c, i) => { c.scale.set(1, 1, Math.max(0.01, seg(t, B.shake + 0.4 + i * 0.22, B.shake + 1.4 + i * 0.22))) })
    const bb = seg(t, B.burst - 0.8, B.burst) * (1 - 0.6 * seg(t, B.burst + 0.3, B.end))
    glow2.opacity = bb * 0.3
    beams.current.visible = bb > 0.01
    beams.current.scale.set(0.6 + bb * 0.6, 0.2 + bb * 1.0, 0.6 + bb * 0.6)
    beams.current.rotation.y = t * 0.6
    flashM.opacity = Math.max(0, 1 - (t - B.burst) / 0.6) * (t >= B.burst ? 0.95 : 0)
    flash.current.visible = flashM.opacity > 0.01
    flash.current.position.copy(P).addScaledVector(L.clone().sub(P).normalize(), 0.5)
    flash.current.lookAt(P)
  }, -1)

  return (
    <group>
      <PizzHome />
      <Character look={PIZZ_LOOK} state={pizz} />
      {/* trunk */}
      <group ref={trunk} position={[TR.x, GY, TR.z]}>
        <Trunk />
        <group ref={lid} position={[0, TH, -TD / 2]}>
          <TrunkLid />
        </group>
        <mesh ref={beam} position={[0, TH + 2.2, 0]} material={glow}>
          <cylinderGeometry args={[TW * 0.42, TW * 0.36, 4.4, 24, 1, true]} />
        </mesh>
        <mesh position={[0, TH - 0.02, 0]} rotation-x={-Math.PI / 2} material={mat('#58f0ff', { emissive: '#3fe6ff', ei: 1.4, rough: 0.3 })}>
          <planeGeometry args={[TW - 0.14, TD - 0.14]} />
        </mesh>
      </group>
      {/* the hole, the dirt mound and the patch that covers it */}
      <group position={[TR.x, GY, TR.z]}>
        <mesh position={[0, 0.025, 0]} rotation-x={-Math.PI / 2} material={mat('#4a3322', { rough: 1 })} receiveShadow>
          <circleGeometry args={[1.35, 40]} />
        </mesh>
        <mesh ref={mound} position={[2.1, 0, -0.5]} material={mat('#6b4a2f', { rough: 1 })} castShadow receiveShadow>
          <sphereGeometry args={[0.95, 20, 12, 0, Math.PI * 2, 0, Math.PI / 2]} />
        </mesh>
        <mesh ref={cap} position={[0, 0.06, 0]} material={mat('#5d4029', { rough: 1 })} receiveShadow>
          <cylinderGeometry args={[1.4, 1.5, 0.12, 40]} />
        </mesh>
        <group ref={dust}>
          {Array.from({ length: 7 }, (_, i) => (
            <mesh key={i} position={[Math.cos(i * 0.9) * 1.1, 0.3, Math.sin(i * 0.9) * 0.8]} material={dustM}><sphereGeometry args={[0.6, 10, 8]} /></mesh>
          ))}
        </group>
        <group ref={sign} position={[-1.55, 0, 0.5]} rotation-y={-0.55}>
          <mesh position={[0, 0.6, 0]} material={mat('#6e4a2f')} castShadow><boxGeometry args={[0.1, 1.2, 0.1]} /></mesh>
          <mesh position={[0, 1.15, 0.06]} material={mat('#b98552', { rough: 0.9 })} castShadow><boxGeometry args={[1.25, 0.62, 0.06]} /></mesh>
          <Text font="/fonts/lilita.woff" fontSize={0.13} color="#2a1a10" anchorX="center" anchorY="middle" position={[0, 1.28, 0.1]}>NO ABRIR HASTA</Text>
          <Text font="/fonts/lilita.woff" fontSize={0.3} color="#c0261d" anchorX="center" anchorY="middle" position={[0, 1.07, 0.1]}>2050</Text>
        </group>
        <group ref={sprouts}>
          {sproutData.map((d, i) => (
            <group key={i} position={[d.x, 0, d.z]}>
              <mesh position={[0, 0.14, 0]} material={mat('#4f9a3a', { rough: 0.9 })}><coneGeometry args={[0.06, 0.3, 5]} /></mesh>
              <mesh position={[0.07, 0.1, 0.02]} rotation-z={-0.5} material={mat('#5fae45', { rough: 0.9 })}><coneGeometry args={[0.05, 0.22, 5]} /></mesh>
              {d.flower && <mesh position={[0, 0.3, 0]} material={mat(d.flower, { rough: 0.6 })}><sphereGeometry args={[0.06, 8, 6]} /></mesh>}
            </group>
          ))}
        </group>
        <group ref={cracks} position={[0, 0.14, 0]}>
          {crackData.map((c, i) => (
            <group key={i} rotation-y={c.a}>
              <mesh position={[0, 0, c.len / 2]} material={crackM}><boxGeometry args={[0.07, 0.03, c.len]} /></mesh>
            </group>
          ))}
        </group>
        <group ref={beams}>
          {[0, 1, 2, 3, 4].map((i) => (
            <mesh key={i} position={[0, 3, 0]} rotation-y={i * 1.26} rotation-z={(i - 2) * 0.12} material={glow2}>
              <cylinderGeometry args={[0.35 + i * 0.12, 0.08, 6, 12, 1, true]} />
            </mesh>
          ))}
        </group>
      </group>
      <mesh ref={flash} material={flashM} renderOrder={999}><planeGeometry args={[4, 4]} /></mesh>
    </group>
  )
}

function Trunk() {
  const wood = mat('#8a5530', { rough: 0.8 }), dark = mat('#5a361d', { rough: 0.85 }), metal = mat('#d9a93a', { rough: 0.35, metal: 0.8 })
  const w = TW, d = TD, h = TH, th = 0.07
  return (
    <group>
      <mesh position={[0, th / 2, 0]} material={dark} castShadow receiveShadow><boxGeometry args={[w, th, d]} /></mesh>
      <mesh position={[0, h / 2, d / 2 - th / 2]} material={wood} castShadow receiveShadow><boxGeometry args={[w, h, th]} /></mesh>
      <mesh position={[0, h / 2, -d / 2 + th / 2]} material={wood} castShadow receiveShadow><boxGeometry args={[w, h, th]} /></mesh>
      <mesh position={[w / 2 - th / 2, h / 2, 0]} material={wood} castShadow receiveShadow><boxGeometry args={[th, h, d]} /></mesh>
      <mesh position={[-w / 2 + th / 2, h / 2, 0]} material={wood} castShadow receiveShadow><boxGeometry args={[th, h, d]} /></mesh>
      {[-0.55, 0.55].map((x) => (
        <mesh key={x} position={[x * w * 0.8, h / 2, 0]} material={metal} castShadow><boxGeometry args={[0.1, h + 0.02, d + 0.03]} /></mesh>
      ))}
      <mesh position={[0, h * 0.82, d / 2 + 0.01]} material={metal}><boxGeometry args={[w + 0.03, 0.07, 0.02]} /></mesh>
      <mesh position={[0, 0.06, d / 2 + 0.01]} material={metal}><boxGeometry args={[w + 0.03, 0.07, 0.02]} /></mesh>
      {/* glowing year plate */}
      <mesh position={[0, h * 0.45, d / 2 + 0.02]} material={mat('#10202c', { rough: 0.4 })}><boxGeometry args={[0.62, 0.26, 0.02]} /></mesh>
      <Text font="/fonts/lilita.woff" fontSize={0.19} color="#6ff3ff" anchorX="center" anchorY="middle" position={[0, h * 0.45, d / 2 + 0.035]}>2050</Text>
    </group>
  )
}

function TrunkLid() {
  const wood = mat('#94603a', { rough: 0.8 }), metal = mat('#d9a93a', { rough: 0.35, metal: 0.8 })
  // pivot at the back edge; the lid extends towards +z
  return (
    <group>
      <mesh position={[0, 0.06, TD / 2]} material={wood} castShadow receiveShadow><boxGeometry args={[TW + 0.04, 0.12, TD + 0.04]} /></mesh>
      <mesh position={[0, 0.13, TD / 2]} rotation-z={Math.PI / 2} material={wood} castShadow>
        <cylinderGeometry args={[TD / 2 + 0.02, TD / 2 + 0.02, TW + 0.04, 24, 1, false, 0, Math.PI]} />
      </mesh>
      {[-0.55, 0.55].map((x) => (
        <mesh key={x} position={[x * TW * 0.8, 0.14, TD / 2]} rotation-z={Math.PI / 2} material={metal} castShadow>
          <cylinderGeometry args={[TD / 2 + 0.04, TD / 2 + 0.04, 0.1, 24, 1, false, 0, Math.PI]} />
        </mesh>
      ))}
      <mesh position={[0, 0.0, TD + 0.03]} material={metal}><boxGeometry args={[0.18, 0.2, 0.04]} /></mesh>
    </group>
  )
}
