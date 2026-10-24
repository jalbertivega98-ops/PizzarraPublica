"""Objetos del mundo dibujado (evolución visual de octubre de 2026): barcos, banderas, tratados, símbolos, atriles,
prismáticos y faros. Mismo estilo que los personajes pizarra: contorno negro, colores vivos, formas simpáticas.

Se registran en objetos.TIPOS al importar el paquete (ver objetos.py), así que en el storyboard se usan igual:
  {"type": "objeto", "objeto": "barco", "props": {"bandera": "marruecos", "numero": "613"}, "acciones": [{"at", "x", "dur"}]}

  barco      buque militar de perfil. props: color, bandera (espana|marruecos|otan|ue), numero, estela (true),
             _mov y _dir los pone el motor (estela larga y espuma en la proa cuando navega)
  bandera    mástil con bandera ondeando: espana | marruecos | otan | ue | ceuta. props: mastil (alto en px)
  documento  pergamino que se despliega. props: titulo, subtitulo, articulos [{id, titulo, lineas, clave}],
             resalta [ids de artículo] (subrayado amarillo animado), progreso (se despliega en "dibujo" s)
  otan       el símbolo de la OTAN dibujado (rosa de los vientos) en una chapa redonda
  atril      atril de mitin con el nombre del partido en su color. props: texto, color
  prismaticos  prismáticos (los sostiene un personaje con la pose "prismaticos")
  faro       faro de puerto con la luz girando
  barquito   barca de pesca que se mece (decorado de puerto)
"""
import math

import skia

from .estilo import COL, degradado, elipse, mezcla, pieza, poly, relleno, rgb, rrect, suave, texto_cartoon, trazo


def _font(size, cual="hand"):
    import wb
    return wb.font(cual, size)


def _texto(c, txt, x, y, size, color="tinta", cual="hand"):
    f = _font(size, cual)
    c.drawString(txt, x - f.measureText(txt) / 2, y, f, relleno(color))


def _eo(k):
    k = max(0.0, min(1.0, k))
    return 1 - (1 - k) ** 3


# ------------------------------------------------------------------ banderas
def _estrella5(cx, cy, r, ri=None, rot=-90):
    ri = ri or r * 0.4
    pts = []
    for i in range(10):
        a = math.radians(rot + i * 36)
        rr = r if i % 2 == 0 else ri
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return poly(pts)


def _pentagrama(c, cx, cy, r, color, w):
    """Estrella de cinco puntas solo con el trazo entrelazado (bandera de Marruecos)."""
    pts = [(cx + r * math.cos(math.radians(-90 + i * 144)), cy + r * math.sin(math.radians(-90 + i * 144))) for i in range(5)]
    p = poly(pts)
    c.drawPath(p, trazo(w, color))


def rosa_otan(c, x, y, r, fondo=(18, 40, 96), linea="blanco"):
    """Rosa de los vientos de la OTAN (cuatro puntas blancas y cuatro líneas) dentro de un círculo."""
    c.drawCircle(x, y, r, relleno(fondo))
    for a in (0, 90, 180, 270):
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        c.drawLine(x + ca * r * 0.62, y + sa * r * 0.62, x + ca * r * 0.98, y + sa * r * 0.98, trazo(r * 0.05, linea))
    c.drawCircle(x, y, r * 0.5, trazo(r * 0.045, linea))
    for a in (0, 90, 180, 270):
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        q = [(x + ca * r * 0.58, y + sa * r * 0.58)]
        for s in (-1, 1):
            b = math.radians(a + 90 * s)
            q.append((x + math.cos(b) * r * 0.14, y + math.sin(b) * r * 0.14))
        pts = [(x, y), q[1], q[0], q[2]]
        c.drawPath(poly([q[0], q[1], (x, y)]), relleno(linea))
        c.drawPath(poly([q[0], q[2], (x, y)]), relleno(mezcla(linea if isinstance(linea, tuple) else COL[linea], fondo, 0.25)))
        del pts


