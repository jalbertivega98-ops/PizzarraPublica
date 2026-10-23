"""Personajes-pizarra de Pizarra Pública (biblioteca fija: mismos diseños en todos los vídeos).

Cada personaje es una pizarra con marco, ojos grandes, brazos de manguera con guantes blancos,
piernas con zapatillas y accesorios propios. Se dibuja por piezas para poder animarlo:
cara (expresión), brazos (pose), mirada, parpadeo, boca al hablar, pasos al andar, saltos.

Coordenadas locales: centro de la pizarra en (0, 0), pizarra de 300 × 380, pies en y ≈ 330.
"""
import math

import numpy as np
import skia

from .estilo import (COL, TINTA, degradado, elipse, manguera, pieza, poly, relleno, rgb, rrect, sombra_suelo,
                     suave, trazo)

W2, H2 = 150, 190  # media anchura / altura de la pizarra
OJOS_Y = -48
BOCA_Y = 52

# ------------------------------------------------------------------ fichas de personaje
PERSONAJES = {
    "piz": dict(nombre="Piz", papel="El protagonista", cara="normal", marco="marco", acento="rojo",
                garabatos=("bombilla", "barras"), zapatilla="rojo", rotulador=True,
                descripcion="Curioso, entusiasta y cercano. Es quien vive las historias."),
    "profe": dict(nombre="Profe Piza", papel="El experto", cara="normal", marco="marco", acento="azul",
                  garabatos=("lineas",), zapatilla="gris", gafas="redondas", bigote=True, pajarita="azul",
                  birrete=True, descripcion="Aporta datos y contexto. Garantiza que todo sea riguroso."),
    "critica": dict(nombre="Piza Crítica", papel="La escéptica", cara="esceptica", marco="marco", acento="rosa",
                    canto="rosa", pestanas=True, garabatos=("flecha",), zapatilla="negro",
                    descripcion="Cuestiona y detecta las contradicciones."),
    "pizon": dict(nombre="Pizón", papel="El dubitativo", cara="confundido", marco="marco", acento="azul",
                  garabatos=("grafica",), zapatilla="negro", estrecho=True,
                  descripcion="Hace las preguntas que todos nos hacemos."),
    "sarcastica": dict(nombre="Piza Sarcástica", papel="La irónica", cara="burla", marco="marco", acento="verde",
                       gafas="sol", garabatos=("barras",), zapatilla="rojo",
                       descripcion="Señala lo absurdo con humor."),
    "indignada": dict(nombre="Piza Indignada", papel="La indignada", cara="indignado", marco="marco", acento="rojo",
                      garabatos=("tachon",), zapatilla="rojo", melena=True,
                      descripcion="Se enfada con las injusticias y las incoherencias."),
    # extras del mundo (no protagonistas)
    "banquero": dict(nombre="Pizarra banquera", papel="Trabaja en el banco", cara="normal", marco="marco_oscuro",
                     acento="azul", corbata="azul", garabatos=("euro",), zapatilla="negro"),
    "banquera_seria": dict(nombre="Pizarra de riesgos", papel="Analiza tu hipoteca", cara="serio", marco="marco_oscuro",
                           acento="azul", gafas="cuadradas", corbata="azul", garabatos=("lineas",), zapatilla="negro"),
    "hacienda": dict(nombre="Pizarra de Hacienda", papel="Cobra impuestos", cara="normal", marco="marco_oscuro",
                     acento="amarillo", corbata="rojo", visera=True, garabatos=("porcentaje",), zapatilla="negro"),
    # candidatos (verano 2026): pizarras reconocibles por el pelo, la barba y la chapa con el nombre; sin caricatura
    "sanchez": dict(nombre="Pedro Sánchez", papel="Candidato del PSOE", cara="normal", marco="marco", acento="psoe",
                    pelo=((105, 100, 106), "corto"), chapa=("SÁNCHEZ", "psoe"), zapatilla="blanco", garabatos=()),
    "feijoo": dict(nombre="Alberto Núñez Feijóo", papel="Candidato del PP", cara="normal", marco="marco", acento="pp",
                   pelo=((222, 222, 226), "canoso"), chapa=("FEIJÓO", "pp"), zapatilla="azul", garabatos=()),
    "abascal": dict(nombre="Santiago Abascal", papel="Candidato de Vox", cara="normal", marco="marco", acento="vox",
                    pelo=((50, 44, 44), "corto"), barba=(60, 52, 52), chapa=("ABASCAL", "vox"), zapatilla="verde_osc",
                    garabatos=()),
    # creadores de contenido (oct. 2026): misma regla, chapa con el nombre y sin caricatura
    "wild": dict(nombre="Jordi Wild", papel="Presentador de The Wild Project", cara="normal", marco="marco", acento="gris",
                 pelo=((40, 36, 36), "corto"), barba=(46, 40, 40), chapa=("JORDI WILD", "tinta"), zapatilla="negro", garabatos=()),
    "broncano": dict(nombre="David Broncano", papel="Presentador de La Revuelta (La 1)", cara="normal", marco="marco", acento="gris",
                     pelo=((62, 46, 36), "corto"), barba=(78, 60, 48), chapa=("BRONCANO", "rojo"), zapatilla="blanco", garabatos=()),
    "colau": dict(nombre="Ada Colau", papel="Candidata del Frente Amplio", cara="normal", marco="marco", acento="gris",
                  melena=(70, 50, 40), pelo=((70, 50, 40), "corto"), chapa=("COLAU", "gris"), zapatilla="negro", garabatos=()),
    "diputado": dict(nombre="Pizarra diputada", papel="Un diputado cualquiera (sin partido)", cara="normal", marco="marco_oscuro",
                     acento="gris", corbata="tinta", chapa=("DIPUTADO", "gris"), zapatilla="negro", garabatos=("euro",)),
    # caso Diputación de Badajoz (2026): sin caricatura, solo la chapa con el nombre y sin colores de partido
    "david": dict(nombre="David Sánchez", papel="Hermano del presidente del Gobierno", cara="normal", marco="marco", acento="gris",
                  pelo=((70, 62, 60), "corto"), chapa=("DAVID S.", "gris"), zapatilla="negro", garabatos=()),
    "gallardo": dict(nombre="Miguel Ángel Gallardo", papel="Expresidente de la Diputación de Badajoz", cara="normal", marco="marco_oscuro",
                     acento="gris", pelo=((222, 222, 226), "canoso"), corbata="tinta", chapa=("GALLARDO", "gris"), zapatilla="negro",
                     garabatos=()),
    # fichaje del PP por Barcelona (oct. 2026): misma regla, pelo rapado a los lados y chapa con el apellido
    "albiol": dict(nombre="Xavier García Albiol", papel="Alcalde de Badalona y candidato del PP por Barcelona", cara="normal",
                   marco="marco", acento="pp", pelo=((96, 90, 92), "rapado"), chapa=("ALBIOL", "pp"), zapatilla="azul",
                   garabatos=()),
    "jueza": dict(nombre="La jueza", papel="Instruye la causa", cara="serio", marco="marco_oscuro", acento="gris", gafas="cuadradas",
                  melena=True, chapa=("JUEZA", "tinta"), zapatilla="negro", garabatos=()),
    "estafador": dict(nombre="El estafador", papel="Se hace pasar por tu banco", cara="burla", marco="marco_oscuro",
                      acento="gris", antifaz=True, corbata="tinta", garabatos=("euro",), zapatilla="negro"),
}

