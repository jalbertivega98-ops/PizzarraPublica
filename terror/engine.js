// MOTOR TERROR — casa oscura en primera persona con linterna (Three.js)
// Determinista: window.renderAt(t) dibuja el fotograma del segundo t.
import * as THREE from 'three';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { ShaderPass } from 'three/addons/postprocessing/ShaderPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';

export const W = 1080, H = 1920;

// ---------- utilidades ----------
export function rng(seed) { let s = seed >>> 0; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); }
export const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
export const smooth = (x) => { x = clamp(x); return x * x * (3 - 2 * x); };
export const lerp = (a, b, k) => a + (b - a) * k;
export const win = (t, a, b) => clamp((t - a) / (b - a));
function hash(n) { return (Math.sin(n * 127.1) * 43758.5453) % 1; }
export function noise1(x) { const i = Math.floor(x), f = x - i; const a = Math.abs(hash(i)), b = Math.abs(hash(i + 1)); return lerp(a, b, f * f * (3 - 2 * f)); }

// ---------- texturas procedurales ----------
function canvasTex(w, h, draw, repeat = [1, 1], srgb = true) {
  const c = document.createElement('canvas'); c.width = w; c.height = h;
  const g = c.getContext('2d'); draw(g, w, h);
  const t = new THREE.CanvasTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(...repeat);
  if (srgb) t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 4; return t;
}
function grime(g, w, h, r, n = 60, col = '0,0,0', amax = 0.25) {
  for (let i = 0; i < n; i++) {
    const x = r() * w, y = r() * h, rad = 20 + r() * w * 0.25;
    const gr = g.createRadialGradient(x, y, 0, x, y, rad);
    gr.addColorStop(0, `rgba(${col},${r() * amax})`); gr.addColorStop(1, `rgba(${col},0)`);
    g.fillStyle = gr; g.fillRect(0, 0, w, h);
  }
}
function speckle(g, w, h, r, n, a = 0.15) {
  for (let i = 0; i < n; i++) { const v = r() < 0.5 ? 0 : 255; g.fillStyle = `rgba(${v},${v},${v},${r() * a})`; g.fillRect(r() * w, r() * h, 1 + r() * 2, 1 + r() * 2); }
}
export const TEX = {};
export function makeTextures() {
  const r = rng(7);
  TEX.wood = canvasTex(512, 512, (g, w, h) => {
    const pl = 6;
    for (let i = 0; i < pl; i++) {
      const base = 40 + r() * 25; g.fillStyle = `rgb(${base + 22},${base + 8},${base - 8})`; g.fillRect(i * w / pl, 0, w / pl, h);
      for (let k = 0; k < 90; k++) { g.strokeStyle = `rgba(20,8,0,${0.08 + r() * 0.15})`; g.lineWidth = 1 + r() * 2; const x = i * w / pl + r() * w / pl; g.beginPath(); g.moveTo(x, 0); g.bezierCurveTo(x + r() * 8 - 4, h / 3, x + r() * 8 - 4, 2 * h / 3, x + r() * 6 - 3, h); g.stroke(); }
      g.fillStyle = 'rgba(0,0,0,0.85)'; g.fillRect(i * w / pl, 0, 3, h);
      const cut = r() * h; g.fillRect(i * w / pl, cut, w / pl, 3);
    }
    grime(g, w, h, r, 40, '0,0,0', 0.4); speckle(g, w, h, r, 3000);
  }, [1.2, 4]);
  TEX.wallpaper = canvasTex(512, 512, (g, w, h) => {
    g.fillStyle = '#3b4434'; g.fillRect(0, 0, w, h);
    g.strokeStyle = 'rgba(160,150,110,0.25)'; g.lineWidth = 3;
    for (let y = 0; y < 4; y++) for (let x = 0; x < 3; x++) {
      const cx = x * w / 2.5 + (y % 2) * w / 5 + 40, cy = y * h / 3.5 + 60;
      g.beginPath(); g.ellipse(cx, cy, 34, 54, 0, 0, Math.PI * 2); g.stroke();
      g.beginPath(); g.moveTo(cx, cy - 70); g.quadraticCurveTo(cx + 40, cy, cx, cy + 70); g.quadraticCurveTo(cx - 40, cy, cx, cy - 70); g.stroke();
      g.beginPath(); g.arc(cx, cy, 10, 0, Math.PI * 2); g.stroke();
    }
    for (let x = 0; x < w; x += 64) { g.fillStyle = 'rgba(0,0,0,0.12)'; g.fillRect(x, 0, 4, h); }
    grime(g, w, h, r, 50, '20,15,5', 0.5);
    // manchas de humedad que chorrean
    for (let i = 0; i < 10; i++) { const x = r() * w; const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, 'rgba(30,20,5,0.5)'); gr.addColorStop(1, 'rgba(30,20,5,0)'); g.fillStyle = gr; g.fillRect(x, 0, 3 + r() * 10, h * (0.3 + r() * 0.7)); }
    speckle(g, w, h, r, 4000, 0.2);
  }, [2, 1]);
  TEX.plaster = canvasTex(256, 256, (g, w, h) => { g.fillStyle = '#5a5650'; g.fillRect(0, 0, w, h); grime(g, w, h, r, 40, '0,0,0', 0.5); speckle(g, w, h, r, 2500, 0.25); for (let i = 0; i < 8; i++) { g.strokeStyle = 'rgba(0,0,0,0.5)'; g.lineWidth = 1; g.beginPath(); let x = r() * w, y = r() * h; g.moveTo(x, y); for (let k = 0; k < 8; k++) { x += r() * 30 - 15; y += r() * 30 - 15; g.lineTo(x, y); } g.stroke(); } }, [2, 4]);
  TEX.door = canvasTex(256, 512, (g, w, h) => {
    g.fillStyle = '#3a2516'; g.fillRect(0, 0, w, h);
    for (let k = 0; k < 120; k++) { g.strokeStyle = `rgba(10,4,0,${0.1 + r() * 0.2})`; g.lineWidth = 1; const y = r() * h; g.beginPath(); g.moveTo(0, y); g.bezierCurveTo(w / 3, y + r() * 6 - 3, 2 * w / 3, y + r() * 6 - 3, w, y + r() * 4 - 2); g.stroke(); }
    const P = [[24, 24, w - 48, h * 0.36], [24, h * 0.44, w - 48, h * 0.5]];
    for (const [x, y, ww, hh] of P) { g.strokeStyle = 'rgba(0,0,0,0.7)'; g.lineWidth = 8; g.strokeRect(x, y, ww, hh); g.strokeStyle = 'rgba(120,80,50,0.25)'; g.lineWidth = 2; g.strokeRect(x + 6, y + 6, ww - 12, hh - 12); }
    grime(g, w, h, r, 30, '0,0,0', 0.5); speckle(g, w, h, r, 2000);
  });
  TEX.doorScratched = canvasTex(256, 512, (g, w, h) => {
    g.drawImage(TEX.door.image, 0, 0);
    for (let s = 0; s < 4; s++) { const x0 = 70 + s * 34; for (let k = 0; k < 4; k++) { g.strokeStyle = `rgba(200,170,140,${0.35 + r() * 0.2})`; g.lineWidth = 2; g.beginPath(); g.moveTo(x0 + k * 8, 180 + r() * 20); g.lineTo(x0 + k * 8 + 16 + r() * 10, 380 + r() * 40); g.stroke(); } }
    g.fillStyle = 'rgba(70,0,0,0.6)'; g.beginPath(); g.ellipse(128, 420, 50, 22, 0.2, 0, Math.PI * 2); g.fill();
  });
  TEX.siding = canvasTex(512, 512, (g, w, h) => {
    for (let y = 0; y < h; y += 32) { const b = 38 + r() * 12; g.fillStyle = `rgb(${b},${b + 2},${b + 6})`; g.fillRect(0, y, w, 32); g.fillStyle = 'rgba(0,0,0,0.6)'; g.fillRect(0, y + 29, w, 3); }
    grime(g, w, h, r, 60, '0,0,0', 0.6); speckle(g, w, h, r, 3000);
  }, [3, 3]);
  TEX.roof = canvasTex(256, 256, (g, w, h) => { for (let y = 0; y < h; y += 16) for (let x = -(y / 16 % 2) * 16; x < w; x += 32) { const b = 18 + r() * 14; g.fillStyle = `rgb(${b},${b},${b + 4})`; g.fillRect(x, y, 30, 14); } }, [6, 4]);
  TEX.ground = canvasTex(512, 512, (g, w, h) => { g.fillStyle = '#141a10'; g.fillRect(0, 0, w, h); grime(g, w, h, r, 80, '40,30,15', 0.5); for (let i = 0; i < 6000; i++) { g.strokeStyle = `rgba(${40 + r() * 40},${50 + r() * 40},${20 + r() * 20},${r() * 0.5})`; g.beginPath(); const x = r() * w, y = r() * h; g.moveTo(x, y); g.lineTo(x + r() * 4 - 2, y - 3 - r() * 8); g.stroke(); } }, [20, 20]);
  TEX.path = canvasTex(256, 256, (g, w, h) => { g.fillStyle = '#2a251e'; g.fillRect(0, 0, w, h); grime(g, w, h, r, 40, '0,0,0', 0.5); speckle(g, w, h, r, 3000, 0.4); }, [1, 6]);
  TEX.portrait = (seed) => canvasTex(256, 320, (g, w, h) => {
    const q = rng(seed); g.fillStyle = '#1a1410'; g.fillRect(0, 0, w, h);
    const gr = g.createRadialGradient(w / 2, h * 0.45, 10, w / 2, h * 0.45, h * 0.6); gr.addColorStop(0, '#5a4a38'); gr.addColorStop(1, '#120d09'); g.fillStyle = gr; g.fillRect(0, 0, w, h);
    g.fillStyle = '#0c0907'; g.beginPath(); g.ellipse(w / 2, h * 0.95, w * 0.42, h * 0.32, 0, 0, Math.PI * 2); g.fill();
    g.fillStyle = '#c8b8a0'; g.beginPath(); g.ellipse(w / 2, h * 0.42, w * 0.2, h * 0.2, 0, 0, Math.PI * 2); g.fill();
    g.fillStyle = '#000'; // ojos tachados / huecos
    g.beginPath(); g.ellipse(w / 2 - 22, h * 0.4, 12, 9, 0, 0, Math.PI * 2); g.fill(); g.beginPath(); g.ellipse(w / 2 + 22, h * 0.4, 12, 9, 0, 0, Math.PI * 2); g.fill();
    if (q() < 0.6) { g.strokeStyle = 'rgba(0,0,0,0.9)'; g.lineWidth = 9; g.beginPath(); g.moveTo(w / 2 - 50, h * 0.36); g.lineTo(w / 2 + 50, h * 0.46); g.stroke(); g.beginPath(); g.moveTo(w / 2 + 50, h * 0.36); g.lineTo(w / 2 - 50, h * 0.46); g.stroke(); }
    g.fillStyle = '#3a0000'; g.fillRect(w / 2 - 14, h * 0.52, 28, 4);
    grime(g, w, h, q, 30, '0,0,0', 0.6); speckle(g, w, h, q, 2000, 0.3);
  });
}

