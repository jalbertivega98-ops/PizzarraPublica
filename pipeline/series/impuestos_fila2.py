#!/usr/bin/env python3
"""Segunda fila de Impuestos en TikTok: «Los tres, cara a cara», «¿Adónde van tus impuestos?» y
«España en 20 años · Impuestos». Guiones: docs/series/impuestos/guiones_impuestos_fila2.md
Uso: python3 series/impuestos_fila2.py  → storyboards/impuestos_{comparativa,adonde_van}.json y espana20_impuestos.json
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "storyboards")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
from espana20_vivienda import bar, counter, stamp  # noqa: E402
from impuestos import coin  # noqa: E402
from vivienda import T  # noqa: E402

PARTIES = [("PSOE", "psoe", 200), ("PP", "pp", 540), ("VOX", "vox", 880)]
VOICE = {"engine": "edge", "voice_id": "es-ES-AlvaroNeural"}
TT_TAGS = ["#PizarraPública", "#PolíticaEspañola", "#Elecciones29N", "#Impuestos", "#AprendeEnTikTok"]


def base(slug, title, tag, accent, scenes, caption, pinned, sources, hashtags):
    return dict(slug=slug, title=title, series_tag=tag, accent=accent, icon_accent={"blue": "gray", "red": "yellow"},
                handle="@pizarrapublica", voice=VOICE, music_volume=0.15, music_bpm=96, scribble_volume=0.05,
                end_hold=0.9, line_gap=0.1, sources=sources, caption=caption, pinned_comment=pinned, hashtags=hashtags,
                scenes=scenes)


# ------------------------------------------------------------------ 1 · cara a cara
def fila(title, intro, cells, foot):
    """Una fila de la tabla: título y tres columnas (PSOE, PP, Vox) que entran con su frase."""
    els = [T(title, 540, 450, 120, at="L0", dur=0.4)]
    for i, ((name, color, x), (txt, st, sub, _)) in enumerate(zip(PARTIES, cells)):
        at = f"L{i + 1}"
        els += [T(name, x, 610, 74, color=color, at=at, dur=0.3),
                dict(type="underline", x0=x - 120, x1=x + 120, y=635, color=color, width=8, at="+0", dur=0.2),
                T(txt, x, 730, 46, font="body", at="+0.05", dur=0.6, line_height=1.15)]
        if st:
            els.append(stamp(st, sub, f"L{i + 1}@0.6", x=x, y=1080, w=300, h=100, size=38, rotate=-6))
    lines = [intro] + [c[3] for c in cells]
    return dict(id=title.lower(), lines=lines, footnote=foot, elements=els)


def comparativa():
    scenes = [
        dict(id="gancho", lines=["PSOE, PP y Vox: qué harían con tus impuestos, cara a cara."], tail=0.3, elements=[
            T("IMPUESTOS", 540, 470, 100, at=0, dur=0.4),
            *[e for name, color, x in PARTIES for e in coin(color, x, 760, 0.85, at="+0.02", dur=0.45)],
            T("CARA A CARA", 540, 1120, 140, at="+0.05", dur=0.45),
        ]),
        fila("IRPF", "Primero, el IRPF.", [
            ("0 € si cobras\nel salario mínimo", "APROBADO", "Congreso · 03/2026", "El PSOE ya ha quitado el IRPF a quien cobra el salario mínimo."),
            ("tramos con\nla inflación\ny el doble\npor hijo", "PROPUESTA", "decálogo PP", "El PP lo actualizaría con la inflación y duplicaría la rebaja por hijo."),
            ("0 € hasta\n22.000 €;\nluego 15 % y 25 %", "PROPUESTA", "programa Vox", "Vox: 0 euros hasta 22.000, y luego un 15 o un 25 %."),
        ], "Hacienda 17/02/2026 · decálogo PP · programa Vox, págs. 36-37"),
        fila("IVA", "Segundo, el IVA.", [
            ("10 % a los\npisos turísticos", "PENDIENTE", "RDL 29/2026", "El PSOE sube al 10 % el de los pisos turísticos."),
            ("0 % en\nalimentos\nbásicos", "PROPUESTA", "decálogo PP", "El PP lo bajaría a cero en alimentos básicos."),
            ("general:\ndel 21 % al 18 %", "PROPUESTA", "programa Vox", "Vox bajaría el general del 21 al 18 %."),
        ], "RDL 29/2026 · decálogo PP · programa Vox, pág. 37"),
        fila("¿COSTE?", "Y la gran pregunta: ¿cuánto cuesta?", [
            ("sin cifras", None, None, "El PSOE no da cifras de sus promesas."),
            ("sin cifras", None, None, "El PP, tampoco."),
            ("40.000 M€\nsolo el IRPF\n(cálculo de Vox)", "ESTIMACIÓN", "del propio partido", "Vox calcula 40.000 millones, solo en el IRPF."),
        ], "Forbes 05/10/2026 · programa de Vox, pág. 37"),
        dict(id="cierre", lines=["¿Con cuál te quedas? Comenta.", "Mañana: adónde van tus impuestos."], elements=[
            T("¿CON CUÁL\nTE QUEDAS?", 540, 520, 120, at="L0", dur=0.5, line_height=1.05),
            *[e for name, color, x in PARTIES for e in coin(color, x, 860, 0.7, at="+0.02", dur=0.35)],
            T("PRÓXIMO", 540, 1130, 66, color="gray", at="L1", dur=0.3),
            T("¿ADÓNDE VAN?", 540, 1260, 120, color="blue", at="+0.05", dur=0.4),
        ]),
    ]
    caption = ("⚖️ Impuestos: PSOE, PP y Vox, cara a cara\n💶 IRPF: 0 € con el SMI ✅ · tramos con la inflación 📝 · 0 € hasta 22.000 📝\n"
               "🛒 IVA: 10 % pisos turísticos ⏳ · 0 % alimentos básicos 📝 · general al 18 % 📝\n"
               "🔢 ¿Coste? PSOE y PP no dan cifras; Vox calcula 40.000 M€\n💬 ¿Con cuál te quedas?\n"
               "➡️ Próximo: ¿adónde van tus impuestos? · Síguenos para no perderte el siguiente\n"
               "📚 Fuentes: Hacienda 17/02, RDL 29/2026 (BOE 07/10), decálogo del PP, programa de Vox (págs. 36-37), Forbes 05/10.")
    return base("impuestos_comparativa", "Impuestos · Los tres, cara a cara", "IMPUESTOS · CARA A CARA", "ink", scenes, caption,
                "📚 Fuentes: Hacienda 17/02, RDL 29/2026 (BOE 07/10), decálogo del PP, programa de Vox (págs. 36-37), Forbes 05/10.",
                [], TT_TAGS + ["#PSOE", "#PP", "#Vox"])


# ------------------------------------------------------------------ 2 · ¿adónde van?
def adonde_van():
    scenes = [
        dict(id="gancho", lines=["De cada 100 euros que gastan las administraciones, ¿sabes cuántos van a pensiones?", "28."], tail=0.35,
             footnote="IGAE, gasto por funciones 2024: pensiones 206.130 de 725.001 M€",
             elements=[
                 T("DE CADA 100 €", 540, 460, 110, at=0, dur=0.45),
                 *coin("yellow", 540, 760, 1.3, at="+0.05", dur=0.6),
                 T("¿cuántos a pensiones?", 540, 1000, 66, font="body", color="gray", at="+0.1", dur=0.5),
                 counter(0, 28, 1210, 230, color="blue", at="L1", dur=1.0, sep=False, suffix=" €"),
             ]),
        dict(id="social", lines=["En total, 41 euros van a protección social: pensiones, paro y ayudas.", "14 van a sanidad y 9 a educación."],
             footnote="IGAE 2024: protección social 297.532 · salud 102.942 · educación 65.862 M€",
             elements=[
                 T("DE CADA 100 €", 540, 450, 90, at="L0", dur=0.4),
                 bar("social", 41, 41, 80, "blue", "41 €", "L0@0.3", bw=220, h=500),
                 bar("sanidad", 14, 41, 400, "green", "14 €", "L1@0.05", bw=220, h=500),
                 bar("educación", 9, 41, 720, "yellow", "9 €", "L1@0.45", bw=220, h=500),
             ]),
        dict(id="intereses", lines=["Y 5 euros, solo a pagar los intereses de la deuda.", "Más que defensa, vivienda y medio ambiente juntos."],
             footnote="IGAE 2024: defensa 14.233 + vivienda 7.613 + medio ambiente 15.539 M€",
             elements=[
                 *coin("red", 540, 560, 1.0, at="L0", dur=0.5),
                 stamp("INTERESES", "de la deuda · 5 €", "L0@0.5", y=770, w=520, h=140, size=60, color="red"),
                 bar("intereses", 38793, 38793, 180, "red", "38.793 M€", "L1", h=240, y=1240),
                 bar("los 3 juntos", 37385, 38793, 670, "gray", "37.385 M€", "L1@0.4", h=240, y=1240),
             ]),
        dict(id="nomina", lines=["¿Y cuánto pagas tú? Si tu empresa gasta 100 euros en tu sueldo, 41 se van en impuestos y cotizaciones.",
                                 "La media de la OCDE es 35."],
             footnote="OCDE, Taxing Wages 2026: soltero sin hijos, sueldo medio, 2025",
             elements=[
                 T("TU NÓMINA", 540, 460, 110, at="L0", dur=0.4),
                 dict(type="icon", name="document", x=540, y=680, scale=0.9, at="+0.05", dur=0.5),
                 T("por cada 100 € que cuesta tu sueldo", 540, 870, 54, font="body", color="gray", at="L0@0.3", dur=0.4),
                 T("España", 140, 990, 60, align="left", at="L0@0.6", dur=0.3),
                 T("41,4 %", 940, 990, 72, align="right", color="red", at="+0.02", dur=0.3),
                 dict(type="gauge", box=[140, 1025, 800, 100], value=41.4, max=100, color="red", at="+0.02", dur=0.9),
                 T("OCDE", 140, 1215, 60, align="left", at="L1", dur=0.3),
                 T("35,1 %", 940, 1215, 72, align="right", color="gray", at="+0.02", dur=0.3),
                 dict(type="gauge", box=[140, 1250, 800, 100], value=35.1, max=100, color="gray", at="+0.02", dur=0.9),
             ]),
        dict(id="gasolina", lines=["Y al llenar el depósito: el 39 % de lo que pagas por la gasolina son impuestos.", "En la zona euro, el 48 %."],
             footnote="Ministerio de Hacienda, 29/09/2026 (antes de la rebaja temporal de octubre)",
             elements=[
                 T("GASOLINA", 540, 460, 120, at="L0", dur=0.4),
                 T("parte del precio que son impuestos", 540, 560, 54, font="body", color="gray", at="+0.05", dur=0.4),
                 bar("España", 39, 48.1, 180, "red", "39 %", "L0@0.5", h=440),
                 bar("zona euro", 48.1, 48.1, 670, "gray", "48 %", "L1", h=440),
             ]),
        dict(id="cierre", lines=["¿Te sorprende alguno? Comenta.", "Mañana: así han cambiado tus impuestos en 20 años."], elements=[
            T("¿TE\nSORPRENDE?", 540, 560, 140, at="L0", dur=0.5, line_height=1.0),
            *coin("yellow", 540, 860, 0.8, at="+0.05", dur=0.4),
            T("PRÓXIMO", 540, 1080, 66, color="gray", at="L1", dur=0.3),
            T("ESPAÑA EN 20 AÑOS", 540, 1200, 96, color="blue", at="+0.05", dur=0.4),
        ]),
    ]
    src = ("📚 Fuentes: IGAE, gasto de las administraciones por funciones 2024; OCDE, Taxing Wages 2026; "
           "Ministerio de Hacienda 29/09/2026. Los «de cada 100 €» son cuentas nuestras con las cifras oficiales.")
    caption = ("💶 ¿Adónde van tus impuestos?\n👵 De cada 100 € de gasto público, 28 van a pensiones y 41 a protección social\n"
               "🏥 14 a sanidad · 🎓 9 a educación\n🏦 5 a intereses de la deuda: más que defensa, vivienda y medio ambiente juntos\n"
               "🧾 Nómina: 41,4 % en impuestos y cotizaciones (OCDE: 35,1 %)\n⛽ Gasolina: 39 % del precio son impuestos (zona euro: 48 %)\n"
               "💬 ¿Te sorprende alguno?\n➡️ Próximo: España en 20 años · Impuestos · Síguenos para no perderte el siguiente\n" + src)
    return base("impuestos_adonde_van", "¿Adónde van tus impuestos?", "IMPUESTOS · CURIOSIDADES", "blue", scenes, caption, src,
                [], TT_TAGS + ["#GastoPúblico", "#Pensiones"])


# ------------------------------------------------------------------ 3 · España en 20 años
def espana20_impuestos():
    scenes = [
        dict(id="gancho", lines=["En 2025, Hacienda recaudó 325.000 millones de euros.", "Récord histórico."], tail=0.35,
             footnote="AEAT, Informe anual de recaudación 2025", elements=[
                 T("RECAUDACIÓN 2025", 540, 470, 100, at=0, dur=0.45),
                 *coin("ink", 540, 740, 1.3, at="+0.05", dur=0.6),
                 counter(0, 325356, 1060, 170, at=0.3, dur=1.6, suffix=" M€"),
                 stamp("RÉCORD", "histórico", "L1", y=1250, w=420, h=140, size=66, color="red"),
             ]),
        dict(id="titulo", lines=["Así han cambiado tus impuestos en veinte años."], tail=0.3, elements=[
            T("ESPAÑA EN 20 AÑOS", 540, 480, 76, at="L0", dur=0.5),
            T("2006", 290, 720, 170, at="+0.05", dur=0.4),
            dict(type="arrow", **{"from": [440, 660], "to": [620, 660]}, width=10, curve=0.1, at="+0.05", dur=0.35),
            T("2026", 800, 720, 170, color="red", at="+0.05", dur=0.4),
            *coin("yellow", 540, 990, 1.0, at="+0.05", dur=0.6),
            T("LOS IMPUESTOS", 540, 1290, 120, at="+0.05", dur=0.45),
        ]),
        dict(id="recaudacion", lines=["En 2006 se recaudaban 179.000 millones. En 2007, 200.000.",
                                      "Llegó la crisis y en 2009 cayó a 144.000: un 17 % menos.",
                                      "Desde entonces, no ha parado de subir."],
             footnote="AEAT, informes anuales de recaudación 2006, 2007, 2009 y 2025\n(millones de euros, sin descontar inflación)", zoom=0.02,
             elements=[
                 T("RECAUDACIÓN (miles de M€)", 540, 440, 66, at="L0", dur=0.5),
                 dict(type="linechart", box=[150, 560, 800, 600], min=100000, max=350000, x_from=2006, x_to=2025,
                      color="ink", width=13, area="blue", at="L0", dur=0.5, seg_dur=0.9,
                      reveal_at=["L0@0.3", "L0@0.75", "L1@0.4", "L2@0.2"],
                      points=[dict(x=2006, value=179380, value_label="179", label_dx=50, label_dy=80),
                              dict(x=2007, value=200676, value_label="201", label_dx=60, label=""),
                              dict(x=2009, value=144023, value_label="144", label_dy=80),
                              dict(x=2025, value=325356, value_label="325", color="red", label_dx=-30)]),
                 stamp("CRISIS", "−17 %", "L1@0.75", x=560, y=1000, w=320, h=120, size=56, rotate=-8),
             ]),
        dict(id="iva", lines=["El IVA era del 16 %. En 2010 subió al 18. Y en 2012, al 21, donde sigue."],
             footnote="Ley 26/2009 · Real Decreto-ley 20/2012", elements=[
                 T("IVA GENERAL", 540, 450, 110, at="L0", dur=0.4),
                 bar("2006", 16, 21, 80, "gray", "16 %", "L0@0.2", bw=220, h=560),
                 bar("2010", 18, 21, 400, "blue", "18 %", "L0@0.45", bw=220, h=560),
                 bar("2012", 21, 21, 720, "red", "21 %", "L0@0.7", bw=220, h=560),
             ]),
        dict(id="smi", lines=["El salario mínimo era de 541 euros al mes. Hoy, 1.221.", "Y en 2026, quien lo cobra no paga IRPF."],
             footnote="RD 2002/2005 y RD 126/2026 (14 pagas) · Hacienda, 17/02/2026", elements=[
                 T("SALARIO MÍNIMO", 540, 460, 110, at="L0", dur=0.4),
                 T("2006: 541 €/mes", 540, 640, 66, font="body", color="gray", at="+0.1", dur=0.4),
                 counter(541, 1221, 880, 210, color="blue", at="L0@0.4", dur=1.4, suffix=" €"),
                 T("2026, al mes", 540, 990, 58, font="body", color="gray", at="L0@0.5", dur=0.4),
                 stamp("0 € IRPF", "si cobras el SMI", "L1@0.3", y=1220, w=520, h=150, size=70, color="green"),
             ]),
        dict(id="balanza", lines=["¿Pagamos mucho? Depende de cómo lo mires.",
                                  "En total, España recauda el 37,8 % de su PIB. La media del euro, el 40,3.",
                                  "Pero sobre el trabajo pagamos más: el 41 % del coste de un sueldo, frente al 35 de la OCDE."],
             footnote="Comisión Europea, fiscalidad 2026 (dato 2025) · OCDE, Taxing Wages 2026", elements=[
                 T("¿PAGAMOS MUCHO?", 540, 450, 100, at="L0", dur=0.4),
                 T("TODO (sobre el PIB)", 540, 570, 60, color="gray", at="L1", dur=0.3),
                 T("España", 140, 660, 58, align="left", at="L1@0.2", dur=0.3),
                 T("37,8 %", 940, 660, 68, align="right", color="blue", at="+0.02", dur=0.3),
                 dict(type="gauge", box=[140, 690, 800, 80], value=37.8, max=50, color="blue", at="+0.02", dur=0.8),
                 T("zona euro", 140, 810, 58, align="left", at="L1@0.55", dur=0.3),
                 T("40,3 %", 940, 810, 68, align="right", color="gray", at="+0.02", dur=0.3),
                 dict(type="gauge", box=[140, 840, 800, 80], value=40.3, max=50, color="gray", at="+0.02", dur=0.8),
                 T("TRABAJO (sobre un sueldo)", 540, 980, 60, color="gray", at="L2", dur=0.3),
                 T("España", 140, 1070, 58, align="left", at="L2@0.25", dur=0.3),
                 T("41,4 %", 940, 1070, 68, align="right", color="red", at="+0.02", dur=0.3),
                 dict(type="gauge", box=[140, 1100, 800, 80], value=41.4, max=50, color="red", at="+0.02", dur=0.8),
                 T("OCDE", 140, 1220, 58, align="left", at="L2@0.6", dur=0.3),
                 T("35,1 %", 940, 1220, 68, align="right", color="gray", at="+0.02", dur=0.3),
                 dict(type="gauge", box=[140, 1250, 800, 80], value=35.1, max=50, color="gray", at="+0.02", dur=0.8),
             ]),
        dict(id="futuro", lines=["¿Y si seguimos así? La Comisión Europea prevé que la presión fiscal suba al 38,4 % en 2027."],
             footnote="Comisión Europea, previsión oficial (no es cálculo nuestro)", elements=[
                 T("¿Y SI SEGUIMOS ASÍ?", 540, 460, 90, at="L0", dur=0.45),
                 T("2025", 290, 720, 130, color="gray", at="L0@0.3", dur=0.35),
                 T("37,8 %", 290, 850, 100, color="gray", at="+0.02", dur=0.35),
                 dict(type="arrow", **{"from": [440, 780], "to": [620, 740]}, width=10, curve=0.1, color="red", at="L0@0.5", dur=0.35),
                 T("2027", 800, 720, 130, at="L0@0.6", dur=0.35),
                 counter(37.8, 38.4, 860, 110, color="red", at="L0@0.65", dur=1.2, decimals=1, sep=False, suffix=" %", x=800),
                 T("presión fiscal sobre el PIB", 540, 1000, 58, font="body", color="gray", at="L0@0.7", dur=0.4),
                 stamp("PREVISIÓN", "Comisión Europea", "L0@0.85", y=1220, w=520, h=140, size=60),
             ]),
        dict(id="cierre", lines=["¿Pagas mucho o poco? Te leo.", "Síguenos: ahora toca inmigración."], elements=[
            T("¿MUCHO\nO POCO?", 540, 560, 140, at="L0", dur=0.5, line_height=1.0),
            *coin("yellow", 540, 860, 0.8, at="+0.05", dur=0.4),
            T("PRÓXIMO", 540, 1080, 66, color="gray", at="L1", dur=0.3),
            T("INMIGRACIÓN", 540, 1210, 120, color="blue", at="+0.05", dur=0.4),
        ]),
    ]
    src = ("📚 Fuentes: AEAT (recaudación 2006, 2007, 2009 y 2025), Ley 26/2009 y RDL 20/2012 (IVA), RD 2002/2005 y RD 126/2026 (SMI), "
           "Hacienda 17/02/2026, Comisión Europea (fiscalidad 2026 y previsión 2027), OCDE Taxing Wages 2026. Euros nominales.")
    caption = ("💶 Tus impuestos: 2006 → 2026\n📈 Recaudación récord: 325.356 M€ en 2025 (179.380 en 2006)\n📉 La crisis: −17 % en 2009\n"
               "🛒 IVA: del 16 % al 21 %\n🧾 SMI: de 541 a 1.221 €/mes, y desde 2026 sin IRPF\n"
               "⚖️ En total, menos que la media del euro (37,8 % vs 40,3 %); sobre el sueldo, más que la OCDE (41,4 % vs 35,1 %)\n"
               "💬 ¿Pagas mucho o poco?\n➡️ Próximo: Inmigración · Síguenos para no perderte el siguiente\n" + src)
    return base("espana20_impuestos", "España en 20 años · Los impuestos", "ESPAÑA EN 20 AÑOS · IMPUESTOS", "red", scenes, caption, src,
                [], TT_TAGS + ["#España20Años"])


if __name__ == "__main__":
    for story in (comparativa(), adonde_van(), espana20_impuestos()):
        path = os.path.join(OUT, f"{story['slug']}.json")
        json.dump(story, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(path)