# ------------------------------------------------------------------ expresiones
# ojo: escala, parpado (0 abierto … 1 cerrado), inclinación del párpado (enfado <0, pena >0), tam. pupila
# cejas: (alto, ángulo izq, ángulo der) · boca: tipo · extra: adornos alrededor
EXPRESIONES = {
    "normal":      dict(ojo=1.0, parpado=0.0, pupila=1.0, cejas=(0, 8, -8), boca="sonrisa"),
    "sorpresa":    dict(ojo=1.18, parpado=0.0, pupila=0.7, cejas=(-22, 12, -12), boca="o", extra="exclamacion"),
    "pensativo":   dict(ojo=1.0, parpado=0.15, pupila=1.0, cejas=(-8, -6, 14), boca="lado", mira=(10, -12), extra="pregunta"),
    "ilusionado":  dict(ojo=1.08, parpado=0.0, pupila=1.15, cejas=(-14, 10, -10), boca="grande", extra="destellos"),
    "preocupado":  dict(ojo=1.0, parpado=0.1, pupila=0.9, cejas=(-6, -16, 16), boca="ondulada", extra="sudor"),
    "riendo":      dict(ojo=1.0, parpado=1.0, pupila=1.0, cejas=(-12, 10, -10), boca="risa", cerrados="feliz"),
    "indignado":   dict(ojo=1.0, parpado=0.38, inclina=-1, pupila=0.85, cejas=(10, -26, 26), boca="grito", extra="rayos"),
    "confundido":  dict(ojo=0.95, parpado=0.1, pupila=0.9, cejas=(-4, 14, -2), boca="ondulada", mira=(8, 0), extra="pregunta"),
    "idea":        dict(ojo=1.05, parpado=0.0, pupila=1.0, cejas=(-12, 10, -10), boca="sonrisa", extra="bombilla"),
    "susto":       dict(ojo=1.25, parpado=0.0, pupila=0.55, cejas=(-26, 18, -18), boca="dientes", extra="sudor"),
    "triste":      dict(ojo=1.0, parpado=0.3, inclina=1, pupila=1.0, cejas=(-4, -18, 18), boca="triste", extra="lagrima"),
    "enfado":      dict(ojo=1.0, parpado=0.35, inclina=-1, pupila=0.9, cejas=(8, -22, 22), boca="enfado", extra="vapor"),
    "esceptica":   dict(ojo=0.95, parpado=0.45, pupila=1.0, cejas=(2, -4, 16), boca="lado", mira=(10, 0), pestanas=True),
    "burla":       dict(ojo=1.0, parpado=0.3, pupila=1.0, cejas=(-4, 12, -2), boca="burla"),
    "serio":       dict(ojo=0.95, parpado=0.4, pupila=0.9, cejas=(4, -10, 10), boca="plana"),
    "vacio":       dict(ojo=0.95, parpado=0.25, pupila=0.6, cejas=(0, 0, 0), boca="plana"),
}
# pose de brazos que acompaña a cada cara si no se elige otra
BRAZOS_DE = {"sorpresa": "arriba", "pensativo": "piensa", "ilusionado": "puno", "preocupado": "manos_juntas",
             "indignado": "punos", "susto": "cabeza", "idea": "pulgar", "triste": "caidos", "enfado": "jarras",
             "esceptica": "cruzados", "confundido": "encoge", "burla": "senala"}


