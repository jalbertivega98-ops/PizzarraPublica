export const NOISE_GLSL = /* glsl */ `
float pv_hash(vec2 p){ p = fract(p*vec2(123.34,456.21)); p += dot(p,p+45.32); return fract(p.x*p.y); }
float pv_vnoise(vec2 p){
  vec2 i = floor(p), f = fract(p);
  float a = pv_hash(i), b = pv_hash(i+vec2(1.,0.)), c = pv_hash(i+vec2(0.,1.)), d = pv_hash(i+vec2(1.,1.));
  vec2 u = f*f*(3.-2.*f);
  return mix(mix(a,b,u.x), mix(c,d,u.x), u.y);
}
float pv_fbm(vec2 p){ float s=0., a=.5; for(int i=0;i<4;i++){ s+=a*pv_vnoise(p); p*=2.03; a*=.5; } return s; }
`

import type * as THREE from 'three'

/** Adds wind sway to an (instanced) material. Height factor = local y / h. */
export function addWind(mat: THREE.Material, uTime: { value: number }, strength = 0.12, height = 6) {
  mat.onBeforeCompile = (shader) => {
    shader.uniforms.uTime = uTime
    shader.vertexShader = shader.vertexShader
      .replace('#include <common>', `#include <common>\nuniform float uTime;`)
      .replace(
        '#include <begin_vertex>',
        `#include <begin_vertex>
        {
          vec3 ip = vec3(0.);
          #ifdef USE_INSTANCING
            ip = instanceMatrix[3].xyz;
          #endif
          float hf = clamp(position.y / ${height.toFixed(2)}, 0., 1.);
          hf = hf*hf;
          float ph = ip.x*0.13 + ip.z*0.17;
          float w = sin(uTime*1.3 + ph) * 0.6 + sin(uTime*2.7 + ph*1.7) * 0.25;
          transformed.x += w * ${strength.toFixed(3)} * hf * ${height.toFixed(2)} * 0.15;
          transformed.z += cos(uTime*1.1 + ph*1.3) * ${(strength * 0.6).toFixed(3)} * hf * ${height.toFixed(2)} * 0.15;
        }`,
      )
  }
  mat.customProgramCacheKey = () => 'wind' + strength + '_' + height
}
