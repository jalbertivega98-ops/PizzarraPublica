"""Objetos del universo (biblioteca fija): dinero, papeles, herramientas, vehículos, naturaleza y rótulos.

Cada objeto se dibuja centrado en (0, 0) local con un tamaño de unos 200-300 px a escala 1.
Varios tienen cara (cara=...) para que también reaccionen.
"""
import math

import skia

from .estilo import (COL, degradado, elipse, pieza, poly, relleno, rrect, sombra_suelo, suave, texto_cartoon, trazo)


def _cara(c, x, y, s, ex, t=0.0, habla=0.0):
    if not ex:
        return
    from .edificios import cara
    cara(c, x, y, s, ex, (0, 0), 0, habla, t)


def _font(size, cual="hand"):
    import wb
    return wb.font(cual, size)


def _texto(c, txt, x, y, size, color="tinta", cual="hand"):
    f = _font(size, cual)
    c.drawString(txt, x - f.measureText(txt) / 2, y, f, relleno(color))


# ------------------------------------------------------------------ dinero
def billete(c, t=0.0, cara=None, valor="50", **kw):
    p = rrect(-150, -75, 150, 75, 12)
    pieza(c, p, "billete", 6, shader=degradado(-75, 75, (160, 220, 150), "billete"))
    c.drawPath(rrect(-128, -55, 128, 55, 8), trazo(3.5, "verde_osc"))
    c.drawPath(elipse(0, 0, 44, 44), trazo(4, "verde_osc"))
    _texto(c, "€", 0, 18, 56, "verde_osc", "sub")
    for sx in (-1, 1):
        _texto(c, valor, sx * 96, 14, 40, "verde_osc", "sub")
    _cara(c, 0, 4, 0.45, cara, t)


def fajo(c, t=0.0, **kw):
    for i in range(4, -1, -1):
        c.save(); c.translate(i * 8, -i * 14); c.rotate(-3 + i * 1.5)
        billete(c, t, valor=kw.get("valor", "50"))
        c.restore()
    pieza(c, rrect(-20, -90, 20, 80, 4), "amarillo", 4)


def moneda(c, t=0.0, cara=None, **kw):
    gira = abs(math.cos(t * 3)) if kw.get("gira") else 1.0
    c.save(); c.scale(max(0.15, gira), 1)
    pieza(c, elipse(0, 0, 90, 90), "oro", 7, shader=degradado(-90, 90, (255, 226, 120), (220, 160, 30)))
    c.drawPath(elipse(0, 0, 68, 68), trazo(4, (190, 130, 20)))
    if not cara:
        _texto(c, "€", 0, 30, 90, (170, 110, 10), "sub")
    c.restore()
    _cara(c, 0, 20, 0.5, cara, t)


def hucha(c, t=0.0, cara="ilusionado", **kw):
    """Cerdito hucha rosa (los ahorros)."""
    sombra_suelo(c, 0, 150, 160)
    for x in (-90, -40, 40, 90):
        pieza(c, rrect(x - 22, 90, x + 22, 150, 10), (240, 150, 180), 5)
    cuerpo = suave([(-170, 10), (-140, -100), (0, -140), (140, -100), (180, 10), (130, 110), (-120, 110)])
    pieza(c, cuerpo, (248, 170, 196), 7, shader=degradado(-140, 110, (255, 200, 216), (236, 140, 172)))
    pieza(c, poly([(-110, -110), (-80, -170), (-50, -120)]), (240, 150, 180), 5)
    pieza(c, rrect(-40, -146, 40, -130, 6), "tinta", 0)
    pieza(c, elipse(178, 10, 34, 40), (240, 150, 180), 6)
    for y in (-2, 22):
        c.drawCircle(176, y, 6, relleno("tinta"))
    c.drawPath(suave([(-170, 0), (-200, -20), (-210, 10), (-190, 20)], close=False), trazo(6))
    _cara(c, 60, -30, 0.7, cara, t)
    if kw.get("vacia"):
        adorno_moscas(c, t)


