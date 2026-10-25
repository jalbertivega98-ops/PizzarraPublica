"""Elementos animados del universo dentro del motor de vídeo (make_video.py / wb.Element).

Tipos de elemento en el storyboard (todos aceptan "id" para que otros los sigan, miren o la cámara los encuadre):
  personaje  {"quien": "piz", "x", "y" (= pies en el suelo), "scale", "cara", "pose", "mira", "flip", "giro",
              "entra": pop|izq|der|cae|abajo|nada, "habla": true, "objeto": "billete" | {"tipo": ..., ...}}
  edificio   {"edificio": "banco", "x", "y" (= suelo), "scale", "cara", "entra": crece|pop|cae|nada, "piernas": true,
              "variante", "trabajadores", "caras_dentro": {"0": "sorpresa"}}
  objeto     {"objeto": "etiqueta", "props": {...}, "x", "y" (= centro), "scale", "rot", "entra": pop|cae|izq|der,
              "flota": true, "piernas": true}
  rotulo     {"text", "x", "y", "size", "color", "font": "sub", "rot"}: texto cartoon con contorno
  efecto     {"efecto": pum|estrellas|lineas|lluvia|vuelan|flash|polvo, ...} (ver universo/efectos.py)

Línea de tiempo «acciones» (también vale «caras»): [{"at": "@palabra", ...}] con cualquiera de
  cara, pose, mira (izq/der/arriba/abajo o el id de otro elemento), giro, habla, objeto, props, caras_dentro, flip,
  x / y (+ "dur"; "corre": true = corre): anda o corre hasta ahí, mirando hacia donde va,
  sigue: id (+ "offset", "lag"): persigue a otro elemento (null = deja de seguir),
  trota: true | "anda" | false: corre o anda sin moverse del sitio (el fondo pasa por detrás),
  salta, take (reacción cartoon: se estira y se le salen los ojos), aplasta (queda plano como una tortita),
  tropieza (cae de bruces, ve estrellas y se levanta), gira (se da la vuelta; con "flip"), tiembla,
  sale: izq|der|pop|abajo, sfx.
Vida automática: respiración, balanceo, parpadeo, brazos que se balancean al andar, inclinación al correr,
polvo al aterrizar y al correr, pop al cambiar de cara, boca sincronizada con la voz.
"""
import math

import skia

from . import edificios, efectos, objetos, personajes
from .estilo import manguera, texto_cartoon

TIPOS = ("personaje", "edificio", "objeto", "rotulo", "efecto")
DUR_ENTRA = {"personaje": 0.45, "edificio": 0.55, "objeto": 0.35, "rotulo": 0.3, "efecto": 0.0}
DUR_ACC = {"salta": 0.55, "take": 0.6, "aplasta": 0.95, "tropieza": 1.6, "gira": 0.3, "tiembla": 0.6}
PIES = 340  # los pies del personaje están a +340 px del centro de la pizarra (escala 1)
FUERA = 700  # distancia desde la que entra por un lado
VEL_ANDA, VEL_CORRE = 430.0, 1000.0  # px/s
FREC_ANDA, FREC_CORRE = 2.2, 3.4  # ciclos de paso por segundo


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
    e.mundo = getattr(e, "mundo", {})
    # tramos de movimiento: [(t0, t1, x0, y0, x1, y1, corre)]
    x, y = s.get("x", 540), s.get("y", 1300)
    e.tramos = []
    e.arcos = []
    for ch in e.cambios:
        if "x" in ch or "y" in ch:
            nx, ny = ch.get("x", x), ch.get("y", y)
            vel = VEL_CORRE if ch.get("corre") else VEL_ANDA
            d = ch.get("dur", max(0.3, math.hypot(nx - x, ny - y) / vel))
            e.tramos.append((ch["t"], ch["t"] + d, x, y, nx, ny, bool(ch.get("corre"))))
            if ch.get("brinco"):  # salto en arco hasta el destino (p. ej. de la península a Ceuta)
                e.arcos.append((ch["t"], ch["t"] + d, float(ch["brinco"])))
            x, y = nx, ny
    # polvo (aterrizajes y carrera) y pasos (para el sonido)
    e.polvo, e.pasos = [], []
    if s.get("entra") == "cae":
        e.polvo.append(e.t0 + e.dur * 0.7)
    for ch in e.cambios:
        if ch.get("salta"):
            e.polvo.append(ch["t"] + 0.47)
        if ch.get("tropieza"):
            e.polvo.append(ch["t"] + 0.32)
        if ch.get("aplasta"):
            e.polvo.append(ch["t"])
    if e.kind in ("personaje",) or s.get("piernas"):
        for t0, t1, *_r, corre in e.tramos:
            f = FREC_CORRE if corre else FREC_ANDA
            n = int((t1 - t0) * f * 2)
            e.pasos += [(t0 + (i + 0.5) / (2 * f), corre) for i in range(n)]
            if corre:
                e.polvo += [t0 + (i + 0.5) / (2 * f) for i in range(0, n, 2)]
        if s.get("entra") in ("izq", "der"):
            e.pasos += [(e.t0 + e.dur * k, False) for k in (0.2, 0.5, 0.8)]


