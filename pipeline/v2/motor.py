#!/usr/bin/env python3
"""Pizarra Pública v2: motor de animación para Reels/TikTok 1080×1920.

Un vídeo es una lista de *planos* (2-4 s cada uno). Cada plano tiene sus frases de voz, una cámara,
una transición de entrada y unos elementos animados que se sincronizan con palabras concretas
de la narración ("at": "@palabra"). Ver README.md.

  python3 motor.py videos/bajas.py              # vídeo final
  python3 motor.py videos/bajas.py --preview    # 15 fps, rápido
  python3 motor.py videos/bajas.py --hoja       # hoja de contactos (PNG) para revisar el ritmo
"""
import argparse
import importlib.util
import json
import math
import os
import re
import subprocess
import sys
import unicodedata
from multiprocessing import Pool

import numpy as np
import skia

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import dibujo as D  # noqa: E402
import personajes as P  # noqa: E402
import sonido as S  # noqa: E402
from dibujo import H, W, clamp, e_back, e_inout, e_out  # noqa: E402

FPS = 30
TRANS = 0.32          # duración de las transiciones
GAP = 0.10            # silencio entre frases
CAP_Y = 1400          # línea base de los subtítulos (por encima del texto y botones de TikTok/Reels)
ESC = 1.16            # zoom global de la escena: todo grande, que llene la pantalla
ZONA = (230, 1230)    # zona útil de dibujo (y)


# ================================================================== voz y tiempos
def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return re.sub(r"[^a-z0-9ñ%]", "", "".join(c for c in s if unicodedata.category(c) != "Mn"))


def cargar_video(path):
    spec = importlib.util.spec_from_file_location("v_" + os.path.basename(path)[:-3], path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.VIDEO


def cargar_voz(video, linea):
    """Devuelve (pcm, palabras[(texto_subtítulo, t0, t1)]). Sin audio generado: silencio con tiempos estimados."""
    import voz as V

    txt_tts = V.texto_tts(linea)
    txt_sub = linea["text"] if isinstance(linea, dict) else linea
    k = V.clave(txt_tts, video.get("voz", V.VOZ), video.get("velocidad", V.VELOCIDAD))
    mp3 = os.path.join(V.CACHE, k + ".mp3")
    toks = txt_sub.split()
    if not os.path.exists(mp3):
        d = 0.058 * len(txt_tts) + 0.2
        return np.zeros(int(S.SR * d), np.float32), _reparte(toks, 0.05, d - 0.1), False
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", mp3, "-f", "s16le", "-ac", "1", "-ar", str(S.SR), "-"],
                         capture_output=True, check=True).stdout
    pcm = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768
    nz = np.where(np.abs(pcm) > 0.012)[0]
    ini = max(0, nz[0] - int(0.02 * S.SR)) if len(nz) else 0
    fin = nz[-1] + int(0.06 * S.SR) if len(nz) else len(pcm)
    pcm = pcm[ini:fin]
    off = ini / S.SR
    bounds = json.load(open(os.path.join(V.CACHE, k + ".json"), encoding="utf-8"))
    bounds = [(b["w"], b["t"] - off, b["t"] - off + b["d"]) for b in bounds]
    return pcm, _alinea(toks, bounds, len(pcm) / S.SR), True


def _reparte(toks, t0, t1):
    n = sum(len(t) + 2 for t in toks) or 1
    out, c = [], t0
    for t in toks:
        d = (t1 - t0) * (len(t) + 2) / n
        out.append((t, c, c + d * 0.92))
        c += d
    return out


def _alinea(toks, bounds, dur):
    """Asigna a cada palabra del subtítulo el tiempo de la palabra hablada que le corresponde."""
    res = [None] * len(toks)
    j = 0
    for i, tk in enumerate(toks):
        nt = norm(tk)
        for jj in range(j, min(j + 4, len(bounds))):
            if nt and norm(bounds[jj][0]) == nt:
                res[i] = (bounds[jj][1], bounds[jj][2])
                j = jj + 1
                break
    # interpola los que no casan (cifras escritas con dígitos, siglas...)
    known = [(i, r) for i, r in enumerate(res) if r]
    if not known:
        return _reparte(toks, 0.02, dur - 0.05)
    out = []
    for i, tk in enumerate(toks):
        if res[i]:
            out.append((tk, *res[i]))
            continue
        prev = max([k for k in known if k[0] < i], default=None, key=lambda k: k[0])
        nxt = min([k for k in known if k[0] > i], default=None, key=lambda k: k[0])
        a = prev[1][1] if prev else 0.0
        b = nxt[1][0] if nxt else dur
        ia = prev[0] if prev else -1
        ib = nxt[0] if nxt else len(toks)
        seg = (b - a) / (ib - ia - 1 + 1e-9)
        t0 = a + seg * (i - ia - 1)
        out.append((tk, t0, t0 + seg * 0.95))
    return out


# ================================================================== línea de tiempo
class Plano:
    pass


def construye(video):
    planos, clips, t = [], [], 0.0
    real = True
    for i, sp in enumerate(video["planos"]):
        pl = Plano()
        pl.sp, pl.i = sp, i
        pl.ini = t
        cur = t + (0.0 if i == 0 else 0.08) + sp.get("pausa", 0)
        pl.lineas = []
        for linea in sp.get("voz", []):
            pcm, pals, ok = cargar_voz(video, linea)
            real &= ok
            d = len(pcm) / S.SR
            pl.lineas.append({"t0": cur, "t1": cur + d, "pals": [(w, cur + a, cur + b) for w, a, b in pals]})
            clips.append((cur, pcm))
            cur += d + GAP
        fin = cur - GAP + sp.get("cola", 0.18)
        pl.fin = max(fin, t + sp.get("min", 0))
        t = pl.fin
        planos.append(pl)
    return planos, clips, t, real


def resuelve(at, pl, prev=None):
    """'@palabra[+0.2]' = cuando se dice la palabra; 'L1' = inicio de la frase 1; número = s desde el inicio del plano;
    'fin-0.4' = antes del final del plano."""
    if at is None:
        return pl.ini
    if isinstance(at, (int, float)):
        return pl.ini + at
    m = re.fullmatch(r"@([^+\-]+)([+-][\d.]+)?", at)
    if m:
        w = norm(m.group(1))
        for ln in pl.lineas:
            for tk, a, b in ln["pals"]:
                if norm(tk).startswith(w):
                    return a + float(m.group(2) or 0)
        raise ValueError(f"Palabra '{m.group(1)}' no está en el plano {pl.i}: {[x[0] for ln in pl.lineas for x in ln['pals']]}")
    m = re.fullmatch(r"L(\d+)([+-][\d.]+)?", at)
    if m:
        return pl.lineas[int(m.group(1))]["t0"] + float(m.group(2) or 0)
    m = re.fullmatch(r"fin([+-][\d.]+)?", at)
    if m:
        return pl.fin + float(m.group(1) or 0)
    raise ValueError(f"'at' no válido: {at}")