def tela(c, diseno, w, h, t=0.0, onda=1.0):
    """Tela de bandera de w×h que ondea (pegada al mástil por la izquierda, en (0, 0))."""
    n = 14
    filas = []

    def y_of(x, yy):
        a = onda * (x / w) * 14 * math.sin(t * 5 - x / w * 5.5)
        return yy + a

    def bandas(ys, colores):
        for (y0, y1), col in zip(ys, colores):
            p = skia.Path()
            xs = [w * i / n for i in range(n + 1)]
            p.moveTo(xs[0], y_of(xs[0], y0))
            for x in xs[1:]:
                p.lineTo(x, y_of(x, y0))
            for x in reversed(xs):
                p.lineTo(x, y_of(x, y1))
            p.close()
            c.drawPath(p, relleno(col))
            filas.append(p)

    def marco():
        p = skia.Path()
        xs = [w * i / n for i in range(n + 1)]
        p.moveTo(0, y_of(0, 0))
        for x in xs[1:]:
            p.lineTo(x, y_of(x, 0))
        for x in reversed(xs):
            p.lineTo(x, y_of(x, h))
        p.close()
        return p

    cx, cy = w * 0.5, y_of(w * 0.5, h * 0.5)
    if diseno == "espana":
        bandas([(0, h * 0.25), (h * 0.25, h * 0.75), (h * 0.75, h)], [(198, 11, 30), (255, 196, 0), (198, 11, 30)])
        # escudo simplificado (sin detalles heráldicos)
        sx, sy = w * 0.3, y_of(w * 0.3, h * 0.5)
        pieza(c, rrect(sx - h * 0.1, sy - h * 0.14, sx + h * 0.1, sy + h * 0.12, h * 0.04), (198, 11, 30), max(2, h * 0.02))
        c.drawRect(skia.Rect(sx - h * 0.1, sy - h * 0.2, sx + h * 0.1, sy - h * 0.15), relleno((255, 196, 0)))
    elif diseno == "marruecos":
        bandas([(0, h)], [(193, 39, 45)])
        _pentagrama(c, cx, cy, h * 0.26, (0, 98, 51), max(3, h * 0.05))
    elif diseno == "otan":
        bandas([(0, h)], [(18, 40, 96)])
        rosa_otan(c, cx, cy, h * 0.3)
    elif diseno == "ue":
        bandas([(0, h)], [(0, 51, 153)])
        for i in range(12):
            a = math.radians(i * 30)
            c.drawPath(_estrella5(cx + math.cos(a) * h * 0.33, cy + math.sin(a) * h * 0.33, h * 0.055), relleno((255, 204, 0)))
    elif diseno == "ceuta":  # gironado de ocho piezas blanco y negro (como la de Lisboa)
        c.save(); c.clipPath(marco(), skia.ClipOp.kIntersect, True)
        c.drawRect(skia.Rect(-10, -40, w + 10, h + 40), relleno("blanco"))
        R = w * 1.2
        for i in range(8):
            if i % 2:
                continue
            a0, a1 = math.radians(i * 45 - 90), math.radians((i + 1) * 45 - 90)
            c.drawPath(poly([(cx, cy), (cx + R * math.cos(a0), cy + R * math.sin(a0)), (cx + R * math.cos(a1), cy + R * math.sin(a1))]),
                       relleno((30, 30, 34)))
        c.restore()
        pieza(c, rrect(cx - h * 0.1, cy - h * 0.13, cx + h * 0.1, cy + h * 0.13, h * 0.05), "blanco", max(2, h * 0.02))
    elif diseno == "portugal":
        bandas([(0, h)], [(214, 30, 36)])
        c.save(); c.clipPath(marco(), skia.ClipOp.kIntersect, True)
        c.drawRect(skia.Rect(-10, -40, w * 0.4, h + 40), relleno((0, 102, 51)))
        c.restore()
        sx, sy = w * 0.4, y_of(w * 0.4, h * 0.5)
        c.drawCircle(sx, sy, h * 0.24, relleno((255, 220, 0)))
        pieza(c, rrect(sx - h * 0.12, sy - h * 0.14, sx + h * 0.12, sy + h * 0.14, h * 0.05), (214, 30, 36), max(2, h * 0.02))
    elif diseno == "castilla":  # cuartelado de castillos y leones (simplificado: rojo y blanco)
        bandas([(0, h * 0.5), (h * 0.5, h)], [(198, 11, 30), (250, 246, 236)])
        c.save(); c.clipPath(marco(), skia.ClipOp.kIntersect, True)
        c.drawRect(skia.Rect(w * 0.5, -40, w + 10, h * 0.5 + y_of(w * 0.75, 0)), relleno((250, 246, 236)))
        c.drawRect(skia.Rect(w * 0.5, h * 0.5 + y_of(w * 0.75, 0), w + 10, h + 40), relleno((198, 11, 30)))
        c.restore()
    elif diseno in ("argentina", "uruguay"):
        cel = (116, 172, 223)
        if diseno == "argentina":
            bandas([(0, h / 3), (h / 3, 2 * h / 3), (2 * h / 3, h)], [cel, "blanco", cel])
            c.drawCircle(cx, cy, h * 0.11, relleno((246, 180, 14)))
        else:
            ys = [(h * i / 9, h * (i + 1) / 9) for i in range(9)]
            bandas(ys, ["blanco" if i % 2 == 0 else (0, 56, 168) for i in range(9)])
            c.save(); c.clipPath(marco(), skia.ClipOp.kIntersect, True)
            c.drawRect(skia.Rect(-10, -40, w * 0.4, h * 5 / 9 + y_of(w * 0.2, 0)), relleno("blanco"))
            c.restore()
            c.drawCircle(w * 0.2, y_of(w * 0.2, h * 0.27), h * 0.13, relleno((252, 209, 22)))
    elif diseno == "cuba":
        ys = [(h * i / 5, h * (i + 1) / 5) for i in range(5)]
        bandas(ys, [(0, 42, 143) if i % 2 == 0 else "blanco" for i in range(5)])
        tri = poly([(0, y_of(0, 0)), (w * 0.45, y_of(w * 0.45, h * 0.5)), (0, y_of(0, h))])
        c.drawPath(tri, relleno((207, 20, 43)))
        c.drawPath(_estrella5(w * 0.15, y_of(w * 0.15, h * 0.5), h * 0.13), relleno("blanco"))
    elif diseno == "mexico":
        c.save(); c.clipPath(marco(), skia.ClipOp.kIntersect, True)
        for i, col in enumerate(((0, 104, 71), (255, 255, 255), (206, 17, 38))):
            c.drawRect(skia.Rect(w * i / 3, -40, w * (i + 1) / 3, h + 40), relleno(col))
        c.restore()
        c.drawCircle(cx, cy, h * 0.13, relleno((150, 100, 50)))
        c.drawCircle(cx, cy, h * 0.13, trazo(max(2, h * 0.02), (0, 104, 71)))
    elif diseno == "venezuela":
        bandas([(0, h / 3), (h / 3, 2 * h / 3), (2 * h / 3, h)], [(255, 204, 0), (0, 36, 125), (207, 20, 43)])
        for i in range(8):
            a = math.radians(200 + i * 140 / 7)
            c.drawPath(_estrella5(cx + math.cos(a) * h * 0.22, cy + h * 0.1 + math.sin(a) * h * 0.22, h * 0.035), relleno("blanco"))
    elif diseno == "brasil":
        bandas([(0, h)], [(0, 151, 57)])
        c.drawPath(poly([(cx - w * 0.4, cy), (cx, cy - h * 0.38), (cx + w * 0.4, cy), (cx, cy + h * 0.38)]), relleno((254, 221, 0)))
        c.drawCircle(cx, cy, h * 0.2, relleno((0, 39, 118)))
    elif diseno == "onu":
        bandas([(0, h)], [(0, 158, 219)])
        c.drawCircle(cx, cy, h * 0.24, trazo(max(2, h * 0.035), "blanco"))
        c.drawLine(cx - h * 0.24, cy, cx + h * 0.24, cy, trazo(max(2, h * 0.025), "blanco"))
        c.drawLine(cx, cy - h * 0.24, cx, cy + h * 0.24, trazo(max(2, h * 0.025), "blanco"))
    else:
        bandas([(0, h)], ["blanco"])
    c.drawPath(marco(), trazo(max(3, h * 0.035)))


