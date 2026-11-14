import { useMemo } from 'react'
import * as THREE from 'three'
import { clock, holdReady } from '../engine/clock'

const texCache = new Map<string, THREE.Texture>()

/** loads the SVG flag (flag-icons, MIT) into a canvas texture */
export function flagTexture(iso: string) {
  iso = iso.toLowerCase()
  let t = texCache.get(iso)
  if (t) return t
  const canvas = document.createElement('canvas')
  canvas.width = 512; canvas.height = 384
  const ctx = canvas.getContext('2d')!
  ctx.fillStyle = '#ddd'; ctx.fillRect(0, 0, 512, 384)
  const tex = new THREE.CanvasTexture(canvas)
  tex.colorSpace = THREE.SRGBColorSpace
  tex.anisotropy = 4
  const done = holdReady()
  const img = new Image()
  img.onload = () => { ctx.drawImage(img, 0, 0, 512, 384); tex.needsUpdate = true; done() }
  img.onerror = () => done()
  img.src = `${import.meta.env.BASE_URL}flags/${iso}.svg`
  texCache.set(iso, tex)
  return tex
}

const flagGeo = new THREE.PlaneGeometry(1.4, 1.05, 24, 12).translate(0.7, -0.52, 0)

export function makeFlagMaterial(iso: string) {
  const m = new THREE.MeshStandardMaterial({ map: flagTexture(iso), side: THREE.DoubleSide, roughness: 0.85 })
  m.onBeforeCompile = (s) => {
    s.uniforms.uTime = clock.uTime
    s.vertexShader = s.vertexShader.replace('#include <common>', '#include <common>\nuniform float uTime;').replace(
      '#include <begin_vertex>',
      `#include <begin_vertex>
      float k = position.x / 1.4;
      transformed.z += sin(position.x*4.2 - uTime*6.0) * 0.12 * k + sin(position.y*3. + position.x*2. - uTime*4.) * 0.04 * k;
      transformed.y -= k*k*0.06;`,
    ).replace('#include <beginnormal_vertex>', `#include <beginnormal_vertex>
      objectNormal = normalize(vec3(-cos(position.x*4.2 - uTime*6.0)*0.5*(position.x/1.4), 0., 1.));`)
  }
  return m
}

export function Flag({ iso, scale = 1 }: { iso: string; scale?: number }) {
  const m = useMemo(() => makeFlagMaterial(iso), [iso])
  return <mesh geometry={flagGeo} material={m} position={[0.05, 0, 0]} scale={scale} castShadow />
}