# ================================================================== elementos
class El:
    entrada = 0.28

    def __init__(s, sp, pl, video, rng):
        s.sp, s.pl, s.video = sp, pl, video
        s.t0 = resuelve(sp.get("at"), pl)
        s.t1 = resuelve(sp["hasta"], pl) if "hasta" in sp else None
        s.x, s.y = sp.get("x", 540), sp.get("y", 700)
        s.esc = sp.get("tam", 1.0)
        s.rot = sp.get("rot", 0)
        s.z = sp.get("z", 0)
        s.rng = rng
        s.anim = sp.get("anim", "pop")
        s.prep()

    def prep(s):
        pass

    def golpes(s):
        """[(t, fuerza)] para la sacudida de cámara."""
        return []

    def sonidos(s):
        """[(t, nombre, kw)]"""
        return [(s.t0, "pop", {"pitch": s.rng.uniform(0.85, 1.3)})] if s.anim in ("pop", "cae") else []

    def transform(s, cv, t):
        """Aplica la animación de entrada/salida. Devuelve alpha o None si no se ve."""
        if t < s.t0:
            return None
        u = (t - s.t0) / s.entrada
        sal = 1.0
        if s.t1 is not None:
            if t > s.t1 + 0.2:
                return None
            if t > s.t1:
                sal = 1 - (t - s.t1) / 0.2
        cv.translate(s.x, s.y)
        if s.rot:
            cv.rotate(s.rot)
        a = s.anim
        if a == "pop":
            k = e_back(u) * sal
            cv.scale(s.esc * max(k, 0.001), s.esc * max(k, 0.001))
        elif a == "golpe":  # cae desde grande (sello, cifras)
            k = 1 + 1.6 * (1 - e_out(u * 1.6))
            cv.scale(s.esc * k, s.esc * k)
            return int(255 * clamp(u * 3) * sal)
        elif a == "cae":
            dy = -900 * (1 - D.e_elastic(u * 0.55)) if u < 1.8 else 0
            cv.translate(0, dy)
            cv.scale(s.esc, s.esc)
        elif a.startswith("entra"):
            lado = -1 if a.endswith("izq") else 1
            k = e_out(u * 0.9)
            cv.translate(lado * 900 * (1 - k), 0)
            sq = 1 + 0.12 * math.sin(clamp(u) * math.pi)
            cv.scale(s.esc * sq, s.esc / sq)
        elif a == "fade":
            cv.scale(s.esc, s.esc)
            return int(255 * clamp(u) * sal)
        else:
            cv.scale(s.esc, s.esc)
        return int(255 * sal)

    def dibuja(s, cv, t):
        cv.save()
        al = s.transform(cv, t)
        if al is not None and al > 0:
            s.pinta(cv, t, al)
        cv.restore()

    def pinta(s, cv, t, al):
        pass


class Num(El):
    """Cifra gigante con contador. sp: val, desde, dec, suf, pre, color, tam(px), dur, fondo (yellow/estallido), golpe."""
    entrada = 0.22

    def prep(s):
        sp = s.sp
        s.anim = sp.get("anim", "golpe" if sp.get("golpe") else "pop")
        s.val, s.desde = sp["val"], sp.get("desde", 0)
        s.dur = sp.get("dur", 0.9 if s.desde != s.val else 0)
        s.f = D.fuente("num", sp.get("px", 210))
        s.col = sp.get("color", "ink")

    def golpes(s):
        return [(s.t0 + s.dur, 1.0 if s.sp.get("golpe") else 0.4)]

    def sonidos(s):
        out = []
        if s.dur > 0:
            out.append((s.t0, "contador", {"d": s.dur}))
        out.append((s.t0 + s.dur, "impacto" if s.sp.get("golpe") else "pop", {} if s.sp.get("golpe") else {"pitch": 0.8}))
        return out

    def pinta(s, cv, t, al):
        u = clamp((t - s.t0) / s.dur) if s.dur > 0 else 1
        v = s.desde + (s.val - s.desde) * e_out(u)
        txt = s.sp.get("pre", "") + D.fmt_num(v, s.sp.get("dec", 0)) + s.sp.get("suf", "")
        w = s.f.measureText(txt)
        px = s.f.getSize()
        wfin = s.f.measureText(s.sp.get("pre", "") + D.fmt_num(s.val, s.sp.get("dec", 0)) + s.sp.get("suf", ""))
        if wfin > 900:
            k = 900 / wfin
            cv.scale(k, k)
        fondo = s.sp.get("fondo")
        if fondo == "estallido":
            _estallido(cv, 0, -px * 0.35, max(w, px) * 0.72, s.sp.get("fondo_color", "yellow"), t, al)
        elif fondo:
            cv.save()
            cv.rotate(-2)
            r = skia.Rect(-w / 2 - 30, -px * 0.78, -w / 2 - 30 + (w + 60) * e_out((t - s.t0) / 0.3), px * 0.08)
            cv.drawRoundRect(r, 18, 18, D.p_fill(fondo, al))
            cv.restore()
        # sacudida del número mientras cuenta
        if 0 < u < 1:
            cv.translate(s.rng.uniform(-3, 3), s.rng.uniform(-3, 3))
        D.texto(cv, txt, 0, 0, s.f, s.col, "white", 18, alpha=al)
        if s.sp.get("sub"):
            D.texto(cv, s.sp["sub"], 0, px * 0.42, D.fuente("mano", px * 0.26), "ink", "white", 10, alpha=al)


def _estallido(cv, cx, cy, r, color, t, al, puntas=14):
    p = skia.Path()
    rot = t * 18
    for k in range(puntas * 2):
        a = math.radians(rot + k * 180 / puntas)
        rr = r * (1.0 if k % 2 == 0 else 0.72)
        x, y = cx + rr * math.cos(a), cy + rr * 0.8 * math.sin(a)
        p.moveTo(x, y) if k == 0 else p.lineTo(x, y)
    p.close()
    cv.save()
    cv.translate(*D.OFF)
    cv.drawPath(p, D.p_fill(color, al))
    cv.restore()
    cv.drawPath(p, D.p_stroke("ink", 7, al))


class Txt(El):
    """Texto. sp: t, px, fuente (num|mano|ui), color, marca (color de subrayador), lineas separadas por \\n, ancho."""

    def prep(s):
        sp = s.sp
        s.f = D.fuente(sp.get("fuente", "num"), sp.get("px", 90))
        s.lineas = sp["t"].split("\n")
        s.col = sp.get("color", "ink")
        s.anim = sp.get("anim", "pop")

    def pinta(s, cv, t, al):
        px = s.f.getSize()
        lh = px * 1.08
        wmax = max(s.f.measureText(x) for x in s.lineas) + (44 if s.sp.get("marca") else 0)
        lim = s.sp.get("ancho", 740 if abs(s.x - 540) < 120 else 2 * min(s.x, 1080 - s.x) / 1.16 - 30)
        if wmax > lim:
            cv.scale(lim / wmax, lim / wmax)
        y0 = -lh * (len(s.lineas) - 1) / 2 + px * 0.35
        resp = 1 + 0.018 * math.sin((t - s.t0) * 4 + s.y)
        cv.scale(resp, resp)
        for i, ln in enumerate(s.lineas):
            y = y0 + i * lh
            if s.anim == "escribe":
                n = int(len(ln) * clamp((t - s.t0 - i * 0.25) / max(0.25, len(ln) * 0.035)))
                ln = ln[:n]
            if s.sp.get("marca"):
                w = s.f.measureText(s.lineas[i])
                k = e_out((t - s.t0 - 0.1 - i * 0.12) / 0.3)
                if k > 0:
                    cv.save()
                    cv.rotate(-1.5)
                    cv.drawRoundRect(skia.Rect(-w / 2 - 22, y - px * 0.78, -w / 2 - 22 + (w + 44) * k, y + px * 0.16), 14, 14,
                                     D.p_fill(s.sp["marca"], al))
                    cv.restore()
            D.texto(cv, ln, 0, y, s.f, s.col, "white" if not s.sp.get("marca") else None, 14, alpha=al)


class Sello(El):
    entrada = 0.2

    def prep(s):
        s.anim = "golpe"
        s.rot = s.sp.get("rot", -10)
        s.f = D.fuente("num", s.sp.get("px", 84))

    def golpes(s):
        return [(s.t0 + 0.12, 1.3)]

    def sonidos(s):
        return [(s.t0 + 0.1, "sello", {})]

    def pinta(s, cv, t, al):
        txt = s.sp["t"]
        w = s.f.measureText(txt)
        px = s.f.getSize()
        c = s.sp.get("color", "red")
        r = skia.Rect(-w / 2 - 34, -px * 0.95, w / 2 + 34, px * 0.38)
        cv.drawRoundRect(r, 16, 16, D.p_fill("white", int(al * 0.85)))
        cv.drawRoundRect(r, 16, 16, D.p_stroke(c, 12, al))
        r2 = skia.Rect(r.left() + 14, r.top() + 14, r.right() - 14, r.bottom() - 14)
        cv.drawRoundRect(r2, 10, 10, D.p_stroke(c, 4, al))
        cv.drawString(txt, -w / 2, 0, s.f, D.p_fill(c, al))


