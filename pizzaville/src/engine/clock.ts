// Global world clock. Every animation reads `clock.t` (seconds) instead of
// R3F's delta, so that video capture is frame-exact and reproducible:
// in record mode the exporter sets clock.t = frame / fps before each render.
export const params = new URLSearchParams(typeof location !== 'undefined' ? location.search : '')
export const RECORD = params.get('record') === '1'

export const clock = {
  t: 0,
  speed: 1,
  paused: false,
  /** shared uniform objects for shaders (wind, water, flags) */
  uTime: { value: 0 },
}

export function tickLive(delta: number) {
  if (RECORD || clock.paused) return
  clock.t += Math.min(delta, 0.1) * clock.speed
  clock.uTime.value = clock.t
}

export function setTime(t: number) {
  clock.t = t
  clock.uTime.value = t
}

// readiness tracking for the exporter (fonts, textures…)
let pending = 0
const waiters: (() => void)[] = []
export function holdReady() {
  pending++
  let done = false
  return () => {
    if (done) return
    done = true
    pending--
    if (pending === 0) waiters.splice(0).forEach((f) => f())
  }
}
export function whenReady(maxMs = 10000): Promise<void> {
  if (pending === 0) return Promise.resolve()
  return new Promise((r) => { waiters.push(r); setTimeout(() => { if (pending) console.warn('whenReady timeout, pending', pending); r() }, maxMs) })
}

export const ease = {
  inOut: (t: number) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2),
  out: (t: number) => 1 - Math.pow(1 - t, 3),
  in: (t: number) => t * t * t,
  outBack: (t: number) => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2) },
  outElastic: (t: number) => t === 0 ? 0 : t === 1 ? 1 : Math.pow(2, -10 * t) * Math.sin((t * 10 - 0.75) * ((2 * Math.PI) / 3)) + 1,
  expoInOut: (t: number) => t === 0 ? 0 : t === 1 ? 1 : t < 0.5 ? Math.pow(2, 20 * t - 10) / 2 : (2 - Math.pow(2, -20 * t + 10)) / 2,
}
export const clamp01 = (v: number) => Math.min(1, Math.max(0, v))
/** progress of t inside [a,b] */
export const seg = (t: number, a: number, b: number) => clamp01((t - a) / (b - a))
