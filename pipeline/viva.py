"""Estilo «viva» del motor de pizarra (docs/enganche.md).

Se activa con "estilo": "viva" en el storyboard y añade, sin tocar los vídeos antiguos:
  · anclas por palabra ("at": "@15,6") con los tiempos reales de la voz,
  · cámara que sigue al trazo y da golpes de zoom,
  · transiciones variadas (borrador, barrido, zoom, papel),
  · efectos de sonido sincronizados y cortes de música,
  · el informe de ritmo <slug>_ritmo.txt.
"""
import math
import os
import re
import sys
import unicodedata

import numpy as np
import skia

import wb
from wb import H, W

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "v2"))
import sonido  # noqa: E402  (efectos generados por código, del motor v2)

TRANSICIONES = ("borrador", "barrido", "zoom", "papel")
DUR_TRANS = {"borrador": 0.36, "barrido": 0.26, "zoom": 0.32, "papel": 0.3, "corte": 0.0}
CENTRO = (W / 2, 820)


def es_viva(story):
    return story.get("estilo") == "viva"


# ------------------------------------------------------------------ palabras
def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    w = "".join(ch for ch in w if unicodedata.category(ch) != "Mn")
    return w.strip("¿?¡!.,:;…«»\"()'")


def estimar_palabras(text, t0, t1):
    """Reparto por número de letras (cuando la voz no trae tiempos por palabra)."""
    words = text.split()
    if not words:
        return []
    weights = np.array([len(w) + 1.5 for w in words], float)
    cum = np.concatenate([[0], np.cumsum(weights)]) / weights.sum()
    return [(w, t0 + cum[i] * (t1 - t0), t0 + cum[i + 1] * (t1 - t0)) for i, w in enumerate(words)]


def palabras_reales(text, al, t0, dur):
    """Ajusta los tiempos de ElevenLabs (palabras de la voz) a las palabras del subtítulo."""
    sub = text.split()
    if not al or len(al) != len(sub):
        if al and len(al) > 1:  # mismas fronteras de tiempo repartidas sobre las palabras del texto
            a, b = al[0]["t0"], al[-1]["t1"]
            return estimar_palabras(text, t0 + a, t0 + min(b, dur))
        return estimar_palabras(text, t0, t0 + dur)
    return [(w, t0 + x["t0"], t0 + min(x["t1"], dur)) for w, x in zip(sub, al)]


def buscar_palabra(scene, palabra, n=1):
    objetivo = norm(palabra)
    hits = []
    for ln in scene["lines"]:
        for w, a, b in ln["words"]:
            nw = norm(w)
            if nw == objetivo or (len(objetivo) >= 4 and nw.startswith(objetivo)):
                hits.append(a)
    if len(hits) < n:
        raise ValueError(f"No encuentro la palabra «{palabra}» (#{n}) en la escena: "
                         + " | ".join(ln["text"] for ln in scene["lines"]))
    return hits[n - 1]


ANCLA = re.compile(r"@(.+?)(?:#(\d+))?([+-]\d*\.?\d+)?$")


def resolver_palabra(at, scene):
    m = ANCLA.fullmatch(at)
    if not m:
        return None
    return buscar_palabra(scene, m.group(1), int(m.group(2) or 1)) + float(m.group(3) or 0)