class Gente(El):
    """Rejilla de personitas. sp: n, cols, sep, destacar [índices], color, apagar (at): el resto se vuelve gris."""

    def prep(s):
        sp = s.sp
        s.n, s.cols, s.sep = sp.get("n", 10), sp.get("cols", 5), sp.get("sep", 150)
        s.dest = set(sp.get("destacar", []))
        s.t_apaga = resuelve(sp["apagar"], s.pl) if "apagar" in sp else None
        s.anim = "none"

    def sonidos(s):
        return [(s.t0 + i * 0.06, "pop", {"pitch": 0.9 + 0.05 * i}) for i in range(0, s.n, 2)]

    def pinta(s, cv, t, al):
        rows = math.ceil(s.n / s.cols)
        for i in range(s.n):
            r, c = divmod(i, s.cols)
            x = (c - (s.cols - 1) / 2) * s.sep
            y = (r - (rows - 1) / 2) * s.sep * 1.25
            k = e_back((t - s.t0 - i * 0.06) / 0.25)
            if k <= 0:
                continue
            col = s.sp.get("color", "blue")
            if s.t_apaga is not None and t > s.t_apaga and i not in s.dest:
                col = D.mezcla(col, "light", clamp((t - s.t_apaga) / 0.3))
            if i in s.dest and s.t_apaga is not None and t > s.t_apaga:
                k *= 1 + 0.15 * math.sin((t - s.t_apaga) * 10) * math.exp(-(t - s.t_apaga) * 2)
                col = s.sp.get("color_dest", "red")
            cv.save()
            cv.translate(x, y)
            cv.scale(k * s.sep / 150, k * s.sep / 150)
            cv.drawCircle(4, -38, 26, D.p_fill(col, al))
            cv.drawRoundRect(skia.Rect(-38 + 4, -6 + 4, 38 + 4, 64 + 4), 26, 26, D.p_fill(col, al))
            cv.drawCircle(0, -42, 26, D.p_stroke("ink", 6, al))
            cv.drawRoundRect(skia.Rect(-38, -6, 38, 64), 26, 26, D.p_stroke("ink", 6, al))
            cv.restore()


class Barras(El):
    """Barras verticales comparadas. sp: items=[{label, val, color, txt}], w, h (alto máx), max."""

    def prep(s):
        s.anim = "none"
        s.items = s.sp["items"]
        s.mx = s.sp.get("max", max(i["val"] for i in s.items))
        s.fl = D.fuente("num", s.sp.get("px_label", 46))
        s.fv = D.fuente("num", s.sp.get("px_val", 76))

    def sonidos(s):
        return [(s.t0 + i * s.sp.get("escalon", 0.35), "whoosh", {"d": 0.25}) for i in range(len(s.items))] + \
               [(s.t0 + i * s.sp.get("escalon", 0.35) + 0.6, "pop", {"pitch": 0.8}) for i in range(len(s.items))]

    def pinta(s, cv, t, al):
        n = len(s.items)
        ancho = s.sp.get("w", 760)
        hmax = s.sp.get("h", 600)
        bw = ancho / n * 0.62
        cv.drawPath(D.camino([(-ancho / 2 - 20, 0), (ancho / 2 + 20, 0)]), D.p_stroke("ink", 8, al))
        for i, it in enumerate(s.items):
            x = (i - (n - 1) / 2) * ancho / n
            k = e_out((t - s.t0 - i * s.sp.get("escalon", 0.35)) / 0.7)
            h = hmax * it["val"] / s.mx * k
            if h > 0:
                r = skia.Rect(x - bw / 2, -h, x + bw / 2, 0)
                cv.save()
                cv.translate(*D.OFF)
                cv.drawRect(r, D.p_fill(it.get("color", "blue"), al))
                cv.restore()
                cv.drawRect(r, D.p_stroke("ink", 7, al))
                v = it["val"] * k
                txt = it.get("txt", "{v}").format(v=D.fmt_num(v, it.get("dec", 0)))
                D.texto(cv, txt, x, -h - 24, s.fv, it.get("color_txt", "ink"), "white", 12, alpha=al)
            D.texto(cv, it["label"], x, 64, s.fl, "ink", "white", 8, alpha=al)


class Linea(El):
    """Gráfica de línea que se dibuja. sp: datos [[x,y]...], w, h, color, etiquetas {x: texto}, dur, ymax."""

    def prep(s):
        s.anim = "none"
        d = s.sp["datos"]
        xs = [p[0] for p in d]
        ymax = s.sp.get("ymax", max(p[1] for p in d) * 1.1)
        w, h = s.sp.get("w", 820), s.sp.get("h", 520)
        s.pts = [(-w / 2 + w * (x - xs[0]) / (xs[-1] - xs[0]), -h * y / ymax) for x, y in d]
        s.xs = xs
        s.dur = s.sp.get("dur", 2.0)
        s.trazo = D.Trazo(s.pts, s.sp.get("color", "red"), 12, rng=s.rng, amp=0.6)
        s.f = D.fuente("num", s.sp.get("px", 50))
        s.fx = D.fuente("ui", 34)
        s.w, s.h = w, h

    def sonidos(s):
        return [(s.t0, "rotulador", {"d": s.dur})]

    def pinta(s, cv, t, al):
        w, h = s.w, s.h
        cv.drawPath(D.camino([(-w / 2 - 20, 0), (w / 2 + 30, 0)]), D.p_stroke("ink", 7, al))
        u = clamp((t - s.t0) / s.dur)
        s.trazo.dibuja(cv, max(u, 0.001), al)
        n = len(s.pts)
        for i, (x, y) in enumerate(s.pts):
            ti = s.t0 + s.dur * i / (n - 1)
            et = s.sp.get("etiquetas", {}).get(s.xs[i]) or s.sp.get("etiquetas", {}).get(str(s.xs[i]))
            if t >= ti:
                cv.drawCircle(x, y, 11, D.p_fill(s.sp.get("color", "red"), al))
                if et:
                    k = e_back((t - ti) / 0.25)
                    cv.save()
                    cv.translate(x, y - 40)
                    cv.scale(k, k)
                    D.texto(cv, et, 0, 0, s.f, "ink", "white", 12, alpha=al)
                    cv.restore()
                    D.texto(cv, str(s.xs[i]), x, 50, s.fx, "gray", "white", 6, alpha=al)


class Icono(El):
    def prep(s):
        fn = D.ICONOS[s.sp["n"]]
        s.trazos = fn(s.rng, s.sp["color"]) if "color" in s.sp else fn(s.rng)
        s.anim = s.sp.get("anim", "pop")

    def sonidos(s):
        if s.anim == "traza":
            return [(s.t0, "rotulador", {"d": s.sp.get("dur", 0.5)})]
        return super().sonidos()

    def pinta(s, cv, t, al):
        if s.sp.get("flota", True):
            amp = 1.0 if s.sp.get("flota") else 0.45
            cv.translate(0, amp * 10 * math.sin((t - s.t0) * 3 + s.x))
            cv.rotate(amp * 4 * math.sin((t - s.t0) * 2.3 + s.y))
        frac = clamp((t - s.t0) / s.sp.get("dur", 0.5)) if s.anim == "traza" else 1
        D.dibuja_trazos(cv, s.trazos, frac, al)


class Pers(El):
    """Personaje. sp: tipo, cara, pose, sostiene, mira, cambios=[[at, {cara|pose}]], bote, tiembla."""
    entrada = 0.45

    def prep(s):
        s.anim = s.sp.get("anim", "entra_izq" if s.x < 540 else "entra_der")
        s.cambios = [(resuelve(a, s.pl), c) for a, c in s.sp.get("cambios", [])]

    def sonidos(s):
        out = [(s.t0, "whoosh", {"d": 0.3})] if s.anim.startswith("entra") else [(s.t0, "pop", {"pitch": 0.7})]
        for tc, c in s.cambios:
            if c.get("cara") in ("sorpresa", "shock"):
                out.append((tc, "boing", {}))
        return out

    def pinta(s, cv, t, al):
        cara, pose = s.sp.get("cara", "neutral"), s.sp.get("pose", "normal")
        tiembla = s.sp.get("tiembla", False)
        for tc, c in s.cambios:
            if t >= tc:
                cara, pose = c.get("cara", cara), c.get("pose", pose)
                tiembla = c.get("tiembla", tiembla)
        bote = math.sin((t - s.t0) * 5) * 6
        cv.translate(0, bote)
        if tiembla:
            cv.translate(math.sin(t * 70) * 5, 0)
        if s.sp.get("tipo") == "hucha":
            P.dibuja_hucha(cv, t, cara)
        else:
            P.dibuja_personaje(cv, s.sp.get("tipo", "ciudadano"), t, cara, pose, s.sp.get("sostiene"), s.sp.get("mira", 1))
        if s.sp.get("rotulo"):
            D.texto(cv, s.sp["rotulo"], 0, 215, D.fuente("num", s.sp.get("px_rotulo", 44)), s.sp.get("color_rotulo", "ink"), "white", 10)


