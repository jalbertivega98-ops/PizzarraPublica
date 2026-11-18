// Shared poses for COSAS DE PAREJA (Dani right, Lucía left: Dani looks at her with yaw<0, she looks at him with yaw>0)
import { pose } from './pareja_kit'

export const D = {
  idle: pose({ smile: 0.15, lids: 0.15 }),
  bored: pose({ lids: 0.4, smile: -0.1 }),
  wait: pose({ lids: 0.3, pitch: 0.05, brows: 0.2, browTilt: -0.3, smile: -0.2, lSh: [0.55, 0.2], lEl: -1.3 }),
  ask: pose({ yaw: -0.45, brows: 0.4, lids: 0.05 }),
  hopeful: pose({ yaw: -0.45, brows: 0.6, smile: 0.6, lids: 0, lSh: [0.7, 0.3], lEl: -1.1 }),
  trying: pose({ yaw: -0.45, brows: 0.45, browTilt: -0.3, smile: 0.25, lSh: [0.85, 0.35], lEl: -1.0 }),
  nod: pose({ yaw: -0.4, pitch: 0.15, smile: 0.5, brows: 0.3 }),
  tired: pose({ yaw: -0.3, lids: 0.5, brows: 0.25, browTilt: -0.5, smile: -0.2 }),
  slump: pose({ sink: 0.1, pitch: 0.22, lids: 0.6, brows: 0.3, browTilt: -0.7, roll: -0.08, smile: -0.4 }),
  stunned: pose({ yaw: -0.5, lids: 0, brows: 1, browTilt: -0.2, mouth: 0.3 }),
  stare: pose({ yaw: 0, lids: 0, brows: 0.2, smile: -0.3 }),
  camera: pose({ yaw: 0, lids: 0.1, brows: 0.6, browTilt: -0.4, smile: -0.25 }), // looks at the viewer
  think: pose({ yaw: 0.25, pitch: -0.15, brows: 0.5, browTilt: -0.6, lSh: [1.25, 0.25], lEl: -1.75 }),
  panic: pose({ yaw: -0.5, brows: 1, browTilt: -1, lids: 0, mouth: 0.3, lean: -0.04 }),
  sorry: pose({ lids: 0.35, yaw: -0.4, pitch: 0.15, brows: 0.6, browTilt: -1, lSh: [0.9, -0.12], lEl: -1.2, rSh: [0.9, 0.12], rEl: -1.2 }),
  defeated: pose({ pitch: 0.25, lids: 0.6, brows: 0.4, browTilt: -0.8, sink: 0.07, smile: -0.4, roll: -0.06 }),
  hot: pose({ yaw: 0.1, pitch: -0.1, lids: 0.45, brows: 0.3, browTilt: -0.6, smile: -0.3, mouth: 0.25, rSh: [1.45, -0.25], rEl: -1.6 }),
  sneaky: pose({ yaw: 0.35, lids: 0.35, brows: -0.2, browTilt: 0.6, smile: 0.3, lean: 0.05 }),
  point: pose({ yaw: -0.45, brows: 0.3, smile: 0.2, lSh: [1.25, 0.15], lEl: -0.3 }),
  photo: pose({ yaw: -0.5, pitch: 0.05, brows: 0.3, lids: 0.15, rSh: [1.35, 0.35], rEl: -0.9 }),
  photoLow: pose({ yaw: -0.5, pitch: -0.15, sink: 0.12, brows: 0.6, browTilt: -0.4, rSh: [1.1, 0.4], rEl: -0.6, lean: 0.1 }),
  pain: pose({ yaw: -0.2, roll: 0.15, lids: 0.6, brows: 0.6, browTilt: -1, smile: -0.6, mouth: 0.2, lSh: [0.6, 0.6], lEl: -1.8 }),
  chew: pose({ yaw: 0.1, pitch: 0.1, lids: 0.2, smile: 0.5, rSh: [1.3, -0.1], rEl: -1.7 }),
  guilty: pose({ yaw: -0.25, pitch: 0.15, lids: 0.3, brows: 0.6, browTilt: -0.9, smile: -0.35, rSh: [1.2, -0.1], rEl: -1.6 }),
  faint: pose({ roll: -0.3, pitch: -0.25, lids: 1, brows: 0.5, mouth: 0.4, sink: 0.08, lean: -0.08 }),
  breathe: pose({ pitch: -0.1, lids: 0.8, brows: 0.3, lean: -0.05 }),
}

