#!/usr/bin/env python3
"""Genera un Reel whiteboard 1080x1920 a partir de un storyboard JSON.

Uso:
    python3 make_video.py storyboards/reel01_presidente.json [--out ../output] [--preview]

Pasos: voz (Piper, es_ES) por frase -> línea de tiempo -> render de fotogramas
(skia) -> música y efectos generados -> mezcla y MP4 (ffmpeg) -> SRT y texto.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import wave

import numpy as np
import skia

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import music  # noqa: E402
import wb  # noqa: E402
from wb import H, W  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 30
TRANSITION = 0.3


# ------------------------------------------------------------------ voz
def tts_lines(story, workdir):
    from piper import PiperVoice, SynthesisConfig

    vcfg = story.get("voice", {})
    model = os.path.expanduser(vcfg.get("model", os.path.join(HERE, "voices", "es_ES-davefx-medium.onnx")))
    if not os.path.isabs(model):
        model = os.path.join(HERE, model)
    voice = PiperVoice.load(model)
    syn = SynthesisConfig(speaker_id=vcfg.get("speaker"), length_scale=vcfg.get("length_scale", 0.92),
                          noise_scale=vcfg.get("noise_scale", 0.6), noise_w_scale=vcfg.get("noise_w", 0.8))
    sr = None
    out = []
    for si, sc in enumerate(story["scenes"]):
        for li, line in enumerate(sc["lines"]):
            text = line["tts"] if isinstance(line, dict) and "tts" in line else (line["text"] if isinstance(line, dict) else line)
            path = os.path.join(workdir, f"s{si:02d}_l{li:02d}.wav")
            with wave.open(path, "wb") as wf:
                voice.synthesize_wav(text, wf, syn_config=syn)
            with wave.open(path, "rb") as wf:
                sr = wf.getframerate()
                pcm = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float32) / 32768
            # recorta silencios de los extremos
            nz = np.where(np.abs(pcm) > 0.01)[0]
            if len(nz):
                pcm = pcm[max(0, nz[0] - int(0.03 * sr)): nz[-1] + int(0.08 * sr)]
            out.append((si, li, pcm))
    return out, sr


# ------------------------------------------------------------------ tiempo
def build_timeline(story, audio, sr):
    gap = story.get("line_gap", 0.12)
    t = 0.0
    scenes = []
    clips = []
    by_scene = {}
    for si, li, pcm in audio:
        by_scene.setdefault(si, []).append((li, pcm))
    for si, sc in enumerate(story["scenes"]):
        start = t
        cur = start + sc.get("lead", 0.0 if si == 0 else TRANSITION)
        lines = []
        for li, pcm in by_scene[si]:
            d = len(pcm) / sr
            raw = sc["lines"][li]
            text = raw["text"] if isinstance(raw, dict) else raw
            lines.append({"t0": cur, "t1": cur + d, "text": text})
            clips.append((cur, pcm))
            cur += d + gap
        end = max(cur - gap + sc.get("tail", 0.45), start + sc.get("min_dur", 0))
        scenes.append({"start": start, "end": end, "lines": lines})
        t = end
    return scenes, clips, t


def resolve_at(at, scene, prev_end):
    """'L1+0.3' = inicio de la frase 1 + 0,3 s; '+0.2' = tras el elemento anterior; número = s desde la escena."""
    if isinstance(at, (int, float)):
        return scene["start"] + at
    m = re.fullmatch(r"L(\d+)(?:@([\d.]+))?([+-][\d.]+)?", at)
    if m:
        ln = scene["lines"][int(m.group(1))]
        base = ln["t0"]
        if m.group(2):  # fracción de la frase: 'L1@0.5'
            base += (ln["t1"] - ln["t0"]) * float(m.group(2))
        return base + float(m.group(3) or 0)
    if at.startswith("+"):
        return prev_end + float(at[1:])
    if at == "end":
        return scene["end"]
    raise ValueError(f"'at' no válido: {at}")


def build_elements(story, scenes):
    rng = np.random.default_rng(42)
    per_scene = []
    for sc, tl in zip(story["scenes"], scenes):
        els = []
        prev_end = tl["start"]
        for spec in sc["elements"]:
            t0 = resolve_at(spec.get("at", "+0.05"), tl, prev_end)
            if "out" in spec:
                spec = dict(spec, out_t=resolve_at(spec["out"], tl, prev_end))
            e = wb.Element(spec, t0, rng)
            els.append(e)
            prev_end = t0 + e.dur
        per_scene.append(els)
    return per_scene


# ------------------------------------------------------------------ subtítulos
def subtitle_chunks(scenes, max_words=4, max_chars=24):
    """Divide cada frase en bloques cortos; los tiempos por palabra se estiman por nº de letras."""
    chunks = []
    for sc in scenes:
        for ln in sc["lines"]:
            words = ln["text"].split()
            weights = np.array([len(w) + 1.5 for w in words], float)
            cum = np.concatenate([[0], np.cumsum(weights)]) / weights.sum()
            dur = ln["t1"] - ln["t0"]
            wt = [(ln["t0"] + cum[i] * dur, ln["t0"] + cum[i + 1] * dur) for i in range(len(words))]
            group = []
            for i, w in enumerate(words):
                if group and (len(group) >= max_words or len(" ".join(words[j] for j in group + [i])) > max_chars):
                    chunks.append({"words": [(words[j], *wt[j]) for j in group]})
                    group = []
                group.append(i)
                if re.search(r"[.,:;?!]$", w) and len(group) >= 2:
                    chunks.append({"words": [(words[j], *wt[j]) for j in group]})
                    group = []
            if group:
                chunks.append({"words": [(words[j], *wt[j]) for j in group]})
    for i, ch in enumerate(chunks):
        ch["t0"] = ch["words"][0][1]
        ch["t1"] = ch["words"][-1][2]
        if i + 1 < len(chunks):
            ch["t1"] = max(ch["t1"], min(chunks[i + 1]["words"][0][1], ch["t1"] + 0.4))
    return chunks


def write_srt(chunks, path):
    def ts(t):
        ms = int(round(t * 1000))
        return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
    with open(path, "w", encoding="utf-8") as f:
        for i, ch in enumerate(chunks, 1):
            f.write(f"{i}\n{ts(ch['t0'])} --> {ts(ch['t1'])}\n{' '.join(w for w, _, _ in ch['words'])}\n\n")


def draw_subtitle(c, chunks, t, y=1520):
    ch = next((ch for ch in chunks if ch["t0"] <= t < ch["t1"]), None)
    if not ch:
        return
    f = wb.font("sub", 66)
    space = f.measureText(" ")
    widths = [f.measureText(w) for w, _, _ in ch["words"]]
    total = sum(widths) + space * (len(widths) - 1)
    x = W / 2 - total / 2
    pop = wb.ease_out((t - ch["t0"]) / 0.12)
    c.save()
    c.translate(W / 2, y)
    c.scale(0.9 + 0.1 * pop, 0.9 + 0.1 * pop)
    c.translate(-W / 2, -y)
    bg = skia.Paint(Color=skia.Color(255, 255, 255, 235), AntiAlias=True)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - 28, y - 70, x + total + 28, y + 26), 22, 22), bg)
    for (w, w0, w1), wd in zip(ch["words"], widths):
        active = w0 <= t < w1 + 0.05
        if active:
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - 8, y - 62, x + wd + 8, y + 16), 12, 12),
                        skia.Paint(Color=wb.rgb("yellow"), AntiAlias=True))
        c.drawString(w, x, y, f, skia.Paint(Color=wb.rgb("ink"), AntiAlias=True))
        x += wd + space
    c.restore()


def publicacion_text(story):
    """Descripción para Instagram + hashtags + comentario fijado con las fuentes."""
    txt = story.get("caption", "").strip() + "\n\n" + " ".join(story.get("hashtags", [])) + "\n"
    if story.get("pinned_comment"):
        txt += "\n--- Comentario fijado ---\n" + story["pinned_comment"].strip() + "\n"
    return txt


# ------------------------------------------------------------------ render
def draw_chrome(c, story, scene_spec, t, total):
    # barra de progreso
    c.drawRect(skia.Rect(0, 0, W * t / total, 12), skia.Paint(Color=wb.rgb(story.get("accent", "blue")), AntiAlias=True))
    # etiqueta de serie
    tag = story.get("series_tag")
    if tag:
        f = wb.font("ui", 34)
        tw = f.measureText(tag)
        r = skia.Rect(W / 2 - tw / 2 - 26, 250, W / 2 + tw / 2 + 26, 306)
        c.drawRRect(skia.RRect.MakeRectXY(r, 28, 28), skia.Paint(Color=wb.rgb("ink"), AntiAlias=True))
        c.drawString(tag, W / 2 - tw / 2, 290, f, skia.Paint(Color=wb.rgb("paper"), AntiAlias=True))
    handle = story.get("handle")
    if handle:
        f = wb.font("ui", 32)
        c.drawString(handle, W / 2 - f.measureText(handle) / 2, 1650, f, skia.Paint(Color=wb.rgb("gray"), AntiAlias=True))
    note = scene_spec.get("footnote")
    if note:
        f = wb.font("ui", 27)
        for i, ln in enumerate(note.split("\n")):
            c.drawString(ln, W / 2 - f.measureText(ln) / 2, 1395 + i * 36, f, skia.Paint(Color=wb.rgb("gray"), AntiAlias=True))


def render(story, scenes, elements, chunks, total, out_video_noaudio, preview=False):
    surface = skia.Surface(W, H)
    c = surface.getCanvas()
    paper = wb.paper_texture()
    nframes = int(np.ceil(total * FPS))
    step = 1
    fps = FPS
    if preview:  # rápido: 10 fps
        step, fps = 3, 10
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}",
           "-r", str(fps), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
           "-pix_fmt", "yuv420p", out_video_noaudio]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    prev_last = None
    cur_scene = -1
    last_frame = None
    for fi in range(0, nframes, step):
        t = fi / FPS
        si = max(i for i, s in enumerate(scenes) if s["start"] <= t + 1e-9)
        if si != cur_scene:
            prev_last = last_frame
            cur_scene = si
        sc, spec = scenes[si], story["scenes"][si]
        local = t - sc["start"]
        c.clear(wb.rgb("paper"))
        c.drawImage(paper, 0, 0)
        # cámara: zoom lento por escena
        z = 1 + spec.get("zoom", 0.035) * wb.ease((t - sc["start"]) / max(0.1, sc["end"] - sc["start"]))
        c.save()
        c.translate(W / 2, 820)
        c.scale(z, z)
        c.translate(-W / 2, -820)
        tip, tip_col = None, "ink"
        for e in elements[si]:
            tp = e.draw(c, t)
            if tp is not None:
                tip, tip_col = tp, e.spec.get("color", "ink") if e.kind != "highlight" else "yellow"
        if tip is not None:
            wb.draw_marker(c, tip, tip_col if tip_col in wb.PALETTE else "ink")
        c.restore()
        draw_chrome(c, story, spec, t, total)
        draw_subtitle(c, chunks, t)
        frame = surface.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType)
        # transición: el papel nuevo entra desde la derecha
        if prev_last is not None and local < TRANSITION:
            k = wb.ease(local / TRANSITION)
            off = int(W * (1 - k))
            shown = frame.copy()
            shown[:, off:] = frame[:, : W - off]
            shown[:, :off] = prev_last[:, W - off:] if off > 0 else shown[:, :0]
            frame = shown
        else:
            last_frame = frame
        proc.stdin.write(frame.tobytes())
        if fi % (FPS * 5) == 0:
            print(f"  fotograma {fi}/{nframes}", flush=True)
    proc.stdin.close()
    proc.wait()


def drawing_intervals(elements):
    iv = []
    for els in elements:
        for e in els:
            if e.kind in ("counter",) or e.dur < 0.15:
                continue
            iv.append((e.t0, e.t0 + e.dur))
    return iv


def build_audio(story, clips, sr, total, elements, workdir):
    n = int(total * sr) + sr
    voice = np.zeros(n, np.float32)
    for t0, pcm in clips:
        a = int(t0 * sr)
        voice[a:a + len(pcm)] += pcm[: n - a]
    vpath = os.path.join(workdir, "voice.wav")
    _write_wav(vpath, voice[: int(total * sr)], sr)
    mpath = os.path.join(workdir, "music.wav")
    _write_wav(mpath, music.background(total, bpm=story.get("music_bpm", 92)), music.SR)
    spath = os.path.join(workdir, "scribble.wav")
    _write_wav(spath, music.scribble(total, drawing_intervals(elements)), music.SR)
    return vpath, mpath, spath


def _write_wav(path, x, sr):
    x = np.clip(x, -1, 1)
    with wave.open(path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes((x * 32767).astype(np.int16).tobytes())


def mux(video, vpath, mpath, spath, out, story):
    mv = story.get("music_volume", 0.16)
    sv = story.get("scribble_volume", 0.05)
    flt = (f"[1:a]aresample=44100,highpass=f=70,acompressor=threshold=-18dB:ratio=3:attack=5:release=80,"
           f"volume=1.0,asplit=2[v][vsc];"
           f"[2:a]volume={mv}[m];[m][vsc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=300[md];"
           f"[3:a]volume={sv}[s];"
           f"[v][md][s]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-i", vpath, "-i", mpath, "-i", spath,
           "-filter_complex", flt, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ac", "2",
           "-ar", "48000", "-movflags", "+faststart", "-shortest", out]
    subprocess.run(cmd, check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("storyboard")
    ap.add_argument("--out", default=os.path.join(HERE, "..", "output"))
    ap.add_argument("--preview", action="store_true", help="render rápido a 10 fps")
    ap.add_argument("--keep-work", action="store_true", help="conserva audios y vídeo intermedios")
    args = ap.parse_args()
    story = json.load(open(args.storyboard, encoding="utf-8"))
    wb.ICON_ACCENT.update(story.get("icon_accent", {}))
    slug = story["slug"]
    outdir = os.path.abspath(os.path.join(args.out, slug))
    work = os.path.join(outdir, "_work")
    os.makedirs(work, exist_ok=True)

    print("1/5 Voz…")
    audio, sr = tts_lines(story, work)
    scenes, clips, total = build_timeline(story, audio, sr)
    total += story.get("end_hold", 1.2)
    scenes[-1]["end"] = total
    print(f"   duración total: {total:.1f} s")
    elements = build_elements(story, scenes)
    chunks = subtitle_chunks(scenes)
    write_srt(chunks, os.path.join(outdir, f"{slug}.srt"))

    print("2/5 Fotogramas…")
    noaudio = os.path.join(work, "video_noaudio.mp4")
    render(story, scenes, elements, chunks, total, noaudio, preview=args.preview)
    print("3/5 Música y efectos…")
    vpath, mpath, spath = build_audio(story, clips, sr, total, elements, work)
    print("4/5 Mezcla…")
    final = os.path.join(outdir, f"{slug}.mp4")
    mux(noaudio, vpath, mpath, spath, final, story)
    print("5/5 Textos…")
    with open(os.path.join(outdir, f"{slug}_publicacion.txt"), "w", encoding="utf-8") as f:
        f.write(publicacion_text(story))
    timing = [{"escena": s.get("id"), "inicio": round(tl["start"], 2), "fin": round(tl["end"], 2),
               "frases": [{"t0": round(l["t0"], 2), "t1": round(l["t1"], 2), "texto": l["text"]} for l in tl["lines"]]}
              for s, tl in zip(story["scenes"], scenes)]
    json.dump(timing, open(os.path.join(outdir, f"{slug}_tiempos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if not args.keep_work:
        shutil.rmtree(work, ignore_errors=True)
    print("Listo:", final)


if __name__ == "__main__":
    main()