def bandera(c, t=0.0, diseno="espana", mastil=360, ancho=200, alto=None, **kw):
    """(0, 0) = pie del mástil."""
    alto = alto or ancho * 0.66
    pieza(c, rrect(-8, -mastil, 8, 0, 6), (200, 200, 206), 4)
    c.drawCircle(0, -mastil - 6, 12, relleno("oro")); c.drawCircle(0, -mastil - 6, 12, trazo(4))
    c.save(); c.translate(8, -mastil + 6)
    tela(c, diseno, ancho, alto, t)
    c.restore()


def chincheta(c, t=0.0, diseno="espana", **kw):
    """Banderita clavada en el mapa (pin)."""
    bandera(c, t, diseno, mastil=150, ancho=110)
    c.drawCircle(0, 0, 10, relleno("tinta"))


# ------------------------------------------------------------------ barcos
def _estela(c, t, largo, mov):
    """Espuma detrás del barco: olitas blancas que se alejan y se abren en V."""
    n = 9
    for i in range(n):
        k = ((t * (1.6 if mov else 0.5) + i / n) % 1.0)
        x = 250 + k * largo
        abre = 18 + k * (90 if mov else 30)
        a = int(230 * (1 - k))
        for s in (-1, 1):
            c.drawCircle(x, 92 + s * abre * 0.25, 14 + 22 * k, relleno("blanco", a))
    p = skia.Path()
    p.moveTo(250, 100)
    p.lineTo(250 + largo, 100 - (40 if mov else 12))
    p.lineTo(250 + largo, 100 + (40 if mov else 12))
    p.close()
    c.drawPath(p, relleno((235, 248, 255), 150))


