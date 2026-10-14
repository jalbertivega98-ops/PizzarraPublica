#!/usr/bin/env python3
"""«Piz y la casa imposible» (2026): episodio con el motor de animación de serie (gags, planos, parallax, banda sonora).

Misma historia y datos que series/compra2026.py (fuentes allí), más:
  ITP de segunda mano 2026: del 4 % (País Vasco) al 10 % (Cataluña) → hasta 22.300 € sobre 223.000 €.
Estructura de dibujos animados: objetivo (su casa) → problema (le dirán que no) → obstáculos crecientes
(precio, banco, Hacienda, la casa que se aleja) → giro (la hipoteca sería más barata que su alquiler) →
causa (letra pequeña: 35 %) → conclusión + siguiente capítulo con la llamada a seguir dentro de la historia.
Gags: el precio cae del cielo y le aplasta · Hacienda entra con la factura · la casa sale corriendo ·
lupa sobre la letra pequeña · el contrato de alquiler le persigue.
Uso: python3 series/compra2026_serie.py  → storyboards/compra2026_serie.json
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "storyboards")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
import compra2026 as base  # noqa: E402
from padres_viva import V  # noqa: E402
from universo import gags  # noqa: E402

C = "red"
SUELO = 1340


def piz(x, at=0.0, scale=0.85, cara="ilusionado", acciones=(), **kw):
    return dict(type="personaje", quien="piz", id="piz", x=x, y=SUELO, scale=scale, at=at, cara=cara,
                acciones=list(acciones), **kw)


def pj(quien, x, at, scale=0.8, cara="normal", acciones=(), **kw):
    return dict(type="personaje", quien=quien, x=x, y=SUELO, scale=scale, at=at, cara=cara, acciones=list(acciones), **kw)


def obj(tipo, x, y, at, scale=1.0, props=None, acciones=(), **kw):
    return dict(type="objeto", objeto=tipo, x=x, y=y, scale=scale, at=at, props=props or {}, acciones=list(acciones), **kw)


def rot(text, x, y, at, size=90, color="amarillo", **kw):
    kw.setdefault("hud", True)  # los datos van fijos en pantalla: la cámara se mueve por el mundo, no por los datos
    return dict(type="rotulo", text=text, x=x, y=y, size=size, color=color, at=at, **kw)


def edif(tipo, x, at, scale=1.0, acciones=(), **kw):
    return dict(type="edificio", edificio=tipo, x=x, y=SUELO, scale=scale, at=at, acciones=list(acciones), **kw)


def plano(at, plano="general", sobre=None, dur=0.6, **kw):
    return dict(at=at, plano=plano, sobre=sobre, dur=dur, **kw)


precio_els, precio_piz = gags.cae_del_cielo("223.000 €", "@223.000-0.6", 330, 520, scale=1.35)

scenes = [
    # 1 · OBJETIVO + PROBLEMA: lo tiene todo… y el banco le dirá que no
    dict(id="gancho", fondo="calle", animo="alegre", lines=[
        V("Piz tiene trabajo fijo, cinco años ahorrando… y un sueño: una casa.", "energia"),
        V("Spoiler: el banco le dirá que no.", "remate", 0.25),
    ], camara=[plano(0, "medio", [500, 1000], 0), plano("@sueño", "general", dur=0.7),
               plano("@no", "medio", "piz", 0.15)],
       luz=[{"at": "@Spoiler", "tipo": "foco", "sobre": "piz", "r": 380, "dur": 0.2}, {"at": "@no+0.6", "tipo": "normal"}],
       elements=[
        piz(150, 0, 0.85, "ilusionado", entra="nada", objeto="hucha", pose="sostiene", acciones=[
            {"at": 0, "x": 330, "dur": 1.6}, {"at": "@fijo", "cara": "riendo"},
            {"at": "@ahorrando", "salta": True}, {"at": "@sueño", "objeto": None, "pose": "arriba", "cara": "ilusionado", "mira": "casa"},
            {"at": "@Spoiler", "cara": "preocupado", "pose": "manos_juntas", "mira": "camara"},
            {"at": "@no", "take": True, "cara": "susto", "pose": "cabeza"}]),
        obj("checklist", 700, 560, "@trabajo", 1.0, hud=True, props={"items": ["Trabajo fijo", "5 años ahorrando"], "marcas": []},
            acciones=[{"at": "@fijo", "props": {"marcas": ["si"]}, "sfx": "ding"},
                      {"at": "@ahorrando", "props": {"marcas": ["si", "si"]}, "sfx": "ding"}], out="@sueño"),
        edif("casa", 800, "@sueño", 0.7, id="casa", cara="ilusionado", acciones=[{"at": "@no", "cara": "triste"}]),
        obj("bocadillo", 760, 560, "@sueño+0.3", 0.9, props={"texto": "¡Mi casa!", "cola": [-1, 1]}, out="@Spoiler"),
        rot("¡DENEGADA!", 540, 600, "@no", 120, C, golpe=True, rot=-6),
    ]),
    # 2 · OBSTÁCULO 1: el precio le cae encima
    dict(id="precio", fondo="calle", animo="comico", trans="pan", footnote=base.CJE, lines=[
        V("Precio medio de un piso en España: 223.000 euros.", "normal"),
    ], camara=[plano(0, "general", dur=0), plano("@223.000+0.6", "medio", "piz", 0.25),
               plano("@euros+0.3", "general", dur=0.6)],
       elements=[
        edif("casa", 790, 0, 0.8, id="casa", cara="ilusionado", entra="nada", acciones=[{"at": "@223.000+0.7", "cara": "riendo"}]),
        piz(330, 0, 0.85, "ilusionado", entra="nada", acciones=precio_piz),
        *precio_els,
    ]),
    # 3 · OBSTÁCULO 2: el banco (la cámara le sigue hasta la puerta)
    dict(id="banco", fondo="calle", animo="curioso", trans="pan", footnote=base.CJE, lines=[
        V("El banco presta el 80 %. El resto, lo pone él.", "intriga"),
    ], camara=[plano(0, "medio", "piz", 0, aire=120), plano("@banco+0.2", "general", dur=0.8),
               plano("@resto", "medio", "piz", 0.3)],
       elements=[
        edif("banco", 640, 0, 0.88, id="banco", cara="ilusionado", entra="nada",
             acciones=[{"at": "@80", "cara": "riendo"},
                       {"at": "@resto", "cara": "burla", "caras_dentro": {"0": "burla", "1": "esceptica", "2": "riendo", "3": "serio"}}]),
        piz(-80, 0, 0.6, "ilusionado", entra="nada", acciones=[
            {"at": 0, "x": 190, "dur": 1.1}, {"at": "@80", "cara": "riendo", "pose": "pulgar"},
            {"at": "@él", "take": True, "cara": "susto", "pose": None}]),
        rot("BANCO: 80 %", 600, 440, "@80", 104, "azul_claro", golpe=True, out="@resto"),
        rot("TÚ: 20 % + GASTOS", 560, 440, "@resto", 86, C, golpe=True),
    ]),
    # 4 · OBSTÁCULO 3: dentro del banco… y Hacienda
    dict(id="entrada", fondo="banco_dentro", animo="tension", trans="iris", footnote=base.CJE + "\nITP 2026: 4-10 % según comunidad", lines=[
        V("Entrada, notaría…", "normal"),
        V("y sorpresa: Hacienda, que se lleva hasta 22.300 euros de impuesto.", "sorpresa"),
        V("En total, 66.900 euros. Y Piz tiene 20.000.", "remate", 0.2),
    ], camara=[plano(0, "medio", "banquero", 0), plano("@sorpresa", "general", dur=0.35),
               plano("@66.900", "medio", "piz", 0.3), plano("@20.000", "primero", "piz", 0.3)],
       elements=[
        pj("banquero", 240, 0, 0.88, "serio", entra="nada", id="banquero", pose="senala",
           acciones=[{"at": "@notaría", "cara": "burla"}, {"at": "@Hacienda", "cara": "sorpresa", "mira": "hacienda"},
                     {"at": "@66.900", "cara": "esceptica", "pose": "encoge", "mira": "piz"}]),
        piz(820, 0, 0.82, "ilusionado", entra="nada", objeto="hucha", pose="sostiene",
            acciones=[{"at": "@notaría", "cara": "preocupado"}, {"at": "@Hacienda", "take": True, "cara": "susto", "mira": "hacienda"},
                      {"at": "@66.900", "cara": "susto", "mira": "camara", "tiembla": True},
                      {"at": "@20.000", "cara": "triste", "objeto": None, "pose": "caidos"}]),
        obj("cartel", 260, 430, "@Entrada", 0.7, props={"texto": "ENTRADA"}, entra="cae", dur=0.5),
        obj("cartel", 560, 430, "@notaría", 0.7, props={"texto": "+ NOTARÍA"}, entra="cae", dur=0.5),
        gags.aparece_hacienda("@Hacienda-0.2", 560),
        rot("+ 22.300 €", 820, 430, "@22.300", 92, C, golpe=True),
        rot("66.900 €", 540, 600, "@66.900", 150, C, golpe=True, out="@20.000"),
        gags.dinero_vuela("@tiene", 900, 1080, 6),
        rot("TIENE 20.000 €", 540, 600, "@20.000", 92, "verde", golpe=True),
    ]),
    # 5 · OBSTÁCULO 4: la casa sale corriendo
    dict(id="sube", fondo="calle", animo="comico", trans="iris", footnote="Ministerio de Vivienda, 2.º trim. 2026 (+12,5 % anual) · cálculo sobre 223.000 €", lines=[
        V("Así que ahorra más. Pero el piso sube un 12,5 % en un año:", "normal"),
        V("casi 25.000 euros más. Más de lo que ahorró.", "sorpresa"),
    ], camara=[plano(0, "general", dur=0), plano("@sube", "medio", "piz", 0.4, aire=180),
               plano("@25.000", "general", dur=0.5)],
       elements=[
        piz(160, 0, 0.75, "ilusionado", entra="nada", objeto="hucha", pose="sostiene",
            acciones=[{"at": "@ahorra", "x": 420, "corre": True}, {"at": "@sube", "x": 620, "corre": True},
                      {"at": "@12,5", "tropieza": True, "cara": "susto"},
                      {"at": "@25.000", "cara": "indignado", "objeto": None, "pose": "punos", "mira": "casa"},
                      {"at": "@ahorró", "cara": "triste", "pose": "caidos"}]),
        edif("casa", 690, 0, 0.6, id="casa", cara="ilusionado", entra="nada", piernas=True,
             acciones=gags.casa_se_aleja("casa", [("@ahorra+0.3", 860), ("@sube+0.2", 1010)])
             + [{"at": "@12,5", "cara": "burla"}]),
        rot("+12,5 %", 860, 470, "@12,5", 120, C, golpe=True, out="@25.000"),
        rot("+25.000 €", 600, 460, "@25.000", 140, C, golpe=True, fx=[{"at": "@ahorró", "do": "rodear"}]),
        rot("sus ahorros: 20.000 €", 330, 600, "@ahorró", 56, "blanco"),
    ]),
    # 6 · GIRO: su hipoteca sería más barata que su alquiler (silencio dramático)
    dict(id="absurdo", fondo="salon", musica="corte", animo="triste", trans="pan",
         footnote="INE, julio 2026: tipo medio 3,01 % · 80 % a 30 años · alquiler: CJE", lines=[
        V("Y lo más absurdo:", "intriga", 0.5),
        V("su hipoteca serían 753 euros al mes.", "sorpresa"),
        V("Menos que su alquiler: 1.176.", "remate"),
    ], camara=[plano(0, "medio", "piz", 0), plano("@hipoteca", "general", dur=0.5),
               plano("@1.176", "primero", "piz", 0.2)],
       luz=[{"at": 0, "tipo": "foco", "sobre": "piz", "r": 460}, {"at": "@hipoteca", "tipo": "normal", "dur": 0.4}],
       elements=[
        piz(560, 0, 0.9, "pensativo", entra="nada", pose="piensa",
            acciones=[{"at": "@753", "cara": "sorpresa", "pose": None, "mira": "calc"},
                      {"at": "@Menos", "cara": "confundido", "mira": "camara"},
                      {"at": "@1.176", "cara": "indignado", "salta": True}]),
        obj("calculadora", 220, 730, "@hipoteca", 0.85, id="calc", props={"texto": "0"}, sfx="calculadora",
            acciones=[{"at": "@753", "props": {"texto": "753"}}]),
        rot("753 €/mes", 230, 940, "@753", 76, "verde", golpe=True),
        obj("etiqueta", 840, 640, "@alquiler", 0.72, props={"texto": "1.176 €", "color": "rojo"}, entra="cae", dur=0.5, rot=6),
        rot("ALQUILER", 840, 520, "@alquiler", 58, C),
        pj("sarcastica", 940, "@1.176+0.3", 0.45, "burla", entra="pop"),
    ]),
    # 7 · CAUSA: la letra pequeña
    dict(id="motivo", fondo="banco_dentro", animo="tension", trans="iris",
         footnote="Criterio habitual de los bancos: cuota ≤ 30-35 % del sueldo · sueldo joven: CJE", lines=[
        V("¿Por qué le dicen que no? Por la letra pequeña:", "intriga"),
        V("la cuota no puede pasar del 35 % del sueldo. La de Piz sería el 63 %.", "remate"),
    ], camara=[plano(0, "medio", "banquera", 0), plano("@pequeña", "detalle", "contrato", 0.5),
               plano("@sueldo+0.2", "general", dur=0.4), plano("@63", "primero", "piz", 0.2)],
       luz=[{"at": "@63", "tipo": "alarma"}],
       elements=[
        pj("banquera_seria", 200, 0, 0.8, "serio", entra="nada", id="banquera", pose="sostiene", objeto="lupa",
           acciones=[{"at": "@pequeña", "cara": "burla", "mira": "contrato"}, {"at": "@63", "cara": "esceptica", "pose": "cruzados", "objeto": None}]),
        piz(880, 0, 0.75, "confundido", entra="nada",
            acciones=[{"at": "@pequeña", "mira": "contrato"}, {"at": "@63", "take": True, "cara": "susto"},
                      {"at": "@63+0.7", "cara": "triste", "pose": "caidos"}]),
        *gags.lupa_letra_pequena("@pequeña-0.4", 560, 650, "cuota ≤ 35 % del sueldo", scale=0.9),
        rot("63 %", 560, 520, "@63", 190, C, golpe=True),
    ]),
    # 8 · CONCLUSIÓN + siguiente capítulo: el alquiler le persigue… y Piz nos pide ayuda
    dict(id="final", fondo="calle", animo="final", trans="iris", lines=[
        V("Así que Piz paga 1.176 de alquiler… por no poder pagar 753.", "remate"),
        V("¿Tiene salida? PSOE, PP y Vox proponen cosas muy distintas.", "intriga"),
        V("Síguenos para ver si Piz lo consigue.", "energia"),
    ], camara=[plano(0, "general", dur=0), plano("@paga", "medio", "piz", 0.4, aire=150),
               plano("@salida", "general", dur=0.5), plano("@Síguenos", "medio", "piz", 0.4)],
       elements=[
        piz(150, 0, 0.75, "susto", entra="nada", pose=None,
            acciones=[{"at": 0, "x": 760, "corre": True, "dur": 2.6}, {"at": "@753", "gira": True, "flip": True, "cara": "indignado"},
                      {"at": "@salida", "x": 540, "dur": 0.6, "cara": "pensativo", "pose": "piensa", "mira": "camara"},
                      {"at": "@Síguenos", "cara": "ilusionado", "pose": "ruega", "mira": "camara", "salta": True},
                      {"at": "@consigue", "pose": "saluda", "cara": "riendo"}]),
        gags.persecucion(0, "piz", "contrato", {"titulo": "ALQUILER", "hojas": 1}, x=-300, scale=0.65, offset=-340),
        rot("1.176 €/mes", 300, 470, "@1.176", 80, C, golpe=True, out="@salida"),
        obj("cartel", 220, 470, "@PSOE", 0.85, props={"texto": "PSOE", "color": "psoe", "tinta": "blanco"}, golpe=True, hud=True),
        obj("cartel", 540, 430, "@PP", 0.85, props={"texto": "PP", "color": "pp", "tinta": "blanco"}, golpe=True, hud=True),
        obj("cartel", 860, 470, "@Vox", 0.85, props={"texto": "VOX", "color": "vox", "tinta": "blanco"}, golpe=True, hud=True),
        rot("SÍGUENOS", 540, 640, "@Síguenos", 110, "amarillo", fx=[{"at": "@consigue", "do": "latir"}]),
    ]),
]

SB = dict(base.SB)
SB.update(
    slug="compra2026_serie", title="Piz y la casa imposible", scenes=scenes, banda=True,
    music_volume=0.2, scribble_volume=0.0, sfx_volume=1.0, end_hold=1.2,
    caption=("🏠 Piz tiene trabajo fijo y 5 años ahorrando. El banco le dice que no.\n"
             "💶 Piso medio: 223.000 € · entrada + impuestos: 66.900 € (hasta 22.300 € de ITP)\n"
             "🏃 La casa corre más que él: +12,5 % en un año\n"
             "🤯 Su hipoteca: 753 €/mes. Su alquiler: 1.176 €\n"
             "💬 ¿Te ha pasado algo parecido? Cuéntanoslo\n"
             "➡️ Próximo capítulo: qué proponen PSOE, PP y Vox · 🔔 Síguenos · 📚 Fuentes en comentarios"),
    pinned_comment=base.SB["pinned_comment"].replace("Álex es un personaje", "Piz es un personaje").replace(
        "INE hipotecas jul. 2026", "ITP 2026: 4-10 % según comunidad (10 % de 223.000 = 22.300 €) · INE hipotecas jul. 2026"),
)

if __name__ == "__main__":
    path = os.path.join(OUT, f"{SB['slug']}.json")
    json.dump(SB, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(path)