def _sigue(e, t):
    """(id, offset, lag) del elemento al que persigue en el instante t, o None."""
    v, tc, _ = _vigente(e, t, "sigue", None)
    if not v:
        return None, tc
    ch = next(ch for ch in e.cambios if ch["t"] == tc and "sigue" in ch)
    return (v, ch.get("offset", -260), ch.get("lag", 0.3)), tc


def _pos(e, t, prof=0):
    """(x, y, moviendo, dirección -1/1/0, corre)."""
    s = e.spec
    x, y = s.get("x", 540), s.get("y", 1300)
    mov, dirx, corre = False, 0, False
    for t0, t1, x0, y0, x1, y1, cr in e.tramos:
        if t >= t1:
            x, y = x1, y1
        elif t >= t0:
            k = (t - t0) / (t1 - t0)
            k = k if cr else _ease(k)  # al correr, velocidad constante
            x, y = x0 + (x1 - x0) * k, y0 + (y1 - y0) * k
            mov, dirx, corre = True, (1 if x1 > x0 else -1 if x1 < x0 else 0), cr
            break
    for t0, t1, h in getattr(e, "arcos", ()):
        if t0 <= t < t1:
            y -= h * math.sin(math.pi * (t - t0) / (t1 - t0))
    seg, tc = _sigue(e, t)
    if seg and prof < 3:
        obj = e.mundo.get(seg[0])
        if obj is not None and hasattr(obj, "tramos"):
            k = _eo((t - tc) / 0.4)  # se engancha a la persecución
            tx, ty, tmov, tdir, tcorre = _pos(obj, t - seg[2], prof + 1)
            nx = tx + seg[1]
            x = x + (nx - x) * k
            mov, corre = tmov or mov, tcorre
            dirx = tdir if tdir else (1 if seg[1] < 0 else -1)
    return x, y, mov, dirx, corre


def _vigente(e, t, campo, defecto):
    v, tc, prev = defecto, -1e9, defecto
    for ch in e.cambios:
        if ch["t"] <= t and campo in ch:
            prev, v, tc = v, ch[campo], ch["t"]
    return v, tc, prev


def _accion(e, t, nombre):
    """Fase 0-1 de la acción activa más reciente con ese nombre, o None."""
    d = DUR_ACC[nombre]
    for ch in reversed(e.cambios):
        if ch.get(nombre) and 0 <= t - ch["t"] < d:
            return (t - ch["t"]) / d
    return None


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


def centro(e, t=None):
    x0, y0, x1, y1 = bbox(e, t)
    return (x0 + x1) / 2, (y0 + y1) / 2


def _mira(e, v, t, x, y):
    """Pupilas: dirección fija o hacia otro elemento (id)."""
    if isinstance(v, str):
        fijo = {"izq": (-14, 0), "der": (14, 0), "arriba": (0, -12), "abajo": (0, 12), "camara": (0, 0)}
        if v in fijo:
            return fijo[v]
        obj = e.mundo.get(v)
        if obj is not None:
            ox, oy = centro(obj, t)
            dx, dy = ox - x, oy - (y - 500 * e.spec.get("scale", 1.0))
            n = math.hypot(dx, dy) or 1
            return (14 * dx / n, 12 * dy / n)
        return (0, 0)
    return tuple(v or (0, 0))


def tamano(e):
    s = e.spec
    k = e.kind
    if k == "personaje":
        return 560, 760
    if k == "edificio":
        return edificios.TAMANO.get(s["edificio"], (600, 600))
    if k == "objeto":
        return objetos.TAMANO.get(_tipo_obj(e), (300, 300))
    if k == "efecto":
        return efectos.tamano(s)
    import wb
    f = wb.font(s.get("font", "sub"), s.get("size", 90))
    return f.measureText(s["text"]) + 40, s.get("size", 90) * 1.2


