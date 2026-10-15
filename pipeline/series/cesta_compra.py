#!/usr/bin/env python3
"""«La cesta de la compra» (2026): cuánto han subido los alimentos desde enero de 2021.

Fuentes (INE, IPC base 2025, ECOICOP v2, datos definitivos de septiembre de 2026, nota del 14/10/2026):
  Alimentos y bebidas no alcohólicas (IPC290755): 74,772 (ene-2021) → 101,934 (sep-2026) = +36,3 %.
  Índice general: 82,407 → 104,978 = +27,4 % (≈ 9 puntos menos).
  50 € de hoy = 50 × 74,772 / 101,934 = 36,68 € en enero de 2021.
  Subclases ene-2021 → sep-2026: huevos +91,1 %, chocolate +58,2 %, aceites vegetales +56,1 %, leche entera +52,5 %, azúcar +25,9 %.
  Tasa anual sep-2026: alimentos +2,7 %, IPC general +4,9 %.
  Matiz: desde 2025 el INE ya no separa el aceite de oliva («aceites vegetales»).
Uso: python3 series/cesta_compra.py → storyboards/cesta_compra.json
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
INE = "INE, IPC base 2025: alimentos y bebidas no alcohólicas, enero 2021 → septiembre 2026 · cálculo propio"


def quien(q, x, at=0.0, scale=0.75, cara="normal", acciones=(), **kw):
    return pj(q, x, at, scale, cara, acciones, id=q, **kw)


def etq(texto, x, y, at, color="amarillo", scale=0.75, **kw):
    return obj("etiqueta", x, y, at, scale, props={"texto": texto, "color": color}, entra="pop", sfx="kaching", **kw)


huevo_els, huevo_piz = gags.cae_del_cielo("HUEVOS +91 %", "@huevos-0.4", 330, 560, scale=1.15)

scenes = [
    # 1 · GANCHO
    dict(id="gancho", fondo="calle", animo="curioso", footnote=INE, lines=[
        V("Lo que hoy pagas 50 euros en el súper, en 2021 te costaba 36.", "energia"),
        V("¿Qué ha subido tanto?", "remate", 0.2),
    ], camara=[plano(0, "general", dur=0), plano("@2021", "abierto", "piz", 0.4)],
       elements=[
        edif("supermercado", 330, 0, 0.62, id="super", entra="nada"),
        quien("piz", 1300, 0, 0.72, "ilusionado", entra="nada", objeto="saco", pose="sostiene", acciones=[
            {"at": "@50", "x": 800, "dur": 0.9}, {"at": "@2021", "take": True, "cara": "susto"},
            {"at": "@subido", "mira": "camara", "cara": "indignado", "pose": "jarras", "objeto": None}]),
        rot("HOY: 50 €", 540, 520, "@50", 100, C, golpe=True),
        rot("2021: 36,68 €", 540, 660, "@2021", 90, "verde", golpe=True),
        rot("¿?", 800, 820, "@subido", 140, "amarillo", golpe=True),
    ]),
    # 2 · EL DATO
    dict(id="ipc", fondo="oficina", animo="curioso", trans="pan", footnote=INE, lines=[
        V("Según el INE, la comida ha subido un 36 % desde enero de 2021.", "normal"),
        V("Nueve puntos más que el resto de precios.", "sorpresa", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@Nueve", "medio", "profe", 0.3, aire=220)],
       elements=[
        quien("profe", 280, 0, 0.75, "normal", entra="izq", pose="senala_arriba", acciones=[
            {"at": "@36", "pose": "senala", "cara": "serio"}, {"at": "@Nueve", "salta": True, "cara": "sorpresa"}]),
        obj("grafica", 760, 860, "@comida", 0.85, entra="pop", props={"valores": [1, 1.1, 1.5, 2.2, 2.6], "color": "rojo"}),
        rot("COMIDA: +36 %", 620, 600, "@36", 90, C, golpe=True),
        rot("RESTO: +27 %", 620, 720, "@Nueve", 76, "amarillo", golpe=True),
    ]),
    # 3 · LOS HUEVOS
    dict(id="huevos", fondo="salon", animo="comico", trans="iris", footnote="INE, subclase «Huevos» (IPC291439): 58,931 → 112,611", lines=[
        V("El récord, los huevos: un 91 % más. Casi el doble.", "sorpresa"),
    ], camara=[plano(0, "general", dur=0), plano("@doble", "medio", "piz", 0.3, aire=200)],
       elements=[
        quien("piz", 330, 0, 0.75, "normal", entra="izq", acciones=huevo_piz + [{"at": "@doble+0.4", "cara": "indignado"}]),
        *huevo_els,
        quien("pizon", 820, "@récord", 0.72, "sorpresa", entra="der", acciones=[{"at": "@doble", "take": True}]),
        rot("× 1,9", 800, 520, "@doble", 120, C, golpe=True),
    ]),
    # 4 · LA LISTA
    dict(id="lista", fondo="salon", animo="tension", trans="pan", footnote="INE, subclases: aceites vegetales (IPC291663) · leche entera (IPC291643) · chocolate (IPC291739)", lines=[
        V("El aceite, un 56 % más. La leche entera, un 52.", "normal"),
        V("Y el chocolate, un 58.", "remate", 0.1),
    ], camara=[plano(0, "general", dur=0), plano("@chocolate", "abierto", dur=0.4)],
       elements=[
        quien("pizon", 260, 0, 0.72, "preocupado", entra="nada", acciones=[
            {"at": "@aceite", "take": True}, {"at": "@leche", "cara": "susto", "tiembla": True},
            {"at": "@chocolate", "tropieza": True}]),
        etq("ACEITE +56 %", 720, 560, "@aceite", "amarillo"),
        etq("LECHE +52 %", 720, 760, "@leche", "blanco"),
        etq("CHOCOLATE +58 %", 720, 960, "@chocolate", "rojo"),
    ]),
    # 5 · GIRO
    dict(id="azucar", fondo="rayos", animo="comico", musica="corte", trans="iris", footnote="INE, subclase «Azúcar» (IPC291731): +25,9 %", lines=[
        V("¿Y el azúcar? Solo un 26 %. De los que menos.", "sorpresa"),
    ], camara=[plano(0, "general", dur=0), plano("@menos", "medio", "sarcastica", 0.3, aire=220)],
       elements=[
        quien("sarcastica", 540, 0, 0.8, "burla", entra="pop", acciones=[
            {"at": "@26", "pose": "pulgar", "cara": "riendo"}, {"at": "@menos", "salta": True}]),
        rot("AZÚCAR: +26 %", 540, 560, "@26", 100, "verde", golpe=True),
    ]),
    # 6 · MATIZ
    dict(id="matiz", fondo="oficina", animo="curioso", trans="pan", footnote="INE, IPC septiembre 2026: alimentos +2,7 % · general +4,9 % (tasa anual)", lines=[
        V("Ojo: este año la comida sube un 2,7 %, menos que el resto, que va al 4,9.", "normal"),
        V("Lo de antes ya no baja: se queda.", "remate", 0.2),
    ], camara=[plano(0, "general", dur=0), plano("@queda", "medio", "piz", 0.3, aire=200)],
       elements=[
        quien("profe", 280, 0, 0.72, "normal", entra="nada", pose="senala_arriba", acciones=[
            {"at": "@2,7", "pose": "senala"}, {"at": "@4,9", "mira": "piz"}, {"at": "@queda", "cara": "serio", "pose": "encoge"}]),
        quien("piz", 800, 0, 0.72, "pensativo", entra="der", acciones=[
            {"at": "@2,7", "cara": "ilusionado", "salta": True}, {"at": "@baja", "cara": "preocupado"},
            {"at": "@queda", "take": True, "cara": "triste"}]),
        rot("COMIDA HOY: +2,7 %", 540, 520, "@2,7", 72, "verde", golpe=True),
        rot("GENERAL: +4,9 %", 540, 640, "@4,9", 72, "amarillo", golpe=True),
    ]),
    # 7 · FINAL
    dict(id="final", fondo="calle", animo="final", trans="iris", footnote="El IPC mide una cesta media: tu ticket puede subir más o menos", lines=[
        V("¿Qué es lo que más notas en tu ticket? Te leemos.", "normal"),
        V("Y síguenos: la próxima, las listas de espera.", "energia", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@síguenos", "abierto", dur=0.4)],
       elements=[
        edif("supermercado", 760, 0, 0.55, id="super", entra="nada"),
        quien("piz", 280, 0, 0.72, "normal", entra="nada", objeto="contrato", pose="sostiene", acciones=[
            {"at": "@notas", "mira": "camara", "cara": "pensativo"}, {"at": "@leemos", "pose": "senala", "cara": "ilusionado", "objeto": None},
            {"at": "@síguenos", "pose": "saluda", "cara": "riendo"}, {"at": "@espera", "salta": True}]),
        rot("¿QUÉ NOTAS MÁS?", 540, 470, "@notas", 100, "amarillo", golpe=True, out="@síguenos"),
        rot("SÍGUENOS", 540, 470, "@síguenos", 110, "amarillo", fx=[{"at": "@espera", "do": "latir"}]),
    ]),
]

SB = dict(base.SB)
SB.update(
    slug="cesta_compra", title="La cesta de la compra", series_tag="TU DINERO, CON DATOS",
    scenes=scenes, banda=True, music_volume=0.2, scribble_volume=0.0, sfx_volume=1.0, end_hold=0.9,
    portada={"t": 3.0, "titulo": "Lo que te cuesta el súper", "capitulo": None},
    sources=["INE: IPC base 2025, alimentos y bebidas no alcohólicas y subclases (septiembre 2026)",
             "INE: nota de prensa IPC septiembre 2026 (14/10/2026)"],
    caption=("🛒 Lo que hoy pagas 50 € en el súper, en enero de 2021 costaba 36,68 €\n"
             "📈 Alimentos: +36 % desde 2021 · IPC general: +27 %\n"
             "🥚 Huevos +91 % · 🫒 Aceites +56 % · 🍫 Chocolate +58 % · 🥛 Leche entera +52 %\n"
             "🍬 Azúcar: solo +26 %\n"
             "📉 Este año la comida sube un 2,7 %, menos que el resto (4,9 %)\n"
             "💬 ¿Qué notas más en tu ticket?\n"
             "➡️ Próximo: listas de espera · 🔔 Síguenos · 📚 Fuentes en comentarios"),
    pinned_comment=("📚 Fuente: INE, IPC base 2025 (ECOICOP v2), datos definitivos de septiembre de 2026 (nota del 14/10/2026). "
                    "Alimentos y bebidas no alcohólicas: índice 74,772 (ene-2021) → 101,934 (sep-2026). Subclases: huevos, aceites vegetales "
                    "(incluye el de oliva, que el INE ya no separa), leche entera, chocolate y azúcar. Cálculo propio de las variaciones. "
                    "El IPC mide una cesta media. ¿Ves un error? Dínoslo."),
    hashtags=["#PizarraPública", "#IPC", "#CestaDeLaCompra", "#Inflación", "#INE", "#TuDinero", "#Supermercado"],
)

if __name__ == "__main__":
    path = os.path.join(OUT, f"{SB['slug']}.json")
    json.dump(SB, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(path)
