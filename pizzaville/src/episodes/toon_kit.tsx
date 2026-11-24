// Kit TOON de COSAS DE PAREJA (v2): varias escenas por episodio, personajes de cuerpo entero,
// caras 2D exageradas, efectos de cómic (flash, líneas de impacto, temblor de cámara).
import { useMemo, useRef, type ReactNode } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import * as THREE from 'three'
import { clock, ease, seg } from '../engine/clock'
import { useLines, type Line } from '../engine/voice'
import { ToonChar, T0, F0, mixT, DANI_T, LUCIA_T, type TPose, type Face } from '../scene/Toon'

export type FP = Partial<Face>
export const tp = (o: Partial<Omit<TPose, 'face'>> & { f?: FP } = {}): TPose => {
  const { f, ...rest } = o
  return { ...T0, ...rest, face: { ...F0, ...(f ?? {}) } }
}
/** override a pose: body fields and face fields */
export const with_ = (p: TPose, o: Partial<Omit<TPose, 'face'>> & { f?: FP }): TPose => {
  const { f, ...rest } = o
  return { ...p, ...rest, face: { ...p.face, ...(f ?? {}) } }
}

// ------- body bases
export const B = {
  stand: {},
  sit: { y: -0.2, hip: [-1.5, -1.5] as [number, number], knee: [1.5, 1.5] as [number, number] },
  pad: { lSh: [1.0, -0.3] as [number, number], lEl: -1.1, rSh: [1.0, -0.3] as [number, number], rEl: -1.1 }, // holding a controller
  wheel: { lSh: [1.35, 0.05] as [number, number], lEl: -0.35, rSh: [1.35, 0.05] as [number, number], rEl: -0.35 },
  hips: { lSh: [0.2, 0.55] as [number, number], lEl: -1.9, rSh: [0.2, 0.55] as [number, number], rEl: -1.9 }, // hands on hips
  armsUp: { lSh: [2.6, 0.5] as [number, number], lEl: -0.4, rSh: [2.6, 0.5] as [number, number], rEl: -0.4 },
  fists: { lSh: [0.5, 0.35] as [number, number], lEl: -2.0, rSh: [0.5, 0.35] as [number, number], rEl: -2.0 },
  hold: { rSh: [1.1, 0.1] as [number, number], rEl: -1.0 }, // holding something in the right hand in front
  hold2: { lSh: [1.1, 0.1] as [number, number], lEl: -1.0, rSh: [1.1, 0.1] as [number, number], rEl: -1.0 },
  faceHands: { lSh: [1.9, -0.35] as [number, number], lEl: -2.3, rSh: [1.9, -0.35] as [number, number], rEl: -2.3 },
  cheek: { lSh: [1.5, -0.1] as [number, number], lEl: -2.4 }, // hand on cheek (thinking)
  point: { rSh: [1.5, 0.15] as [number, number], rEl: -0.1 },
  shrug: { lSh: [0.4, 0.9] as [number, number], lEl: -1.6, rSh: [0.4, 0.9] as [number, number], rEl: -1.6 },
}

