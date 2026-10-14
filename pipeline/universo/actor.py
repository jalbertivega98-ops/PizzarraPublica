"""Elementos animados del universo dentro del motor de vídeo (make_video.py / wb.Element).

Tipos de elemento en el storyboard:
  personaje  {"quien": "piz", "x", "y" (= pies en el suelo), "scale", "cara", "pose", "mira", "flip",
              "entra": pop|izq|der|cae|abajo|nada, "habla": true, "objeto": "billete" | {"tipo": ..., ...}}
  edificio   {"edificio": "banco", "x", "y" (= suelo), "scale", "cara", "entra": crece|pop|cae|nada,
              "variante", "trabajadores", "caras_dentro": {"0": "sorpresa"}}
  objeto     {"objeto": "etiqueta", "props": {...}, "x", "y" (= centro), "scale", "rot", "entra": pop|cae|izq|der,
              "flota": true}
  rotulo     {"text", "x", "y", "size", "color", "font": "sub", "rot"}: texto cartoon con contorno

Línea de tiempo «acciones» (también vale «caras»): [{"at": "@palabra", ...}] con cualquiera de
  cara, pose, mira, habla, objeto, props, caras_dentro, flip,
  x / y (+ "dur": anda/se desplaza hasta ahí), salta: true, tiembla: true, sale: izq|der|pop|abajo, sfx.
Idle automático: respiración, parpadeo, balanceo; pop al cambiar de cara; boca sincronizada con la voz.
"""
import math

import skia

from . import edificios, objetos, personajes
from .estilo import texto_cartoon

TIPOS = ("personaje", "edificio", "objeto", "rotulo")
DUR_ENTRA = {"personaje": 0.45, "edificio": 0.55, "objeto": 0.35, "rotulo": 0.3}
PIES = 340  # los pies del personaje están a +340 px del centro de la pizarra (escala 1)
FUERA = 700  # distancia desde la que entra por un lado


def _eo(k):  # ease out
    k = max(0.0, min(1.0, k))
    return 1 - (1 - k) ** 3


def _back(k, s=1.9):  # ease out con rebote (overshoot)
    k = max(0.0, min(1.0, k)) - 1
    return 1 + (s + 1) * k ** 3 + s * k ** 2


def _ease(k):
    k = max(0.0, min(1.0, k))
    return k * k * (3 - 2 * k)


def preparar(e):
    """Se llama tras resolver los tiempos (make_video.build_elements)."""
    s = e.spec
    if "dur" not in s:
        e.dur = DUR_ENTRA[e.kind] if s.get("entra", "pop") != "nada" else 0.0
    e.palabras = getattr(e, "palabras", [])
    # tramos de movimiento: [(t0, t1, x0, y0, x1, y1)]
    x, y = s.get("x", 540), s.get("y", 1300)
    e.tramos = []
    for ch in e.cambios:
        if "x" in ch or "y" in ch:
            nx, ny = ch.get("x", x), ch.get("y", y)
            d = ch.get("dur", max(0.35, abs(nx - x) / 900))
            e.tramos.append((ch["t"], ch["t"] + d, x, y, nx, ny))
            x, y = nx, ny


def _pos(e, t):
    s = e.spec
    x, y = s.get("x", 540), s.get("y", 1300)
    moviendo = False
    for t0, t1, x0, y0, x1, y1 in e.tramos:
        if t >= t1:
            x, y = x1, y1
        elif t >= t0:
            k = _ease((t - t0) / (t1 - t0))
            x, y = x0 + (x1 - x0) * k, y0 + (y1 - y0) * k
            moviendo = True
            break
    return x, y, moviendo


def _vigente(e, t, campo, defecto):
    v, tc, prev = defecto, -1e9, defecto
    for ch in e.cambios:
        if ch["t"] <= t and campo in ch:
            prev, v, tc = v, ch[campo], ch["t"]
    return v, tc, prev


def _habla(e, t):
    on, _, _ = _vigente(e, t, "habla", e.spec.get("habla", False))
    if not on:
        return 0.0
    for w0, w1 in e.palabras:
        if w0 <= t < w1 + 0.04:
            k = (t - w0) / 0.13
            return 0.25 + 0.75 * abs(math.sin(math.pi * k))
    return 0.0


