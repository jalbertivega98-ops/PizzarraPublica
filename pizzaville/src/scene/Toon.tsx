// Personajes TOON de «Cosas de pareja» (v2, nov 2026): cuerpo entero, sombreado cartoon con contorno negro
// y una cara dibujada en 2D (canvas) sobre la cabeza, para expresiones exageradas: ojos saltones,
// lágrimas a chorro, venas, humo, cara roja, sudor, ojos de corazón o de espiral.
import { useMemo, useRef, type ReactNode } from 'react'
import { useFrame } from '@react-three/fiber'
import { Outlines } from '@react-three/drei'
import * as THREE from 'three'
import { clock } from '../engine/clock'

export type ToonLook = {
  skin: string; hair: string; top: string; pants: string; shoes: string; iris: string
  style: 'dani' | 'lucia'
}

export type Face = {
  open: number // eye openness 0..1
  eye: number // eye size (1 normal, 1.6 popping)
  pupil: number // pupil size (1 normal, 0.4 tiny = shock)
  lx: number; ly: number // gaze -1..1
  brow: number // -1 low … 1 high
  ang: number // + angry V … - worried
  mouth: number // 0 closed … 1 wide open
  smile: number // -1 frown … 1 grin
  mw: number // mouth width
  teeth: number // >0.5 gritted teeth / forced smile
  blush: number; tears: number; sweat: number; vein: number; rage: number; hearts: number; spiral: number; bags: number; sparkle: number
}
export type TPose = {
  // body
  y: number // root height offset
  hip: [number, number]; knee: [number, number] // legs [left, right]: hip pitch (- = forward), knee bend (+)
  lean: number; twist: number; roll: number
  yaw: number; pitch: number; tilt: number; head: number // head scale (exaggeration)
  lSh: [number, number]; lEl: number; rSh: [number, number]; rEl: number // shoulders [forward, out], elbows
  squash: number // body squash/stretch (+ stretch)
  shake: number // trembling amount
  face: Face
}

export const F0: Face = { open: 1, eye: 1, pupil: 1, lx: 0, ly: 0, brow: 0, ang: 0, mouth: 0, smile: 0.1, mw: 1, teeth: 0, blush: 0, tears: 0, sweat: 0, vein: 0, rage: 0, hearts: 0, spiral: 0, bags: 0, sparkle: 0 }
export const T0: TPose = { y: 0, hip: [0, 0], knee: [0, 0], lean: 0, twist: 0, roll: 0, yaw: 0, pitch: 0, tilt: 0, head: 1, lSh: [0.1, 0.12], lEl: -0.25, rSh: [0.1, 0.12], rEl: -0.25, squash: 0, shake: 0, face: F0 }

const lerp = (a: number, b: number, k: number) => a + (b - a) * k
export function mixFace(a: Face, b: Face, k: number): Face {
  const o: any = {}
  for (const key in a) o[key] = lerp((a as any)[key], (b as any)[key], k)
  return o
}
export function mixT(a: TPose, b: TPose, k: number): TPose {
  const L2 = (x: [number, number], y: [number, number]): [number, number] => [lerp(x[0], y[0], k), lerp(x[1], y[1], k)]
  return {
    y: lerp(a.y, b.y, k), hip: L2(a.hip, b.hip), knee: L2(a.knee, b.knee), lean: lerp(a.lean, b.lean, k), twist: lerp(a.twist, b.twist, k), roll: lerp(a.roll, b.roll, k),
    yaw: lerp(a.yaw, b.yaw, k), pitch: lerp(a.pitch, b.pitch, k), tilt: lerp(a.tilt, b.tilt, k), head: lerp(a.head, b.head, k),
    lSh: L2(a.lSh, b.lSh), lEl: lerp(a.lEl, b.lEl, k), rSh: L2(a.rSh, b.rSh), rEl: lerp(a.rEl, b.rEl, k), squash: lerp(a.squash, b.squash, k), shake: lerp(a.shake, b.shake, k),
    face: mixFace(a.face, b.face, k),
  }
}

