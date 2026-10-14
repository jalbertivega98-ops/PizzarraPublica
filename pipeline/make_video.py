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
import viva  # noqa: E402
import wb  # noqa: E402
from wb import H, W  # noqa: E402
from universo import actor as universo_actor  # noqa: E402
from universo import fondos as universo_fondos  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 30
TRANSITION = 0.3


# ------------------------------------------------------------------ voz
def tts_elevenlabs(story, workdir):
    """Frases ya generadas con ElevenLabs (tts_elevenlabs.py, en GitHub Actions) y guardadas en voces_elevenlabs/."""
    import subprocess
    from tts_elevenlabs import CACHE, MODEL, edge_model, key, line_text, line_tono

    vcfg = story["voice"]
    sr, out, missing = 44100, [], []
    for si, sc in enumerate(story["scenes"]):
        for li, line in enumerate(sc["lines"]):
            text = line_text(line)
            model = vcfg.get("model") or (edge_model() if vcfg["engine"] == "edge" else MODEL)
            path = os.path.join(CACHE, key(vcfg["voice_id"], model, text, line_tono(story, line)) + ".mp3")
            if not os.path.exists(path):
                missing.append(text)
                continue
            raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "s16le", "-ac", "1", "-ar", str(sr), "-"],
                                 capture_output=True, check=True).stdout
            pcm = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768
            nz = np.where(np.abs(pcm) > 0.01)[0]
            a = 0
            if len(nz):
                a = max(0, nz[0] - int(0.03 * sr))
                pcm = pcm[a: nz[-1] + int(0.08 * sr)]
            words = None
            if os.path.exists(path[:-4] + ".json"):  # tiempos por palabra (estilo «viva»)
                words = [dict(w, t0=w["t0"] - a / sr, t1=w["t1"] - a / sr) for w in json.load(open(path[:-4] + ".json", encoding="utf-8"))]
            out.append((si, li, pcm, words))
    if missing:
        sys.exit(f"Faltan {len(missing)} frases ({vcfg['engine']}); ejecuta la acción «Voces ElevenLabs». Primera: {missing[0]}")
    return out, sr


def tts_maqueta(story, sr=44100):
    """Sin voz: silencio con la duración aproximada de cada frase (para revisar ritmo y encuadres)."""
    out = []
    for si, sc in enumerate(story["scenes"]):
        for li, line in enumerate(sc["lines"]):
            text = line["text"] if isinstance(line, dict) else line
            out.append((si, li, np.zeros(int(sr * (0.25 + 0.062 * len(text))), np.float32), None))
    return out, sr


def tts_lines(story, workdir, maqueta=False):
    if maqueta:
        return tts_maqueta(story)
    if story.get("voice", {}).get("engine") in ("elevenlabs", "edge"):
        return tts_elevenlabs(story, workdir)
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
            out.append((si, li, pcm, None))
    return out, sr


# ------------------------------------------------------------------ tiempo
def build_timeline(story, audio, sr):
    vv = viva.es_viva(story)
    gap = story.get("line_gap", 0.05 if vv else 0.12)
    t = 0.0
    scenes = []
    clips = []
    by_scene = {}
    for si, li, pcm, words in audio:
        by_scene.setdefault(si, []).append((li, pcm, words))
    for si, sc in enumerate(story["scenes"]):
        start = t
        lead = viva.DUR_TRANS.get(viva.transicion_de(story, si), TRANSITION) if vv and si else TRANSITION
        cur = start + sc.get("lead", 0.0 if si == 0 else lead)
        lines = []
        for li, pcm, words in by_scene[si]:
            d = len(pcm) / sr
            raw = sc["lines"][li]
            text = raw["text"] if isinstance(raw, dict) else raw
            cur += raw.get("pausa", 0.0) if isinstance(raw, dict) else 0.0  # silencio con intención
            lines.append({"t0": cur, "t1": cur + d, "text": text, "words": viva.palabras_reales(text, words, cur, d)})
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
    if at.startswith("@"):  # palabra exacta de la narración: "@15,6", "@sueldo#2", "@casa+0.2"
        return viva.resolver_palabra(at, scene)
    raise ValueError(f"'at' no válido: {at}")


