import { useMemo } from 'react'
import * as THREE from 'three'
import { ROAD, HOME_PATH, heightAt } from '../world/terrain'
import { NOISE_GLSL } from './glsl'

type Line = typeof ROAD

/** dirt ribbon following the terrain, soft alpha edges */
function ribbon(line: Line, halfW: number, step: number, s0 = 0, s1 = line.length) {
  const pos: number[] = [], uv: number[] = [], idx: number[] = []
  const across = 6
  let row = 0
  for (let s = s0; s <= s1 + 0.001; s += step) {
    const p = line.at(s)
    const nx = -p.tz, nz = p.tx
    for (let k = 0; k <= across; k++) {
      const u = k / across * 2 - 1
      const x = p.x + nx * u * halfW, z = p.z + nz * u * halfW
      pos.push(x, heightAt(x, z) + 0.06, z)
      uv.push(u, s)
    }
    if (row > 0) {
      const a = (row - 1) * (across + 1), b = row * (across + 1)
      for (let k = 0; k < across; k++) idx.push(a + k, b + k, a + k + 1, a + k + 1, b + k, b + k + 1)
    }
    row++
  }
  const g = new THREE.BufferGeometry()
  g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3))
  g.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2))
  g.setIndex(idx)
  g.computeVertexNormals()
  return g
}

function dirtMaterial(color: string) {
  const m = new THREE.MeshStandardMaterial({ color, roughness: 1, transparent: true, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -2 })
  m.onBeforeCompile = (s) => {
    s.vertexShader = s.vertexShader.replace('#include <common>', '#include <common>\nvarying vec2 vRUv;\nvarying vec3 vRW;').replace('#include <uv_vertex>', '#include <uv_vertex>\nvRUv = uv;').replace('#include <worldpos_vertex>', '#include <worldpos_vertex>\nvRW = (modelMatrix*vec4(transformed,1.)).xyz;')
    s.fragmentShader = s.fragmentShader
      .replace('#include <common>', '#include <common>\nvarying vec2 vRUv;\nvarying vec3 vRW;\n' + NOISE_GLSL)
      .replace(
        '#include <color_fragment>',
        `#include <color_fragment>
        float e = abs(vRUv.x);
        float n = pv_fbm(vRW.xz*0.7);
        float edge = 1. - smoothstep(0.62 + 0.25*n, 1.0, e);
        // wheel ruts & pebbles
        float rut = smoothstep(0.08, 0.0, abs(e - 0.42)) * 0.12;
        float peb = smoothstep(0.78, 0.92, pv_vnoise(vRW.xz*5.)) * 0.18;
        diffuseColor.rgb *= 0.86 + 0.28*n - rut + peb;
        diffuseColor.a *= edge;`,
      )
  }
  return m
}

export function Roads() {
  const road = useMemo(() => ribbon(ROAD, 3.1, 2), [])
  const path = useMemo(() => ribbon(HOME_PATH, 0.95, 0.5), [])
  const mat = useMemo(() => dirtMaterial('#b39a6c'), [])
  const pmat = useMemo(() => dirtMaterial('#bba479'), [])
  return (
    <group>
      <mesh geometry={road} material={mat} receiveShadow renderOrder={1} />
      <mesh geometry={path} material={pmat} receiveShadow renderOrder={1} />
    </group>
  )
}