export const Lx = {
  idle: pose({ smile: 0.15 }),
  sweet: pose({ yaw: 0.5, brows: 0.6, browTilt: -0.3, smile: 0.9, lids: 0, roll: 0.12, lean: 0.05 }),
  happy: pose({ yaw: 0.15, smile: 0.85, brows: 0.35 }),
  excited: pose({ yaw: 0.5, brows: 0.9, smile: 1, lids: 0, rSh: [1.6, -0.3], rEl: -0.5, lean: 0.06 }),
  disgust: pose({ yaw: 0.45, smile: -0.7, brows: -0.15, browTilt: 0.4, lids: 0.35, roll: -0.12 }),
  meh: pose({ yaw: 0.3, smile: -0.35, lids: 0.45, brows: 0.1, roll: 0.08 }),
  annoyed: pose({ yaw: 0.55, browTilt: 1, brows: -0.3, lean: 0.08, smile: -0.3 }),
  stare: pose({ yaw: 0.55, brows: -0.3, browTilt: 1, lids: 0.2, lean: 0.06 }),
  pose1: pose({ yaw: -0.15, roll: 0.15, smile: 0.7, brows: 0.4, rSh: [1.5, -0.4], rEl: -1.9, lSh: [0.4, 0.5], lEl: -1.4 }), // posing for photo
  pose2: pose({ yaw: 0.2, roll: -0.12, pitch: -0.1, smile: 0.95, lids: 0.15, lSh: [1.0, 0.1], lEl: -2.0 }),
  mirror: pose({ yaw: -0.4, pitch: 0.05, brows: 0.2, browTilt: 0.3, lids: 0.15, smile: -0.1, lSh: [0.3, 0.4], lEl: -1.5 }), // checks herself
  doubt: pose({ yaw: 0.3, brows: 0.4, browTilt: -0.5, smile: -0.2, lSh: [1.0, 0.3], lEl: -1.8 }),
  rush: pose({ yaw: 0.45, brows: 0.8, smile: 0.4, lean: 0.06, rSh: [1.3, -0.4], rEl: -0.6 }),
  shiver: pose({ yaw: 0.35, pitch: 0.1, brows: 0.7, browTilt: -0.8, smile: -0.4, sink: 0.04, lSh: [0.9, -0.2], lEl: -1.7, rSh: [0.9, 0.2], rEl: -1.7 }),
  whistle: pose({ yaw: -0.35, pitch: -0.3, lids: 0.1, brows: 0.5, mouth: 0.12, smile: -0.1 }),
  sleep: pose({ roll: -0.3, pitch: 0.15, lids: 1, smile: 0.15, sink: 0.04, side: 0.1, lean: -0.03 }),
  phone: pose({ rSh: [1.5, -0.2], rEl: -1.1, pitch: 0.28, yaw: 0.05, brows: 0.1 }),
  sad: pose({ yaw: 0.45, pitch: 0.12, brows: 0.8, browTilt: -0.9, smile: -0.5, lids: 0.2 }),
  stareFood: pose({ yaw: 0.55, pitch: 0.12, lids: 0.1, brows: 0.2, browTilt: 0.3, smile: -0.25, lean: 0.07 }),
  smug: pose({ yaw: 0.45, lids: 0.35, smile: 0.7, brows: 0.25, roll: 0.1 }),
  cross: pose({ yaw: 0.5, brows: -0.3, browTilt: 1, smile: -0.4, lSh: [0.9, -0.35], lEl: -1.6, rSh: [0.9, 0.35], rEl: -1.6 }),
}
