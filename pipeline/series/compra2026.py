#!/usr/bin/env python3
"""«Álex quiere comprarse una casa» (2026): primer vídeo con el estándar de enganche (estilo «viva»).

Álex es un personaje; los datos son reales:
  Consejo de la Juventud de España (CJE), Observatorio de Emancipación, nota del 22/05/2026 (cje.org/observatorio_2025):
    sueldo medio de una persona joven 14.292 €/año (1.191 €/mes); alquiler medio 1.176 €/mes (98,7 %);
    precio medio de la vivienda libre 223.000 €; entrada necesaria 66.900 € (30 %: 20 % no financiado + gastos);
    4,7 años de sueldo íntegro para reunirla.
  Ministerio de Vivienda, valor tasado de la vivienda libre, 2.º trimestre 2026 (17/09/2026): 2.355 €/m², +12,5 % interanual.
    Sobre 223.000 €: 223.000 − 223.000/1,125 ≈ 24.800 € más en un año (cálculo propio).
  INE, Estadística de hipotecas, julio 2026 (28/09/2026): tipo medio 3,01 %.
    Cuota: 80 % de 223.000 = 178.400 € a 30 años al 3,01 % → 753 €/mes = 63 % de 1.191 € (cálculo propio).
  Regla de los bancos: la cuota no debería pasar del 30-35 % de los ingresos netos (criterio habitual de concesión).
  ITP de segunda mano 2026: del 4 % (País Vasco) al 10 % (Cataluña) → 8.920-22.300 € sobre 223.000 €.
Uso: python3 series/compra2026.py  → storyboards/compra2026_alex.json
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "storyboards")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
from padres_viva import V  # noqa: E402
from vivienda import T, stamp  # noqa: E402

VOZ = {"engine": "elevenlabs", "voice_id": "Iohr8NC0THLcVZXLaHlP"}  # «Pizarra Pública»
C = "red"
CJE = "Consejo de la Juventud · Observatorio de Emancipación (mayo 2026)"


def alex(x, y, scale, at, cara="normal", caras=(), **kw):
    return dict(type="tu", etiqueta="ÁLEX", x=x, y=y, scale=scale, at=at, dur=0.6, cara=cara, caras=list(caras), **kw)


scenes = [
    # GANCHO: lo tiene todo… y le dicen que no
    dict(id="gancho", lines=[
        V("Álex tiene trabajo fijo y cinco años ahorrando.", "energia"),
        V("Y aun así, el banco le va a decir que no.", "remate", 0.2),
        V("Síguenos, que esto te sonará."),
    ], elements=[
        alex(300, 980, 1.45, 0, caras=[{"at": "@no", "cara": "susto"}, {"at": "@sonara", "cara": "duda"}]),
        dict(type="check", x=560, y=560, r=40, color="green", width=12, at="@trabajo", dur=0.25),
        T("trabajo fijo", 615, 585, 70, align="left", at="@trabajo", dur=0.35),
        dict(type="check", x=560, y=730, r=40, color="green", width=12, at="@ahorrando", dur=0.25),
        T("5 años ahorrando", 615, 755, 54, align="left", at="@cinco", dur=0.4),
        T("EL BANCO…", 760, 930, 70, color="gray", at="@banco", dur=0.3),
        stamp("DENEGADA", "hipoteca", "@no", y=1060, w=440, h=140, size=64) | {"x": 760, "color": C, "golpe": True},
        stamp("SÍGUENOS", "@pizarrapublica", "@síguenos", y=1300, w=420, h=120, size=54) | {"x": 760},
    ]),
    # EL PISO Y EL 80 %
    dict(id="precio", footnote=CJE, lines=[
        V("Piso medio en España: 223.000 euros.", "normal"),
        V("El banco presta el 80 %. El resto, lo pone él.", "intriga"),
    ], elements=[
        dict(type="icon", name="house", x=540, y=600, scale=1.7, at=0.05, dur=0.6),
        dict(type="cara", x=540, y=640, scale=1.1, cara="normal", at="@medio", dur=0.25, caras=[{"at": "@banco", "cara": "risa"}]),
        T("223.000 €", 540, 1010, 190, color=C, at="@223.000", dur=0.35, golpe=True,
          fx=[{"at": "@banco", "do": "mover", "y": 860, "scale": 0.75}]),
        dict(type="gauge", box=[140, 1000, 800, 90], value=80, max=100, color="blue", at="@80", dur=0.9),
        T("el banco: 80 %", 140 + 400 * 0.8, 1160, 56, font="body", color="blue", at="@80", dur=0.3),
        T("ÁLEX: 20 % + gastos", 540, 1290, 76, color=C, at="@resto", dur=0.4),
    ]),
    # LA ENTRADA
    dict(id="entrada", footnote=CJE, lines=[
        V("Entrada, impuestos y notaría: 66.900 euros.", "sorpresa"),
        V("Álex tiene 20.000.", "remate", 0.3),
        V("Le faltan casi 47.000.", "remate"),
    ], elements=[
        T("entrada", 200, 470, 64, at="@entrada", dur=0.25),
        T("+ impuestos", 520, 470, 64, at="@impuestos", dur=0.3),
        T("+ notaría", 860, 470, 64, at="@notaría", dur=0.25),
        T("66.900 €", 540, 650, 170, color=C, at="@66.900", dur=0.35, golpe=True),
        dict(type="bars", x=170, y=1220, h=430, bar_w=170, gap=90, max=70,
             bars=[{"label": "NECESITA", "value": 66.9, "value_label": "66.900", "color": C}], at="@66.900+0.3", dur=0.7),
        dict(type="bars", x=430, y=1220, h=430, bar_w=170, gap=90, max=70,
             bars=[{"label": "TIENE", "value": 20, "value_label": "20.000", "color": "green"}], at="@20.000", dur=0.6),
        alex(830, 1010, 1.15, "@tiene", caras=[{"at": "@faltan", "cara": "susto"}]),
        T("faltan 46.900 €", 540, 1340, 74, color=C, at="@faltan", dur=0.35, fx=[{"at": "@47.000", "do": "latir"}]),
    ]),
    # BUCLE ABIERTO: el piso corre más que él
    dict(id="sube", footnote="Ministerio de Vivienda, 2.º trim. 2026 (+12,5 % anual) · cálculo sobre 223.000 €", lines=[
        V("Pero lo peor no es eso.", "intriga"),
        V("Mientras ahorra, el piso sube un 12,5 % en un año.", "normal"),
        V("Casi 25.000 euros más. Más que todo lo que ahorró.", "sorpresa"),
    ], elements=[
        T("…Y LO PEOR", 540, 470, 96, at=0.05, dur=0.35),
        dict(type="icon", name="house", x=430, y=700, scale=1.0, at="@ahorra", dur=0.5,
             fx=[{"at": "@sube", "do": "mover", "y": 640, "scale": 1.1}, {"at": "@12,5", "do": "temblar"}]),
        dict(type="arrow", **{"from": [620, 820], "to": [790, 560]}, color=C, width=10, at="@sube", dur=0.35),
        T("+12,5 %", 540, 990, 180, color=C, at="@12,5", dur=0.3, golpe=True),
        T("+25.000 € el piso", 540, 1140, 96, color=C, at="@25.000", dur=0.35, fx=[{"at": "@todo", "do": "rodear"}]),
        T("20.000 € sus ahorros", 540, 1280, 72, font="body", color="gray", at="@ahorró", dur=0.35),
    ]),
    # GIRO: la hipoteca le saldría más barata que el alquiler
    dict(id="absurdo", musica="corte", trans="borrador",
         footnote="INE, julio 2026: tipo medio 3,01 % · 80 % a 30 años · alquiler: CJE", lines=[
        V("Y lo más absurdo:", "intriga", 0.5),
        V("su hipoteca serían 753 euros al mes.", "sorpresa"),
        V("Menos que un alquiler medio: 1.176.", "remate"),
    ], elements=[
        T("LO MÁS ABSURDO", 540, 480, 96, at=0.05, dur=0.4, fx=[{"at": "@absurdo", "do": "temblar"}, {"at": "@753", "do": "subrayar"}]),
        T("HIPOTECA", 290, 690, 70, at="@hipoteca", dur=0.3),
        T("753 €", 290, 850, 160, color="green", at="@753", dur=0.3, golpe=True),
        T("al mes", 290, 950, 56, font="body", at="@mes", dur=0.25),
        T("ALQUILER", 790, 690, 70, at="@alquiler", dur=0.3),
        T("1.176 €", 790, 850, 160, color=C, at="@1.176", dur=0.3, golpe=True),
        T("<", 540, 860, 150, at="@menos", dur=0.2, golpe=True),
        dict(type="cara", x=540, y=1170, scale=1.6, cara="duda", at="@menos", dur=0.3,
             caras=[{"at": "@1.176", "cara": "enfado"}]),
    ]),
    # EL MOTIVO DEL «NO»
    dict(id="motivo", trans="papel", footnote="Criterio habitual de los bancos: cuota ≤ 30-35 % del sueldo · sueldo joven: CJE", lines=[
        V("¿Y por qué se la niegan?", "intriga"),
        V("El banco no acepta cuotas de más del 35 % del sueldo.", "normal"),
        V("Y la de Álex sería el 63 %.", "remate", 0.2),
    ], elements=[
        dict(type="icon", name="question", x=540, y=560, scale=0.9, at=0.05, dur=0.4, fx=[{"at": "@banco", "do": "borrar"}]),
        T("MÁXIMO 35 %", 540, 560, 110, at="@35", dur=0.35),
        dict(type="gauge", box=[140, 760, 800, 100], value=63, max=100, mark=35, color=C, at="@sueldo", dur=1.2),
        T("35 %", 140 + 800 * 0.35, 730, 50, font="body", at="@sueldo", dur=0.2),
        T("63 %", 540, 1110, 220, color=C, at="@63", dur=0.3, golpe=True),
        alex(860, 1190, 0.85, "@niegan", cara="enfado", caras=[{"at": "@63", "cara": "triste"}]),
    ]),
    # FINAL: conclusión + siguiente capítulo + síguenos
    dict(id="conclusion", trans="zoom", lines=[
        V("Así que Álex paga 1.176 de alquiler… por no poder pagar 753 de hipoteca.", "remate"),
    ], elements=[
        alex(540, 1060, 1.35, 0.05, cara="triste"),
        T("paga 1.176 €", 270, 470, 76, color=C, at="@1.176", dur=0.3, golpe=True, fx=[{"at": "@poder", "do": "temblar"}]),
        T("753 €", 810, 470, 90, color="green", at="@753", dur=0.3, fx=[{"at": "@hipoteca", "do": "tachar"}]),
    ]),
    dict(id="final", trans="barrido", lines=[
        V("¿Y qué proponen PSOE, PP y Vox para Álex? En el próximo vídeo.", "energia"),
        V("Síguenos para no perdértelo.", "energia"),
    ], elements=[
        alex(540, 800, 1.3, 0.05, cara="duda", caras=[{"at": "@síguenos", "cara": "risa"}]),
        T("PSOE", 230, 1180, 96, color="psoe", at="@psoe", dur=0.25, golpe=True),
        T("PP", 540, 1180, 96, color="pp", at="@pp", dur=0.2, golpe=True),
        T("VOX", 850, 1180, 96, color="vox", at="@vox", dur=0.25, golpe=True),
        stamp("SÍGUENOS", "@pizarrapublica", "@síguenos", y=1330, w=480, h=120, size=56)
        | {"fx": [{"at": "@perdértelo", "do": "latir"}]},
    ]),
]

SB = dict(
    slug="compra2026_alex", title="Álex quiere comprarse una casa", series_tag="COMPRAR CASA EN 2026", accent=C,
    estilo="viva", icon_accent={"blue": "gray", "red": "yellow"},
    handle="@pizarrapublica", voice=VOZ,
    music_volume=0.12, scribble_volume=0.05, end_hold=1.0,
    sources=[
        "Consejo de la Juventud de España, Observatorio de Emancipación (nota 22/05/2026): https://www.cje.org/en/observatorio_2025/",
        "Ministerio de Vivienda, valor tasado de la vivienda libre, 2.º trimestre 2026 (17/09/2026)",
        "INE, Estadística de hipotecas, julio 2026 (28/09/2026): https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736170236&menu=ultiDatos&idp=1254735576757",
    ],
    caption=("🏠 Álex tiene trabajo fijo y 5 años ahorrando. El banco le dice que no.\n"
             "💶 Piso medio: 223.000 € · entrada + impuestos: 66.900 €\n"
             "📈 El piso sube un 12,5 % en un año: casi 25.000 € más\n"
             "🤯 Su hipoteca: 753 €/mes. Su alquiler: 1.176 €\n"
             "💬 ¿Te ha pasado algo parecido? Cuéntanoslo\n"
             "➡️ Próximo: qué proponen PSOE, PP y Vox · 🔔 Síguenos · 📚 Fuentes en comentarios"),
    pinned_comment=("📚 Fuentes: Consejo de la Juventud, Observatorio de Emancipación (mayo 2026): sueldo joven 1.191 €/mes, "
                    "alquiler 1.176 €, precio medio 223.000 €, entrada 66.900 € · Ministerio de Vivienda 2T 2026: +12,5 % · "
                    "INE hipotecas jul. 2026: tipo medio 3,01 % · Cuota calculada al 80 % y 30 años. Álex es un personaje; "
                    "los datos son reales. ¿Ves un error? Dínoslo."),
    hashtags=["#PizarraPública", "#Vivienda", "#Hipoteca", "#ComprarCasa", "#Jóvenes", "#Alquiler", "#España"],
    scenes=scenes,
)

if __name__ == "__main__":
    path = os.path.join(OUT, f"{SB['slug']}.json")
    json.dump(SB, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(path)
