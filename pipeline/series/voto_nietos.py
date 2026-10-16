#!/usr/bin/env python3
"""«Los 163.020 que no podrán votar el 29N» (16/10/2026). Mundo dibujado: viaje por el mapa del mundo.

Guion y fuentes: docs/series/cinco_mundo/guiones.md · investigación: /mnt/project-files/insta/investigacion/temas5_mundo.md
  Ley 20/2022 de Memoria Democrática, disp. adicional 8ª. Solicitudes: 1,2 millones de expedientes (Albares, El Español
    29/04/2026); por consulado: Argentina 462.815, São Paulo +150.000, La Habana 137.770, México ~120.000.
  CERA: 2.328.260 (2023) → 2.736.522 (1/7/2026) (Diario Constitucional 15/09/2026, auto del Supremo).
  Supremo, Sala 3ª: suspensión cautelar de los efectos electorales de su inscripción en el CERA (septiembre), pedida
    por Vox e Iustitia Europa; no anula nacionalidades; quien acredite exilio queda fuera. 12/10/2026: rechaza el
    recurso de la Abogacía del Estado (RTVC 12/10). 163.020 afectados (Abogacía del Estado, Xataka 09/10).
  Posturas: PSOE (Mínguez, Orain 13/10) «no la comparte pero la acata»; PP (Feijóo, 12/10) «no puede haber dudas sobre
    el censo»; Vox (Buxadé, 12/10) «el Supremo ha hecho justicia».
"""
from _mundo import *  # noqa: F401,F403

R = "mundo"
MAD = P(R, -3.7, 40.4)
BSAS = P(R, -58.4, -34.6)
SPAULO = P(R, -46.6, -23.5)
HABANA = P(R, -82.4, 23.1)
MEXICO = P(R, -99.1, 19.4)
ATL = P(R, -40, 8)
RUTAS = [("arg", (-58.4, -34.6)), ("bra", (-46.6, -23.5)), ("cub", (-82.4, 23.1)), ("mex", (-99.1, 19.4))]
FLEY = "Ley 20/2022 de Memoria Democrática, disp. adicional 8ª"
FSUP = "Tribunal Supremo, Sala 3ª · RTVC 12/10/2026 · Abogacía del Estado"


def ruta(id, desde, dur=1.1):
    lon, lat = desde
    medio = ((lon + -3.7) / 2, (lat + 40.4) / 2 + 9)
    return linea(id, [(lon, lat), medio, (-3.7, 40.4)], "rojo", dur, discontinua=True, ancho=6)


