// Piezas compartidas por los episodios (carteles, puentes, vallas, marcador de parcela).
import { Billboard, Text } from '@react-three/drei'
import { mat } from '../scene/materials'

export function Tag({ text, y, color, bg = '#1a2233', big = false }: { text: string; y: number; color: string; bg?: string; big?: boolean }) {
  const fs = big ? 0.42 : 0.3
  const w = 0.6 + text.length * fs * 0.62
  return (
    <Billboard position={[0, y, 0]}>
      <mesh position={[0, 0, -0.01]} material={mat(bg, { transparent: true, opacity: big ? 0.95 : 0.8 })}>
        <planeGeometry args={[w, fs * 1.7]} />
      </mesh>
      <Text font="/fonts/fredoka600.woff" fontSize={fs} color={color} anchorX="center" anchorY="middle">{text}</Text>
    </Billboard>
  )
}

export function BigLabel({ text, position, color }: { text: string; position: [number, number, number]; color: string }) {
  return (
    <Billboard position={position}>
      <Text font="/fonts/lilita.woff" fontSize={9} color={color} outlineWidth={0.6} outlineColor="#1a2233" anchorX="center" anchorY="middle">{text}</Text>
    </Billboard>
  )
}

export function Bridge({ x }: { x: number }) {
  const z0 = -42, z1 = -80, y = 2.3
  const len = z0 - z1
  return (
    <group position={[x, y, (z0 + z1) / 2]}>
      <mesh material={mat('#9a6a43', { rough: 0.85 })} castShadow receiveShadow>
        <boxGeometry args={[4.2, 0.45, len]} />
      </mesh>
      {[-2, 2].map((s) => (
        <mesh key={s} position={[s, 0.75, 0]} material={mat('#6e4a2f', { rough: 0.9 })} castShadow>
          <boxGeometry args={[0.18, 0.18, len]} />
        </mesh>
      ))}
      {Array.from({ length: 9 }, (_, i) => [-2, 2].map((s) => (
        <mesh key={i + '_' + s} position={[s, 0.4, -len / 2 + 2 + i * (len - 4) / 8]} material={mat('#6e4a2f')}>
          <boxGeometry args={[0.16, 0.8, 0.16]} />
        </mesh>
      )))}
    </group>
  )
}

export function Fence({ w, d }: { w: number; d: number }) {
  const m = mat('#f2ede2', { rough: 0.8 })
  return (
    <group position={[0, 0.45, 0]}>
      {[[0, d / 2, w, 0.1], [0, -d / 2, w, 0.1], [w / 2, 0, 0.1, d], [-w / 2, 0, 0.1, d]].map(([x, z, a, b], i) => (
        <mesh key={i} position={[x, 0, z]} material={m}><boxGeometry args={[a, 0.7, b]} /></mesh>
      ))}
    </group>
  )
}

export function PlotMarker() {
  return (
    <group>
      <Billboard>
        <mesh material={mat('#ffffff', { rough: 0.4, emissive: '#ffffff', ei: 0.85 })} position={[0, 0, -0.02]}><circleGeometry args={[1.5, 32]} /></mesh>
        <mesh material={mat('#ff7a3d', { rough: 0.4, emissive: '#ff7a3d', ei: 0.8 })} position={[0, 0, -0.01]}><ringGeometry args={[1.25, 1.5, 32]} /></mesh>
        <Text font="/fonts/lilita.woff" fontSize={1.1} color="#ff7a3d" anchorX="center" anchorY="middle" position={[0, 0.08, 0]}>+</Text>
      </Billboard>
      <mesh position={[0, -2.2, 0]} material={mat('#ffffff', { transparent: true, opacity: 0.5 })}><cylinderGeometry args={[0.05, 0.05, 1.6, 6]} /></mesh>
    </group>
  )
}