class Dinero(El):
    """Billetes volando. sp: modo (lluvia|fuga|explota), n, desde [x,y], hacia [x,y], dur."""

    def prep(s):
        s.anim = "none"
        n = s.sp.get("n", 18)
        r = s.rng
        s.parts = [(r.uniform(-1, 1), r.uniform(-1, 1), r.uniform(0, 0.5), r.uniform(-400, 400), r.uniform(0.6, 1.1)) for _ in range(n)]
        s.bill = D.ico_billete(r)

    def sonidos(s):
        return [(s.t0, "caja", {}), (s.t0, "whoosh", {"d": 0.5})]

    def pinta(s, cv, t, al):
        modo = s.sp.get("modo", "lluvia")
        dur = s.sp.get("dur", 1.6)
        for a, b, delay, spin, sc in s.parts:
            u = (t - s.t0 - delay) / dur
            if u < 0 or u > 1.2:
                continue
            if modo == "lluvia":
                x, y = a * 520, -800 + u * 1900 + b * 150
            elif modo == "explota":
                x, y = a * 700 * e_out(u), b * 500 * e_out(u) + 900 * u * u
            else:  # fuga: de 'desde' a 'hacia'
                (x0, y0), (x1, y1) = s.sp.get("desde", [0, 0]), s.sp.get("hacia", [0, -900])
                x = x0 + (x1 - x0) * e_inout(u) + a * 120 * math.sin(u * 6)
                y = y0 + (y1 - y0) * e_inout(u) + b * 80
            cv.save()
            cv.translate(x, y)
            cv.rotate(spin * u)
            cv.scale(sc * 0.75, sc * 0.75 * (0.6 + 0.4 * abs(math.cos(u * 8 + a * 5))))
            D.dibuja_trazos(cv, s.bill, 1.0, al)
            cv.restore()


class Marca(El):
    """Anotación de rotulador: circulo (rx, ry), tacha (w), subraya (w), flecha (de, a)."""

    def prep(s):
        s.anim = "none"
        k, c = s.sp["k"], s.sp.get("color", "red")
        r = s.rng
        if k == "circulo":
            pts = D.elipse(0, 0, s.sp.get("rx", 200), s.sp.get("ry", 90), -100, 380)
            s.trazos = [D.Trazo(pts, c, 10, rng=r, amp=3)]
        elif k == "tacha":
            w, h = s.sp.get("w", 400), s.sp.get("h", 60)
            s.trazos = [D.Trazo([(-w / 2, h / 2), (w / 2, -h / 2)], c, 14, rng=r, amp=2),
                        D.Trazo([(-w / 2, -h / 2), (w / 2, h / 2)], c, 14, rng=r, amp=2)]
        elif k == "subraya":
            w = s.sp.get("w", 400)
            s.trazos = [D.Trazo([(-w / 2, 0), (w / 2, -6)], c, 12, rng=r, amp=2), D.Trazo([(-w / 2 + 20, 18), (w / 2 - 10, 12)], c, 9, rng=r, amp=2)]
        elif k == "flecha":
            (x0, y0), (x1, y1) = s.sp["de"], s.sp["a"]
            s.x, s.y = 0, 0
            nx, ny = -(y1 - y0) * 0.15, (x1 - x0) * 0.15
            cx, cy = (x0 + x1) / 2 + nx, (y0 + y1) / 2 + ny
            ts = np.linspace(0, 1, 30)
            body = [((1 - u) ** 2 * x0 + 2 * (1 - u) * u * cx + u * u * x1, (1 - u) ** 2 * y0 + 2 * (1 - u) * u * cy + u * u * y1) for u in ts]
            ang = math.atan2(body[-1][1] - body[-4][1], body[-1][0] - body[-4][0])
            h1 = (x1 + 40 * math.cos(ang + 2.6), y1 + 40 * math.sin(ang + 2.6))
            h2 = (x1 + 40 * math.cos(ang - 2.6), y1 + 40 * math.sin(ang - 2.6))
            s.trazos = [D.Trazo(body, c, 11, rng=r, amp=1.5), D.Trazo([h1, (x1, y1), h2], c, 11, rng=r, amp=0.5)]
        s.dur = s.sp.get("dur", 0.4)

    def sonidos(s):
        return [(s.t0, "rotulador", {"d": s.dur})]

    def pinta(s, cv, t, al):
        D.dibuja_trazos(cv, s.trazos, clamp((t - s.t0) / s.dur), al)


class Estallido(El):
    def prep(s):
        s.anim = s.sp.get("anim", "pop")

    def pinta(s, cv, t, al):
        _estallido(cv, 0, 0, s.sp.get("r", 300), s.sp.get("color", "yellow"), t, al, s.sp.get("puntas", 14))


class Bocadillo(El):
    """Bocadillo de diálogo. sp: t (con \\n), w, cola [dx, dy], px, color."""

    def prep(s):
        s.f = D.fuente(s.sp.get("fuente", "mano"), s.sp.get("px", 58))

    def pinta(s, cv, t, al):
        ls = s.sp["t"].split("\n")
        px = s.f.getSize()
        w = s.sp.get("w", max(s.f.measureText(x) for x in ls) + 70)
        h = len(ls) * px * 1.1 + 50
        cdx, cdy = s.sp.get("cola", [-80, h / 2 + 60])
        p = skia.Path()
        p.addRoundRect(skia.Rect(-w / 2, -h / 2, w / 2, h / 2), 40, 40)
        tri = skia.Path()
        tri.moveTo(-30, h / 2 - 10)
        tri.lineTo(cdx, cdy)
        tri.lineTo(30, h / 2 - 10)
        tri.close()
        p = skia.Op(p, tri, skia.PathOp.kUnion_PathOp) or p
        cv.save()
        cv.translate(*D.OFF)
        cv.drawPath(p, D.p_fill(s.sp.get("color", "yellow"), al))
        cv.restore()
        cv.drawPath(p, D.p_fill("white", al))
        cv.drawPath(p, D.p_stroke("ink", 7, al))
        y = -h / 2 + 25 + px * 0.85
        for ln in ls:
            D.texto(cv, ln, 0, y, s.f, s.sp.get("color_txt", "ink"), None, 0, alpha=al)
            y += px * 1.1