def barco(c, t=0.0, color=(150, 160, 172), bandera="espana", numero="", estela=True, _mov=False, _dir=0, cara=None, **kw):
    """Buque militar de perfil mirando a la izquierda (proa en x < 0); (0, 0) = centro, línea de flotación y = 90."""
    bob = 6 * math.sin(t * 2.2)
    rol = 1.5 * math.sin(t * 1.7 + 0.5)
    _dir = _dir or kw.get("rumbo", -1)
    c.save()
    if _dir > 0:  # navega hacia la derecha: se da la vuelta
        c.scale(-1, 1)
    if estela:
        _estela(c, t, 520 if _mov else 160, _mov)
    c.translate(0, bob); c.rotate(rol)
    osc = mezcla(color, "tinta", 0.35)
    # casco
    casco = poly([(-330, 20), (290, 20), (275, 110), (-250, 110)])
    pieza(c, casco, color, 7, shader=degradado(20, 110, mezcla(color, "blanco", 0.15), osc))
    c.drawLine(-320, 52, 284, 52, trazo(5, osc))
    if numero:
        _texto(c, str(numero), -150, 95, 44, "blanco", "sub")
    # superestructura, puente y mástil con radar
    pieza(c, rrect(-60, -80, 170, 22, 10), mezcla(color, "blanco", 0.2), 6)
    pieza(c, rrect(-30, -150, 110, -76, 10), mezcla(color, "blanco", 0.3), 6)
    for x in (-10, 30, 70):
        pieza(c, rrect(x, -134, x + 26, -110, 5), "cristal", 4)
    c.drawLine(40, -150, 40, -260, trazo(7))
    giro = math.sin(t * 4)
    pieza(c, rrect(40 - 46 * abs(giro), -246, 40 + 46 * abs(giro), -228, 6), (220, 224, 230), 4)
    # cañón de proa (pequeño y redondeado)
    pieza(c, elipse(-210, 6, 44, 26), mezcla(color, "blanco", 0.1), 5)
    pieza(c, rrect(-300, -6, -220, 8, 6), osc, 4)
    # bandera en popa (bandera=None: barco sin bandera, «alguien»)
    if not bandera:
        c.restore()
        _agua(c, bob)
        return
    c.drawLine(262, 20, 262, -110, trazo(5))
    c.save(); c.translate(262, -108)
    if _dir > 0:
        c.scale(-1, 1); c.translate(0, 0)
    tela(c, bandera, 110, 72, t, 0.8)
    c.restore()
    # espuma en la proa cuando navega
    if _mov:
        for i in range(4):
            k = (t * 3 + i / 4) % 1
            c.drawCircle(-330 - 30 * k, 92 - 30 * k, 12 + 10 * (1 - k), relleno("blanco", int(240 * (1 - k))))
    c.restore()
    _agua(c, bob)


