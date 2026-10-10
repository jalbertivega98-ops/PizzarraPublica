#!/usr/bin/env python3
"""Genera los storyboards de la Serie 1 · Vivienda (un episodio por partido).

Todos los episodios salen de la misma plantilla: mismas escenas, mismas posiciones
y mismos tiempos relativos. Solo cambian los textos, el color del partido y las fuentes.
Uso: python3 series/vivienda.py   → storyboards/vivienda_ep{n}_{partido}.json
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "storyboards")
CONSULTA = "Consultado el 10/10/2026."
sys.path.insert(0, os.path.join(HERE, ".."))
import wb  # noqa: E402


def fit(text, size, maxw, font="hand"):
    """Reduce el tamaño hasta que la línea más larga quepa en maxw píxeles."""
    w = max(wb.font(font, size).measureText(ln) for ln in text.split("\n"))
    return size if w <= maxw else int(size * maxw / w)


def T(text, x, y, size=72, color="ink", at="+0.05", dur=0.5, font="hand", align="center", **kw):
    return dict(type="text", text=text, x=x, y=y, size=size, color=color, at=at, dur=dur, font=font, align=align, **kw)


def L(text, tts=None):
    return {"tts": tts, "text": text} if tts else text


def stamp(text, sub, at, y=1250, w=600, h=150, size=60):
    return dict(type="stamp", text=text, sub=sub, x=540, y=y, w=w, h=h, size=size, rotate=-5, at=at, dur=0.55)


def key_lines(lines, at, y0=1010):
    """Frases clave bajo el dibujo: la primera en rotulador, el resto en letra de cuaderno."""
    els, y = [], y0
    for i, ln in enumerate(lines):
        txt, size = (ln, 66 if i == 0 else 56) if isinstance(ln, str) else ln
        fnt = "hand" if i == 0 else "body"
        size = fit(txt, size, 960, fnt)
        els.append(T(txt, 540, y, size, font=fnt, at=at if i == 0 else "+0.1", dur=0.5))
        y += size + 22
    return els


# ------------------------------------------------------------------ escenas comunes
def sc_gancho(p):
    top, big, bottom = p["hook"]
    y = 450 + 100 * top.count("\n")
    return dict(id="gancho", lines=[p["l_hook"]], tail=0.3, elements=[
        T(top, 540, 440, 92, at=0, dur=0.6, line_height=1.08),
        T(big, 540, y + 165, fit(big, 160, 900), color=p["color"], at="+0.05", dur=0.5),
        T(bottom, 540, y + 270, 80, at="+0.05", dur=0.45),
        dict(type="icon", name="house", fill=p["color"], x=540, y=y + 560, scale=1.5, at="+0.05", dur=0.8),
    ])


def sc_situacion(p):
    status, source, key = p["situ"]
    return dict(id="situacion", lines=p["l_situ"], elements=[
        dict(type="icon", name="person", tie=True, accent="light", x=270, y=600, scale=0.95, at="L0", dur=0.7),
        T(status, 270, 830, 62, at="+0.05", dur=0.4, line_height=1.05),
        dict(type="icon", name="document", x=800, y=600, scale=1.0, at="L1", dur=0.6),
        T(source, 800, 830, 50, font="body", at="+0.05", dur=0.5, line_height=1.1),
        dict(type="highlight", x0=200, x1=880, y=1130, width=72, at="L1@0.5", dur=0.35),
        T(key, 540, 1150, 74, color=p["color"], at="+0", dur=0.6),
    ])


def sc_medida(p, n, m):
    els = [
        dict(type="circle", x=150, y=480, rx=62, color=p["color"], width=9, at="L0", dur=0.35),
        T(str(n), 150, 512, 96, color=p["color"], at="+0", dur=0.2),
        T(m["title"], 240, 512, fit(m["title"], 78, 800), align="left", at="+0.05", dur=0.5),
    ]
    if m.get("big"):  # cifra grande en lugar del dibujo
        els.append(T(m["big"], 540, 810, 150, color=p["color"], at="L0@0.3", dur=0.6))
    else:
        els.append(dict(type="icon", name=m["icon"], x=540, y=760, scale=m.get("scale", 1.1), at="L0@0.3", dur=0.7,
                        **({"fill": p["color"]} if m["icon"] == "house" else {})))
    els += key_lines(m["key"], "L0@0.45")
    els.append(stamp(m["stamp"], m["sub"], "L0@0.8"))
    return dict(id=f"medida{n}", lines=[m["line"]], footnote=m["foot"], elements=els)


def sc_ojo(p):
    o = p["ojo"]
    els = [
        dict(type="highlight", x0=390, x1=690, y=500, width=90, at="L0", dur=0.3),
        T("¡OJO!", 540, 540, 140, at="+0", dur=0.35),
        dict(type="icon", name=o.get("icon", "clock"), x=540, y=770, scale=1.0, at="+0.05", dur=0.6),
    ]
    els += key_lines(o["key"], "L0@0.35")
    if o.get("stamp"):
        els.append(stamp(o["stamp"], o["sub"], "L0@0.75"))
    return dict(id="ojo", lines=[o["line"]], footnote=o["foot"], elements=els)


def sc_voto(p):
    v = p["voto"]
    si = v["vote"] == "SÍ"
    els = [
        T("2 de octubre", 540, 470, 70, at="L0", dur=0.4),
        T("decretos de vivienda del Gobierno", 540, 545, 52, font="body", color="gray", at="+0", dur=0.4),
        dict(type="icon", name="ballot_box", x=260, y=800, scale=1.0, at="L0@0.3", dur=0.6),
        T(v["vote"], 610, 880, 210, color=p["color"], at="L0@0.55", dur=0.35),
        dict(type="check" if si else "cross", x=880, y=810, r=75 if si else 65, color="ink",
             width=14, at="+0.05", dur=0.3),
    ]
    lines = [v["line"]]
    if v.get("promise"):
        lines.append(v["promise"]["line"])
        els += [
            dict(type="icon", name="bubble", x=230, y=1120, scale=0.75, at="L1", dur=0.5),
            T(v["promise"]["text"], 640, 1110, 66, at="+0.05", dur=0.5),
            stamp("PROPUESTA", v["promise"]["sub"], "L1@0.5", y=1235, w=420, h=115, size=46),
        ]
    return dict(id="voto", lines=lines, footnote=v["foot"], elements=els)


def sc_cierre(p):
    els = [
        dict(type="icon", name="calendar", x=200, y=540, scale=0.8, at="L0", dur=0.5),
        T("Programa 29N:", 360, 520, 70, align="left", at="+0.05", dur=0.4),
        T("aún sin publicar", 360, 600, 60, font="body", color="gray", align="left", at="+0.05", dur=0.4),
    ]
    nxt = p["next"]
    if nxt:
        name, color = nxt
        els += [
            T("PRÓXIMO EPISODIO", 540, 820, 74, at="L1", dur=0.45),
            dict(type="icon", name="house", fill=color, x=540, y=1060, scale=1.25, at="+0.05", dur=0.6),
            T(name, 540, 1330, 110, color=color, at="+0.05", dur=0.4),
        ]
    else:  # último episodio: las cuatro casas y la serie siguiente
        els.append(T("FIN DE LA SERIE", 540, 820, 74, at="L1", dur=0.45))
        for i, (x, c) in enumerate(zip((210, 430, 650, 870), ("psoe", "pp", "vox", "sumar"))):
            els.append(dict(type="icon", name="house", fill=c, x=x, y=1010, scale=0.7, at="+0.02", dur=0.3))
        els += [
            T("Serie 2:", 540, 1230, 64, font="body", color="gray", at="L2", dur=0.3),
            T("IMPUESTOS", 540, 1330, 110, at="+0.05", dur=0.45),
        ]
    return dict(id="cierre", lines=p["l_cierre"], elements=els)


def build(p):
    scenes = [sc_gancho(p), sc_situacion(p)]
    scenes += [sc_medida(p, i + 1, m) for i, m in enumerate(p["medidas"])]
    scenes += [sc_ojo(p), sc_voto(p), sc_cierre(p)]
    return dict(
        slug=p["slug"], title=p["title"], series_tag=f"VIVIENDA · EP. {p['ep']}/4", accent=p["color"], icon_accent={"blue": "gray", "red": "yellow"},
        handle="@pizarrapublica", voice={"engine": "edge", "voice_id": "es-ES-AlvaroNeural"},
        music_volume=0.14, scribble_volume=0.05, end_hold=0.8, line_gap=0.1,
        sources=p["sources"], caption=p["caption"], pinned_comment=p["pinned"], hashtags=p["hashtags"],
        scenes=scenes,
    )


def pinned(short):
    """Comentario fijado corto; los enlaces completos están en `sources` y en docs/series/vivienda."""
    return f"📚 Fuentes: {short}. ¿Ves un error? Dínoslo y lo corregimos."


def caption(hook, steps, nxt):
    """Formato corto (joel, 10/10/2026): gancho, 4 medidas, pregunta y siguiente episodio."""
    return f"🤯 {hook}\n" + "\n".join(steps) + f"\n💬 ¿Qué medida te afecta más?\n➡️ {nxt} · 📚 Fuentes en comentarios"


TAGS = ["#PizarraPública", "#PolíticaParaPrincipiantes", "#PolíticaEspañola", "#Vivienda", "#Elecciones29N", "#Alquiler"]
CIERRE_29N = L("Su programa para el 29 de noviembre aún no está publicado.", "Su programa para el veintinueve de noviembre aún no está publicado.")
VOTO_SRC = "Congreso, votación del 02/10/2026 (Infobae/EFE)"

# ------------------------------------------------------------------ episodios
PSOE_SRC = [
    "Ley 12/2023, de 24 de mayo, por el derecho a la vivienda. BOE 25/05/2023. https://www.boe.es/buscar/act.php?id=BOE-A-2023-12203",
    "Plan Estatal de Vivienda 2026-2030 (Real Decreto 326/2026, BOE 23/04/2026). RTVC/EFE 21/04/2026: https://rtvc.es/el-plan-estatal-de-vivienda-movilizara-7-000-millones-de-euros-21-abril-2026/",
    "Real Decreto-ley 29/2026, de 6 de octubre. BOE 07/10/2026. https://www.boe.es/buscar/doc.php?id=BOE-A-2026-20823",
    "La Moncloa, nota del 08/10/2026 sobre los decretos de vivienda: https://www.lamoncloa.gob.es/serviciosdeprensa/notasprensa/vivienda-agenda-urbana/Paginas/2026/decreto-vivienda-medidas.aspx",
    "Votación del 02/10/2026, Infobae/EFE: https://www.infobae.com/america/agencias/2026/10/02/el-congreso-rechaza-el-decreto-de-medidas-de-vivienda-con-los-votos-de-pp-vox-junts-y-upn/",
    "Entrevista a Pedro Sánchez, Qué! 09/10/2026: https://www.que.es/2026/10/09/sanchez-intervencion-vivienda-29n/",
]
PSOE = dict(
    ep=1, slug="vivienda_ep1_psoe", name="PSOE", color="psoe", next=("PP", "pp"),
    title="Vivienda · Ep. 1/4 · ¿Qué propone el PSOE?",
    hook=("¿QUÉ HA HECHO\nY QUÉ PROMETE", "EL PSOE", "CON LA VIVIENDA?"),
    l_hook=L("¿Qué ha hecho y qué promete el PSOE con la vivienda? Te lo explico en un minuto.",
             "¿Qué ha hecho y qué promete el Pesoe con la vivienda? Te lo explico en un minuto."),
    situ=("EN EL\nGOBIERNO", "con Sumar\nMinisterio de Vivienda", "aprobado + promesas"),
    l_situ=[L("El PSOE gobierna con Sumar y lleva el Ministerio de Vivienda.", "El Pesoe gobierna con Sumar y lleva el Ministerio de Vivienda."),
            "Por eso aquí hay medidas aprobadas, no solo promesas."],
    medidas=[
        dict(title="Ley de Vivienda", icon="document", key=["zonas tensionadas", "las comunidades pueden contener el alquiler"],
             stamp="APROBADO", sub="Ley 12/2023 · BOE", foot="Ley 12/2023, de 24 de mayo (BOE 25/05/2023)",
             line=L("Uno: la Ley de Vivienda de 2023. Permite a las comunidades declarar zonas tensionadas y contener allí el precio del alquiler.",
                    "Uno: la Ley de Vivienda de dos mil veintitrés. Permite a las comunidades declarar zonas tensionadas y contener allí el precio del alquiler.")),
        dict(title="Plan Estatal 2026-2030", icon="euro", scale=0.9, big="7.000 M€", key=["Estado + comunidades", "construir · rehabilitar · ayudas al alquiler"],
             stamp="APROBADO", sub="Real Decreto 326/2026 · BOE", foot="Real Decreto 326/2026 (BOE 23/04/2026)",
             line=L("Dos: el Plan Estatal de Vivienda 2026-2030. Son 7.000 millones entre el Estado y las comunidades para construir, rehabilitar y ayudar al alquiler.",
                    "Dos: el Plan Estatal de Vivienda dos mil veintiséis, dos mil treinta. Son siete mil millones entre el Estado y las comunidades para construir, rehabilitar y ayudar al alquiler.")),
        dict(title="Decreto del 6 de octubre", icon="house", scale=0.9, key=["freno a desahucios de vulnerables", "préstamos al 0 % de hasta 50.000 €"],
             stamp="PENDIENTE", sub="RDL 29/2026 · en vigor", foot="Real Decreto-ley 29/2026 (BOE 07/10/2026)",
             line=L("Tres: el decreto del 6 de octubre. Frena desahucios de personas vulnerables, limita compras de grandes propietarios y crea préstamos sin intereses de hasta 50.000 euros para la primera vivienda.",
                    "Tres: el decreto del seis de octubre. Frena desahucios de personas vulnerables, limita compras de grandes propietarios y crea préstamos sin intereses de hasta cincuenta mil euros para la primera vivienda.")),
    ],
    ojo=dict(key=["ya está en vigor…", "pero decae si el Congreso no lo convalida"], foot="Constitución, art. 86",
             line="Ojo: ese decreto ya está en vigor, pero decae si el Congreso no lo convalida."),
    voto=dict(vote="SÍ", foot="Congreso 02/10/2026 · Sánchez en Qué! 09/10/2026",
              line=L("El 2 de octubre votó sí a los decretos de vivienda.", "El dos de octubre votó sí a los decretos de vivienda."),
              promise=dict(text="alquiler indefinido", sub="09/10/2026", line="Y Sánchez promete alquileres indefinidos en su programa.")),
    l_cierre=[CIERRE_29N, L("En el próximo episodio: qué propone el PP.", "En el próximo episodio: qué propone el pepé.")],
    sources=PSOE_SRC, pinned=pinned("Ley 12/2023, RD 326/2026 y RDL 29/2026 (BOE), La Moncloa 08/10, EFE 02/10, Qué! 09/10"), hashtags=TAGS + ["#PSOE"],
    caption=caption(
        "¿Qué ha hecho el PSOE con la vivienda?",
        ["🏠 Ley de Vivienda 2023 ✅", "💶 Plan Estatal: 7.000 M€ ✅",
         "🔑 Decreto del 6/10: freno a desahucios y préstamos al 0 % ⏳", "📜 Promete alquileres indefinidos 📝"],
        "Ep. 1/4 · Próximo: PP"),
)

PP_SRC = [
    "PP, decálogo económico. idealista 28/09/2026: https://www.idealista.com/news/inmobiliario/vivienda/2026/09/28/916106-el-pp-propone-acabar-con-las-zonas-tensionadas-y-avales-de-hasta-el-100-para-la",
    "El Debate 27/09/2026: https://www.eldebate.com/economia/20260927/pp-propone-avales-publicos-100-exenciones-fiscales-jovenes-compren-vivienda_463308.html",
    "PP, «Propuestas para una revolución fiscal para menores de 40 años» (Hucha Hogar Joven): https://www.pp.es/sites/default/files/documentos/una_revolucion_fiscal_para_la_generacion_perdida_de_la_vivienda.pdf",
    "Votación del 02/10/2026, Infobae/EFE: https://www.infobae.com/america/agencias/2026/10/02/el-congreso-rechaza-el-decreto-de-medidas-de-vivienda-con-los-votos-de-pp-vox-junts-y-upn/",
]
PP = dict(
    ep=2, slug="vivienda_ep2_pp", name="PP", color="pp", next=("VOX", "vox"),
    title="Vivienda · Ep. 2/4 · ¿Qué propone el PP?",
    hook=("¿QUÉ PROPONE", "EL PP", "PARA LA VIVIENDA?"),
    l_hook=L("¿Qué propone el PP para la vivienda? Te lo explico en un minuto.", "¿Qué propone el pepé para la vivienda? Te lo explico en un minuto."),
    situ=("EN LA\nOPOSICIÓN", "decálogo 27/09/2026\nplan para jóvenes", "propuestas, no leyes"),
    l_situ=[L("El PP está en la oposición en el Congreso.", "El pepé está en la oposición en el Congreso."),
            "Sus propuestas salen de su decálogo económico de septiembre y de su plan de vivienda para jóvenes."],
    medidas=[
        dict(title="Construir", icon="house", scale=0.9, key=["1.000.000 de viviendas en 4 años", "más suelo y menos trámites"],
             stamp="PROPUESTA", sub="decálogo · 27/09/2026", foot="PP, decálogo económico (prensa, 27/09/2026)",
             line=L("Uno: construir. Dice que creará las condiciones para levantar un millón de viviendas en cuatro años, con más suelo y menos trámites.")),
        dict(title="Comprar", icon="euro", scale=0.9, big="100 %", key=["avales públicos para jóvenes", "hucha con desgravación para menores de 40"],
             stamp="PROPUESTA", sub="decálogo + plan jóvenes", foot="PP, decálogo (27/09/2026) y Hucha Hogar Joven (07/02/2025)",
             line=L("Dos: comprar. Avales públicos de hasta el cien por cien de la hipoteca para jóvenes, y una hucha para ahorrar con desgravación si tienes menos de 40 años.",
                    "Dos: comprar. Avales públicos de hasta el cien por cien de la hipoteca para jóvenes, y una hucha para ahorrar con desgravación si tienes menos de cuarenta años.")),
        dict(title="Alquiler y okupación", icon="document", key=["fin de las zonas tensionadas", "ley antiokupación"],
             stamp="PROPUESTA", sub="decálogo · 27/09/2026", foot="PP, decálogo económico (prensa, 27/09/2026)",
             line=L("Tres: alquiler y okupación. Quiere acabar con las zonas tensionadas y aprobar una ley antiokupación.",
                    "Tres: alquiler y ocupación. Quiere acabar con las zonas tensionadas y aprobar una ley anti ocupación.")),
    ],
    ojo=dict(icon="euro", key=[("21.000-26.000 € *", 76), "* ahorro en impuestos para un joven"], stamp="ESTIMACIÓN", sub="del propio partido",
             foot="Cálculo del PP (idealista, 28/09/2026)",
             line=L("Ojo: calcula que un joven se ahorraría entre 21.000 y 26.000 euros en impuestos. Es una estimación del propio partido.",
                    "Ojo: calcula que un joven se ahorraría entre veintiún mil y veintiséis mil euros en impuestos. Es una estimación del propio partido.")),
    voto=dict(vote="NO", foot=VOTO_SRC,
              line=L("El 2 de octubre votó no a los decretos de vivienda del Gobierno.", "El dos de octubre votó no a los decretos de vivienda del Gobierno.")),
    l_cierre=[CIERRE_29N, "En el próximo episodio: qué propone Vox."],
    sources=PP_SRC, pinned=pinned("decálogo económico del PP (27/09/2026), plan Hucha Hogar Joven (pp.es), EFE 02/10"), hashtags=TAGS + ["#PP"],
    caption=caption(
        "¿Qué propone el PP para la vivienda?",
        ["🏗️ Un millón de viviendas en 4 años 📝", "🔑 Avales de hasta el 100 % para jóvenes 📝",
         "🏠 Fin de las zonas tensionadas y ley antiokupación 📝", "🧾 Ahorro fiscal de 21.000-26.000 € (cálculo del PP) 🔢"],
        "Ep. 2/4 · Próximo: Vox"),
)

VOX_PDF = "https://www.voxespana.es/wp-content/uploads/2025/10/Programa-WEB-021025.pdf"
VOX_SRC = [
    f"Vox, «Programa económico y de vivienda» (en su web; la ruta del archivo indica octubre de 2025), págs. 44-47: {VOX_PDF}",
    "Las Voces del Pueblo 04/10/2026, sobre la alternativa de vivienda de Vox: https://www.lasvocesdelpueblo.com/vox-activa-su-alternativa-residencial-tras-el-derribo-de-los-decretos-de-sanchez/",
    "Votación del 02/10/2026, Infobae/EFE: https://www.infobae.com/america/agencias/2026/10/02/el-congreso-rechaza-el-decreto-de-medidas-de-vivienda-con-los-votos-de-pp-vox-junts-y-upn/",
]
VOX = dict(
    ep=3, slug="vivienda_ep3_vox", name="VOX", color="vox", next=("SUMAR", "sumar"),
    title="Vivienda · Ep. 3/4 · ¿Qué propone Vox?",
    hook=("¿QUÉ PROPONE", "VOX", "PARA LA VIVIENDA?"),
    l_hook="¿Qué propone Vox para la vivienda? Te lo explico en un minuto.",
    situ=("EN LA\nOPOSICIÓN", "programa económico\ny de vivienda", "propuestas, no leyes"),
    l_situ=["Vox está en la oposición en el Congreso.",
            "Sus propuestas salen de su programa económico y de vivienda, que tiene publicado en su web."],
    medidas=[
        dict(title="Construir", icon="house", scale=0.9, key=["más suelo y menos trámites", "«inundar España de bloques de vivienda protegida»"],
             stamp="PROPUESTA", sub="programa de Vox", foot="Vox, Programa económico y de vivienda, págs. 44-45",
             line="Uno: construir. Más suelo disponible, menos trámites y, en sus palabras, «inundar España de bloques de vivienda protegida», con colaboración pública y privada."),
        dict(title="Impuestos", icon="euro", scale=0.9, big="IVA 0", key=["en la compra de la primera vivienda", "donaciones familiares: 100 % bonificadas"],
             stamp="PROPUESTA", sub="programa de Vox", foot="Vox, Programa económico y de vivienda, págs. 46-47",
             line="Dos: impuestos. Quitar el IVA en la compra de la primera vivienda y bonificar al cien por cien las donaciones familiares para comprar casa."),
        dict(title="Quién accede", icon="person", scale=0.9, key=["arraigo en España: prioridad en vivienda protegida", "no alquilar a inmigrantes en situación irregular"],
             stamp="PROPUESTA", sub="programa de Vox", foot="Vox, Programa económico y de vivienda, pág. 46",
             line="Tres: quién accede. Quiere que el arraigo de la familia en España sea el criterio para la vivienda protegida, y prohibir alquilar a inmigrantes en situación irregular."),
    ],
    ojo=dict(icon="document", key=["derogar todas las medidas", "que intervienen el mercado del alquiler"], foot="Vox, Programa económico y de vivienda, pág. 45",
             line="Ojo: también propone derogar todas las medidas que intervienen el alquiler."),
    voto=dict(vote="NO", foot=VOTO_SRC,
              line=L("El 2 de octubre votó no a los decretos de vivienda del Gobierno.", "El dos de octubre votó no a los decretos de vivienda del Gobierno.")),
    l_cierre=[CIERRE_29N, "En el próximo episodio: qué propone Sumar."],
    sources=VOX_SRC, pinned=pinned("Programa económico y de vivienda de Vox, págs. 44-47 (voxespana.es), EFE 02/10"), hashtags=TAGS + ["#Vox"],
    caption=caption(
        "¿Qué propone Vox para la vivienda?",
        ["🏗️ Más suelo y vivienda protegida 📝", "🧾 IVA 0 en la primera vivienda 📝",
         "⚖️ Arraigo en España para acceder a vivienda protegida 📝", "🚫 Derogar las medidas que intervienen el alquiler 📝"],
        "Ep. 3/4 · Próximo: Sumar"),
)

SUMAR_SRC = [
    "Votación del 15/09/2026 sobre la ley de Sumar, idealista 16/09/2026: https://www.idealista.com/news/inmobiliario/vivienda/2026/09/16/914312-el-congreso-con-la-abstencion-del-psoe-tumba-la-ley-de-sumar-para-prohibir-que-los",
    "Real Decreto-ley 28/2026, de 6 de octubre. BOE 07/10/2026: https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-20822",
    "Real Decreto-ley 29/2026 y nota de La Moncloa 08/10/2026: https://www.lamoncloa.gob.es/serviciosdeprensa/notasprensa/vivienda-agenda-urbana/Paginas/2026/decreto-vivienda-medidas.aspx",
    "Lo que pidió Sumar en la negociación, idealista 28/09/2026: https://www.idealista.com/news/inmobiliario/vivienda/2026/09/28/916123-el-gobierno-negocia-un-nuevo-decreto-de-vivienda-con-los-precios-en-maximos",
    "Postura del PNV, moncloa.com 08/10/2026: https://www.moncloa.com/2026/10/08/decreto-vivienda-pnv-diputacion-permanente-3444289",
    "Frente Amplio, El Español 04/10/2026: https://www.elespanol.com/espana/politica/20261004/frente-amplio-nueva-marca-sumar-presentara-octubre-hoja-ruta/1003744408063_0.html",
    "Votación del 02/10/2026, Infobae/EFE: https://www.infobae.com/america/agencias/2026/10/02/el-congreso-rechaza-el-decreto-de-medidas-de-vivienda-con-los-votos-de-pp-vox-junts-y-upn/",
]
SUMAR = dict(
    ep=4, slug="vivienda_ep4_sumar", name="SUMAR", color="sumar", next=None,
    title="Vivienda · Ep. 4/4 · ¿Qué propone Sumar?",
    hook=("¿QUÉ PROPONE", "SUMAR", "PARA LA VIVIENDA?"),
    l_hook="¿Qué propone Sumar para la vivienda? Te lo explico en un minuto.",
    situ=("EN EL\nGOBIERNO", "con el PSOE\nsin el Ministerio de Vivienda", "29N: Frente Amplio"),
    l_situ=[L("Sumar gobierna con el PSOE, pero no lleva Vivienda.", "Sumar gobierna con el Pesoe, pero no lleva Vivienda."),
            L("Para el 29 de noviembre se presenta como Frente Amplio, con IU, Más Madrid y los Comuns.",
              "Para el veintinueve de noviembre se presenta como Frente Amplio, con Izquierda Unida, Más Madrid y los Comúns.")],
    medidas=[
        dict(title="Fondos y empresas", icon="house", scale=0.9, key=["prohibir que compren viviendas", "rechazada por segunda vez"],
             stamp="RECHAZADA", sub="Congreso · 15/09/2026", foot="Votación en el Congreso del 15/09/2026 (idealista)",
             line=L("Uno: prohibir que las empresas y los fondos compren viviendas. Lo llevó al Congreso y fue rechazado por segunda vez el 15 de septiembre.",
                    "Uno: prohibir que las empresas y los fondos compren viviendas. Lo llevó al Congreso y fue rechazado por segunda vez el quince de septiembre.")),
        dict(title="Renovación automática", icon="loop", scale=0.9, key=["a partir de 5 años, el contrato se renueva", "si el casero no renueva: indemnización"],
             stamp="PENDIENTE", sub="RDL 28/2026", foot="Real Decreto-ley 28/2026 (BOE 07/10/2026)",
             line="Dos: que los contratos de alquiler se renueven solos. A partir de los cinco años, el casero que no renueve tendría que indemnizar al inquilino."),
        dict(title="Congelar alquileres", icon="euro", scale=0.9, big="2 %", key=["pidió congelarlos", "entró un tope de subida hasta 2027"],
             stamp="PENDIENTE", sub="RDL 29/2026 · en vigor", foot="Real Decreto-ley 29/2026 (BOE 07/10/2026)",
             line=L("Tres: en la negociación del decreto pidió congelar los alquileres. Entró una versión parcial: subidas de como máximo un dos por ciento hasta 2027.",
                    "Tres: en la negociación del decreto pidió congelar los alquileres. Entró una versión parcial: subidas de como máximo un dos por ciento hasta dos mil veintisiete.")),
    ],
    ojo=dict(key=["solo si la convalida el Congreso", "el PNV ya ha dicho que no la apoya"], foot="idealista 06/10/2026 · moncloa.com 08/10/2026",
             line=L("Ojo: la renovación automática solo entraría en vigor si la convalida el Congreso, y el PNV ya ha dicho que no la apoya.",
                    "Ojo: la renovación automática solo entraría en vigor si la convalida el Congreso, y el pe ene uve ya ha dicho que no la apoya.")),
    voto=dict(vote="SÍ", foot=VOTO_SRC,
              line=L("El 2 de octubre votó sí a los decretos de vivienda.", "El dos de octubre votó sí a los decretos de vivienda.")),
    l_cierre=[CIERRE_29N, "Aquí acaba la serie de vivienda.", "En la próxima: impuestos."],
    sources=SUMAR_SRC, pinned=pinned("votación del Congreso 15/09, RDL 28/2026 y 29/2026 (BOE 07/10), idealista 28/09, moncloa.com 08/10, El Español 04/10, EFE 02/10"), hashtags=TAGS + ["#Sumar"],
    caption=caption(
        "¿Qué propone Sumar para la vivienda?",
        ["🚫 Prohibir que fondos y empresas compren pisos ❌", "🔁 Renovación automática del alquiler tras 5 años ⏳",
         "📈 Tope del 2 % a las subidas hasta 2027 ⏳", "🗳️ En el 29N va como Frente Amplio"],
        "Ep. 4/4 · Próxima serie: impuestos"),
)

if __name__ == "__main__":
    # con --textos DIR también reescribe DIR/<epN_partido>/<slug>_publicacion.txt sin volver a renderizar
    textos = sys.argv[sys.argv.index("--textos") + 1] if "--textos" in sys.argv else None
    for p in (PSOE, PP, VOX, SUMAR):
        story = build(p)
        path = os.path.join(OUT, f"{p['slug']}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(story, f, ensure_ascii=False, indent=1)
        print("→", os.path.relpath(path))
        if textos:
            from make_video import publicacion_text
            out = os.path.join(textos, p["slug"].replace("vivienda_", ""), f"{p['slug']}_publicacion.txt")
            with open(out, "w", encoding="utf-8") as f:
                f.write(publicacion_text(story))
            print("→", out)