// ---------- materiales ----------
export function mat(map, opts = {}) { return new THREE.MeshStandardMaterial({ map, bumpMap: map, bumpScale: (opts.bump ?? 1.5) * 0.6, roughness: opts.rough ?? 0.85, metalness: 0, color: opts.color ?? 0xffffff, ...opts.extra }); }

// ---------- escena base ----------
export function createWorld() {
  const canvas = document.getElementById('c');
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, preserveDrawingBuffer: true, powerPreference: 'high-performance' });
  renderer.setPixelRatio(1); renderer.setSize(W, H, false);
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = (window.EXPO||1.0);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x020306);
  scene.fog = new THREE.FogExp2(0x05070a, 0.06);
  const camera = new THREE.PerspectiveCamera(62, W / H, 0.05, 200);
  scene.add(camera);

  // linterna pegada a la cámara
  const flash = new THREE.SpotLight(0xfff1d6, 60, 30, 0.48, 0.6, 1.3);
  flash.castShadow = true; flash.shadow.mapSize.set(1024, 1024); flash.shadow.camera.near = 0.1; flash.shadow.bias = -0.0005;
  flash.position.set(0.18, -0.12, 0.05); camera.add(flash);
  const flashTarget = new THREE.Object3D(); flashTarget.position.set(0, -0.1, -3); camera.add(flashTarget); flash.target = flashTarget;
  const fill = new THREE.PointLight(0xffe8c8, 0.6, 3.5, 2); fill.position.set(0, 0, 0.3); camera.add(fill); // rebote suave

  // partículas de polvo alrededor de la cámara
  const N = 900, pos = new Float32Array(N * 3), r = rng(99);
  for (let i = 0; i < N; i++) { pos[i * 3] = (r() - 0.5) * 3; pos[i * 3 + 1] = (r() - 0.5) * 2.4; pos[i * 3 + 2] = -0.4 - r() * 4.5; }
  const dg = new THREE.BufferGeometry(); dg.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  const dust = new THREE.Points(dg, new THREE.PointsMaterial({ size: 0.0045, color: 0xfff0d0, transparent: true, opacity: 0.4, depthWrite: false, blending: THREE.AdditiveBlending }));
  dust.userData.base = pos.slice(); camera.add(dust);

  // post-proceso: grano, viñeta, aberración, parpadeo, tinte
  const composer = new EffectComposer(renderer);
  composer.setPixelRatio(1); composer.setSize(W, H);
  composer.addPass(new RenderPass(scene, camera));
  composer.addPass(new OutputPass());
  const post = new ShaderPass({
    uniforms: { tDiffuse: { value: null }, uTime: { value: 0 }, uGrain: { value: 0.11 }, uVig: { value: 0.75 }, uAb: { value: 0.0022 }, uBright: { value: 1 }, uRed: { value: 0 }, uShake: { value: 0 } },
    vertexShader: `varying vec2 vUv; void main(){ vUv=uv; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0);} `,
    fragmentShader: `uniform sampler2D tDiffuse; uniform float uTime,uGrain,uVig,uAb,uBright,uRed,uShake; varying vec2 vUv;
      float h(vec2 p){ return fract(sin(dot(p,vec2(12.9898,78.233)))*43758.5453); }
      void main(){
        vec2 uv=vUv; uv.x += (h(vec2(floor(uv.y*90.0),uTime))-0.5)*uShake;
        vec2 d=uv-0.5; float ab=uAb*(1.0+dot(d,d)*6.0);
        vec3 c=vec3(texture2D(tDiffuse,uv+d*ab*3.0).r, texture2D(tDiffuse,uv).g, texture2D(tDiffuse,uv-d*ab*3.0).b);
        float l=dot(c,vec3(0.299,0.587,0.114));
        c=mix(c, vec3(l)*vec3(0.92,1.0,0.95), 0.35);              // desaturar hacia verde frío
        c=pow(c, vec3(1.08)); c*=uBright;
        c=mix(c, c*vec3(1.6,0.35,0.3), uRed);
        float v=1.0-dot(d*vec2(1.0,0.62),d*vec2(1.0,0.62))*uVig*2.2; c*=clamp(v,0.0,1.0);
        float g=h(uv*vec2(1080.0,1920.0)+fract(uTime*7.13)*100.0)-0.5; c+=g*uGrain;
        c+= (h(vec2(floor(uv.y*480.0),floor(uTime*24.0)))-0.5)*0.012;  // líneas VHS sutiles
        gl_FragColor=vec4(c,1.0);
      }`
  });
  composer.addPass(post);
  return { renderer, scene, camera, flash, fill, dust, composer, post };
}