def _agua(c, bob):
    """Agua por delante del casco (el barco «se hunde» en el mar)."""
    p = skia.Path()
    p.moveTo(-380, 104 + bob)
    for i in range(16):
        x = -380 + i * 50
        p.quadTo(x + 12, 94 + bob, x + 25, 104 + bob)
        p.quadTo(x + 37, 114 + bob, x + 50, 104 + bob)
    p.lineTo(420, 160); p.lineTo(-380, 160); p.close()
    c.drawPath(p, relleno((118, 190, 234), 240))
    c.drawPath(p, trazo(4, (60, 120, 175), 200))


def barquito(c, t=0.0, color="rojo", **kw):
    bob = 5 * math.sin(t * 2 + kw.get("fase", 0))
    c.save(); c.translate(0, bob); c.rotate(3 * math.sin(t * 1.6 + kw.get("fase", 0)))
    pieza(c, poly([(-120, 0), (120, 0), (90, 50), (-90, 50)]), color, 5)
    c.drawLine(-110, 16, 110, 16, trazo(4, "blanco"))
    c.drawLine(0, 0, 0, -110, trazo(5))
    pieza(c, poly([(6, -104), (6, -10), (80, -14)]), "blanco", 4)
    c.restore()


def faro(c, t=0.0, **kw):
    """(0, 0) = base."""
    pieza(c, poly([(-60, 0), (60, 0), (36, -300), (-36, -300)]), "blanco", 6)
    for y0 in (-90, -200):
        c.save(); c.clipPath(poly([(-60, 0), (60, 0), (36, -300), (-36, -300)]))
        c.drawRect(skia.Rect(-70, y0 - 40, 70, y0), relleno("rojo"))
        c.restore()
    c.drawPath(poly([(-60, 0), (60, 0), (36, -300), (-36, -300)]), trazo(6))
    pieza(c, rrect(-50, -380, 50, -300, 12), "luz", 6)
    pieza(c, poly([(-56, -380), (56, -380), (0, -430)]), "rojo", 6)
    a = t * 2.5
    for s in (0, math.pi):
        dx = math.cos(a + s)
        p = poly([(0, -340), (dx * 420, -400), (dx * 420, -280)])
        c.drawPath(p, relleno((255, 245, 180), int(110 * abs(dx))))


# ------------------------------------------------------------------ papeles y símbolos
def documento(c, t=0.0, titulo="TRATADO", subtitulo="", articulos=(), resalta=(), progreso=1.0, _cambios=(), ancho=760, **kw):
    """Pergamino que se despliega de arriba abajo; (0, 0) = centro."""
    alto_total = 140 + sum(70 + 54 * len(a.get("lineas", [])) for a in articulos) + 40
    k = _eo(progreso)
    alto = max(60, alto_total * k)
    y0 = -alto_total / 2
    papel = (250, 240, 214)
    c.save()
    c.clipRect(skia.Rect(-ancho / 2 - 40, y0 - 40, ancho / 2 + 40, y0 + alto + 10))
    hoja = rrect(-ancho / 2, y0, ancho / 2, y0 + alto_total, 18)
    pieza(c, hoja, papel, 7, shader=degradado(y0, y0 + alto_total, (255, 248, 226), (240, 226, 192)))
    y = y0 + 90
    ft = _font(50, "sub")
    _texto(c, titulo, 0, y, min(50, 50 * (ancho - 70) / max(1, ft.measureText(titulo))), "tinta", "sub")
    if subtitulo:
        _texto(c, subtitulo, 0, y + 46, 32, (120, 100, 80))
    y += 100
    vistos = {}
    for tc, props in _cambios:
        for r in props.get("resalta", []) or []:
            vistos.setdefault(r, tc)
    for a in articulos:
        res = a.get("id") in resalta
        kr = _eo((t - vistos.get(a.get("id"), -9)) / 0.5) if res else 0.0
        _texto(c, a.get("titulo", ""), 0, y, 40, "rojo" if res else "tinta", "sub")
        y += 60
        for i, ln in enumerate(a.get("lineas", [])):
            f = _font(36)
            wln = f.measureText(ln)
            if kr > 0:  # subrayado de rotulador fosforito que se pinta de izquierda a derecha
                kk = max(0.0, min(1.0, kr * len(a["lineas"]) - i))
                if kk > 0:
                    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-wln / 2 - 10, y - 34, -wln / 2 - 10 + (wln + 20) * kk, y + 10), 8, 8),
                                relleno((255, 226, 60), 210))
            c.drawString(ln, -wln / 2, y, f, relleno((60, 50, 40)))
            y += 54
        y += 10
    c.restore()
    # rodillos arriba y abajo (el de abajo baja al desplegarse)
    for yy in (y0 - 6, y0 + alto + 6):
        pieza(c, rrect(-ancho / 2 - 34, yy - 22, ancho / 2 + 34, yy + 22, 22), (214, 180, 120), 6)
        for sx in (-1, 1):
            pieza(c, elipse(sx * (ancho / 2 + 40), yy, 16, 28), (170, 120, 70), 5)


