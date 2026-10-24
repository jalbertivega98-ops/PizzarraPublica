#!/usr/bin/env python3
"""«Tus padres a tu edad», rehecho con el estándar de enganche (estilo «viva», docs/enganche.md).

Mismos datos que series/padres.py:
  Consejo de la Juventud de España, Observatorio de Emancipación, 2.º semestre de 2025 (EFE, 22/05/2026):
    sueldo medio de una persona joven 1.191 €/mes; alquiler medio 1.176 € (98,7 % del sueldo);
    comprar una vivienda cuesta 15,6 años de sueldo íntegro.
  Banco de España, Encuesta Financiera de las Familias (vía CaixaBank Research):
    hogares con cabeza de familia menor de 35 propietarios: 66 % en 2002, ≈36 % en 2024.
Uso: python3 series/padres_viva.py  → storyboards/padres_viva.json
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "storyboards")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
from vivienda import T, stamp  # noqa: E402

VOZ = {"engine": "elevenlabs", "voice_id": "Iohr8NC0THLcVZXLaHlP"}  # «Pizarra Pública»
C = "red"
CJE = "Consejo de la Juventud · Observatorio de Emancipación, 2.º sem. 2025"
BDE = "Banco de España · Encuesta Financiera de las Familias (menores de 35)"


def V(text, tono=None, pausa=None):
    d = {"text": text}
    if tono:
        d["tono"] = tono
    if pausa:
        d["pausa"] = pausa
    return d


scenes = [
    # GANCHO: contradicción en 2 s, el fotograma 0 ya tiene dibujo
    dict(id="gancho", footnote=CJE, lines=[
        V("Sueldo medio de un joven: 1.191 euros.", "energia"),
        V("Alquiler medio: 1.176.", "sorpresa"),
        V("Te sobran 15 euros.", "remate", 0.25),
        V("Síguenos, que esto va contigo."),
    ], elements=[
        dict(type="tu", x=820, y=930, scale=1.45, at=0, dur=0.7,
             caras=[{"at": "@1.176", "cara": "sorpresa"}, {"at": "@15", "cara": "susto"}, {"at": "@síguenos", "cara": "normal"}]),
        T("SUELDO", 290, 500, 74, at=0.1, dur=0.3),
        T("1.191 €", 290, 650, 150, color="green", at="@1.191", dur=0.35, golpe=True),
        T("ALQUILER", 290, 830, 74, at="@alquiler", dur=0.3),
        T("− 1.176 €", 290, 980, 140, color=C, at="@1.176", dur=0.35, golpe=True),
        dict(type="line", pts=[(60, 1045), (540, 1050)], width=8, at="@sobran", dur=0.2),
        T("15 €", 290, 1230, 210, color=C, at="@15", dur=0.25, golpe=True,
          fx=[{"at": "@euros#2", "do": "rodear"}, {"at": "@contigo", "do": "latir"}]),
        stamp("SÍGUENOS", "@pizarrapublica", "@síguenos", y=1250, w=420, h=120, size=54) | {"x": 820},
    ]),
    # ESCALADA: comprar todavía es peor
    dict(id="comprar", footnote=CJE, lines=[
        V("¿Y comprar? Peor.", "intriga"),
        V("15,6 años de sueldo íntegro.", "sorpresa"),
        V("Sin gastar ni un euro en nada más."),
    ], elements=[
        dict(type="icon", name="house", x=540, y=640, scale=1.9, at=0.05, dur=0.6),
        dict(type="cara", x=540, y=690, scale=1.2, cara="risa", at="@peor", dur=0.25),
        T("15,6", 540, 1080, 270, color=C, at="@15,6", dur=0.3, golpe=True),
        T("AÑOS DE SUELDO", 540, 1190, 92, at="@años", dur=0.35),
        T("sin gastar ni un euro", 540, 1310, 72, font="body", at="@gastar", dur=0.35,
          fx=[{"at": "@nada", "do": "subrayar", "color": C}]),
    ]),
    # BUCLE ABIERTO + COMPARACIÓN: los padres a tu edad, y el giro
    dict(id="padres", footnote=BDE, lines=[
        V("Pero lo que de verdad duele es compararte.", "intriga"),
        V("A tu edad, dos de cada tres de tus padres ya tenían casa.", "normal"),
        V("¿Hoy? Uno de cada tres.", "remate", 0.5),
    ], musica="corte", elements=[
        T("A TU EDAD…", 540, 480, 100, at=0.05, dur=0.35, fx=[{"at": "@hoy", "do": "borrar", "dur": 0.3}]),
        dict(type="tu", x=280, y=1010, scale=1.4, etiqueta="TUS PADRES", color_etiqueta="gray", cara="normal",
             at="@compararte", dur=0.6, caras=[{"at": "@padres", "cara": "risa"}],
             fx=[{"at": "@hoy", "do": "borrar", "dur": 0.4}]),
        dict(type="bars", x=590, y=1250, h=560, bar_w=170, gap=90, max=70,
             bars=[{"label": "2002", "value": 66, "value_label": "66 %", "color": "gray"}], at="@dos", dur=0.8,
             fx=[{"at": "@casa", "do": "latir", "fuerza": 0.08}]),
        dict(type="tu", x=280, y=1010, scale=1.4, cara="triste", at="@uno", dur=0.4),
        dict(type="bars", x=840, y=1250, h=560, bar_w=170, gap=90, max=70,
             bars=[{"label": "2024", "value": 36, "value_label": "36 %", "color": C}], at="@uno", dur=0.6),
        T("1 DE CADA 3", 540, 490, 120, color=C, at="@tres#2", dur=0.25, golpe=True),
    ]),
    # FINAL: pregunta A/B + síguenos
    dict(id="final", lines=[
        V("¿Y tú dónde vives? A: de alquiler. B: con tus padres.", "energia"),
        V("Comenta, y síguenos para el siguiente."),
    ], elements=[
        dict(type="tu", x=540, y=800, scale=1.4, cara="duda", at=0.05, dur=0.5),
        T("A: DE ALQUILER", 540, 1140, 92, at="@a", dur=0.3, fx=[{"at": "@b", "do": "latir"}]),
        T("B: CON MIS PADRES", 540, 1260, 92, color=C, at="@b", dur=0.3, fx=[{"at": "@comenta", "do": "latir"}]),
        stamp("SÍGUENOS", "@pizarrapublica", "@síguenos", y=1370, w=480, h=120, size=56)
        | {"fx": [{"at": "@siguiente", "do": "latir"}]},
    ]),
]

SB = dict(
    slug="padres_viva", title="Tus padres a tu edad", series_tag="TUS PADRES A TU EDAD", accent=C,
    estilo="viva", icon_accent={"blue": "gray", "red": "yellow"},
    handle="@pizarrapublica", voice=VOZ,
    music_volume=0.12, scribble_volume=0.05, end_hold=0.8,
    sources=[
        "Consejo de la Juventud de España, Observatorio de Emancipación, 2.º semestre 2025 (EFE, 22/05/2026)",
        "Banco de España, Encuesta Financiera de las Familias 2002-2024 (vía CaixaBank Research): https://www.caixabankresearch.com/es/economia-y-mercados/mercado-laboral-y-demografia/encuesta-financiera-familias-espana-no-pais-0",
    ],
    caption=("💸 Sueldo medio de un joven: 1.191 €. Alquiler medio: 1.176 €. Te sobran 15 €.\n"
             "🏠 Comprar: 15,6 años de sueldo íntegro\n"
             "👨‍👩‍👦 A tu edad, 2 de cada 3 de tus padres ya tenían casa. Hoy, 1 de cada 3\n"
             "💬 ¿Y tú? A: de alquiler · B: con tus padres\n"
             "🔔 Síguenos · 📚 Fuentes en comentarios"),
    pinned_comment=("📚 Fuentes: Consejo de la Juventud, Observatorio de Emancipación 2.º sem. 2025 (sueldo joven 1.191 €, "
                    "alquiler medio 1.176 €, compra = 15,6 años de sueldo) · Banco de España, Encuesta Financiera de las Familias "
                    "(menores de 35 con vivienda en propiedad: 66 % en 2002, 36 % en 2024). ¿Ves un error? Dínoslo."),
    hashtags=["#PizarraPública", "#Vivienda", "#Jóvenes", "#Alquiler", "#Generaciones"],
    scenes=scenes,
)

if __name__ == "__main__":
    path = os.path.join(OUT, "padres_viva.json")
    json.dump(SB, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(path)
