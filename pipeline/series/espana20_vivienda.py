#!/usr/bin/env python3
"""Storyboard de «España en 20 años · La vivienda» (cierre de la Serie 1 · Vivienda).

Datos oficiales 2006-2026 con gráfica de línea, contadores y barras. Guion revisado por joel:
docs/series/vivienda/guion_vivienda_20_anos.md
Uso: python3 series/espana20_vivienda.py  → storyboards/espana20_vivienda.json
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "storyboards")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
from vivienda import T  # noqa: E402


def counter(frm, to, y, size=170, color="ink", at="+0.05", dur=1.2, decimals=0, sep=True, prefix="", suffix="", **kw):
    return dict(type="counter", **{"from": frm}, to=to, x=540, y=y, size=size, color=color, at=at, dur=dur,
                decimals=decimals, sep=sep, prefix=prefix, suffix=suffix, **kw)


def stamp(text, sub, at, x=540, y=1250, w=600, h=150, size=60, color="ink", rotate=-5, **kw):
    return dict(type="stamp", text=text, sub=sub, x=x, y=y, w=w, h=h, size=size, color=color, rotate=rotate, at=at, dur=0.55, **kw)


def bar(label, value, vmax, x, color, value_label, at, dur=0.9, y=1100, h=520, bw=230):
    return dict(type="bars", x=x, y=y, h=h, bar_w=bw, gap=60, max=vmax, at=at, dur=dur,
                bars=[dict(label=label, value=value, color=color, value_label=value_label)])


SCENES = [
    dict(id="gancho", lines=["En 2007 se terminaron más de 640.000 casas en España.", "En 2025, solo 92.000."], tail=0.35, zoom=0.05,
         elements=[
             dict(type="icon", name="crane", x=540, y=660, scale=1.4, at=0, dur=0.9),
             T("2007", 540, 1015, 90, color="gray", at=0.1, dur=0.3, out="L1"),
             counter(0, 641419, 1205, 180, at=0.2, dur=1.4, out="L1"),
             T("2025", 540, 1015, 90, color="red", at="L1", dur=0.3),
             counter(641419, 92000, 1205, 180, color="red", at="L1", dur=1.1),
             T("viviendas terminadas al año", 540, 1295, 58, font="body", color="gray", at=0.3, dur=0.5),
         ]),
    dict(id="titulo", lines=["Así ha cambiado la vivienda en veinte años."], tail=0.3,
         elements=[
             T("ESPAÑA EN 20 AÑOS", 540, 480, 76, at="L0", dur=0.5),
             T("2006", 290, 720, 170, at="+0.05", dur=0.4),
             dict(type="arrow", **{"from": [440, 660], "to": [620, 660]}, width=10, curve=0.1, at="+0.05", dur=0.35),
             T("2026", 800, 720, 170, color="red", at="+0.05", dur=0.4),
             dict(type="icon", name="house", x=540, y=1010, scale=1.25, fill="light", at="+0.05", dur=0.7),
             T("LA VIVIENDA", 540, 1290, 120, at="+0.05", dur=0.45),
         ]),
    dict(id="precio", lines=["En 2006, el metro cuadrado costaba 1.990 euros.",
                             "En 2008 tocó techo: 2.101. Y la burbuja estalló.",
                             "En 2014 se hundió hasta 1.456.",
                             "Hoy está en 2.355 euros: récord histórico."],
         footnote="Ministerio de Vivienda, valor tasado: 4.º trim. 2006, 1.er trim. 2008,\n3.er trim. 2014 y 2.º trim. 2026", zoom=0.02,
         elements=[
             T("PRECIO DE LA VIVIENDA (€/m²)", 540, 440, 66, at="L0", dur=0.5),
             dict(type="linechart", box=[150, 560, 800, 600], min=1200, max=2500, x_from=2006, x_to=2026,
                  color="ink", width=13, area="blue", at="L0", dur=0.5, seg_dur=0.9,
                  reveal_at=["L0@0.6", "L1@0.25", "L2@0.4", "L3@0.35"],
                  points=[dict(x=2006, value=1990.5, value_label="1.990", label_dx=60, label_dy=80),
                          dict(x=2008, value=2101.4, value_label="2.101", label_dx=40, label=""),
                          dict(x=2014, value=1455.8, value_label="1.456", label_dy=80),
                          dict(x=2026, value=2355, value_label="2.355", color="red", label_dx=-30)]),
             stamp("BURBUJA", None, "L1@0.75", x=520, y=640, w=360, h=110, size=56, rotate=-8, out="L2@0.7"),
             stamp("RÉCORD", None, "L3@0.6", x=720, y=690, w=320, h=110, size=58, color="red", rotate=-6),
         ]),
    dict(id="ojo", lines=["Pero ojo: desde 2006, el precio ha subido un 18 %.", "Y el sueldo medio, un 50 %."],
         footnote="Ministerio de Vivienda (precio) · INE, Estructura Salarial 2006 y 2024",
         elements=[
             T("¡OJO!", 540, 470, 120, color="red", at="L0", dur=0.35),
             bar("precio", 18, 50, 180, "red", "+18 %", "L0@0.5"),
             T("de 1.990 a 2.355 €/m²", 295, 1250, 44, font="body", color="gray", at="+0.1", dur=0.4),
             bar("sueldo", 50, 50, 670, "green", "+50 %", "L1@0.2"),
             T("de 19.681 a 29.540 €/año", 785, 1250, 44, font="body", color="gray", at="+0.1", dur=0.4),
         ]),
    dict(id="problema", lines=["Entonces, ¿cuál es el problema?", "Que faltan casas."], tail=0.35,
         elements=[
             dict(type="icon", name="question", color="red", x=540, y=720, scale=1.6, at="L0", dur=0.6),
             T("FALTAN CASAS", 540, 1130, 150, color="red", at="L1", dur=0.45),
             dict(type="underline", x0=150, x1=930, y=1175, color="red", width=10, at="+0.02", dur=0.3),
         ]),
    dict(id="poblacion", lines=["Somos cinco millones más que en 2006."],
         footnote="INE: Padrón a 1/1/2006 y población residente a 1/7/2026",
         elements=[
             *[dict(type="icon", name="person", accent="light", x=140 + i * 200, y=650, scale=0.8, at=f"L0@{0.05 + i * 0.08:.2f}", dur=0.4)
               for i in range(5)],
             counter(44.7, 49.8, 1060, 190, at="L0@0.2", dur=1.6, decimals=1, sep=False, suffix=" M"),
             T("habitantes en España", 540, 1160, 60, font="body", color="gray", at="L0@0.4", dur=0.4),
             T("+5,1 millones", 540, 1290, 96, color="blue", at="L0@0.8", dur=0.4),
         ]),
    dict(id="hogares", lines=["En 2025 se crearon 240.000 hogares nuevos.", "Y se terminaron 92.000 viviendas."],
         footnote="Banco de España, Informe Anual 2025",
         elements=[
             T("SOLO EN 2025", 540, 450, 80, at="L0", dur=0.4),
             bar("hogares", 240000, 240000, 180, "blue", "240.000", "L0@0.3"),
             bar("viviendas", 92000, 240000, 670, "gray", "92.000", "L1@0.2"),
             dict(type="line", pts=[[420, 580], [900, 580]], color="red", width=6, at="L1@0.7", dur=0.25),
             T("faltan\n148.000", 785, 700, 64, color="red", at="+0.05", dur=0.4, line_height=1.0),
         ]),
    dict(id="deficit", lines=["Resultado: ya faltan 750.000 viviendas."], tail=0.5,
         footnote="Banco de España, Informe Anual 2025 (déficit acumulado 2021-2025)",
         elements=[
             *[dict(type="icon", name="house", color="gray", fill="paper", x=220 + i * 320, y=660, scale=0.95, at=f"L0@{i * 0.12:.2f}", dur=0.45)
               for i in range(3)],
             counter(0, 750000, 1110, 200, color="red", at="L0@0.25", dur=1.6),
             T("viviendas que faltan", 540, 1215, 64, font="body", color="gray", at="L0@0.3", dur=0.4),
         ]),
    dict(id="alquiler", lines=["¿Consecuencias? El alquiler ha pasado de 10 a 14 euros el metro."],
         footnote="Fotocasa: máximo de mayo de 2007 y julio de 2026 (€/m² al mes)",
         elements=[
             T("CONSECUENCIAS", 540, 450, 90, color="red", at="L0", dur=0.4),
             dict(type="icon", name="document", x=540, y=680, scale=1.0, at="+0.05", dur=0.5),
             T("ALQUILER", 540, 860, 72, at="+0.05", dur=0.35),
             T("10,12 €", 280, 1040, 110, color="gray", at="L0@0.45", dur=0.35),
             dict(type="arrow", **{"from": [440, 1000], "to": [600, 1000]}, width=9, curve=0.1, at="+0.02", dur=0.3),
             T("14,14 €", 800, 1040, 120, color="red", at="+0.02", dur=0.35),
             T("2007", 280, 1110, 46, font="body", color="gray", at="L0@0.45", dur=0.3),
             T("2026", 800, 1110, 46, font="body", color="gray", at="+0.3", dur=0.3),
             stamp("+40 %", "por metro cuadrado", "L0@0.8", y=1260, w=380, h=130, size=60, color="red"),
         ]),
    dict(id="jovenes", lines=["Los jóvenes con casa propia han bajado del 41 al 22 %."],
         footnote="Banco de España, Informe Anual 2025",
         elements=[
             T("JÓVENES CON CASA PROPIA", 540, 460, 74, at="L0", dur=0.45),
             T("2007", 140, 650, 64, align="left", at="L0@0.2", dur=0.3),
             T("41 %", 940, 650, 76, align="right", color="blue", at="+0.02", dur=0.3),
             dict(type="gauge", box=[140, 690, 800, 110], value=41, max=100, color="blue", at="+0.02", dur=0.9),
             T("2025", 140, 960, 64, align="left", at="L0@0.6", dur=0.3),
             T("22 %", 940, 960, 76, align="right", color="red", at="+0.02", dur=0.3),
             dict(type="gauge", box=[140, 1000, 800, 110], value=22, max=100, color="red", at="+0.02", dur=0.9),
             T("casi la mitad que antes", 540, 1270, 64, font="body", color="gray", at="L0@0.85", dur=0.4),
         ]),
    dict(id="emancipacion", lines=["Y nos vamos de casa de los padres a los 30. En 2006, a los 28 y medio."],
         footnote="Eurostat: edad media al dejar el hogar familiar, 2006 y 2025",
         elements=[
             T("EDAD PARA IRSE DE CASA", 540, 460, 76, at="L0", dur=0.45),
             dict(type="icon", name="calendar", x=540, y=720, scale=1.1, at="+0.05", dur=0.55),
             counter(28.7, 30.2, 1110, 200, at="L0@0.45", dur=1.6, decimals=1, sep=False, suffix=" años"),
             T("en 2006: 28,7", 540, 1230, 56, font="body", color="gray", at="L0@0.3", dur=0.4),
         ]),
    dict(id="futuro", lines=["¿Y si seguimos así? Cada año, más hogares que casas.",
                             "Al ritmo de 2025, en 2030 faltaría más de un millón de viviendas."],
         footnote="Cálculo propio con datos del Banco de España:\n750.000 + 148.000 al año durante 5 años",
         elements=[
             T("¿Y SI SEGUIMOS ASÍ?", 540, 460, 90, at="L0", dur=0.45),
             dict(type="arrow", **{"from": [170, 1020], "to": [880, 600]}, color="blue", width=10, curve=-0.08, at="L0@0.45", dur=0.6, out="L1"),
             T("hogares", 880, 560, 58, color="blue", at="+0", dur=0.3, out="L1"),
             dict(type="arrow", **{"from": [170, 1020], "to": [880, 900]}, color="gray", width=10, curve=-0.05, at="L0@0.6", dur=0.6, out="L1"),
             T("casas", 880, 980, 58, color="gray", at="+0", dur=0.3, out="L1"),
             T("2030", 540, 720, 140, at="L1@0.15", dur=0.4),
             counter(750000, 1000000, 950, 190, color="red", at="L1@0.3", dur=1.6, prefix="+"),
             T("viviendas que faltarían", 540, 1050, 60, font="body", color="gray", at="L1@0.35", dur=0.4),
             stamp("ESTIMACIÓN", "cálculo propio · datos BdE", "L1@0.8", y=1250, w=560, h=140, size=56),
         ]),
    dict(id="cierre", lines=["¿Y tú, cuándo podrás tener casa?", "Síguenos: ahora, los impuestos."],
         elements=[
             T("¿Y TÚ?", 540, 560, 170, at="L0", dur=0.4),
             dict(type="icon", name="house", x=540, y=820, scale=1.0, fill="yellow", at="+0.05", dur=0.55),
             T("PRÓXIMO", 540, 1060, 70, color="gray", at="L1", dur=0.3),
             T("IMPUESTOS", 540, 1200, 130, color="blue", at="+0.05", dur=0.4),
         ]),
]

STORY = {
    "slug": "espana20_vivienda",
    "title": "España en 20 años · La vivienda",
    "series_tag": "ESPAÑA EN 20 AÑOS · VIVIENDA",
    "accent": "red",
    "icon_accent": {},
    "handle": "@pizarrapublica",
    "voice": {"engine": "edge", "voice_id": "es-ES-AlvaroNeural"},
    "music_volume": 0.15,
    "music_bpm": 96,
    "scribble_volume": 0.05,
    "end_hold": 0.9,
    "line_gap": 0.1,
    "sources": [
        "Ministerio de Vivienda, valor tasado 2.º trim. 2026 (2.355 €/m²): https://www.pressdigital.es/articulo/economia/2026-09-17/6018677-vivienda-sube-125-segundo-trimestre-alcanza-nuevo-record-2355-euros-metro-cuadrado",
        "Máximo 1.er trim. 2008 (2.101,4 €/m²): https://www.eldiario.es/economia/precio-medio-vivienda-libre-sube-10-4-segundo-trimestre-acerca-maximo-2008_1_12616074.amp.html",
        "Mínimo 3.er trim. 2014 (1.455,8 €/m²): https://www.idealista.com/news/node/743555",
        "Finales de 2006 (1.990,50 €/m²): https://www.consumer.es/vivienda/el-precio-de-la-vivienda-aumento-un-91-en-2006-segun-datos-oficiales.html",
        "INE, salario medio 2006 (19.680,88 €): https://ine.es/daco/daco42/salarial/prinre06.pdf",
        "INE, salario medio 2024 (29.540,26 €): https://ine.es/dyngs/Prensa/EAES2024.htm",
        "Padrón 1/1/2006 (44.708.964), RD 1627/2006: https://www.boe.es/eli/es/rd/2006/12/29/1627",
        "INE, población 1/7/2026 (49.801.559): https://ine.es/dyngs/Prensa/ECP2T26.htm",
        "Banco de España, Informe Anual 2025 (déficit 750.000; 240.000 hogares; 92.000 viviendas; jóvenes propietarios 41 % a 22 %): https://www.eldiario.es/economia/banco-espana-eleva-750-000-viviendas-faltan-anticipa-deficit-agravara-proximos-anos_1_13313634.amp.html",
        "Fomento, 641.419 viviendas terminadas en 2007: https://www.consumer.es/?p=209953",
        "Fotocasa, alquiler: máximo de mayo de 2007 (10,12 €/m²): https://prensa.fotocasa.es/wp-content/uploads/2018/01/NdP-Indice-Anual-Alquiler-2017.pdf",
        "Fotocasa, julio de 2026 (14,14 €/m²): https://www.bolsamania.com/noticias_print/empresas/economiavivienda--el-precio-del-alquiler-rompe-en-julio-con-52-meses-de-alzas-tras-bajar-un-16-segun-fotocasa--23202603.html",
        "Eurostat yth_demo_030 (28,7 en 2006; 30,2 en 2025): https://ec.europa.eu/eurostat/databrowser/view/yth_demo_030/default/table",
    ],
    "caption": "🏠 La vivienda en España: 2006 → 2026\n📈 Precio récord: 2.355 €/m² (en 2008 eran 2.101)\n💶 Pero el sueldo medio ha subido más que el precio\n🏗️ En 2007 se terminaron 641.000 casas; en 2025, 92.000\n❗ Faltan 750.000 viviendas y los jóvenes propietarios bajan del 41 al 22 %\n💬 ¿A qué edad te independizaste (o cuándo crees que podrás)?\n➡️ España en 20 años · 📚 Fuentes en comentarios",
    "pinned_comment": "📚 Fuentes: Ministerio de Vivienda (valor tasado 2006-2026), INE (salarios 2006 y 2024; población), Banco de España (Informe Anual 2025), Fotocasa, Eurostat. La cifra de 2030 es un cálculo nuestro con datos del Banco de España. ¿Ves un error? Dínoslo.",
    "hashtags": ["#PizarraPública", "#PolíticaEspañola", "#Elecciones29N", "#Vivienda", "#Alquiler", "#España20Años"],
    "scenes": SCENES,
}

if __name__ == "__main__":
    path = os.path.join(OUT, "espana20_vivienda.json")
    json.dump(STORY, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(path)
