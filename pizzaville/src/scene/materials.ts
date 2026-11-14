import * as THREE from 'three'

const cache = new Map<string, THREE.Material>()

export function mat(color: string, o: { rough?: number; metal?: number; emissive?: string; ei?: number; vc?: boolean; side?: THREE.Side; transparent?: boolean; opacity?: number } = {}) {
  const key = JSON.stringify([color, o])
  let m = cache.get(key)
  if (!m) {
    m = new THREE.MeshStandardMaterial({
      color, roughness: o.rough ?? 0.8, metalness: o.metal ?? 0, vertexColors: !!o.vc, side: o.side ?? THREE.FrontSide,
      emissive: new THREE.Color(o.emissive ?? '#000000'), emissiveIntensity: o.ei ?? 1,
      transparent: !!o.transparent, opacity: o.opacity ?? 1, depthWrite: !o.transparent,
    })
    cache.set(key, m)
  }
  return m
}

/** materials whose emissive follows the night factor (windows, lamps) */
export const nightMats: { m: THREE.MeshStandardMaterial; day: number; night: number }[] = []
export function nightMat(color: string, emissive: string, day = 0.05, night = 1.6) {
  const key = 'night' + color + emissive + day + night
  let m = cache.get(key) as THREE.MeshStandardMaterial | undefined
  if (!m) {
    m = new THREE.MeshStandardMaterial({ color, roughness: 0.25, metalness: 0.1, emissive: new THREE.Color(emissive), emissiveIntensity: day })
    cache.set(key, m)
    nightMats.push({ m, day, night })
  }
  return m
}
