// LA CASA · Episodio 0 — llegada, entrada y las tres puertas
import * as THREE from 'three';
import { W, H, rng, clamp, smooth, lerp, win, noise1, TEX, makeTextures, mat, createWorld, box, setUV, door, deadTree, cameraAt } from './engine.js';

makeTextures();
const { renderer, scene, camera, flash, fill, dust, composer, post } = createWorld();

export const SCENE_END = 22.8;
// cámara lenta entre 11 y 12.9 s de escena para que quepa la narración
const warp = (tv) => tv < 11 ? tv : tv < 14.1 ? 11 + (tv - 11) * (1.9 / 3.1) : tv - 1.2;
const unwarp = (ts) => ts < 11 ? ts : ts < 12.9 ? 11 + (ts - 11) * (3.1 / 1.9) : ts + 1.2;
export const DUR = unwarp(SCENE_END);
// eventos de sonido (los lee sonido.py a través de timeline.json)
const SCENE_EVENTS = [
  { t: 0.0, s: 'viento', d: 8.5 }, { t: 0.0, s: 'drone', d: 24 },
  { t: 0.42, s: 'trueno', v: 1.0 }, { t: 2.62, s: 'trueno', v: 0.55 },
  { t: 3.4, s: 'golpe_titulo' },
  ...[...Array(9)].map((_, i) => ({ t: 0.4 + i * 0.62, s: 'paso_tierra', v: 0.6 })),
  ...[...Array(3)].map((_, i) => ({ t: 6.05 + i * 0.5, s: 'paso_madera', v: 0.7 })),
  { t: 5.6, s: 'chirrido', d: 1.5 }, { t: 7.2, s: 'paso_madera' }, { t: 7.75, s: 'paso_madera' },
  { t: 8.4, s: 'portazo' },
  { t: 9.0, s: 'paso_madera' }, { t: 9.6, s: 'paso_madera' },
  { t: 9.9, s: 'pelota', d: 1.4 },
  { t: 11.3, s: 'paso_madera' }, { t: 11.45, s: 'toc', v: 0.9 }, { t: 11.62, s: 'toc', v: 0.9 }, { t: 11.79, s: 'toc', v: 0.9 },
  { t: 12.6, s: 'paso_madera' }, { t: 12.95, s: 'zumbido_linterna', d: 0.75 },
  { t: 13.18, s: 'susto' }, { t: 13.2, s: 'latido', d: 8.5 },
  { t: 14.8, s: 'chirrido', d: 1.4, v: 0.6 },
  { t: 15.7, s: 'bombilla', d: 7 }, { t: 16.2, s: 'pop' }, { t: 16.5, s: 'pop' }, { t: 16.8, s: 'pop' }, { t: 18.4, s: 'golpe_titulo', v: 0.7 },
];
const VOZ = [['l1', 0.4], ['l2', 4.1], ['l4', 15.0], ['l5', 19.65]];  // narrador Adam (voz/ep00_adam)
export const EVENTS = [...SCENE_EVENTS.map(e => ({ ...e, t: +unwarp(e.t).toFixed(3) })), ...VOZ.map(([f, t]) => ({ t, s: 'voz', f }))];

// ---------------- CIELO ----------------
const skyTex = (() => {
  const c = document.createElement('canvas'); c.width = 512; c.height = 1024; const g = c.getContext('2d');
  const gr = g.createLinearGradient(0, 0, 0, 1024); gr.addColorStop(0, '#02030a'); gr.addColorStop(0.5, '#0b1322'); gr.addColorStop(0.62, '#141b26'); gr.addColorStop(1, '#05070a');
  g.fillStyle = gr; g.fillRect(0, 0, 512, 1024);
  const r = rng(3); for (let i = 0; i < 40; i++) { const x = r() * 512, y = 150 + r() * 450, rad = 40 + r() * 140; const q = g.createRadialGradient(x, y, 0, x, y, rad); q.addColorStop(0, `rgba(60,70,90,${0.2 + r() * 0.25})`); q.addColorStop(1, 'rgba(60,70,90,0)'); g.fillStyle = q; g.fillRect(0, 0, 512, 1024); }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
})();
const skyMat = new THREE.MeshBasicMaterial({ map: skyTex, side: THREE.BackSide, fog: false, color: 0xffffff });
const sky = new THREE.Mesh(new THREE.SphereGeometry(90, 32, 16), skyMat); scene.add(sky);
const moon = new THREE.Mesh(new THREE.CircleGeometry(2.4, 32), new THREE.MeshBasicMaterial({ color: 0xd8dccf, fog: false }));
moon.position.set(-4, 30, -45); scene.add(moon);
const halo = new THREE.Mesh(new THREE.CircleGeometry(9, 32), new THREE.MeshBasicMaterial({ color: 0x8090a0, transparent: true, opacity: 0.12, fog: false, depthWrite: false }));
halo.position.set(-4, 30, -45.1); scene.add(halo);