def adorno_moscas(c, t):
    for i in range(3):
        a = t * 4 + i * 2.1
        x, y = 140 * math.cos(a), -180 + 40 * math.sin(a * 1.3)
        c.drawCircle(x, y, 7, relleno("tinta"))
        c.drawPath(elipse(x - 6, y - 8, 7, 4), relleno("blanco", 200))


def saco(c, t=0.0, cara=None, **kw):
    sombra_suelo(c, 0, 150, 150)
    p = suave([(-60, -120), (60, -120), (40, -90), (150, 40), (110, 150), (-110, 150), (-150, 40), (-40, -90)])
    pieza(c, p, (214, 184, 130), 7, shader=degradado(-120, 150, (236, 210, 160), (196, 160, 104)))
    c.drawLine(-50, -96, 50, -96, trazo(10, "madera"))
    texto_cartoon(c, "€", 0, 85, 120, color="oro", fuente="sub")
    _cara(c, 0, 0, 0.5, cara, t)


# ------------------------------------------------------------------ papeles
def contrato(c, t=0.0, cara=None, titulo="HIPOTECA", **kw):
    """Papel con letra pequeña; pagina>0 añade hojas detrás."""
    for i in range(kw.get("hojas", 2), 0, -1):
        c.save(); c.translate(i * 10, -i * 8); c.rotate(i * 2.5)
        pieza(c, rrect(-130, -170, 130, 170, 6), "gris_claro", 5)
        c.restore()
    pieza(c, rrect(-130, -170, 130, 170, 6), "blanco", 6, shader=degradado(-170, 170, "blanco", "pizarra_sombra"))
    _texto(c, titulo, 0, -118, 42, "tinta", "sub")
    for i in range(10):
        y = -84 + i * 22
        w = 200 if i % 3 else 150
        c.drawLine(-100, y, -100 + w, y, trazo(4, "gris"))
    c.drawPath(suave([(30, 140), (60, 120), (80, 146), (110, 126)], close=False), trazo(4, "azul"))
    _cara(c, 0, 10, 0.6, cara, t)


def cartel(c, t=0.0, texto="", lineas=None, color="blanco", tinta="tinta", ancho=None, **kw):
    """Pizarra/rótulo con texto (titulares, condiciones…)."""
    lineas = lineas or [texto]
    f = _font(54, "sub")
    w = ancho or max(f.measureText(l) for l in lineas) + 70
    h = 70 + 64 * len(lineas)
    pieza(c, rrect(-w / 2, -h / 2, w / 2, h / 2, 18), color, 7)
    for i, l in enumerate(lineas):
        _texto(c, l, 0, -h / 2 + 88 + i * 64, 54, tinta, "sub")


def checklist(c, t=0.0, items=(), marcas=(), **kw):
    """Hoja de requisitos: marcas = lista de 'si'/'no'/None por item."""
    f = _font(46)
    w = max([f.measureText(i) for i in items] + [200]) + 160
    h = 80 + 70 * len(items)
    pieza(c, rrect(-w / 2, -h / 2, w / 2, h / 2, 14), "blanco", 7, shader=degradado(-h / 2, h / 2, "blanco", "pizarra_sombra"))
    pieza(c, rrect(-60, -h / 2 - 22, 60, -h / 2 + 14, 8), "gris", 5)
    for i, it in enumerate(items):
        y = -h / 2 + 70 + i * 70
        pieza(c, rrect(-w / 2 + 30, y - 22, -w / 2 + 74, y + 22, 6), "blanco", 4.5)
        m = marcas[i] if i < len(marcas) else None
        if m == "si":
            c.drawPath(poly([(-w / 2 + 34, y), (-w / 2 + 50, y + 18), (-w / 2 + 84, y - 30)], close=False), trazo(9, "verde"))
        elif m == "no":
            c.drawLine(-w / 2 + 34, y - 20, -w / 2 + 72, y + 20, trazo(9, "rojo"))
            c.drawLine(-w / 2 + 72, y - 20, -w / 2 + 34, y + 20, trazo(9, "rojo"))
        c.drawString(it, -w / 2 + 100, y + 16, f, relleno("tinta"))