class Medidor(El):
    """Barra de progreso «prometido vs cumplido». sp: val, max, w, color, etiqueta, txt."""

    def prep(s):
        s.anim = "none"
        s.f = D.fuente("num", s.sp.get("px", 64))

    def sonidos(s):
        return [(s.t0, "contador", {"d": s.sp.get("dur", 1.2)}), (s.t0 + s.sp.get("dur", 1.2), "error", {})]

    def pinta(s, cv, t, al):
        w, h = s.sp.get("w", 840), s.sp.get("h", 110)
        u = clamp((t - s.t0) / s.sp.get("dur", 1.2))
        k = s.sp["val"] / s.sp.get("max", 100)
        # primero amaga con llenarse y luego se queda en el valor real
        f = k * e_out(u) if not s.sp.get("amago") else (min(1, u * 2.2) * 0.35 if u < 0.45 else 0.35 + (k - 0.35) * e_out((u - 0.45) / 0.55))
        r = skia.Rect(-w / 2, -h / 2, w / 2, h / 2)
        cv.drawRoundRect(r, h / 2, h / 2, D.p_fill("white", al))
        if f > 0:
            cv.save()
            cv.clipRRect(skia.RRect.MakeRectXY(r, h / 2, h / 2))
            cv.drawRect(skia.Rect(-w / 2, -h / 2, -w / 2 + w * f, h / 2), D.p_fill(s.sp.get("color", "red"), al))
            cv.restore()
        cv.drawRoundRect(r, h / 2, h / 2, D.p_stroke("ink", 8, al))
        if s.sp.get("etiqueta"):
            D.texto(cv, s.sp["etiqueta"], -w / 2, -h / 2 - 26, D.fuente("num", 44), "ink", "white", 8, alinea="i", alpha=al)
        if u >= 1 and s.sp.get("txt"):
            kk = e_back((t - s.t0 - s.sp.get("dur", 1.2)) / 0.25)
            cv.save()
            cv.translate(-w / 2 + w * f + 20, h / 2 + 100)
            cv.scale(kk, kk)
            D.texto(cv, s.sp["txt"], 60, 0, s.f, s.sp.get("color", "red"), "white", 14, alpha=al)
            cv.restore()


class Panel(El):
    """Panel de color con título (para comparaciones lado a lado). sp: w, h, color, t, px."""

    def prep(s):
        s.f = D.fuente("num", s.sp.get("px", 54))

    def pinta(s, cv, t, al):
        w, h = s.sp.get("w", 460), s.sp.get("h", 700)
        r = skia.Rect(-w / 2, -h / 2, w / 2, h / 2)
        cv.save()
        cv.translate(*D.OFF)
        cv.drawRoundRect(r, 30, 30, D.p_fill(s.sp.get("color", "yellow"), int(al * 0.9)))
        cv.restore()
        cv.drawRoundRect(r, 30, 30, D.p_stroke("ink", 7, al))
        if s.sp.get("t"):
            D.texto(cv, s.sp["t"], 0, -h / 2 + s.f.getSize() + 20, s.f, s.sp.get("color_txt", "ink"), "white", 10, alpha=al)


class Burbujas(El):
    """Lluvia de anuncios: etiquetas que caen y se amontonan. sp: items [texto], px, colores."""

    def prep(s):
        s.anim = "none"
        s.f = D.fuente("num", s.sp.get("px", 60))
        r = s.rng
        n = len(s.sp["items"])
        s.pos = [((-1) ** i * r.uniform(60, 250), -430 + 860 * i / max(1, n - 1) + r.uniform(-25, 25), r.uniform(-12, 12)) for i in range(n)]

    def sonidos(s):
        return [(s.t0 + i * s.sp.get("escalon", 0.18), "pop", {"pitch": 1 + 0.06 * i}) for i in range(len(s.sp["items"]))]

    def pinta(s, cv, t, al):
        cols = s.sp.get("colores", ["yellow", "orange", "pink", "teal", "light"])
        for i, (txt, (x, y, rot)) in enumerate(zip(s.sp["items"], s.pos)):
            k = e_back((t - s.t0 - i * s.sp.get("escalon", 0.18)) / 0.25)
            if k <= 0:
                continue
            cv.save()
            cv.translate(x, y)
            cv.rotate(rot)
            cv.scale(k, k)
            w = s.f.measureText(txt) + 50
            hh = s.f.getSize() * 1.35
            r = skia.Rect(-w / 2, -hh / 2, w / 2, hh / 2)
            cv.save()
            cv.translate(*D.OFF)
            cv.drawRoundRect(r, 20, 20, D.p_fill(cols[i % len(cols)], al))
            cv.restore()
            cv.drawRoundRect(r, 20, 20, D.p_fill("white", al))
            cv.drawRoundRect(r, 20, 20, D.p_stroke("ink", 6, al))
            D.texto(cv, txt, 0, s.f.getSize() * 0.36, s.f, "ink", None, 0, alpha=al)
            cv.restore()


class Encuesta(El):
    """Encuesta para comentar: pregunta, dos tarjetas A/B y cartel «COMENTA A o B». Coordenadas absolutas.
    sp: pregunta, a, b, color_a, color_b, at (pregunta), at_a, at_b, at_c (cartel)."""

    def prep(s):
        s.anim, s.x, s.y = "none", 0, 0
        sp, pl = s.sp, s.pl
        s.ta = resuelve(sp["at_a"], pl) if "at_a" in sp else s.t0 + 0.4
        s.tb = resuelve(sp["at_b"], pl) if "at_b" in sp else s.ta + 0.4
        s.tc = resuelve(sp["at_c"], pl) if "at_c" in sp else s.tb + 0.6
        s.fq = D.fuente("num", sp.get("px", 74))
        s.fl = D.fuente("num", 66)
        s.fb = D.fuente("num", 96)
        s.fc = D.fuente("num", 72)

    def golpes(s):
        return [(s.tc + 0.1, 0.8)]

    def sonidos(s):
        return [(s.t0, "pop", {"pitch": 0.9}), (s.ta, "pop", {"pitch": 1.1}), (s.tb, "pop", {"pitch": 1.3}),
                (s.tc + 0.05, "sello", {})]

    def _tarjeta(s, cv, t, t0, y, letra, txt, col):
        k = e_back((t - t0) / 0.3)
        if k <= 0:
            return
        w, h = 820, 180
        # tras el cartel, las tarjetas laten por turnos
        lat = 1 + 0.035 * max(0, math.sin((t - s.tc) * 5 - (0 if letra == "A" else math.pi))) if t > s.tc + 0.3 else 1
        cv.save()
        cv.translate(540, y)
        cv.scale(k * lat, k * lat)
        r = skia.Rect(-w / 2, -h / 2, w / 2, h / 2)
        cv.save()
        cv.translate(14, 14)
        cv.drawRoundRect(r, 34, 34, D.p_fill(col))
        cv.restore()
        cv.drawRoundRect(r, 34, 34, D.p_fill("white"))
        cv.drawRoundRect(r, 34, 34, D.p_stroke("ink", 8))
        cx = -w / 2 + 110
        cv.drawCircle(cx, 0, 72, D.p_fill(col))
        cv.drawCircle(cx, 0, 72, D.p_stroke("ink", 7))
        D.texto(cv, letra, cx, s.fb.getSize() * 0.36, s.fb, "white", "ink", 10)
        lim = w - 260
        tw = s.fl.measureText(txt)
        cv.save()
        x0 = cx + 110
        if tw > lim:
            cv.translate(x0, 0)
            cv.scale(lim / tw, lim / tw)
            x0 = 0
        D.texto(cv, txt, x0, s.fl.getSize() * 0.36, s.fl, "ink", None, 0, alinea="i")
        cv.restore()
        cv.restore()

    def pinta(s, cv, t, al):
        # pregunta
        k = e_back((t - s.t0) / 0.3)
        if k > 0:
            lineas = s.sp["pregunta"].split("\n")
            px = s.fq.getSize()
            cv.save()
            cv.translate(540, 420)
            cv.scale(k, k)
            for i, ln in enumerate(lineas):
                D.texto(cv, ln, 0, (i - (len(lineas) - 1) / 2) * px * 1.1 + px * 0.35, s.fq, "ink", "white", 14)
            cv.restore()
        s._tarjeta(cv, t, s.ta, 640, "A", s.sp["a"], s.sp.get("color_a", "red"))
        s._tarjeta(cv, t, s.tb, 870, "B", s.sp["b"], s.sp.get("color_b", "blue"))
        # cartel
        u = (t - s.tc) / 0.25
        if u > 0:
            k = 1 + 1.2 * (1 - e_out(min(1, u * 1.4)))
            k *= 1 + 0.05 * math.sin((t - s.tc) * 7) if u > 1.5 else 1
            cv.save()
            cv.translate(540, 1100)
            cv.rotate(-3)
            cv.scale(k, k)
            txt = "COMENTA  A  o  B"
            w = s.fc.measureText(txt) + 90
            r = skia.Rect(-w / 2, -66, w / 2, 66)
            a = int(255 * clamp(u * 3))
            cv.drawRoundRect(r, 66, 66, D.p_fill("ink", a))
            cv.drawRoundRect(r, 66, 66, D.p_stroke("yellow", 8, a))
            D.texto(cv, txt, 0, s.fc.getSize() * 0.36, s.fc, "yellow", None, 0, alpha=a)
            cv.restore()
            # flecha que rebota hacia los comentarios
            dy = 18 * abs(math.sin((t - s.tc) * 6))
            y = 1195 + dy
            pa = D.p_stroke("ink", 12, a)
            cv.drawLine(540, y, 540, y + 60, pa)
            cv.drawLine(510, y + 32, 540, y + 62, pa)
            cv.drawLine(570, y + 32, 540, y + 62, pa)


