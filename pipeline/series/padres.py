#!/usr/bin/env python3
"""«Tus padres a tu edad»: un vídeo corto (≈25 s) en estilo pizarra (motor v1).

Datos:
  Banco de España, Encuesta Financiera de las Familias (vía CaixaBank Research, 2025-2026):
    hogares con cabeza de familia menor de 35 propietarios de su vivienda: 66 % en 2002, 32 % en 2022, ≈36 % en 2024.
  Consejo de la Juventud de España, Observatorio de Emancipación, 2.º semestre de 2025 (EFE, 22/05/2026):
    comprar una vivienda cuesta 15,6 años del sueldo íntegro de un joven; alquiler medio 1.176 € = 98,7 % de su sueldo (1.191 €);
    tasa de emancipación 16-29: 14,5 %; edad media de emancipación 30,2 años.
Uso: python3 series/padres.py  → storyboards/padres_a_tu_edad.json
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "storyboards")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
from vivienda import L, T, fit, stamp  # noqa: E402

VOZ = {"engine": "elevenlabs", "voice_id": "Iohr8NC0THLcVZXLaHlP"}  # «Pizarra Pública»
C = "red"

scenes = [
    dict(id="gancho", lines=[L("A tu edad, dos de cada tres de tus padres ya tenían casa propia.",
                               "A tu edad, dos de cada tres de tus padres ya tenían casa propia."),
                             L("Síguenos, que esto va contigo.")], tail=0.15, elements=[
        T("TUS PADRES", 540, 440, 96, at=0, dur=0.5),
        T("A TU EDAD", 540, 560, 96, color=C, at="+0.05", dur=0.5),
        dict(type="bars", x=300, y=1180, h=480, bar_w=170, gap=130, max=70,
             bars=[{"label": "2002", "value": 66, "color": "gray"}], at="L0@0.3", dur=1.0),
        T("66 %", 385, 640, 80, color="gray", at="L0@0.7", dur=0.3),
        stamp("SÍGUENOS", "@pizarrapublica", "L1", y=1290, w=520, h=130, size=60),
    ]),
    dict(id="hoy", lines=[L("Hoy, solo uno de cada tres.")], footnote="Banco de España · Encuesta Financiera de las Familias (menores de 35)",
         elements=[
        T("¿Y HOY?", 540, 470, 96, at="L0", dur=0.4),
        dict(type="bars", x=300, y=1180, h=480, bar_w=170, gap=130, max=70,
             bars=[{"label": "2002", "value": 66, "color": "gray"},
                   {"label": "2024", "value": 36, "color": C}], at="L0", dur=1.0),
        T("66 %", 385, 640, 80, color="gray", at="L0", dur=0.2),
        T("36 %", 685, 870, 80, color=C, at="L0@0.6", dur=0.3),
    ]),
    dict(id="compra", lines=[L("Comprar un piso hoy cuesta 15,6 años de sueldo íntegro de un joven. Sin gastar ni un euro.",
                               "Comprar un piso hoy cuesta quince coma seis años de sueldo íntegro de un joven. Sin gastar ni un euro.")],
         footnote="Consejo de la Juventud · Observatorio de Emancipación, 2025", elements=[
        dict(type="icon", name="house", x=540, y=560, scale=1.1, at="L0", dur=0.6),
        T("15,6", 540, 900, 220, color=C, at="L0@0.25", dur=0.5),
        T("AÑOS DE SUELDO", 540, 1030, 84, at="+0.05", dur=0.45),
        dict(type="highlight", x0=230, x1=850, y=1170, width=70, at="L0@0.7", dur=0.3),
        T("sin gastar ni un euro", 540, 1190, 70, font="body", at="+0", dur=0.4),
    ]),
    dict(id="alquiler", lines=[L("¿Y alquilar? El alquiler medio se come el 98,7 % de su sueldo.",
                                 "¿Y alquilar? El alquiler medio se come el noventa y ocho coma siete por ciento de su sueldo.")],
         footnote="Consejo de la Juventud · alquiler medio 1.176 € · sueldo joven 1.191 €", elements=[
        T("¿Y ALQUILAR?", 540, 470, 96, at="L0", dur=0.4),
        dict(type="gauge", box=[140, 640, 800, 90], value=98.7, max=100, mark=30, color=C, at="L0@0.3", dur=1.2),
        T("lo sano: 30 %", 140 + 800 * 0.30, 610, 44, font="body", color="gray", at="L0@0.4", dur=0.3),
        T("98,7 %", 540, 950, 190, color=C, at="L0@0.55", dur=0.5),
        T("DE SU SUELDO", 540, 1080, 84, at="+0.05", dur=0.4),
    ]),
    dict(id="cierre", lines=[L("¿Y tú? A: casa propia. B: de alquiler. C: con tus padres. Comenta y síguenos.",
                               "¿Y tú? A: casa propia. B: de alquiler. C: con tus padres. Comenta, y síguenos.")], elements=[
        T("¿Y TÚ?", 540, 520, 130, at="L0", dur=0.4),
        T("A: casa propia", 540, 760, 84, at="L0@0.1", dur=0.3, align="center"),
        T("B: de alquiler", 540, 880, 84, at="L0@0.3", dur=0.3),
        T("C: con mis padres", 540, 1000, 84, color=C, at="L0@0.5", dur=0.3),
        T("COMENTA", 540, 1130, 64, color="gray", at="L0@0.7", dur=0.3),
        stamp("SÍGUENOS", "@pizarrapublica", "L0@0.8", y=1290, w=520, h=130, size=60),
    ]),
]

SB = dict(
    slug="padres_a_tu_edad", title="Tus padres a tu edad", series_tag="TUS PADRES A TU EDAD", accent=C,
    icon_accent={"blue": "gray", "red": "yellow"},
    handle="@pizarrapublica", voice=VOZ,
    music_volume=0.12, scribble_volume=0.05, end_hold=0.8, line_gap=0.06,
    sources=[
        "Banco de España, Encuesta Financiera de las Familias 2002-2024 (vía CaixaBank Research): https://www.caixabankresearch.com/es/economia-y-mercados/mercado-laboral-y-demografia/encuesta-financiera-familias-espana-no-pais-0",
        "Consejo de la Juventud de España, Observatorio de Emancipación, 2.º semestre 2025 (EFE, 22/05/2026)",
    ],
    caption=("🏠 A tu edad, 2 de cada 3 de tus padres ya tenían casa. Hoy, 1 de cada 3.\n"
             "📈 Comprar: 15,6 años de sueldo íntegro de un joven\n"
             "💸 Alquilar: el 98,7 % de su sueldo\n"
             "💬 ¿Y tú? A: casa propia · B: alquiler · C: con tus padres\n"
             "🔔 Síguenos para estar al día · 📚 Fuentes en comentarios"),
    pinned_comment=("📚 Fuentes: Banco de España, Encuesta Financiera de las Familias (hogares menores de 35 con vivienda en propiedad: "
                    "66 % en 2002, 36 % en 2024) · Consejo de la Juventud, Observatorio de Emancipación 2025. ¿Ves un error? Dínoslo."),
    hashtags=["#PizarraPública", "#Vivienda", "#Jóvenes", "#Alquiler", "#Generaciones"],
    scenes=scenes,
)

if __name__ == "__main__":
    path = os.path.join(OUT, "padres_a_tu_edad.json")
    json.dump(SB, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(path)