// ------- faces
export const FX = {
  calm: { smile: 0.15 },
  happy: { smile: 0.9, brow: 0.3, mouth: 0.25, sparkle: 0.3 },
  joy: { smile: 1, mouth: 0.7, brow: 0.6, eye: 1.15, sparkle: 1 },
  sweet: { smile: 0.8, brow: 0.5, ang: -0.3, open: 0.85, blush: 0.7, sparkle: 0.8, eye: 1.1 },
  cry: { tears: 1, open: 0.05, mouth: 0.75, smile: -0.7, brow: 0.6, ang: -0.9 },
  cryOpen: { tears: 0.9, open: 1, eye: 1.25, sparkle: 1, mouth: 0.45, smile: -0.4, brow: 0.7, ang: -0.8 },
  shock: { eye: 1.65, pupil: 0.4, mouth: 0.9, smile: -0.3, brow: 1, open: 1 },
  doubt: { open: 0.8, brow: 0.3, ang: -0.4, smile: -0.25, lx: 0.5, ly: -0.3 },
  annoyed: { open: 0.55, ang: 0.6, brow: -0.3, smile: -0.4, vein: 0.6 },
  angry: { ang: 1, brow: -0.7, teeth: 1, smile: -0.6, vein: 1, open: 0.9, pupil: 0.6, eye: 1.1 },
  scream: { ang: 1, brow: -0.6, mouth: 1, mw: 1.4, smile: -0.5, vein: 1, eye: 1.3, pupil: 0.5 },
  rage: { ang: 1, brow: -0.8, mouth: 1, mw: 1.5, smile: -0.5, vein: 1, rage: 1, eye: 1.35, pupil: 0.35 },
  fake: { teeth: 1, smile: 0.95, eye: 1.2, pupil: 0.6, brow: 0.5, ang: 0.2, vein: 0.7, sweat: 0.8 },
  dead: { open: 0.35, bags: 1, smile: -0.35, pupil: 0.7, brow: -0.1, ly: 0.3 },
  sneaky: { open: 0.5, lx: 0.8, smile: 0.45, ang: 0.5, brow: -0.2, sweat: 0.5 },
  suspicious: { open: 0.4, ang: 0.6, smile: -0.3, lx: 0.6, brow: -0.2 },
  sleepy: { open: 0.3, smile: -0.1, brow: 0.2, ang: -0.3 },
  gamer: { eye: 1.25, pupil: 0.55, ang: 0.8, brow: -0.5, teeth: 1, smile: 0.4, sparkle: 0.2, ly: 0.2 },
  focus: { eye: 1.1, ang: 0.7, brow: -0.4, smile: 0.35, open: 0.8, sparkle: 0.6 },
  hearts: { hearts: 1, smile: 1, mouth: 0.4, blush: 1 },
  dizzy: { spiral: 1, mouth: 0.4, smile: -0.2 },
  smug: { open: 0.55, smile: 0.8, ang: 0.3, brow: 0.2, lx: -0.4 },
  nervous: { eye: 1.3, pupil: 0.45, teeth: 1, smile: 0.4, sweat: 1, brow: 0.8, ang: -0.6 },
  sad: { open: 0.8, smile: -0.6, brow: 0.7, ang: -0.9, ly: 0.4 },
  camera: { open: 0.75, smile: -0.2, brow: 0.5, ang: -0.3 }, // deadpan to the viewer
}

export function trackT(keys: [number, TPose][], t: number, blend = 0.22): TPose {
  let i = 0
  while (i + 1 < keys.length && t >= keys[i + 1][0]) i++
  const cur = keys[i][1], prev = i > 0 ? keys[i - 1][1] : cur
  const k = i > 0 ? ease.inOut(seg(t, keys[i][0], keys[i][0] + blend)) : 1
  return mixT(prev, cur, k)
}

const VOW = /[aeiouáéíóúü]/gi
export function lip(l: Line | undefined, t: number) {
  if (!l) return 0
  const lt = t - l.at
  if (lt < 0 || lt > l.dur) return 0
  for (const w of l.words) if (lt >= w.t && lt <= w.t + w.d) {
    const syl = Math.max(1, (w.w.match(VOW) ?? []).length)
    return 0.15 + 0.85 * Math.pow(Math.abs(Math.sin(((lt - w.t) / w.d) * syl * Math.PI)), 0.7)
  }
  return 0
}

export type Shot = { p: [number, number, number]; l: [number, number, number]; fov: number; push?: number }
export const POP = '\\t(0,180,\\fscx112\\fscy112)\\t(180,360,\\fscx100\\fscy100)'
export type Overlay = { a: number; b: number; st: string; tx: string }
export const box = (a: number, b: number, y: number, size: number, tx: string, an = 5): Overlay =>
  ({ a, b, st: 'Box', tx: `{\\an${an}\\pos(540,${y})\\fad(80,120)${POP}\\fs${size}}${tx}` })