def etiqueta(c, t=0.0, texto="223.000 €", color="amarillo", cara=None, **kw):
    """Etiqueta de precio colgante."""
    f = _font(80, "sub")
    w = f.measureText(texto) + 130
    p = poly([(-w / 2, -60), (w / 2 - 50, -60), (w / 2, 0), (w / 2 - 50, 60), (-w / 2, 60)])
    pieza(c, p, color, 7, shader=degradado(-60, 60, "blanco", color))
    c.drawCircle(w / 2 - 50, 0, 12, relleno("blanco"))
    c.drawCircle(w / 2 - 50, 0, 12, trazo(5))
    c.drawString(texto, -w / 2 + 26, 28, f, relleno("tinta"))
    _cara(c, -w / 2 + 10, -80, 0.4, cara, t)


def bocadillo(c, t=0.0, texto="", lineas=None, cola=(-1, 1), **kw):
    """Bocadillo de diálogo; cola = dirección hacia el que habla."""
    lineas = lineas or [texto]
    f = _font(52)
    w = max(f.measureText(l) for l in lineas) + 80
    h = 50 + 60 * len(lineas)
    p = rrect(-w / 2, -h / 2, w / 2, h / 2, 40)
    tail = poly([(cola[0] * w * 0.15, h / 2 - 6), (cola[0] * w * 0.35, h / 2 + 60 * cola[1]), (cola[0] * w * 0.30, h / 2 - 6)])
    c.drawPath(tail, relleno("blanco")); c.drawPath(tail, trazo(6))
    pieza(c, p, "blanco", 6)
    for i, l in enumerate(lineas):
        c.drawString(l, -f.measureText(l) / 2, -h / 2 + 64 + i * 60, f, relleno("tinta"))


# ------------------------------------------------------------------ herramientas
def lupa(c, t=0.0, **kw):
    c.save(); c.rotate(-30)
    pieza(c, rrect(-18, 70, 18, 230, 14), "madera", 6)
    pieza(c, elipse(0, 0, 90, 90), "gris", 7)
    pieza(c, elipse(0, 0, 70, 70), "cristal", 5, shader=degradado(-70, 70, "blanco", "cristal"))
    c.drawPath(suave([(-40, -30), (-20, -50), (10, -56)], close=False), trazo(8, "blanco"))
    c.restore()


def calculadora(c, t=0.0, texto="753", cara=None, **kw):
    pieza(c, rrect(-110, -160, 110, 160, 20), (70, 76, 92), 7)
    pieza(c, rrect(-84, -134, 84, -64, 8), (190, 226, 190), 5)
    f = _font(52, "sub")
    c.drawString(texto, 74 - f.measureText(texto), -80, f, relleno("tinta"))
    for r in range(4):
        for k in range(3):
            pieza(c, rrect(-84 + k * 60, -42 + r * 50, -40 + k * 60, -6 + r * 50, 8),
                  "naranja" if (k == 2) else "gris_claro", 4)
    _cara(c, 0, -230, 0.5, cara, t)


def reloj(c, t=0.0, cara=None, velocidad=1.0, **kw):
    pieza(c, elipse(0, 0, 120, 120), "blanco", 8, shader=degradado(-120, 120, "blanco", "gris_claro"))
    for sx in (-1, 1):
        pieza(c, elipse(sx * 80, -110, 34, 30), "rojo", 6)
    for i in range(12):
        a = i * math.pi / 6
        c.drawLine(96 * math.cos(a), 96 * math.sin(a), 106 * math.cos(a), 106 * math.sin(a), trazo(5))
    a = t * velocidad * 2 * math.pi - math.pi / 2
    c.drawLine(0, 0, 80 * math.cos(a), 80 * math.sin(a), trazo(8))
    a2 = t * velocidad * 2 * math.pi / 12 - math.pi / 2
    c.drawLine(0, 0, 50 * math.cos(a2), 50 * math.sin(a2), trazo(10))
    c.drawCircle(0, 0, 10, relleno("tinta"))
    _cara(c, 0, 40, 0.4, cara, t)