// ---------------------------------------------------------------- toon materials
let GRAD: THREE.DataTexture | null = null
function grad() {
  if (GRAD) return GRAD
  const d = new Uint8Array([90, 90, 90, 255, 175, 175, 175, 255, 255, 255, 255, 255])
  GRAD = new THREE.DataTexture(d, 3, 1, THREE.RGBAFormat)
  GRAD.minFilter = GRAD.magFilter = THREE.NearestFilter
  GRAD.needsUpdate = true
  return GRAD
}
export const toon = (c: string, extra: Partial<THREE.MeshToonMaterialParameters> = {}) => new THREE.MeshToonMaterial({ color: c, gradientMap: grad(), ...extra })
export const OUT = 0.012
/** black cartoon contour around a mesh */
export const Ol = ({ w = OUT }: { w?: number }) => <Outlines thickness={w} color="#1a1216" />

// ---------------------------------------------------------------- face canvas
const W = 512
function ellipse(c: CanvasRenderingContext2D, x: number, y: number, rx: number, ry: number) { c.beginPath(); c.ellipse(x, y, Math.max(0.1, rx), Math.max(0.1, ry), 0, 0, Math.PI * 2) }
function heart(c: CanvasRenderingContext2D, x: number, y: number, s: number) {
  c.beginPath(); c.moveTo(x, y + s * 0.9)
  c.bezierCurveTo(x - s * 1.4, y - s * 0.1, x - s * 0.7, y - s * 1.2, x, y - s * 0.45)
  c.bezierCurveTo(x + s * 0.7, y - s * 1.2, x + s * 1.4, y - s * 0.1, x, y + s * 0.9); c.closePath()
}