// ---------------- LUCES EXTERIORES ----------------
const moonL = new THREE.DirectionalLight(0x7f95c0, 0.35); moonL.position.set(-10, 20, 12); scene.add(moonL);
const hemi = new THREE.HemisphereLight(0x223040, 0x050505, 0.25); scene.add(hemi);
const bolt = new THREE.DirectionalLight(0xc8d8ff, 0); bolt.position.set(6, 30, 20); scene.add(bolt);

// ---------------- TERRENO ----------------
const ground = new THREE.Mesh(new THREE.PlaneGeometry(200, 200), mat(TEX.ground, { bump: 3 })); ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; scene.add(ground);
const path = new THREE.Mesh(new THREE.PlaneGeometry(1.6, 22), mat(TEX.path, { bump: 4 })); path.rotation.x = -Math.PI / 2; path.position.set(0, 0.01, 12.5); path.receiveShadow = true; scene.add(path);
[[-4.5, 9, 1.4, 11], [5.2, 6, 1.2, 12], [-7.5, 3, 1.7, 13], [8, 12, 1.5, 14], [-3.6, 16, 1.0, 15], [3.4, 15, 1.1, 18]].forEach(([x, z, s, sd]) => scene.add(deadTree(sd, x, z, s)));
const fenceM = new THREE.MeshStandardMaterial({ color: 0x1a1612, roughness: 1 });
for (let i = 0; i < 9; i++) { const r = rng(40 + i); for (const sx of [-1, 1]) { if (r() < 0.25) continue; const p = box(0.08, 0.9 + r() * 0.3, 0.08, fenceM, sx * 1.5, 0.45, 18 - i * 2); p.rotation.z = (r() - 0.5) * 0.35; scene.add(p); } }

