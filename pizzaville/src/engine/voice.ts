// Voice lines: timing (from edge-tts word boundaries when available) and
// procedural lip-sync. Without audio, durations are estimated from text.
import { holdReady } from './clock'

export type Word = { w: string; t: number; d: number }
export type Line = { id: string; text: string; at: number; words: Word[]; dur: number; hasAudio: boolean }

const VOWELS = /[aeiouáéíóúü]/gi

function estimate(text: string): Word[] {
  const out: Word[] = []
  let t = 0
  for (const raw of text.split(/\s+/)) {
    const syl = Math.max(1, (raw.match(VOWELS) ?? []).length)
    const d = syl * 0.16
    out.push({ w: raw.replace(/[¡!¿?.,…]/g, ''), t, d })
    t += d + (/[.!?…]$/.test(raw) ? 0.35 : /,$/.test(raw) ? 0.15 : 0.03)
  }
  return out
}

/** loads line timings; desired start times may be pushed later to avoid overlap */
export function useLines(episode: string, script: { id: string; text: string; at: number }[]) {
  const lines: Line[] = script.map((s) => {
    const words = estimate(s.text)
    const last = words[words.length - 1]
    return { ...s, words, dur: last.t + last.d, hasAudio: false }
  })
  const done = holdReady()
  Promise.all(
    lines.map(async (l) => {
      try {
        const r = await fetch(`/voz/${episode}/${l.id}.json`)
        if (!r.ok) return
        const j = await r.json()
        if (j.text !== l.text || !j.words?.length) return // stale audio for an edited line
        l.words = j.words
        const last = j.words[j.words.length - 1]
        l.dur = last.t + last.d + 0.15
        l.hasAudio = true
      } catch { /* no audio yet */ }
    }),
  ).then(() => {
    // avoid overlaps
    for (let i = 1; i < lines.length; i++) lines[i].at = Math.max(lines[i].at, lines[i - 1].at + lines[i - 1].dur + 0.2)
    done()
  })
  return lines
}

/** mouth openness 0..1 at time t */
export function mouthAt(lines: Line[], t: number) {
  for (const l of lines) {
    const lt = t - l.at
    if (lt < 0 || lt > l.dur) continue
    for (const w of l.words) {
      if (lt >= w.t && lt <= w.t + w.d) {
        const syl = Math.max(1, (w.w.match(VOWELS) ?? []).length)
        const ph = ((lt - w.t) / w.d) * syl
        const v = Math.abs(Math.sin(ph * Math.PI))
        return 0.18 + 0.72 * Math.pow(v, 0.7)
      }
    }
    return 0.05
  }
  return 0
}

export function speakingAt(lines: Line[], t: number) {
  return lines.find((l) => t >= l.at && t <= l.at + l.dur) ?? null
}