export type Place = { p: [number, number, number]; ry: number }
export type Scene = {
  id: string
  from: string // first line id of the scene
  at?: number // offset (s) relative to that line's start
  bg: string
  Set: (p: { st: Record<string, any> }) => ReactNode
  dani?: Place; lucia?: Place // undefined = not in the scene
  shots: Record<string, Shot>
}
export type Beat = {
  d?: TPose; l?: TPose; cut?: string; dAt?: number; lAt?: number; cutAt?: number; dMid?: TPose; lMid?: TPose
  flash?: string // flash colour at line start
  lines?: number // comic impact lines strength during the line
  shake?: number // camera shake during the line
  zoom?: number // punch-in on the cut (fov multiplier at the start, eases back)
}
export type ToonSpec = {
  id: string
  script: { id: string; kind: 'T' | 'D' | 'H'; text: string }[]
  gap: Record<string, number>
  scenes: Scene[]
  beats: Record<string, Beat>
  d0: TPose; l0: TPose; cut0: string
  frame?: (t: number, a: (id: string) => number, l: (id: string) => Line, st: Record<string, any>, f: { dani: TPose; lucia: TPose }) => void
  sfx: (l: (id: string) => Line) => { type: string; at: number; g?: number }[]
  overlays: (l: (id: string) => Line, dur: number) => Overlay[]
  music?: string
  tail?: number
  hands?: (st: Record<string, any>) => { dani?: ReactNode; danil?: ReactNode; lucia?: ReactNode; lucial?: ReactNode; daniHead?: ReactNode; luciaHead?: ReactNode }
  extras?: (st: Record<string, any>) => ReactNode
}

/** a thing that is visible only while show() is true */
export function Show({ show, children }: { show: () => boolean; children: ReactNode }) {
  const g = useRef<THREE.Group>(null!)
  useFrame(() => { g.current.visible = show() })
  return <group ref={g}>{children}</group>
}

function impactTexture() {
  const cv = document.createElement('canvas'); cv.width = 540; cv.height = 960
  const c = cv.getContext('2d')!
  c.fillStyle = '#000'
  let s = 7
  const rnd = () => ((s = (s * 16807) % 2147483647) / 2147483647)
  for (let i = 0; i < 90; i++) {
    const a = (i / 90) * Math.PI * 2 + rnd() * 0.05, w = 0.006 + rnd() * 0.018, r0 = 230 + rnd() * 140
    c.beginPath()
    c.moveTo(270 + Math.cos(a - w) * 1200, 480 + Math.sin(a - w) * 1200)
    c.lineTo(270 + Math.cos(a) * r0, 480 + Math.sin(a) * r0 * 1.5)
    c.lineTo(270 + Math.cos(a + w) * 1200, 480 + Math.sin(a + w) * 1200)
    c.fill()
  }
  const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace
  return t
}