// ---------------- CASA (exterior) ----------------
const house = new THREE.Group(); scene.add(house);
const sid = mat(TEX.siding, { bump: 2 });
const HW = 6, HD = 12, HH = 6.2;
house.add(setUV(box(HW - 0.55, HH, 0.2, sid, -(HW + 0.55) / 2, HH / 2, 0), 1, 1));
house.add(setUV(box(HW - 0.55, HH, 0.2, sid, (HW + 0.55) / 2, HH / 2, 0), 1, 1));
house.add(box(1.1, HH - 2.35, 0.2, sid, 0, 2.35 + (HH - 2.35) / 2, 0));
house.add(box(0.2, HH, HD, sid, -HW, HH / 2, -HD / 2)); house.add(box(0.2, HH, HD, sid, HW, HH / 2, -HD / 2)); house.add(box(HW * 2, HH, 0.2, sid, 0, HH / 2, -HD));
// tejado a dos aguas
const roofM = mat(TEX.roof, { bump: 3 });
const rl = Math.hypot(HW + 0.6, 3.4);
const ang = Math.atan2(3.4, HW + 0.6);
for (const s of [-1, 1]) { const r = box(rl, 0.18, HD + 1.2, roofM, s * (HW + 0.6) / 2, HH + 1.7, -HD / 2); r.rotation.z = -s * ang; house.add(r); }
const gable = new THREE.Shape(); gable.moveTo(-HW, 0); gable.lineTo(HW, 0); gable.lineTo(0, 3.4); gable.closePath();
const gm = new THREE.Mesh(new THREE.ExtrudeGeometry(gable, { depth: 0.2, bevelEnabled: false }), sid); gm.position.set(0, HH, -0.1); gm.castShadow = true; house.add(gm);
// chimenea
house.add(box(0.9, 3, 0.9, mat(TEX.plaster, { color: 0x553a30 }), 3.4, HH + 2.6, -7));
// ventanas
const glassDark = new THREE.MeshStandardMaterial({ color: 0x05070a, roughness: 0.15, metalness: 0.6 });
const frameW = new THREE.MeshStandardMaterial({ color: 0x2a2620, roughness: 0.9 });
const lit = new THREE.MeshBasicMaterial({ color: 0x000000 });
function windowAt(x, y, w = 1.2, h = 1.5, m = glassDark) {
  const g = new THREE.Group(); g.position.set(x, y, 0.12);
  const pane = new THREE.Mesh(new THREE.PlaneGeometry(w, h), m); g.add(pane);
  g.add(box(w + 0.16, 0.1, 0.1, frameW, 0, h / 2 + 0.05, 0)); g.add(box(w + 0.16, 0.12, 0.18, frameW, 0, -h / 2 - 0.05, 0.03));
  g.add(box(0.08, h, 0.08, frameW, -w / 2 - 0.04, 0, 0)); g.add(box(0.08, h, 0.08, frameW, w / 2 + 0.04, 0, 0));
  g.add(box(0.05, h, 0.05, frameW, 0, 0, 0.02)); g.add(box(w, 0.05, 0.05, frameW, 0, 0.15, 0.02));
  house.add(g); return g;
}
windowAt(-3.2, 1.9); windowAt(3.2, 1.9); windowAt(-3.2, 4.5); windowAt(3.2, 4.5);
const upWin = windowAt(0, 4.4, 1.0, 1.3, lit);
// silueta en la ventana de arriba
const silMat = new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: 0 });
const silh = new THREE.Group(); silh.position.set(0, 4.25, 0.135); house.add(silh);
const sh1 = new THREE.Mesh(new THREE.CircleGeometry(0.15, 20), silMat); sh1.position.y = 0.22; silh.add(sh1);
const sh2 = new THREE.Mesh(new THREE.PlaneGeometry(0.42, 0.6), silMat); sh2.position.y = -0.25; silh.add(sh2);
const winGlow = new THREE.PointLight(0xffa040, 0, 6, 2); winGlow.position.set(0, 4.4, 0.8); scene.add(winGlow);
// porche
const porchM = mat(TEX.wood, { color: 0x8a7a6a });
house.add(setUV(box(4.2, 0.25, 1.9, porchM, 0, 0.125, 0.95), 1, 0.4));
house.add(setUV(box(1.6, 0.12, 0.4, porchM, 0, 0.06, 2.1), 1, 0.2));
for (const s of [-1, 1]) house.add(box(0.14, 2.6, 0.14, frameW, s * 1.95, 1.55, 1.78));
const proof = box(4.6, 0.12, 2.2, roofM, 0, 2.9, 0.95); proof.rotation.x = 0.15; house.add(proof);
// farol del porche roto
house.add(box(0.12, 0.25, 0.12, new THREE.MeshStandardMaterial({ color: 0x111111, metalness: 0.7, roughness: 0.4 }), 0.85, 2.3, 0.14));

// ---------------- INTERIOR ----------------
const inn = new THREE.Group(); inn.position.y = 0.25; scene.add(inn);
const wallM = mat(TEX.wallpaper, { bump: 1.2 });
const floorM = mat(TEX.wood, { bump: 2, rough: 0.6 });
const ceilM = mat(TEX.plaster, { bump: 2 });
const HL = 10.5, HWid = 1.1, CH = 2.7;
inn.add(setUV(box(HWid * 2, 0.05, HL, floorM, 0, -0.025, -HL / 2, { cast: false }), 1, 1));
inn.add(box(HWid * 2, 0.05, HL, ceilM, 0, CH + 0.025, -HL / 2, { cast: false }));
function wallSeg(x, z0, z1) { const len = z0 - z1; const w = box(0.08, CH, len, wallM, x, CH / 2, (z0 + z1) / 2); setUV(w, len / 2.2, 1); inn.add(w);
  inn.add(box(0.05, 0.16, len, mat(TEX.door, { color: 0x553a2a }), x - Math.sign(x) * 0.05, 0.08, (z0 + z1) / 2)); }