FX_DUR = {"tachar": 0.35, "rodear": 0.4, "subrayar": 0.25, "borrar": 0.4, "latir": 0.35, "temblar": 0.45,
          "mover": 0.45, "golpe": 0.25}


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
            # vida después de dibujarse: fx (tachar, rodear, borrar, latir, temblar, mover, golpe) y cambios de cara
            e.fx = [(resolve_at(f["at"], tl, t0 + e.dur), f.get("dur", FX_DUR.get(f["do"], 0.35)), f) for f in spec.get("fx", [])]
            e.cambios = sorted(({**ch, "t": resolve_at(ch["at"], tl, t0 + e.dur)}
                                for ch in spec.get("caras", []) + spec.get("acciones", [])), key=lambda ch: ch["t"])
            if e.kind in wb.UNIVERSO:  # personajes del universo: palabras de la escena para mover la boca
                e.palabras = [(a, b) for ln in tl["lines"] for _, a, b in ln.get("words", [])]
                universo_actor.preparar(e)
            els.append(e)
            prev_end = t0 + e.dur
        per_scene.append(els)
    if viva.es_viva(story) and per_scene and per_scene[0]:
        # gancho: el fotograma 0 ya tiene el primer dibujo a medio trazar
        e = per_scene[0][0]
        if e.t0 <= 0.05:
            e.t0 -= e.dur * 0.55
    return per_scene


# ------------------------------------------------------------------ subtítulos
def subtitle_chunks(scenes, max_words=4, max_chars=24):
    """Divide cada frase en bloques cortos; los tiempos por palabra se estiman por nº de letras."""
    chunks = []
    for sc in scenes:
        for ln in sc["lines"]:
            words = [w for w, _, _ in ln["words"]]
            wt = [(a, b) for _, a, b in ln["words"]]
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
        hx = W / 2 - f.measureText(handle) / 2
        if scene_spec.get("fondo", story.get("fondo")):
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(hx - 18, 1618, hx + f.measureText(handle) + 18, 1662), 20, 20),
                        skia.Paint(Color=skia.Color(255, 255, 255, 225), AntiAlias=True))
        c.drawString(handle, hx, 1650, f, skia.Paint(Color=wb.rgb("gray"), AntiAlias=True))
    note = scene_spec.get("footnote")
    if note:
        f = wb.font("ui", 27)
        fondo = scene_spec.get("fondo", story.get("fondo"))
        for i, ln in enumerate(note.split("\n")):
            x, y = W / 2 - f.measureText(ln) / 2, (1590 if fondo else 1395) + i * 36
            if fondo:  # sobre un fondo de color, la fuente va en una pastilla blanca
                c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - 16, y - 27, x + f.measureText(ln) + 16, y + 9), 14, 14),
                            skia.Paint(Color=skia.Color(255, 255, 255, 225), AntiAlias=True))
            c.drawString(ln, x, y, f, skia.Paint(Color=wb.rgb("gray" if not fondo else "ink"), AntiAlias=True))


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
    vv = viva.es_viva(story)
    cam, cam_scene = None, -1
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
        c.save()
        fondo = spec.get("fondo", story.get("fondo"))
        if vv:  # cámara viva: sigue al trazo, golpes de zoom
            if si != cam_scene:
                cam, cam_scene = viva.Camara(), si
            viva.Camara.aplicar(c, *cam.update(t, elements[si]))
            if fondo:  # mundo cartoon: el fondo se mueve con la cámara
                universo_fondos.dibuja(c, fondo, t)
        else:  # cámara: zoom lento por escena
            z = 1 + spec.get("zoom", 0.035) * wb.ease((t - sc["start"]) / max(0.1, sc["end"] - sc["start"]))
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
        if vv:  # la transición mueve solo la pizarra; barra, etiqueta y subtítulos quedan encima
            board = surface.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType)
            tipo = viva.transicion_de(story, si) if si else None
            dtr = viva.DUR_TRANS.get(tipo, TRANSITION)
            if prev_last is not None and local < dtr:
                c.drawImage(skia.Image.fromarray(viva.mezcla(tipo, prev_last, board, local / dtr),
                                                 colorType=skia.kRGBA_8888_ColorType), 0, 0)
            else:
                last_frame = board
            draw_chrome(c, story, spec, t, total)
            viva.draw_subtitle(c, chunks, t, story.get("accent", "red"))
            proc.stdin.write(surface.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType).tobytes())
            if fi % (FPS * 5) == 0:
                print(f"  fotograma {fi}/{nframes}", flush=True)
            continue
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
            if e.kind in ("counter",) + wb.UNIVERSO or e.dur < 0.15:
                continue
            iv.append((max(0.0, e.t0), max(0.0, e.t0 + e.dur)))
    return iv


