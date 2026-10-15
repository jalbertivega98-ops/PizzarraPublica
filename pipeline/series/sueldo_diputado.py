#!/usr/bin/env python3
"""«¿Cuánto cobra un diputado?» (2026): un diputado raso frente al sueldo mediano (Piz) y el SMI (Pizón).

Fuentes y cálculo:
  Congreso, «Régimen económico y ayudas de los Señores Diputados», retribuciones 2026 (congreso.es/es/cem/regecodip):
    asignación constitucional 3.366,99 €/mes; indemnización por gastos 2.162,85 €/mes (fuera de Madrid) o 1.032,38 € (Madrid),
    exenta de IRPF (art. 17.2.b Ley 35/2006). Portavoz de grupo +3.197,41 €/mes; Presidencia del Congreso 14.330,84 €/mes (suma propia).
  Diputado raso de fuera de Madrid: 5.529,84 €/mes × 12 = 66.358 €/año (con 14 pagas de asignación, 73.092 €; nº de pagas no publicado).
  INE, Encuesta Anual de Estructura Salarial 2024 (28/05/2026): salario mediano 24.497,17 € → 66.358 / 24.497 = 2,7 años.
  SMI 2026: 17.094 €/año (RD 126/2026) → 3,9 años.
Uso: python3 series/sueldo_diputado.py → storyboards/sueldo_diputado.json
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "storyboards")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
import compra2026 as base  # noqa: E402
from compra2026_serie import obj, pj, plano, rot, edif  # noqa: E402
from padres_viva import V  # noqa: E402
from universo import gags  # noqa: E402

C = "red"
CONG = "Congreso de los Diputados, retribuciones 2026 · diputado sin cargo, de fuera de Madrid"


def quien(q, x, at=0.0, scale=0.75, cara="normal", acciones=(), **kw):
    return pj(q, x, at, scale, cara, acciones, id=q, **kw)


saco_els, saco_pizon = gags.cae_del_cielo("3,9 AÑOS", "@mínimo-0.5", 300, 560, scale=1.1, onomatopeya="¡PLAF!")

scenes = [
    # 1 · GANCHO
    dict(id="gancho", fondo="calle", animo="curioso", footnote=CONG, lines=[
        V("Un diputado cobra en un año lo que un trabajador normal tarda casi tres en ganar.", "energia"),
        V("Y una parte, sin pagar IRPF.", "remate", 0.2),
    ], camara=[plano(0, "general", dur=0), plano("@tres", "abierto", "piz", 0.4)],
       elements=[
        edif("congreso", 330, 0, 0.62, id="congreso", entra="nada"),
        quien("diputado", 330, "@diputado", 0.6, "normal", entra="pop", acciones=[{"at": "@año", "pose": "pulgar"},
                                                                               {"at": "@IRPF", "cara": "riendo", "salta": True}]),
        quien("piz", 1300, 0, 0.72, "normal", entra="nada", acciones=[{"at": "@trabajador", "x": 820, "dur": 0.9},
                                                                       {"at": "@tres", "take": True, "cara": "susto"},
                                                                       {"at": "@IRPF", "mira": "diputado", "cara": "indignado"}]),
        rot("1 AÑO", 330, 520, "@año", 100, "amarillo", golpe=True),
        rot("≈ 3 AÑOS", 800, 520, "@tres", 100, C, golpe=True),
        rot("SIN IRPF", 540, 700, "@IRPF", 90, "verde", golpe=True),
    ]),
    # 2 · LA NÓMINA
    dict(id="nomina", fondo="oficina", animo="curioso", trans="pan", footnote=CONG, lines=[
        V("Su sueldo base, la asignación, son 3.367 euros al mes. La cobran todos.", "normal"),
        V("Si es de fuera de Madrid, suma 2.163 para gastos. Total: 5.530 al mes.", "normal", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@5.530", "medio", "diputado", 0.3, aire=220)],
       elements=[
        quien("diputado", 300, 0, 0.75, "normal", entra="izq", acciones=[
            {"at": "@3.367", "pose": "sostiene", "objeto": "fajo", "cara": "ilusionado"},
            {"at": "@Madrid", "mira": "der"}, {"at": "@2.163", "salta": True, "cara": "riendo"},
            {"at": "@5.530", "pose": "arriba", "objeto": None}]),
        obj("calculadora", 800, 860, "@asignación", 0.85, id="calc", props={"texto": "3.367"}, entra="pop", sfx="calculadora",
            acciones=[{"at": "@2.163", "props": {"texto": "+2.163"}, "salta": True},
                      {"at": "@5.530", "props": {"texto": "5.530"}, "salta": True}]),
        rot("ASIGNACIÓN: 3.367 €", 600, 600, "@3.367", 74, "amarillo", golpe=True, out="@Madrid"),
        rot("+ GASTOS: 2.163 €", 600, 600, "@2.163", 74, "verde", golpe=True, out="@5.530"),
        rot("5.530 €/MES", 600, 600, "@5.530", 110, "amarillo", golpe=True),
        dict(type="efecto", efecto="lluvia", objeto="moneda", n=10, x0=150, x1=500, at="@5.530", vida=1.8),
    ]),
    # 3 · LO EXENTO
    dict(id="exento", fondo="oficina", animo="comico", trans="iris", footnote="Indemnización exenta de IRPF: art. 17.2.b Ley 35/2006 (según el Congreso)", lines=[
        V("Y esos 2.163 de gastos están exentos: Hacienda no los toca.", "sorpresa"),
        V("Son para pagarse el alojamiento y los viajes a Madrid.", "normal", 0.2),
    ], camara=[plano(0, "general", dur=0), plano("@exentos", "medio", "hacienda", 0.3, aire=200)],
       elements=[
        quien("diputado", 280, 0, 0.75, "normal", entra="nada", pose="sostiene", objeto="billete", acciones=[
            {"at": "@exentos", "pose": "pulgar", "cara": "riendo"}, {"at": "@alojamiento", "mira": "camara", "cara": "normal"}]),
        gags.aparece_hacienda("@Hacienda-0.3", 800, factura="IRPF"),
        dict(type="efecto", efecto="pum", text="¡NO!", x=640, y=820, at="@toca", scale=0.8, vida=0.8),
        rot("0 € DE IRPF", 600, 600, "@exentos", 100, "verde", golpe=True, out="@alojamiento"),
        rot("ALOJAMIENTO + VIAJES", 600, 600, "@alojamiento", 72, "blanco", golpe=True),
        obj("avion", 540, 960, "@viajes", 0.6, entra="izq", acciones=[{"at": "@Madrid", "sale": "der"}]),
    ]),
    # 4 · PIZ: el sueldo mediano
    dict(id="piz", fondo="calle", animo="tension", trans="pan", footnote="INE, Encuesta de Estructura Salarial 2024 (mediana) · 12 pagas", lines=[
        V("Piz cobra el sueldo mediano de España: 24.497 euros al año, según el INE.", "normal"),
        V("El diputado, unos 66.000. A Piz le cuesta casi tres años.", "sorpresa", 0.2),
    ], camara=[plano(0, "general", dur=0), plano("@tres", "medio", "piz", 0.3, aire=220)],
       elements=[
        quien("diputado", 260, "@diputado", 0.7, "normal", entra="izq", objeto="saco", pose="sostiene",
              acciones=[{"at": "@66.000", "salta": True, "cara": "ilusionado"}]),
        quien("piz", 800, 0, 0.72, "ilusionado", entra="der", objeto="hucha", pose="sostiene", acciones=[
            {"at": "@24.497", "salta": True}, {"at": "@66.000", "mira": "diputado", "cara": "sorpresa"},
            {"at": "@tres", "tropieza": True, "objeto": None}]),
        obj("reloj", 800, 600, "@cuesta", 0.7, entra="pop", velocidad=4),
        rot("24.497 €/AÑO", 800, 470, "@24.497", 74, "amarillo", golpe=True, out="@cuesta"),
        rot("66.358 €/AÑO", 270, 470, "@66.000", 74, "verde", golpe=True),
        rot("× 2,7", 800, 470, "@tres", 120, C, golpe=True),
    ]),
    # 5 · PIZÓN: el SMI
    dict(id="pizon", fondo="salon", animo="triste", trans="corte", footnote="SMI 2026: 17.094 €/año (RD 126/2026)", lines=[
        V("Y Pizón, con el sueldo mínimo, necesita casi cuatro.", "remate"),
    ], camara=[plano(0, "general", dur=0), plano("@cuatro", "medio", "pizon", 0.3, aire=200)],
       elements=[
        quien("pizon", 300, 0, 0.75, "normal", entra="izq", acciones=saco_pizon + [{"at": "@cuatro+0.6", "cara": "triste", "pose": "caidos"}]),
        *saco_els,
        rot("17.094 €/AÑO", 700, 470, "@Pizón", 74, "amarillo", golpe=True),
    ]),
    # 6 · LOS CARGOS
    dict(id="cargos", fondo="rayos", animo="comico", trans="iris", footnote="Congreso 2026: portavoz de grupo +3.197,41 €/mes · Presidencia 14.330,84 €/mes (suma propia)", lines=[
        V("Y eso, sin cargos. Un portavoz suma 3.197 euros más al mes.", "normal"),
        V("Y la presidencia del Congreso pasa de 14.000.", "sorpresa", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@14.000", "abierto", dur=0.4)],
       elements=[
        quien("profe", 300, 0, 0.75, "serio", entra="izq", pose="senala_arriba", acciones=[
            {"at": "@portavoz", "pose": "senala"}, {"at": "@14.000", "take": True, "cara": "sorpresa"}]),
        quien("sarcastica", 800, "@cargos", 0.72, "burla", entra="pop", acciones=[
            {"at": "@3.197", "pose": "jarras"}, {"at": "@14.000", "salta": True, "cara": "riendo"}]),
        obj("grafica", 560, 900, "@portavoz", 0.75, entra="pop", props={"valores": [1, 1.6, 4.3], "color": "verde"}),
        rot("PORTAVOZ: +3.197 €", 560, 520, "@3.197", 72, "amarillo", golpe=True, out="@presidencia"),
        rot("PRESIDENCIA: 14.331 €", 560, 520, "@14.000", 72, C, golpe=True),
    ]),
    # 7 · MATIZ + FINAL
    dict(id="final", fondo="calle", animo="final", trans="iris", footnote="Con 14 pagas de asignación serían 73.092 €/año (el Congreso no publica el nº de pagas)", lines=[
        V("Ojo: los gastos no son sueldo, compensan vivir lejos de casa.", "normal"),
        V("¿Te parece mucho o poco? Te leemos. Y síguenos: la próxima, la cesta de la compra.", "energia", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@síguenos", "abierto", dur=0.4)],
       elements=[
        quien("profe", 280, 0, 0.72, "normal", entra="nada", pose="senala_arriba",
              acciones=[{"at": "@compensan", "pose": "senala", "mira": "piz"}, {"at": "@poco", "mira": "camara", "cara": "pensativo"}]),
        quien("piz", 790, 0, 0.72, "pensativo", entra="nada", acciones=[
            {"at": "@sueldo", "cara": "sorpresa"}, {"at": "@mucho", "pose": "encoge", "cara": "confundido"},
            {"at": "@leemos", "pose": "senala", "cara": "ilusionado"}, {"at": "@síguenos", "pose": "saluda", "cara": "riendo"},
            {"at": "@compra", "salta": True}]),
        rot("GASTOS ≠ SUELDO", 540, 470, "@Ojo", 90, "amarillo", golpe=True, out="@mucho"),
        rot("¿MUCHO O POCO?", 540, 470, "@mucho", 100, "amarillo", golpe=True, out="@síguenos"),
        rot("SÍGUENOS", 540, 470, "@síguenos", 110, "amarillo", fx=[{"at": "@compra", "do": "latir"}]),
    ]),
]

SB = dict(base.SB)
SB.update(
    slug="sueldo_diputado", title="¿Cuánto cobra un diputado?", series_tag="TU DINERO, CON DATOS",
    scenes=scenes, banda=True, music_volume=0.2, scribble_volume=0.0, sfx_volume=1.0, end_hold=0.9,
    portada={"t": 3.4, "titulo": "¿Cuánto cobra un diputado?", "capitulo": None},
    sources=["Congreso de los Diputados: régimen económico de los diputados, retribuciones 2026",
             "INE: Encuesta Anual de Estructura Salarial 2024 (28/05/2026)", "SMI 2026: Real Decreto 126/2026"],
    caption=("🏛️ Un diputado cobra en un año lo que el trabajador mediano gana en casi tres\n"
             "💶 Asignación: 3.367 €/mes · gastos (fuera de Madrid): 2.163 €/mes, sin IRPF\n"
             "📊 Total: 5.530 €/mes, unos 66.000 € al año\n"
             "🧑‍💼 Sueldo mediano (INE): 24.497 € → 2,7 años · SMI: 3,9 años\n"
             "⚖️ Los gastos compensan vivir lejos de casa: no son sueldo\n"
             "💬 ¿Mucho o poco?\n"
             "➡️ Próximo: la cesta de la compra · 🔔 Síguenos · 📚 Fuentes en comentarios"),
    pinned_comment=("📚 Fuentes: Congreso de los Diputados, régimen económico 2026 (asignación 3.366,99 €/mes; indemnización 2.162,85 €/mes "
                    "fuera de Madrid y 1.032,38 € en Madrid, exenta de IRPF; portavoz +3.197,41 €; Presidencia 14.330,84 €/mes, suma propia) · "
                    "INE, Estructura Salarial 2024: mediana 24.497,17 € · SMI 2026 (RD 126/2026): 17.094 €. Cálculo con 12 pagas; el Congreso "
                    "no publica el número de pagas (con 14 de asignación, 73.092 €). Diputado sin cargo, de fuera de Madrid. ¿Ves un error? Dínoslo."),
    hashtags=["#PizarraPública", "#Congreso", "#Diputados", "#Sueldos", "#INE", "#TuDinero", "#Elecciones29N"],
)

if __name__ == "__main__":
    path = os.path.join(OUT, f"{SB['slug']}.json")
    json.dump(SB, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(path)