scenes = [
    # 1 · GANCHO: el mapa del mundo se dibuja, zoom a Argentina, Piz con su pasaporte… y la urna se cierra
    dict(id="gancho", fondo="mar_mapa", limites=LIM, animo="tension", footnote=FSUP, lines=[
        V("Hay 163.020 personas con pasaporte español recién estrenado que el 29N no podrán votar.", "energia"),
        V("Al menos, de momento.", "remate", 0.2),
    ], camara=[zoom(0, ATL, 1.0, 0), zoom("@personas", BSAS, 4.2, 1.0), zoom("@29N", [BSAS[0] + 30, BSAS[1] - 20], 5.5, 0.6),
               zoom("@momento", [BSAS[0] + 20, BSAS[1] - 10], 4.6, 0.6)],
       elements=[
        mapa(R, 0, 1.6, acciones=[{"at": "@personas", "props": {"resalta": ["ARG"]}, "sfx": "pop"}]),
        quien("piz", BSAS[0] - 26, "@pasaporte-0.3", 0.1, "ilusionado", y=BSAS[1] + 8, entra="cae",
              objeto="pasaporte", pose="sostiene", acciones=[
                  {"at": "@podrán", "cara": "sorpresa", "take": True, "mira": "urna"},
                  {"at": "@momento", "cara": "preocupado", "pose": "encoge", "objeto": None, "mira": "camara"}]),
        obj("urna", BSAS[0] + 50, BSAS[1] - 12, "@29N-0.2", 0.085, id="urna", entra="crece", sfx="pop",
            props={"llena": 0.3, "texto": "29N"}),
        rot("163.020", 540, 430, "@163.020", 140, "amarillo", golpe=True),
        rot("SIN VOTO EL 29N", 540, 560, "@votar", 80, "blanco", golpe=True),
        sello("EN PAUSA", "rojo", 700, "@momento"),
    ]),
    # 2 · LA LEY: el pergamino de la ley de nietos y el contador de solicitudes
    dict(id="ley", fondo={"tipo": "plano", "color": (28, 52, 110)}, animo="curioso", trans="papel", footnote=FLEY, lines=[
        V("En 2022, la Ley de Memoria Democrática dejó pedir la nacionalidad a hijos y nietos de españoles, nacidos fuera.", "normal"),
        V("Se presentaron 1,2 millones de solicitudes.", "normal", 0.15),
    ], camara=[plano(0, "general", [540, 820], 0), plano("@hijos", "general", [540, 760], 0.6, zoom=1.12),
               plano("@1,2", "general", [540, 900], 0.6)],
       elements=[
        obj("documento", 540, 840, 0.2, 1.3, id="doc", entra="nada", dibujo=1.0, sfx="papel", props={
            "titulo": "LEY DE MEMORIA DEMOCRÁTICA", "subtitulo": "Ley 20/2022 · disposición adicional 8ª",
            "articulos": [{"id": "da8", "titulo": "LA «LEY DE NIETOS»",
                           "lineas": ["Hijos y nietos de españoles,", "nacidos fuera de España,", "pueden pedir la nacionalidad"]}]},
            out="@1,2", acciones=[{"at": "@hijos", "props": {"resalta": ["da8"]}}]),
        quien("piz", 1300, "@nacionalidad-0.5", 0.45, "ilusionado", y=1560, entra="nada", objeto="pasaporte", pose="sostiene",
              acciones=[{"at": "@nacionalidad-0.5", "x": 900, "dur": 0.6}, {"at": "@nacionalidad", "salta": True, "cara": "riendo"},
                        {"at": "@solicitudes", "cara": "sorpresa", "take": True, "objeto": None, "pose": "cabeza"}]),
        obj("contador", 540, 760, "@1,2", 1.0, hud=True, entra="pop", sfx="kaching",
            props={"valor": 1200000, "sufijo": "", "ancho": 820}),
        rot("SOLICITUDES", 540, 560, "@1,2", 80, "blanco", golpe=True),
        dict(type="efecto", efecto="lluvia", objeto="papeleta", n=12, x0=150, x1=930, at="@solicitudes", vida=1.8),
    ]),
    # 3 · EL VIAJE: de América a España, rutas dibujadas y banderas con las cifras por consulado
    dict(id="viaje", fondo="mar_mapa", limites=LIM, animo="aventura", trans="zoom",
         footnote="Solicitudes por consulado a 31/3/2026 · Albares (El Español, 29/04/2026)", lines=[
        V("La mayoría, desde América: casi 463.000 en Argentina, más de 150.000 en São Paulo…", "normal"),
        V("casi 138.000 en Cuba y unas 120.000 en México.", "normal", 0.05),
    ], camara=[zoom(0, P(R, -50, -15), 2.4, 0), zoom("@São", P(R, -48, -20), 3.0, 0.7), zoom("@Cuba", P(R, -88, 22), 3.0, 0.8),
               zoom("@México+0.6", P(R, -45, 15), 1.15, 1.2)],
       elements=[
        mapa(R, 0, 0.01, progreso=1.0, resalta=["ARG"], acciones=[
            {"at": "@Argentina", "props": {"lineas": [ruta("arg", RUTAS[0][1])]}, "sfx": "rotulador"},
            {"at": "@São", "props": {"resalta": ["ARG", "BRA"], "lineas": [ruta("arg", RUTAS[0][1]), ruta("bra", RUTAS[1][1])]}, "sfx": "rotulador"},
            {"at": "@Cuba", "props": {"resalta": ["ARG", "BRA", "CUB"], "lineas": [ruta(i, p) for i, p in RUTAS[:3]]}, "sfx": "rotulador"},
            {"at": "@México", "props": {"resalta": ["ARG", "BRA", "CUB", "MEX", "ESP"], "lineas": [ruta(i, p) for i, p in RUTAS]}, "sfx": "rotulador"}]),
        obj("chincheta", BSAS[0], BSAS[1], "@Argentina", 0.3, props={"diseno": "argentina"}, entra="cae"),
        obj("chincheta", SPAULO[0], SPAULO[1], "@São", 0.3, props={"diseno": "brasil"}, entra="cae"),
        obj("chincheta", HABANA[0], HABANA[1], "@Cuba", 0.3, props={"diseno": "cuba"}, entra="cae"),
        obj("chincheta", MEXICO[0], MEXICO[1], "@México", 0.3, props={"diseno": "mexico"}, entra="cae"),
        obj("chincheta", MAD[0], MAD[1], "@México+0.4", 0.3, props={"diseno": "espana"}, entra="cae"),
        obj("avion", BSAS[0] + 10, BSAS[1] - 20, "@Argentina", 0.1, id="avion", entra="pop", flota=True,
            acciones=[{"at": "@Argentina+0.1", "x": SPAULO[0] + 30, "y": SPAULO[1] - 40, "dur": 1.6},
                      {"at": "@Cuba-0.3", "x": HABANA[0] + 40, "y": HABANA[1] - 30, "dur": 1.2},
                      {"at": "@México+0.3", "x": MAD[0] - 60, "y": MAD[1] - 20, "dur": 1.6}]),
        quien("piz", BSAS[0] + 30, 0, 0.12, "ilusionado", y=BSAS[1] + 10, entra="nada", acciones=[
            {"at": "@São-0.3", "x": SPAULO[0] - 10, "y": SPAULO[1] + 8, "dur": 0.6, "brinco": 40, "cara": "riendo"},
            {"at": "@Cuba-0.2", "x": HABANA[0] + 10, "y": HABANA[1] + 8, "dur": 0.7, "brinco": 60},
            {"at": "@México-0.2", "x": MEXICO[0] + 6, "y": MEXICO[1] + 8, "dur": 0.5, "brinco": 30, "cara": "sorpresa"}]),
        rot("ARGENTINA · 462.815", 540, 430, "@Argentina", 70, "amarillo", golpe=True, out="@São"),
        rot("SÃO PAULO · +150.000", 540, 430, "@São", 70, "amarillo", golpe=True, out="@Cuba"),
        rot("CUBA · 137.770", 540, 430, "@Cuba", 70, "amarillo", golpe=True, out="@México"),
        rot("MÉXICO · ~120.000", 540, 430, "@México", 70, "amarillo", golpe=True),
    ]),
    # 4 · EL CENSO: el contador del censo de españoles en el extranjero se dispara; la urna se llena
    dict(id="censo", fondo="colegio", animo="tension", trans="iris",
         footnote="CERA: 2.328.260 (2023) → 2.736.522 (1/7/2026) · auto del Supremo", lines=[
        V("Y el censo de españoles que votan desde fuera se disparó: más de 400.000 electores nuevos desde 2023.", "normal"),
    ], camara=[plano(0, "general", [540, 900], 0), plano("@disparó", "medio", "urna", 0.6, aire=200),
               plano("@400.000", "general", [540, 900], 0.5)],
       elements=[
        obj("urna", 540, 1120, 0, 0.9, id="urna", entra="cae", sfx="golpe", props={"llena": 0.25, "texto": "EXTRANJERO"},
            acciones=[{"at": "@disparó", "props": {"llena": 0.7}, "tiembla": True}, {"at": "@400.000", "props": {"llena": 1.0}, "salta": True}]),
        dict(type="efecto", efecto="lluvia", objeto="papeleta", n=16, x0=300, x1=780, at="@disparó", vida=1.6),
        quien("pizon", 180, 0.2, 0.6, "normal", entra="izq", acciones=[{"at": "@disparó", "cara": "sorpresa", "take": True, "mira": "urna"}]),
        quien("critica", 900, 0.4, 0.6, "normal", entra="der", acciones=[{"at": "@400.000", "cara": "susto", "pose": "cabeza"}]),
        obj("contador", 540, 520, "@españoles", 0.9, hud=True, entra="pop", dibujo=2.6,
            props={"valor": 2736522, "ancho": 800}),
        rot("+408.262", 540, 700, "@400.000", 110, "amarillo", golpe=True, rot=-4),
    ]),
    # 5 · EL SUPREMO: la jueza, el sello cautelar y el «no» al Gobierno
    dict(id="supremo", fondo={"tipo": "plano", "color": (110, 40, 52)}, animo="tension", trans="corte", footnote=FSUP, lines=[
        V("Vox y la asociación Iustitia Europa fueron al Supremo, que en septiembre suspendió ese voto de forma cautelar.", "normal"),
        V("El Gobierno recurrió y, el 12 de octubre, el Supremo dijo que no.", "normal", 0.15),
        V("Ojo: nadie pierde la nacionalidad, y quien acredite exilio sí vota.", "remate", 0.2),
    ], camara=[plano(0, "general", [540, 900], 0), plano("@cautelar", "medio", "jueza", 0.5, aire=160),
               plano("@Gobierno", "general", [540, 900], 0.5), plano("@Ojo", "medio", "piz", 0.5, aire=200)],
       elements=[
        quien("jueza", 300, 0, 0.8, "serio", entra="pop", acciones=[
            {"at": "@suspendió", "pose": "senala_arriba", "cara": "serio"}, {"at": "@no", "pose": "jarras", "cara": "serio"}]),
        obj("pergamino", 790, 900, "@Supremo", 0.62, entra="abajo", sfx="papel", out="@Ojo",
            props={"titulo": "AUTO DEL SUPREMO", "fecha": "Sala 3ª · 2026", "lineas": ["Se suspende", "el voto de los", "nacionalizados", "(cautelar)"]}),
        sello("SUSPENSIÓN CAUTELAR", "rojo", 440, "@suspendió", out="@Gobierno"),
        sello("RECURSO DEL GOBIERNO: NO", "rojo", 440, "@no", out="@Ojo"),
        quien("piz", 1250, "@Ojo-0.5", 0.5, "normal", entra="nada", acciones=[
            {"at": "@Ojo-0.5", "x": 860, "dur": 0.5}, {"at": "@nacionalidad", "pose": "pulgar", "cara": "riendo", "objeto": "pasaporte"},
            {"at": "@exilio", "pose": "senala_arriba", "cara": "idea"}]),
        sello("NACIONALIDAD: SE MANTIENE", "verde", 440, "@nacionalidad"),
        rot("CON EXILIO ACREDITADO, SÍ VOTA", 540, 560, "@exilio", 54, "blanco", golpe=True),
    ]),
    # 6 · LAS POSTURAS: tres atriles, una frase documentada cada uno
    dict(id="posturas", fondo="calle", animo="curioso", trans="iris",
         footnote="PSOE: Mínguez (13/10) · PP: Feijóo (12/10) · Vox: Buxadé (12/10)", lines=[
        V("El PSOE no comparte la decisión, pero la acata.", "normal"),
        V("El PP dice que no puede haber dudas sobre el censo.", "normal", 0.1),
        V("Y Vox, que el Supremo ha hecho justicia.", "normal", 0.1),
    ], camara=[plano(0, "general", dur=0), plano("@PSOE", "medio", "p1", 0.5), plano("@PP", "medio", "p2", 0.5),
               plano("@Vox", "medio", "p3", 0.5), plano("@justicia+0.4", "general", dur=0.6)],
       elements=[
        quien("diputado", 230, 0, 0.55, "normal", id="p1", entra="pop", acciones=[
            {"at": "@comparte", "pose": "cruzados", "cara": "esceptica"}, {"at": "@acata", "pose": "encoge", "cara": "serio"}]),
        quien("diputado", 540, 0.15, 0.55, "normal", id="p2", entra="pop", acciones=[{"at": "@dudas", "pose": "senala_arriba", "cara": "serio"}]),
        quien("diputado", 850, 0.3, 0.55, "normal", id="p3", entra="pop", acciones=[{"at": "@justicia", "pose": "puno", "cara": "riendo"}]),
        *atriles(),
        rot("PSOE: «LA ACATAMOS»", 540, 450, "@acata", 66, "blanco", golpe=True, out="@PP"),
        rot("PP: «SIN DUDAS SOBRE EL CENSO»", 540, 450, "@censo", 56, "blanco", golpe=True, out="@Vox"),
        rot("VOX: «SE HA HECHO JUSTICIA»", 540, 450, "@justicia", 58, "blanco", golpe=True),
    ]),
    # 7 · FINAL: zoom out del mundo con las rutas; Piz pregunta
    dict(id="final", fondo="mar_mapa", limites=LIM, animo="final", trans="zoom", footnote="Te leemos en comentarios", lines=[
        V("¿Deberían poder votar el 29N? Te leo.", "normal"),
        V("Y síguenos para el próximo viaje de Piz.", "energia", 0.15),
    ], camara=[zoom(0, MAD, 5.0, 0), zoom(0.2, ATL, 1.0, 2.2)],
       elements=[
        mapa(R, 0, 0.01, progreso=1.0, resalta=["ESP", "ARG", "BRA", "CUB", "MEX"],
             lineas=[ruta(i, p, 0.01) for i, p in RUTAS]),
        quien("piz", 790, "@Deberían", 0.6, "pensativo", y=1500, hud=True, entra="abajo", acciones=[
            {"at": "@votar", "pose": "senala_izq"}, {"at": "@leo", "mira": "camara", "cara": "ilusionado"},
            {"at": "@síguenos", "pose": "saluda", "cara": "riendo"}, {"at": "@viaje", "salta": True}]),
        rot("¿SÍ O NO?", 540, 450, "@29N", 120, "amarillo", golpe=True, out="@síguenos-0.3"),
        rot("SÍGUENOS", 540, 450, "@síguenos", 110, "amarillo", fx=[{"at": "@Piz", "do": "latir"}]),
    ]),
]