function drawFace(c: CanvasRenderingContext2D, f: Face, look: ToonLook, t: number, skin: string) {
  c.clearRect(0, 0, W, W)
  const ink = '#1a1216'
  c.lineCap = 'round'; c.lineJoin = 'round'
  const ex = 92, ey = 250 // eye offset from center, eye line
  const R = 46 * f.eye, RY = 56 * f.eye
  // under-eye bags
  if (f.bags > 0.05) {
    c.strokeStyle = `rgba(90,60,110,${0.7 * Math.min(1, f.bags)})`; c.lineWidth = 7
    for (const s of [-1, 1]) { c.beginPath(); c.arc(256 + s * ex, ey + 30, 42, 0.25 * Math.PI, 0.75 * Math.PI); c.stroke(); c.beginPath(); c.arc(256 + s * ex, ey + 44, 34, 0.3 * Math.PI, 0.7 * Math.PI); c.stroke() }
  }
  // blush
  if (f.blush > 0.02 || f.rage > 0.02) {
    c.fillStyle = `rgba(255,80,90,${0.55 * Math.min(1, f.blush + f.rage * 0.4)})`
    for (const s of [-1, 1]) { ellipse(c, 256 + s * 150, 335, 44, 24); c.fill() }
  }
  // stubble for Dani
  if (look.style === 'dani') {
    c.fillStyle = 'rgba(60,40,40,0.13)'
    c.beginPath(); c.moveTo(110, 330); c.quadraticCurveTo(256, 520, 402, 330); c.quadraticCurveTo(256, 440, 110, 330); c.fill()
  }
  for (const s of [-1, 1]) {
    const x = 256 + s * ex
    if (f.hearts > 0.5) {
      const b = 1 + 0.12 * Math.sin(t * 14)
      c.fillStyle = '#ff2d55'; heart(c, x, ey, 48 * b * f.eye); c.fill(); c.lineWidth = 6; c.strokeStyle = ink; c.stroke()
      continue
    }
    if (f.spiral > 0.5) {
      c.fillStyle = '#fff'; ellipse(c, x, ey, R, RY); c.fill(); c.lineWidth = 6; c.strokeStyle = ink; c.stroke()
      c.beginPath(); for (let a = 0; a < 16; a += 0.2) { const r = a * 2.6; c.lineTo(x + Math.cos(a + t * 8 * s) * r, ey + Math.sin(a + t * 8 * s) * r) } c.lineWidth = 5; c.stroke()
      continue
    }
    const open = Math.max(0, Math.min(1, f.open))
    if (open < 0.12) {
      // closed: happy arcs when smiling, flat line otherwise, squeezed >< when crying hard
      c.strokeStyle = ink; c.lineWidth = 10; c.beginPath()
      if (f.tears > 0.6) { c.moveTo(x - 34, ey - 18); c.lineTo(x + 6 * s, ey); c.lineTo(x - 34, ey + 18); if (s < 0) { c.beginPath(); c.moveTo(x + 34, ey - 18); c.lineTo(x - 6, ey); c.lineTo(x + 34, ey + 18) } }
      else if (f.smile > 0.4) c.arc(x, ey + 14, 36, 1.15 * Math.PI, 1.85 * Math.PI)
      else { c.moveTo(x - 38, ey + 4); c.quadraticCurveTo(x, ey + 18, x + 38, ey + 4) }
      c.stroke()
    } else {
      c.save()
      ellipse(c, x, ey, R, RY); c.fillStyle = '#ffffff'; c.fill(); c.clip()
      const px = x + f.lx * R * 0.42, py = ey + f.ly * RY * 0.4
      const ir = 27 * Math.min(1.25, f.eye) * (0.55 + 0.45 * f.pupil)
      if (f.pupil > 0.45) { c.fillStyle = look.iris; ellipse(c, px, py, ir, ir * 1.12); c.fill() }
      c.fillStyle = ink; ellipse(c, px, py, ir * 0.55 * f.pupil, ir * 0.62 * f.pupil); c.fill()
      c.fillStyle = '#fff'; ellipse(c, px + ir * 0.35, py - ir * 0.4, 9 + 5 * f.sparkle, 10 + 5 * f.sparkle); c.fill()
      if (f.sparkle > 0.3) { ellipse(c, px - ir * 0.3, py + ir * 0.35, 5, 5); c.fill() }
      // upper lid
      const lidY = ey - RY + 2 * RY * (1 - open)
      c.fillStyle = skin; c.fillRect(x - R - 4, ey - RY - 10, 2 * R + 8, lidY - (ey - RY - 10))
      // angry lids slant
      if (f.ang > 0.3) { c.beginPath(); c.moveTo(x - R * s - 4 * s, ey - RY - 4); c.lineTo(x + R * s + 6 * s, ey - RY - 4); c.lineTo(x + R * s + 6 * s, ey - RY * (1 - f.ang * 0.9)); c.closePath(); c.fill() }
      if (f.ang < -0.3) { c.beginPath(); c.moveTo(x - R * s - 6 * s, ey - RY - 4); c.lineTo(x + R * s + 4 * s, ey - RY - 4); c.lineTo(x - R * s - 6 * s, ey - RY * (1 + f.ang * 0.7)); c.closePath(); c.fill() }
      c.restore()
      c.strokeStyle = ink; c.lineWidth = 7; ellipse(c, x, ey, R, RY); c.stroke()
      if (open < 0.97) { c.lineWidth = 9; c.beginPath(); c.moveTo(x - R, lidY); c.lineTo(x + R, lidY); c.stroke() }
      if (look.style === 'lucia') { // lashes
        c.lineWidth = 7; for (const k of [0.55, 0.85]) { const a = -Math.PI / 2 + s * k; c.beginPath(); c.moveTo(x + Math.cos(a) * R * 0.9 * s * s + s * R * 0.75, ey - RY * 0.55); c.lineTo(x + s * (R + 18), ey - RY * 0.55 - 18 * k); c.stroke() }
      }
    }
    // brows
    const bh = look.style === 'dani' ? 17 : 11
    const by = ey - RY - 26 - f.brow * 30 + (1 - Math.min(1, open)) * 6
    const a = f.ang * 0.5 * s
    c.save(); c.translate(x, by); c.rotate(a)
    c.fillStyle = look.style === 'dani' ? '#1e1714' : '#6b2c17'
    c.beginPath(); c.ellipse(0, 0, 50, bh, 0, Math.PI, 0); c.lineTo(50, 2); c.quadraticCurveTo(0, -bh * 0.2, -50, 2); c.fill()
    c.restore()
  }
  // mouth
  const mx = 256, my = 400, mw = 70 * f.mw, open = Math.max(0, f.mouth)
  c.strokeStyle = ink; c.lineWidth = 9
  if (f.teeth > 0.5 && open < 0.5) {
    // gritted teeth / forced smile
    const w = 92 * f.mw, h = 46, cy = my - f.smile * 10
    c.beginPath(); c.moveTo(mx - w, cy - h / 2 - f.smile * 18); c.quadraticCurveTo(mx, cy - h / 2 + f.smile * 14, mx + w, cy - h / 2 - f.smile * 18)
    c.lineTo(mx + w * 0.9, cy + h / 2 - f.smile * 10); c.quadraticCurveTo(mx, cy + h / 2 + f.smile * 34, mx - w * 0.9, cy + h / 2 - f.smile * 10); c.closePath()
    c.fillStyle = '#fff'; c.fill(); c.stroke()
    c.lineWidth = 5; c.beginPath(); c.moveTo(mx - w * 0.95, cy + 2); c.quadraticCurveTo(mx, cy + 2 + f.smile * 22, mx + w * 0.95, cy + 2); c.stroke()
    for (let i = -3; i <= 3; i++) { c.beginPath(); c.moveTo(mx + i * w * 0.27, cy - h / 2 + 4 + Math.abs(i) * -3); c.lineTo(mx + i * w * 0.27, cy + h / 2 - 2 + f.smile * (10 - Math.abs(i) * 4)); c.stroke() }
  } else if (open < 0.07) {
    c.beginPath(); c.moveTo(mx - mw, my - f.smile * 22); c.quadraticCurveTo(mx, my + f.smile * 40, mx + mw, my - f.smile * 22); c.stroke()
  } else {
    const h = 20 + open * 120, w = mw * (0.8 + open * 0.45)
    const top = my - f.smile * 18 - h * 0.15
    c.beginPath(); c.moveTo(mx - w, top); c.quadraticCurveTo(mx, top + f.smile * 34, mx + w, top)
    c.bezierCurveTo(mx + w, top + h * (0.9 + f.smile * 0.3), mx - w, top + h * (0.9 + f.smile * 0.3), mx - w, top)
    c.closePath(); c.fillStyle = '#5a1420'; c.fill()
    c.save(); c.clip()
    c.fillStyle = '#ff6f7d'; ellipse(c, mx, top + h * (0.82 + f.smile * 0.2), w * 0.55, h * 0.3); c.fill()
    c.fillStyle = '#fff'; c.fillRect(mx - w, top - 30, 2 * w, 30 + Math.min(26, h * 0.22) + f.smile * 8)
    c.restore()
    c.stroke()
  }
  // tears (waterfalls when tears ~1)
  if (f.tears > 0.05) {
    const k = Math.min(1, f.tears)
    for (const s of [-1, 1]) {
      const x = 256 + s * (ex + 10)
      c.fillStyle = `rgba(80,180,255,${0.85 * k})`
      const w2 = 10 + 22 * k
      c.beginPath(); c.moveTo(x - w2 / 2, ey + RY * 0.6); c.lineTo(x + w2 / 2, ey + RY * 0.6)
      c.lineTo(x + w2 / 2 + 8 * k, 512); c.lineTo(x - w2 / 2 - 8 * k, 512); c.closePath(); c.fill()
      c.fillStyle = `rgba(220,245,255,${0.9 * k})`
      for (let i = 0; i < 4; i++) { const yy = ey + RY * 0.6 + ((t * 420 + i * 60) % 260); ellipse(c, x, yy, 4, 10); c.fill() }
    }
  }
  // sweat drop
  if (f.sweat > 0.05) {
    const yy = 110 + ((t * 40) % 40), x = 400
    c.globalAlpha = Math.min(1, f.sweat)
    c.fillStyle = '#9fdcff'; c.beginPath(); c.moveTo(x, yy - 34); c.quadraticCurveTo(x + 26, yy + 6, x, yy + 16); c.quadraticCurveTo(x - 26, yy + 6, x, yy - 34); c.fill()
    c.lineWidth = 5; c.strokeStyle = ink; c.stroke(); c.globalAlpha = 1
  }
  // anger vein
  if (f.vein > 0.05) {
    const x = 360, y = 92, sc = 0.8 + 0.25 * Math.abs(Math.sin(t * 9))
    c.globalAlpha = Math.min(1, f.vein); c.strokeStyle = '#e0142c'; c.lineWidth = 12
    for (let q = 0; q < 4; q++) {
      const a = q * Math.PI / 2 + Math.PI / 4
      c.beginPath(); c.arc(x + Math.cos(a) * 28 * sc, y + Math.sin(a) * 28 * sc, 18 * sc, a + Math.PI * 0.55, a + Math.PI * 1.45); c.stroke()
    }
    c.globalAlpha = 1
  }
}