def otan(c, t=0.0, r=170, **kw):
    """Chapa con el símbolo de la OTAN."""
    pieza(c, elipse(0, 0, r + 22, r + 22), (230, 232, 238), 7)
    rosa_otan(c, 0, 0, r)
    c.drawCircle(0, 0, r, trazo(5))
    if kw.get("texto", True):
        texto_cartoon(c, "OTAN", 0, r + 90, 70, color="blanco", fuente="sub")


def atril(c, t=0.0, texto="", color="gris", **kw):
    """Atril de mitin: (0, 0) = suelo. El personaje va detrás (se dibuja antes)."""
    col = COL.get(color, (150, 150, 150)) if isinstance(color, str) else color
    pieza(c, poly([(-150, -330), (150, -330), (120, 0), (-120, 0)]), (246, 246, 250), 7,
          shader=degradado(-330, 0, (255, 255, 255), (220, 224, 232)))
    pieza(c, poly([(-170, -370), (170, -370), (156, -326), (-156, -326)]), (90, 94, 104), 6)
    c.drawRect(skia.Rect(-128, -250, 128, -170), relleno(col))
    c.drawRect(skia.Rect(-128, -250, 128, -170), trazo(5))
    if texto:
        f = _font(64, "sub")
        size = 64 if f.measureText(texto) < 230 else 64 * 230 / f.measureText(texto)
        _texto(c, texto, 0, -190, size, "blanco", "sub")
    # micrófono
    c.drawLine(60, -370, 90, -440, trazo(6))
    pieza(c, elipse(94, -450, 16, 20), (60, 60, 66), 4)


def prismaticos(c, t=0.0, **kw):
    for sx in (-1, 1):
        pieza(c, rrect(sx * 64 - 44, -40, sx * 64 + 44, 70, 22), (60, 64, 76), 6)
        pieza(c, elipse(sx * 64, -40, 40, 18), (140, 200, 240), 5)
        c.drawPath(elipse(sx * 64 - 10, -44, 12, 5), relleno("blanco", 200))
    pieza(c, rrect(-26, -10, 26, 30, 8), (90, 94, 106), 5)


def sello(c, t=0.0, texto="CONFIRMADO", color="verde", **kw):
    """Sello de tinta torcido (hechos confirmados / declaraciones / en discusión)."""
    col = COL.get(color, (60, 170, 90)) if isinstance(color, str) else color
    f = _font(58, "sub")
    w = f.measureText(texto) + 60
    c.save(); c.rotate(-6)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-w / 2, -50, w / 2, 40), 14, 14), relleno("blanco", 235))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-w / 2, -50, w / 2, 40), 14, 14), trazo(8, col))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-w / 2 + 10, -40, w / 2 - 10, 30), 10, 10), trazo(3, col))
    _texto(c, texto, 0, 12, 58, col, "sub")
    c.restore()


TIPOS = {"barco": barco, "barquito": barquito, "faro": faro, "bandera": bandera, "chincheta": chincheta,
         "documento": documento, "otan": otan, "atril": atril, "prismaticos": prismaticos, "sello": sello}
TAMANO = {"barco": (680, 420), "barquito": (260, 170), "faro": (140, 440), "bandera": (240, 400), "chincheta": (140, 180),
          "documento": (840, 900), "otan": (420, 520), "atril": (340, 450), "prismaticos": (240, 140), "sello": (520, 120)}
APOYADOS = {"faro", "bandera", "chincheta", "atril"}
