import { useMemo, useRef } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import * as THREE from 'three'
import { world } from '../engine/director'

// --------------------------------------------------------- time of day
type Sky = { zenith: THREE.Color; horizon: THREE.Color; sun: THREE.Color; sunI: number; hemiSky: THREE.Color; hemiGround: THREE.Color; hemiI: number; night: number }
const K = (h: number, zen: string, hor: string, sun: string, sunI: number, hemi: number) => ({ h, zen: new THREE.Color(zen), hor: new THREE.Color(hor), sun: new THREE.Color(sun), sunI, hemi })
const KEYS = [
  K(0, '#0b1430', '#1d2a4d', '#7a8cc4', 0.15, 0.25),
  K(5.5, '#1f2e5c', '#e79a6e', '#ff9a5c', 0.5, 0.45),
  K(7.5, '#4f8fd6', '#f3c9a1', '#ffd2a1', 2.2, 0.85),
  K(12, '#3f86da', '#bcd9ef', '#fff4e3', 3.0, 1.0),
  K(16.5, '#4a88d4', '#f2d6b0', '#ffdcae', 2.7, 0.95),
  K(19.2, '#3a4f8c', '#f19a6b', '#ff8a4d', 1.2, 0.6),
  K(20.6, '#141d40', '#3b3a66', '#8090d0', 0.25, 0.3),
  K(24, '#0b1430', '#1d2a4d', '#7a8cc4', 0.15, 0.25),
]
export function skyAt(hour: number): Sky {
  hour = ((hour % 24) + 24) % 24
  let i = 0
  while (i < KEYS.length - 2 && KEYS[i + 1].h <= hour) i++
  const a = KEYS[i], b = KEYS[i + 1]
  const t = (hour - a.h) / (b.h - a.h)
  const night = hour < 5.5 || hour > 20 ? 1 : hour < 7 ? 1 - (hour - 5.5) / 1.5 : hour > 19 ? (hour - 19) : 0
  return {
    zenith: a.zen.clone().lerp(b.zen, t),
    horizon: a.hor.clone().lerp(b.hor, t),
    sun: a.sun.clone().lerp(b.sun, t),
    sunI: THREE.MathUtils.lerp(a.sunI, b.sunI, t),
    hemiSky: a.zen.clone().lerp(b.zen, t).lerp(new THREE.Color('#ffffff'), 0.35),
    hemiGround: new THREE.Color('#5d6b3a').lerp(new THREE.Color('#1a2030'), night),
    hemiI: THREE.MathUtils.lerp(a.hemi, b.hemi, t),
    night: Math.min(1, Math.max(0, night)),
  }
}
export function sunDirection(hour: number, out = new THREE.Vector3()) {
  // sun rises east (+x), sets west (-x), tilted to the south (+z) so the
  // south-facing door of Pizz's house is lit in the afternoon
  const a = ((hour - 6) / 12) * Math.PI
  const el = Math.sin(a)
  out.set(Math.cos(a) * -0.9, Math.max(el, -0.3) * 0.95 + 0.05, 0.55).normalize()
  if (hour < 6 || hour > 18) out.set(-0.3, 0.6, 0.4).normalize() // moon light
  return out
}

const skyVert = /* glsl */ `
varying vec3 vDir;
void main(){ vDir = normalize(position); vec4 p = modelViewMatrix*vec4(position,1.); gl_Position = projectionMatrix*p; gl_Position.z = gl_Position.w; }`
const skyFrag = /* glsl */ `
uniform vec3 uZenith; uniform vec3 uHorizon; uniform vec3 uSun; uniform vec3 uSunDir; uniform float uNight; uniform float uTime;
varying vec3 vDir;
float h(vec3 p){ return fract(sin(dot(p, vec3(12.9898,78.233,45.164)))*43758.5453); }
void main(){
  vec3 d = normalize(vDir);
  float y = clamp(d.y, -1., 1.);
  float t = pow(clamp(y,0.,1.), 0.45);
  vec3 col = mix(uHorizon, uZenith, t);
  col = mix(col, uHorizon*0.85, smoothstep(0.0,-0.25,y));
  float sd = max(dot(d, normalize(uSunDir)), 0.);
  col += uSun * (pow(sd, 6.)*0.25 + pow(sd, 64.)*0.6) * (1.-uNight*0.7);
  col += uSun * smoothstep(0.9993, 0.9997, sd) * 2.5 * (1.-uNight);
  // stars
  if (uNight > 0.01 && y > 0.) {
    vec3 c = floor(d*420.);
    float s = step(0.9975, h(c));
    col += vec3(s) * uNight * smoothstep(0.,0.3,y) * (0.6+0.4*sin(uTime*3.+h(c)*50.));
  }
  gl_FragColor = vec4(col, 1.);
  #include <tonemapping_fragment>
  #include <colorspace_fragment>
}`