# ------------------------------------------------------------------ guantes y zapatillas
def guante(c, x, y, ang, tipo="abierto", s=1.0, lado=1):
    """Guante blanco de dibujo animado. ang = dirección del antebrazo (grados)."""
    c.save()
    c.translate(x, y)
    c.rotate(ang + 90)
    c.scale(s * lado, s)
    w = 4.5
    sh = ("guante_sombra",)
    # puño de la manga (rollito)
    pieza(c, rrect(-20, -14, 20, 4, 8), "blanco", w)
    if tipo == "puno":
        pieza(c, suave([(-24, 2), (24, 2), (28, 26), (20, 46), (-18, 46), (-28, 26)]), "blanco", w,
              sombra=(elipse(8, 40, 22, 10), sh[0]))
        for i in range(3):
            c.drawPath(suave([(-14 + i * 11, 30), (-12 + i * 11, 44)], close=False), trazo(3.5))
    elif tipo in ("senala", "pulgar", "arriba"):
        pieza(c, suave([(-22, 2), (22, 2), (26, 24), (18, 44), (-16, 44), (-26, 24)]), "blanco", w,
              sombra=(elipse(8, 38, 20, 9), sh[0]))
        if tipo == "pulgar":  # pulgar hacia arriba (perpendicular al brazo)
            pieza(c, rrect(-40, 4, -14, 20, 9), "blanco", w)
        else:  # índice estirado
            pieza(c, rrect(-8, 38, 8, 84, 8), "blanco", w)
    else:  # abierto: palma + 4 dedos
        pieza(c, elipse(0, 28, 26, 24), "blanco", w, sombra=(elipse(8, 40, 24, 12), sh[0]))
        for i, (dx, ln) in enumerate(((-17, 30), (-6, 38), (6, 38), (17, 32))):
            pieza(c, rrect(dx - 6.5, 36, dx + 6.5, 36 + ln, 6.5), "blanco", w)
        pieza(c, rrect(-42, 14, -18, 28, 7), "blanco", w)  # pulgar
    c.restore()


def zapatilla(c, x, y, lado=1, color="rojo", s=1.0, lev=0.0):
    """Zapatilla de deporte blanca con detalles de color; lado=1 mira a la derecha."""
    c.save()
    c.translate(x, y)
    c.scale(s * lado, s)
    c.rotate(-8 * lev)
    w = 5
    col = COL.get(color, COL["rojo"]) if color != "negro" else COL["tinta"]
    suela = suave([(-34, -2), (52, -2), (60, 10), (52, 20), (-34, 20), (-42, 10)])
    pieza(c, suela, "gris_claro", w)
    cuerpo = suave([(-34, 0), (-30, -34), (-6, -40), (18, -26), (44, -16), (58, -2), (40, 4), (-28, 4)])
    pieza(c, cuerpo, "blanco", w, sombra=(elipse(-10, 0, 40, 12), "guante_sombra"))
    c.drawPath(suave([(-26, -10), (-4, -14), (20, -4)], close=False), trazo(7, col))  # franja
    pieza(c, elipse(46, -6, 9, 7), col, 3.5)  # puntera de color
    for i in range(3):
        c.drawLine(-6 + i * 9, -34 + i * 4, 4 + i * 9, -30 + i * 4, trazo(3))
    c.restore()


# ------------------------------------------------------------------ garabatos del tablero
def garabatos(c, tipos, alpha=255):
    for g in tipos:
        if g == "bombilla":
            c.drawPath(elipse(-92, -128, 16, 18), trazo(4, "amarillo", alpha))
            c.drawPath(poly([(-100, -112), (-84, -112), (-86, -100), (-98, -100)], False), trazo(4, "amarillo", alpha))
            for a in range(-150, -20, 32):
                r = math.radians(a)
                c.drawLine(-92 + 26 * math.cos(r), -128 + 26 * math.sin(r), -92 + 34 * math.cos(r),
                           -128 + 34 * math.sin(r), trazo(3, "amarillo", alpha))
        elif g == "barras":
            for i, h in enumerate((22, 36, 52)):
                x = 52 + i * 22
                c.drawPath(poly([(x, 150), (x, 150 - h), (x + 14, 150 - h), (x + 14, 150)], False),
                           trazo(4, ("naranja", "amarillo", "rojo")[i], alpha))
            c.drawPath(suave([(44, 140), (80, 118), (118, 92)], close=False), trazo(3.5, "rojo", alpha))
        elif g == "grafica":
            c.drawPath(poly([(48, 150), (70, 126), (90, 138), (118, 104)], False), trazo(4, "azul", alpha))
            c.drawPath(poly([(44, 100), (44, 152), (124, 152)], False), trazo(3, "azul", alpha))
        elif g == "lineas":
            for i in range(3):
                c.drawLine(40, 108 + i * 16, 118 - i * 18, 108 + i * 16, trazo(3.5, "azul_claro", alpha))
        elif g == "flecha":
            c.drawPath(suave([(56, 150), (88, 128), (114, 110)], close=False), trazo(4, "rosa", alpha))
            c.drawPath(poly([(100, 106), (116, 108), (110, 122)], False), trazo(4, "rosa", alpha))
        elif g == "euro":
            c.drawPath(elipse(90, 128, 22, 22), trazo(4, "verde", alpha))
            c.drawLine(76, 124, 96, 124, trazo(3, "verde", alpha))
            c.drawLine(76, 134, 96, 134, trazo(3, "verde", alpha))
        elif g == "porcentaje":
            c.drawLine(70, 150, 112, 104, trazo(4, "rojo", alpha))
            c.drawPath(elipse(74, 110, 7, 7), trazo(4, "rojo", alpha))
            c.drawPath(elipse(108, 144, 7, 7), trazo(4, "rojo", alpha))
        elif g == "tachon":
            c.drawPath(poly([(54, 112), (70, 150), (86, 112), (102, 150), (118, 112)], False), trazo(4, "rojo", alpha))


