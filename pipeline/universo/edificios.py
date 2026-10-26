"""Edificios con personalidad (biblioteca fija): casa, piso, banco, Hacienda, Congreso, hospital, supermercado, fábrica.

Cada edificio se dibuja en coordenadas locales con la base del suelo en y = 0, y tiene una cara
(ojos + boca) que usa las mismas expresiones que los personajes. Algunos llevan pizarras trabajando dentro.
"""
import math

import skia

from . import personajes as P
from .estilo import (COL, degradado, elipse, pieza, poly, relleno, rgb, rrect, sombra_suelo, suave, texto_cartoon,
                     trazo)


def cara(c, x, y, s, expresion="normal", mira=(0, 0), parpadeo=0.0, habla=0.0, t=0.0):
    """Ojos y boca de pizarra sobre cualquier superficie, centrados en (x, y)."""
    ex = P.EXPRESIONES.get(expresion, P.EXPRESIONES["normal"])
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    parp = max(ex["parpado"], parpadeo)
    mx, my = mira[0] + ex.get("mira", (0, 0))[0], mira[1] + ex.get("mira", (0, 0))[1]
    for ox, lado in ((-45, -1), (45, 1)):
        P.ojo(c, ox, P.OJOS_Y, ex["ojo"], parp, ex.get("inclina", 0), ex["pupila"], (mx, my), lado, ex.get("cerrados"))
    P.cejas(c, *ex["cejas"])
    P.boca(c, ex["boca"], habla)
    c.restore()


def ventana(c, x, y, w, h, luz=False, cruz=True):
    pieza(c, rrect(x, y, x + w, y + h, 6), "luz" if luz else "cristal", 5,
          shader=degradado(y, y + h, "blanco" if not luz else "luz", "cristal" if not luz else "naranja"))
    c.drawLine(x + w * 0.2, y + h * 0.75, x + w * 0.6, y + h * 0.2, trazo(4, "blanco", 160))
    if cruz:
        c.drawLine(x + w / 2, y, x + w / 2, y + h, trazo(4))
        c.drawLine(x, y + h / 2, x + w, y + h / 2, trazo(4))


