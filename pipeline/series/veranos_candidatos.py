#!/usr/bin/env python3
"""«Así veranean los tres candidatos» (verano 2026): Sánchez, Feijóo y Abascal como pizarras.

Mismo tiempo y mismo tono para los tres (un gag suave cada uno). Fuentes (prensa; ninguno publicó datos oficiales):
  Sánchez: El Independiente 01/08/2026 (La Mareta, Falcon, 1 de agosto, Ceuta el 31/07, zona de navegación restringida)
    https://www.elindependiente.com/espana/2026/08/01/pedro-sanchez-se-va-de-vacaciones-a-la-mareta-lanzarote-en-plena-crisis-de-ceuta/amp/
    Vozpópuli 30/07/2026 (más de 60 agentes estimados con las cifras del año anterior, patrullera; contrato de
    unos 250.000 € de vigilancia privada del recinto)
    https://www.vozpopuli.com/espana/las-vacaciones-de-sanchez-en-la-mareta-obliga-a-movilizar-a-60-policias-y-guardias-civiles-un-barco-y-helicopteros.html
  Feijóo: Infobae 08/08/2026 (Moaña, casa de su pareja frente a la playa de O Con, baño, Monte Faro de Domaio, fútbol con su hijo)
    https://www.infobae.com/espana/2026/08/08/asi-son-las-vacaciones-de-los-politicos-espanoles-de-yolanda-diaz-en-un-resort-de-lujo-en-grecia-a-feijoo-o-abascal-en-pueblos-del-norte/
  Abascal: El Debate 22/07/2026 (Benia de Onís, ~200 habitantes, casa alquilada unas semanas, Covadonga) e Infobae
    08/08/2026 (barco por la costa de Llanes, quesería de Gamonéu)
    https://www.eldebate.com/gente/20260722/pueblo-asturiano-200-habitantes-elegido-santiago-abascal-veraneo_441930.html
Uso: python3 series/veranos_candidatos.py → storyboards/veranos_candidatos.json
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "storyboards")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
import compra2026 as base  # noqa: E402
from compra2026_serie import obj, pj, plano, rot  # noqa: E402
from padres_viva import V  # noqa: E402

C = "red"
SUELO = 1340
INDEP = "El Independiente (01/08/2026)"
VOZ = "Vozpópuli (30/07/2026), estimación"
INFOBAE = "Infobae (08/08/2026)"
DEBATE = "El Debate (22/07/2026) · Infobae (08/08/2026)"


def cand(quien, x, at=0.0, scale=0.8, cara="normal", acciones=(), **kw):
    return pj(quien, x, at, scale, cara, acciones, id=quien, **kw)


scenes = [
    # 1 · GANCHO: los tres en fila, cada uno con su destino
    dict(id="gancho", fondo={"tipo": "playa", "variante": "ria"}, animo="alegre", footnote="Prensa · julio y agosto de 2026", lines=[
        V("Tres candidatos al 29N.", "energia"),
        V("Tres veranos que no se parecen en nada.", "remate", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@veranos", "abierto", dur=0.5)],
       elements=[
        cand("sanchez", 220, 0, 0.62, "riendo", entra="pop", acciones=[{"at": "@veranos", "mira": "feijoo"}, {"at": "@nada", "pose": "encoge"}]),
        cand("feijoo", 540, "@candidatos-0.3", 0.62, "ilusionado", entra="pop", acciones=[{"at": "@veranos", "mira": "abascal"}, {"at": "@nada", "pose": "encoge"}]),
        cand("abascal", 860, "@candidatos", 0.62, "normal", entra="pop", acciones=[{"at": "@veranos", "mira": "sanchez"}, {"at": "@nada", "pose": "encoge"}]),
        rot("LANZAROTE", 220, 560, "@veranos", 52, "amarillo"),
        rot("MOAÑA", 540, 500, "@veranos+0.2", 52, "amarillo"),
        rot("ASTURIAS", 860, 560, "@veranos+0.4", 52, "amarillo"),
    ]),
    # 2 · SÁNCHEZ: llega en Falcon a La Mareta
    dict(id="sanchez", fondo={"tipo": "playa", "variante": "volcan"}, animo="curioso", trans="iris", footnote=INDEP, lines=[
        V("Sánchez: La Mareta, la residencia oficial en Lanzarote.", "normal"),
        V("Llegó el 1 de agosto en un Falcon, un día después de visitar Ceuta en plena crisis migratoria.", "intriga"),
    ], camara=[plano(0, "general", dur=0), plano("@Falcon", "abierto", dur=0.5), plano("@Ceuta", "medio", "sanchez", 0.4, aire=180)],
       elements=[
        obj("avion", -400, 520, 0, 0.9, entra="nada", id="avion", sfx="whoosh",
            acciones=[{"at": 0, "x": 1500, "y": 440, "dur": 3.2}]),
        cand("sanchez", 1300, "@residencia", 0.75, "ilusionado", entra="der", acciones=[
            {"at": "@residencia", "x": 620, "dur": 1.4}, {"at": "@Lanzarote", "salta": True, "cara": "riendo"},
            {"at": "@Llegó", "mira": "avion"}, {"at": "@agosto", "pose": "saluda", "cara": "riendo"},
            {"at": "@Ceuta", "cara": "preocupado", "pose": "piensa", "mira": "izq"},
            {"at": "@migratoria", "cara": "serio"}]),
        rot("LA MARETA", 540, 470, "@Mareta", 90, "amarillo", golpe=True, out="@agosto"),
        rot("1 DE AGOSTO", 540, 470, "@agosto", 90, "amarillo", golpe=True, out="@Ceuta"),
        rot("31/07: CEUTA", 540, 470, "@Ceuta", 90, C, golpe=True),
    ]),
    # 3 · SEGURIDAD Y COSTE: el gag del mar restringido y el único número publicado
    dict(id="seguridad", fondo={"tipo": "playa", "variante": "volcan"}, animo="comico", trans="pan", footnote=VOZ + " · " + INDEP, lines=[
        V("Por seguridad: más de 60 agentes, una patrullera y el mar de delante, restringido.", "normal"),
        V("Coste publicado: unos 250.000 euros de vigilancia privada.", "remate", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@mar", "medio", "sanchez", 0.3, aire=200), plano("@Coste", "general", dur=0.4)],
       elements=[
        cand("sanchez", 320, 0, 0.75, "ilusionado", entra="nada", acciones=[
            {"at": "@seguridad", "x": 520, "dur": 0.9}, {"at": "@patrullera", "mira": "der"},
            {"at": "@mar", "mira": "der"}, {"at": "@restringido", "take": True, "cara": "sorpresa"},
            {"at": "@Coste", "cara": "pensativo", "mira": "camara"},
            {"at": "@250.000", "pose": "encoge", "cara": "serio"}]),
        obj("coche", -300, SUELO - 90, "@agentes", 0.6, entra="nada", props={"color": "azul"},
            acciones=[{"at": "@agentes", "x": 1400, "dur": 2.4}]),
        obj("cartel", 850, 1000, "@restringido-0.2", 0.62, props={"lineas": ["NAVEGACIÓN", "RESTRINGIDA"], "color": "rojo", "tinta": "blanco"},
            entra="cae", dur=0.5, sfx="golpe"),
        rot("+60 AGENTES", 540, 470, "@60", 110, "amarillo", golpe=True, out="@Coste"),
        rot("+ PATRULLERA", 540, 590, "@patrullera", 70, "blanco", out="@Coste"),
        rot("250.000 €", 540, 500, "@250.000", 130, C, golpe=True),
        rot("vigilancia privada del recinto", 540, 620, "@vigilancia", 54, "blanco"),
    ]),
    # 5 · FEIJÓO: Moaña, ría de Vigo
    dict(id="feijoo", fondo={"tipo": "playa", "variante": "ria"}, animo="alegre", trans="pan", footnote=INFOBAE, lines=[
        V("Feijóo: Moaña, en la ría de Vigo, en la casa de su pareja frente a la playa.", "normal"),
        V("Baño, monte… y fútbol en la arena.", "energia", 0.1),
    ], camara=[plano(0, "general", dur=0), plano("@fútbol", "medio", "feijoo", 0.3, aire=220)],
       elements=[
        cand("feijoo", -200, 0, 0.75, "ilusionado", entra="nada", acciones=[
            {"at": 0, "x": 420, "dur": 1.5}, {"at": "@Vigo", "pose": "senala", "mira": "der", "cara": "riendo"},
            {"at": "@pareja", "salta": True}, {"at": "@playa", "pose": "arriba", "mira": "camara"},
            {"at": "@Baño", "salta": True, "cara": "riendo"}, {"at": "@monte", "pose": "arriba"},
            {"at": "@fútbol", "pose": "punos", "cara": "ilusionado", "mira": "balon"},
            {"at": "@arena+0.55", "take": True, "cara": "sorpresa"}, {"at": "@arena+1.3", "cara": "riendo", "pose": "pulgar"}]),
        obj("balon", 900, SUELO - 70, "@fútbol-0.2", 0.9, id="balon", entra="pop",
            acciones=[{"at": "@fútbol+0.2", "x": 560, "y": SUELO - 520, "dur": 0.45}, {"at": "@arena+0.4", "x": 480, "y": SUELO - 470, "dur": 0.2},
                      {"at": "@arena+0.7", "x": 880, "y": SUELO - 70, "dur": 0.5}]),
        dict(type="efecto", efecto="pum", text="¡BOING!", x=520, y=760, at="@arena+0.55", scale=0.7, vida=0.7),
        rot("MOAÑA", 540, 470, "@Moaña", 100, "amarillo", golpe=True, out="@Baño"),
        rot("BAÑO · MONTE · FÚTBOL", 540, 470, "@Baño", 70, "amarillo"),
    ]),
    # 6 · ABASCAL: Benia de Onís, Asturias
    dict(id="abascal", fondo={"tipo": "playa", "variante": "montana"}, animo="alegre", trans="pan", footnote=DEBATE, lines=[
        V("Abascal: unas semanas en Benia de Onís, un pueblo asturiano de 200 vecinos.", "normal"),
        V("Covadonga, barco por Llanes… y una quesería.", "energia", 0.1),
    ], camara=[plano(0, "general", dur=0), plano("@quesería", "medio", "abascal", 0.3, aire=220)],
       elements=[
        cand("abascal", 1300, 0, 0.75, "ilusionado", entra="nada", acciones=[
            {"at": 0, "x": 620, "dur": 1.5}, {"at": "@Onís", "pose": "senala_izq", "mira": "izq", "cara": "riendo"},
            {"at": "@asturiano", "salta": True}, {"at": "@200", "mira": "camara", "pose": "jarras"},
            {"at": "@Covadonga", "pose": "arriba", "cara": "riendo"}, {"at": "@Llanes", "salta": True},
            {"at": "@quesería", "mira": "queso", "pose": "punos", "cara": "sorpresa"},
            {"at": "@quesería+0.6", "take": True}, {"at": "@quesería+1.2", "cara": "riendo", "pose": "pulgar"}]),
        obj("queso", 400, 1120, "@quesería-0.3", 0.8, id="queso", entra="cae", dur=0.5, props={"texto": "GAMONÉU", "cara": "riendo"}),
        rot("BENIA DE ONÍS", 540, 470, "@Benia", 90, "amarillo", golpe=True, out="@200"),
        rot("200 VECINOS", 540, 470, "@200", 100, "amarillo", golpe=True, out="@Covadonga"),
        rot("COVADONGA · LLANES", 540, 470, "@Covadonga", 70, "amarillo"),
    ]),
    # 7 · CONTRASTE: por qué solo hay cifras de uno
    dict(id="contraste", fondo="plano", animo="curioso", trans="iris", footnote="Prensa · julio y agosto de 2026", lines=[
        V("Lo curioso: solo hay cifras del verano de Sánchez, porque viaja como presidente.", "intriga"),
        V("Los de Feijóo y Abascal son privados: no hay datos.", "remate", 0.15),
    ], camara=[plano(0, "general", dur=0)],
       elements=[
        cand("sanchez", 220, 0, 0.62, "normal", entra="pop", acciones=[{"at": "@Sánchez", "salta": True, "pose": "encoge"},
                                                                       {"at": "@presidente", "pose": "senala_arriba", "cara": "serio"},
                                                                       {"at": "@privados", "mira": "feijoo"}]),
        cand("feijoo", 540, 0, 0.62, "normal", entra="pop", acciones=[{"at": "@Feijóo", "salta": True, "cara": "pensativo"}, {"at": "@datos", "pose": "encoge", "mira": "camara"}]),
        cand("abascal", 860, 0, 0.62, "normal", entra="pop", acciones=[{"at": "@Abascal", "salta": True, "cara": "pensativo"}, {"at": "@datos", "pose": "encoge", "mira": "camara"}]),
        rot("250.000 €", 220, 640, "@cifras", 64, C, golpe=True),
        rot("COMO PRESIDENTE", 540, 470, "@presidente", 76, "amarillo", golpe=True, out="@privados"),
        rot("PRIVADOS", 540, 470, "@privados", 90, "amarillo", golpe=True),
        rot("?", 540, 640, "@privados", 120, "blanco", golpe=True),
        rot("?", 860, 640, "@privados+0.2", 120, "blanco", golpe=True),
    ]),
    # 8 · FINAL: del bañador al 29N, pregunta y llamada dentro de la escena
    dict(id="final", fondo={"tipo": "playa", "variante": "ria"}, animo="final", trans="iris", footnote="Elecciones generales · 29 de noviembre de 2026", lines=[
        V("Y ahora, del bañador al 29N.", "energia"),
        V("¿Qué verano se parece más al tuyo? Te leemos. Y síguenos.", "intriga", 0.1),
    ], camara=[plano(0, "general", dur=0), plano("@síguenos", "abierto", dur=0.4)],
       elements=[
        cand("sanchez", 220, 0, 0.62, "riendo", entra="nada", acciones=[{"at": "@29N", "salta": True}, {"at": "@verano", "mira": "camara", "cara": "pensativo"}, {"at": "@leemos", "pose": "senala", "cara": "ilusionado"}, {"at": "@síguenos", "pose": "saluda", "cara": "riendo"}]),
        cand("feijoo", 540, 0, 0.62, "riendo", entra="nada", acciones=[{"at": "@29N+0.15", "salta": True}, {"at": "@verano", "mira": "camara", "cara": "pensativo"}, {"at": "@leemos", "pose": "senala", "cara": "ilusionado"}, {"at": "@síguenos", "pose": "saluda", "cara": "riendo"}]),
        cand("abascal", 860, 0, 0.62, "riendo", entra="nada", acciones=[{"at": "@29N+0.3", "salta": True}, {"at": "@verano", "mira": "camara", "cara": "pensativo"}, {"at": "@leemos", "pose": "senala", "cara": "ilusionado"}, {"at": "@síguenos", "pose": "saluda", "cara": "riendo"}]),
        rot("29N", 540, 480, "@29N", 160, "amarillo", golpe=True, out="@verano"),
        rot("¿Y EL TUYO?", 540, 480, "@verano", 110, "amarillo", golpe=True, out="@síguenos"),
        rot("SÍGUENOS", 540, 480, "@síguenos", 110, "amarillo", fx=[{"at": "@síguenos+0.6", "do": "latir"}]),
    ]),
]

SB = dict(base.SB)
SB.update(
    slug="veranos_candidatos", title="Así veranean los tres candidatos", series_tag="CAMINO AL 29N",
    scenes=scenes, banda=True, music_volume=0.2, scribble_volume=0.0, sfx_volume=1.0, end_hold=0.9,
    portada={"t": 3.0, "titulo": "Así veranean los tres candidatos", "capitulo": None},
    sources=[
        "El Independiente (01/08/2026): https://www.elindependiente.com/espana/2026/08/01/pedro-sanchez-se-va-de-vacaciones-a-la-mareta-lanzarote-en-plena-crisis-de-ceuta/amp/",
        "Vozpópuli (30/07/2026): https://www.vozpopuli.com/espana/las-vacaciones-de-sanchez-en-la-mareta-obliga-a-movilizar-a-60-policias-y-guardias-civiles-un-barco-y-helicopteros.html",
        "Infobae (08/08/2026): https://www.infobae.com/espana/2026/08/08/asi-son-las-vacaciones-de-los-politicos-espanoles-de-yolanda-diaz-en-un-resort-de-lujo-en-grecia-a-feijoo-o-abascal-en-pueblos-del-norte/",
        "El Debate (22/07/2026): https://www.eldebate.com/gente/20260722/pueblo-asturiano-200-habitantes-elegido-santiago-abascal-veraneo_441930.html",
    ],
    caption=("☀️ Tres candidatos al 29N, tres veranos muy distintos\n"
             "✈️ Sánchez: La Mareta (Lanzarote), llegó en Falcon el 1 de agosto\n"
             "⚽ Feijóo: Moaña, en la ría de Vigo, baño, monte y fútbol\n"
             "🧀 Abascal: Benia de Onís (Asturias), Covadonga, Llanes y quesería\n"
             "💬 ¿Qué verano se parece más al tuyo?\n"
             "➡️ Camino al 29N · 🔔 Síguenos · 📚 Fuentes en comentarios"),
    pinned_comment=("📚 Fuentes (prensa, ninguno publicó datos oficiales): El Independiente 01/08/2026 · Vozpópuli 30/07/2026 "
                    "(+60 agentes es una estimación con las cifras del año anterior; contrato de unos 250.000 € de vigilancia privada) · "
                    "Infobae 08/08/2026 · El Debate 22/07/2026. Los veranos de Feijóo y Abascal son privados: no hay cifras de coste. "
                    "¿Ves un error? Dínoslo."),
    hashtags=["#PizarraPública", "#29N", "#Elecciones2026", "#PedroSánchez", "#Feijóo", "#Abascal", "#Vacaciones", "#Política"],
)

if __name__ == "__main__":
    path = os.path.join(OUT, f"{SB['slug']}.json")
    json.dump(SB, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(path)