// ---------------------------------------------------------------- body pieces
function Limb({ len, r0, r1, mat, ol = true }: { len: number; r0: number; r1: number; mat: THREE.Material; ol?: boolean }) {
  return (
    <mesh material={mat} position={[0, -len / 2, 0]} castShadow>
      <capsuleGeometry args={[(r0 + r1) / 2, len, 4, 10]} />
      {ol && <Ol />}
    </mesh>
  )
}

function Hair({ style, mat }: { style: ToonLook['style']; mat: THREE.Material }) {
  if (style === 'dani') {
    return (
      <group>
        {/* cap of short hair, pushed back so the face stays free */}
        <mesh material={mat} position={[0, 0.06, -0.035]} rotation-x={-0.5} scale={[1.07, 0.95, 1.07]} castShadow>
          <sphereGeometry args={[0.3, 24, 14, 0, Math.PI * 2, 0, Math.PI * 0.5]} /><Ol />
        </mesh>
        {/* quiff */}
        {[[-0.1, 0.27, 0.13, 0.1], [0.02, 0.3, 0.15, 0.11], [0.13, 0.27, 0.12, 0.09]].map(([x, y, z, r], i) => (
          <mesh key={i} material={mat} position={[x, y, z]} scale={[1.2, 0.8, 1]} castShadow><sphereGeometry args={[r, 12, 8]} /><Ol /></mesh>
        ))}
        {/* sideburns */}
        {[-1, 1].map((s) => <mesh key={s} material={mat} position={[s * 0.285, -0.02, 0.02]} scale={[0.35, 1, 0.7]}><sphereGeometry args={[0.08, 10, 8]} /></mesh>)}
      </group>
    )
  }
  return (
    <group>
      <mesh material={mat} position={[0, 0.05, -0.03]} rotation-x={-0.42} scale={[1.08, 1.0, 1.09]} castShadow>
        <sphereGeometry args={[0.3, 24, 14, 0, Math.PI * 2, 0, Math.PI * 0.52]} /><Ol />
      </mesh>
      {/* side curtains of hair down to the shoulders */}
      {[-1, 1].map((s) => (
        <mesh key={s} material={mat} position={[s * 0.27, -0.12, -0.03]} rotation-z={s * 0.08} scale={[0.5, 1, 0.8]} castShadow>
          <capsuleGeometry args={[0.1, 0.32, 4, 10]} /><Ol />
        </mesh>
      ))}
      <mesh material={mat} position={[0, -0.1, -0.17]} scale={[1.25, 1, 0.55]} castShadow><capsuleGeometry args={[0.2, 0.3, 4, 12]} /><Ol /></mesh>
      {/* fringe */}
      <mesh material={mat} position={[-0.1, 0.22, 0.17]} rotation={[0.5, 0, 0.6]} scale={[1.5, 0.55, 0.8]} castShadow><sphereGeometry args={[0.1, 12, 8]} /><Ol /></mesh>
      <mesh material={mat} position={[0.12, 0.24, 0.15]} rotation={[0.5, 0, -0.4]} scale={[1.2, 0.5, 0.8]} castShadow><sphereGeometry args={[0.09, 12, 8]} /><Ol /></mesh>
      {/* high bun + scrunchie */}
      <mesh material={mat} position={[0, 0.36, -0.08]} castShadow><sphereGeometry args={[0.12, 14, 10]} /><Ol /></mesh>
      <mesh position={[0, 0.27, -0.06]} rotation-x={0.3}><torusGeometry args={[0.07, 0.025, 6, 14]} /><meshToonMaterial color="#ffd23f" gradientMap={grad()} /></mesh>
    </group>
  )
}