# ------------------------------------------------------------------ cámara
class Camara:
    """Encuadre que sigue al elemento activo, con golpes de zoom y un leve movimiento constante."""

    def __init__(self):
        self.cx, self.cy, self.z = CENTRO[0], CENTRO[1], 1.0
        self.last_t = None

    def foco(self, t, els):
        best = None
        for e in els:
            if e.hidden(t):
                continue
            activo = e.t0 <= t < e.t0 + e.dur + 0.5
            for t0, d, f in e.fx:
                if t0 <= t < t0 + d + 0.4 and f["do"] != "borrar":
                    activo = True
            if activo and (best is None or e.t0 >= best.t0):
                best = e
        return best

    def update(self, t, els, base_zoom=1.04):
        dt = 1 / 30 if self.last_t is None else max(1e-3, t - self.last_t)
        self.last_t = t
        tx, ty, tz = CENTRO[0], CENTRO[1], base_zoom
        e = self.foco(t, els)
        if e is not None:
            x0, y0, x1, y1 = e.bbox()
            ex, ey = (x0 + x1) / 2, (y0 + y1) / 2
            tx = CENTRO[0] + max(-70, min(70, (ex - CENTRO[0]) * 0.3))
            ty = CENTRO[1] + max(-90, min(60, (ey - CENTRO[1]) * 0.3))
            ancho = max(x1 - x0, (y1 - y0) * 0.56)
            tz = base_zoom + (0.06 if ancho < 450 else 0.03 if ancho < 750 else 0.0)
        a = 1 - math.exp(-dt / 0.45)
        self.cx += (tx - self.cx) * a
        self.cy += (ty - self.cy) * a
        self.z += (tz - self.z) * a
        # golpes: el más reciente manda
        kick, shake = 0.0, 0.0
        for el in els:
            for tg in ([el.t0] if el.spec.get("golpe") else []) + [t0 for t0, d, f in el.fx if f["do"] == "golpe"]:
                if 0 <= t - tg < 0.6:
                    k = math.exp(-(t - tg) / 0.16)
                    kick = max(kick, 0.075 * k)
                    shake = max(shake, 9 * k)
        drift = 0.006 * math.sin(t * 0.9)
        sx = shake * math.sin(t * 83)
        sy = shake * math.cos(t * 71)
        return self.cx + sx, self.cy + sy, self.z + kick + drift

    @staticmethod
    def aplicar(c, cx, cy, z):
        c.translate(CENTRO[0], CENTRO[1])
        c.scale(z, z)
        c.translate(-cx, -cy)


# ------------------------------------------------------------------ transiciones
_SURF = None


def _img(a):
    return skia.Image.fromarray(a, colorType=skia.kRGBA_8888_ColorType)


def mezcla(tipo, prev, cur, k):
    """Fotograma de transición (k de 0 a 1) entre el último de la escena anterior y el actual."""
    global _SURF
    if tipo == "papel":
        off = int(W * (1 - wb.ease(k)))
        out = cur.copy()
        out[:, off:] = cur[:, : W - off]
        if off > 0:
            out[:, :off] = prev[:, W - off:]
        return out
    if _SURF is None:
        _SURF = skia.Surface(W, H)
    c = _SURF.getCanvas()
    pi, ci = _img(prev), _img(cur)
    if tipo == "borrador":
        e = wb.ease(k)
        c.drawImage(ci, 0, 0)
        # la pizarra vieja se borra con pasadas en diagonal
        x = -250 + (W + 500) * e
        path = skia.Path()
        path.moveTo(x, 0)
        for i in range(13):
            y = H * (i + 1) / 13
            path.lineTo(x - 220 * (i % 2) - 120 * (y / H), y)
        path.lineTo(W + 10, H)
        path.lineTo(W + 10, 0)
        path.close()
        c.save()
        c.clipPath(path, skia.ClipOp.kIntersect, True)
        c.drawImage(pi, 0, 0)
        c.restore()
        wb.draw_eraser(c, x - 60, 300 + (H - 700) * ((e * 5) % 1))
    elif tipo == "barrido":
        e = wb.ease(k)
        blur = 60 * math.sin(math.pi * k)
        p = skia.Paint(ImageFilter=skia.ImageFilters.Blur(blur, 0.1)) if blur > 1 else skia.Paint()
        c.clear(wb.rgb("paper"))
        c.drawImage(pi, -W * e, 0, skia.SamplingOptions(), p)
        c.drawImage(ci, W * (1 - e), 0, skia.SamplingOptions(), p)
    elif tipo == "zoom":
        e = wb.ease(k)
        c.clear(wb.rgb("paper"))
        c.save()
        z = 1 + 0.9 * e
        c.translate(CENTRO[0], CENTRO[1]); c.scale(z, z); c.translate(-CENTRO[0], -CENTRO[1])
        c.drawImage(pi, 0, 0, skia.SamplingOptions(), skia.Paint(Alphaf=1 - e))
        c.restore()
        c.save()
        z = 0.82 + 0.18 * e
        c.translate(CENTRO[0], CENTRO[1]); c.scale(z, z); c.translate(-CENTRO[0], -CENTRO[1])
        c.drawImage(ci, 0, 0, skia.SamplingOptions(), skia.Paint(Alphaf=e))
        c.restore()
    else:
        return cur
    return _SURF.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType)


