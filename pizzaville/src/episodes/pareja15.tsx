// COSAS DE PAREJA · «No quiero nada» — formato narrador (Martín por dentro, Inés solo sus frases).
// Todo en el sofá: pide una hamburguesa, ella «no quiere nada» y se come media. Ritmo lento: frases cortas, pocas ideas estiradas.
// Un solo audio continuo con pausas añadidas, sin música ni efectos.
import { useMemo, useRef, type ReactNode } from 'react'
import { useFrame } from '@react-three/fiber'
import { RoundedBox } from '@react-three/drei'
import * as THREE from 'three'
import { CONV } from './pareja15_data'
import { LivingRoom, PairEpisode, Show, pose, track, type Overlay, type PairSpec } from './pareja_kit'
import { clock } from '../engine/clock'

const fm = (c: string, r = 0.8) => new THREE.MeshStandardMaterial({ color: c, roughness: r, flatShading: true })
const at = Object.fromEntries(CONV.map((c) => [c.id, c.at])) as Record<string, number>
/** start time of the n-th line (1-based) that starts with this text */
const A = (s: string, n = 1) => CONV.filter((c) => c.text.toLowerCase().startsWith(s.toLowerCase()))[n - 1].at
const END = CONV[CONV.length - 1].at
const LX = -0.42, DX = 0.42, Z = -0.35, HY = 1.52

// ---------------- moments
const T = {
  order: A('Pido una'), deliver: A('Llega el'), open: A('Abro la bolsa'), fry1: A('Primera patata'), look: A('Ella levanta'),
  give: A('Le doy'), takes2: A('Coge dos'), chew: A('Masticamos'), takes1: A('Coge otra'), burger: A('Abro la hamburguesa'),
  eyes: A('Ella la mira'), bite: A('Se come la mitad'), full: A('Uf'), left: A('Me quedan'), pickle: A('Me lo como'), app: A('Abro la aplicación'),
  fries: A('Pues pídeme'), sure2: A('Le pregunto si', 2),
}

// ---------------- phone screens
const rr = (c: CanvasRenderingContext2D, x: number, y: number, w: number, h: number, r: number) => { c.beginPath(); c.roundRect(x, y, w, h, r); c.fill() }
function useScreen(draw: (c: CanvasRenderingContext2D, w: number, h: number) => void) {
  return useMemo(() => {
    const cv = document.createElement('canvas'); cv.width = 540; cv.height = 1100
    draw(cv.getContext('2d')!, cv.width, cv.height)
    const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace
    return tex
  }, [])
}
const Screen = ({ tex }: { tex: THREE.Texture }) => <mesh position={[0, 0, 0.0065]}><planeGeometry args={[0.072, 0.146]} /><meshBasicMaterial map={tex} toneMapped={false} /></mesh>
function OrderScreen({ again }: { again?: boolean }) {
  const tex = useScreen((c, w) => {
    c.fillStyle = '#fff7ee'; c.fillRect(0, 0, w, 1100)
    c.fillStyle = '#ff6a3d'; c.fillRect(0, 0, w, 150)
    c.fillStyle = '#ffffff'; c.font = '700 40px sans-serif'; c.fillText(again ? 'Tu pedido' : 'Pedido confirmado', 40, 95)
    // burger drawing
    c.fillStyle = '#e1a14a'; c.beginPath(); c.ellipse(w / 2, 300, 140, 70, 0, Math.PI, 0); c.fill()
    c.fillStyle = '#5b3420'; c.fillRect(w / 2 - 140, 300, 280, 36)
    c.fillStyle = '#f5c43a'; c.fillRect(w / 2 - 150, 336, 300, 16)
    c.fillStyle = '#e1a14a'; rr(c, w / 2 - 140, 352, 280, 46, 20)
    c.fillStyle = '#1d1d1f'; c.font = '600 36px sans-serif'; c.textAlign = 'center'
    c.fillText(again ? '1 × Doble queso + bacon' : '1 × Doble queso + bacon', w / 2, 480)
    if (again) { c.fillText('1 × Patatas grandes', w / 2, 535) }
    c.fillStyle = '#ff6a3d'; c.font = '700 64px sans-serif'; c.fillText('35 min', w / 2, again ? 660 : 610)
    c.fillStyle = '#6b6b6b'; c.font = '30px sans-serif'; c.fillText('Llega entre 21:40 y 21:50', w / 2, again ? 715 : 665)
    c.fillStyle = '#ff6a3d'; rr(c, 60, 860, w - 120, 110, 55); c.fillStyle = '#ffffff'; c.font = '700 40px sans-serif'; c.fillText(again ? 'Pedir otra vez' : 'Seguir pedido', w / 2, 930)
  })
  return <Screen tex={tex} />
}
function PhoneProp({ screen }: { screen?: ReactNode }) {
  return (
    <group>
      <RoundedBox args={[0.08, 0.16, 0.012]} radius={0.008} smoothness={2}><meshStandardMaterial color="#1a1a22" roughness={0.35} /></RoundedBox>
      {screen ?? <mesh position={[0, 0, 0.0065]}><planeGeometry args={[0.072, 0.146]} /><meshBasicMaterial color="#9fd0ff" toneMapped={false} /></mesh>}
    </group>
  )
}
const INS: Record<string, [number, number, number]> = { order: [20, 1, 0], again: [24, 1, 0] }
function PhoneInsert({ p, screen }: { p: [number, number, number]; screen: ReactNode }) {
  const g = useRef<THREE.Group>(null!)
  useFrame(() => { g.current.rotation.z = Math.sin(clock.t * 1.3) * 0.02 })
  return (
    <group position={p}>
      <pointLight position={[0.1, 0.3, 0.5]} intensity={1.2} distance={2} color="#cfd9ff" />
      <mesh position={[0, -0.02, -0.06]}><planeGeometry args={[0.6, 0.6]} /><meshStandardMaterial color="#e0a63c" roughness={0.95} /></mesh>
      <group ref={g}><PhoneProp screen={screen} /></group>
    </group>
  )
}