if __name__ == "__main__":
    episodio("voto_nietos", "Los 163.020 que no podrán votar el 29N", scenes,
             {"t": 2.4, "titulo": "Los 163.020 que no podrán votar el 29N", "capitulo": None},
             ["Ley 20/2022 de Memoria Democrática, disposición adicional 8ª (BOE)",
              "Albares: 1,2 millones de expedientes y solicitudes por consulado (El Español, 29/04/2026)",
              "Auto del Tribunal Supremo, Sala 3ª, septiembre de 2026 (LegalToday/Europa Press 08/09; Diario Constitucional 15/09)",
              "El Supremo rechaza el recurso de la Abogacía del Estado (RTVC, 12/10/2026)",
              "163.020 afectados según la Abogacía del Estado (Xataka, 09/10/2026)",
              "Reacciones: Orain 13/10/2026; Moncloa.com 12/10/2026",
              "Mapas dibujados sobre contornos de Natural Earth (dominio público)"],
             ("🌎 163.020 españoles nuevos no podrán votar el 29N (de momento)\n"
              "📜 La ley de nietos (2022) abrió la nacionalidad a hijos y nietos de españoles nacidos fuera\n"
              "✈️ 1,2 millones de solicitudes: Argentina, Brasil, Cuba, México…\n"
              "⚖️ El Supremo suspendió su voto de forma cautelar y el 12/10 rechazó el recurso del Gobierno\n"
              "🛂 Nadie pierde la nacionalidad, y quien acredite exilio sí vota\n"
              "💬 ¿Deberían poder votar el 29N?\n"
              "🔔 Síguenos · 📚 Fuentes en comentarios"),
             "📚 Fuentes: Ley 20/2022 (BOE) · Albares en El Español 29/04/2026 · Supremo (LegalToday 08/09, RTVC 12/10) · "
             "Abogacía del Estado (Xataka 09/10) · Orain 13/10 · Moncloa.com 12/10. ¿Ves un error? Dínoslo.",
             ["#leydenietos", "#29N", "#elecciones", "#nacionalidad", "#Argentina", "#Cuba", "#politica", "#pizarrapublica"],
             series_tag="EXPLICADO FÁCIL")