wallSeg(-HWid, 0, -3.5); wallSeg(-HWid, -4.5, -HL); wallSeg(HWid, 0, -6.0); wallSeg(HWid, -7.0, -HL);
inn.add(box(0.08, CH - 2.13, 1.0, wallM, -HWid, 2.13 + (CH - 2.13) / 2, -4));
inn.add(box(0.08, CH - 2.13, 1.0, wallM, HWid, 2.13 + (CH - 2.13) / 2, -6.5));
inn.add(box(HWid * 2, CH - 2.13, 0.08, wallM, 0, 2.13 + (CH - 2.13) / 2, -HL));
for (const s of [-1, 1]) inn.add(box((HWid * 2 - 0.96) / 2, 2.13, 0.08, wallM, s * (0.48 + (HWid * 2 - 0.96) / 4), 1.065, -HL));
// cuartos oscuros detrás de las puertas
const voidM = new THREE.MeshStandardMaterial({ color: 0x0a0a0a, roughness: 1, side: THREE.BackSide });
const room1 = new THREE.Mesh(new THREE.BoxGeometry(3, CH, 3), voidM); room1.position.set(-HWid - 1.5, CH / 2, -4); inn.add(room1);
const room2 = new THREE.Mesh(new THREE.BoxGeometry(3, CH, 3), voidM); room2.position.set(HWid + 1.5, CH / 2, -6.5); inn.add(room2);
const room3 = new THREE.Mesh(new THREE.BoxGeometry(3, CH, 3), voidM); room3.position.set(0, CH / 2, -HL - 1.5); inn.add(room3);
// puertas
const D0 = door(TEX.door); D0.group.position.set(0, 0, 0); inn.add(D0.group);           // entrada
const D1 = door(TEX.door); D1.group.position.set(-HWid, 0, -4); D1.group.rotation.y = Math.PI / 2; inn.add(D1.group);
const D2 = door(TEX.door); D2.group.position.set(HWid, 0, -6.5); D2.group.rotation.y = -Math.PI / 2; inn.add(D2.group);
const D3 = door(TEX.doorScratched); D3.group.position.set(0, 0, -HL); inn.add(D3.group);
D1.hinge.rotation.y = 0.42;
// luz roja bajo la puerta 2
const redStrip = new THREE.Mesh(new THREE.PlaneGeometry(0.9, 0.05), new THREE.MeshBasicMaterial({ color: 0xff2000 }));
redStrip.rotation.y = -Math.PI / 2; redStrip.position.set(HWid - 0.05, 0.02, -6.5); inn.add(redStrip);
const redL = new THREE.PointLight(0xff1a00, 1.5, 2.2, 2); redL.position.set(HWid - 0.2, 0.06, -6.5); inn.add(redL);
// marcos con retratos
function frameAt(x, z, y, seed, tilt) {
  const g = new THREE.Group(); g.position.set(x - Math.sign(x) * 0.06, y, z); g.rotation.y = -Math.sign(x) * Math.PI / 2; g.rotation.z = tilt;
  g.add(box(0.62, 0.76, 0.05, new THREE.MeshStandardMaterial({ color: 0x3a2a10, metalness: 0.5, roughness: 0.5 }), 0, 0, 0));
  const pic = new THREE.Mesh(new THREE.PlaneGeometry(0.5, 0.64), new THREE.MeshStandardMaterial({ map: TEX.portrait(seed), roughness: 0.6 })); pic.position.z = 0.03; g.add(pic);
  inn.add(g);
}
frameAt(-HWid, -2.0, 1.65, 11, 0.06); frameAt(-HWid, -7.4, 1.7, 12, -0.12); frameAt(HWid, -3.1, 1.7, 13, -0.04); frameAt(HWid, -8.6, 1.6, 14, 0.18);
// mesita con vela
const tM = mat(TEX.door, { color: 0x7a5a40 });
inn.add(box(0.4, 0.05, 0.9, tM, HWid - 0.25, 0.85, -2.6));
for (const [dx, dz] of [[-0.15, -0.4], [0.15, -0.4], [-0.15, 0.4], [0.15, 0.4]]) inn.add(box(0.04, 0.85, 0.04, tM, HWid - 0.25 + dx, 0.425, -2.6 + dz));
const candle = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.22, 10), new THREE.MeshStandardMaterial({ color: 0xd8d0b8 })); candle.position.set(HWid - 0.25, 0.985, -2.45); inn.add(candle);
// alfombra
const rug = new THREE.Mesh(new THREE.PlaneGeometry(1.0, 8.5), mat(TEX.plaster, { color: 0x6a1010, bump: 3 })); rug.rotation.x = -Math.PI / 2; rug.position.set(0, 0.006, -5.6); rug.receiveShadow = true; inn.add(rug);
// bombilla colgando
const bulbG = new THREE.Group(); bulbG.position.set(0, CH, -5.6); inn.add(bulbG);
const wire = new THREE.Mesh(new THREE.CylinderGeometry(0.006, 0.006, 0.6, 4), new THREE.MeshStandardMaterial({ color: 0x111111 })); wire.position.y = -0.3; bulbG.add(wire);
const bulb = new THREE.Mesh(new THREE.SphereGeometry(0.06, 12, 10), new THREE.MeshStandardMaterial({ color: 0x888877, roughness: 0.2, transparent: true, opacity: 0.8 })); bulb.position.y = -0.64; bulb.castShadow = true; bulbG.add(bulb);
const bulbL = new THREE.PointLight(0xffb060, 0, 7, 1.6); bulbL.position.y = -0.7; bulbL.castShadow = true; bulbL.shadow.mapSize.set(512, 512); bulbG.add(bulbL);
// pelota
const ball = new THREE.Mesh(new THREE.SphereGeometry(0.11, 20, 14), new THREE.MeshStandardMaterial({ color: 0x6a0c0c, roughness: 0.85 })); ball.castShadow = true; inn.add(ball);
// la figura
const figM = new THREE.MeshBasicMaterial({ color: 0x000000 });
const fig = new THREE.Group(); inn.add(fig);
const body = new THREE.Mesh(new THREE.CapsuleGeometry(0.17, 1.35, 4, 10), figM); body.position.y = 1.05; body.scale.z = 0.6; fig.add(body);
const head = new THREE.Mesh(new THREE.SphereGeometry(0.14, 12, 10), figM); head.position.set(0, 2.0, 0); head.scale.y = 1.25; fig.add(head);
for (const s of [-1, 1]) { const a = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.03, 1.15, 6), figM); a.position.set(s * 0.22, 1.15, 0); a.rotation.z = s * 0.05; fig.add(a); }
const eyeM = new THREE.MeshBasicMaterial({ color: 0xffffff });
for (const s of [-1, 1]) { const e = new THREE.Mesh(new THREE.SphereGeometry(0.014, 8, 6), eyeM); e.position.set(s * 0.05, 2.02, 0.12); fig.add(e); }
fig.visible = false;