def bbox(e, t=None):
    w, h = tamano(e)
    sc = e.spec.get("scale", 1.0)
    w, h = w * sc, h * sc
    t = getattr(e, "_t", e.t0 + e.dur) if t is None else t
    x, y = _pos(e, t)[:2] if hasattr(e, "tramos") else (e.spec.get("x", 540), e.spec.get("y", 1300))
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
                dy = -1500 * (1 - (k / 0.7) ** 2)
                sy, sx = 1.12, 0.92  # se estira al caer
            else:
                q = (k - 0.7) / 0.3
                sy = 1 - 0.3 * math.sin(math.pi * q)
                sx = 1 + 0.22 * math.sin(math.pi * q)
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
        elif sale == "arriba":
            dy -= 1600 * k * k
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
    M0 = c.getTotalMatrix()
    if e.kind == "efecto":
        efectos.dibuja(c, e, t, am)
        return None
    sc = s.get("scale", 1.0)
    x, y, moviendo, dirx, corre = _pos(e, t)
    dx, dy, sx, sy, a, paso = _entrada(e, t)
    if a <= 0 or sx <= 0 or sy <= 0:
        return None
    rot = 0.0  # inclinación alrededor de los pies (grados)
    ojos = 1.0
    giro_auto = 0.0
    # --- acciones cartoon
    q = _accion(e, t, "salta")
    if q is not None:
        if q < 0.12:  # anticipación: se agacha
            sy *= 1 - 0.18 * math.sin(math.pi * q / 0.24)
            sx *= 1 + 0.1 * math.sin(math.pi * q / 0.24)
        elif q < 0.86:
            k = (q - 0.12) / 0.74
            dy -= 190 * math.sin(math.pi * k)
            sy *= 1 + 0.12 * math.sin(math.pi * k)
            sx *= 1 - 0.06 * math.sin(math.pi * k)
        else:  # aterrizaje
            k = (q - 0.86) / 0.14
            sy *= 1 - 0.16 * math.sin(math.pi * k)
            sx *= 1 + 0.1 * math.sin(math.pi * k)
    q = _accion(e, t, "take")
    if q is not None:
        k = math.sin(math.pi * min(1.0, q * 1.4))
        dy -= 70 * k
        sy *= 1 + 0.28 * k
        sx *= 1 - 0.12 * k
        ojos = 1 + 0.75 * k
    q = _accion(e, t, "aplasta")
    if q is not None:
        if q < 0.65:
            sy *= 0.24 if q > 0.04 else 1 - 0.76 * (q / 0.04)
            sx *= 1.55 if q > 0.04 else 1 + 0.55 * (q / 0.04)
            ojos = 1.25
        else:
            k = (q - 0.65) / 0.35
            sy *= 0.24 + 0.76 * _back(k, 2.6)
            sx *= 1.55 - 0.55 * _back(k, 2.6)
    q = _accion(e, t, "tropieza")
    lado = dirx or (1 if not s.get("flip") else -1)
    tropezando = q is not None
    if q is not None:
        if q < 0.2:  # tropieza y cae de bruces
            k = q / 0.2
            rot = lado * 88 * k * k
            dx += lado * 60 * k
        elif q < 0.68:  # en el suelo, viendo estrellas
            rot = lado * (88 + 3 * math.sin((q - 0.2) * 40) * (0.68 - q))
            dx += lado * 60
        else:  # se levanta de un salto
            k = (q - 0.68) / 0.32
            rot = lado * 88 * (1 - _eo(k * 1.3))
            dy -= 80 * math.sin(math.pi * k)
            dx += lado * 60
    q = _accion(e, t, "gira")
    if q is not None:
        sx *= max(0.12, abs(math.cos(math.pi * q)))
    q = _accion(e, t, "tiembla")
    if q is not None:
        dx += 14 * math.sin(q * 48) * (1 - q)
    cara, tc, _ = _vigente(e, t, "cara", s.get("cara"))
    if 0 <= t - tc < 0.22:  # «pop» de reacción: estira y encoge
        k = (t - tc) / 0.22
        sy *= 1 + 0.1 * math.sin(math.pi * k)
        sx *= 1 - 0.05 * math.sin(math.pi * k)
    # el giro (flip) cambia a mitad de la vuelta
    flip = s.get("flip", False)
    for ch in e.cambios:
        if "flip" in ch and ch["t"] + (0.15 if ch.get("gira") else 0) <= t:
            flip = ch["flip"]
    # «trota»: corre (o anda, "anda") sin moverse del sitio; el fondo es el que pasa (fondo "parque" con velocidad)
    trota, _, _ = _vigente(e, t, "trota", s.get("trota", False))
    if trota and not moviendo and e.kind == "personaje" and not tropezando:
        moviendo, corre, dirx = True, trota != "anda", (-1 if flip else 1)
    # andar / correr: paso, inclinación hacia delante y cara hacia donde va
    if moviendo and (e.kind == "personaje" or s.get("piernas")):
        paso = (t - e.t0) * (FREC_CORRE if corre else FREC_ANDA)
        rot += dirx * (11 if corre else 4)
        giro_auto = dirx * (0.7 if corre else 0.5)
        if e.kind != "personaje":
            dy -= abs(math.sin(paso * math.pi)) * 26 * (1.6 if corre else 1)
    elif e.kind == "personaje" and not tropezando:  # balanceo y respiración (idle)
        b = math.sin(t * 2 * math.pi / 2.4 + (x % 7))
        sy *= 1 + 0.014 * b
        sx *= 1 - 0.007 * b
        rot += 1.2 * math.sin(t * 1.3 + x * 0.01)
    alpha = int(255 * am * a)
    c.save()
    c.translate(x + dx, y + dy)
    if rot and e.kind in ("personaje", "edificio") or (rot and s.get("piernas")):
        c.rotate(rot)
    c.scale(sc * sx * (-1 if flip else 1), sc * sy)
    if s.get("rot"):
        c.rotate(s["rot"])
    if alpha < 255:
        c.saveLayerAlpha(None, alpha)
    tip = None
    dib = s.get("dibuja")
    if dib and t - e.t0 < dib:  # «se dibuja»: el rotulador lo va trazando de izquierda a derecha
        k = max(0.0, (t - e.t0) / dib)
        w, h = tamano(e)
        abajo = e.kind in ("personaje", "edificio") or (e.kind == "objeto" and _tipo_obj(e) in objetos.APOYADOS)
        x0, y0 = -w / 2, (-h if abajo else -h / 2)
        xe = x0 + w * k
        c.save()
        c.clipRect(skia.Rect(x0 - 400, y0 - 400, xe, y0 + h + 400))
        tip = (xe, y0 + h * (0.5 + 0.42 * math.sin(k * 38)))
    if e.kind == "personaje":
        mira_v, _, _ = _vigente(e, t, "mira", s.get("mira"))
        mira = _mira(e, mira_v, t, x, y) if mira_v is not None else ((dirx * 14, 0) if moviendo else (0, 0))
        if flip:
            mira = (-mira[0], mira[1])
        giro, _, _ = _vigente(e, t, "giro", s.get("giro", 0.0))
        giro = giro_auto * (-1 if flip else 1) if moviendo else giro
        if isinstance(mira_v, str) and mira_v in e.mundo and not moviendo:
            giro = 0.35 * (1 if mira[0] > 0 else -1)
        _personaje(e, c, t, cara, tc, paso, mira, ojos, corre, giro)
        if tropezando and 0.18 < _accion(e, t, "tropieza") < 0.95:
            c.save(); c.translate(0, -PIES - 250)
            efectos.estrellas_cabeza(c, t)
            c.restore()
    elif e.kind == "edificio":
        _edificio(e, c, t, cara, paso)
    elif e.kind == "objeto":
        t_obj = _objeto(e, c, t, cara, paso, moviendo, dirx)
        tip = tip or t_obj
    else:
        texto_cartoon(c, s["text"], 0, s.get("size", 90) * 0.35, s.get("size", 90), color=s.get("color", "amarillo"),
                      fuente=s.get("font", "sub"))
    if tip is not None:
        tip = _a_mundo(M0, c, tip)
    if dib and t - e.t0 < dib:
        c.restore()
    if alpha < 255:
        c.restore()
    c.restore()
    # polvo a los pies (en coordenadas de mundo, sin la escala del salto)
    for tp in e.polvo:
        if 0 <= t - tp < 0.5:
            efectos.polvo(c, x, y, (t - tp) / 0.5, sc, dirx)
    return tip