def transicion_de(story, si):
    sc = story["scenes"][si]
    if "trans" in sc:
        return sc["trans"]
    return TRANSICIONES[(si - 1) % len(TRANSICIONES)]


# ------------------------------------------------------------------ subtítulos
def draw_subtitle(c, chunks, t, color="red", y=1505):
    ch = next((ch for ch in chunks if ch["t0"] <= t < ch["t1"]), None)
    if not ch:
        return
    f = wb.font("sub", 76)
    space = f.measureText(" ")
    widths = [f.measureText(w) for w, _, _ in ch["words"]]
    total = sum(widths) + space * (len(widths) - 1)
    x = W / 2 - total / 2
    pop = wb.ease_out((t - ch["t0"]) / 0.1)
    c.save()
    c.translate(W / 2, y)
    c.scale(0.85 + 0.15 * pop, 0.85 + 0.15 * pop)
    c.translate(-W / 2, -y)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - 30, y - 80, x + total + 30, y + 30), 24, 24),
                skia.Paint(Color=skia.Color(255, 255, 255, 240), AntiAlias=True))
    for (w, w0, w1), wd in zip(ch["words"], widths):
        if w0 <= t < w1 + 0.05:
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - 9, y - 70, x + wd + 9, y + 18), 13, 13),
                        skia.Paint(Color=wb.rgb("yellow"), AntiAlias=True))
        col = color if re.search(r"\d", w) else "ink"
        c.drawString(w, x, y, f, skia.Paint(Color=wb.rgb(col), AntiAlias=True))
        x += wd + space
    c.restore()


# ------------------------------------------------------------------ sonido
SFX_VOL = {"pop": 0.22, "impacto": 0.55, "sello": 0.5, "whoosh": 0.35, "contador": 0.25, "borrador": 0.3, "ding": 0.25}


def borrador_snd(d=0.35, seed=0):
    n = int(sonido.SR * d)
    x = np.random.default_rng(seed).uniform(-1, 1, n)
    x = np.convolve(x, np.ones(5) / 5, mode="same")
    t = np.arange(n) / sonido.SR
    env = (0.55 + 0.45 * np.sin(2 * np.pi * 9 * t)) * np.sin(np.pi * t / d) ** 0.7
    return (x * env * 0.7).astype(np.float32)


def eventos_sonido(story, scenes, elements):
    ev = []
    for si, (sc, els) in enumerate(zip(scenes, elements)):
        if si > 0:
            tipo = transicion_de(story, si)
            ev.append((sc["start"], "borrador" if tipo == "borrador" else "whoosh", {}))
        for e in els:
            k = e.kind
            if e.spec.get("golpe"):
                ev.append((e.t0, "impacto", {}))
            elif k == "stamp":
                ev.append((e.t0 + e.dur * 0.6, "sello", {}))
            elif k == "counter":
                ev.append((e.t0, "contador", {"d": e.dur}))
            elif k in ("icon", "tu", "cara", "check", "cross", "circle"):
                ev.append((e.t0, "pop", {"pitch": 0.9 + 0.25 * (len(ev) % 3)}))
            for ch in getattr(e, "cambios", []):
                ev.append((ch["t"], "pop", {"pitch": 1.4}))
            for t0, d, f in e.fx:
                if f["do"] == "borrar":
                    ev.append((t0, "borrador", {"d": d}))
                elif f["do"] == "golpe":
                    ev.append((t0, "impacto", {}))
                elif f["do"] in ("latir", "rodear", "tachar"):
                    ev.append((t0, "pop", {"pitch": 1.2}))
    return ev