TIPOS_EL = {"num": Num, "txt": Txt, "sello": Sello, "gente": Gente, "barras": Barras, "linea": Linea, "icono": Icono,
            "pers": Pers, "dinero": Dinero, "circulo": Marca, "tacha": Marca, "subraya": Marca, "flecha": Marca,
            "estallido": Estallido, "bocadillo": Bocadillo, "medidor": Medidor, "panel": Panel, "burbujas": Burbujas,
            "encuesta": Encuesta}


# ================================================================== cámara
def camara(pl, t, golpes):
    """Matriz de cámara del plano: escala, desplazamiento y sacudidas."""
    cam = pl.sp.get("cam", "empuja")
    u = (t - pl.ini) / max(0.1, pl.fin - pl.ini)
    s, dx, dy, rot = 1.0, 0.0, 0.0, 0.0
    if cam == "golpe":          # entra muy cerca y se aleja rápido
        s = 1 + 0.35 * (1 - e_out((t - pl.ini) / 0.45)) + 0.04 * u
    elif cam == "empuja":       # acercamiento lento continuo
        s = 1.0 + 0.09 * e_inout(u)
    elif cam == "aleja":
        s = 1.12 - 0.12 * e_inout(u)
    elif cam == "deriva":
        s, dx = 1.06, 40 * math.sin(u * math.pi - math.pi / 2)
    elif cam == "inclina":
        s, rot = 1.05, -2.5 + 5 * e_inout(u)
    # zoom a un punto: "foco": [x, y, escala, at]
    if "foco" in pl.sp:
        fx, fy, fs, fat = pl.sp["foco"]
        k = e_inout((t - resuelve(fat, pl)) / 0.5)
        s *= 1 + (fs - 1) * k
        dx += (540 - fx) * (fs - 1) / fs * k
        dy += (800 - fy) * (fs - 1) / fs * k
    for tg, f in golpes:
        if tg <= t < tg + 0.35:
            a = (1 - (t - tg) / 0.35) ** 2 * 16 * f
            dx += a * math.sin(t * 91)
            dy += a * math.cos(t * 73)
            s *= 1 + 0.025 * f * (1 - (t - tg) / 0.35)
    return s, dx, dy, rot