// ---------------- CÁMARA ----------------
const KEYS = [
  { t: 0, p: [0.3, 1.65, 16.5], l: [0, 3.8, 0] },
  { t: 3.4, p: [0.1, 1.65, 8.8], l: [0, 3.2, 0] },
  { t: 5.5, p: [0, 1.9, 1.55], l: [0, 1.6, 0] },
  { t: 7.0, p: [0, 1.9, 1.05], l: [0, 1.6, -4] },
  { t: 8.8, p: [0, 1.9, -1.3], l: [0, 1.55, -6] },
  { t: 10.5, p: [0.15, 1.9, -2.3], l: [-1.2, 0.55, -3.8] },
  { t: 12.1, p: [0.05, 1.9, -3.2], l: [1.2, 0.7, -6.5] },
  { t: 13.4, p: [0, 1.9, -4.0], l: [0, 1.55, -10.5] },
  { t: 15.0, p: [0, 1.9, -4.2], l: [0, 1.5, -10.5] },
  { t: 16.3, p: [-0.05, 2.05, -0.55], l: [0, 1.25, -8.0] },
  { t: 22.8, p: [-0.05, 2.05, -0.8], l: [0, 1.25, -8.0] },
];

// ---------------- OVERLAY ----------------
const $ = (id) => document.getElementById(id);
const TEXTS = [  // tiempo de vídeo (sincronizado con la voz)
  { a: 0.4, b: 4.0, s: 'Esta casa… <br>lleva diez años abandonada.' },
  { a: 4.1, b: 8.2, s: 'Desde que murió su dueña. <br>Tenía 78 años.' },
  { a: 15.0, b: 19.3, s: 'A partir de aquí… no voy solo. <br>Vosotros me vais a guiar.' },
];
function typed(s, k) { const plain = s.replace(/<br>/g, '\n'); const n = Math.floor(plain.length * clamp(k)); return plain.slice(0, n).replace(/\n/g, '<br>'); }
function overlay(t, tv) {
  let cur = null; for (const x of TEXTS) if (tv >= x.a && tv < x.b) cur = x;
  const el = $('t1');
  if (cur) { el.innerHTML = typed(cur.s, (tv - cur.a) / Math.min(1.0, (cur.b - cur.a) * 0.5)); el.style.opacity = Math.min(1, (cur.b - tv) / 0.25); } else el.style.opacity = 0;
  const ti = $('title'), k = win(t, 3.4, 3.7) * (1 - win(t, 5.3, 5.7));
  ti.style.opacity = k; ti.style.transform = `scale(${1.15 - 0.15 * smooth(win(t, 3.4, 5.6))})`;
  ti.style.filter = `blur(${(1 - win(t, 3.4, 3.6)) * 8}px)`;
  $('ep').style.opacity = win(t, 7.2, 7.6) * 0.85;
  $('rec').style.opacity = t > 7.2 && Math.floor(t * 1.6) % 2 === 0 ? 0.9 : 0;
  // etiquetas de las puertas proyectadas a pantalla
  const pts = [[-HWid + 0.05, 1.35, -4], [HWid - 0.05, 1.35, -6.5], [0, 1.3, -HL + 0.05]];
  pts.forEach((p, i) => {
    const v = new THREE.Vector3(p[0], p[1] + 0.25, p[2]).project(camera);
    const el = $('l' + (i + 1)), a = 16.2 + i * 0.3, kk = win(t, a, a + 0.25);
    const pop = kk < 1 ? 0.6 + 0.55 * Math.sin(kk * Math.PI * 0.75) : 1 + 0.04 * Math.sin((t - a) * 5);
    el.style.left = ((v.x + 1) / 2 * W) + 'px'; el.style.top = ((1 - v.y) / 2 * H) + 'px';
    el.style.opacity = kk; el.style.transform = `translate(-50%,-50%) scale(${pop})`;
  });
  const c = $('cta'), kc = win(t, 18.4, 18.7); c.style.opacity = kc; c.style.transform = `translateY(${(1 - smooth(kc)) * 60}px)`;
}