def _a_mundo(M0, c, pt):
    """Punta del rotulador en coordenadas del mundo (fuera de la cámara se dibuja a escala de cámara: con mucho
    zoom el rotulador taparía la pantalla, así que solo aparece en planos abiertos)."""
    if math.hypot(M0.getScaleX(), M0.getSkewY()) > 1.6:
        return None
    inv = skia.Matrix()
    if not M0.invert(inv):
        return None
    d = c.getTotalMatrix().mapXY(float(pt[0]), float(pt[1]))
    w = inv.mapXY(d.x(), d.y())
    return (w.x(), w.y())


def _personaje(e, c, t, cara, tc, paso, mira, ojos, corre, giro):
    s = e.spec
    pose, tp, pose_prev = _vigente(e, t, "pose", s.get("pose"))
    if pose is None:  # sin pose fija: la pose sigue a la cara
        pose = personajes.BRAZOS_DE.get(cara or "normal", "normal")
        pose_prev = personajes.BRAZOS_DE.get(_vigente(e, tc - 1e-3, "cara", s.get("cara"))[0] or "normal", "normal")
        tp = tc
    pose_prev = pose_prev or personajes.BRAZOS_DE.get(cara or "normal", "normal")
    q = _accion(e, t, "tropieza")
    if q is not None and q < 0.68:
        pose, pose_prev, tp = "cae", "cae", -1e9
    k_pose = _eo((t - tp) / 0.2) if t - tp < 0.2 else 1.0
    obj, _, _ = _vigente(e, t, "objeto", s.get("objeto"))
    c.translate(0, -PIES)
    personajes.dibuja(c, s.get("quien", "piz"), cara=cara, pose=pose, pose_prev=pose_prev, k_pose=k_pose,
                      mira=mira, parpadeo=_parpadeo(e, t), habla=_habla(e, t), paso=paso, t=t, objeto=obj,
                      ojos=ojos, corre=corre, giro=giro, sombra=_accion(e, t, "salta") is None)


