import { useMemo } from 'react'
import * as THREE from 'three'
import { heightAt, TERRAIN_SIZE, forestDensity, detailNoise, WATER_LEVEL, waterDist, ROAD, HOME_PATH } from '../world/terrain'
import { smoothstep, lerp } from '../world/rng'
import { NOISE_GLSL } from './glsl'


const C = (s: string) => new THREE.Color(s)
const grassA = C('#77b155'), grassB = C('#5f9c45'), grassDry = C('#a9b862'), grassDeep = C('#4c8a3c')
const forestC = C('#3f6f33'), sand = C('#d2c08e'), mud = C('#8d7f5d'), rock = C('#8d877c'), rockDark = C('#6c675f')
const snow = C('#f3f5f7'), dirt = C('#a68d62')

const INNER = 600
const INNER_STEP = 3
const RINGS_A = 512

/** hybrid mesh: dense square grid clipped to a disc + isotropic polar rings to the horizon */
export function buildTerrainGeometry() {
  const pos: number[] = []
  const idx: number[] = []
  // inner grid
  const n = Math.round((INNER * 2) / INNER_STEP) + 1
  const base0 = 0
  for (let j = 0; j < n; j++) for (let i = 0; i < n; i++) {
    const x = -INNER + i * INNER_STEP, z = -INNER + j * INNER_STEP
    pos.push(x, heightAt(x, z), z)
  }
  const r2 = (k: number) => pos[k * 3] ** 2 + pos[k * 3 + 2] ** 2
  const lim = INNER * INNER
  for (let j = 0; j < n - 1; j++) for (let i = 0; i < n - 1; i++) {
    const a = base0 + j * n + i, b = a + 1, c = a + n, d = c + 1
    if (r2(a) > lim && r2(b) > lim && r2(c) > lim && r2(d) > lim) continue
    if (Math.max(r2(a), r2(b), r2(c), r2(d)) > (INNER + 6) ** 2) continue
    if ((i + j) % 2) idx.push(a, c, b, b, c, d)
    else idx.push(a, c, d, a, d, b)
  }
  // outer rings
  const ringStart = pos.length / 3
  const radii: number[] = []
  let r = INNER - 12
  while (r < TERRAIN_SIZE / 2) { radii.push(r); r *= 1 + (Math.PI * 2) / RINGS_A }
  radii.push(TERRAIN_SIZE / 2)
  radii.forEach((rr, ri) => {
    for (let k = 0; k < RINGS_A; k++) {
      const a = (k / RINGS_A) * Math.PI * 2
      const x = Math.cos(a) * rr, z = Math.sin(a) * rr
      // tuck the overlap under the inner disc
      pos.push(x, heightAt(x, z) - (ri === 0 ? 0.6 : 0), z)
    }
  })
  for (let ri = 0; ri < radii.length - 1; ri++) for (let k = 0; k < RINGS_A; k++) {
    const k2 = (k + 1) % RINGS_A
    const a = ringStart + ri * RINGS_A + k, b = ringStart + ri * RINGS_A + k2
    const c = a + RINGS_A, d = b + RINGS_A
    idx.push(a, b, c, b, d, c)
  }
  const g = new THREE.BufferGeometry()
  g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3))
  g.setIndex(idx)
  g.computeVertexNormals()
  const count = pos.length / 3
  const col = new Float32Array(count * 3)
  const nor = g.getAttribute('normal') as THREE.BufferAttribute
  const tmp = new THREE.Color()
  for (let v = 0; v < count; v++) {
    const x = pos[v * 3], h = pos[v * 3 + 1], z = pos[v * 3 + 2]
    const ny = nor.getY(v)
    const slope = Math.sqrt(Math.max(0, 1 - ny * ny)) / Math.max(ny, 0.05)
    const r = Math.hypot(x, z)
    const dn = detailNoise(x, z)
    // base grass
    tmp.copy(grassA).lerp(grassB, 0.5 + 0.5 * dn)
    tmp.lerp(grassDry, smoothstep(0.35, 0.9, detailNoise(x * 0.3 + 40, z * 0.3)) * 0.55)
    tmp.lerp(grassDeep, smoothstep(0.2, 0.8, detailNoise(x * 0.12 - 9, z * 0.12 + 3)) * 0.4)
    // forests darken the floor (and colour far mountain slopes)
    const fd = forestDensity(x, z)
    if (r > 60) tmp.lerp(forestC, fd * smoothstep(60, 140, r) * 0.75)
    // water banks
    if (h < WATER_LEVEL + 1.4 && r < 3000) {
      const wd = waterDist(x, z)
      if (wd < 20) tmp.lerp(h < WATER_LEVEL + 0.2 ? mud : sand, smoothstep(WATER_LEVEL + 1.4, WATER_LEVEL + 0.3, h) * 0.9)
    }
    // rock on slopes and altitude
    const rockAmt = Math.max(smoothstep(0.75, 1.35, slope) * smoothstep(40, 160, h), smoothstep(300, 470, h) * 0.85)
    tmp.lerp(lerp(0, 1, 0.5 + 0.5 * dn) > 0.5 ? rock : rockDark, rockAmt)
    // snow caps
    const sn = smoothstep(560 + 50 * dn, 640 + 50 * dn, h) * (1 - smoothstep(1.0, 1.8, slope))
    tmp.lerp(snow, sn)
    // dirt tint near roads (the road ribbon itself sits on top)
    if (r < 1600) {
      const rd = Math.min(ROAD.query(x, z, 8).d, HOME_PATH.query(x, z, 4).d + 1.5)
      if (rd < 8) tmp.lerp(dirt, smoothstep(8, 3, rd) * 0.5)
    }
    col[v * 3] = tmp.r; col[v * 3 + 1] = tmp.g; col[v * 3 + 2] = tmp.b
  }
  g.setAttribute('color', new THREE.BufferAttribute(col, 3))
  g.computeBoundingSphere()
  return g
}

export function makeTerrainMaterial() {
  const m = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.95, metalness: 0 })
  m.onBeforeCompile = (s) => {
    s.vertexShader = s.vertexShader
      .replace('#include <common>', '#include <common>\nvarying vec3 vPvWorld;')
      .replace('#include <worldpos_vertex>', '#include <worldpos_vertex>\nvPvWorld = (modelMatrix * vec4(transformed,1.0)).xyz;')
    s.fragmentShader = s.fragmentShader
      .replace('#include <common>', '#include <common>\nvarying vec3 vPvWorld;\n' + NOISE_GLSL)
      .replace(
        '#include <color_fragment>',
        `#include <color_fragment>
        {
          float camD = length(vPvWorld - cameraPosition);
          float fade = 1. - smoothstep(60., 420., camD);
          float n1 = pv_fbm(vPvWorld.xz * 0.45);
          float n2 = pv_vnoise(vPvWorld.xz * 2.3);
          float big = pv_fbm(vPvWorld.xz * 0.012);
          diffuseColor.rgb *= mix(1.0, 0.86 + 0.26*n1 + 0.08*(n2-.5), fade);
          diffuseColor.rgb *= 0.9 + 0.2*big;
        }`,
      )
  }
  return m
}

export function Terrain() {
  const geo = useMemo(buildTerrainGeometry, [])
  const mat = useMemo(makeTerrainMaterial, [])
  return <mesh geometry={geo} material={mat} receiveShadow />
}