// ---------------- the food on the blanket, between them
const RED = fm('#c8372d', 0.6), FRY = fm('#f2c14e', 0.6), FRYT = fm('#d99a2b', 0.6), PAPER = fm('#efe3c8', 0.9), BAG = fm('#b88a55', 0.95)
const BUN = fm('#d9953f', 0.6), PATTY = fm('#5b3420', 0.8), CHEESE = fm('#f5c43a', 0.5), BACON = fm('#a8432f', 0.7), PICKLE = fm('#6f8f3a', 0.6)
// fries: index 0 = the longest, 1 = the most toasted (the two he had set apart), then the rest
const FRIES = Array.from({ length: 12 }, (_, i) => ({ x: -0.045 + (i % 6) * 0.018, z: i < 6 ? 0.012 : -0.012, h: i === 0 ? 0.16 : 0.09 + ((i * 37) % 5) * 0.008, tilt: ((i * 53) % 7 - 3) * 0.05 }))
/** when each fry disappears */
const gone = (i: number) => {
  if (i === 0 || i === 1) return T.takes2 + 0.2 // she takes the best two
  if (i === 2) return T.give + 0.2 // the one he gives her
  if (i === 3) return T.fry1 + 0.3 // his first
  if (i === 4) return T.takes1 + 0.2
  if (i < 10) return T.burger - 0.5 + (i - 5) * 0.2 // eaten between scenes
  return 1e9 // two left
}
function Food() {
  const fries = useRef<THREE.Group>(null!)
  const half = useRef<THREE.Group>(null!)
  const pick = useRef<THREE.Mesh>(null!)
  const bagG = useRef<THREE.Group>(null!)
  const foodG = useRef<THREE.Group>(null!)
  useFrame(() => {
    const t = clock.t
    bagG.current.visible = t > T.deliver - 0.2
    foodG.current.visible = t > T.open + 0.3
    fries.current.children.forEach((m, i) => { m.visible = t < gone(i) })
    half.current.visible = t < T.bite + 0.4 // she eats the half with the bacon
    pick.current.visible = t < T.pickle + 0.3
  })
  return (
    <group position={[0.12, 0.78, Z + 0.45]}>
      {/* the paper bag, open, on the right */}
      <group ref={bagG} position={[0.26, 0.12, -0.05]} rotation-y={-0.3}>
        <mesh material={BAG}><boxGeometry args={[0.18, 0.24, 0.12]} /></mesh>
        <mesh position={[0, 0.121, 0]} rotation-x={-Math.PI / 2} material={fm('#5b4027')}><planeGeometry args={[0.16, 0.1]} /></mesh>
        <mesh position={[0, 0.02, 0.061]} material={fm('#ff6a3d', 0.7)}><circleGeometry args={[0.04, 10]} /></mesh>
      </group>
      <group ref={foodG}>
        {/* fries box */}
        <group position={[-0.12, 0.02, 0]}>
          <mesh position={[0, 0.05, 0]} material={RED}><boxGeometry args={[0.13, 0.1, 0.06]} /></mesh>
          <mesh position={[0, 0.06, 0.031]} material={fm('#f5c43a', 0.5)}><circleGeometry args={[0.025, 8]} /></mesh>
          <group ref={fries}>
            {FRIES.map((f, i) => <mesh key={i} position={[f.x, 0.1 + f.h / 2 - 0.04, f.z]} rotation-z={f.tilt} material={i === 1 ? FRYT : FRY}><boxGeometry args={[0.013, f.h, 0.013]} /></mesh>)}
          </group>
        </group>
        {/* burger on its open box: one half has the bacon */}
        <group position={[0.1, 0.0, 0.02]}>
          <mesh position={[0, 0.005, 0]} material={PAPER}><boxGeometry args={[0.24, 0.01, 0.2]} /></mesh>
          {[[-1, true], [1, false]].map(([s, isHalf]) => {
            const body = (
              <group position={[(s as number) * 0.042, 0, 0]}>
                <mesh position={[0, 0.025, 0]} material={BUN}><boxGeometry args={[0.075, 0.03, 0.12]} /></mesh>
                <mesh position={[0, 0.05, 0]} material={PATTY}><boxGeometry args={[0.078, 0.022, 0.12]} /></mesh>
                <mesh position={[0, 0.064, 0]} material={CHEESE}><boxGeometry args={[0.082, 0.008, 0.125]} /></mesh>
                {isHalf && <mesh position={[0, 0.072, 0]} material={BACON}><boxGeometry args={[0.07, 0.008, 0.1]} /></mesh>}
                <mesh position={[0, 0.095, 0]} material={BUN}><sphereGeometry args={[0.062, 8, 4, 0, Math.PI * 2, 0, Math.PI / 2]} /></mesh>
              </group>
            )
            return isHalf ? <group key="h" ref={half}>{body}</group> : <group key="o">{body}</group>
          })}
          <mesh ref={pick} position={[0.1, 0.015, 0.07]} rotation-x={-Math.PI / 2} material={PICKLE}><circleGeometry args={[0.018, 8]} /></mesh>
        </group>
      </group>
    </group>
  )
}
/** a fry or a piece of burger in a hand (visible while a test is true) */
const FryInHand = ({ show }: { show: () => boolean }) => <Show show={show}><mesh position={[0, -0.04, 0.05]} rotation-x={0.3} material={FRY}><boxGeometry args={[0.013, 0.11, 0.013]} /></mesh></Show>