def _parpadeo(e, t):
    nombre = str(e.spec.get("quien", e.spec.get("edificio", ""))) + str(e.spec.get("x", 0))
    sem = (sum(map(ord, nombre)) % 97) / 97
    ph = (t / 3.3 + sem) % 1
    return max(0.0, 1 - abs(ph - 0.5) / 0.025) if abs(ph - 0.5) < 0.025 else 0.0


def _mira(v):
    if isinstance(v, str):
        return {"izq": (-14, 0), "der": (14, 0), "arriba": (0, -12), "abajo": (0, 12), "camara": (0, 0)}.get(v, (0, 0))
    return tuple(v or (0, 0))


def tamano(e):
    s = e.spec
    k = e.kind
    if k == "personaje":
        return 560, 760
    if k == "edificio":
        return edificios.TAMANO.get(s["edificio"], (600, 600))
    if k == "objeto":
        tp = s["objeto"]["tipo"] if isinstance(s["objeto"], dict) else s["objeto"]
        return objetos.TAMANO.get(tp, (300, 300))
    import wb
    f = wb.font(s.get("font", "sub"), s.get("size", 90))
    return f.measureText(s["text"]) + 40, s.get("size", 90) * 1.2


def bbox(e):
    w, h = tamano(e)
    sc = e.spec.get("scale", 1.0)
    w, h = w * sc, h * sc
    x, y, _ = _pos(e, getattr(e, "_t", e.t0 + e.dur))
    if e.kind in ("personaje", "edificio") or (e.kind == "objeto" and _tipo_obj(e) in objetos.APOYADOS):
        return (x - w / 2, y - h, x + w / 2, y)
    return (x - w / 2, y - h / 2, x + w / 2, y + h / 2)


def _tipo_obj(e):
    o = e.spec["objeto"]
    return o["tipo"] if isinstance(o, dict) else o


def _entrada(e, t):
    """(dx, dy, sx, sy, alpha, paso) de la animación de entrada/salida."""
    s = e.spec
    modo = s.get("entra", "crece" if e.kind == "edificio" else "pop")
    dx = dy = 0.0
    sx = sy = 1.0
    a = 1.0
    paso = None
    if e.dur > 0 and t < e.t0 + e.dur and modo != "nada":
        k = (t - e.t0) / e.dur
        if modo == "pop":
            sx = sy = max(0.0, _back(k))
        elif modo == "crece":
            sy = max(0.0, _back(k, 1.4))
            sx = min(1.0, 0.6 + 0.4 * _eo(k * 1.4))
        elif modo in ("izq", "der"):
            lado = -1 if modo == "izq" else 1
            dx = lado * FUERA * (1 - _eo(k))
            paso = k * 3
        elif modo == "cae":
            if k < 0.7:
                dy = -1400 * (1 - (k / 0.7) ** 2)
            else:
                q = (k - 0.7) / 0.3
                sy = 1 - 0.25 * math.sin(math.pi * q)
                sx = 1 + 0.18 * math.sin(math.pi * q)
        elif modo == "abajo":
            dy = 900 * (1 - _eo(k))
    sale, ts, _ = _vigente(e, t, "sale", None)
    if sale:
        k = min(1.0, (t - ts) / 0.45)
        if sale in ("izq", "der"):
            dx += (-1 if sale == "izq" else 1) * 1300 * _ease(k)
            paso = (t - ts) * 3
        elif sale == "abajo":
            dy += 1400 * k * k
        else:
            sx *= 1 - _eo(k)
            sy *= 1 - _eo(k)
        if k >= 1:
            a = 0.0
    return dx, dy, sx, sy, a, paso