def _piernas(c, ancho, base, paso, alto=110, zap="rojo", s=1.0):
    """Piernitas con zapatillas para edificios y objetos que andan o persiguen."""
    for i, sx in enumerate((-ancho * 0.22, ancho * 0.22)):
        lado = -1 if i == 0 else 1
        fx, fy, lev = sx, base + alto, 0.0
        if paso is not None:
            fase = paso * 2 * math.pi + (0 if i == 0 else math.pi)
            fx += 40 * s * math.sin(fase)
            lev = max(0.0, math.cos(fase))
            fy -= 30 * s * lev
        manguera(c, (sx, base - 4), (fx, fy - 10 * s), 0.12 * lado, 20 * s)
        personajes.zapatilla(c, fx + 10 * lado, fy, lado, zap, 1.3 * s, lev)


def _edificio(e, c, t, cara, paso):
    s = e.spec
    dentro, _, _ = _vigente(e, t, "caras_dentro", s.get("caras_dentro", {}))
    est = {"cara": cara or "normal", "mira": _mira(e, _vigente(e, t, "mira", s.get("mira"))[0], t, 0, 0),
           "parpadeo": _parpadeo(e, t), "habla": _habla(e, t),
           "caras_dentro": {int(k): v for k, v in (dentro or {}).items()}}
    if cara is None:
        est.pop("cara")
    if "texto" in s:  # rótulo propio (ayuntamiento, abandonado)
        est["texto"] = s["texto"]
    kw = {k: s[k] for k in ("variante", "trabajadores") if k in s}
    if s.get("piernas"):
        w, _ = edificios.TAMANO.get(s["edificio"], (500, 500))
        c.translate(0, -120)
        _piernas(c, w * 0.8, 0, paso, 120, s=1.4)
    edificios.dibuja(c, s["edificio"], est, t, **kw)


def _objeto(e, c, t, cara, paso, moviendo=False, dirx=0):
    s = e.spec
    o = s["objeto"]
    kw = dict(o) if isinstance(o, dict) else {"tipo": o}
    kw.update(s.get("props", {}))
    cambios = [(e.t0, s.get("props", {}))]
    for ch in e.cambios:
        if ch["t"] <= t and "props" in ch:
            kw.update(ch["props"])
            cambios.append((ch["t"], ch["props"]))
    if cara:
        kw["cara"] = cara
    if kw["tipo"] in objetos.DIBUJO and "progreso" not in kw:
        kw["progreso"] = min(1.0, (t - e.t0) / max(0.3, s.get("dibujo", objetos.DIBUJO[kw["tipo"]])))
    if kw["tipo"] in ("mapa", "documento", "barco", "camion", "carabela"):
        kw.update(_cambios=cambios, _t0=e.t0, _mov=moviendo, _dir=dirx)
    if s.get("flota"):
        c.translate(0, 10 * math.sin(t * 2.6 + e.t0))
    if s.get("piernas"):
        w, h = objetos.TAMANO.get(kw["tipo"], (300, 300))
        _piernas(c, w, h / 2 - 10, paso, 100)
    return objetos.dibuja(c, kw, t)
