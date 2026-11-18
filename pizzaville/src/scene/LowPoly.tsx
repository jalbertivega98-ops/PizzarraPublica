// Personajes low-poly de «Cosas de pareja»: caras facetadas, ojos de punto, cejas gruesas.
// Pose = función pura del tiempo (la elige el episodio), así cada fotograma es reproducible.
import { useMemo, useRef, type ReactNode } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

export type LPLook = { skin: string; hair: string; top: string; hairStyle: 'dani' | 'lucia'; eye?: string }

export type LPPose = {
  yaw: number; pitch: number; roll: number; lean: number; side: number
  lSh: [number, number]; lEl: number; rSh: [number, number]; rEl: number
  brows: number // -1 angry … 0 … 1 surprised/sad-raised
  browTilt: number // + = angry V, - = worried
  lids: number // 0 open … 1 closed
  mouth: number // 0 closed … 1 open (lip-sync)
  smile: number // -1 frown … 1 smile
  sink: number // slide down into the bed (m)
}

export const P0: LPPose = { yaw: 0, pitch: 0, roll: 0, lean: 0, side: 0, lSh: [0.25, 0.15], lEl: -0.9, rSh: [0.25, -0.15], rEl: -0.9, brows: 0, browTilt: 0, lids: 0, mouth: 0, smile: 0, sink: 0 }

export function mixPose(a: LPPose, b: LPPose, k: number): LPPose {
  const L = (x: number, y: number) => x + (y - x) * k
  return {
    yaw: L(a.yaw, b.yaw), pitch: L(a.pitch, b.pitch), roll: L(a.roll, b.roll), lean: L(a.lean, b.lean), side: L(a.side, b.side),
    lSh: [L(a.lSh[0], b.lSh[0]), L(a.lSh[1], b.lSh[1])], lEl: L(a.lEl, b.lEl), rSh: [L(a.rSh[0], b.rSh[0]), L(a.rSh[1], b.rSh[1])], rEl: L(a.rEl, b.rEl),
    brows: L(a.brows, b.brows), browTilt: L(a.browTilt, b.browTilt), lids: L(a.lids, b.lids), mouth: L(a.mouth, b.mouth), smile: L(a.smile, b.smile), sink: L(a.sink, b.sink),
  }
}

const flat = (c: string, rough = 0.85) => new THREE.MeshStandardMaterial({ color: c, roughness: rough, flatShading: true })

function hairGeo(style: LPLook['hairStyle']) {
  const parts: THREE.BufferGeometry[] = []
  const add = (g: THREE.BufferGeometry, x: number, y: number, z: number, sx = 1, sy = 1, sz = 1, rx = 0, ry = 0, rz = 0) => {
    g.applyMatrix4(new THREE.Matrix4().compose(new THREE.Vector3(x, y, z), new THREE.Quaternion().setFromEuler(new THREE.Euler(rx, ry, rz)), new THREE.Vector3(sx, sy, sz)))
    parts.push(g.toNonIndexed())
  }
  if (style === 'dani') {
    // short curly black hair: a cap plus lumpy curls
    add(new THREE.SphereGeometry(0.275, 9, 6, 0, Math.PI * 2, 0, Math.PI * 0.5), 0, 0.03, -0.015, 1.02, 1.0, 1.02, -0.25)
    for (let i = 0; i < 14; i++) {
      const a = (i / 14) * Math.PI * 2, r = 0.2 + (i % 3) * 0.02
      add(new THREE.IcosahedronGeometry(0.075 + (i % 2) * 0.015, 0), Math.cos(a) * r, 0.2 + (i % 3) * 0.025, Math.sin(a) * r * 0.9 - 0.02)
    }
    add(new THREE.IcosahedronGeometry(0.09, 0), 0.04, 0.27, 0.06)
    add(new THREE.IcosahedronGeometry(0.08, 0), -0.07, 0.26, 0.1)
  } else {
    // long copper hair with a messy bun on top
    add(new THREE.SphereGeometry(0.28, 9, 7, 0, Math.PI * 2, 0, Math.PI * 0.55), 0, 0.02, -0.01, 1.03, 1.0, 1.04, -0.2)
    add(new THREE.IcosahedronGeometry(0.13, 1), 0, 0.34, -0.06)
    add(new THREE.IcosahedronGeometry(0.07, 0), 0.08, 0.36, 0.0)
    add(new THREE.CylinderGeometry(0.27, 0.31, 0.44, 9, 1, true, Math.PI * 0.42, Math.PI * 1.16), 0, -0.14, -0.03, 1, 1, 1)
    add(new THREE.BoxGeometry(0.09, 0.4, 0.12), 0.25, -0.12, 0.04, 1, 1, 1, 0, 0, 0.06)
    add(new THREE.BoxGeometry(0.09, 0.4, 0.12), -0.25, -0.12, 0.04, 1, 1, 1, 0, 0, -0.06)
    add(new THREE.BoxGeometry(0.22, 0.07, 0.1), -0.06, 0.2, 0.2, 1, 1, 1, 0.5, 0, 0.35)
  }
  const merged = new THREE.BufferGeometry()
  const pos: number[] = []
  for (const p of parts) pos.push(...(p.getAttribute('position').array as Float32Array))
  merged.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3))
  merged.computeVertexNormals()
  return merged
}