# ================================================================== render
class Render:
    def __init__(s, video, preview=False):
        s.video = video
        s.planos, s.clips, s.dur, s.voz_real = construye(video)
        rng = np.random.default_rng(7)
        for pl in s.planos:
            pl.els = []
            for sp in pl.sp.get("el", []):
                pl.els.append(TIPOS_EL[sp["k"]](sp, pl, video, np.random.default_rng(rng.integers(1 << 30))))
            pl.els.sort(key=lambda e: e.z)
            if pl.els:
                ini = pl.ini + (0.04 if pl.i else 0)
                primero = min(pl.els, key=lambda e: e.t0)
                if primero.t0 > ini + 0.3:
                    primero.t0 = ini
            pl.golpes = [g for e in pl.els for g in e.golpes()]
            if video.get("duro"):   # modo duro: sacudidas más fuertes
                pl.golpes = [(tg, f * 2.2) for tg, f in pl.golpes]
        s.fondo = s._fondo()
        s.fcap = D.fuente("num", 80)
        s.flogo = D.fuente("num", 30)
        s.ffuente = D.fuente("ui", 28)
        s.acento = video.get("acento", "red")
        s.claves = [norm(c) for c in video.get("claves", [])]

    def _fondo(s):
        rng = np.random.default_rng(3)
        base = np.array(D.PAL["papel"], np.float32)
        n = rng.normal(0, 3.2, (H // 4, W // 4)).repeat(4, 0).repeat(4, 1)
        img = np.clip(base[None, None, :] + n[:, :, None], 0, 255)
        # viñeta suave
        yy, xx = np.mgrid[0:H, 0:W]
        v = 1 - 0.07 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
        img = (img * v[:, :, None]).astype(np.uint8)
        rgba = np.dstack([img, np.full((H, W), 255, np.uint8)])
        return skia.Image.fromarray(rgba, colorType=skia.kRGBA_8888_ColorType)

    # ---------------------------------------------------- plano
    def pinta_plano(s, cv, pl, t):
        cv.drawImage(s.fondo, 0, 0)
        # cuadrícula de pizarra muy suave
        p = D.p_stroke("light", 2, 110)
        for y in range(0, H, 90):
            cv.drawLine(0, y, W, y, p)
        sc, dx, dy, rot = camara(pl, t, pl.golpes)
        s.fondo_plano(cv, pl, t)
        cv.save()
        cv.translate(W / 2 + dx, 790 + dy)
        cv.rotate(rot)
        cv.scale(sc * ESC, sc * ESC)
        cv.translate(-W / 2, -760)
        for e in pl.els:
            e.dibuja(cv, t)
        cv.restore()

    def fondo_plano(s, cv, pl, t):
        """Fondo de color del plano: rayos, mancha o liso (por defecto alterna)."""
        tipo = pl.sp.get("fondo")
        if tipo is None:
            tipo = "rayos" if pl.sp.get("cam") == "golpe" else ("mancha" if pl.i % 2 else "liso")
        col = pl.sp.get("fondo_color", s.acento)
        u = t - pl.ini
        if tipo == "rayos":
            cx, cy = W / 2, 760
            p = skia.Path()
            for k in range(18):
                a0 = math.radians(u * 12 + k * 20)
                a1 = a0 + math.radians(10)
                p.moveTo(cx, cy)
                p.lineTo(cx + 2000 * math.cos(a0), cy + 2000 * math.sin(a0))
                p.lineTo(cx + 2000 * math.cos(a1), cy + 2000 * math.sin(a1))
                p.close()
            cv.drawPath(p, D.p_fill(col, 34))
        elif tipo == "mancha":
            r = 470 + 12 * math.sin(u * 2)
            cv.drawCircle(W / 2 + 10, 770, r, D.p_fill(col, 40))
            cv.drawCircle(W / 2, 760, r, D.p_stroke(col, 5, 90))
        elif tipo == "color":
            cv.drawRect(skia.Rect(0, 0, W, H), D.p_fill(col, 60))

    def plano_en(s, t):
        for i, pl in enumerate(s.planos):
            if t < pl.fin:
                return i
        return len(s.planos) - 1

    def frame(s, cv, t):
        i = s.plano_en(t)
        pl = s.planos[i]
        # transición de entrada al plano i (centrada en pl.ini) o de salida hacia i+1
        sig = s.planos[i + 1] if i + 1 < len(s.planos) else None
        if sig is not None and t > pl.fin - TRANS / 2:
            s.transicion(cv, pl, sig, t, (t - (pl.fin - TRANS / 2)) / TRANS)
        elif i > 0 and t < pl.ini + TRANS / 2:
            s.transicion(cv, s.planos[i - 1], pl, t, (t - (pl.ini - TRANS / 2)) / TRANS)
        else:
            s.pinta_plano(cv, pl, t)
        if s.video.get("duro"):
            s.flash_duro(cv, pl, t)
        s.hud(cv, t, pl)

    def flash_duro(s, cv, pl, t):
        """Modo duro: destello rojo y marco en cada golpe."""
        k = 0.0
        for tg, f in pl.golpes:
            if tg <= t < tg + 0.3:
                k = max(k, 1 - (t - tg) / 0.3)
        if pl.sp.get("cam") == "golpe" and t < pl.ini + 0.3:
            k = max(k, 1 - (t - pl.ini) / 0.3)
        if k <= 0:
            return
        cv.drawRect(skia.Rect(0, 0, W, H), D.p_fill("red", int(70 * k)))
        cv.drawRect(skia.Rect(0, 0, W, H), D.p_stroke("red", 60 * k + 1, int(230 * k)))

    def _snap(s, pl, t):
        surf = skia.Surface(W, H)
        s.pinta_plano(surf.getCanvas(), pl, t)
        return surf.makeImageSnapshot()

    def transicion(s, cv, a, b, t, p):
        p = clamp(p)
        tipo = b.sp.get("trans", "barrido")
        ia = s._snap(a, min(t, a.fin - 1e-3))
        ib = s._snap(b, max(t, b.ini))
        if tipo == "corte":
            cv.drawImage(ia if p < 0.5 else ib, 0, 0)
            return
        if tipo == "barrido":   # whip pan con desenfoque de movimiento
            k = e_inout(p)
            blur = skia.Paint(ImageFilter=skia.ImageFilters.Blur(60 * math.sin(math.pi * p) + 0.01, 0.01))
            cv.drawImage(ia, -W * k, 0, paint=blur)
            cv.drawImage(ib, W * (1 - k), 0, paint=blur)
        elif tipo == "sube":
            k = e_inout(p)
            blur = skia.Paint(ImageFilter=skia.ImageFilters.Blur(0.01, 60 * math.sin(math.pi * p) + 0.01))
            cv.drawImage(ia, 0, -H * k, paint=blur)
            cv.drawImage(ib, 0, H * (1 - k), paint=blur)
        elif tipo == "zoom":
            cv.save()
            k = e_inout(p)
            sc = 1 + 2.2 * k
            cv.translate(W / 2, 800)
            cv.scale(sc, sc)
            cv.translate(-W / 2, -800)
            cv.drawImage(ia, 0, 0, paint=skia.Paint(Alphaf=1 - k))
            cv.restore()
            cv.save()
            sc = 0.5 + 0.5 * k
            cv.translate(W / 2, 800)
            cv.scale(sc, sc)
            cv.translate(-W / 2, -800)
            cv.drawImage(ib, 0, 0, paint=skia.Paint(Alphaf=k))
            cv.restore()
        elif tipo == "flash":
            cv.drawImage(ia if p < 0.5 else ib, 0, 0)
            cv.drawRect(skia.Rect(0, 0, W, H), D.p_fill("white", int(255 * (1 - abs(2 * p - 1)))))
        elif tipo == "tinta":   # una mancha de rotulador barre la pantalla
            cv.drawImage(ia, 0, 0)
            band = skia.Path()
            x = -400 + (W + 800) * e_inout(p)
            band.moveTo(x - 300, -100)
            band.lineTo(x + 100, -100)
            band.lineTo(x - 200, H + 100)
            band.lineTo(x - 600, H + 100)
            band.close()
            rev = skia.Path()
            rev.moveTo(-1000, -100)
            rev.lineTo(x - 300, -100)
            rev.lineTo(x - 600, H + 100)
            rev.lineTo(-1000, H + 100)
            rev.close()
            cv.save()
            cv.clipPath(rev, skia.ClipOp.kIntersect, True)
            cv.drawImage(ib, 0, 0)
            cv.restore()
            cv.drawPath(band, D.p_fill(s.acento))

    # ---------------------------------------------------- capa fija: subtítulos, logo, barra
    def hud(s, cv, t, pl):
        # barra de progreso
        cv.drawRect(skia.Rect(0, 0, W * t / s.dur, 12), D.p_fill(s.acento))
        # logo
        r = skia.Rect(48, 150, 48 + 300, 150 + 54)
        cv.drawRoundRect(r, 12, 12, D.p_fill("ink"))
        cv.drawString("PIZARRA PÚBLICA", 66, 188, s.flogo, D.p_fill("yellow"))
        serie = s.video.get("serie")
        if serie:
            f = D.fuente("ui", 26)
            cv.drawString(serie, 52, 238, f, D.p_fill("ink"))
        # fuente del dato
        sin_subs = getattr(s, "sin_subs", False) or s.video.get("sin_subs")
        fu = None if sin_subs else pl.sp.get("fuente")
        if fu:
            txt = "Fuente: " + fu
            w = s.ffuente.measureText(txt)
            r = skia.Rect(W / 2 - w / 2 - 22, 1262, W / 2 + w / 2 + 22, 1308)
            cv.drawRoundRect(r, 23, 23, D.p_fill("white", 235))
            cv.drawRoundRect(r, 23, 23, D.p_stroke("gray", 3))
            cv.drawString(txt, W / 2 - w / 2, 1295, s.ffuente, D.p_fill("gray"))
        if not sin_subs:
            s.subtitulos(cv, t)

    def trozos(s):
        if hasattr(s, "_tr"):
            return s._tr
        out = []
        for pl in s.planos:
            for ln in pl.lineas:
                cur = []
                for w, a, b in ln["pals"]:
                    cur.append((w, a, b))
                    txt = " ".join(x[0] for x in cur)
                    if len(cur) >= 3 or len(txt) >= 15 or re.search(r"[.,:;?!…]$", w):
                        out.append(cur)
                        cur = []
                if cur:
                    out.append(cur)
        s._tr = out
        return out

    def subtitulos(s, cv, t):
        tr = s.trozos()
        act = None
        for i, c in enumerate(tr):
            fin = tr[i + 1][0][1] if i + 1 < len(tr) and tr[i + 1][0][1] - c[-1][2] < 0.6 else c[-1][2] + 0.25
            if c[0][1] - 0.04 <= t < fin:
                act = c
                break
        if not act:
            return
        f = s.fcap
        words = [w for w, a, b in act]
        sp = f.measureText(" ")
        ws = [f.measureText(w) for w in words]
        total = sum(ws) + sp * (len(ws) - 1)
        k = e_back((t - act[0][1] + 0.04) / 0.12, 2.4)
        cv.save()
        cv.translate(W / 2, CAP_Y)
        cv.scale(0.85 + 0.15 * k, 0.85 + 0.15 * k)
        x = -total / 2
        for (w, a, b), ww in zip(act, ws):
            hablando = a - 0.03 <= t
            nw = norm(w)
            clave = any(ch.isdigit() for ch in w) or any(nw.startswith(c) for c in s.claves if c)
            if hablando and t < b + 0.05:
                cv.drawRoundRect(skia.Rect(x - 12, -62, x + ww + 12, 18), 14, 14, D.p_fill("yellow"))
            col = s.acento if clave else "ink"
            al = 255 if hablando else 120
            cv.drawString(w, x, 0, f, D.p_stroke("white", 14, al))
            cv.drawString(w, x, 0, f, D.p_fill(col, al))
            x += ww + sp
        cv.restore()


# ================================================================== audio
def mezcla_audio(r, path):
    dur = r.dur + 0.6
    n = int(S.SR * dur)
    voz = np.zeros(n, np.float32)
    for t0, pcm in r.clips:
        i = int(t0 * S.SR)
        m = min(len(pcm), n - i)
        voz[i:i + m] += pcm[:m]
    if np.abs(voz).max() > 0:
        voz *= 0.9 / np.abs(voz).max()
    silencios = []
    for pl in r.planos:
        if pl.sp.get("pausa"):
            silencios.append((pl.ini, pl.ini + pl.sp["pausa"] + 0.05))
    mcfg = r.video.get("musica", {})
    mus = S.musica(dur, mcfg.get("bpm", 104), mcfg.get("tono", 0), mcfg.get("seed", 1), silencios)
    # duck: baja la música cuando hay voz
    env = np.convolve(np.abs(voz), np.ones(2205) / 2205, mode="same")
    duck = 1 - 0.65 * np.clip(env / 0.05, 0, 1)
    mus = mus[:n] * duck[: len(mus)] * mcfg.get("vol", 0.42)
    fx = np.zeros(n, np.float32)
    seed = 0
    eventos = []
    for pl in r.planos:
        for e in pl.els:
            eventos += e.sonidos()
        for at, nombre in pl.sp.get("sfx", []):
            eventos.append((resuelve(at, pl), nombre, {}))
        if pl.i > 0 and pl.sp.get("trans", "barrido") != "corte":
            eventos.append((pl.ini - TRANS / 2, "whoosh", {"d": TRANS + 0.05}))
        if pl.sp.get("pausa"):
            eventos.append((pl.ini + pl.sp["pausa"], "impacto", {"fuerza": 1.0}))
    gan = {"pop": 0.5, "whoosh": 0.45, "impacto": 0.9, "sello": 0.9, "contador": 0.5, "caja": 0.5, "rotulador": 0.45,
           "subida": 0.55, "error": 0.5, "ding": 0.5, "boing": 0.35, "glitch": 0.45, "tick": 0.4}
    for t0, nombre, kw in eventos:
        seed += 1
        sig = S.contador(seed=seed, **kw) if nombre == "contador" else S.efecto(nombre, seed=seed, **kw)
        i = int(max(0, t0) * S.SR)
        m = min(len(sig), n - i)
        if m > 0:
            fx[i:i + m] += sig[:m] * gan.get(nombre, 0.5)
    mix = voz + mus + fx * 0.8
    mix = np.tanh(mix * 1.1) * 0.95
    pcm = (mix * 32767).astype(np.int16)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(S.SR), "-ac", "1", "-i", "-", path],
                   input=pcm.tobytes(), check=True)