def maceta(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    for dx, dy, r in ((-22, -70, 30), (20, -78, 32), (0, -104, 30), (-30, -100, 22), (30, -110, 22)):
        pieza(c, elipse(dx, dy, r, r * 0.9), "hierba", 4.5)
    pieza(c, poly([(-40, -46), (40, -46), (32, 0), (-32, 0)]), "piedra_osc", 5)
    c.restore()


# ------------------------------------------------------------------ casa
def casa(c, est, t=0.0, variante="moderna"):
    """Casa unifamiliar con cara: las ventanas son los ojos, la puerta la boca sonriente."""
    w, h = 460, 330
    sombra_suelo(c, 0, 4, 280)
    pared = "fachada" if variante != "antigua" else "piedra"
    pieza(c, rrect(-w / 2, -h, w / 2, 0, 10), pared, 6, shader=degradado(-h, 0, "blanco" if variante == "moderna" else pared, pared),
          sombra=(rrect(w / 2 - 60, -h, w / 2, 0, 0), "piedra_osc"))
    # tejado
    tejado = poly([(-w / 2 - 40, -h + 6), (0, -h - 200), (w / 2 + 40, -h + 6)])
    pieza(c, tejado, "teja", 7, sombra=(poly([(0, -h - 200), (w / 2 + 40, -h + 6), (w / 2 - 30, -h + 6)]), "rojo_osc"))
    for i in range(1, 4):
        y = -h - 200 + i * 50
        x = 200 * i / 4 + 10
        c.drawLine(-x, y, x, y, trazo(4, "rojo_osc", 200))
    pieza(c, rrect(110, -h - 170, 160, -h - 60, 4), "teja", 6)  # chimenea
    # puerta (boca) + ventanas-ojo
    ex = est.get("cara", "normal")
    cara(c, 0, -h + 150, 1.15, ex, est.get("mira", (0, 0)), est.get("parpadeo", 0), est.get("habla", 0), t)
    pieza(c, rrect(150, -120, 210, 0, 6), "madera", 5)
    c.drawCircle(160, -60, 5, relleno("tinta"))
    maceta(c, -180, 0, 0.7)


def piso(c, est, t=0.0):
    """Bloque de pisos antiguo con cara (para «el piso medio»)."""
    w, h = 420, 640
    sombra_suelo(c, 0, 4, 260)
    pieza(c, rrect(-w / 2, -h, w / 2, 0, 8), "piedra", 6, sombra=(rrect(w / 2 - 50, -h, w / 2, 0, 0), "piedra_osc"))
    pieza(c, rrect(-w / 2 - 14, -h - 26, w / 2 + 14, -h + 6, 6), "piedra_osc", 6)
    for row in range(2):
        for col in range(3):
            ventana(c, -150 + col * 110, -h + 260 + row * 120, 80, 90, luz=(row + col) % 2 == 0)
    cara(c, 0, -h + 150, 1.0, est.get("cara", "normal"), est.get("mira", (0, 0)), est.get("parpadeo", 0), est.get("habla", 0), t)
    pieza(c, rrect(-50, -120, 50, 0, 8), "madera", 5)
    pieza(c, rrect(-70, -150, 70, -120, 6), "verde_osc", 5)


# ------------------------------------------------------------------ banco
def banco(c, est, t=0.0, trabajadores=None):
    """El banco de la referencia: fachada con cara y guantes, cristalera con pizarras banqueras dentro."""
    w, h = 900, 760
    sombra_suelo(c, 0, 6, 480)
    # escalones
    for i in range(3):
        pieza(c, rrect(-w / 2 - 30 + i * 18, -22 * (i + 1), w / 2 + 30 - i * 18, -22 * i, 4), "piedra", 5)
    base = -66
    # cuerpo y frontón
    pieza(c, rrect(-w / 2, base - h + 180, w / 2, base, 8), "piedra", 7, shader=degradado(base - h, base, "blanco", "piedra"))
    fronton = poly([(-w / 2 + 40, base - h + 190), (-w / 2 + 70, base - h + 20), (-120, base - h + 20), (-80, base - h - 30),
                    (80, base - h - 30), (120, base - h + 20), (w / 2 - 70, base - h + 20), (w / 2 - 40, base - h + 190)])
    pieza(c, fronton, "piedra", 7, shader=degradado(base - h - 30, base - h + 190, "blanco", "piedra"))
    # cornisa
    pieza(c, rrect(-w / 2 - 24, base - h + 170, w / 2 + 24, base - h + 210, 8), "gris_claro", 6)
    # rótulo BANCO
    texto_cartoon(c, "BANCO", -150, base - h + 140, 130, color=(70, 76, 92), fuente="sub", borde=4)
    # cara en el frontón
    cara(c, 230, base - h + 70, 0.85, est.get("cara", "riendo" if est.get("habla", 0) else "ilusionado"),
         est.get("mira", (-10, 4)), est.get("parpadeo", 0), est.get("habla", 0), t)
    # guantes saliendo de los lados
    P.guante(c, -w / 2 - 30, base - h + 260, 230, "abierto", 1.6, -1)
    P.guante(c, w / 2 + 30, base - h + 260, -50, "senala", 1.6, 1)
    # cristalera con interior iluminado
    cx0, cx1, cy0, cy1 = -w / 2 + 40, w / 2 - 40, base - h + 230, base - 20
    vid = rrect(cx0, cy0, cx1, cy1, 8)
    pieza(c, vid, "luz", 6, shader=degradado(cy0, cy1, "luz", (250, 210, 150)))
    c.save()
    c.clipPath(vid, skia.ClipOp.kIntersect, True)
    for i in range(5):  # lámparas
        c.drawCircle(cx0 + 90 + i * 170, cy0 + 26, 14, relleno("blanco", 230))
    gente = trabajadores or [("banquero", "normal", "Asesor\nhipotecas"), ("banquera_seria", "serio", "Análisis\nde riesgo"),
                             ("banquero", "burla", "Condiciones"), ("banquera_seria", "esceptica", "Aprobación\nfinal")]
    n = len(gente)
    for i, (quien, ex, rot) in enumerate(gente):
        x = cx0 + (cx1 - cx0) * (i + 0.5) / n
        # cartel colgante
        import wb
        f = wb.font("hand", 30)
        lines = rot.split("\n")
        ww = max(f.measureText(l) for l in lines) + 30
        pieza(c, rrect(x - ww / 2, cy0 + 50, x + ww / 2, cy0 + 56 + 36 * len(lines), 6), "tinta", 0)
        for j, ln in enumerate(lines):
            c.drawString(ln, x - f.measureText(ln) / 2, cy0 + 84 + 34 * j, f, relleno("blanco"))
        c.save(); c.translate(x, cy1 - 150); c.scale(0.42, 0.42)
        ex_i = est.get("caras_dentro", {}).get(i, ex)
        P.dibuja(c, quien, cara=ex_i, pose="sostiene2" if i % 2 else "senala", t=t + i, sombra=False)
        c.restore()
        # mostrador
        pieza(c, rrect(x - 90, cy1 - 70, x + 90, cy1 - 40, 4), "madera", 5)
    c.restore()
    for i in range(1, 4):  # montantes de la cristalera
        x = cx0 + (cx1 - cx0) * i / 4
        c.drawRect(skia.Rect(x - 8, cy0, x + 8, cy1), relleno("gris"))
        c.drawRect(skia.Rect(x - 8, cy0, x + 8, cy1), trazo(5))
    c.drawPath(vid, trazo(7))
    maceta(c, -w / 2 - 40, 0, 1.0)
    maceta(c, w / 2 + 40, 0, 1.0)


# ------------------------------------------------------------------ Hacienda
def hacienda(c, est, t=0.0):
    w, h = 820, 700
    sombra_suelo(c, 0, 6, 440)
    pieza(c, rrect(-w / 2, -h, w / 2, 0, 8), (226, 216, 196), 7, shader=degradado(-h, 0, "piedra", (214, 200, 176)))
    pieza(c, rrect(-w / 2 - 20, -h - 40, w / 2 + 20, -h + 10, 8), "gris_claro", 6)
    texto_cartoon(c, "HACIENDA", 0, -h + 130, 110, color=(160, 40, 40), fuente="sub", borde=4)
    cara(c, 0, -h + 330, 1.15, est.get("cara", "burla"), est.get("mira", (0, 0)), est.get("parpadeo", 0), est.get("habla", 0), t)
    for x in (-300, -200, 200, 300):  # ventanas con pizarras de Hacienda
        ventana(c, x - 40, -h + 220, 80, 100, luz=True, cruz=False)
    for x in (-250, 250):
        c.save(); c.translate(x, -h + 560); c.scale(0.32, 0.32)
        P.dibuja(c, "hacienda", cara="burla", pose="sostiene2", t=t, sombra=False)
        c.restore()
    pieza(c, rrect(-80, -170, 80, 0, 10), "madera", 6)
    maceta(c, -w / 2 - 30, 0, 0.9)


# ------------------------------------------------------------------ Congreso
def congreso(c, est, t=0.0):
    w, h = 980, 640
    sombra_suelo(c, 0, 6, 520)
    for i in range(4):
        pieza(c, rrect(-w / 2 - 40 + i * 20, -24 * (i + 1), w / 2 + 40 - i * 20, -24 * i, 4), "piedra", 5)
    base = -96
    pieza(c, rrect(-w / 2, base - h + 160, w / 2, base, 6), "piedra", 7)
    pieza(c, poly([(-w / 2 + 120, base - h + 170), (0, base - h - 30), (w / 2 - 120, base - h + 170)]), "piedra", 7)
    cara(c, 0, base - h + 120, 0.7, est.get("cara", "serio"), est.get("mira", (0, 0)), est.get("parpadeo", 0), est.get("habla", 0), t)
    for i in range(6):  # columnas
        x = -w / 2 + 110 + i * (w - 220) / 5
        pieza(c, rrect(x - 30, base - h + 190, x + 30, base, 6), "blanco", 6, shader=degradado(0, 0, "blanco", "piedra", x - 30, x + 30))
    for sx in (-1, 1):  # leones
        x = sx * (w / 2 + 70)
        pieza(c, rrect(x - 70, -160, x + 70, -100, 8), "piedra_osc", 6)
        pieza(c, elipse(x, -190, 56, 48), "oro", 6)
        cara(c, x, -170, 0.38, "serio", (0, 0), 0, 0, t)
    texto_cartoon(c, est.get("texto") or "CONGRESO", 0, base - h + 250, 70, color="tinta", fuente="sub", borde=2)


# ------------------------------------------------------------------ hospital, súper, fábrica
def hospital(c, est, t=0.0):
    w, h = 760, 720
    sombra_suelo(c, 0, 6, 420)
    pieza(c, rrect(-w / 2, -h, w / 2, 0, 10), "blanco", 7, shader=degradado(-h, 0, "blanco", "gris_claro"))
    pieza(c, rrect(-60, -h - 10, 60, -h + 110, 10), "rojo", 6)
    pieza(c, rrect(-20, -h + 10, 20, -h + 90, 4), "blanco", 4)
    pieza(c, rrect(-40, -h + 30, 40, -h + 70, 4), "blanco", 4)
    cara(c, 0, -h + 290, 1.05, est.get("cara", "preocupado"), est.get("mira", (0, 0)), est.get("parpadeo", 0), est.get("habla", 0), t)
    for r in range(2):
        for i in range(5):
            if 1 <= i <= 3:
                continue
            ventana(c, -w / 2 + 50 + i * 140, -h + 180 + r * 200, 90, 100)
    pieza(c, rrect(-110, -180, 110, 0, 10), "cristal", 6)
    texto_cartoon(c, "URGENCIAS", 0, -200, 54, color="rojo", fuente="sub", borde=2)


def supermercado(c, est, t=0.0):
    w, h = 860, 520
    sombra_suelo(c, 0, 6, 460)
    pieza(c, rrect(-w / 2, -h, w / 2, 0, 10), "fachada", 7)
    for i in range(9):  # toldo de rayas
        x = -w / 2 + i * w / 9
        pieza(c, poly([(x, -h + 120), (x + w / 9, -h + 120), (x + w / 9, -h + 190), (x, -h + 190)]),
              "rojo" if i % 2 == 0 else "blanco", 5)
    texto_cartoon(c, "SÚPER", 0, -h + 90, 90, color="verde", fuente="sub", borde=3)
    cara(c, 0, -h + 290, 0.9, est.get("cara", "ilusionado"), est.get("mira", (0, 0)), est.get("parpadeo", 0), est.get("habla", 0), t)
    pieza(c, rrect(-w / 2 + 40, -200, -140, -20, 6), "cristal", 6)
    pieza(c, rrect(140, -200, w / 2 - 40, -20, 6), "cristal", 6)
    pieza(c, rrect(-100, -220, 100, 0, 6), "cristal", 6)


def fabrica(c, est, t=0.0):
    w, h = 900, 460
    sombra_suelo(c, 0, 6, 480)
    teeth = [(-w / 2, -h + 120)]
    for i in range(4):
        x = -w / 2 + i * w / 4
        teeth += [(x + w / 4, -h), (x + w / 4, -h + 120)]
    pieza(c, poly(teeth + [(w / 2, 0), (-w / 2, 0)]), "gris_claro", 7)
    for x in (-300, 280):  # chimeneas con humo
        pieza(c, rrect(x, -h - 260, x + 70, -h + 40, 6), "teja", 6)
        for k in range(3):
            f = ((t * 0.6 + k / 3) % 1)
            c.drawCircle(x + 35 + 40 * f, -h - 290 - 160 * f, 30 + 40 * f, relleno("gris_claro", int(220 * (1 - f))))
    cara(c, 0, -h + 260, 0.9, est.get("cara", "serio"), est.get("mira", (0, 0)), est.get("parpadeo", 0), est.get("habla", 0), t)
    for x in (-330, -220, 160, 270):
        ventana(c, x, -190, 70, 80)
    pieza(c, rrect(-90, -180, 90, 0, 6), "madera", 6)


# ------------------------------------------------------------------ ayuntamiento, edificio abandonado
def ayuntamiento(c, est, t=0.0):
    """Casa consistorial con balcón, reloj y banderas; est["texto"] = rótulo."""
    w, h = 900, 720
    sombra_suelo(c, 0, 6, 480)
    pieza(c, rrect(-w / 2, -h, w / 2, 0, 8), "fachada", 7, shader=degradado(-h, 0, (250, 222, 190), (232, 196, 158)))
    pieza(c, rrect(-w / 2 - 20, -h - 30, w / 2 + 20, -h + 20, 8), "teja", 6)
    pieza(c, rrect(-120, -h - 190, 120, -h - 20, 10), "piedra", 6)  # torreta del reloj
    c.drawCircle(0, -h - 105, 62, relleno("blanco")); c.drawCircle(0, -h - 105, 62, trazo(6))
    a = t * 0.5
    c.drawLine(0, -h - 105, 40 * math.sin(a), -h - 105 - 40 * math.cos(a), trazo(6))
    c.drawLine(0, -h - 105, 0, -h - 150, trazo(6))
    for x, rayas in ((-170, ("rojo", "amarillo", "amarillo", "rojo")), (170, ("amarillo", "rojo") * 4 + ("amarillo",))):
        c.drawLine(x, -h - 20, x, -h - 240, trazo(6))  # mástiles con las banderas de España y de Cataluña
        d = 1 if x > 0 else -1
        ola = 6 * math.sin(t * 5 + x)
        for i, col in enumerate(rayas):
            a = 64 / len(rayas)
            y0 = -h - 236 + i * a
            pieza(c, suave([(x, y0), (x + 70 * d, y0 + ola), (x + 120 * d, y0), (x + 120 * d, y0 + a), (x + 70 * d, y0 + a + ola), (x, y0 + a)]), col, 0)
        c.drawPath(suave([(x, -h - 236), (x + 70 * d, -h - 236 + ola), (x + 120 * d, -h - 236), (x + 120 * d, -h - 172), (x + 70 * d, -h - 172 + ola), (x, -h - 172)]), trazo(5))
    texto_cartoon(c, est.get("texto", "AYUNTAMIENTO"), 0, -h + 110, 66, color="tinta", fuente="sub", borde=2)
    cara(c, 0, -h + 250, 1.0, est.get("cara", "normal"), est.get("mira", (0, 0)), est.get("parpadeo", 0), est.get("habla", 0), t)
    for x in (-330, -200, 200, 330):
        ventana(c, x - 40, -h + 220, 80, 110, luz=True)
    pieza(c, rrect(-170, -h + 450, 170, -h + 474, 6), "tinta", 0)  # balcón
    for i in range(9):
        x = -160 + i * 40
        c.drawLine(x, -h + 450, x, -h + 400, trazo(5))
    c.drawLine(-170, -h + 400, 170, -h + 400, trazo(6))
    pieza(c, rrect(-90, -200, 90, 0, 40), "madera", 6)
    maceta(c, -w / 2 - 30, 0, 0.9)
    maceta(c, w / 2 + 30, 0, 0.9)


def abandonado(c, est, t=0.0):
    """Edificio viejo cerrado: ventanas tapiadas con tablas; est["texto"] = rótulo."""
    w, h = 900, 640
    sombra_suelo(c, 0, 6, 480)
    pieza(c, rrect(-w / 2, -h, w / 2, 0, 6), (206, 198, 186), 7, shader=degradado(-h, 0, (214, 206, 194), (180, 170, 156)))
    for x, y in ((-300, -h + 60), (240, -h + 380), (-80, -120)):  # grietas
        c.drawPath(suave([(x, y), (x + 20, y + 30), (x + 6, y + 60), (x + 30, y + 90)], close=False), trazo(4, (110, 100, 90)))
    texto_cartoon(c, est.get("texto", "B9"), 0, -h + 100, 90, color=(120, 40, 40), fuente="sub", borde=3)
    cara(c, 0, -h + 280, 0.9, est.get("cara", "triste"), est.get("mira", (0, 0)), est.get("parpadeo", 0), est.get("habla", 0), t)
    for r in range(2):
        for x in (-330, -190, 110, 250):
            y = -h + 200 + r * 210
            pieza(c, rrect(x, y, x + 90, y + 110, 4), (60, 60, 70), 5)
            for k in (25, 70):  # tablas cruzadas
                c.save(); c.translate(x + 45, y + k); c.rotate(-12 if k < 50 else 10)
                pieza(c, rrect(-58, -10, 58, 10, 3), "madera", 4)
                c.restore()
    pieza(c, rrect(-90, -200, 90, 0, 6), (90, 80, 72), 6)
    pieza(c, rrect(-110, -110, 110, -70, 4), "madera", 4)


TIPOS = {"casa": casa, "piso": piso, "banco": banco, "hacienda": hacienda, "congreso": congreso, "hospital": hospital,
         "supermercado": supermercado, "fabrica": fabrica,
         "ayuntamiento": ayuntamiento, "abandonado": abandonado}
# tamaño aproximado (ancho, alto) para la cámara
TAMANO = {"casa": (520, 560), "piso": (450, 680), "banco": (1000, 900), "hacienda": (880, 760), "congreso": (1120, 760),
          "hospital": (800, 760), "supermercado": (900, 560), "fabrica": (940, 780),
          "ayuntamiento": (960, 1000), "abandonado": (940, 700)}


def dibuja(c, tipo, est=None, t=0.0, **kw):
    TIPOS[tipo](c, est or {}, t, **kw)
