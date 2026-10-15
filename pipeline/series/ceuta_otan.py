#!/usr/bin/env python3
"""«Si atacan Ceuta, ¿viene la OTAN?» (15/10/2026). Primer episodio de la evolución visual: mundo dibujado.

Guion y fuentes: docs/series/ceuta_otan/guion_ceuta_otan.md (copia en /mnt/project-files/insta/guiones/).
  Tratado del Atlántico Norte (nato.int): art. 5 (ataque a uno = ataque a todos, «en Europa o Norteamérica»),
    art. 6 (Europa, Norteamérica, Turquía e islas del Atlántico norte al norte del trópico de Cáncer), art. 4 (consultas).
  Ceuta: portuguesa desde 1415; el Tratado de Lisboa (1668) reconoce la soberanía española.
  Buques: Sánchez lo confirmó el 12/10/2026 (30 y 31 de julio); Elma Saiz (13/10): «puntual»; El País (fuentes
    anónimas): se repitió a principios de agosto (sin confirmar); Marruecos no reconoce la soberanía española
    sobre Ceuta ni sus aguas (Infobae, 15/10/2026).
  Partidos: PSOE en el Senado (24/02/2022): «absolutamente amparadas»; Vox: moción para cambiar el art. 6, rechazada
    (24/02/2022); PP: Feijóo traslada a la Audiencia Nacional la información de los buques (14/10/2026).
Regla del proyecto: la entrada masiva de julio y sus víctimas no se usan como gancho.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from _tu_dinero import *  # noqa: F401,F403,E402
from universo import mapas  # noqa: E402

MX, MY = 540, 820  # el mapa del Estrecho está centrado aquí (escala 1)
LIM = [-6000, -6000, 7000, 7000]  # en los mapas la cámara puede ir lejos (el mar es infinito)


SUELO_ATRIL = 1350


def quien(q, x, at=0.0, scale=0.75, cara="normal", acciones=(), y=1340, **kw):
    kw.setdefault("id", q)
    return dict(type="personaje", quien=q, x=x, y=y, scale=scale, at=at, cara=cara, acciones=list(acciones), **kw)


def P(lon, lat, region="estrecho"):
    return [round(v, 1) for v in mapas.punto(region, lon, lat, MX, MY, 1.0)]


CEUTA = P(-5.335, 35.895)
TARIFA = P(-5.61, 36.02)
ESTRECHO = P(-5.45, 36.0)
MAR_ESTE = P(-5.05, 35.95)
AGUAS = [[-5.402, 35.936], [-5.35, 35.946], [-5.29, 35.937], [-5.258, 35.912], [-5.275, 35.876], [-5.33, 35.843]]
ORDEN = ["Spain", "Portugal", "Gibraltar", "Ceuta", "Morocco", "Melilla", "Balearic Islands", "France", "Andorra", "Algeria"]
AT = (540, 820)  # el mapa atlántico


def PA(lon, lat):
    return [round(v, 1) for v in mapas.punto("atlantico", lon, lat, AT[0], AT[1], 1.0)]


def mapa_estrecho(at=0.0, dibujo=1.6, acciones=(), **props):
    return obj("mapa", MX, MY, at, 1.0, id="mapa", entra="nada", dibujo=dibujo,
               props={"region": "estrecho", "orden": ORDEN, **props}, acciones=list(acciones))


def zoom(at, sobre, z, dur=0.9, **kw):
    """Plano sobre un punto del mapa con zoom z (veces el plano general)."""
    return plano(at, "general", list(sobre), dur, zoom=z, **kw)


def sello(texto, color, y, at, out=None):
    d = obj("sello", 540, y, at, 1.0, hud=True, props={"texto": texto, "color": color}, entra="pop", sfx="golpe")
    if out:
        d["out"] = out
    return d


FTRAT = "Tratado del Atlántico Norte (1949), arts. 5 y 6 · nato.int"
FBUQ = "Sánchez, 12/10/2026 · Gobierno, 13/10 · El País · Infobae"

scenes = [
    # 1 · GANCHO: el mapa se dibuja, la cámara cae sobre Ceuta, aparece un buque y Piz se sorprende
    dict(id="gancho", fondo="mar_mapa", limites=LIM, animo="tension", footnote=FTRAT, lines=[
        V("Si alguien atacara Ceuta, ¿vendría la OTAN a defenderla?", "energia"),
        V("Spoiler: no es automático.", "remate", 0.2),
    ], camara=[plano(0, "general", dur=0), zoom("@Ceuta", ESTRECHO, 2.2, 0.8), zoom("@OTAN", CEUTA, 6.5, 0.7),
               zoom("@Spoiler", ESTRECHO, 4.2, 0.6)],
       elements=[
        mapa_estrecho(0, 1.5, acciones=[{"at": "@Ceuta", "props": {"resalta": ["Ceuta"]}, "sfx": "pop"}]),
        obj("barco", MAR_ESTE[0] + 30, MAR_ESTE[1] + 4, "@atacara", 0.12, id="barco", entra="pop", sfx="redoble",
            props={"bandera": None, "numero": "?", "rumbo": -1},
            acciones=[{"at": "@atacara", "x": CEUTA[0] + 40, "y": CEUTA[1] - 8, "dur": 2.6}]),
        quien("piz", TARIFA[0] - 6, "@OTAN-0.5", 0.055, "normal", y=TARIFA[1] + 6, entra="pop", acciones=[
            {"at": "@OTAN", "take": True, "cara": "sorpresa", "mira": "barco"},
            {"at": "@Spoiler", "cara": "confundido", "pose": "encoge", "mira": "camara"}]),
        rot("¿LA OTAN", 540, 430, "@OTAN", 104, "amarillo", golpe=True),
        rot("DEFENDERÍA CEUTA?", 540, 545, "@OTAN+0.15", 92, "blanco", golpe=True),
        rot("NO ES AUTOMÁTICO", 540, 680, "@automático", 78, "rojo", golpe=True, rot=-4),
    ]),
    # 2 · DÓNDE ESTÁ: se ilumina la península, luego Ceuta; Piz salta el Estrecho; banderas
    dict(id="donde", fondo="mar_mapa", limites=LIM, animo="curioso", trans="corte", footnote="Ceuta: 18,5 km², ciudad autónoma",
         lines=[V("Ceuta es una ciudad española… en África.", "normal"),
                V("Al otro lado del Estrecho, pegada a Marruecos.", "normal", 0.1)],
       camara=[zoom(0, ESTRECHO, 4.2, 0), zoom("@española", P(-4.6, 38.6), 1.15, 0.9), zoom("@África", ESTRECHO, 5.5, 0.9),
               zoom("@Estrecho", P(-5.47, 35.96), 8.5, 0.6)],
       elements=[
        mapa_estrecho(0, 0.01, progreso=1.0, resalta=["Ceuta"], acciones=[
            {"at": "@española", "props": {"resalta": ["Ceuta", "Spain"]}},
            {"at": "@África", "props": {"resalta": ["Ceuta"], "apaga": ["Spain", "Portugal", "France"]}},
            {"at": "@Marruecos", "props": {"resalta": ["Ceuta", "Morocco"], "apaga": ["Spain", "Portugal", "France"]}}]),
        obj("chincheta", P(-3.7, 40.4)[0], P(-3.7, 40.4)[1], "@española", 0.28, props={"diseno": "espana"}, entra="cae",
            out="@África"),
        quien("piz", TARIFA[0] - 4, 0, 0.05, "normal", y=TARIFA[1] + 6, entra="nada", acciones=[
            {"at": "@África", "mira": "der", "cara": "pensativo"},
            {"at": "@Estrecho", "x": CEUTA[0] - 6, "y": CEUTA[1] + 10, "dur": 0.75, "brinco": 26, "cara": "riendo"},
            {"at": "@Marruecos", "mira": "abajo", "cara": "sorpresa"}]),
        obj("chincheta", CEUTA[0] + 14, CEUTA[1] + 2, "@Estrecho+0.6", 0.05, props={"diseno": "espana"}, entra="cae"),
        obj("chincheta", P(-5.42, 35.82)[0], P(-5.42, 35.82)[1], "@Marruecos", 0.05, props={"diseno": "marruecos"}, entra="cae"),
        rot("ESPAÑOLA", 540, 450, "@española", 96, "amarillo", golpe=True, out="@África"),
        rot("…EN ÁFRICA", 540, 450, "@África", 96, "amarillo", golpe=True),
    ]),
    # 3 · LA CIUDAD: Piz pasea junto a las Murallas Reales
    dict(id="ciudad", fondo="ceuta", animo="alegre", trans="zoom", footnote="Tratado de Lisboa, 1668", lines=[
        V("Portuguesa desde 1415. Española desde 1668.", "normal"),
        V("Murallas incluidas.", "remate", 0.15),
    ], camara=[plano(0, "abierto", [380, 1000], 0), plano("@1668", "medio", "piz", 0.8, aire=120),
               plano("@Murallas", "general", [540, 900], 0.6), plano("@incluidas+1.6", "abierto", [420, 950], 1.0)],
       elements=[
        quien("piz", -120, 0, 0.62, "ilusionado", entra="nada", acciones=[
            {"at": 0, "x": 330, "dur": 2.0}, {"at": "@1415", "mira": "arriba"},
            {"at": "@1668", "x": 520, "dur": 1.0, "mira": "camara", "cara": "riendo"},
            {"at": "@Murallas", "pose": "senala_arriba", "salta": True, "cara": "riendo"},
            {"at": "@incluidas+0.5", "gira": True, "flip": True, "pose": "normal"}, {"at": "@incluidas+0.9", "x": 380, "dur": 1.0}]),
        rot("1415 · PORTUGAL", 540, 450, "@1415", 80, "blanco", golpe=True),
        rot("1668 · ESPAÑA", 540, 560, "@1668", 88, "amarillo", golpe=True),
    ]),
    # 4 · EL TRATADO: el pergamino se despliega con los artículos 5 y 6
    dict(id="tratado", fondo={"tipo": "plano", "color": (28, 52, 110)}, animo="curioso", trans="papel", footnote=FTRAT, lines=[
        V("La OTAN funciona con el artículo 5: si atacan a uno, atacan a todos.", "normal"),
        V("Pero el artículo 6 dice dónde: Europa, Norteamérica e islas del Atlántico norte.", "normal", 0.15),
    ], camara=[plano(0, "general", [540, 860], 0), plano("@5", "general", [540, 700], 0.6, zoom=1.12),
               plano("@6", "general", [540, 980], 0.6, zoom=1.12), plano("@norte", "general", [540, 860], 0.6)],
       elements=[
        obj("otan", 540, 215, 0, 0.42, entra="pop", sfx="kaching"),
        obj("documento", 540, 860, 0.3, 1.18, id="doc", entra="nada", dibujo=1.1, sfx="papel", props={
            "titulo": "TRATADO DEL ATLÁNTICO NORTE", "subtitulo": "Washington, 1949",
            "articulos": [
                {"id": "a5", "titulo": "ARTÍCULO 5", "lineas": ["Un ataque armado contra uno", "se considera un ataque", "contra todos"]},
                {"id": "a6", "titulo": "ARTÍCULO 6", "lineas": ["Dónde vale: Europa, Norteamérica,", "Turquía e islas del Atlántico norte", "al norte del trópico de Cáncer"]}]},
            acciones=[{"at": "@uno", "props": {"resalta": ["a5"]}}, {"at": "@dónde", "props": {"resalta": ["a5", "a6"]}}]),
        quien("piz", 1300, "@6-0.4", 0.36, "pensativo", y=1500, entra="nada", acciones=[
            {"at": "@6-0.4", "x": 930, "dur": 0.6}, {"at": "@dónde", "pose": "senala_izq", "mira": "doc"},
            {"at": "@norte", "cara": "sorpresa", "take": True}]),
    ]),
    # 5 · EL MAPA DEL TRATADO: lo que cubre y lo que no (Ceuta, Melilla… y Hawái)
    dict(id="ambito", fondo="mar_mapa", limites=LIM, animo="comico", trans="zoom", footnote=FTRAT + " · Natural Earth", lines=[
        V("Ceuta y Melilla están en África, y el tratado no las nombra.", "normal"),
        V("Ni siquiera Hawái entra.", "remate", 0.2),
    ], camara=[plano(0, "general", [540, 820], 0), zoom("@Ceuta", PA(-8, 38), 2.6, 0.9), zoom("@Hawái", PA(-140, 25), 1.4, 0.8), zoom("@entra+1.5", PA(-150, 22), 2.0, 0.8)],
       elements=[
        obj("mapa", AT[0], AT[1], 0, 1.0, id="atl", entra="nada", dibujo=1.3,
            props={"region": "atlantico", "ambito6": True, "tropico": True,
                   "orden": ["USA", "CAN", "GRL", "ESP", "PRT", "FRA", "GBR", "TUR"]}),
        rot("DENTRO DEL ARTÍCULO 6", 540, 430, 0.3, 66, "blanco", out="@Ceuta"),
        rot("CEUTA Y MELILLA: FUERA", 540, 430, "@nombra", 76, "rojo", golpe=True, out="@Hawái"),
        quien("piz", PA(-157, 21)[0] + 10, "@Hawái-0.2", 0.11, "normal", y=PA(-157, 21)[1] + 8, entra="cae", acciones=[
            {"at": "@entra", "take": True, "cara": "sorpresa", "pose": "cabeza"}, {"at": "@entra+0.7", "tropieza": True}]),
        rot("¡NI HAWÁI!", 540, 430, "@Hawái", 110, "amarillo", golpe=True, rot=-5),
    ]),
    # 6 · EL MATIZ: no es automático, pero hay otras vías
    dict(id="matiz", fondo="mar_mapa", limites=LIM, animo="curioso", trans="corte",
         footnote="Art. 4 del Tratado (consultas) · Art. 42.7 del Tratado de la UE", lines=[
        V("¿Nadie ayudaría? Tampoco.", "normal"),
        V("España puede pedir consultas a los aliados, y la Unión Europea tiene su propia ayuda mutua.", "normal", 0.15),
    ], camara=[zoom(0, PA(-6, 44), 2.4, 0), zoom("@consultas", PA(2, 46), 2.0, 0.8)],
       elements=[
        obj("mapa", AT[0], AT[1], 0, 1.0, entra="nada", props={"region": "atlantico", "ambito6": True, "tropico": True, "progreso": 1.0}),
        quien("piz", PA(-4, 40)[0], 0, 0.1, "preocupado", y=PA(-4, 40)[1] + 10, entra="nada", acciones=[
            {"at": "@Tampoco", "cara": "ilusionado", "salta": True}, {"at": "@consultas", "pose": "senala", "mira": "der"}]),
        obj("bandera", PA(8, 50)[0], PA(8, 50)[1], "@aliados", 0.26, props={"diseno": "otan"}, entra="crece", sfx="papel"),
        obj("bandera", PA(18, 47)[0], PA(18, 47)[1], "@Unión", 0.26, props={"diseno": "ue"}, entra="crece", sfx="papel"),
        rot("ART. 4: CONSULTAS", 540, 430, "@consultas", 76, "blanco", golpe=True),
        rot("UE: AYUDA MUTUA", 540, 540, "@Unión", 76, "amarillo", golpe=True),
    ]),
    # 7 · LA TENSIÓN: buques en el Estrecho, hechos confirmados y lo que está en discusión
    dict(id="buques", fondo="mar_mapa", limites=LIM, animo="tension", trans="zoom", footnote=FBUQ, lines=[
        V("¿Por qué se habla ahora? Sánchez confirmó que buques militares marroquíes entraron en aguas de Ceuta en julio.", "normal"),
        V("El Gobierno dice que fue puntual. Si se repitió en agosto, no está confirmado.", "normal", 0.15),
        V("Y Marruecos no reconoce esas aguas como españolas.", "remate", 0.15),
    ], camara=[zoom(0, P(-5.25, 35.98), 6.5, 0), zoom("@aguas", P(-5.3, 35.93), 8.5, 0.8),
               zoom("@Gobierno", P(-5.27, 35.97), 7.0, 0.6), zoom("@Marruecos", P(-5.3, 35.95), 7.5, 0.6)],
       elements=[
        mapa_estrecho(0, 0.01, progreso=1.0, acciones=[
            {"at": "@aguas", "props": {"lineas": [{"id": "aguas", "puntos": AGUAS, "color": "rojo", "discontinua": True, "ancho": 6, "dur": 1.2}]}, "sfx": "papel"}]),
        quien("piz", P(-5.44, 36.075)[0], 0, 0.03, "normal", y=P(-5.44, 36.075)[1], entra="nada",
              objeto="prismaticos", pose="prismaticos", acciones=[{"at": "@buques", "cara": "sorpresa", "mira": "der"},
                                                                    {"at": "@puntual", "cara": "pensativo"},
                                                                    {"at": "@reconoce", "objeto": None, "pose": "encoge", "cara": "preocupado", "mira": "camara"}]),
        obj("barco", P(-4.95, 35.93)[0], P(-4.95, 35.93)[1], "@buques-0.3", 0.035, id="b1", entra="pop",
            props={"bandera": "marruecos", "rumbo": -1}, acciones=[{"at": "@buques", "x": P(-5.215, 35.93)[0], "dur": 3.2}]),
        obj("barco", P(-4.92, 35.885)[0], P(-4.92, 35.885)[1], "@militares", 0.032, entra="pop",
            props={"bandera": "marruecos", "rumbo": -1}, acciones=[{"at": "@militares", "x": P(-5.19, 35.885)[0], "dur": 3.0}]),
        sello("CONFIRMADO", "verde", 470, "@confirmó", out="@Gobierno"),
        sello("GOBIERNO: «PUNTUAL»", "azul", 470, "@puntual", out="@agosto-0.3"),
        sello("¿AGOSTO? SIN CONFIRMAR", "naranja", 470, "@agosto", out="@Marruecos-0.2"),
        rot("MARRUECOS NO LAS RECONOCE", 540, 470, "@reconoce", 64, "blanco", golpe=True),
    ]),
    # 8 · LAS POSTURAS: tres atriles, una frase documentada cada uno
    dict(id="posturas", fondo="calle", animo="curioso", trans="iris",
         footnote="Senado, 24/02/2022 · Feijóo, 14/10/2026", lines=[
        V("El PSOE dijo en el Senado, en 2022, que ya están amparadas.", "normal"),
        V("El PP ha llevado lo de los buques a la Audiencia Nacional.", "normal", 0.1),
        V("Y Vox pidió cambiar el tratado para nombrarlas; el Senado dijo no.", "normal", 0.1),
    ], camara=[plano(0, "general", dur=0), plano("@PSOE", "medio", "p1", 0.5), plano("@PP", "medio", "p2", 0.5),
               plano("@Vox", "medio", "p3", 0.5), plano("@Senado#2", "general", dur=0.6)],
       elements=[
        quien("diputado", 230, 0, 0.55, "normal", id="p1", entra="pop", acciones=[{"at": "@Senado", "salta": True, "mira": "camara"},
                                                                               {"at": "@2022", "cara": "pensativo", "pose": "senala_arriba"}, {"at": "@amparadas", "pose": "pulgar", "cara": "riendo"}]),
        quien("diputado", 540, 0.15, 0.55, "normal", id="p2", entra="pop", acciones=[{"at": "@Audiencia", "pose": "senala_arriba", "cara": "serio"}]),
        quien("diputado", 850, 0.3, 0.55, "normal", id="p3", entra="pop", acciones=[{"at": "@cambiar", "pose": "puno", "cara": "enfadado"},
                                                                                 {"at": "@Senado#2", "cara": "triste", "pose": "caidos"}]),
        obj("atril", 230, SUELO_ATRIL, 0, 0.46, props={"texto": "PSOE", "color": "psoe"}, entra="nada"),
        obj("atril", 540, SUELO_ATRIL, 0.15, 0.46, props={"texto": "PP", "color": "pp"}, entra="nada"),
        obj("atril", 850, SUELO_ATRIL, 0.3, 0.46, props={"texto": "VOX", "color": "vox"}, entra="nada"),
        rot("PSOE: «YA ESTÁN AMPARADAS»", 540, 450, "@amparadas", 62, "blanco", golpe=True, out="@PP"),
        rot("PP: A LA AUDIENCIA NACIONAL", 540, 450, "@Audiencia", 62, "blanco", golpe=True, out="@Vox"),
        rot("VOX: CAMBIAR EL TRATADO", 540, 450, "@cambiar", 62, "blanco", golpe=True),
        rot("SENADO: NO", 540, 560, "@Senado#2", 80, "rojo", golpe=True),
    ]),
    # 9 · FINAL: la cámara se aleja, Ceuta iluminada, Piz pregunta
    dict(id="final", fondo="mar_mapa", limites=LIM, animo="final", trans="zoom", footnote="Te leemos en comentarios", lines=[
        V("¿Debería el tratado nombrar a Ceuta y Melilla? Te leo.", "normal"),
        V("Y síguenos para el próximo viaje de Piz.", "energia", 0.15),
    ], camara=[zoom(0, CEUTA, 7.0, 0), zoom(0.2, P(-3.6, 38.2), 1.0, 2.2)],
       elements=[
        mapa_estrecho(0, 0.01, progreso=1.0, resalta=["Ceuta", "Melilla"]),
        quien("piz", 790, "@Debería", 0.6, "pensativo", y=1500, hud=True, entra="abajo", acciones=[
            {"at": "@Ceuta", "pose": "senala_izq"}, {"at": "@leo", "mira": "camara", "cara": "ilusionado"},
            {"at": "@síguenos", "pose": "saluda", "cara": "riendo"}, {"at": "@viaje", "salta": True}]),
        rot("¿SÍ O NO?", 540, 450, "@Melilla", 120, "amarillo", golpe=True, out="@síguenos-0.3"),
        rot("SÍGUENOS", 540, 450, "@síguenos", 110, "amarillo", fx=[{"at": "@Piz", "do": "latir"}]),
    ]),
]

if __name__ == "__main__":
    episodio("ceuta_otan", "Si atacan Ceuta, ¿viene la OTAN?", scenes,
             {"t": 2.6, "titulo": "Si atacan Ceuta, ¿viene la OTAN?", "capitulo": None},
             ["Tratado del Atlántico Norte (1949), arts. 4, 5 y 6: https://www.nato.int/cps/en/natohq/official_texts_17120.htm",
              "Tratado de la Unión Europea, art. 42.7 (cláusula de ayuda mutua)",
              "Senado, Comisión de Defensa, 24/02/2022: moción de Vox sobre el art. 6 (Ceuta al Día, El Confidencial Digital)",
              "Sánchez confirma los buques (12/10/2026, The Objective/Euronews); Elma Saiz (13/10, Infobae); Maldita (15/10)",
              "Feijóo lleva los buques a la Audiencia Nacional (El Independiente, 14/10/2026)",
              "Marruecos no reconoce la soberanía sobre Ceuta ni sus aguas (Infobae, 15/10/2026)",
              "Mapas dibujados sobre contornos de Natural Earth (dominio público)"],
             ("🌍 Si atacan Ceuta, ¿viene la OTAN? No es automático\n"
              "📜 Art. 5: un ataque a uno es un ataque a todos\n"
              "🗺️ Art. 6: Europa, Norteamérica e islas al norte del trópico. Ceuta y Melilla, en África, no se nombran\n"
              "🤝 Hay otras vías: consultas (art. 4) y la ayuda mutua de la UE\n"
              "🚢 Buques marroquíes en aguas de Ceuta: confirmado por Sánchez; agosto, sin confirmar\n"
              "💬 ¿Debería el tratado nombrar a Ceuta y Melilla?\n"
              "🔔 Síguenos · 📚 Fuentes en comentarios"),
             "📚 Fuentes: Tratado del Atlántico Norte arts. 4-6 (nato.int) · TUE art. 42.7 · Senado 24/02/2022 · "
             "Sánchez 12/10/2026 · Gobierno 13/10 · Feijóo 14/10 · Infobae 15/10 · Maldita 15/10. ¿Ves un error? Dínoslo.",
             ["#Ceuta", "#OTAN", "#Melilla", "#Marruecos", "#politica", "#España", "#29N", "#pizarrapublica"],
             series_tag="EXPLICADO FÁCIL")