# ------------------------------------------------------------------ cara
def ojo(c, x, y, s, parp, inclina, pup, mira, lado, cerrados=None, pestanas=False):
    rx, ry = 38 * s, 50 * s
    if cerrados == "feliz":  # ojos cerrados de risa: ^ ^
        p = skia.Path()
        p.moveTo(x - rx * 0.8, y + 6)
        p.quadTo(x, y - ry * 0.9, x + rx * 0.8, y + 6)
        c.drawPath(p, trazo(7))
        return
    blanco = elipse(x, y, rx, ry)
    c.drawPath(blanco, relleno("blanco"))
    c.save()
    c.clipPath(blanco, skia.ClipOp.kIntersect, True)
    px, py = x + mira[0] * 1.2, y + 8 * s + mira[1] * 1.2
    c.drawOval(skia.Rect(px - 15 * pup * s, py - 20 * pup * s, px + 15 * pup * s, py + 20 * pup * s), relleno("tinta"))
    c.drawOval(skia.Rect(px - 6 * s, py - 12 * pup * s, px + 1 * s, py - 4 * pup * s), relleno("blanco"))
    if parp > 0:  # párpado superior (color pizarra) con inclinación
        drop = -ry + 2 * ry * parp
        tilt = 16 * s * inclina * lado
        lid = poly([(x - rx - 4, y - ry - 6), (x + rx + 4, y - ry - 6), (x + rx + 4, y + drop + tilt),
                    (x - rx - 4, y + drop - tilt)])
        c.drawPath(lid, relleno("pizarra"))
        c.drawLine(x - rx, y + drop - tilt * 0.9, x + rx, y + drop + tilt * 0.9, trazo(6))
    c.restore()
    c.drawPath(blanco, trazo(6))
    if pestanas:
        for i in range(3):
            a = math.radians(-150 + i * 22) if lado < 0 else math.radians(-30 - i * 22)
            c.drawLine(x + rx * 0.9 * math.cos(a), y + ry * 0.9 * math.sin(a), x + (rx + 14) * math.cos(a),
                       y + (ry + 14) * math.sin(a), trazo(4))


def boca(c, tipo, abre=0.0, s=1.0):
    """abre (0-1) abre la boca al hablar."""
    y = BOCA_Y
    if abre > 0.05 and tipo in ("sonrisa", "plana", "lado", "burla", "serio", "triste", "ondulada"):
        tipo = "habla"
    if tipo in ("sonrisa", "grande", "risa", "habla", "grito", "enfado", "dientes"):
        w = {"sonrisa": 62, "grande": 74, "risa": 80, "habla": 46, "grito": 52, "enfado": 44, "dientes": 54}[tipo]
        d = {"sonrisa": 62, "grande": 80, "risa": 92, "habla": 26 + 46 * abre, "grito": 70, "enfado": 30,
             "dientes": 34}[tipo]
        p = skia.Path()
        if tipo in ("grito", "enfado"):  # boca abierta hacia abajo
            p.moveTo(-w, y + d * 0.55)
            p.cubicTo(-w * 0.8, y - d * 0.15, w * 0.8, y - d * 0.15, w, y + d * 0.55)
            p.cubicTo(w * 0.7, y + d, -w * 0.7, y + d, -w, y + d * 0.55)
        else:
            top = 4 if tipo != "habla" else -4
            p.moveTo(-w, y + top - 10)
            p.quadTo(0, y + top + 6, w, y + top - 10)
            p.cubicTo(w * 0.85, y + d, -w * 0.85, y + d, -w, y + top - 10)
        p.close()
        c.drawPath(p, relleno("boca"))
        c.save()
        c.clipPath(p, skia.ClipOp.kIntersect, True)
        if tipo in ("grito", "dientes", "enfado"):
            c.drawRect(skia.Rect(-w, y - 40, w, y + (8 if tipo != "dientes" else 16)), relleno("blanco"))
            if tipo == "dientes":
                for i in range(-3, 4):
                    c.drawLine(i * 14, y - 4, i * 14, y + 18, trazo(3))
        if tipo != "dientes":
            c.drawOval(skia.Rect(-w * 0.55, y + d * 0.55, w * 0.55, y + d * 1.25), relleno("lengua"))
        c.restore()
        c.drawPath(p, trazo(6))
        return
    p = skia.Path()
    if tipo == "o":
        c.drawOval(skia.Rect(-22, y - 8, 22, y + 46), relleno("boca"))
        c.drawOval(skia.Rect(-14, y + 22, 14, y + 42), relleno("lengua"))
        c.drawOval(skia.Rect(-22, y - 8, 22, y + 46), trazo(6))
        return
    if tipo == "lado":
        p.moveTo(-26, y + 18)
        p.quadTo(10, y + 26, 34, y + 4)
    elif tipo == "burla":
        p.moveTo(-34, y + 14)
        p.quadTo(4, y + 30, 40, y)
        c.drawPath(p, trazo(7))
        c.drawLine(34, y - 4, 44, y + 6, trazo(5))
        return
    elif tipo == "ondulada":
        p.moveTo(-36, y + 22)
        p.cubicTo(-20, y + 6, -8, y + 34, 6, y + 18)
        p.cubicTo(18, y + 4, 28, y + 30, 38, y + 16)
    elif tipo == "triste":
        p.moveTo(-34, y + 34)
        p.quadTo(0, y + 2, 34, y + 34)
    else:  # plana / serio / vacio
        p.moveTo(-30, y + 20)
        p.lineTo(30, y + 18)
    c.drawPath(p, trazo(7))


