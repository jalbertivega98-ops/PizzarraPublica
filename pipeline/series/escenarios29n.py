#!/usr/bin/env python3
"""29N · ¿Qué tiene que pasar para que gobierne…? Un episodio por partido (PSOE, PP, Vox).

Estilo pizarra con rotulador (motor v1), misma estructura para los tres:
gancho + síguenos, la regla de los 176, dónde está hoy, su camino a 176, qué tendría que pasar,
el precedente de 2023, qué promete para los próximos años, pregunta + síguenos.
Uso: python3 series/escenarios29n.py  → storyboards/escenarios29n_ep{n}_{partido}.json

Encuestas de octubre de 2026 (escaños; punto medio si dan horquilla):
  GESOP/El Periódico 6-8/10: PP 123, PSOE 110, Vox 70 · Sigma Dos/El Mundo 11/10: 135, 103, 68
  40dB/El País 7-8/10: 132, 112, 66 · SocioMétrica/El Español 1-3/10: 143, 106, 62
  Imop/El Confidencial 5-7/10: 130, 110, 70 · DYM 8/10: 141, 109, 63
  Media: PP 134, PSOE 108, Vox 66-67; PP+Vox ≈ 200 (todas por encima de 176).
  Voto: PP ≈ 32,8 %, Vox ≈ 18,7 % (media de las que publican %), diferencia ≈ 14 puntos.
  Imop: PSOE y los partidos que apoyaron a Sánchez en 2023 suman 148.
2023: PP 137, PSOE 121, Vox 33. Investidura de Feijóo (27/09/2023): 172 sí, 178 no.
  Investidura de Sánchez (16/11/2023): 179 sí. Vox dejó 5 gobiernos autonómicos con el PP el 11/07/2024.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "storyboards")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
from vivienda import L, T, fit, stamp, key_lines  # noqa: E402

VOZ = {"engine": "elevenlabs", "voice_id": "Iohr8NC0THLcVZXLaHlP"}  # «Pizarra Pública» (ElevenLabs, voz propia)
ENCUESTAS = "Media de 6 encuestas (1-11 oct. 2026)"


def sc_gancho(p):
    top, big, bottom = p["hook"]
    return dict(id="gancho", lines=[p["l_hook"], L("Síguenos para entender el 29 de noviembre sin líos.",
                                                    "Síguenos para entender el veintinueve ene sin líos.")], tail=0.2, elements=[
        T(top, 540, 450, fit(top, 92, 960), at=0, dur=0.6),
        T(big, 540, 640, fit(big, 170, 900), color=p["color"], at="+0.05", dur=0.5),
        T(bottom, 540, 760, fit(bottom, 80, 960), at="+0.05", dur=0.45),
        dict(type="icon", name="ballot_box", x=540, y=1010, scale=1.2, at="+0.05", dur=0.7),
        stamp("SÍGUENOS", "@pizarrapublica", "L1", y=1260, w=520, h=140, size=64),
    ])


def sc_regla(p):
    return dict(id="regla", lines=[L("La regla: para gobernar hacen falta 176 diputados de 350. Da igual quién quede primero.",
                                     "La regla: para gobernar hacen falta ciento setenta y seis diputados de trescientos cincuenta. Da igual quién quede primero.")],
                footnote="Constitución, art. 99", elements=[
        dict(type="hemicycle", x=540, y=930, r_in=150, r_out=380, rows=9, dot=10, count=350, highlight=176, hl_color=p["color"],
             at="L0", dur=1.6),
        dict(type="counter", **{"from": 0}, to=176, x=540, y=900, size=130, color=p["color"], at="L0@0.25", dur=1.2),
        T("de 350", 540, 990, 60, font="body", color="gray", at="+0.05", dur=0.3),
        dict(type="highlight", x0=200, x1=880, y=1150, width=72, at="L0@0.7", dur=0.35),
        T("ganar ≠ gobernar", 540, 1170, 80, at="+0", dur=0.5),
    ])


def sc_hoy(p):
    h = p["hoy"]
    return dict(id="hoy", lines=[h["line"]], footnote=ENCUESTAS, elements=[
        T("¿DÓNDE ESTÁ HOY?", 540, 470, 82, at="L0", dur=0.5),
        dict(type="bars", x=300, y=1180, h=520, bar_w=170, gap=130, max=145,
             bars=[{"label": "2023", "value": h["antes"], "color": "gray"},
                   {"label": "ENCUESTAS", "value": h["hoy"], "color": p["color"]}], at="L0@0.2", dur=1.4),
        T(h["key"], 540, 1290, fit(h["key"], 60, 960), font="body", at="L0@0.75", dur=0.5),
    ])


def sc_camino(p):
    c = p["camino"]
    return dict(id="camino", lines=[c["line"]], footnote=c["foot"], elements=[
        T(c["title"], 540, 470, fit(c["title"], 80, 960), at="L0", dur=0.5),
        dict(type="gauge", box=[140, 640, 800, 90], value=c["value"], max=230, mark=176, color=p["color"], at="L0@0.2", dur=1.4),
        T("176", 140 + 800 * 176 / 230, 610, 52, font="body", at="L0@0.3", dur=0.3),
        T(str(c["value"]), 540, 930, 170, color=p["color"], at="L0@0.45", dur=0.5),
        T(c["key"], 540, 1080, fit(c["key"], 74, 960), at="L0@0.6", dur=0.5),
        *([stamp(c["stamp"], c["sub"], "L0@0.8", y=1260, w=560, h=140, size=56)] if c.get("stamp") else []),
    ])


def sc_pasar(p):
    a = p["pasar"]
    els = [T("¿QUÉ TENDRÍA QUE PASAR?", 540, 470, fit("¿QUÉ TENDRÍA QUE PASAR?", 82, 980), at="L0", dur=0.5)]
    y = 680
    for i, (txt, ok) in enumerate(a["items"]):
        at = f"L0@{0.25 + 0.3 * i:.2f}"
        els += [dict(type="circle", x=150, y=y - 25, rx=48, color=p["color"], width=8, at=at, dur=0.3),
                T(str(i + 1), 150, y, 70, color=p["color"], at="+0", dur=0.15),
                T(txt, 230, y, fit(txt, 62, 800), align="left", at="+0.05", dur=0.5)]
        y += 200
    els += key_lines([a["key"]], a.get("at_key", "L1"), y0=1250)
    return dict(id="pasar", lines=a["lines"], footnote=a["foot"], elements=els)


def sc_precedente(p):
    r = p["prec"]
    return dict(id="precedente", lines=[r["line"]], footnote=r["foot"], elements=[
        dict(type="highlight", x0=390, x1=690, y=500, width=90, at="L0", dur=0.3),
        T("¡OJO!", 540, 540, 140, at="+0", dur=0.35),
        T(r["year"], 540, 760, 150, color="gray", at="L0@0.15", dur=0.5),
        *key_lines(r["key"], "L0@0.35", y0=930),
        stamp(r["stamp"], r["sub"], "L0@0.8", y=1260, w=600, h=140, size=56),
    ])


def sc_promesas(p):
    m = p["promesas"]
    els = [T(m["title"], 540, 470, fit(m["title"], 80, 980), at="L0", dur=0.5)]
    y = 660
    for i, txt in enumerate(m["items"]):
        els += [dict(type="check", x=150, y=y - 25, r=40, color=p["color"], width=12, at=f"L0@{0.2 + 0.25 * i:.2f}", dur=0.3),
                T(txt, 230, y, fit(txt, 64, 810), align="left", at="+0.05", dur=0.5)]
        y += 180
    els.append(stamp("PROMESA", m["sub"], "L0@0.85", y=1260, w=520, h=140, size=58))
    return dict(id="promesas", lines=[m["line"]], footnote=m["foot"], elements=els)


def sc_cierre(p):
    q = p["cierre"]
    els = [
        dict(type="icon", name="question", x=540, y=560, scale=1.0, at="L0", dur=0.5),
        T(q["pregunta"], 540, 800, fit(q["pregunta"], 84, 980), at="L0@0.2", dur=0.6, line_height=1.08),
        T("COMENTA", 540, 1000, 70, color="gray", at="L1", dur=0.3),
        T(q["opciones"], 540, 1100, fit(q["opciones"], 88, 980), color=p["color"], at="+0.05", dur=0.4),
        stamp("SÍGUENOS", q["sub"], "L2", y=1270, w=560, h=140, size=64),
    ]
    return dict(id="cierre", lines=q["lines"], elements=els)


def build(p):
    scenes = [sc_gancho(p), sc_regla(p), sc_hoy(p), sc_camino(p), sc_pasar(p), sc_precedente(p), sc_promesas(p), sc_cierre(p)]
    return dict(
        slug=p["slug"], title=p["title"], series_tag=f"29N · ¿GOBIERNA? · EP. {p['ep']}/3", accent=p["color"],
        icon_accent={"blue": "gray", "red": "yellow"},
        handle="@pizarrapublica", voice=VOZ,
        music_volume=0.12, scribble_volume=0.05, end_hold=0.8, line_gap=0.08,
        sources=p["sources"], caption=p["caption"], pinned_comment=p["pinned"], hashtags=p["hashtags"],
        scenes=scenes,
    )


SRC_ENCUESTAS = [
    "Ara (09-12/10/2026), recopilación de encuestas del 29N: GESOP, Sigma Dos, 40dB, SocioMétrica, GAD3, CIS: https://en.ara.cat/politics/what-do-the-polls-for-the-spanish-elections-of-november-29-say_1_5874100.html",
    "El Liberal (09/10/2026): Imop/El Confidencial, 40dB y DYM: https://www.elliberal.cat/2026/10/09/la-derecha-lograria-201-escanos-y-vox-duplicaria-su-representacion-el-29n/",
    "Constitución Española, art. 99 (investidura)",
    "Resultados de las generales del 23/07/2023 (Ministerio del Interior)",
]
TAGS = ["#PizarraPública", "#PolíticaEspañola", "#Elecciones29N", "#Encuestas"]
PIN = "📚 Fuentes: media de 6 encuestas de octubre (GESOP, Sigma Dos, 40dB, SocioMétrica, Imop, DYM); {extra}. Las encuestas no son resultados. ¿Ves un error? Dínoslo y lo corregimos."


def caption(hook, steps, q, nxt):
    return f"🤯 {hook}\n" + "\n".join(steps) + f"\n💬 {q}\n➡️ 29N · Ep. {nxt} · 🔔 Síguenos para no perderte el siguiente · 📚 Fuentes en comentarios"


PSOE = dict(
    ep=1, slug="escenarios29n_ep1_psoe", color="psoe", title="29N · ¿Qué tiene que pasar para que gobierne el PSOE?",
    hook=("¿PUEDE GANAR", "EL PSOE", "EL 29 DE NOVIEMBRE?"),
    l_hook=L("¿Puede volver a gobernar el PSOE el 29 de noviembre? Te cuento qué tendría que pasar.",
             "¿Puede volver a gobernar el Pesoe el veintinueve de noviembre? Te cuento qué tendría que pasar."),
    hoy=dict(antes=121, hoy=108, key="2023: 121 · Encuestas de octubre: 108 de media",
             line=L("Las seis encuestas de octubre le dan de media 108 diputados. En 2023 sacó 121.",
                    "Las seis encuestas de octubre le dan de media ciento ocho diputados. En dos mil veintitrés sacó ciento veintiuno.")),
    camino=dict(title="PSOE + SUS SOCIOS DE 2023", value=148, key="le faltarían 28", stamp="NO LLEGA", sub="Imop · 5-7 oct.",
                foot="Imop para El Confidencial (5-7/10/2026)",
                line=L("Sumando a todos los partidos que le apoyaron en 2023, llegaría a unos 148. Le faltarían 28.",
                       "Sumando a todos los partidos que le apoyaron en dos mil veintitrés, llegaría a unos ciento cuarenta y ocho. Le faltarían veintiocho.")),
    pasar=dict(items=[("Que PP y Vox no sumen 176", False), ("Que Junts y PNV le vuelvan a apoyar", True)],
               key="Hoy PP + Vox suman unos 200", foot=ENCUESTAS,
               lines=[L("Tendrían que pasar dos cosas: que PP y Vox no sumen 176, y que Junts y PNV le vuelvan a apoyar.",
                        "Tendrían que pasar dos cosas: que pepé y Vox no sumen ciento setenta y seis, y que Junts y PeNeVe le vuelvan a apoyar."),
                      L("Hoy las encuestas les dan unos 200.", "Hoy las encuestas les dan unos doscientos.")]),
    prec=dict(year="2023", key=["las encuestas daban mayoría a PP y Vox", "se quedaron en 170 y gobernó Sánchez"], stamp="179 VOTOS", sub="investidura · 16/11/2023",
              foot="Resultados 23J 2023 · investidura del 16/11/2023",
              line=L("Ojo: en 2023 las encuestas también daban mayoría a PP y Vox. Se quedaron en 170, y Sánchez fue investido con 179 votos.",
                     "Ojo: en dos mil veintitrés las encuestas también daban mayoría a pepé y Vox. Se quedaron en ciento setenta, y Sánchez fue investido con ciento setenta y nueve votos.")),
    promesas=dict(title="SI GOBIERNA, PROMETE", items=["Alquileres sin fecha de fin", "Jornada de 36 h antes de 2030", "Pensiones que suben con el IPC"],
                  sub="aún sin programa del 29N", foot="Anuncios de Sánchez (9-11/10/2026) · 41.º Congreso del PSOE",
                  line=L("Si gobierna, promete alquileres sin fecha de fin, jornada de 36 horas antes de 2030 y pensiones que suban con los precios.",
                         "Si gobierna, promete alquileres sin fecha de fin, jornada de treinta y seis horas antes de dos mil treinta y pensiones que suban con los precios.")),
    cierre=dict(pregunta="¿PUEDE\nREMONTAR?", opciones="SÍ  o  NO", sub="mañana: el PP",
                lines=["¿Crees que puede remontar?", "Comenta sí o no.",
                       L("Y síguenos: mañana, qué tiene que pasar para que gobierne el PP.",
                         "Y síguenos: mañana, qué tiene que pasar para que gobierne el pepé.")]),
    sources=SRC_ENCUESTAS + ["Qué! (09/10/2026), alquiler indefinido; Forbes (05/10/2026), resoluciones del 41.º Congreso del PSOE; The Objective (08/10/2026), pensiones con el IPC"],
    pinned=PIN.format(extra="Imop/El Confidencial (socios: 148); resultados 2023 e investidura del 16/11/2023; anuncios de Sánchez 9-11/10"),
    hashtags=TAGS + ["#PSOE"],
    caption=caption("¿Qué tiene que pasar para que gobierne el PSOE?",
                    ["🗳️ Hacen falta 176 diputados de 350", "📊 Encuestas de octubre: 108 de media (en 2023, 121)",
                     "➕ Con sus socios de 2023: unos 148. Le faltan 28", "⚠️ En 2023 las encuestas también fallaron: PP + Vox, 170"],
                    "¿Puede remontar? Sí o no", "1/3 · Próximo: PP"),
)

PP = dict(
    ep=2, slug="escenarios29n_ep2_pp", color="pp", title="29N · ¿Qué tiene que pasar para que gobierne el PP?",
    hook=("TODAS LAS ENCUESTAS", "DAN GANADOR AL PP", "pero ganar no es gobernar"),
    l_hook=L("Todas las encuestas dan ganador al PP. Pero ganar no es gobernar. Te cuento qué tendría que pasar.",
             "Todas las encuestas dan ganador al pepé. Pero ganar no es gobernar. Te cuento qué tendría que pasar."),
    hoy=dict(antes=137, hoy=134, key="2023: 137 · Encuestas de octubre: 134 de media",
             line=L("Las seis encuestas de octubre le dan de media 134 diputados. En 2023 sacó 137… y no pudo gobernar.",
                    "Las seis encuestas de octubre le dan de media ciento treinta y cuatro diputados. En dos mil veintitrés sacó ciento treinta y siete… y no pudo gobernar.")),
    camino=dict(title="¿MAYORÍA ABSOLUTA SOLO?", value=134, key="ninguna encuesta se la da", stamp="NO LLEGA", sub="la más alta: 147",
                foot="NC Report (agosto): 145-147, la más alta",
                line=L("¿Mayoría absoluta él solo? Ninguna encuesta se la da. La más alta, 147.",
                       "¿Mayoría absoluta él solo? Ninguna encuesta se la da. La más alta, ciento cuarenta y siete.")),
    pasar=dict(items=[("Que PP + Vox sumen 176", True), ("Que Vox le apoye: dentro o fuera", True)],
               key="Hoy PP + Vox suman unos 200", foot=ENCUESTAS,
               lines=[L("Tendrían que pasar dos cosas: que PP y Vox sumen 176, y que Vox le apoye, dentro del Gobierno o desde fuera.",
                        "Tendrían que pasar dos cosas: que pepé y Vox sumen ciento setenta y seis, y que Vox le apoye, dentro del Gobierno o desde fuera."),
                      L("Hoy las encuestas les dan unos 200.", "Hoy las encuestas les dan unos doscientos.")]),
    prec=dict(year="2023", key=["las encuestas decían lo mismo", "sumaron 170 y Feijóo no fue investido"], stamp="172 SÍ · 178 NO", sub="investidura · 27/09/2023",
              foot="Resultados 23J 2023 · investidura del 27/09/2023",
              line=L("Ojo: en 2023 las encuestas decían lo mismo. Sumaron 170, y Feijóo perdió la investidura: 172 votos a favor y 178 en contra.",
                     "Ojo: en dos mil veintitrés las encuestas decían lo mismo. Sumaron ciento setenta, y Feijóo perdió la investidura: ciento setenta y dos votos a favor y ciento setenta y ocho en contra.")),
    promesas=dict(title="SI GOBIERNA, PROMETE", items=["IVA 0 % en alimentos básicos", "Avales del 100 % de la hipoteca", "Visado por puntos para inmigrar"],
                  sub="aún sin programa del 29N", foot="Decálogo económico del PP (27/09/2026) · Plan de Inmigración (14/10/2025)",
                  line=L("Si gobierna, promete IVA cero en alimentos básicos, avales del 100 % de la hipoteca para jóvenes y un visado por puntos para inmigrar.",
                         "Si gobierna, promete IVA cero en alimentos básicos, avales del cien por cien de la hipoteca para jóvenes y un visado por puntos para inmigrar.")),
    cierre=dict(pregunta="¿EL PP SOLO\nO CON VOX?", opciones="A: SOLO   B: CON VOX", sub="mañana: Vox",
                lines=["¿Mejor el PP solo o con Vox?", "Comenta A o B.",
                       "Y síguenos: mañana, qué tiene que pasar para que gobierne Vox."]),
    sources=SRC_ENCUESTAS + ["NC Report/La Razón (agosto 2026)", "Investidura fallida de Feijóo, 27/09/2023 (EFE)",
                             "PP, decálogo económico (27/09/2026) y Plan Nacional de Inmigración (14/10/2025), pp.es"],
    pinned=PIN.format(extra="NC Report (agosto); resultados 2023 e investidura del 27/09/2023; decálogo económico del PP (27/09/2026) y Plan de Inmigración (14/10/2025)"),
    hashtags=TAGS + ["#PP"],
    caption=caption("Todas las encuestas dan ganador al PP. Pero ganar no es gobernar",
                    ["🗳️ Hacen falta 176 diputados de 350", "📊 Encuestas de octubre: 134 de media (en 2023, 137)",
                     "🚫 Mayoría absoluta solo: ninguna encuesta se la da", "⚠️ En 2023 sumó 170 con Vox y Feijóo no fue investido"],
                    "¿Mejor el PP solo o con Vox? A o B", "2/3 · Próximo: Vox"),
)

VOX = dict(
    ep=3, slug="escenarios29n_ep3_vox", color="vox", title="29N · ¿Qué tiene que pasar para que gobierne Vox?",
    hook=("LAS ENCUESTAS NO LE DAN GANADOR", "PERO VOX PUEDE DECIDIR", "quién gobierna"),
    l_hook=L("Ninguna encuesta da ganador a Vox el 29 de noviembre. Pero puede decidir quién gobierna. Te cuento cómo.",
             "Ninguna encuesta da ganador a Vox el veintinueve de noviembre. Pero puede decidir quién gobierna. Te cuento cómo."),
    hoy=dict(antes=33, hoy=66, key="2023: 33 · Encuestas de octubre: 66 de media",
             line=L("Las seis encuestas de octubre le dan de media 66 diputados. El doble que en 2023, cuando sacó 33.",
                    "Las seis encuestas de octubre le dan de media sesenta y seis diputados. El doble que en dos mil veintitrés, cuando sacó treinta y tres.")),
    camino=dict(title="PP + VOX", value=200, key="por encima de 176", stamp="LA LLAVE", sub="sin Vox, el PP no llega",
                foot=ENCUESTAS,
                line=L("¿Ser el más votado? Tendría que ganar unos 14 puntos. Pero el PP no llega solo, y con Vox sumaría unos 200.",
                       "¿Ser el más votado? Tendría que ganar unos catorce puntos. Pero el pepé no llega solo, y con Vox sumaría unos doscientos.")),
    pasar=dict(items=[("Entrar en el Gobierno con el PP", True), ("Apoyar desde fuera o abstenerse", True)],
               key="Vox decide el precio de su apoyo", foot=ENCUESTAS,
               lines=["Tendría dos caminos: entrar en el Gobierno con el PP, o apoyarle desde fuera.",
                      "Y el precio de ese apoyo lo pone Vox."]),
    prec=dict(year="2023", key=["entró en 5 gobiernos autonómicos con el PP", "y los dejó en julio de 2024"], stamp="SALIÓ", sub="11/07/2024 · reparto de menores",
              foot="El Independiente (11/07/2024)",
              line=L("Ojo: en 2023 entró en cinco gobiernos autonómicos con el PP. Los dejó en julio de 2024 por el reparto de menores migrantes.",
                     "Ojo: en dos mil veintitrés entró en cinco gobiernos autonómicos con el pepé. Los dejó en julio de dos mil veinticuatro por el reparto de menores migrantes.")),
    promesas=dict(title="LO QUE PIDE EN SU PROGRAMA", items=["Prioridad nacional en vivienda", "Devolver a quien entró irregular", "0 € de IRPF hasta 22.000 €"],
                  sub="aún sin programa del 29N", foot="Programa económico y de vivienda de Vox · mitin de Estepona (11/10/2026)",
                  line=L("Lo que pide: prioridad nacional en la vivienda protegida, devolver a quien entró de forma irregular y nada de IRPF hasta 22.000 euros.",
                         "Lo que pide: prioridad nacional en la vivienda protegida, devolver a quien entró de forma irregular y nada de IRPF hasta veintidós mil euros.")),
    cierre=dict(pregunta="¿VOX DEBERÍA ENTRAR\nEN EL GOBIERNO?", opciones="SÍ  o  NO", sub="no te pierdas el 29N",
                lines=["¿Vox debería entrar en el Gobierno?", "Comenta sí o no.",
                       "Y síguenos para no perderte nada del 29 de noviembre."]),
    sources=SRC_ENCUESTAS + ["El Independiente (11/07/2024): Vox rompe cinco gobiernos autonómicos con el PP",
                             "Vox, programa económico y de vivienda (voxespana.es, págs. 36-37 y 44-47); El Independiente (11/10/2026), mitin de Estepona"],
    pinned=PIN.format(extra="El Independiente 11/07/2024 (salida de 5 gobiernos autonómicos); programa económico y de vivienda de Vox"),
    hashtags=TAGS + ["#Vox"],
    caption=caption("Ninguna encuesta da ganador a Vox. Pero puede decidir quién gobierna",
                    ["🗳️ Hacen falta 176 diputados de 350", "📊 Encuestas de octubre: 66 de media (en 2023, 33)",
                     "🔑 El PP no llega solo: con Vox, unos 200", "⚠️ En 2024 dejó 5 gobiernos autonómicos con el PP"],
                    "¿Vox debería entrar en el Gobierno? Sí o no", "3/3"),
)


if __name__ == "__main__":
    for p in (PSOE, PP, VOX):
        path = os.path.join(OUT, p["slug"] + ".json")
        json.dump(build(p), open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("→", os.path.relpath(path, os.path.join(HERE, "..")))