def dibujar(e, c, t, am):
    if t < e.t0:
        return None
    e._t = t
    s = e.spec
    sc = s.get("scale", 1.0)
    x, y, moviendo = _pos(e, t)
    dx, dy, sx, sy, a, paso = _entrada(e, t)
    if a <= 0 or sx <= 0 or sy <= 0:
        return None
    # saltos y temblores
    for ch in e.cambios:
        if ch.get("salta") and 0 <= t - ch["t"] < 0.5:
            q = (t - ch["t"]) / 0.5
            dy -= 170 * math.sin(math.pi * q)
            if q < 0.12 or q > 0.88:
                sy *= 0.9; sx *= 1.07
        if ch.get("tiembla") and 0 <= t - ch["t"] < 0.6:
            dx += 14 * math.sin((t - ch["t"]) * 80) * (1 - (t - ch["t"]) / 0.6)
    cara, tc, _ = _vigente(e, t, "cara", s.get("cara"))
    if 0 <= t - tc < 0.22:  # «pop» de reacción: estira y encoge
        q = (t - tc) / 0.22
        sy *= 1 + 0.1 * math.sin(math.pi * q)
        sx *= 1 - 0.05 * math.sin(math.pi * q)
    flip, _, _ = _vigente(e, t, "flip", s.get("flip", False))
    if moviendo and e.kind == "personaje":
        paso = (t - e.t0) * 2.4
    # respiración (idle)
    if e.kind == "personaje":
        b = math.sin(t * 2 * math.pi / 2.4 + (x % 7))
        sy *= 1 + 0.014 * b
        sx *= 1 - 0.007 * b
    alpha = int(255 * am * a)
    c.save()
    c.translate(x + dx, y + dy)
    c.scale(sc * sx * (-1 if flip else 1), sc * sy)
    if s.get("rot"):
        c.rotate(s["rot"])
    if alpha < 255:
        c.saveLayerAlpha(None, alpha)
    if e.kind == "personaje":
        _personaje(e, c, t, cara, tc, paso)
    elif e.kind == "edificio":
        _edificio(e, c, t, cara)
    elif e.kind == "objeto":
        _objeto(e, c, t, cara)
    else:
        texto_cartoon(c, s["text"], 0, s.get("size", 90) * 0.35, s.get("size", 90), color=s.get("color", "amarillo"),
                      fuente=s.get("font", "sub"))
    if alpha < 255:
        c.restore()
    c.restore()
    return None


def _personaje(e, c, t, cara, tc, paso):
    s = e.spec
    pose, tp, pose_prev = _vigente(e, t, "pose", s.get("pose"))
    if pose is None:  # sin pose fija: la pose sigue a la cara
        pose = personajes.BRAZOS_DE.get(cara or "normal", "normal")
        pose_prev = personajes.BRAZOS_DE.get(_vigente(e, tc - 1e-3, "cara", s.get("cara"))[0] or "normal", "normal")
        tp = tc
    pose_prev = pose_prev or personajes.BRAZOS_DE.get(cara or "normal", "normal")
    k_pose = _eo((t - tp) / 0.2) if t - tp < 0.2 else 1.0
    mira, _, _ = _vigente(e, t, "mira", s.get("mira"))
    obj, _, _ = _vigente(e, t, "objeto", s.get("objeto"))
    c.translate(0, -PIES)
    personajes.dibuja(c, s.get("quien", "piz"), cara=cara, pose=pose, pose_prev=pose_prev, k_pose=k_pose,
                      mira=_mira(mira), parpadeo=_parpadeo(e, t), habla=_habla(e, t), paso=paso, t=t, objeto=obj)


def _edificio(e, c, t, cara):
    s = e.spec
    dentro, _, _ = _vigente(e, t, "caras_dentro", s.get("caras_dentro", {}))
    est = {"cara": cara or "normal", "mira": _mira(_vigente(e, t, "mira", s.get("mira"))[0]),
           "parpadeo": _parpadeo(e, t), "habla": _habla(e, t),
           "caras_dentro": {int(k): v for k, v in (dentro or {}).items()}}
    if cara is None:
        est.pop("cara")
    kw = {k: s[k] for k in ("variante", "trabajadores") if k in s}
    edificios.dibuja(c, s["edificio"], est, t, **kw)


def _objeto(e, c, t, cara):
    s = e.spec
    o = s["objeto"]
    kw = dict(o) if isinstance(o, dict) else {"tipo": o}
    kw.update(s.get("props", {}))
    for ch in e.cambios:
        if ch["t"] <= t and "props" in ch:
            kw.update(ch["props"])
    if cara:
        kw["cara"] = cara
    if kw["tipo"] == "grafica" and "progreso" not in kw:
        kw["progreso"] = min(1.0, (t - e.t0) / max(0.3, s.get("dibujo", 1.2)))
    if s.get("flota"):
        c.translate(0, 10 * math.sin(t * 2.6 + e.t0))
    objetos.dibuja(c, kw, t)