def pista_efectos(total, ev, sr):
    out = np.zeros(int(total * sr) + sr, np.float32)
    for t, nombre, kw in ev:
        if nombre == "pop":
            x = sonido.pop(kw.get("pitch", 1.0))
        elif nombre == "impacto":
            x = sonido.impacto(0.8)
        elif nombre == "sello":
            x = sonido.sello()
        elif nombre == "whoosh":
            x = sonido.whoosh(0.3)
        elif nombre == "contador":
            x = sonido.contador(min(kw.get("d", 1.0), 2.0))
        elif nombre == "borrador":
            x = borrador_snd(kw.get("d", 0.35))
        else:
            continue
        a = int(max(0, t) * sr)
        x = x * SFX_VOL.get(nombre, 0.3)
        out[a:a + len(x)] += x[: len(out) - a]
    return out[: int(total * sr)]


def envolvente_musica(story, scenes, total, sr):
    """1 = música normal; 0 en los cortes ("musica": "corte" en la escena: silencio hasta que vuelve la voz)."""
    g = np.ones(int(total * sr), np.float32)
    rampa = int(0.04 * sr)
    for spec, sc in zip(story["scenes"], scenes):
        if spec.get("musica") != "corte" or not sc["lines"]:
            continue
        a, b = int(sc["start"] * sr), int((sc["lines"][-1]["t1"] if spec.get("corte_toda") else sc["lines"][0]["t0"] + 0.05) * sr)
        g[a:b] = 0
        g[max(0, a - rampa):a] = np.linspace(1, 0, len(g[max(0, a - rampa):a]))
        g[b:b + rampa] = np.linspace(0, 1, len(g[b:b + rampa]))
    return g


# ------------------------------------------------------------------ ritmo
def informe_ritmo(story, scenes, elements, total, max_hueco=2.5, max_escena=9.0):
    """Lista de avisos: huecos sin cambios visuales, gancho lento, escenas largas, final sin pregunta."""
    ev = []
    for si, (sc, els) in enumerate(zip(scenes, elements)):
        ev.append((sc["start"], f"escena {story['scenes'][si].get('id', si)}"))
        for e in els:
            ev.append((e.t0, e.kind))
            ev += [(ch["t"], "cara") for ch in getattr(e, "cambios", [])]
            ev += [(t0, f["do"]) for t0, d, f in e.fx]
    ev.sort()
    avisos = []
    primero = min((e.t0 for e in elements[0]), default=9)
    if primero > 0.05:
        avisos.append(f"GANCHO: el primer dibujo aparece en {primero:.2f} s (debe estar en el fotograma 0)")
    if scenes[0]["lines"] and scenes[0]["lines"][0]["t0"] > 0.4:
        avisos.append(f"GANCHO: la voz empieza en {scenes[0]['lines'][0]['t0']:.2f} s (máx. 0,4 s)")
    tiempos = [t for t, _ in ev] + [total - story.get("end_hold", 1.2)]
    for a, b in zip(tiempos[:-1], tiempos[1:]):
        if b - a > max_hueco:
            avisos.append(f"RITMO: {b - a:.1f} s sin cambios visuales entre {a:.1f} y {b:.1f} s")
    for spec, sc in zip(story["scenes"], scenes):
        if sc["end"] - sc["start"] > max_escena:
            avisos.append(f"ESCENA larga: «{spec.get('id')}» dura {sc['end'] - sc['start']:.1f} s (máx. {max_escena:.0f})")
    if total > 60:
        avisos.append(f"DURACIÓN: {total:.1f} s (objetivo 30-45 s)")
    final = " ".join(ln["text"] for ln in scenes[-1]["lines"]).lower()
    if "?" not in final and "síguenos" not in final and "siguenos" not in final:
        avisos.append("FINAL: la última escena no tiene pregunta ni «síguenos»")
    huecos = np.diff(tiempos)
    resumen = (f"Duración {total:.1f} s · {len(ev)} cambios visuales · uno cada {total / max(1, len(ev)):.2f} s de media "
               f"· hueco máximo {huecos.max():.2f} s")
    return resumen, avisos