def cejas(c, alto, ai, ad, s=1.0):
    for x, a in ((-45, ai), (45, ad)):
        c.save()
        c.translate(x, OJOS_Y - 66 * s + alto)
        c.rotate(a)
        p = skia.Path()
        p.moveTo(-26, 4)
        p.quadTo(0, -10, 26, 4)
        c.drawPath(p, trazo(8))
        c.restore()


def adornos(c, extra, t):
    if extra == "exclamacion":
        for dx, ang in ((-170, -25), (-140, -5)):
            c.save(); c.translate(dx, -230); c.rotate(ang)
            c.drawLine(0, -26, 0, 8, trazo(9, "rojo")); c.drawCircle(0, 24, 5, relleno("rojo")); c.restore()
    elif extra == "pregunta":
        import wb
        f = wb.font("hand", 92)
        c.drawString("?", 120, -200 + 6 * math.sin(t * 4), f, relleno("azul"))
    elif extra == "destellos":
        for i, (dx, dy) in enumerate(((-60, -250), (0, -270), (60, -250))):
            k = 0.8 + 0.2 * math.sin(t * 8 + i)
            c.drawLine(dx * 1.0, dy, dx * 1.25, dy - 30 * k, trazo(8, "amarillo"))
    elif extra == "sudor":
        for i, (dx, dy) in enumerate(((168, -120), (186, -78))):
            p = skia.Path()
            y = dy + (t * 40 + i * 20) % 30
            p.moveTo(dx, y - 22); p.quadTo(dx + 13, y, dx, y + 9); p.quadTo(dx - 13, y, dx, y - 22)
            pieza(c, p, "azul_claro", 3.5)
    elif extra == "lagrima":
        p = skia.Path()
        y = OJOS_Y + 50 + (t * 60) % 60
        p.moveTo(-48, y - 18); p.quadTo(-36, y, -48, y + 8); p.quadTo(-60, y, -48, y - 18)
        pieza(c, p, "azul_claro", 3.5)
    elif extra == "rayos":
        for dx, ang in ((-150, -20), (150, 20), (0, 0)):
            c.save(); c.translate(dx, -236 + abs(dx) * 0.2); c.rotate(ang)
            c.drawPath(poly([(-10, -28), (6, -6), (-4, -4), (10, 24)], False), trazo(7, "rojo"))
            c.restore()
    elif extra == "vapor":
        for sx in (-1, 1):
            k = (t * 2) % 1
            c.drawPath(elipse(sx * (150 + 30 * k), -200 - 50 * k, 16 + 14 * k, 12 + 10 * k),
                       relleno("gris_claro", int(220 * (1 - k))))
    elif extra == "bombilla":
        c.save(); c.translate(150, -250)
        c.drawCircle(0, 0, 44, relleno("amarillo", 90))
        pieza(c, elipse(0, -4, 26, 28), "amarillo", 5)
        pieza(c, rrect(-13, 22, 13, 40, 4), "gris", 4)
        c.restore()