// ---------------- acting (seated on the sofa: her left, him right)
const arms = { rSh: [0.35, -0.12] as [number, number], rEl: -1.2, lSh: [0.35, 0.12] as [number, number], lEl: -1.2 }
const phone = { rSh: [0.75, -0.05] as [number, number], rEl: -1.6 }
const eat = { rSh: [0.85, 0.05] as [number, number], rEl: -2.1 }
const reach = { rSh: [0.75, 0.45] as [number, number], rEl: -0.7 }
const D = {
  phone: pose({ yaw: 0.05, pitch: 0.35, lids: 0.25, brows: 0.15, ...arms, ...phone }),
  her: pose({ yaw: -0.45, lids: 0.25, brows: 0.15, ...arms }),
  cam: pose({ yaw: 0.05, lids: 0.45, brows: 0.05, smile: -0.1, ...arms }),
  down: pose({ yaw: -0.15, pitch: 0.4, lids: 0.2, brows: 0.25, smile: 0.25, ...arms, rSh: [0.6, 0.2], rEl: -0.9 }),
  happy: pose({ yaw: -0.05, pitch: 0.1, lids: 0.45, brows: 0.2, smile: 0.5, ...arms, ...eat }),
  wary: pose({ yaw: -0.4, lids: 0.3, brows: 0.35, browTilt: -0.4, smile: -0.1, ...arms, rSh: [0.5, 0.15], rEl: -1.2 }),
  give: pose({ yaw: -0.45, lids: 0.3, brows: 0.25, smile: 0.05, ...arms, rSh: [0.7, 0.5], rEl: -0.9 }),
  hurt: pose({ yaw: -0.45, lids: 0.1, brows: 0.6, browTilt: -0.6, smile: -0.25, ...arms }),
  chew: pose({ yaw: 0, pitch: 0.05, lids: 0.5, brows: 0, smile: -0.05, ...arms }),
  proud: pose({ yaw: -0.15, pitch: 0.3, lids: 0.15, brows: 0.4, smile: 0.4, ...arms, rSh: [0.55, 0.2], rEl: -0.9, lSh: [0.55, -0.1], lEl: -0.9 }),
  guard: pose({ yaw: -0.45, lids: 0.2, brows: 0.5, browTilt: -0.3, smile: -0.1, ...arms, lSh: [0.6, -0.2], lEl: -1.4 }),
  defeated: pose({ yaw: 0.05, pitch: 0.05, lids: 0.6, brows: -0.1, browTilt: -0.3, smile: -0.25, ...arms }),
  pickle: pose({ yaw: 0, pitch: 0.1, lids: 0.55, brows: -0.05, smile: -0.15, ...arms, ...eat }),
  last: pose({ yaw: 0.06, pitch: 0.02, lids: 0.55, brows: 0.15, browTilt: -0.3, smile: -0.25, ...arms, ...phone }),
}
const I = {
  phone: pose({ yaw: 0.1, pitch: 0.35, lids: 0.25, brows: 0.1, ...arms, ...phone }),
  casual: pose({ yaw: 0.35, pitch: 0.2, lids: 0.3, brows: 0.15, smile: 0.1, ...arms, ...phone }),
  look: pose({ yaw: 0.35, pitch: 0.25, lids: 0.05, brows: 0.45, smile: 0.25, ...arms, rSh: [0.45, -0.1], rEl: -1.4 }),
  sweet: pose({ yaw: 0.45, lids: 0.15, brows: 0.45, browTilt: -0.4, smile: 0.55, roll: -0.06, ...arms }),
  reach: pose({ yaw: 0.3, pitch: 0.3, lids: 0.1, brows: 0.3, smile: 0.4, ...arms, ...reach }),
  eat: pose({ yaw: 0.15, pitch: 0.05, lids: 0.35, brows: 0.15, smile: 0.3, ...arms, ...eat }),
  critic: pose({ yaw: 0.35, pitch: 0, lids: 0.35, brows: 0.25, browTilt: 0.3, smile: -0.1, ...arms, ...eat }),
  baby: pose({ yaw: 0.25, pitch: 0.3, lids: 0, brows: 0.6, browTilt: -0.6, smile: 0.6, ...arms, lSh: [0.6, 0.5], lEl: -2.0 }),
  full: pose({ yaw: 0.3, pitch: -0.12, lids: 0.6, brows: 0.2, smile: 0.4, lean: -0.08, ...arms, lSh: [0.3, 0.3], lEl: -1.5 }),
  ask: pose({ yaw: 0.45, lids: 0.15, brows: 0.5, smile: 0.1, ...arms }),
  order: pose({ yaw: 0.45, lids: 0.25, brows: 0.3, smile: 0.35, ...arms, lSh: [0.5, 0.4], lEl: -1.2 }),
  nothing: pose({ yaw: 0.2, pitch: 0.3, lids: 0.3, brows: 0.15, smile: 0.15, ...arms, ...phone }),
}