export function LowPolyChar({ look, pose, position, ry = 0, hand, topColor }: { look: LPLook; pose: () => LPPose; position: [number, number, number]; ry?: number; hand?: ReactNode; topColor?: () => string | undefined }) {
  const root = useRef<THREE.Group>(null!)
  const chest = useRef<THREE.Group>(null!)
  const head = useRef<THREE.Group>(null!)
  const lSh = useRef<THREE.Group>(null!), rSh = useRef<THREE.Group>(null!), lEl = useRef<THREE.Group>(null!), rEl = useRef<THREE.Group>(null!)
  const eyes = useRef<THREE.Group>(null!), lidsG = useRef<THREE.Group>(null!)
  const bl = useRef<THREE.Mesh>(null!), br = useRef<THREE.Mesh>(null!)
  const mOpen = useRef<THREE.Mesh>(null!), mLine = useRef<THREE.Mesh>(null!)
  const M = useMemo(() => ({ skin: flat(look.skin, 0.75), hair: flat(look.hair, 0.9), top: flat(look.top, 0.9), black: new THREE.MeshStandardMaterial({ color: '#141014', roughness: 0.4 }), white: new THREE.MeshBasicMaterial({ color: '#ffffff' }), mouth: flat('#3a1418', 0.8) }), [look])
  const hair = useMemo(() => hairGeo(look.hairStyle), [look.hairStyle])
  const headGeo = useMemo(() => { const g = new THREE.IcosahedronGeometry(0.27, 2); g.scale(1, 1.06, 0.97); return g }, [])

  useFrame(() => {
    const p = pose()
    const tc = topColor?.()
    if (tc && '#' + M.top.color.getHexString() !== tc.toLowerCase()) M.top.color.set(tc)
    root.current.position.set(position[0] + p.side, position[1] - p.sink, position[2])
    root.current.rotation.y = ry
    chest.current.rotation.set(p.lean, 0, p.roll * 0.3)
    head.current.rotation.set(p.pitch, p.yaw, p.roll)
    lSh.current.rotation.set(-p.lSh[0], 0, p.lSh[1]); lEl.current.rotation.set(p.lEl, 0, 0)
    rSh.current.rotation.set(-p.rSh[0], 0, p.rSh[1]); rEl.current.rotation.set(p.rEl, 0, 0)
    const lid = THREE.MathUtils.clamp(p.lids, 0, 1)
    eyes.current.scale.y = Math.max(0.08, 1 - lid)
    lidsG.current.visible = lid > 0.85
    eyes.current.visible = lid <= 0.85
    const by = 0.105 + p.brows * 0.03 - lid * 0.015
    bl.current.position.y = by; br.current.position.y = by
    bl.current.rotation.z = -p.browTilt * 0.35; br.current.rotation.z = p.browTilt * 0.35
    const m = THREE.MathUtils.clamp(p.mouth, 0, 1)
    mOpen.current.visible = m > 0.08; mLine.current.visible = m <= 0.08
    mOpen.current.scale.set(0.9 + m * 0.2, 0.25 + m * 0.75, 1)
    mLine.current.rotation.z = p.smile * 0.22 // smirk
  })

  return (
    <group ref={root}>
      <group ref={chest}>
        {/* torso (sits on the bed, lower body hidden under the duvet) */}
        <mesh material={M.top} position={[0, 0.32, 0]} castShadow><cylinderGeometry args={[0.24, 0.3, 0.62, 8]} /></mesh>
        <mesh material={M.top} position={[0, 0.64, 0]} castShadow><sphereGeometry args={[0.24, 8, 4, 0, Math.PI * 2, 0, Math.PI / 2]} /></mesh>
        <mesh material={M.skin} position={[0, 0.72, 0]}><cylinderGeometry args={[0.07, 0.08, 0.12, 7]} /></mesh>
        {/* arms */}
        {([[1, lSh, lEl], [-1, rSh, rEl]] as const).map(([s, sh, el]) => (
          <group key={s} ref={sh} position={[s * 0.29, 0.58, 0]}>
            <mesh material={M.top} position={[0, -0.13, 0]} castShadow><cylinderGeometry args={[0.075, 0.07, 0.28, 7]} /></mesh>
            <group ref={el} position={[0, -0.27, 0]}>
              <mesh material={M.skin} position={[0, -0.12, 0]} castShadow><cylinderGeometry args={[0.06, 0.055, 0.25, 7]} /></mesh>
              <mesh material={M.skin} position={[0, -0.27, 0]} castShadow><icosahedronGeometry args={[0.068, 0]} /></mesh>
              {s === -1 && hand && <group position={[0, -0.3, 0]}>{hand}</group>}
            </group>
          </group>
        ))}
        {/* head */}
        <group ref={head} position={[0, 0.78, 0]}>
          <group position={[0, 0.25, 0]}>
            <mesh geometry={headGeo} material={M.skin} castShadow />
            <mesh geometry={hair} material={M.hair} castShadow />
            {[1, -1].map((s) => <mesh key={s} material={M.skin} position={[s * 0.265, -0.01, 0]} scale={[0.5, 1, 0.8]}><icosahedronGeometry args={[0.055, 0]} /></mesh>)}
            <mesh material={M.skin} position={[0, -0.03, 0.262]}><icosahedronGeometry args={[0.035, 0]} /></mesh>
            <group ref={eyes} position={[0, 0.035, 0]}>
              {[1, -1].map((s) => (
                <group key={s} position={[s * 0.095, 0, 0.245]}>
                  <mesh material={M.black}><sphereGeometry args={[0.028, 10, 8]} /></mesh>
                  <mesh material={M.white} position={[0.009, 0.01, 0.024]}><circleGeometry args={[0.007, 8]} /></mesh>
                </group>
              ))}
            </group>
            <group ref={lidsG} position={[0, 0.03, 0.262]}>
              {[1, -1].map((s) => <mesh key={s} material={M.black} position={[s * 0.095, 0, 0]}><boxGeometry args={[0.06, 0.009, 0.01]} /></mesh>)}
            </group>
            <mesh ref={bl} material={M.black} position={[0.095, 0.105, 0.245]}><boxGeometry args={[0.085, 0.022, 0.02]} /></mesh>
            <mesh ref={br} material={M.black} position={[-0.095, 0.105, 0.245]}><boxGeometry args={[0.085, 0.022, 0.02]} /></mesh>
            <mesh ref={mLine} material={M.black} position={[0, -0.1, 0.255]}><boxGeometry args={[0.07, 0.012, 0.01]} /></mesh>
            <mesh ref={mOpen} material={M.mouth} position={[0, -0.105, 0.248]} scale={[1, 0.5, 1]}><sphereGeometry args={[0.035, 10, 8]} /></mesh>
          </group>
        </group>
      </group>
    </group>
  )
}
