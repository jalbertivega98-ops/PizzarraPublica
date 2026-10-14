#!/usr/bin/env python3
"""«Piz quiere comprarse una casa» (2026) con la nueva identidad visual: pizarras-personaje y mundo cartoon.

Misma historia y mismos datos que series/compra2026.py (fuentes allí); el protagonista ahora es Piz.
Guion visual pedido por joel: Piz ilusionado → casa sonriente → susto con el precio → va al banco →
pizarras banqueras dentro → condiciones de la hipoteca → impuestos y gastos → reacciona a cada obstáculo.
Uso: python3 series/compra2026_universo.py  → storyboards/compra2026_piz.json
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "storyboards")
sys.path.insert(0, HERE)
import compra2026 as base  # noqa: E402
from padres_viva import V  # noqa: E402

C = "red"
SUELO = 1340


def piz(x, at=0.05, scale=0.8, cara="ilusionado", acciones=(), **kw):
    return dict(type="personaje", quien="piz", x=x, y=SUELO, scale=scale, at=at, cara=cara, acciones=list(acciones), **kw)


def pj(quien, x, at, scale=0.6, cara="normal", acciones=(), y=SUELO, **kw):
    return dict(type="personaje", quien=quien, x=x, y=y, scale=scale, at=at, cara=cara, acciones=list(acciones), **kw)


def obj(tipo, x, y, at, scale=1.0, props=None, acciones=(), **kw):
    return dict(type="objeto", objeto=tipo, x=x, y=y, scale=scale, at=at, props=props or {}, acciones=list(acciones), **kw)


def rot(text, x, y, at, size=90, color="amarillo", **kw):
    return dict(type="rotulo", text=text, x=x, y=y, size=size, color=color, at=at, **kw)


def edif(tipo, x, at, scale=1.0, acciones=(), y=SUELO, **kw):
    return dict(type="edificio", edificio=tipo, x=x, y=y, scale=scale, at=at, acciones=list(acciones), **kw)


scenes = [
    # GANCHO: lo tiene todo… y le dicen que no
    dict(id="gancho", fondo="calle", lines=[
        V("Piz tiene trabajo fijo y cinco años ahorrando.", "energia"),
        V("Y aun así, el banco le va a decir que no.", "remate", 0.2),
        V("Síguenos, que esto te sonará."),
    ], elements=[
        piz(290, 0, 1.0, "ilusionado", acciones=[
            {"at": "@fijo", "pose": "pulgar"}, {"at": "@ahorrando", "salta": True, "cara": "riendo", "pose": "arriba"},
            {"at": "@banco", "cara": "preocupado", "pose": None}, {"at": "@no", "cara": "susto", "tiembla": True},
            {"at": "@síguenos", "cara": "normal", "pose": "saluda"}]),
        edif("casa", 810, "@trabajo-0.3", 0.7, cara="ilusionado", acciones=[{"at": "@banco", "sale": "pop"}]),
        obj("checklist", 720, 560, "@trabajo", 1.15, props={"items": ["Trabajo fijo", "5 años ahorrando"], "marcas": []},
            acciones=[{"at": "@fijo", "props": {"marcas": ["si"]}}, {"at": "@ahorrando", "props": {"marcas": ["si", "si"]}}],
            out="@aun"),
        edif("banco", 770, "@banco", 0.55, cara="burla", entra="cae"),
        rot("¡DENEGADA!", 560, 620, "@no", 130, C, golpe=True, rot=-6),
        rot("SÍGUENOS", 560, 440, "@síguenos", 96, "amarillo", fx=[{"at": "@sonará", "do": "latir"}]),
    ]),
    # LA CASA Y SU PRECIO
    dict(id="precio", fondo="calle", footnote=base.CJE, lines=[
        V("Piso medio en España: 223.000 euros.", "normal"),
    ], elements=[
        edif("casa", 690, 0.0, 1.0, cara="ilusionado", entra="nada", acciones=[{"at": "@223.000", "cara": "riendo"}]),
        piz(210, 0.0, 0.85, "ilusionado", entra="izq", acciones=[{"at": "@223.000", "cara": "susto", "salta": True}]),
        obj("etiqueta", 680, 560, "@223.000", 1.2, entra="cae", golpe=True, props={"texto": "223.000 €"}, rot=-4),
    ]),
    # EL BANCO, CON SUS PIZARRAS BANQUERAS
    dict(id="banco", fondo="calle", trans="barrido", footnote=base.CJE, lines=[
        V("El banco presta el 80 %. El resto, lo pone él.", "intriga"),
    ], elements=[
        edif("banco", 600, 0.0, 0.85, cara="ilusionado",
             acciones=[{"at": "@80", "cara": "riendo"}, {"at": "@resto", "cara": "burla",
                                                          "caras_dentro": {"0": "burla", "1": "esceptica", "2": "riendo", "3": "serio"}}]),
        rot("BANCO: 80 %", 560, 450, "@80", 100, "azul_claro", golpe=True, out="@resto"),
        piz(150, "@resto-0.4", 0.55, "confundido", entra="izq", acciones=[{"at": "@él", "cara": "susto", "tiembla": True}]),
        rot("TÚ: 20 % + GASTOS", 560, 450, "@resto", 84, C, golpe=True),
    ]),
    # DENTRO DEL BANCO: ENTRADA, IMPUESTOS Y NOTARÍA
    dict(id="entrada", fondo="banco_dentro", trans="zoom", footnote=base.CJE, lines=[
        V("Entrada, impuestos y notaría: 66.900 euros.", "sorpresa"),
        V("Piz tiene 20.000.", "remate", 0.3),
        V("Le faltan casi 47.000.", "remate"),
    ], elements=[
        pj("banquero", 250, 0.0, 0.88, "serio", entra="nada", pose="senala",
           acciones=[{"at": "@impuestos", "cara": "burla"}, {"at": "@faltan", "cara": "esceptica", "pose": "encoge"}]),
        piz(820, 0.0, 0.85, "ilusionado", entra="der",
            acciones=[{"at": "@impuestos", "cara": "preocupado"}, {"at": "@66.900", "cara": "susto", "salta": True},
                      {"at": "@tiene", "cara": "triste", "objeto": "hucha", "pose": "sostiene"},
                      {"at": "@faltan", "cara": "susto", "tiembla": True, "objeto": None, "pose": "cabeza"}]),
        obj("cartel", 220, 420, "@entrada", 0.7, props={"texto": "ENTRADA"}, entra="cae"),
        obj("cartel", 540, 420, "@impuestos", 0.7, props={"texto": "+ IMPUESTOS", "color": "amarillo"}, entra="cae"),
        obj("cartel", 860, 420, "@notaría", 0.7, props={"texto": "+ NOTARÍA"}, entra="cae"),
        rot("66.900 €", 540, 610, "@66.900", 150, C, golpe=True, out="@tiene"),
        rot("TIENE 20.000 €", 540, 600, "@20.000", 96, "verde", golpe=True, out="@faltan"),
        rot("FALTAN 46.900 €", 540, 600, "@faltan", 104, C, golpe=True, fx=[{"at": "@47.000", "do": "latir"}]),
    ]),
    # BUCLE ABIERTO: la casa corre más que él
    dict(id="sube", fondo="calle", trans="barrido",
         footnote="Ministerio de Vivienda, 2.º trim. 2026 (+12,5 % anual) · cálculo sobre 223.000 €", lines=[
        V("Pero lo peor no es eso.", "intriga"),
        V("Mientras ahorra, el piso sube un 12,5 % en un año.", "normal"),
        V("Casi 25.000 euros más. Más que todo lo que ahorró.", "sorpresa"),
    ], elements=[
        rot("…Y LO PEOR", 540, 470, 0.05, 110, "amarillo", out="@sube"),
        piz(230, 0.0, 0.85, "preocupado", entra="nada", objeto="hucha", pose="sostiene",
            acciones=[{"at": "@peor", "cara": "pensativo"}, {"at": "@ahorra", "cara": "ilusionado", "pose": "sostiene2"},
                      {"at": "@sube", "cara": "susto", "pose": "sostiene"}, {"at": "@25.000", "cara": "indignado", "tiembla": True},
                      {"at": "@ahorró", "cara": "triste", "objeto": None, "pose": "caidos"}]),
        edif("casa", 770, 0.0, 0.75, cara="riendo", entra="nada",
             fx=[{"at": "@sube", "do": "mover", "x": 740, "y": 1060, "scale": 1.3, "dur": 0.9}],
             acciones=[{"at": "@12,5", "salta": True}]),
        obj("grafica", 760, 520, "@sube", 0.8, props={"valores": [1, 1.03, 1.06, 1.09, 1.125]}, dibujo=1.6, out="@25.000"),
        rot("+12,5 %", 290, 520, "@12,5", 110, C, golpe=True, out="@25.000"),
        rot("+25.000 €", 560, 470, "@25.000", 140, C, golpe=True, fx=[{"at": "@todo", "do": "rodear"}]),
        rot("sus ahorros: 20.000 €", 330, 620, "@ahorró", 56, "blanco"),
    ]),
    # GIRO: la hipoteca le saldría más barata que el alquiler
    dict(id="absurdo", fondo="salon", musica="corte", trans="borrador",
         footnote="INE, julio 2026: tipo medio 3,01 % · 80 % a 30 años · alquiler: CJE", lines=[
        V("Y lo más absurdo:", "intriga", 0.5),
        V("su hipoteca serían 753 euros al mes.", "sorpresa"),
        V("Menos que un alquiler medio: 1.176.", "remate"),
    ], elements=[
        piz(540, 0.0, 0.9, "pensativo", entra="nada", pose="piensa",
            acciones=[{"at": "@753", "cara": "sorpresa", "pose": None}, {"at": "@menos", "cara": "confundido"},
                      {"at": "@1.176", "cara": "indignado", "salta": True}]),
        rot("LO MÁS ABSURDO", 540, 420, 0.05, 92, "amarillo", fx=[{"at": "@absurdo", "do": "temblar"}]),
        rot("HIPOTECA", 250, 540, "@hipoteca", 56, "verde"),
        obj("calculadora", 250, 720, "@hipoteca", 0.85, props={"texto": "753"}),
        rot("753 €", 250, 930, "@753", 84, "verde", golpe=True),
        rot("ALQUILER", 830, 540, "@alquiler", 56, C),
        obj("etiqueta", 830, 660, "@1.176", 0.7, props={"texto": "1.176 €", "color": "rojo"}, entra="cae", golpe=True, rot=6),
        pj("sarcastica", 940, "@1.176+0.3", 0.45, "burla", entra="pop"),
    ]),
    # EL MOTIVO DEL «NO»
    dict(id="motivo", fondo="banco_dentro", trans="papel",
         footnote="Criterio habitual de los bancos: cuota ≤ 30-35 % del sueldo · sueldo joven: CJE", lines=[
        V("¿Y por qué se la niegan?", "intriga"),
        V("El banco no acepta cuotas de más del 35 % del sueldo.", "normal"),
        V("Y la de Piz sería el 63 %.", "remate", 0.2),
    ], elements=[
        pj("banquera_seria", 230, 0.0, 0.85, "serio", entra="izq",
           acciones=[{"at": "@banco", "pose": "senala"}, {"at": "@sueldo", "pose": "senala_arriba", "cara": "burla"},
                     {"at": "@63", "cara": "esceptica", "pose": "cruzados"}]),
        piz(850, 0.0, 0.8, "confundido", entra="der",
            acciones=[{"at": "@35", "cara": "preocupado"}, {"at": "@Piz", "cara": "susto", "salta": True}, {"at": "@63", "cara": "triste", "pose": "caidos"}]),
        obj("checklist", 540, 520, "@banco", 1.1,
            props={"items": ["Trabajo fijo", "Ahorros", "Cuota < 35 %"], "marcas": ["si", "si"]},
            acciones=[{"at": "@63", "props": {"marcas": ["si", "si", "no"]}, "sfx": "error"}],
            fx=[{"at": "@sueldo", "do": "latir"}]),
        rot("63 %", 540, 820, "@63", 170, C, golpe=True),
    ]),
    # CONCLUSIÓN
    dict(id="conclusion", fondo="calle", trans="zoom", lines=[
        V("Así que Piz paga 1.176 de alquiler… por no poder pagar 753 de hipoteca.", "remate"),
    ], elements=[
        piz(540, 0.0, 1.0, "triste", entra="nada", pose="caidos",
            acciones=[{"at": "@1.176", "objeto": {"tipo": "fajo"}, "pose": "sostiene"},
                      {"at": "@poder", "cara": "preocupado", "mira": "der"},
                      {"at": "@hipoteca", "cara": "indignado", "objeto": None, "pose": "punos", "tiembla": True}]),
        rot("PAGA 1.176 €", 310, 470, "@1.176", 70, C, golpe=True, fx=[{"at": "@alquiler", "do": "latir"}]),
        rot("753 €", 790, 470, "@753", 100, "verde", fx=[{"at": "@hipoteca", "do": "tachar"}]),
    ]),
    # FINAL: siguiente capítulo + síguenos
    dict(id="final", fondo={"tipo": "rayos", "color": "amarillo"}, trans="barrido", lines=[
        V("¿Y qué proponen PSOE, PP y Vox para Piz? En el próximo vídeo.", "energia"),
        V("Síguenos para no perdértelo.", "energia"),
    ], elements=[
        piz(540, 0.0, 0.95, "pensativo", entra="pop", pose="piensa",
            acciones=[{"at": "@próximo", "cara": "idea", "pose": "senala_arriba"},
                      {"at": "@síguenos", "cara": "riendo", "pose": "saluda", "salta": True}]),
        obj("cartel", 220, 420, "@psoe", 0.9, props={"texto": "PSOE", "color": "psoe", "tinta": "blanco"}, golpe=True),
        obj("cartel", 540, 390, "@pp", 0.9, props={"texto": "PP", "color": "pp", "tinta": "blanco"}, golpe=True),
        obj("cartel", 860, 420, "@vox", 0.9, props={"texto": "VOX", "color": "vox", "tinta": "blanco"}, golpe=True),
        rot("SÍGUENOS", 540, 560, "@síguenos", 110, "blanco", fx=[{"at": "@perdértelo", "do": "latir"}]),
    ]),
]

SB = dict(base.SB)
SB.update(
    slug="compra2026_piz", title="Piz quiere comprarse una casa", scenes=scenes,
    caption=base.SB["caption"].replace("Álex", "Piz"),
    pinned_comment=base.SB["pinned_comment"].replace("Álex es un personaje", "Piz es un personaje"),
)

if __name__ == "__main__":
    path = os.path.join(OUT, f"{SB['slug']}.json")
    json.dump(SB, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(path)