const DaniHand = () => (
  <group>
    <Show show={() => clock.t < T.deliver - 0.3 || (clock.t > T.app - 0.2)}><group rotation={[0.3, 0, 0]} position={[0, -0.02, 0.05]}><PhoneProp /></group></Show>
    <FryInHand show={() => (clock.t > T.fry1 && clock.t < T.look) || (clock.t > T.give - 0.2 && clock.t < T.give + 0.25)} />
  </group>
)
const LuciaHand = () => (
  <group>
    <Show show={() => clock.t < T.look + 0.2 || (clock.t > T.fries + 1.2)}><group rotation={[0.3, 0, 0]} position={[0, -0.02, 0.05]}><PhoneProp /></group></Show>
    <FryInHand show={() => (clock.t > T.takes2 + 0.2 && clock.t < T.chew + 1.0) || (clock.t > T.takes1 + 0.2 && clock.t < T.burger)} />
  </group>
)

const V = (x: number, y: number, z: number) => [x, y, z] as [number, number, number]
const F = V(0.12, 0.78, Z + 0.45) // food origin
const shots = {
  two: { p: V(0, HY + 0.22, Z + 2.75), l: V(0, HY - 0.18, Z), fov: 44, push: 0.3 },
  lucia: { p: V(-0.1, HY + 0.12, Z + 2.25), l: V(LX, HY - 0.1, Z), fov: 36, push: 0.1 },
  dani: { p: V(0.1, HY + 0.12, Z + 2.25), l: V(DX, HY - 0.1, Z), fov: 36, push: 0.1 },
  daniCam: { p: V(DX - 0.02, HY + 0.06, Z + 1.95), l: V(DX, HY - 0.06, Z), fov: 34, push: 0.06 },
  luciaClose: { p: V(LX + 0.05, HY + 0.06, Z + 1.95), l: V(LX, HY - 0.06, Z), fov: 34, push: 0.06 },
  food: { p: V(F[0] + 0.05, F[1] + 0.75, F[2] + 0.95), l: V(F[0] + 0.02, F[1] + 0.08, F[2]), fov: 36, push: 0.1 },
  fries: { p: V(F[0] - 0.1, F[1] + 0.42, F[2] + 0.62), l: V(F[0] - 0.12, F[1] + 0.12, F[2]), fov: 34, push: 0.06 },
  burger: { p: V(F[0] + 0.12, F[1] + 0.48, F[2] + 0.62), l: V(F[0] + 0.1, F[1] + 0.06, F[2] + 0.02), fov: 34, push: 0.06 },
  order: { p: V(INS.order[0], INS.order[1] + 0.01, 0.27), l: V(INS.order[0], INS.order[1], 0), fov: 36, push: 0.03 },
  again: { p: V(INS.again[0], INS.again[1] + 0.01, 0.27), l: V(INS.again[0], INS.again[1], 0), fov: 36, push: 0.03 },
}

