#!/usr/bin/env python3
"""Genera los storyboards de la Serie 3 · Inmigración (un episodio por partido).

Misma estructura y estética que Vivienda e Impuestos: gancho, situación, tres medidas,
«¡ojo!», resumen en una frase y cierre. El símbolo de la serie es un documento (los papeles)
dentro de un círculo del color del partido.
Uso: python3 series/inmigracion.py [--textos DIR]  → storyboards/inmigracion_ep{n}_{partido}.json
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "storyboards")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
from vivienda import T, fit, sc_medida, sc_ojo, sc_situacion, stamp, key_lines, pinned  # noqa: E402


def badge(color, x, y, scale=1.0, at="+0.05", dur=0.6):
    """Papeles: círculo del color del partido con un documento dentro."""
    return [dict(type="circle", x=x, y=y, rx=int(120 * scale), color=color, width=int(12 * max(scale, 0.6)), at=at, dur=dur * 0.6),
            dict(type="icon", name="document", x=x, y=y, scale=0.85 * scale, at="+0", dur=dur * 0.5)]


def sc_gancho(p):
    top, big, bottom = p["hook"]
    return dict(id="gancho", lines=[p["l_hook"]], tail=0.3, elements=[
        T(top, 540, 440, 92, at=0, dur=0.6),
        T(big, 540, 615, fit(big, 160, 900), color=p["color"], at="+0.05", dur=0.5),
        T(bottom, 540, 720, fit(bottom, 80, 960), at="+0.05", dur=0.45),
        *badge(p["color"], 540, 1010, 1.5),
    ])


def sc_resumen(p):
    r = p["resumen"]
    els = [
        T("EN UNA FRASE", 540, 500, 70, at="L0", dur=0.4),
        dict(type="icon", name="bubble", x=540, y=700, scale=0.9, at="+0.05", dur=0.5),
        T(r["big"], 540, 960, fit(r["big"], 110, 960), color=p["color"], at="L0@0.3", dur=0.6, line_height=1.05),
    ]
    els += key_lines([r["key"]], "L0@0.6", y0=1120)
    els.append(stamp(r.get("stamp", "PROPUESTA"), r["sub"], "L0@0.8", y=1260, w=440, h=120, size=48))
    return dict(id="resumen", lines=[r["line"]], footnote=r["foot"], elements=els)


def sc_cierre(p):
    els = [
        dict(type="icon", name="calendar", x=200, y=540, scale=0.8, at="L0", dur=0.5),
        T("Programa 29N:", 360, 520, 70, align="left", at="+0.05", dur=0.4),
        T(p["programa"], 360, 600, 60, font="body", color="gray", align="left", at="+0.05", dur=0.4),
    ]
    if p["next"]:
        name, color = p["next"]
        els += [T("PRÓXIMO EPISODIO", 540, 820, 74, at="L1", dur=0.45), *badge(color, 540, 1050, 1.15),
                T(name, 540, 1330, 110, color=color, at="+0.05", dur=0.4)]
    else:
        els.append(T("FIN DE LA SERIE", 540, 820, 74, at="L1", dur=0.45))
        for x, c in zip((210, 430, 650, 870), ("psoe", "pp", "vox", "sumar")):
            els += badge(c, x, 1010, 0.6, at="+0.02", dur=0.4)
        els += [T("Serie 4:", 540, 1230, 64, font="body", color="gray", at="L2", dur=0.3),
                T("EMPLEO Y SALARIOS", 540, 1330, fit("EMPLEO Y SALARIOS", 110, 960), at="+0.05", dur=0.45)]
    return dict(id="cierre", lines=p["l_cierre"], elements=els)


def build(p):
    scenes = [sc_gancho(p), sc_situacion(p)]
    scenes += [sc_medida(p, i + 1, m) for i, m in enumerate(p["medidas"])]
    scenes += [sc_ojo(p), sc_resumen(p), sc_cierre(p)]
    return dict(
        slug=p["slug"], title=p["title"], series_tag=f"INMIGRACIÓN · EP. {p['ep']}/4", accent=p["color"],
        icon_accent={"blue": "gray", "red": "yellow"},
        handle="@pizarrapublica", voice={"engine": "edge", "voice_id": "es-ES-AlvaroNeural"},
        music_volume=0.14, scribble_volume=0.05, end_hold=0.8, line_gap=0.1,
        sources=p["sources"], caption=p["caption"], pinned_comment=p["pinned"], hashtags=p["hashtags"],
        scenes=scenes,
    )


def caption(hook, steps, question, nxt):
    return f"🤯 {hook}\n" + "\n".join(steps) + f"\n💬 {question}\n➡️ {nxt} · 📚 Fuentes en comentarios"


TAGS = ["#PizarraPública", "#PolíticaParaPrincipiantes", "#PolíticaEspañola", "#Inmigración", "#Elecciones29N", "#Regularización"]
RD316 = "Real Decreto 316/2026, de 14 de abril (BOE-A-2026-8284), resumen de Noticias Obreras (15/04/2026): https://noticiasobreras.es/2026/04/el-boe-publica-el-real-decreto-que-articula-la-regularizacion-extraordinaria-de-personas-migrantes-aprobada-por-el-gobierno/"

# ------------------------------------------------------------------ episodios
PSOE = dict(
    ep=1, slug="inmigracion_ep1_psoe", name="PSOE", color="psoe", next=("PP", "pp"), programa="aún sin publicar",
    title="Inmigración · Ep. 1/4 · ¿Qué ha hecho el PSOE?",
    hook=("¿QUÉ HACE", "EL PSOE", "CON LA INMIGRACIÓN?"),
    l_hook="¿Qué ha hecho y qué promete el PSOE con la inmigración? Te lo explico en un minuto.",
    situ=("EN EL\nGOBIERNO", "con Sumar\nMinisterio de Migraciones", "aprobado + promesas"),
    l_situ=["El PSOE gobierna con Sumar y lleva el Ministerio de Migraciones.",
            "Por eso aquí hay medidas aprobadas, no solo promesas."],
    medidas=[
        dict(title="Regularización extraordinaria", icon="document", big="1 año", key=["de papeles si llegaste antes de 2026", "5 meses aquí y sin antecedentes"],
             stamp="APROBADO", sub="RD 316/2026 · 14/04/2026", foot="Real Decreto 316/2026 (BOE 15/04/2026)",
             line="Uno: la regularización extraordinaria. Papeles por un año para quien llegó antes de 2026 y no tiene antecedentes. Se aprobó en abril, pactada con Podemos."),
        dict(title="Menores que llegan solos", icon="person", scale=0.9, key=["reparto obligatorio entre comunidades", "11 comunidades lo recurren"],
             stamp="APROBADO", sub="Congreso · abril de 2025", foot="Vozpópuli, 26/08/2025",
             line="Dos: los menores que llegan solos. Si Canarias, Ceuta o Melilla se saturan, las demás comunidades tienen que acogerlos. Once lo han recurrido."),
        dict(title="Arraigo", icon="calendar", big="2 años", key=["en España para pedir papeles", "antes eran 3"],
             stamp="APROBADO", sub="RD 1155/2024 · en vigor", foot="Reglamento de extranjería, en vigor desde el 20/05/2025",
             line="Tres: el nuevo reglamento de extranjería, en vigor desde mayo de 2025. Para pedir papeles por arraigo bastan dos años en España, en lugar de tres."),
    ],
    ojo=dict(icon="document", key=[("1.174.978 solicitudes", 80), "el Gobierno calculaba unas 500.000"], foot="Ministerio de Inclusión, balance del 30/06/2026",
             line="Ojo: el Gobierno esperaba unas 500.000 personas y llegaron más de un millón de solicitudes. Pedirlo no es lo mismo que conseguirlo."),
    resumen=dict(big="regularizar", key="a quien ya vive y trabaja aquí", stamp="APROBADO", sub="2025-2026", foot="RD 316/2026 · RD 1155/2024",
                 line="En resumen: regularizar a quien ya vive y trabaja aquí."),
    l_cierre=["Su programa para el 29 de noviembre aún no está publicado.", "En el próximo episodio: qué propone el PP."],
    sources=[
        RD316,
        "Requisitos (llegada antes del 31/12/2025, 5 meses, sin antecedentes, permiso de 1 año), Accem: https://www.accem.es/blog/regularizacion-2026-informacion-practica-para-personas-migrantes-en-espana",
        "Pacto PSOE-Podemos y estimación de 500.000 (Rolling Stone, 27/01/2026): https://es.rollingstone.com/que-sabemos-sobre-la-nueva-regularizacion-masiva-de-inmigrantes-que-residen-en-espana/",
        "Balance: 1.174.978 solicitudes del 16/04 al 30/06/2026, Ministerio de Inclusión (Nuevatribuna, 05/07/2026): https://www.nuevatribuna.es/articulo/actualidad/plazo-presentacion-solicitud-regularizacion-extraordinaria-concluye-1174-978-solicitudes-recibidas/20260705120449252072.html",
        "Reparto de menores y recursos de 11 comunidades (Vozpópuli, 26/08/2025): https://www.vozpopuli.com/espana/politica/el-gobierno-activa-el-reparto-de-menores-inmigrantes-con-11-comunidades-recurriendo-la-norma-ante-el-constitucional.html",
        "Reglamento de extranjería, RD 1155/2024 (Iberley): https://www.iberley.es/noticias/publicado-nuevo-reglamento-extranjeria-34156",
    ],
    pinned=pinned("RD 316/2026 (BOE 15/04), Ministerio de Inclusión 05/07, RD 1155/2024, Vozpópuli 26/08/2025"), hashtags=TAGS + ["#PSOE"],
    caption=caption(
        "¿Qué ha hecho el PSOE con la inmigración?",
        ["🪪 Regularización extraordinaria: papeles para 1 año ✅", "🧒 Reparto obligatorio de menores que llegan solos ✅",
         "⏳ Arraigo: de 3 a 2 años en España ✅", "📈 1,17 millones de solicitudes; se esperaban 500.000"],
        "¿Qué opinas de la regularización?", "Ep. 1/4 · Próximo: PP"),
)

PP = dict(
    ep=2, slug="inmigracion_ep2_pp", name="PP", color="pp", next=("VOX", "vox"), programa="aún sin publicar",
    title="Inmigración · Ep. 2/4 · ¿Qué propone el PP?",
    hook=("¿QUÉ HARÍA", "EL PP", "CON LA INMIGRACIÓN?"),
    l_hook="¿Qué propone el PP con la inmigración? Te lo explico en un minuto.",
    situ=("EN LA\nOPOSICIÓN", "plan de inmigración\noctubre de 2025", "propuestas, no leyes"),
    l_situ=["El PP está en la oposición en el Congreso.",
            "Sus propuestas salen de su plan de inmigración, que presentó en octubre de 2025."],
    medidas=[
        dict(title="Entrar por trabajo", icon="person", scale=0.9, key=["visado por puntos", "cupos por países y sectores"],
             stamp="PROPUESTA", sub="plan del PP · 2025", foot="PP, Plan Nacional de Inmigración (14/10/2025)",
             line="Uno: entrar por trabajo. Un visado por puntos y cupos por países y sectores, con más plazas para los países que colaboren en controlar la salida."),
        dict(title="Delitos", icon="document", key=["perder la residencia", "si cometes un delito grave"],
             stamp="PROPUESTA", sub="plan del PP · 2025", foot="PP, Plan Nacional de Inmigración (14/10/2025)",
             line="Dos: delitos. Que un extranjero pierda automáticamente la residencia si comete un delito grave."),
        dict(title="Arraigo y nacionalidad", icon="document", key=["arraigo solo como excepción", "nacionalidad: más idioma y Constitución"],
             stamp="PROPUESTA", sub="plan del PP · 2025", foot="PP, Plan Nacional de Inmigración (14/10/2025)",
             line="Tres: papeles y nacionalidad. Que el arraigo vuelva a ser una excepción y que la nacionalidad pida más idioma, cultura y Constitución."),
    ],
    ojo=dict(icon="question", key=["no dice cuántas personas", "entrarían con esos cupos"], foot="PP, Plan Nacional de Inmigración (14/10/2025)",
             line="Ojo: el plan no dice cuántas personas entrarían con esos cupos."),
    resumen=dict(big="inmigración legal", key="ligada al empleo y más control", sub="plan del PP · 2025", foot="pp.es, 14/10/2025",
                 line="En resumen: inmigración legal ligada al empleo y más control."),
    l_cierre=["Su programa para el 29 de noviembre aún no está publicado.", "En el próximo episodio: qué propone Vox."],
    sources=[
        "PP, Plan Nacional de Inmigración presentado por Feijóo en Barcelona (pp.es, 14/10/2025): https://www.pp.es/actualidad/articulos/feijoo-propone-reforzar-los-requisitos-para-que-un-inmigrante-adquiera-la-nacionalidad-la-nacionalidad-espanola-no-se-regala-se-merece/",
        "Moción del PP contra la regularización, aprobada con PP, Vox, Junts y UPN (pp.es, 18/03/2026): https://www.pp.es/actualidad/articulos/la-mayoria-del-congreso-aprueba-una-propuesta-del-pp-que-rechaza-la-regularizacion-masiva-de-inmigrantes-del-gobierno/",
        "Programas del 29N aún sin publicar (Politicheck, 08/10/2026): https://politicheck.es/29n-programas",
    ],
    pinned=pinned("Plan Nacional de Inmigración del PP (pp.es, 14/10/2025), moción del PP en el Congreso (18/03/2026)"), hashtags=TAGS + ["#PP"],
    caption=caption(
        "¿Qué propone el PP con la inmigración?",
        ["💼 Visado por puntos y cupos por países y sectores 📝", "⚖️ Perder la residencia por delitos graves 📝",
         "🪪 Arraigo como excepción y nacionalidad más exigente 📝", "❓ No dice cuántas personas entrarían 📝"],
        "¿Qué opinas del visado por puntos?", "Ep. 2/4 · Próximo: Vox"),
)

VOX = dict(
    ep=3, slug="inmigracion_ep3_vox", name="VOX", color="vox", next=("SUMAR", "sumar"), programa="aún sin publicar",
    title="Inmigración · Ep. 3/4 · ¿Qué propone Vox?",
    hook=("¿QUÉ HARÍA", "VOX", "CON LA INMIGRACIÓN?"),
    l_hook="¿Qué propone Vox con la inmigración? Te lo explico en un minuto.",
    situ=("EN LA\nOPOSICIÓN", "iniciativas en el\nCongreso · 2026", "propuestas, no leyes"),
    l_situ=["Vox está en la oposición en el Congreso.",
            "Sus propuestas salen de las iniciativas que ha llevado al Congreso este año."],
    medidas=[
        dict(title="Expulsiones", icon="document", key=["repatriar a quien entre de forma irregular", "deportar por delitos graves o reincidencia"],
             stamp="PROPUESTA", sub="moción · febrero de 2026", foot="Moción de Vox en el Congreso (febrero de 2026)",
             line="Uno: expulsiones. Repatriar a quien entre de forma irregular y deportar a los extranjeros, con papeles o sin ellos, que cometan delitos graves o reincidan."),
        dict(title="«Prioridad nacional»", icon="house", big="10 años", key=["empadronado para comprar vivienda protegida", "ya en pactos PP-Vox en Extremadura y Aragón"],
             stamp="PROPUESTA", sub="Congreso · 05/05/2026", foot="The Objective, 06/05/2026",
             line="Dos: lo que Vox llama «prioridad nacional» en las ayudas. Por ejemplo, para comprar vivienda protegida, diez años empadronado en España, y cinco para alquilarla."),
        dict(title="Arraigo y nacionalidades", icon="document", key=["eliminar el arraigo como vía", "revisar las nacionalidades concedidas"],
             stamp="PROPUESTA", sub="moción · febrero de 2026", foot="Moción de Vox en el Congreso (febrero de 2026)",
             line="Tres: papeles. Eliminar el arraigo como vía para regularizarse y revisar las nacionalidades concedidas en los últimos años."),
    ],
    ojo=dict(icon="question", key=["recurrió la regularización", "el Supremo no la frenó en mayo"], foot="Tribunal Supremo, 22/05/2026",
             line="Ojo: Vox recurrió la regularización ante el Supremo, que en mayo rechazó frenarla mientras decide."),
    resumen=dict(big="menos inmigración", key="y preferencia para los españoles", sub="iniciativas · 2026", foot="Moción de feb. 2026 · PNL del 05/05/2026",
                 line="En resumen: menos inmigración y preferencia para los españoles."),
    l_cierre=["Su programa para el 29 de noviembre aún no está publicado.", "En el próximo episodio: qué propone Sumar."],
    sources=[
        "Moción de Vox sobre deportaciones, repatriación, arraigo y nacionalidades (El Diario de Madrid, 22/02/2026): https://www.eldiariodemadrid.es/articulo/politica/vox-mocion-congreso-deportaciones-inmigrantes-repatriaciones-politica-migratoria-espana/20260222170439122058.html",
        "Proposición no de ley de «prioridad nacional», 10 y 5 años de empadronamiento (The Objective, 06/05/2026): https://theobjective.com/espana/politica/2026-05-06/vox-prioridad-nacional-inmigrantes-empadronamiento/",
        "El Supremo no suspende la regularización recurrida por Vox y la Comunidad de Madrid (La Voz de Lanzarote, 23/05/2026): https://www.lavozdelanzarote.com/en/news/politics/spain-applauds-that-the-supreme-court-does-not-stop-the-regularization-clears-the-present-of-thousands-of-people_243581_102.html",
        "Vox arranca la campaña con inmigración (moncloa.com, 05/10/2026): https://www.moncloa.com/2026/10/05/elecciones-generales-29n-vox-campana-3443022/",
    ],
    pinned=pinned("moción de Vox (febrero de 2026), PNL de «prioridad nacional» (05/05/2026), auto del Supremo (22/05/2026)"), hashtags=TAGS + ["#Vox"],
    caption=caption(
        "¿Qué propone Vox con la inmigración?",
        ["✈️ Repatriar a irregulares y deportar por delitos graves 📝", "🏠 «Prioridad nacional»: 10 años empadronado para comprar vivienda protegida 📝",
         "🪪 Eliminar el arraigo y revisar nacionalidades 📝", "⚖️ Recurrió la regularización; el Supremo no la frenó"],
        "¿Qué opinas de la «prioridad nacional»?", "Ep. 3/4 · Próximo: Sumar"),
)

SUMAR = dict(
    ep=4, slug="inmigracion_ep4_sumar", name="SUMAR", color="sumar", next=None, programa="se presenta el 17/10",
    title="Inmigración · Ep. 4/4 · ¿Qué propone Sumar?",
    hook=("¿QUÉ HARÍA", "SUMAR", "CON LA INMIGRACIÓN?"),
    l_hook="¿Qué propone Sumar con la inmigración? Te lo explico en un minuto.",
    situ=("EN EL\nGOBIERNO", "con el PSOE\nsin Migraciones", "29N: Frente Amplio"),
    l_situ=["Sumar gobierna con el PSOE, pero no lleva Migraciones.",
            "Para el 29 de noviembre se presenta como Frente Amplio."],
    medidas=[
        dict(title="Regularización", icon="document", key=["la pedía desde 2025", "aprobada en el Gobierno con el PSOE"],
             stamp="APROBADO", sub="RD 316/2026 · con el PSOE", foot="Real Decreto 316/2026 (BOE 15/04/2026)",
             line="Uno: la regularización. Sumar la pedía desde 2025 y la aprobó en el Consejo de Ministros con el PSOE."),
        dict(title="«Regularización permanente»", icon="document", key=["una vía estable para tener papeles", "cambiando la Ley de Extranjería"],
             stamp="PROPUESTA", sub="programa de 2023", foot="Programa de Sumar 2023, pág. 104",
             line="Dos: una «regularización permanente». Cambiar la Ley de Extranjería para que haya una vía estable de conseguir papeles, sin esperar a procesos extraordinarios."),
        dict(title="Cerrar los CIE", icon="document", big="CIE", key=["centros de internamiento de extranjeros", "retienen a personas pendientes de expulsión"],
             stamp="PROPUESTA", sub="programa de 2023", foot="Programa de Sumar 2023",
             line="Tres: cerrar los centros de internamiento de extranjeros, los CIE, donde se retiene a personas pendientes de expulsión."),
    ],
    ojo=dict(icon="calendar", key=["las medidas 2 y 3 son de 2023", "el Frente Amplio presenta programa el 17/10"], foot="Politicheck, 08/10/2026",
             line="Ojo: las medidas dos y tres son de su programa de 2023. El del Frente Amplio se presenta el 17 de octubre."),
    resumen=dict(big="más vías para tener papeles", key="y más derechos", sub="programa de 2023", foot="Programa de Sumar 2023 · RD 316/2026",
                 line="En resumen: más vías para tener papeles y más derechos."),
    l_cierre=["Su programa para el 29 de noviembre se presenta el 17 de octubre.",
              "Aquí acaba la serie de inmigración.", "En la próxima: empleo y salarios."],
    sources=[
        "Sumar pide acelerar la regularización (elDiario.es, 2025): https://www.eldiario.es/politica/sumar-quiere-acelerar-regularizacion-extraordinaria-enfrentar-relato-extrema-derecha-inmigracion_1_12654878.html",
        RD316,
        "Programa de Sumar para el 23J de 2023, pág. 104, regularización permanente y cierre de los CIE (resumen de Politicheck, 08/10/2026): https://politicheck.es/29n-programas",
        "Posiciones de Sumar/Frente Amplio para el 29N (Política Electoral): https://www.politicaelectoral.com/es/espana/generales-2026/nacional/sumar",
    ],
    pinned=pinned("elDiario.es 2025, RD 316/2026 (BOE 15/04), programa de Sumar 2023 (pág. 104)"), hashtags=TAGS + ["#Sumar"],
    caption=caption(
        "¿Qué propone Sumar con la inmigración?",
        ["🪪 Regularización extraordinaria, aprobada con el PSOE ✅", "📜 Una vía permanente para tener papeles 📝",
         "🚪 Cerrar los centros de internamiento (CIE) 📝", "🗳️ En el 29N va como Frente Amplio"],
        "¿Qué opinas de la regularización permanente?", "Ep. 4/4 · Próxima serie: empleo y salarios"),
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
            out = os.path.join(textos, p["slug"].replace("inmigracion_", ""), f"{p['slug']}_publicacion.txt")
            os.makedirs(os.path.dirname(out), exist_ok=True)
            with open(out, "w", encoding="utf-8") as f:
                f.write(publicacion_text(story))
            print("→", out)