// ---------- piezas de construcción ----------
export function box(w, h, d, m, x, y, z, o = {}) {
  const mesh = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), m); mesh.position.set(x, y, z);
  mesh.castShadow = o.cast ?? true; mesh.receiveShadow = true; return mesh;
}
export function setUV(mesh, su, sv) { const uv = mesh.geometry.attributes.uv; for (let i = 0; i < uv.count; i++) uv.setXY(i, uv.getX(i) * su, uv.getY(i) * sv); uv.needsUpdate = true; return mesh; }

// puerta con bisagra: devuelve {group, leaf}; leaf.rotation.y abre
export function door(tex, w = 0.92, h = 2.05) {
  const group = new THREE.Group();
  const frameM = mat(TEX.door, { color: 0x6a5040 });
  group.add(box(0.08, h + 0.08, 0.14, frameM, -w / 2 - 0.04, h / 2, 0));
  group.add(box(0.08, h + 0.08, 0.14, frameM, w / 2 + 0.04, h / 2, 0));
  group.add(box(w + 0.16, 0.08, 0.14, frameM, 0, h + 0.04, 0));
  const hinge = new THREE.Group(); hinge.position.set(-w / 2, 0, 0); group.add(hinge);
  const leaf = box(w, h, 0.05, mat(tex, { bump: 2 }), w / 2, h / 2, 0); hinge.add(leaf);
  const knob = new THREE.Mesh(new THREE.SphereGeometry(0.035, 12, 8), new THREE.MeshStandardMaterial({ color: 0x8a6a30, metalness: 0.9, roughness: 0.35 }));
  knob.position.set(w - 0.1, 1.0, 0.05); knob.castShadow = true; hinge.add(knob);
  const knob2 = knob.clone(); knob2.position.z = -0.05; hinge.add(knob2);
  return { group, hinge };
}