export function Atmosphere() {
  const { scene } = useThree()
  const sun = useRef<THREE.DirectionalLight>(null!)
  const hemi = useRef<THREE.HemisphereLight>(null!)
  const fill = useRef<THREE.DirectionalLight>(null!)
  const skyRef = useRef<THREE.Mesh>(null!)
  const skyMat = useMemo(
    () =>
      new THREE.ShaderMaterial({
        vertexShader: skyVert, fragmentShader: skyFrag, side: THREE.BackSide, depthWrite: false, fog: false,
        uniforms: { uZenith: { value: new THREE.Color() }, uHorizon: { value: new THREE.Color() }, uSun: { value: new THREE.Color() }, uSunDir: { value: new THREE.Vector3() }, uNight: { value: 0 }, uTime: { value: 0 } },
      }),
    [],
  )
  const fog = useMemo(() => new THREE.Fog('#cfe0ee', 300, 5200), [])
  scene.fog = fog
  const target = useMemo(() => new THREE.Object3D(), [])
  const dir = useMemo(() => new THREE.Vector3(), [])

  useFrame(({ camera }) => {
    const hour = world.hour
    skyRef.current.position.copy(camera.position)
    const s = skyAt(hour)
    sunDirection(hour, dir)
    skyMat.uniforms.uZenith.value.copy(s.zenith)
    skyMat.uniforms.uHorizon.value.copy(s.horizon)
    skyMat.uniforms.uSun.value.copy(s.sun)
    skyMat.uniforms.uSunDir.value.copy(dir)
    skyMat.uniforms.uNight.value = s.night
    fog.color.copy(s.horizon).lerp(s.zenith, 0.12)
    // fog adapts to camera altitude so aerial shots still see the horizon
    const alt = Math.max(0, camera.position.y)
    fog.near = 260 + alt * 1.2
    fog.far = 4200 + alt * 6
    world.fogColor.copy(fog.color)
    sun.current.color.copy(s.sun)
    sun.current.intensity = s.sunI
    hemi.current.color.copy(s.hemiSky)
    hemi.current.groundColor.copy(s.hemiGround)
    hemi.current.intensity = s.hemiI
    fill.current.intensity = 0.35 * s.hemiI
    // shadow frustum follows the director's focus
    const f = world.focus
    const span = world.shadowSpan
    target.position.copy(f)
    sun.current.position.copy(f).addScaledVector(dir, 400)
    const cam = sun.current.shadow.camera as THREE.OrthographicCamera
    if (cam.right !== span) {
      cam.left = -span; cam.right = span; cam.top = span; cam.bottom = -span
      cam.updateProjectionMatrix()
    }
    world.sunDir.copy(dir)
  })

  return (
    <>
      <mesh ref={skyRef} material={skyMat} renderOrder={-10} frustumCulled={false}>
        <sphereGeometry args={[9000, 32, 16]} />
      </mesh>
      <primitive object={target} />
      <directionalLight
        ref={sun}
        castShadow
        target={target}
        shadow-mapSize={[2048, 2048]}
        shadow-bias={-0.0004}
        shadow-normalBias={0.04}
        shadow-camera-near={10}
        shadow-camera-far={900}
      />
      <directionalLight ref={fill} position={[300, 200, -400]} color="#bcd4ff" />
      <hemisphereLight ref={hemi} />
    </>
  )
}