def llave(c, t=0.0, **kw):
    c.save(); c.rotate(-20)
    pieza(c, elipse(-100, 0, 60, 60), "oro", 7)
    c.drawCircle(-100, 0, 22, relleno((246, 242, 234)))
    c.drawCircle(-100, 0, 22, trazo(6))
    pieza(c, poly([(-44, -16), (130, -16), (130, 16), (110, 16), (110, 50), (84, 50), (84, 16), (60, 16), (60, 40),
                   (36, 40), (36, 16), (-44, 16)]), "oro", 6)
    c.restore()


def grafica(c, t=0.0, valores=(1, 1.3, 1.8, 2.6, 3.4), color="rojo", progreso=1.0, **kw):
    """Gráfica que sube (se dibuja con progreso 0-1)."""
    pieza(c, rrect(-200, -160, 200, 160, 16), "blanco", 7)
    c.drawLine(-160, 120, 170, 120, trazo(6)); c.drawLine(-160, 120, -160, -130, trazo(6))
    n = len(valores); m = max(valores)
    pts = [(-140 + i * 300 / (n - 1), 110 - v / m * 220) for i, v in enumerate(valores)]
    k = max(0.0, min(1.0, progreso)) * (n - 1)
    shown = pts[:int(k) + 1]
    if int(k) < n - 1:
        a, b = pts[int(k)], pts[int(k) + 1]
        f = k - int(k)
        shown.append((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f))
    if len(shown) > 1:
        c.drawPath(poly(shown, close=False), trazo(14, color))
        x, y = shown[-1]
        c.drawCircle(x, y, 14, relleno(color)); c.drawCircle(x, y, 14, trazo(5))


def flecha(c, t=0.0, color="rojo", largo=260, **kw):
    w = 46
    pieza(c, poly([(-largo / 2, -w / 2), (largo / 2 - 70, -w / 2), (largo / 2 - 70, -w * 1.4), (largo / 2, 0),
                   (largo / 2 - 70, w * 1.4), (largo / 2 - 70, w / 2), (-largo / 2, w / 2)]), color, 7)


# ------------------------------------------------------------------ vehículos
def _rueda(c, x, y, r, t):
    pieza(c, elipse(x, y, r, r), "tinta", 0)
    c.drawCircle(x, y, r * 0.5, relleno("gris_claro"))
    a = t * 8
    c.drawLine(x + r * 0.4 * math.cos(a), y + r * 0.4 * math.sin(a), x - r * 0.4 * math.cos(a), y - r * 0.4 * math.sin(a), trazo(5))


def coche(c, t=0.0, color="azul", cara="normal", **kw):
    sombra_suelo(c, 0, 110, 230)
    pieza(c, rrect(-110, -150, 110, -40, 40), "cristal", 6)
    pieza(c, rrect(-230, -70, 230, 70, 40), color, 7, shader=degradado(-70, 70, "blanco", color))
    pieza(c, elipse(214, -20, 18, 14), "amarillo", 4)
    _rueda(c, -140, 76, 44, t)
    _rueda(c, 140, 76, 44, t)
    _cara(c, 0, -100, 0.5, cara, t)


def bus(c, t=0.0, color="rojo", cara="normal", **kw):
    sombra_suelo(c, 0, 140, 340)
    pieza(c, rrect(-340, -200, 340, 100, 34), color, 7, shader=degradado(-200, 100, "blanco", color))
    for i in range(5):
        ventana(c, -300 + i * 120, -170, 90, 90)
    _rueda(c, -220, 110, 48, t)
    _rueda(c, 220, 110, 48, t)
    _cara(c, 250, 20, 0.42, cara, t)