export function deadTree(seed, x, z, s = 1) {
  const r = rng(seed), g = new THREE.Group(), m = new THREE.MeshStandardMaterial({ color: 0x0d0c0b, roughness: 1 });
  function branch(len, rad, depth, parent) {
    const geo = new THREE.CylinderGeometry(rad * 0.6, rad, len, 5); geo.translate(0, len / 2, 0);
    const b = new THREE.Mesh(geo, m); parent.add(b);
    if (depth <= 0) return;
    const n = 2 + Math.floor(r() * 2);
    for (let i = 0; i < n; i++) { const c = new THREE.Group(); c.position.y = len * (0.55 + r() * 0.45); c.rotation.set((r() - 0.5) * 1.6, r() * 6.28, (r() - 0.5) * 1.6); b.add(c); branch(len * (0.55 + r() * 0.2), rad * 0.55, depth - 1, c); }
  }
  branch(2.2 * s, 0.16 * s, 4, g); g.position.set(x, 0, z); return g;
}

// ---------- cámara por keyframes ----------
// keys: [{t, p:[x,y,z], l:[x,y,z]}]  (interpolación Catmull-Rom con tiempo suavizado)
export function cameraAt(keys, t) {
  if (t <= keys[0].t) return { p: new THREE.Vector3(...keys[0].p), l: new THREE.Vector3(...keys[0].l), speed: 0 };
  const last = keys[keys.length - 1];
  if (t >= last.t) return { p: new THREE.Vector3(...last.p), l: new THREE.Vector3(...last.l), speed: 0 };
  let i = 0; while (keys[i + 1].t < t) i++;
  const k0 = keys[Math.max(0, i - 1)], k1 = keys[i], k2 = keys[i + 1], k3 = keys[Math.min(keys.length - 1, i + 2)];
  const u = (t - k1.t) / (k2.t - k1.t), e = k1.ease === 'lin' ? u : smooth(u);
  const cr = (a, b, c, d) => new THREE.Vector3(...[0, 1, 2].map(j => {
    const p0 = a[j], p1 = b[j], p2 = c[j], p3 = d[j];
    return 0.5 * ((2 * p1) + (-p0 + p2) * e + (2 * p0 - 5 * p1 + 4 * p2 - p3) * e * e + (-p0 + 3 * p1 - 3 * p2 + p3) * e * e * e);
  }));
  const p = cr(k0.p, k1.p, k2.p, k3.p), l = cr(k0.l, k1.l, k2.l, k3.l);
  const dist = Math.hypot(k2.p[0] - k1.p[0], k2.p[2] - k1.p[2]) / (k2.t - k1.t);
  return { p, l, speed: dist * Math.sin(Math.PI * u) * 1.5 };
}