# ================================================================== vídeo
_R = None


def _init(path, preview):
    global _R
    _R = Render(cargar_video(path), preview)


def _trozo(args):
    i0, i1, fps, out = args
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(fps),
                          "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", out],
                         stdin=subprocess.PIPE)
    surf = skia.Surface(W, H)
    for fi in range(i0, i1):
        cv = surf.getCanvas()
        cv.clear(skia.ColorWHITE)
        _R.frame(cv, fi / fps)
        p.stdin.write(surf.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType).tobytes())
    p.stdin.close()
    p.wait()
    return out


def render(path, out_dir, preview=False, procesos=4):
    video = cargar_video(path)
    r = Render(video, preview)
    if not r.voz_real:
        print("⚠ Faltan voces: se usan tiempos estimados y silencio (ejecuta la acción «Voces v2»).")
    slug = video["slug"]
    os.makedirs(out_dir, exist_ok=True)
    work = os.path.join(out_dir, "_work")
    os.makedirs(work, exist_ok=True)
    fps = 15 if preview else FPS
    nf = int(r.dur * fps) + 1
    cortes = np.linspace(0, nf, procesos + 1).astype(int)
    partes = [(cortes[k], cortes[k + 1], fps, os.path.join(work, f"parte{k}.mp4")) for k in range(procesos)]
    with Pool(procesos, initializer=_init, initargs=(path, preview)) as pool:
        hechos = pool.map(_trozo, partes)
    lista = os.path.join(work, "lista.txt")
    open(lista, "w").write("".join(f"file '{os.path.abspath(h)}'\n" for h in hechos))
    wav = os.path.join(work, "audio.wav")
    mezcla_audio(r, wav)
    mp4 = os.path.join(out_dir, slug + ".mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lista, "-i", wav, "-c:v", "copy",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-shortest",
                    "-movflags", "+faststart", mp4], check=True)
    escribe_srt(r, os.path.join(out_dir, slug + ".srt"))
    json.dump({"duracion": round(r.dur, 2), "voz_real": r.voz_real,
               "planos": [{"i": pl.i, "ini": round(pl.ini, 2), "fin": round(pl.fin, 2), "dur": round(pl.fin - pl.ini, 2),
                           "voz": [ln_text(x) for x in pl.sp.get("voz", [])]} for pl in r.planos]},
              open(os.path.join(out_dir, slug + "_tiempos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    portada(path, os.path.join(out_dir, "portada_" + slug + ".png"))
    print(f"✓ {mp4}  ({r.dur:.1f} s)")
    return mp4, r


def ln_text(x):
    return x["text"] if isinstance(x, dict) else x


def escribe_srt(r, path):
    def ts(t):
        h, m = divmod(int(t), 3600)
        m, s_ = divmod(m, 60)
        return f"{h:02d}:{m:02d}:{s_:02d},{int((t % 1) * 1000):03d}"
    out = []
    k = 1
    for pl in r.planos:
        for ln in pl.lineas:
            txt = " ".join(w for w, a, b in ln["pals"])
            out.append(f"{k}\n{ts(ln['t0'])} --> {ts(ln['t1'])}\n{txt}\n")
            k += 1
    open(path, "w", encoding="utf-8").write("\n".join(out))


def hoja(path, out_png, cada=1.0):
    """Hoja de contactos: un fotograma cada `cada` segundos, para revisar ritmo y composición."""
    r = Render(cargar_video(path))
    ts = np.arange(0.15, r.dur, cada)
    cols = 8
    tw, th = 270, 480
    rows = math.ceil(len(ts) / cols)
    out = skia.Surface(cols * tw, rows * (th + 30))
    oc = out.getCanvas()
    oc.clear(skia.ColorWHITE)
    surf = skia.Surface(W, H)
    f = D.fuente("ui", 22)
    for i, t in enumerate(ts):
        cv = surf.getCanvas()
        cv.clear(skia.ColorWHITE)
        r.frame(cv, t)
        img = surf.makeImageSnapshot()
        x, y = (i % cols) * tw, (i // cols) * (th + 30)
        oc.drawImageRect(img, skia.Rect(x, y, x + tw, y + th), skia.SamplingOptions(skia.FilterMode.kLinear))
        oc.drawString(f"{t:.1f}s", x + 6, y + th + 22, f, D.p_fill("ink"))
    out.makeImageSnapshot().save(out_png, skia.kPNG)
    return out_png


def portada(path, out_png):
    """Portada 1080×1920 (la parte central 1080×1440 es la que se ve en la cuadrícula de Instagram)."""
    video = cargar_video(path)
    r = Render(video)
    r.sin_subs = True
    cfg = video.get("portada", {})
    surf = skia.Surface(W, H)
    cv = surf.getCanvas()
    r.frame(cv, cfg.get("t", 1.4))
    lineas = cfg.get("titulo", video["titulo"]).split("\n")
    f = D.fuente("num", cfg.get("px", 92))
    y = cfg.get("y", 1250)
    for i, ln in enumerate(lineas):
        w = f.measureText(ln)
        k = min(1.0, 960 / w)
        cv.save()
        cv.translate(W / 2, y + i * f.getSize() * 1.12)
        cv.rotate(-2)
        cv.scale(k, k)
        rr = skia.Rect(-w / 2 - 26, -f.getSize() * 0.82, w / 2 + 26, f.getSize() * 0.2)
        cv.drawRoundRect(rr, 16, 16, D.p_fill("ink"))
        cv.drawString(ln, -w / 2, 0, f, D.p_fill("yellow" if i == 0 else "white"))
        cv.restore()
    surf.makeImageSnapshot().save(out_png, skia.kPNG)
    return out_png


def fotograma(path, t, out_png):
    r = Render(cargar_video(path))
    surf = skia.Surface(W, H)
    r.frame(surf.getCanvas(), t)
    surf.makeImageSnapshot().save(out_png, skia.kPNG)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--out", default=os.path.join(HERE, "..", "..", "videos", "datos_incomodos"))
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--hoja", action="store_true")
    ap.add_argument("--t", type=float)
    ap.add_argument("--portada", action="store_true")
    a = ap.parse_args()
    v = cargar_video(a.video)
    out = os.path.join(a.out, v["slug"])
    if a.hoja:
        os.makedirs(out, exist_ok=True)
        print(hoja(a.video, os.path.join(out, "_hoja.png")))
    elif a.portada:
        os.makedirs(out, exist_ok=True)
        print(portada(a.video, os.path.join(out, "portada_" + v["slug"] + ".png")))
    elif a.t is not None:
        os.makedirs(out, exist_ok=True)
        fotograma(a.video, a.t, os.path.join(out, f"_t{a.t:.1f}.png"))
    else:
        render(a.video, out, a.preview)
