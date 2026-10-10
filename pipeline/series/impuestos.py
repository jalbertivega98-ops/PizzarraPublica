#!/usr/bin/env python3
"""Genera los storyboards de la Serie 2 · Impuestos (un episodio por partido).

Misma estructura y estética que la Serie 1 (series/vivienda.py): gancho, situación,
tres medidas, «¡ojo!», resumen en una frase y cierre. Solo cambian textos, color y fuentes.
Uso: python3 series/impuestos.py [--textos DIR]  → storyboards/impuestos_ep{n}_{partido}.json
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "storyboards")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
from vivienda import L, T, fit, sc_medida, sc_ojo, sc_situacion, stamp, key_lines, pinned  # noqa: E402


def coin(color, x, y, scale=1.0, at="+0.05", dur=0.6):
    """Moneda: círculo del color del partido con el símbolo del euro."""
    return [dict(type="circle", x=x, y=y, rx=int(120 * scale), color=color, width=int(12 * max(scale, 0.6)), at=at, dur=dur * 0.6),
            dict(type="icon", name="euro", x=x - 8 * scale, y=y, scale=scale, at="+0", dur=dur * 0.5)]


def sc_gancho(p):
    top, big, bottom = p["hook"]
    return dict(id="gancho", lines=[p["l_hook"]], tail=0.3, elements=[
        T(top, 540, 440, 92, at=0, dur=0.6),
        T(big, 540, 615, fit(big, 160, 900), color=p["color"], at="+0.05", dur=0.5),
        T(bottom, 540, 720, 80, at="+0.05", dur=0.45),
        *coin(p["color"], 540, 1010, 1.5),
    ])


def sc_resumen(p):
    r = p["resumen"]
    els = [
        T("EN UNA FRASE", 540, 500, 70, at="L0", dur=0.4),
        dict(type="icon", name="bubble", x=540, y=700, scale=0.9, at="+0.05", dur=0.5),
        T(r["big"], 540, 960, fit(r["big"], 110, 960), color=p["color"], at="L0@0.3", dur=0.6, line_height=1.05),
    ]
    els += key_lines([r["key"]], "L0@0.6", y0=1120)
    els.append(stamp("PROPUESTA", r["sub"], "L0@0.8", y=1260, w=440, h=120, size=48))
    return dict(id="resumen", lines=[r["line"]], footnote=r["foot"], elements=els)


def sc_cierre(p):
    els = [
        dict(type="icon", name="calendar", x=200, y=540, scale=0.8, at="L0", dur=0.5),
        T("Programa 29N:", 360, 520, 70, align="left", at="+0.05", dur=0.4),
        T(p["programa"], 360, 600, 60, font="body", color="gray", align="left", at="+0.05", dur=0.4),
    ]
    if p["next"]:
        name, color = p["next"]
        els += [T("PRÓXIMO EPISODIO", 540, 820, 74, at="L1", dur=0.45), *coin(color, 540, 1050, 1.15),
                T(name, 540, 1330, 110, color=color, at="+0.05", dur=0.4)]
    else:
        els.append(T("FIN DE LA SERIE", 540, 820, 74, at="L1", dur=0.45))
        for x, c in zip((210, 430, 650, 870), ("psoe", "pp", "vox", "sumar")):
            els += coin(c, x, 1010, 0.6, at="+0.02", dur=0.4)
        els += [T("Serie 3:", 540, 1230, 64, font="body", color="gray", at="L2", dur=0.3),
                T("INMIGRACIÓN", 540, 1330, 110, at="+0.05", dur=0.45)]
    return dict(id="cierre", lines=p["l_cierre"], elements=els)


def build(p):
    scenes = [sc_gancho(p), sc_situacion(p)]
    scenes += [sc_medida(p, i + 1, m) for i, m in enumerate(p["medidas"])]
    scenes += [sc_ojo(p), sc_resumen(p), sc_cierre(p)]
    return dict(
        slug=p["slug"], title=p["title"], series_tag=f"IMPUESTOS · EP. {p['ep']}/4", accent=p["color"],
        icon_accent={"blue": "gray", "red": "yellow"},
        handle="@pizarrapublica", voice={"engine": "edge", "voice_id": "es-ES-AlvaroNeural"},
        music_volume=0.14, scribble_volume=0.05, end_hold=0.8, line_gap=0.1,
        sources=p["sources"], caption=p["caption"], pinned_comment=p["pinned"], hashtags=p["hashtags"],
        scenes=scenes,
    )


def caption(hook, steps, nxt):
    return f"🤯 {hook}\n" + "\n".join(steps) + f"\n💬 ¿Qué medida te afecta más?\n➡️ {nxt} · 📚 Fuentes en comentarios"


TAGS = ["#PizarraPública", "#PolíticaParaPrincipiantes", "#PolíticaEspañola", "#Impuestos", "#Elecciones29N", "#IRPF"]

# ------------------------------------------------------------------ episodios
PSOE_SRC = [
    "Ministerio de Hacienda, nota del 17/02/2026 (deducción para que el SMI no pague IRPF): https://www.hacienda.gob.es/es-ES/Prensa/Noticias/Paginas/2026/20260217-NP-CM-SMI-DEDUCCION-2026.aspx",
    "Convalidación en el Congreso, 18/03/2026 (Forbes): https://forbes.es/economia/892542/el-congreso-avala-la-exencion-fiscal-del-smi-al-convalidar-el-decreto-de-ayudas-por-temporales/",
    "Real Decreto-ley 29/2026, de 6 de octubre. BOE 07/10/2026: https://www.boe.es/buscar/doc.php?id=BOE-A-2026-20823",
    "Resumen de sus medidas fiscales (Iberley): https://www.iberley.es/noticias/nuevas-medidas-fiscales-vivienda-rd-ley-29-2026-37071",
    "Las posiciones económicas para el 29N (Forbes, 05/10/2026): https://forbes.es/actualidad/1036705/elecciones-2026-batallas-economicas-29-n/",
]
PSOE = dict(
    ep=1, slug="impuestos_ep1_psoe", name="PSOE", color="psoe", next=("PP", "pp"), programa="aún sin publicar",
    title="Impuestos · Ep. 1/4 · ¿Qué propone el PSOE?",
    hook=("¿QUÉ HACE", "EL PSOE", "CON TUS IMPUESTOS?"),
    l_hook=L("¿Qué ha hecho y qué promete el PSOE con tus impuestos? Te lo explico en un minuto.",
             "¿Qué ha hecho y qué promete el Pesoe con tus impuestos? Te lo explico en un minuto."),
    situ=("EN EL\nGOBIERNO", "con Sumar\nMinisterio de Hacienda", "aprobado + promesas"),
    l_situ=[L("El PSOE gobierna con Sumar y lleva el Ministerio de Hacienda.", "El Pesoe gobierna con Sumar y lleva el Ministerio de Hacienda."),
            "Por eso aquí hay medidas aprobadas, no solo promesas."],
    medidas=[
        dict(title="IRPF y salario mínimo", icon="euro", big="0 €", key=["de IRPF si cobras el SMI", "17.094 € al año en 2026"],
             stamp="APROBADO", sub="Congreso · 18/03/2026", foot="Hacienda 17/02/2026 · convalidado el 18/03/2026",
             line=L("Uno: quien cobra el salario mínimo, 17.094 euros al año, no paga IRPF en 2026. El Congreso lo convalidó en marzo.",
                    "Uno: quien cobra el salario mínimo, diecisiete mil noventa y cuatro euros al año, no paga IRPF en dos mil veintiséis. El Congreso lo convalidó en marzo.")),
        dict(title="Pisos turísticos", icon="house", big="IVA 10 %", key=["alquileres de 30 noches o menos", "desde el 1 de diciembre"],
             stamp="PENDIENTE", sub="RDL 29/2026 · en vigor", foot="Real Decreto-ley 29/2026 (BOE 07/10/2026)",
             line=L("Dos: el decreto del 6 de octubre pone un IVA del 10 % a los alquileres de 30 noches o menos, como los pisos turísticos, desde el 1 de diciembre.",
                    "Dos: el decreto del seis de octubre pone un IVA del diez por ciento a los alquileres de treinta noches o menos, como los pisos turísticos, desde el uno de diciembre.")),
        dict(title="Caseros que bajan el alquiler", icon="document", big="hasta 100 %", key=["de reducción en el IRPF", "si bajan el precio del alquiler"],
             stamp="PENDIENTE", sub="RDL 29/2026 · en vigor", foot="Real Decreto-ley 29/2026 (BOE 07/10/2026)",
             line=L("Tres: el mismo decreto rebaja el IRPF a los caseros que bajen el alquiler, hasta el 100 % de lo que ganan con él.",
                    "Tres: el mismo decreto rebaja el IRPF a los caseros que bajen el alquiler, hasta el cien por cien de lo que ganan con él.")),
    ],
    ojo=dict(key=["ese decreto ya está en vigor…", "pero decae si el Congreso no lo convalida"], foot="Constitución, art. 86",
             line="Ojo: ese decreto ya está en vigor, pero decae si el Congreso no lo convalida."),
    resumen=dict(big="más progresivo", key="y más lucha contra el fraude", sub="sin cifras aún", foot="Forbes, 05/10/2026",
                 line="Para el 29 de noviembre promete impuestos más progresivos y más lucha contra el fraude, todavía sin cifras."),
    l_cierre=[L("Su programa para el 29 de noviembre aún no está publicado.", "Su programa para el veintinueve de noviembre aún no está publicado."),
              L("En el próximo episodio: qué propone el PP.", "En el próximo episodio: qué propone el pepé.")],
    sources=PSOE_SRC, pinned=pinned("Hacienda 17/02, Congreso 18/03, RDL 29/2026 (BOE 07/10), Forbes 05/10"), hashtags=TAGS + ["#PSOE"],
    caption=caption(
        "¿Qué ha hecho el PSOE con tus impuestos?",
        ["💶 0 € de IRPF si cobras el salario mínimo ✅", "🏠 IVA del 10 % a pisos turísticos desde el 1/12 ⏳",
         "🔑 Rebaja del IRPF a caseros que bajen el alquiler ⏳", "📜 Promete impuestos más progresivos, sin cifras 📝"],
        "Ep. 1/4 · Próximo: PP"),
)

PP_SRC = [
    "PP, decálogo de reformas económicas (septiembre de 2026): https://www.pp.es/actualidad/articulos/el-pp-plantea-un-decalogo-de-reformas-economicas-para-recuperar-el-poder-adquisitivo-y-modernizar-la-economia/",
    "Las posiciones económicas para el 29N (Forbes, 05/10/2026): https://forbes.es/actualidad/1036705/elecciones-2026-batallas-economicas-29-n/",
    "Feijóo propone una rebaja general de impuestos (Vozpópuli, 08/04/2026): https://www.vozpopuli.com/espana/politica/feijoo-propone-una-rebaja-general-de-impuestos-desde-el-iva-para-autonomos-hasta-el-irpf.html",
]
PP = dict(
    ep=2, slug="impuestos_ep2_pp", name="PP", color="pp", next=("VOX", "vox"), programa="aún sin publicar",
    title="Impuestos · Ep. 2/4 · ¿Qué propone el PP?",
    hook=("¿QUÉ HARÍA", "EL PP", "CON TUS IMPUESTOS?"),
    l_hook=L("¿Qué propone el PP con tus impuestos? Te lo explico en un minuto.", "¿Qué propone el pepé con tus impuestos? Te lo explico en un minuto."),
    situ=("EN LA\nOPOSICIÓN", "decálogo económico\nseptiembre de 2026", "propuestas, no leyes"),
    l_situ=[L("El PP está en la oposición en el Congreso.", "El pepé está en la oposición en el Congreso."),
            "Sus propuestas salen de su decálogo económico de septiembre."],
    medidas=[
        dict(title="IRPF", icon="document", key=["tramos actualizados con la inflación", "el doble de mínimo por cada hijo"],
             stamp="PROPUESTA", sub="decálogo · 2026", foot="PP, decálogo económico (septiembre de 2026)",
             line="Uno: el IRPF. Actualizar los tramos con la inflación, para que una subida de sueldo no te haga pagar más, y duplicar la parte de la renta que no tributa por tener hijos."),
        dict(title="IVA", icon="euro", big="IVA 0 %", key=["en alimentos básicos", "energía: del 21 % al 10 %"],
             stamp="PROPUESTA", sub="decálogo · 2026", foot="PP, decálogo económico (septiembre de 2026)",
             line=L("Dos: el IVA. Cero por ciento en alimentos básicos como carne, pescado, leche o fruta, y bajar el de la energía del 21 al 10 %.",
                    "Dos: el IVA. Cero por ciento en alimentos básicos como carne, pescado, leche o fruta, y bajar el de la energía del veintiuno al diez por ciento.")),
        dict(title="Autónomos", icon="person", scale=0.9, big="85.000 €", key=["sin IVA si facturas menos al año", "de 4 declaraciones a 1 o 2"],
             stamp="PROPUESTA", sub="decálogo · 2026", foot="PP, decálogo económico (septiembre de 2026)",
             line=L("Tres: autónomos. Que no tengan que cobrar IVA si facturan menos de 85.000 euros al año, y pasar de cuatro declaraciones a una o dos.",
                    "Tres: autónomos. Que no tengan que cobrar IVA si facturan menos de ochenta y cinco mil euros al año, y pasar de cuatro declaraciones a una o dos.")),
    ],
    ojo=dict(icon="question", key=["no dice cuánto bajaría el IRPF", "ni cuánto costaría"], foot="PP, decálogo económico (septiembre de 2026)",
             line="Ojo: el decálogo no dice cuánto bajaría el IRPF ni cuánto costarían estas rebajas."),
    resumen=dict(big="bajar impuestos", key="sobre todo IRPF e IVA", sub="decálogo · 2026", foot="PP, decálogo · Vozpópuli 08/04/2026",
                 line="En resumen: bajar impuestos, sobre todo el IRPF y el IVA."),
    l_cierre=[L("Su programa para el 29 de noviembre aún no está publicado.", "Su programa para el veintinueve de noviembre aún no está publicado."),
              "En el próximo episodio: qué propone Vox."],
    sources=PP_SRC, pinned=pinned("decálogo económico del PP (pp.es, septiembre de 2026), Forbes 05/10, Vozpópuli 08/04"), hashtags=TAGS + ["#PP"],
    caption=caption(
        "¿Qué propone el PP con tus impuestos?",
        ["📊 IRPF actualizado con la inflación y el doble de mínimo por hijo 📝", "🛒 IVA 0 % en alimentos básicos y 10 % en energía 📝",
         "🧑‍💼 Autónomos sin IVA si facturan menos de 85.000 € 📝", "❓ No dice cuánto costaría 📝"],
        "Ep. 2/4 · Próximo: Vox"),
)

VOX_PDF = "https://www.voxespana.es/wp-content/uploads/2025/10/Programa-WEB-021025.pdf"
VOX_SRC = [
    f"Vox, «Programa económico y de vivienda» (en su web; la ruta del archivo indica octubre de 2025), págs. 36-37: {VOX_PDF}",
    "Presentación del programa con Arthur Laffer (moncloa.com, 12/09/2026): https://www.moncloa.com/2026/09/12/abascal-laffer-giro-economico-vox-3430041",
    "Las posiciones económicas para el 29N (Forbes, 05/10/2026): https://forbes.es/actualidad/1036705/elecciones-2026-batallas-economicas-29-n/",
]
VOX = dict(
    ep=3, slug="impuestos_ep3_vox", name="VOX", color="vox", next=("SUMAR", "sumar"), programa="aún sin publicar",
    title="Impuestos · Ep. 3/4 · ¿Qué propone Vox?",
    hook=("¿QUÉ HARÍA", "VOX", "CON TUS IMPUESTOS?"),
    l_hook="¿Qué propone Vox con tus impuestos? Te lo explico en un minuto.",
    situ=("EN LA\nOPOSICIÓN", "programa económico\ny de vivienda", "propuestas, no leyes"),
    l_situ=["Vox está en la oposición en el Congreso.",
            "Sus propuestas salen de su programa económico, que presentó de nuevo en septiembre."],
    medidas=[
        dict(title="IRPF", icon="euro", big="15 % · 25 %", key=["0 € si ganas menos de 22.000 € al año", "y 4 puntos menos por cada hijo"],
             stamp="PROPUESTA", sub="programa de Vox", foot="Vox, Programa económico y de vivienda, págs. 36-37",
             line=L("Uno: el IRPF. Quien gane menos de 22.000 euros no pagaría. Por encima, un 15 % hasta 70.000 y un 25 % a partir de ahí, con cuatro puntos menos por cada hijo.",
                    "Uno: el IRPF. Quien gane menos de veintidós mil euros no pagaría. Por encima, un quince por ciento hasta setenta mil y un veinticinco por ciento a partir de ahí, con cuatro puntos menos por cada hijo.")),
        dict(title="IVA", icon="document", big="18 %", key=["IVA general: del 21 % al 18 %", "reducido: del 10 % al 8 %"],
             stamp="PROPUESTA", sub="programa de Vox", foot="Vox, Programa económico y de vivienda, pág. 37",
             line=L("Dos: el IVA. Volver a los tipos de antes de 2012: el general, del 21 al 18 %, y el reducido, del 10 al 8 %.",
                    "Dos: el IVA. Volver a los tipos de antes de dos mil doce: el general, del veintiuno al dieciocho por ciento, y el reducido, del diez al ocho.")),
        dict(title="Empresas y autónomos", icon="person", scale=0.9, big="15 %", key=["Sociedades: del 25 % al 15 %", "sin cuota si ganas menos del SMI"],
             stamp="PROPUESTA", sub="programa de Vox", foot="Vox, Programa económico y de vivienda, pág. 37",
             line=L("Tres: empresas y autónomos. Bajar el impuesto de sociedades del 25 al 15 %, y quitar la cuota a los autónomos que ganen menos del salario mínimo.",
                    "Tres: empresas y autónomos. Bajar el impuesto de sociedades del veinticinco al quince por ciento, y quitar la cuota a los autónomos que ganen menos del salario mínimo.")),
    ],
    ojo=dict(icon="euro", key=[("40.000 M€ *", 80), "* coste de su rebaja del IRPF"], stamp="ESTIMACIÓN", sub="del propio partido",
             foot="Vox, Programa económico y de vivienda, pág. 37",
             line=L("Ojo: el propio Vox calcula que su rebaja del IRPF costaría unos 40.000 millones de euros. Propone compensarlo recortando gasto.",
                    "Ojo: el propio Vox calcula que su rebaja del IRPF costaría unos cuarenta mil millones de euros. Propone compensarlo recortando gasto.")),
    resumen=dict(big="bajar impuestos", key="y recortar el gasto público", sub="programa de Vox", foot="Vox, programa · Forbes 05/10/2026",
                 line="En resumen: bajar casi todos los impuestos y recortar el gasto público."),
    l_cierre=[L("Su programa para el 29 de noviembre aún no está publicado.", "Su programa para el veintinueve de noviembre aún no está publicado."),
              "En el próximo episodio: qué propone Sumar."],
    sources=VOX_SRC, pinned=pinned("Programa económico y de vivienda de Vox, págs. 36-37 (voxespana.es), moncloa.com 12/09, Forbes 05/10"), hashtags=TAGS + ["#Vox"],
    caption=caption(
        "¿Qué propone Vox con tus impuestos?",
        ["💶 IRPF: 0 € hasta 22.000 €, luego 15 % y 25 % 📝", "🛒 IVA general del 21 % al 18 % 📝",
         "🏢 Sociedades al 15 % y sin cuota para autónomos bajo el SMI 📝", "🔢 Coste del IRPF: 40.000 M€ (cálculo de Vox)"],
        "Ep. 3/4 · Próximo: Sumar"),
)

SUMAR_SRC = [
    "Impuesto a las grandes herencias registrado el 22/05/2026 (idealista): https://www.idealista.com/news/finanzas/economia/2026/05/22/898769-sumar-lleva-al-congreso-un-nuevo-impuesto-a-herencias-y-donaciones-de-mas-de-un-millon",
    "IU y Movimiento Sumar registran la ley (Mundo Obrero, 23/05/2026): https://mundoobrero.es/2026/05/23/izquierda-unida-y-mov-sumar-registran-una-ley-para-crear-un-impuesto-estatal-a-las-grandes-herencias-y-donaciones/",
    "Las posiciones económicas para el 29N (Forbes, 05/10/2026): https://forbes.es/actualidad/1036705/elecciones-2026-batallas-economicas-29-n/",
    "Programa de Sumar/Frente Amplio para el 29N (Política Electoral): https://www.politicaelectoral.com/es/espana/generales-2026/nacional/sumar",
    "Presentación del Frente Amplio el 17/10 (The Objective, 04/10/2026): https://theobjective.com/espana/politica/2026-10-04/sumar-frente-amplio-octubre-posible-adelanto-electoral/",
]
SUMAR = dict(
    ep=4, slug="impuestos_ep4_sumar", name="SUMAR", color="sumar", next=None, programa="se presenta el 17/10",
    title="Impuestos · Ep. 4/4 · ¿Qué propone Sumar?",
    hook=("¿QUÉ HARÍA", "SUMAR", "CON TUS IMPUESTOS?"),
    l_hook="¿Qué propone Sumar con tus impuestos? Te lo explico en un minuto.",
    situ=("EN EL\nGOBIERNO", "con el PSOE\nsin el Ministerio de Hacienda", "29N: Frente Amplio"),
    l_situ=[L("Sumar gobierna con el PSOE, pero no lleva Hacienda.", "Sumar gobierna con el Pesoe, pero no lleva Hacienda."),
            L("Para el 29 de noviembre se presenta como Frente Amplio.", "Para el veintinueve de noviembre se presenta como Frente Amplio.")],
    medidas=[
        dict(title="Grandes herencias", icon="document", big="+1 M€", key=["impuesto estatal a herencias y donaciones", "de más de un millón de euros"],
             stamp="PROPUESTA", sub="Congreso · 22/05/2026", foot="Proposición de ley registrada el 22/05/2026 (idealista)",
             line=L("Uno: un impuesto estatal a las herencias y donaciones de más de un millón de euros. Lo registró en el Congreso en mayo, con Izquierda Unida.",
                    "Uno: un impuesto estatal a las herencias y donaciones de más de un millón de euros. Lo registró en el Congreso en mayo, con Izquierda Unida.")),
        dict(title="Autónomos", icon="person", scale=0.9, big="85.000 €", key=["sin IVA si facturas menos al año", "en esto coincide con el PP"],
             stamp="PROPUESTA", sub="Forbes · 05/10/2026", foot="Forbes, 05/10/2026",
             line=L("Dos: autónomos. Que quien facture menos de 85.000 euros al año no tenga que cobrar IVA. En esto coincide con el PP.",
                    "Dos: autónomos. Que quien facture menos de ochenta y cinco mil euros al año no tenga que cobrar IVA. En esto coincide con el pepé.")),
        dict(title="Fortunas y banca", icon="euro", key=["más impuestos a las grandes fortunas", "y a la banca"],
             stamp="PROPUESTA", sub="sin cifras aún", foot="Forbes 05/10/2026 · Política Electoral",
             line="Tres: que paguen más las grandes fortunas y la banca. Es uno de sus pilares, aunque aún sin cifras."),
    ],
    ojo=dict(icon="calendar", key=["el programa del Frente Amplio", "se presenta el 17 de octubre"], foot="The Objective, 04/10/2026",
             line=L("Ojo: el programa del Frente Amplio se presenta el 17 de octubre, así que estas medidas pueden cambiar.",
                    "Ojo: el programa del Frente Amplio se presenta el diecisiete de octubre, así que estas medidas pueden cambiar.")),
    resumen=dict(big="más a quien más tiene", key="herencias, fortunas y banca", sub="sin cifras aún", foot="Forbes, 05/10/2026",
                 line="En resumen: que paguen más quienes más tienen."),
    l_cierre=[L("Su programa para el 29 de noviembre se presenta el 17 de octubre.", "Su programa para el veintinueve de noviembre se presenta el diecisiete de octubre."),
              "Aquí acaba la serie de impuestos.", "En la próxima: inmigración."],
    sources=SUMAR_SRC, pinned=pinned("proposición de ley del 22/05 (idealista, Mundo Obrero), Forbes 05/10, The Objective 04/10"), hashtags=TAGS + ["#Sumar"],
    caption=caption(
        "¿Qué propone Sumar con tus impuestos?",
        ["🏛️ Impuesto a herencias de más de 1 millón 📝", "🧑‍💼 Autónomos sin IVA si facturan menos de 85.000 € 📝",
         "🏦 Más impuestos a grandes fortunas y banca, sin cifras 📝", "🗳️ En el 29N va como Frente Amplio"],
        "Ep. 4/4 · Próxima serie: inmigración"),
)

if __name__ == "__main__":
    textos = sys.argv[sys.argv.index("--textos") + 1] if "--textos" in sys.argv else None
    for p in (PSOE, PP, VOX, SUMAR):
        story = build(p)
        path = os.path.join(OUT, f"{p['slug']}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(story, f, ensure_ascii=False, indent=1)
        print("→", os.path.relpath(path))
        if textos:
            from make_video import publicacion_text
            out = os.path.join(textos, p["slug"].replace("impuestos_", ""), f"{p['slug']}_publicacion.txt")
            os.makedirs(os.path.dirname(out), exist_ok=True)
            with open(out, "w", encoding="utf-8") as f:
                f.write(publicacion_text(story))
            print("→", out)
