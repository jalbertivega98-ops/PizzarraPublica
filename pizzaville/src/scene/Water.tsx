import { useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'
import { heightAt, WATER_LEVEL, waterDist } from '../world/terrain'
import { clock } from '../engine/clock'
import { world } from '../engine/director'
import { NOISE_GLSL } from './glsl'

// Heightmap of the central valley baked once: lets the water shader know
// its depth → transparent shallows + animated shore foam.
const HM_RES = 512
const HM_SIZE = 820
function bakeHeightmap() {
  const data = new Float32Array(HM_RES * HM_RES)
  for (let j = 0; j < HM_RES; j++) for (let i = 0; i < HM_RES; i++) {
    const x = ((i + 0.5) / HM_RES - 0.5) * HM_SIZE
    const z = ((j + 0.5) / HM_RES - 0.5) * HM_SIZE
    data[j * HM_RES + i] = waterDist(x, z) < 24 ? heightAt(x, z) : 10
  }
  const t = new THREE.DataTexture(data, HM_RES, HM_RES, THREE.RedFormat, THREE.FloatType)
  t.magFilter = THREE.LinearFilter
  t.minFilter = THREE.LinearFilter
  t.needsUpdate = true
  return t
}

const vert = /* glsl */ `
varying vec3 vW;
#include <fog_pars_vertex>
void main(){
  vec4 w = modelMatrix * vec4(position,1.);
  vW = w.xyz;
  vec4 mvPosition = viewMatrix * w;
  gl_Position = projectionMatrix * mvPosition;
  #include <fog_vertex>
}`
const frag = /* glsl */ `
uniform float uTime; uniform sampler2D uHM; uniform float uHMSize; uniform float uLevel;
uniform vec3 uSunDir; uniform vec3 uSky; uniform vec3 uDeep; uniform vec3 uShallow;
varying vec3 vW;
#include <fog_pars_fragment>
${NOISE_GLSL}
void main(){
  vec2 uv = vW.xz / uHMSize + 0.5;
  float th = uLevel - 3.;
  if (uv.x>0. && uv.x<1. && uv.y>0. && uv.y<1.) th = texture2D(uHM, uv).r;
  float depth = uLevel - th;
  vec2 p = vW.xz;
  float e = 0.15;
  float t = uTime;
  float hA = pv_fbm(p*0.18 + vec2(t*0.25, t*0.12)) + 0.5*pv_fbm(p*0.6 - vec2(t*0.4, -t*0.3));
  float hX = pv_fbm((p+vec2(e,0.))*0.18 + vec2(t*0.25, t*0.12)) + 0.5*pv_fbm((p+vec2(e,0.))*0.6 - vec2(t*0.4, -t*0.3));
  float hZ = pv_fbm((p+vec2(0.,e))*0.18 + vec2(t*0.25, t*0.12)) + 0.5*pv_fbm((p+vec2(0.,e))*0.6 - vec2(t*0.4, -t*0.3));
  vec3 n = normalize(vec3(-(hX-hA)/e*0.35, 1., -(hZ-hA)/e*0.35));
  vec3 v = normalize(cameraPosition - vW);
  float fres = pow(1. - max(dot(n, v), 0.), 4.);
  float dcol = smoothstep(0.0, 2.2, depth);
  vec3 col = mix(uShallow, uDeep, dcol);
  col = mix(col, uSky, clamp(fres*0.85, 0., 0.85));
  vec3 r = reflect(-normalize(uSunDir), n);
  float spec = pow(max(dot(r, v), 0.), 160.) * 2.2;
  col += vec3(1.,0.95,0.85) * spec;
  // sparkles
  col += vec3(1.) * smoothstep(0.92, 1., pv_vnoise(p*3.1 + t*0.8)) * 0.18 * (1.-dcol*0.5);
  // foam at the shore
  float foamBand = 1. - smoothstep(0.0, 0.35 + 0.15*sin(t*1.4 + p.x*0.3), depth);
  float fn = pv_vnoise(p*1.7 + vec2(t*0.6, t*0.2));
  float foam = foamBand * smoothstep(0.35, 0.65, fn + foamBand*0.4);
  col = mix(col, vec3(0.96,0.98,1.), foam*0.85);
  float alpha = mix(0.55, 0.96, smoothstep(0.0, 1.2, depth));
  alpha = max(alpha, foam*0.9);
  if (depth < -0.05) discard;
  gl_FragColor = vec4(col, alpha);
  #include <tonemapping_fragment>
  #include <colorspace_fragment>
  #include <fog_fragment>
}`

export function WaterSurface() {
  const mat = useMemo(() => {
    const m = new THREE.ShaderMaterial({
      vertexShader: vert,
      fragmentShader: frag,
      transparent: true,
      fog: true,
      depthWrite: false,
      uniforms: THREE.UniformsUtils.merge([
        THREE.UniformsLib.fog,
        {
          uHMSize: { value: HM_SIZE }, uLevel: { value: WATER_LEVEL },
          uSunDir: { value: new THREE.Vector3(0, 1, 0) }, uSky: { value: new THREE.Color('#bcd8ee') },
          uDeep: { value: new THREE.Color('#1d6a8c') }, uShallow: { value: new THREE.Color('#58bdb2') },
        },
      ]),
    })
    m.uniforms.uHM = { value: bakeHeightmap() }
    m.uniforms.uTime = clock.uTime
    return m
  }, [])
  useFrame(() => {
    mat.uniforms.uSunDir.value.copy(world.sunDir)
    mat.uniforms.uSky.value.copy(world.fogColor).lerp(new THREE.Color('#9cc4e4'), 0.4)
  })
  return (
    <mesh material={mat} rotation-x={-Math.PI / 2} position-y={WATER_LEVEL} renderOrder={2}>
      <planeGeometry args={[9000, 9000, 1, 1]} />
    </mesh>
  )
}
