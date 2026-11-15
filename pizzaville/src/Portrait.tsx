// Foto de perfil: retrato de Pizz (cara y hombros) sobre fondo liso.  /?portrait=1[&bg=%23...]
import { Canvas, useFrame } from '@react-three/fiber'
import * as THREE from 'three'
import { useMemo } from 'react'
import { Character, PIZZ_LOOK, newState } from './scene/Character'
import { params } from './engine/clock'

const BG = params.get('bg') ?? '#8fd18a'
const NOBG = BG === 'none'
const POSE = params.get('pose')
const P = (params.get('p') ?? '0.32,1.5,1.75,0,1.43,0,26').split(',').map(Number)

function Pose() {
  const st = useMemo(() => { const s = newState(); s.smile = 1; s.ry = -0.12; if (POSE) { s.action = POSE as never; s.actionW = 1; s.actionT = 0.6 }; s.lookAt = new THREE.Vector3(P[0], P[1] + 0.1, P[2]); return s }, [])
  useFrame(({ camera }) => {
    camera.position.set(P[0], P[1], P[2]); camera.lookAt(P[3], P[4], P[5])
    ;(camera as THREE.PerspectiveCamera).fov = P[6]; (camera as THREE.PerspectiveCamera).updateProjectionMatrix()
  })
  return <Character look={PIZZ_LOOK} state={st} />
}

export default function Portrait() {
  return (
    <Canvas shadows gl={{ antialias: true, preserveDrawingBuffer: true, alpha: true }} dpr={1} style={{ position: 'fixed', inset: 0, background: NOBG ? 'transparent' : BG }}>
      {!NOBG && <color attach="background" args={[BG]} />}
      <hemisphereLight args={['#ffffff', '#6a8a5a', 1.4]} />
      <directionalLight position={[2.5, 4, 4]} intensity={2.6} castShadow />
      <directionalLight position={[-3, 2, 1]} intensity={0.8} color="#ffe2c4" />
      <directionalLight position={[0, 3, -4]} intensity={1.4} color="#ffffff" />
      <Pose />
    </Canvas>
  )
}