// ---------------------------------------------------------------- the character
export function ToonChar({ look, pose, place, hand, lHand, visible, headProps }: {
  look: ToonLook
  pose: () => TPose
  place: () => { p: [number, number, number]; ry: number }
  hand?: ReactNode // in the right hand
  lHand?: ReactNode
  visible?: () => boolean
  headProps?: ReactNode
}) {
  const root = useRef<THREE.Group>(null!), hips = useRef<THREE.Group>(null!), spine = useRef<THREE.Group>(null!), head = useRef<THREE.Group>(null!)
  const legs = [useRef<THREE.Group>(null!), useRef<THREE.Group>(null!)], knees = [useRef<THREE.Group>(null!), useRef<THREE.Group>(null!)]
  const sh = [useRef<THREE.Group>(null!), useRef<THREE.Group>(null!)], el = [useRef<THREE.Group>(null!), useRef<THREE.Group>(null!)]
  const steam = useRef<THREE.Group>(null!)
  const M = useMemo(() => ({
    skin: toon(look.skin), hair: toon(look.hair), top: toon(look.top), pants: toon(look.pants), shoes: toon(look.shoes), sole: toon('#f4f1ea'),
  }), [look])
  const baseSkin = useMemo(() => new THREE.Color(look.skin), [look])
  const red = useMemo(() => new THREE.Color('#ff3b30'), [])
  const face = useMemo(() => {
    const cv = document.createElement('canvas'); cv.width = cv.height = W
    const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4
    const mat = new THREE.MeshToonMaterial({ map: tex, transparent: true, gradientMap: grad(), depthWrite: false, polygonOffset: true, polygonOffsetFactor: -2 })
    return { cv, ctx: cv.getContext('2d')!, tex, mat }
  }, [])
  const HR = 0.27 // head radius
  const faceGeo = useMemo(() => new THREE.SphereGeometry(HR * 1.006, 40, 30, Math.PI / 2 - 1.0, 2.0, 0.6, 1.75), [])
  const tall = look.style === 'dani' ? 1 : 0.94

  useFrame(() => {
    const t = clock.t
    const p = pose(), pl = place()
    root.current.visible = visible ? visible() : true
    if (!root.current.visible) return
    const sk = p.shake * 0.025
    const jx = sk * Math.sin(t * 71), jy = sk * Math.sin(t * 53 + 1)
    root.current.position.set(pl.p[0] + jx, pl.p[1] + p.y + jy, pl.p[2])
    root.current.rotation.y = pl.ry
    const st = 1 + p.squash
    hips.current.scale.set(1 / Math.sqrt(st), st, 1 / Math.sqrt(st))
    spine.current.rotation.set(p.lean, p.twist, p.roll)
    head.current.rotation.set(p.pitch, p.yaw, p.tilt)
    head.current.scale.setScalar(p.head)
    for (let i = 0; i < 2; i++) {
      legs[i].current.rotation.x = p.hip[i]
      knees[i].current.rotation.x = p.knee[i]
    }
    sh[0].current.rotation.set(-p.lSh[0], 0, -p.lSh[1]); el[0].current.rotation.set(p.lEl, 0, 0)
    sh[1].current.rotation.set(-p.rSh[0], 0, p.rSh[1]); el[1].current.rotation.set(p.rEl, 0, 0)
    // face
    const rage = Math.min(1, p.face.rage)
    M.skin.color.copy(baseSkin).lerp(red, rage * 0.65)
    drawFace(face.ctx, p.face, look, t, '#' + M.skin.color.getHexString())
    face.tex.needsUpdate = true
    // steam out of the ears
    steam.current.visible = rage > 0.3
    steam.current.children.forEach((c, i) => {
      const ph = ((t * 1.6 + i * 0.27) % 1)
      const s = (i % 2 ? 1 : -1)
      c.position.set(s * (0.3 + ph * 0.35), 0.0 + ph * 0.5, -0.02)
      c.scale.setScalar((0.05 + ph * 0.16) * rage)
    })
  })

  return (
    <group ref={root}>
      <group ref={hips} position={[0, 0.62 * tall, 0]}>
        {/* pelvis */}
        <mesh material={M.pants} position={[0, 0.02, 0]} scale={[1, 0.7, 0.85]} castShadow><sphereGeometry args={[0.19, 16, 10]} /><Ol /></mesh>
        {/* legs */}
        {[-1, 1].map((s, i) => (
          <group key={s} ref={legs[i]} position={[s * 0.1, 0, 0]}>
            <Limb len={0.22 * tall} r0={0.085} r1={0.075} mat={M.pants} />
            <group ref={knees[i]} position={[0, -0.3 * tall, 0]}>
              <Limb len={0.22 * tall} r0={0.075} r1={0.065} mat={M.pants} />
              <group position={[0, -0.3 * tall, 0.05]}>
                <mesh material={M.shoes} scale={[0.9, 0.6, 1.5]} castShadow><sphereGeometry args={[0.085, 14, 8]} /><Ol /></mesh>
                <mesh material={M.sole} position={[0, -0.03, 0]} scale={[0.95, 0.25, 1.55]}><sphereGeometry args={[0.085, 14, 8]} /></mesh>
              </group>
            </group>
          </group>
        ))}
        {/* upper body */}
        <group ref={spine} position={[0, 0.05, 0]}>
          <mesh material={M.top} position={[0, 0.22, 0]} scale={[1, 1, 0.78]} castShadow>
            <capsuleGeometry args={[look.style === 'dani' ? 0.2 : 0.17, 0.2, 6, 16]} /><Ol />
          </mesh>
          {look.style === 'lucia' && <mesh material={M.top} position={[0, 0.1, 0]} scale={[1, 0.7, 0.85]}><sphereGeometry args={[0.21, 16, 10]} /><Ol /></mesh>}
          {/* arms */}
          {[-1, 1].map((s, i) => (
            <group key={s} ref={sh[i]} position={[s * (look.style === 'dani' ? 0.24 : 0.2), 0.37, 0]}>
              <group rotation-z={s * 0.0}>
                <Limb len={0.16} r0={0.06} r1={0.055} mat={M.top} />
                <group ref={el[i]} position={[0, -0.22, 0]}>
                  <Limb len={0.15} r0={0.05} r1={0.045} mat={M.skin} />
                  <mesh material={M.skin} position={[0, -0.24, 0]} castShadow><sphereGeometry args={[0.062, 12, 8]} /><Ol /></mesh>
                  {s === 1 && hand && <group position={[0, -0.27, 0.03]}>{hand}</group>}
                  {s === -1 && lHand && <group position={[0, -0.27, 0.03]}>{lHand}</group>}
                </group>
              </group>
            </group>
          ))}
          {/* neck + head */}
          <mesh material={M.skin} position={[0, 0.47, 0]}><cylinderGeometry args={[0.055, 0.065, 0.1, 10]} /></mesh>
          <group ref={head} position={[0, 0.5, 0]}>
            <group position={[0, HR * 0.95, 0]}>
              <mesh material={M.skin} scale={[1, 1.02, 0.96]} castShadow><sphereGeometry args={[HR, 32, 22]} /><Ol w={0.011} /></mesh>
              <mesh geometry={faceGeo} material={face.mat} scale={[1, 1.02, 0.96]} renderOrder={2} />
              {/* nose + ears */}
              <mesh material={M.skin} position={[0, -0.02, HR * 0.97]} scale={[1, 0.85, 0.8]}><sphereGeometry args={[0.04, 12, 8]} /><Ol w={0.006} /></mesh>
              {[-1, 1].map((s) => <mesh key={s} material={M.skin} position={[s * HR * 0.98, -0.01, 0]} scale={[0.45, 1, 0.75]}><sphereGeometry args={[0.07, 10, 8]} /><Ol w={0.006} /></mesh>)}
              <Hair style={look.style} mat={M.hair} />
              {headProps}
              <group ref={steam}>
                {Array.from({ length: 8 }).map((_, i) => <mesh key={i}><sphereGeometry args={[1, 10, 8]} /><meshToonMaterial color="#f4f4f4" gradientMap={grad()} transparent opacity={0.92} /></mesh>)}
              </group>
            </group>
          </group>
        </group>
      </group>
    </group>
  )
}

export const DANI_T: ToonLook = { style: 'dani', skin: '#f0b98f', hair: '#2a1d17', top: '#ffb627', pants: '#2f4b8c', shoes: '#e8423f', iris: '#6b3e1f' }
export const LUCIA_T: ToonLook = { style: 'lucia', skin: '#f6c9a8', hair: '#b4442a', top: '#8e5cf2', pants: '#2a2633', shoes: '#ffffff', iris: '#2e9a6b' }