# ------------------------------------------------------------------ brazos
# mano (x, y), tipo de guante, curvatura del brazo
POSES = {
    "normal":   (((-236, 150), "abierto", -0.3), ((236, 150), "abierto", 0.3)),
    "saluda":   (((-236, 150), "abierto", -0.3), ((262, -170), "abierto", -0.35)),
    "senala":   (((-236, 150), "abierto", -0.3), ((300, -30), "senala", -0.15)),
    "senala_izq": (((-300, -30), "senala", 0.15), ((236, 150), "abierto", 0.3)),
    "senala_arriba": (((-236, 150), "abierto", -0.3), ((236, -240), "senala", -0.25)),
    "arriba":   (((-232, -222), "abierto", 0.3), ((232, -222), "abierto", -0.3)),
    "jarras":   (((-160, 98), "puno", -0.9), ((160, 98), "puno", 0.9)),
    "punos":    (((-130, 40), "puno", -0.5), ((130, 40), "puno", 0.5)),
    "puno":     (((-196, 128), "abierto", -0.25), ((200, -150), "puno", -0.3)),
    "piensa":   (((-236, 150), "abierto", -0.3), ((70, 120), "senala", 0.6)),
    "cruzados": (((60, 96), "puno", 0.15), ((-60, 110), "puno", -0.15)),
    "manos_juntas": (((-30, 150), "puno", 0.5), ((30, 150), "puno", -0.5)),
    "cabeza":   (((-150, -212), "abierto", 0.7), ((150, -212), "abierto", -0.7)),
    "pulgar":   (((-236, 150), "abierto", -0.3), ((250, 30), "pulgar", -0.3)),
    "caidos":   (((-200, 196), "abierto", -0.08), ((200, 196), "abierto", 0.08)),
    "encoge":   (((-262, -40), "abierto", 0.35), ((262, -40), "abierto", -0.35)),
    "prismaticos": (((-120, -30), "puno", 0.7), ((120, -30), "puno", -0.7)),
    "sostiene": (((-236, 150), "abierto", -0.3), ((246, 40), "puno", 0.3)),
    "sostiene2": (((-150, 60), "puno", -0.3), ((150, 60), "puno", 0.3)),
    # ciclo de caminar / correr (se mezclan según la fase del paso)
    "anda1":    (((-250, 90), "abierto", -0.45), ((210, 190), "abierto", 0.15)),
    "anda2":    (((-210, 190), "abierto", -0.15), ((250, 90), "abierto", 0.45)),
    "corre1":   (((-270, 10), "puno", -0.6), ((200, 170), "puno", 0.3)),
    "corre2":   (((-200, 170), "puno", -0.3), ((270, 10), "puno", 0.6)),
    "cae":      (((-280, -120), "abierto", 0.4), ((280, -120), "abierto", -0.4)),
    "empuja":   (((-236, 150), "abierto", -0.3), ((330, 20), "abierto", -0.05)),
    "ruega":    (((-60, 40), "abierto", 0.6), ((60, 40), "abierto", -0.6)),
}
# poses que dejan los brazos libres para balancearse al andar
BALANCEO = {"normal", "anda1", "anda2", "caidos"}
HOMBROS = ((-W2 + 4, 10), (W2 - 4, 10))


def mezcla_pose(a, b, k):
    if k >= 1 or a == b:
        return POSES[b]
    out = []
    for (pa, ta, ca), (pb, tb, cb) in zip(POSES[a], POSES[b]):
        p = (pa[0] + (pb[0] - pa[0]) * k, pa[1] + (pb[1] - pa[1]) * k)
        out.append((p, tb if k > 0.5 else ta, ca + (cb - ca) * k))
    return out


def brazos(c, pose, frente, s=1.0):
    """frente=False dibuja los brazos de detrás (los que no cruzan la pizarra)."""
    for i, ((hx, hy), tipo, curva) in enumerate(pose):
        sx, sy = HOMBROS[i]
        cruza = (i == 0 and hx > sx + 40) or (i == 1 and hx < sx - 40)
        if cruza != frente:
            continue
        ang = manguera(c, (sx, sy), (hx, hy), curva, 20)
        guante(c, hx, hy, ang, tipo, 1.35, 1 if i == 1 else -1)


# ------------------------------------------------------------------ cuerpo
def cuerpo(c, ficha):
    marco = ficha.get("marco", "marco")
    ancho = 0.86 if ficha.get("estrecho") else 1.0
    x0, x1 = -W2 * ancho, W2 * ancho
    # canto (grosor 3D a la izquierda)
    canto = poly([(x0, -H2 + 6), (x0 - 20, -H2 + 22), (x0 - 20, H2 + 12), (x0, H2)])
    pieza(c, canto, ficha.get("canto", "marco_oscuro"), 6)
    marco_p = rrect(x0, -H2, x1, H2, 16)
    pieza(c, marco_p, marco, 6, shader=degradado(-H2, H2, "marco_claro", marco),
          sombra=(rrect(x0, H2 - 18, x1, H2, 10), "marco_oscuro"))
    tablero = rrect(x0 + 18, -H2 + 18, x1 - 18, H2 - 18, 6)
    pieza(c, tablero, "pizarra", 4.5, shader=degradado(-H2, H2, "pizarra", "pizarra_sombra"))
    # brillo diagonal del tablero
    c.save()
    c.clipPath(tablero, skia.ClipOp.kIntersect, True)
    c.drawPath(poly([(x0 + 40, -H2), (x0 + 110, -H2), (x0 - 10, H2), (x0 - 80, H2)]), relleno("blanco", 70))
    c.restore()
    garabatos(c, ficha.get("garabatos", ()))
    if ficha.get("melena"):  # melena pelirroja de Piza Indignada
        for sx in (-1, 1):
            p = suave([(sx * 100, -H2 - 10), (sx * 175, -110), (sx * 190, 20), (sx * 160, 90), (sx * 150, -60)])
            pieza(c, p, ficha["melena"] if isinstance(ficha["melena"], tuple) else "naranja", 5)