export function ToonEpisode({ spec }: { spec: ToonSpec }) {
  const { camera, scene } = useThree()
  const lines = useMemo(() => useLines(spec.id, spec.script.map((s, i) => ({ ...s, at: i * 3 }))), [])
  const L = (id: string) => lines.find((l) => l.id === id)!
  const kind = (id: string) => spec.script.find((s) => s.id === id)!.kind
  const P = useMemo(() => new THREE.Vector3(), [])
  const LK = useMemo(() => new THREE.Vector3(), [])
  const st = useRef<Record<string, any>>({ scene: spec.scenes[0].id }).current
  const poses = useRef({ dani: spec.d0, lucia: spec.l0 })
  const hud = useRef<THREE.Group>(null!)
  const linesR = useRef<THREE.Mesh>(null!)
  const flashM = useMemo(() => new THREE.MeshBasicMaterial({ color: '#ffffff', transparent: true, opacity: 0, depthTest: false, depthWrite: false, toneMapped: false }), [])
  const linesM = useMemo(() => new THREE.MeshBasicMaterial({ map: impactTexture(), transparent: true, opacity: 0, depthTest: false, depthWrite: false, toneMapped: false }), [])
  const bgc = useMemo(() => new THREE.Color(), [])
  useMemo(() => { scene.background = new THREE.Color(spec.scenes[0].bg); scene.fog = null }, [])

  const layout = () => {
    for (let i = 0; i < lines.length; i++) lines[i].at = i === 0 ? 0.5 : lines[i - 1].at + lines[i - 1].dur + 0.1 + 0.55 * (spec.gap[lines[i].id] ?? 0)
  }
  const duration = () => { layout(); return Math.ceil((lines[lines.length - 1].at + lines[lines.length - 1].dur + (spec.tail ?? 2.0)) * 10) / 10 }

  useMemo(() => {
    const pv = (window as any).__pv
    if (!pv) return
    pv.info = () => {
      layout()
      const d = duration()
      return { id: spec.id, duration: d, music: spec.music ?? 'comedy', subStyle: 'box', overlays: spec.overlays(L, d), lines: lines.map((x) => ({ id: x.id, kind: kind(x.id), at: x.at, dur: x.dur, text: x.text, words: x.words, hasAudio: x.hasAudio })), sfx: spec.sfx(L) }
    }
  }, [])

  const sceneAt = (t: number) => {
    let cur = spec.scenes[0]
    for (const s of spec.scenes) if (t >= L(s.from).at - 0.1 + (s.at ?? 0)) cur = s
    return cur
  }

  useFrame(() => {
    layout()
    const t = clock.t
    const a = (id: string) => L(id).at
    const sc = sceneAt(t)
    st.scene = sc.id
    ;(scene.background as THREE.Color).set(sc.bg)
    // poses
    const dk: [number, TPose][] = [[0, spec.d0]], lk: [number, TPose][] = [[0, spec.l0]], cuts: [number, string, number][] = [[0, spec.cut0, 1]]
    let flash: [number, string] | null = null, shake = 0, impact = 0
    for (const s of spec.script) {
      const b = spec.beats[s.id]; if (!b) continue
      const s0 = a(s.id), du = L(s.id).dur
      if (b.d) dk.push([s0 + (b.dAt ?? 0), b.d])
      if (b.dMid) dk.push([s0 + du * 0.5, b.dMid])
      if (b.l) lk.push([s0 - 0.1 + (b.lAt ?? 0), b.l])
      if (b.lMid) lk.push([s0 + du * 0.5, b.lMid])
      if (b.cut) cuts.push([s0 - 0.1 + (b.cutAt ?? 0), b.cut, b.zoom ?? 1])
      if (b.flash && t >= s0 - 0.05 && t < s0 + 0.5) flash = [t - s0 + 0.05, b.flash]
      const inL = t >= s0 && t <= s0 + du + 0.2
      if (b.shake && inL) shake = Math.max(shake, b.shake)
      if (b.lines && inL) impact = Math.max(impact, b.lines * Math.min(1, (t - s0) * 6))
    }
    const by = (x: any[], y: any[]) => x[0] - y[0]
    dk.sort(by); lk.sort(by); cuts.sort(by)
    const dani = trackT(dk, t), lucia = trackT(lk, t)
    // lip-sync: D lines move Dani's mouth (T lines are thoughts: mouth shut), H lines move Lucía's
    let dm = 0, lm = 0
    for (const s of spec.script) { if (s.kind === 'D') dm = Math.max(dm, lip(L(s.id), t)); if (s.kind === 'H') lm = Math.max(lm, lip(L(s.id), t)) }
    if (dm > 0) dani.face = { ...dani.face, mouth: Math.max(dani.face.mouth * 0.5, dm * 0.75), teeth: dani.face.teeth > 0.5 && dm < 0.2 ? 1 : 0 }
    if (lm > 0) lucia.face = { ...lucia.face, mouth: Math.max(lucia.face.mouth * 0.5, lm * 0.75), teeth: 0 }
    // blinks
    const blink = (off: number) => ((t + off) % 3.7) < 0.11
    if (dani.face.open > 0.5 && dani.face.hearts < 0.5 && dani.face.spiral < 0.5 && blink(0.4)) dani.face = { ...dani.face, open: 0.05, smile: Math.min(dani.face.smile, 0.3) }
    if (lucia.face.open > 0.5 && lucia.face.hearts < 0.5 && blink(1.9)) lucia.face = { ...lucia.face, open: 0.05, smile: Math.min(lucia.face.smile, 0.3) }
    // idle breathing
    dani.squash += 0.012 * Math.sin(t * 2.3); lucia.squash += 0.012 * Math.sin(t * 2.1 + 1)
    const f = { dani, lucia }
    spec.frame?.(t, a, L, st, f)
    poses.current.dani = f.dani; poses.current.lucia = f.lucia

    // camera
    let ci = 0
    while (ci + 1 < cuts.length && t >= cuts[ci + 1][0]) ci++
    const [c0, name, zoom] = cuts[ci]
    const c1 = ci + 1 < cuts.length ? cuts[ci + 1][0] : c0 + 5
    const sh = sc.shots[name] ?? Object.values(sc.shots)[0]
    P.set(...sh.p); LK.set(...sh.l)
    const dir = LK.clone().sub(P).normalize()
    P.addScaledVector(dir, (sh.push ?? 0) * ease.out(seg(t, c0, c1 + 0.5)))
    P.x += Math.sin(t * 0.7) * 0.006; P.y += Math.sin(t * 1.1 + 1) * 0.005
    if (shake > 0) { P.x += Math.sin(t * 63) * 0.02 * shake; P.y += Math.sin(t * 47 + 2) * 0.02 * shake; LK.x += Math.sin(t * 59) * 0.01 * shake }
    camera.position.copy(P); camera.lookAt(LK)
    const pc = camera as THREE.PerspectiveCamera
    const zk = zoom !== 1 ? 1 + (zoom - 1) * (1 - ease.out(seg(t, c0, c0 + 0.45))) : 1
    const fov = sh.fov * zk
    if (Math.abs(pc.fov - fov) > 0.01) { pc.fov = fov; pc.updateProjectionMatrix() }
    // HUD (flash + impact lines) glued to the camera
    hud.current.position.copy(camera.position); hud.current.quaternion.copy(camera.quaternion)
    if (flash) { flashM.color.set(flash[1]); flashM.opacity = 0.85 * (1 - seg(flash[0], 0, 0.45)) } else flashM.opacity = 0
    linesM.opacity = impact * 0.85
    const hh = 2 * 0.3 * Math.tan(THREE.MathUtils.degToRad(fov / 2)) * 1.02
    linesR.current.scale.set(hh * pc.aspect, hh, 1)
    bgc.set(sc.bg)
  }, -1)

  const pl = (who: 'dani' | 'lucia') => () => { const s = spec.scenes.find((x) => x.id === st.scene)!; return s[who] ?? { p: [0, -50, 0] as [number, number, number], ry: 0 } }
  const vis = (who: 'dani' | 'lucia') => () => !!spec.scenes.find((x) => x.id === st.scene)![who]
  const H = useMemo(() => spec.hands?.(st) ?? {}, [])
  return (
    <group>
      {spec.scenes.map((s) => <Show key={s.id} show={() => st.scene === s.id}>{s.Set({ st })}</Show>)}
      <ToonChar look={LUCIA_T} pose={() => poses.current.lucia} place={pl('lucia')} visible={vis('lucia')} hand={H.lucia} lHand={H.lucial} headProps={H.luciaHead} />
      <ToonChar look={DANI_T} pose={() => poses.current.dani} place={pl('dani')} visible={vis('dani')} hand={H.dani} lHand={H.danil} headProps={H.daniHead} />
      {spec.extras?.(st)}
      <group ref={hud}>
        <mesh ref={linesR} position={[0, 0, -0.3]} material={linesM} renderOrder={998}><planeGeometry args={[1, 1]} /></mesh>
        <mesh position={[0, 0, -0.29]} material={flashM} renderOrder={999}><planeGeometry args={[1, 1.6]} /></mesh>
      </group>
    </group>
  )
}