def tren(c, t=0.0, color="azul", cara="normal", vagones=2, **kw):
    sombra_suelo(c, 0, 120, 480)
    for v in range(vagones):
        x = -260 - v * 380
        pieza(c, rrect(x - 170, -150, x + 170, 80, 24), "gris_claro", 7)
        for i in range(3):
            ventana(c, x - 140 + i * 100, -120, 70, 70)
        _rueda(c, x - 100, 96, 34, t); _rueda(c, x + 100, 96, 34, t)
    pieza(c, suave([(-80, -170), (180, -170), (280, 0), (260, 80), (-80, 80)]), color, 7,
          shader=degradado(-170, 80, "blanco", color))
    ventana(c, 120, -140, 90, 80)
    _rueda(c, 0, 96, 34, t); _rueda(c, 180, 96, 34, t)
    _cara(c, 30, -40, 0.5, cara, t)


def ventana(c, x, y, w, h):
    from .edificios import ventana as v
    v(c, x, y, w, h, cruz=False)


# ------------------------------------------------------------------ naturaleza y calle
def arbol(c, t=0.0, **kw):
    sombra_suelo(c, 0, 0, 120)
    pieza(c, rrect(-26, -200, 26, 0, 10), "madera", 6)
    sw = 6 * math.sin(t * 1.5)
    for dx, dy, r in ((-70, -250, 80), (70, -250, 80), (0, -330, 100), (0, -230, 90)):
        pieza(c, elipse(dx + sw, dy, r, r * 0.9), "hierba", 6, shader=degradado(dy - r, dy + r, (150, 210, 100), (90, 160, 60)))


def farola(c, t=0.0, **kw):
    pieza(c, rrect(-10, -420, 10, 0, 6), (70, 76, 92), 5)
    pieza(c, poly([(-40, -420), (40, -420), (24, -470), (-24, -470)]), (70, 76, 92), 5)
    c.drawCircle(0, -416, 18, relleno("amarillo"))


def nube(c, t=0.0, s=1.0, **kw):
    p = skia.Path()
    for dx, dy, r in ((-100, 10, 55), (-40, -30, 75), (40, -40, 70), (105, 5, 55), (0, 20, 60)):
        p.addOval(skia.Rect(dx - r, dy - r, dx + r, dy + r))
    p.addRRect(skia.RRect.MakeRectXY(skia.Rect(-150, 0, 150, 60), 30, 30))
    c.drawPath(p, trazo(10))
    c.drawPath(p, relleno("blanco"))


def sol(c, t=0.0, cara="ilusionado", **kw):
    for i in range(12):
        a = i * math.pi / 6 + t * 0.4
        c.drawLine(130 * math.cos(a), 130 * math.sin(a), 170 * math.cos(a), 170 * math.sin(a), trazo(12, "naranja"))
    pieza(c, elipse(0, 0, 110, 110), "amarillo", 7, shader=degradado(-110, 110, (255, 236, 120), "naranja"))
    _cara(c, 0, 20, 0.6, cara, t)