// ---------------- FOTOGRAMA ----------------
function flashFlicker(t) {
  const off = [[12.95, 13.02], [13.08, 13.12], [13.3, 13.44], [13.6, 13.66]];
  for (const [a, b] of off) if (t >= a && t < b) return 0.04;
  if (t > 12.9 && t < 13.8) return 0.6 + 0.4 * noise1(t * 40);
  return 0.93 + 0.07 * noise1(t * 6);
}
function lightning(t) {
  const strikes = [[0.42, 1.0], [0.58, 0.6], [2.62, 0.5], [2.72, 0.35]];
  let v = 0; for (const [a, s] of strikes) { const d = t - a; if (d >= 0 && d < 0.35) v = Math.max(v, s * Math.exp(-d * 14)); } return v;
}
window.DUR = DUR; window.EVENTS = EVENTS;
window.renderAt = (tv) => {
  const t = warp(tv);
  const inside = smooth(win(t, 6.6, 8.0));
  // cámara + temblor de mano + balanceo al andar
  const c = cameraAt(KEYS, t);
  const bob = Math.sin(t * 9.5) * 0.022 * Math.min(1, c.speed);
  const sx = (noise1(t * 0.9 + 3) - 0.5) * 0.04, sy = (noise1(t * 1.1 + 9) - 0.5) * 0.03;
  let shake = 0; if (t > 8.4 && t < 8.9) shake = (1 - win(t, 8.4, 8.9)) * 0.06; if (t > 13.18 && t < 13.7) shake = Math.max(shake, (1 - win(t, 13.18, 13.7)) * 0.05);
  const jx = (noise1(t * 60) - 0.5) * shake, jy = (noise1(t * 55 + 4) - 0.5) * shake;
  camera.position.set(c.p.x + sx * 0.3 + jx, c.p.y + bob + sy * 0.3 + jy, c.p.z);
  camera.lookAt(c.l.x + sx * 2, c.l.y + sy * 2 + bob * 0.5, c.l.z);
  camera.fov = lerp(62, 72, smooth(win(t, 15.0, 16.3))); camera.updateProjectionMatrix();

  // linterna
  flash.intensity = 55 * flashFlicker(t) * lerp(0.75, 1, inside);
  fill.intensity = 0.5 * flashFlicker(t);
  // exterior: luna + rayos
  const L = lightning(t);
  moonL.intensity = lerp(1.1, 0, inside); hemi.intensity = lerp(0.4, 0.03, inside);
  bolt.intensity = L * 9 * (1 - inside);
  skyMat.color.setScalar(1 + L * 5);
  scene.fog.color.setRGB(lerp(0.02, 0.01, inside) + L * 0.15, lerp(0.028, 0.01, inside) + L * 0.17, lerp(0.04, 0.012, inside) + L * 0.22);
  scene.fog.density = lerp(0.04, 0.065, inside);
  // ventana de arriba: luz tenue + silueta con el 2º rayo
  const wl = (t < 6 ? 0.5 + 0.5 * noise1(t * 3) : 0) * (t > 1.2 ? 1 : 0);
  lit.color.setRGB(0.5 * wl, 0.25 * wl, 0.08 * wl); winGlow.intensity = 2.5 * wl;
  silMat.opacity = (t > 2.6 && t < 3.0) ? 1 : 0;
  // puertas
  D0.hinge.rotation.y = t < 8.35 ? 1.5 * smooth(win(t, 5.6, 7.1)) : lerp(1.45, 0, win(t, 8.25, 8.42));
  D3.hinge.rotation.y = 0.22 * smooth(win(t, 14.8, 16.2));
  // luz roja que parpadea
  const rk = 0.6 + 0.4 * noise1(t * 7) * (noise1(t * 2.3) > 0.4 ? 1 : 0.2);
  redL.intensity = 1.6 * rk * inside; redStrip.material.color.setRGB(rk, 0.08 * rk, 0);
  // bombilla balanceándose
  bulbG.rotation.z = Math.sin(t * 1.7) * 0.18 + (t > 8.4 ? Math.sin((t - 8.4) * 3.1) * 0.25 * Math.exp(-(t - 8.4) * 0.4) : 0);
  bulbG.rotation.x = Math.sin(t * 1.3) * 0.08;
  const bon = t > 15.7 ? (noise1(t * 11) > 0.35 || t > 16.6 ? 1 : 0.1) * (0.75 + 0.25 * noise1(t * 23)) : 0;
  bulbL.intensity = 3.2 * bon; bulb.material.emissive = bulb.material.emissive || new THREE.Color(); bulb.material.emissive.setRGB(1 * bon, 0.6 * bon, 0.25 * bon);
  // pelota que sale rodando de la puerta 1
  const bk = 1 - Math.pow(1 - win(t, 9.9, 11.4), 2.4);
  ball.position.set(lerp(-1.9, -0.35, bk), 0.11, lerp(-4.15, -3.35, bk));
  ball.rotation.z = -bk * 9; ball.rotation.x = -bk * 4; ball.visible = t > 9.5;
  // figura cruzando al fondo
  fig.visible = t > 13.05 && t < 13.55;
  fig.position.set(lerp(1.0, -1.2, win(t, 13.05, 13.55)), 0, -9.6);
  // polvo
  const P = dust.geometry.attributes.position, B = dust.userData.base;
  for (let i = 0; i < P.count; i++) { P.setXYZ(i, B[i * 3] + Math.sin(t * 0.3 + i) * 0.15, B[i * 3 + 1] + Math.sin(t * 0.2 + i * 1.7) * 0.12 - ((t * 0.03 + i * 0.01) % 0.3), B[i * 3 + 2]); }
  P.needsUpdate = true; dust.material.opacity = 0.25 + 0.4 * inside;
  // post
  post.uniforms.uTime.value = t;
  const fadeIn = smooth(win(t, 0, 0.6)), fadeOut = 1 - win(t, SCENE_END - 0.4, SCENE_END) * 0.7;
  post.uniforms.uBright.value = fadeIn * fadeOut * (1 + L * 0.6);
  post.uniforms.uRed.value = (t > 13.15 && t < 13.75 ? (1 - win(t, 13.15, 13.75)) * 0.8 : 0) + (t > 18.4 ? 0.12 : 0);
  post.uniforms.uShake.value = (t > 13.15 && t < 13.5 ? 0.02 : 0) + shake * 0.15;
  post.uniforms.uAb.value = 0.0022 + (t > 13.15 && t < 13.6 ? 0.006 : 0);
  composer.render();
  overlay(t, tv);
  return true;
};
window.ready = true;