def accesorios_cara(c, ficha):
    g = ficha.get("gafas")
    if g == "redondas":
        for x in (-45, 45):
            c.drawPath(elipse(x, OJOS_Y + 4, 46, 46), trazo(8))
        c.drawLine(-2, OJOS_Y, 2, OJOS_Y, trazo(8))
    elif g == "cuadradas":
        for x in (-45, 45):
            c.drawPath(rrect(x - 44, OJOS_Y - 30, x + 44, OJOS_Y + 34, 10), trazo(8))
        c.drawLine(-2, OJOS_Y, 2, OJOS_Y, trazo(8))
    elif g == "sol":
        for x in (-48, 48):
            p = suave([(x - 50, OJOS_Y - 20), (x + 50, OJOS_Y - 24), (x + 44, OJOS_Y + 20), (x - 40, OJOS_Y + 24)])
            pieza(c, p, "tinta", 5, brillo=suave([(x - 30, OJOS_Y - 8), (x - 10, OJOS_Y - 12)], close=False))
        c.drawLine(-4, OJOS_Y - 16, 4, OJOS_Y - 16, trazo(9))
    if ficha.get("barba"):  # barba alrededor de la boca (con hueco para que se vea la expresión)
        p = suave([(-128, OJOS_Y + 50), (-118, BOCA_Y + 60), (-60, BOCA_Y + 98), (0, BOCA_Y + 108), (60, BOCA_Y + 98),
                   (118, BOCA_Y + 60), (128, OJOS_Y + 50), (100, BOCA_Y - 10), (60, BOCA_Y - 30), (-60, BOCA_Y - 30),
                   (-100, BOCA_Y - 10)])
        p.addPath(elipse(0, BOCA_Y + 14, 62, 38))
        p.setFillType(skia.PathFillType.kEvenOdd)
        pieza(c, p, ficha["barba"], 4)
    if ficha.get("antifaz"):  # antifaz de ladrón con agujeros para los ojos
        p = suave([(-125, OJOS_Y - 40), (0, OJOS_Y - 50), (125, OJOS_Y - 40), (120, OJOS_Y + 38), (0, OJOS_Y + 30),
                   (-120, OJOS_Y + 38)])
        for x in (-45, 45):
            p.addPath(elipse(x, OJOS_Y + 2, 36, 32))
        p.setFillType(skia.PathFillType.kEvenOdd)
        pieza(c, p, "tinta", 4)
        for sx in (-1, 1):
            c.drawLine(sx * 122, OJOS_Y - 10, sx * 150, OJOS_Y - 30 + 8 * sx, trazo(8))
    if ficha.get("bigote"):
        p = suave([(0, BOCA_Y - 18), (-34, BOCA_Y - 34), (-64, BOCA_Y - 12), (-30, BOCA_Y - 6),
                   (0, BOCA_Y - 12), (30, BOCA_Y - 6), (64, BOCA_Y - 12), (34, BOCA_Y - 34)])
        pieza(c, p, "madera", 4.5)


def accesorios_cuerpo(c, ficha):
    if ficha.get("pajarita"):
        col = ficha["pajarita"]
        pieza(c, poly([(0, 150), (-40, 128), (-40, 172), (0, 150), (40, 128), (40, 172)]), col, 5)
        pieza(c, elipse(0, 150, 9, 9), col, 4)
    if ficha.get("corbata"):
        col = ficha["corbata"]
        pieza(c, poly([(-12, 112), (12, 112), (8, 124), (20, 178), (0, 192), (-20, 178), (-8, 124)]), col, 4.5)
    if ficha.get("birrete"):
        c.save(); c.translate(70, -H2 - 6); c.rotate(12)
        pieza(c, poly([(-70, -10), (0, -38), (70, -10), (0, 18)]), "tinta", 4, brillo=None)
        pieza(c, rrect(-34, 0, 34, 26, 6), "tinta", 0)
        c.drawLine(50, -16, 64, 30, trazo(4, "amarillo")); c.drawCircle(64, 34, 6, relleno("amarillo"))
        c.restore()
    if ficha.get("pelo"):  # pelo asomando por encima del marco
        col, estilo = ficha["pelo"]
        c.save(); c.translate(0, -H2 + 4)
        if estilo == "canoso":  # pelo blanco, algo despejado arriba
            for sx in (-1, 1):
                pieza(c, suave([(sx * 40, 0), (sx * 70, -40), (sx * 130, -36), (sx * 158, 10), (sx * 120, 6)]), col, 5)
            pieza(c, suave([(-46, -4), (0, -30), (46, -4), (0, 4)]), col, 4)
        elif estilo == "rapado":  # cabeza despejada: solo una franja corta a los lados
            for sx in (-1, 1):
                pieza(c, suave([(sx * 70, 6), (sx * 92, -8), (sx * 148, -12), (sx * 160, 6)]), col, 4)
        else:
            pts = [(-156, 14), (-152, -34)]
            for k in range(7):  # mechones
                x = -130 + k * 44
                pts += [(x, -60 - 8 * (k % 2)), (x + 22, -44)]
            pts += [(158, -30), (156, 14), (60, -4), (-40, 0)]
            pieza(c, poly(pts), col, 5)
        c.restore()
    if ficha.get("chapa"):  # chapa con el apellido (para que se sepa quién es sin caricaturizar)
        txt, col = ficha["chapa"]
        import wb
        f = wb.font("sub", 34)
        w = f.measureText(txt) + 36
        pieza(c, rrect(-w / 2, 172, w / 2, 222, 14), col, 4)
        c.drawString(txt, -w / 2 + 18, 209, f, relleno("blanco"))
    if ficha.get("visera"):
        c.save(); c.translate(0, -H2 - 4)
        pieza(c, suave([(-90, 0), (-70, -46), (70, -46), (90, 0)]), "verde_osc", 5)
        pieza(c, suave([(-110, 4), (0, -10), (110, 4), (0, 16)]), "verde_osc", 5)
        c.restore()