# ------------------------------------------------------------------ móvil
def movil(c, t=0.0, pantalla="sms", texto="", lineas=None, codigo="", remite="BANCO", suena=False, cara=None, **kw):
    """Móvil cartoon. pantalla: sms (burbuja con texto), codigo (código grande), llamada (llamada entrante), aviso."""
    if suena:  # vibra y saca ondas
        c.save(); c.translate(6 * math.sin(t * 70), 0)
    pieza(c, rrect(-140, -230, 140, 230, 34), (52, 56, 70), 7)
    pant = rrect(-118, -192, 118, 192, 16)
    fondo = {"llamada": (40, 160, 90), "aviso": (226, 58, 48)}.get(pantalla, (236, 242, 250))
    pieza(c, pant, fondo, 4)
    c.drawLine(-24, -212, 24, -212, trazo(6))
    if pantalla == "llamada":
        _texto(c, remite, 0, -70, 44, "blanco", "sub")
        _texto(c, "llamando…", 0, -24, 30, "blanco", "ui")
        for x, col in ((-46, "verde"), (46, "rojo")):
            pieza(c, elipse(x, 120, 34, 34), col, 4)
    elif pantalla == "codigo":
        _texto(c, remite, 0, -112, 30, "tinta", "sub")
        _texto(c, "Tu código:", 0, -40, 32, "tinta", "ui")
        size = 64
        while _font(size, "sub").measureText(codigo) > 210 and size > 30:
            size -= 4
        f = _font(size, "sub")
        c.drawString(codigo, -f.measureText(codigo) / 2, 36, f, relleno("rojo"))
        _texto(c, "No lo compartas", 0, 110, 26, "gris", "ui")
    elif pantalla == "aviso":
        _texto(c, "!", 0, 30, 170, "blanco", "sub")
    else:
        _texto(c, remite, 0, -112, 30, "tinta", "sub")
        ls = lineas or [texto]
        h = 40 + 38 * len(ls)
        size = 30
        while max(_font(size, "ui").measureText(l) for l in ls) > 180 and size > 18:
            size -= 2
        f = _font(size, "ui")
        pieza(c, rrect(-104, -86, 104, -86 + h, 18), "blanco", 4)
        for i, l in enumerate(ls):
            c.drawString(l, -90, -86 + 40 + i * 38, f, relleno("tinta"))
    if suena:
        for k in range(3):
            a = (t * 3 + k / 3) % 1
            onda = skia.Paint(Color=skia.Color(28, 28, 34, int(200 * (1 - a))), AntiAlias=True, Style=skia.Paint.kStroke_Style,
                              StrokeWidth=6)
            for sx in (-1, 1):
                r = skia.Rect(-140 - 60 * a, -150 - 40 * a, 140 + 60 * a, -10 + 40 * a)
                c.drawArc(r, -30 if sx > 0 else 150, 60, False, onda)
        c.restore()
    _cara(c, 0, -290, 0.45, cara, t)


TIPOS = {
    "billete": billete, "fajo": fajo, "moneda": moneda, "hucha": hucha, "saco": saco,
    "contrato": contrato, "cartel": cartel, "checklist": checklist, "etiqueta": etiqueta, "bocadillo": bocadillo,
    "lupa": lupa, "calculadora": calculadora, "reloj": reloj, "llave": llave, "grafica": grafica, "flecha": flecha,
    "coche": coche, "bus": bus, "tren": tren, "arbol": arbol, "farola": farola, "nube": nube, "sol": sol, "movil": movil,
}
# tamaño aproximado (ancho, alto) a escala 1, para la cámara y la maquetación
TAMANO = {"billete": (300, 150), "fajo": (340, 220), "moneda": (180, 180), "hucha": (420, 320), "saco": (300, 300),
          "contrato": (280, 360), "cartel": (500, 200), "checklist": (600, 400), "etiqueta": (500, 140),
          "bocadillo": (500, 160), "lupa": (260, 320), "calculadora": (220, 320), "reloj": (260, 280), "llave": (300, 140),
          "grafica": (400, 320), "flecha": (260, 130), "coche": (480, 260), "bus": (700, 360), "tren": (900, 300),
          "arbol": (320, 440), "farola": (100, 470), "nube": (340, 160), "sol": (340, 340), "movil": (300, 480)}
# objetos cuyo (0, 0) es el suelo (el resto está centrado)
APOYADOS = {"arbol", "farola"}


def dibuja(c, tipo, t=0.0, **kw):
    if isinstance(tipo, dict):
        kw = {**tipo, **kw}
        tipo = kw.pop("tipo")
    TIPOS[tipo](c, t=t, **kw)