const W = '{\\an8\\pos(540,70)\\fs34\\bord2\\shad0\\alpha&H50&}@pizarrapublica'
const spec: PairSpec = {
  id: 'pareja15',
  script: CONV.map((c) => ({ id: c.id, text: c.text })),
  fixedAt: at,
  gap: {},
  her: CONV.filter((c) => c.her).map((c) => c.id),
  talk: true,
  quiet: CONV.filter((c) => !c.her).map((c) => c.id), // he never speaks aloud: it's all in his head
  bg: '#1a1420',
  tail: 2.6,
  keyColor: '&H8A6A1E&',
  Set: () => (
    <group>
      <LivingRoom tv={() => 0.6} />
      <Food />
      <PhoneInsert p={INS.order} screen={<OrderScreen />} />
      <PhoneInsert p={INS.again} screen={<OrderScreen again />} />
    </group>
  ),
  pos: { lucia: [LX, 0.5, Z], dani: [DX, 0.5, Z] },
  shots,
  luciaHand: <LuciaHand />,
  daniHand: <DaniHand />,
  frame: (t) => {
    const dani = track([
      [0, D.phone], [A('Le pregunto') - 0.1, D.her], [A('Vale') - 0.1, D.cam], [T.deliver - 0.2, D.down], [A('Huele') - 0.1, D.happy],
      [A('Ella no levanta') - 0.1, D.her], [A('Bien') - 0.05, D.cam], [T.fry1 - 0.1, D.happy], [T.look + 0.2, D.wary],
      [A('No es una') - 0.1, D.cam], [A('¿Me das') + 0.6, D.wary], [T.give - 0.1, D.give], [T.takes2 + 0.2, D.hurt], [A('La más larga') + 0.2, D.cam],
      [T.chew - 0.1, D.chew], [T.takes1 - 0.05, D.hurt], [A('Para comprobarlo') + 0.1, D.cam], [T.burger - 0.15, D.proud],
      [T.eyes - 0.1, D.guard], [A('Bocadito') - 0.1, D.cam], [A('Le dejo') - 0.1, D.give], [T.bite + 0.2, D.hurt], [A('La mitad del') + 0.2, D.defeated],
      [T.left - 0.1, D.down], [T.pickle - 0.1, D.pickle], [A('Sigo con') - 0.1, D.cam], [T.app - 0.1, D.phone], [A('¿Vas a') + 0.5, D.her],
      [T.sure2 - 0.1, D.her], [A('No quiere nada') - 0.1, D.cam], [END - 0.1, D.last],
    ], t, 0.3)
    const lucia = track([
      [0, I.phone], [A('Que no, que no') - 0.15, I.casual], [A('Vale') + 0.3, I.phone], [T.look - 0.1, I.look], [A('¿Me das') - 0.1, I.sweet],
      [T.give + 0.1, I.reach], [T.takes2 + 0.3, I.eat], [A('Están un poco') - 0.1, I.critic], [T.takes1, I.reach], [T.takes1 + 0.5, I.eat],
      [T.eyes - 0.1, I.baby], [A('¿Me dejas') + 0.8, I.sweet], [A('Le dejo') + 0.1, I.reach], [T.bite, I.eat], [T.full - 0.1, I.full],
      [A('¿Vas a') - 0.1, I.ask], [T.fries - 0.1, I.order], [A('Que sí') - 0.1, I.ask], [A('Que sí') + 1.4, I.nothing],
    ], t, 0.3)
    // chewing while eating
    const chewing = (from: number, to: number) => t > from && t < to ? 0.12 + 0.18 * Math.abs(Math.sin(t * 7)) : 0
    dani.mouth = Math.max(dani.mouth, chewing(T.fry1 + 0.4, T.look), chewing(T.chew, T.chew + 1.6), chewing(T.pickle + 0.3, T.pickle + 1.6))
    lucia.mouth = Math.max(lucia.mouth, chewing(T.takes2 + 0.6, A('Están un poco') - 0.1), chewing(T.bite + 0.3, T.full - 0.2))
    return {
      dani, lucia,
      cuts: [
        [0, 'two'], [T.order - 0.1, 'order'], [A('Le pregunto') - 0.1, 'two'], [A('Que no, que no') - 0.08, 'lucia'], [A('Vale') - 0.1, 'daniCam'],
        [T.deliver - 0.1, 'two'], [T.open - 0.1, 'food'], [A('Ella no levanta') - 0.1, 'lucia'], [A('Bien') - 0.1, 'daniCam'], [T.fry1 - 0.1, 'dani'],
        [T.look - 0.1, 'luciaClose'], [A('No es una') - 0.1, 'daniCam'], [A('¿Me das') - 0.08, 'lucia'], [A('Una.') - 0.1, 'daniCam'],
        [T.give - 0.1, 'two'], [T.takes2 - 0.1, 'fries'], [A('Las dos que') - 0.1, 'daniCam'], [A('Silencio') - 0.1, 'two'],
        [A('Están un poco') - 0.08, 'lucia'], [T.takes1 - 0.1, 'fries'], [A('Para comprobarlo') - 0.1, 'daniCam'],
        [T.burger - 0.1, 'burger'], [T.eyes - 0.1, 'luciaClose'], [A('¿Me dejas') - 0.08, 'lucia'], [A('Bocadito') - 0.1, 'daniCam'],
        [A('Le dejo') - 0.1, 'two'], [T.bite - 0.1, 'burger'], [T.full - 0.08, 'lucia'], [T.left - 0.1, 'food'], [A('Sigo con') - 0.1, 'daniCam'],
        [T.app - 0.1, 'again'], [A('¿Vas a') - 0.08, 'lucia'], [A('Otra hamburguesa') - 0.1, 'dani'], [T.fries - 0.08, 'lucia'], [T.sure2 - 0.1, 'two'],
        [A('Que sí') - 0.08, 'lucia'], [A('No quiere nada') - 0.1, 'two'], [END - 0.1, 'daniCam'],
      ],
    }
  },
  sfx: () => [],
  overlays: (_l, dur): Overlay[] => [{ a: 0, b: dur, st: 'Mid', tx: W }],
}

export function Pareja15() { return <PairEpisode spec={spec} /> }