# ------------------------------------------------------------------ personaje completo
def dibuja(c, quien="piz", cara=None, pose=None, pose_prev=None, k_pose=1.0, mira=(0, 0), parpadeo=0.0,
           habla=0.0, paso=None, t=0.0, sombra=True, objeto=None, ojos=1.0, corre=False, giro=0.0):
    """Dibuja el personaje en (0, 0) local. paso = fase de la caminata (None = quieto).
    ojos > 1 = ojos que se salen (reacción cartoon); giro -1..1 = la cara mira hacia un lado (3/4)."""
    ficha = PERSONAJES[quien]
    cara = cara or ficha.get("cara", "normal")
    ex = EXPRESIONES.get(cara, EXPRESIONES["normal"])
    pose = pose or BRAZOS_DE.get(cara, "normal")
    P = list(mezcla_pose(pose_prev or pose, pose, k_pose))
    if paso is not None and (pose in BALANCEO or corre):  # brazos que se balancean con el paso
        a, b = ("corre1", "corre2") if corre else ("anda1", "anda2")
        P = list(mezcla_pose(a, b, 0.5 + 0.5 * math.sin(paso * 2 * math.pi)))
    lleva_rotu = ficha.get("rotulador") and P[0][1] == "abierto" and P[0][0][1] > 60
    if lleva_rotu:
        P[0] = (P[0][0], "puno", P[0][2])
    zap = ficha.get("zapatilla", "rojo")
    if sombra:
        sombra_suelo(c, 0, 340, 170)
    # piernas
    for i, sx in enumerate((-58, 58)):
        lado = -1 if i == 0 else 1
        fx, fy, lev = sx * 1.25, 322, 0.0
        if paso is not None:
            fase = paso * 2 * math.pi + (0 if i == 0 else math.pi)
            fx += (62 if corre else 34) * math.sin(fase)
            lev = max(0.0, math.cos(fase))
            fy -= (44 if corre else 26) * lev
        manguera(c, (sx, H2 - 6), (fx, fy - 10), 0.12 * lado, 22)
        zapatilla(c, fx + 10 * lado, fy + 4, lado, zap, 1.4, lev)
    brazos(c, P, frente=False)
    cuerpo(c, ficha)
    # cara (con giro, los rasgos se desplazan hacia donde mira: vista de 3/4)
    c.save()
    c.translate(giro * 55, 0)
    mx, my = mira
    mx, my = mx + ex.get("mira", (0, 0))[0], my + ex.get("mira", (0, 0))[1]
    parp = max(ex["parpado"], parpadeo)
    for x, lado in ((-45, -1), (45, 1)):
        ojo(c, x * (1 + 0.25 * (ojos - 1)), OJOS_Y - 30 * (ojos - 1), ex["ojo"] * ojos, parp, ex.get("inclina", 0), ex["pupila"], (mx, my), lado,
            ex.get("cerrados"), ficha.get("pestanas") or ex.get("pestanas"))
    if not ficha.get("gafas") == "sol":
        cejas(c, *ex["cejas"])
    boca(c, ex["boca"], habla)
    accesorios_cara(c, ficha)
    c.restore()
    accesorios_cuerpo(c, ficha)
    if lleva_rotu:  # el rotulador rojo de Piz
        hx, hy = P[0][0]
        c.save(); c.translate(hx + 6, hy + 30); c.rotate(-24)
        pieza(c, rrect(-10, -86, 10, 20, 6), "blanco", 4.5)
        pieza(c, rrect(-10, -86, 10, -54, 5), "rojo", 4.5)
        pieza(c, poly([(-6, -86), (6, -86), (2, -100), (-2, -100)]), "rojo", 3.5)
        c.restore()
        ang = math.degrees(math.atan2(hy - HOMBROS[0][1], hx - HOMBROS[0][0]))
        guante(c, hx, hy, ang, "puno", 1.35, -1)
    tipo_obj = objeto.get("tipo") if isinstance(objeto, dict) else objeto
    if tipo_obj == "prismaticos":  # delante de los ojos (pose "prismaticos")
        from . import objetos
        c.save(); c.translate(giro * 55, OJOS_Y + 20); c.scale(0.95, 0.95)
        objetos.dibuja(c, objeto, t)
        c.restore()
        objeto = None
    if objeto:
        from . import objetos
        hx, hy = P[1][0]
        c.save(); c.translate(hx + 30, hy - 10); c.scale(0.55, 0.55)
        objetos.dibuja(c, objeto, t)
        c.restore()
    brazos(c, P, frente=True)
    if ex.get("extra"):
        adornos(c, ex["extra"], t)