def build_audio(story, clips, sr, total, elements, workdir, scenes=None):
    n = int(total * sr) + sr
    voice = np.zeros(n, np.float32)
    for t0, pcm in clips:
        a = int(t0 * sr)
        voice[a:a + len(pcm)] += pcm[: n - a]
    vpath = os.path.join(workdir, "voice.wav")
    _write_wav(vpath, voice[: int(total * sr)], sr)
    mpath = os.path.join(workdir, "music.wav")
    mus = music.background(total, bpm=story.get("music_bpm", 92))
    spath = os.path.join(workdir, "scribble.wav")
    scr = music.scribble(total, drawing_intervals(elements))
    if viva.es_viva(story):  # cortes de música y efectos sincronizados
        mus = mus[: int(total * music.SR)] * viva.envolvente_musica(story, scenes, total, music.SR)[: len(mus)]
        fxpath = os.path.join(workdir, "efectos.wav")
        _write_wav(fxpath, story.get("sfx_volume", 1.0) * viva.pista_efectos(total, viva.eventos_sonido(story, scenes, elements), music.SR), music.SR)
    _write_wav(mpath, mus, music.SR)
    _write_wav(spath, scr, music.SR)
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
    fxpath = os.path.join(os.path.dirname(vpath), "efectos.wav")
    fx = os.path.exists(fxpath)
    flt = (f"[1:a]aresample=44100,highpass=f=70,acompressor=threshold=-18dB:ratio=3:attack=5:release=80,"
           f"volume=1.0,asplit=2[v][vsc];"
           f"[2:a]volume={mv}[m];[m][vsc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=300[md];"
           f"[3:a]volume={sv}[s];"
           + ("[4:a]volume=1.0[fx];[v][md][s][fx]amix=inputs=4" if fx else "[v][md][s]amix=inputs=3")
           + ":normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-i", vpath, "-i", mpath, "-i", spath,
           *(["-i", fxpath] if fx else []),
           "-filter_complex", flt, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ac", "2",
           "-ar", "48000", "-movflags", "+faststart", "-shortest", out]
    subprocess.run(cmd, check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("storyboard")
    ap.add_argument("--out", default=os.path.join(HERE, "..", "output"))
    ap.add_argument("--preview", action="store_true", help="render rápido a 10 fps")
    ap.add_argument("--keep-work", action="store_true", help="conserva audios y vídeo intermedios")
    ap.add_argument("--maqueta", action="store_true", help="sin voz (silencio con duración estimada) para revisar el montaje")
    ap.add_argument("--ritmo", action="store_true", help="solo el informe de ritmo (estilo «viva»), sin render")
    ap.add_argument("--hoja", action="store_true", help="hoja de contactos (1 fotograma por segundo) tras el render")
    args = ap.parse_args()
    story = json.load(open(args.storyboard, encoding="utf-8"))
    wb.ICON_ACCENT.update(story.get("icon_accent", {}))
    slug = story["slug"]
    outdir = os.path.abspath(os.path.join(args.out, slug))
    work = os.path.join(outdir, "_work")
    os.makedirs(work, exist_ok=True)

    print("1/5 Voz…")
    audio, sr = tts_lines(story, work, args.maqueta)
    scenes, clips, total = build_timeline(story, audio, sr)
    total += story.get("end_hold", 1.2)
    scenes[-1]["end"] = total
    print(f"   duración total: {total:.1f} s")
    elements = build_elements(story, scenes)
    chunks = subtitle_chunks(scenes, *((3, 20) if viva.es_viva(story) else ()))
    if viva.es_viva(story):
        resumen, avisos = viva.informe_ritmo(story, scenes, elements, total)
        txt = resumen + "\n" + ("\n".join("⚠ " + a for a in avisos) if avisos else "✓ Cumple el estándar de enganche")
        open(os.path.join(outdir, f"{slug}_ritmo.txt"), "w", encoding="utf-8").write(txt + "\n")
        print("   " + txt.replace("\n", "\n   "))
        if args.ritmo:
            return
    write_srt(chunks, os.path.join(outdir, f"{slug}.srt"))

    print("2/5 Fotogramas…")
    noaudio = os.path.join(work, "video_noaudio.mp4")
    render(story, scenes, elements, chunks, total, noaudio, preview=args.preview)
    print("3/5 Música y efectos…")
    vpath, mpath, spath = build_audio(story, clips, sr, total, elements, work, scenes)
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
    if args.hoja:
        hoja = os.path.join(outdir, f"{slug}_hoja.jpg")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", final, "-vf", "fps=2,scale=216:-2,tile=10x8", "-frames:v", "1",
                        "-q:v", "4", hoja], check=True)
        print("Hoja:", hoja)
    print("Listo:", final)


if __name__ == "__main__":
    main()
