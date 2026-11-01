#!/usr/bin/env python3
"""«Expedientado otra vez» (2/11/2026). La Junta Electoral Central obliga a retirar el vídeo de Sánchez ante el
Guernica y le abre otro expediente. Contador de expedientes y multas. Formato viral: «este vídeo ya no existe» +
contador/ranking. Neutral: versión del PP y de Moncloa, pregunta A/B al final.

Aprobado por joel el 1/11/2026 (20:47 UTC, propuesta 3 de /mnt/project-files/insta/guiones/propuestas_2nov.md).
Fuentes:
  Infobae 29/10/2026: «sexto expediente sancionador», el segundo en este periodo electoral; denunciado por el PP;
    JEC «ha ordenado la retirada del vídeo»; arts. 50.2 y 53 LOREG; frase «Cuando unos apostaban por las bombas,
    nosotros dijimos no a la guerra»; vídeo publicado el 24/10; defensa: «una reflexión sobre la posición de España
    en materia de política internacional», «no contiene mensajes electorales, peticiones de voto ni descalificaciones».
  Moncloa.com 15/10/2026 y La Región 29/10/2026: multas de 500 € (entrevista en Moncloa, ene. 2020) y 2.200 €
    (rueda de prensa en Bruselas, 2023); 2024 otra multa; expediente en las extremeñas; 6/10/2026 rueda de prensa de
    vivienda en Moncloa (expediente 15/10); «6.600 euros en multas desde enero de 2020».
  Esdiario 30/10/2026: Cayetana Álvarez de Toledo (PP), «Séptimo expediente de un tramposo reincidente».
"""
from _mundo import *  # noqa: F401,F403

OSCURO = (30, 34, 52)
PARED = (236, 226, 204)
F_INF = "Infobae, 29/10/2026"
F_MUL = "Moncloa.com 15/10 · La Región 29/10/2026"


def S(text, pausa=None):
    """Frase literal de Sánchez: voz del canal con sonido de tele (no imita su voz)."""
    return dict(V(text, "normal", pausa), efecto_voz="tele")


def bocata(lineas, at, out=None, x=540, y=520, scale=0.72, cola=(-1, 1)):
    d = obj("bocadillo", x, y, at, scale, hud=True, entra="pop", sfx="pop", props={"lineas": lineas, "cola": cola})
    if out:
        d["out"] = out
    return d


def ficha(texto, y, at, color="blanco"):
    return obj("cartel", 540, y, at, 0.9, hud=True, entra="izq", sfx="papel", props={"texto": texto, "color": color})


scenes = [
    # 1 · GANCHO: el vídeo que ya no existe
    dict(id="gancho", fondo={"tipo": "plano", "color": OSCURO}, animo="tension", footnote=F_INF, lines=[
        V("Este vídeo de Pedro Sánchez ya no existe.", "intriga"),
        V("La Junta Electoral le ha obligado a quitarlo.", "remate", 0.2),
    ], camara=[plano(0, "general", [540, 900], 0), plano("@existe", "general", [540, 860], 0.5, zoom=1.12),
               plano("@quitarlo", "general", [540, 960], 0.4)],
       elements=[
        obj("tele", 540, 780, 0, 0.95, hud=True, entra="nada", props={"texto": "SÁNCHEZ", "pantalla": (40, 70, 150)},
            acciones=[{"at": "@existe", "props": {"texto": "NO DISPONIBLE", "pantalla": (60, 60, 70)}},
                      {"at": "@Junta", "props": {"texto": "RETIRADO", "pantalla": (150, 40, 40)}}]),
        rot("24 OCT · REINA SOFÍA", 540, 440, 0.15, 64, "blanco", out="@Junta"),
        quien("sanchez", 860, "@Sánchez", 0.42, "normal", entra="der", acciones=[
            {"at": "@existe", "cara": "sorpresa", "take": True}, {"at": "@quitarlo", "cara": "serio", "pose": "encoge"}]),
        quien("piz", 220, "@vídeo", 0.42, "normal", entra="izq", acciones=[
            {"at": "@existe", "cara": "susto"}, {"at": "@obligado", "pose": "senala", "mira": "der", "cara": "sorpresa"}]),
        rot("JUNTA ELECTORAL CENTRAL", 540, 440, "@Junta", 62, "amarillo"),
        sello("RETIRADO", "rojo", 1180, "@quitarlo"),
    ]),
    # 2 · QUÉ PASÓ: el vídeo ante el Guernica
    dict(id="guernica", fondo={"tipo": "plano", "color": PARED}, animo="curioso", trans="barrido", footnote=F_INF, lines=[
        V("24 de octubre: Sánchez graba un vídeo delante del Guernica."),
        S("«Cuando unos apostaban por las bombas, nosotros dijimos no a la guerra».", 0.1),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@Guernica", "general", [540, 800], 0.6, zoom=1.08),
               plano("@Cuando", "general", [540, 960], 0.5)],
       elements=[
        obj("calendario", 820, 1000, 0, 0.36, hud=True, entra="crece", sfx="papel", out="@Guernica",
            props={"mes": "OCTUBRE 2026", "inicio": 3, "dias": 31, "marcados": [24], "colores": {24: "rojo"}}),
        obj("cartel", 540, 640, "@graba", 1.15, entra="cae", sfx="golpe", dibuja=0.8,
            props={"lineas": ["GUERNICA", "MUSEO REINA SOFÍA"], "color": "gris"}),
        quien("sanchez", -200, "@Sánchez", 0.55, "normal", acciones=[
            {"at": "@Sánchez", "x": 330, "dur": 1.0}, {"at": "@delante", "gira": True, "mira": "camara"},
            {"at": "@Cuando", "pose": "senala", "cara": "serio"}, {"at": "@bombas", "pose": "arriba"}, {"at": "@dijimos", "pose": "cruzados"}, {"at": "@guerra", "pose": "punos"}]),
        obj("movil", 820, 1200, "@vídeo", 0.55, entra="abajo", sfx="pop", props={"pantalla": "aviso", "remite": "GRABANDO",
                                                                                  "lineas": ["REC"]}),
        bocata(["SÁNCHEZ:", "«unos apostaban", "por las bombas…»"], "@Cuando", x=600, y=860, out="@nosotros"),
        bocata(["SÁNCHEZ:", "«…nosotros dijimos", "no a la guerra»"], "@nosotros", x=600, y=860),
        quien("piz", 1180, "@bombas", 0.4, "normal", entra="der", acciones=[{"at": "@bombas", "x": 900, "dur": 0.8}, {"at": "@dijimos", "cara": "pensativo", "pose": "piensa", "mira": "izq"}]),
        sello("BALANCE DEL GOBIERNO", "azul", 1240, "@guerra-0.3"),
    ]),
    # 3 · LA LEY: elecciones convocadas, denuncia del PP, expediente
    dict(id="ley", fondo="oficina", animo="tension", trans="papel", footnote=F_INF + " · LOREG arts. 50.2 y 53", lines=[
        V("Pero ya hay elecciones convocadas, y la ley prohíbe hacer campaña con lo público."),
        V("El PP lo denuncia. El 29 de octubre, la Junta abre expediente.", "normal", 0.15),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@ley", "general", [540, 820], 0.6, zoom=1.1),
               plano("@PP", "general", [540, 960], 0.5), plano("@expediente", "general", [540, 900], 0.4, zoom=1.08)],
       elements=[
        obj("urna", 820, 1180, 0, 0.6, entra="cae", sfx="golpe", props={"texto": "29N"}),
        obj("documento", 470, 760, "@ley", 0.8, hud=True, id="loreg", entra="nada", dibujo=0.9, sfx="papel", props={
            "titulo": "LEY ELECTORAL", "subtitulo": "LOREG", "ancho": 700,
            "articulos": [{"id": "a", "titulo": "ART. 50.2 Y 53", "lineas": ["neutralidad: nada de", "campaña con medios públicos"]}]},
            acciones=[{"at": "@público", "props": {"resalta": ["a"]}}], out="@PP"),
        quien("piz", 860, "@convocadas", 0.45, "pensativo", entra="der", acciones=[
            {"at": "@ley", "pose": "piensa", "mira": "loreg"}, {"at": "@prohíbe", "cara": "sorpresa"}, {"at": "@campaña", "cara": "esceptica"}], out="@PP"),
        quien("feijoo", 260, "@PP", 0.5, "serio", entra="izq", acciones=[{"at": "@denuncia", "pose": "senala", "mira": "der"}]),
        bocata(["PP:", "denuncia ante", "la Junta"], "@denuncia", x=560, y=420, out="@29"),
        obj("calendario", 760, 560, "@29", 0.34, hud=True, entra="crece", sfx="papel",
            props={"mes": "OCTUBRE 2026", "inicio": 3, "dias": 31, "marcados": [29], "colores": {29: "rojo"}}),
        sello("EXPEDIENTE ABIERTO", "rojo", 1240, "@expediente"),
    ]),
    # 4 · EL CONTADOR: no es el primero
    dict(id="contador", fondo={"tipo": "plano", "color": OSCURO}, animo="tension", trans="corte", footnote=F_MUL, lines=[
        V("Y no es el primero. Es el sexto.", "sorpresa"),
        V("2020, entrevista en la Moncloa: 500 euros. 2023, Bruselas: 2.200.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@sexto", "general", [540, 900], 0.3, zoom=1.15),
               plano("@2020", "general", [540, 960], 0.4)],
       elements=[
        obj("contador", 540, 470, "@primero", 0.62, hud=True, entra="pop", sfx="kaching", id="cuenta",
            props={"valor": 1, "sufijo": "º EXPEDIENTE", "ancho": 820},
            acciones=[{"at": "@sexto", "props": {"valor": 6, "desde": 1}, "sfx": "golpe"}]),
        quien("piz", 860, 0, 0.42, "normal", entra="nada", acciones=[
            {"at": "@sexto", "take": True, "cara": "sorpresa"}, {"at": "@500", "cara": "esceptica"},
            {"at": "@2.200", "cara": "sorpresa", "salta": True}]),
        quien("sanchez", 230, "@entrevista", 0.4, "normal", entra="izq", acciones=[
            {"at": "@Bruselas", "pose": "encoge"}]),
        ficha("2020 · MONCLOA · 500 €", 620, "@2020", "amarillo"),
        etq("500 €", 540, 760, "@500", "amarillo", 0.6, hud=True, out="@2023"),
        ficha("2023 · BRUSELAS · 2.200 €", 900, "@2023", "amarillo"),
        etq("2.200 €", 540, 1040, "@2.200", "rojo", 0.6, hud=True),
    ]),
    dict(id="contador2", fondo={"tipo": "plano", "color": OSCURO}, animo="tension", trans="corte", footnote=F_MUL, lines=[
        V("Después 2024, Extremadura, la Moncloa en octubre… y el Guernica."),
        V("Total: 6.600 euros en multas.", "remate", 0.25),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@Total", "general", [540, 1100], 0.4, zoom=1.08)],
       elements=[
        obj("contador", 540, 470, 0, 0.62, hud=True, entra="nada", props={"valor": 6, "desde": 6, "sufijo": "º EXPEDIENTE", "ancho": 820}),
        quien("piz", 860, 0, 0.42, "sorpresa", entra="nada", acciones=[
            {"at": "@Extremadura", "cara": "confundido"}, {"at": "@Guernica", "cara": "pensativo", "pose": "piensa"},
            {"at": "@6.600", "aplasta": True, "cara": "susto"}]),
        ficha("2024 · OTRA MULTA", 620, "@2024"),
        ficha("EXTREMADURA", 760, "@Extremadura"),
        ficha("6 OCT · MONCLOA", 900, "@octubre"),
        ficha("29 OCT · GUERNICA", 1040, "@Guernica", "rojo"),
        monedas("@6.600", 560, 960, 12),
        etq("6.600 € EN MULTAS", 540, 1180, "@6.600", "rojo", 0.85, hud=True, fx=[{"at": "@multas", "do": "latir"}]),
    ]),
    # 5 · LAS DOS VERSIONES: PP y Moncloa
    dict(id="versiones", fondo="calle", animo="curioso", trans="iris", footnote="Esdiario 30/10 · Infobae 29/10/2026", lines=[
        V("El PP cuenta siete: «tramposo reincidente», dice Cayetana Álvarez de Toledo."),
        V("Moncloa responde: una reflexión de política internacional, sin pedir el voto.", "normal", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@Cayetana", "general", [400, 900], 0.5, zoom=1.08),
               plano("@Moncloa", "general", [660, 960], 0.5, zoom=1.06)],
       elements=[
        obj("contador", 540, 470, 0, 0.55, hud=True, entra="pop", sfx="kaching",
            props={"valor": 6, "desde": 6, "sufijo": "º EXPEDIENTE", "ancho": 820},
            acciones=[{"at": "@siete", "props": {"valor": 7, "desde": 6, "sufijo": " SEGÚN EL PP"}, "sfx": "golpe"}], out="@Moncloa"),
        quien("piz", 800, "@PP", 0.45, "normal", entra="der", acciones=[{"at": "@siete", "take": True, "cara": "sorpresa"},
                                                                       {"at": "@tramposo", "cara": "esceptica"}], out="@Moncloa"),
        obj("movil", 300, 820, "@Cayetana", 0.75, hud=True, entra="izq", sfx="pop", props={
            "pantalla": "sms", "remite": "CAYETANA (PP)", "lineas": ["«Séptimo", "expediente de", "un tramposo", "reincidente»"]}),
        quien("sanchez", 820, "@Moncloa", 0.52, "serio", entra="der", acciones=[
            {"at": "@responde", "pose": "manos_juntas"}, {"at": "@internacional", "pose": "senala_arriba", "cara": "normal"},
            {"at": "@voto", "pose": "cruzados"}]),
        bocata(["MONCLOA:", "«sin peticiones", "de voto»"], "@reflexión", x=700, y=560, cola=(1, 1)),
        sello("DECLARACIONES", "azul", 1240, "@voto"),
    ]),
    # 6 · CIERRE: pregunta A/B y «sigue a Piz»
    dict(id="final", fondo="calle", animo="final", trans="corte", footnote=F_INF, lines=[
        V("¿Infracción o persecución? Te leo en comentarios.", "energia"),
        V("Y sigue a Piz para ver si cae otra multa.", "energia", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@sigue", "medio", "piz", 0.5, aire=300)],
       elements=[
        rot("¿INFRACCIÓN", 540, 360, 0, 96, "amarillo", golpe=True, out="@sigue-0.2"),
        rot("O PERSECUCIÓN?", 540, 470, "@persecución", 96, "amarillo", golpe=True, out="@sigue-0.2"),
        quien("piz", 540, 0, 0.62, "pensativo", entra="abajo", acciones=[
            {"at": "@Infracción", "pose": "senala_izq", "mira": "izq"}, {"at": "@persecución", "pose": "senala", "mira": "der"},
            {"at": "@leo", "pose": "piensa", "mira": "camara", "cara": "ilusionado"},
            {"at": "@sigue", "pose": "saluda", "cara": "riendo"}, {"at": "@multa", "cara": "esceptica", "pose": "jarras"}]),
        etq("A · INFRACCIÓN", 260, 760, "@leo", "rojo", 0.6, hud=True, out="@sigue"),
        etq("B · PERSECUCIÓN", 820, 760, "@leo+0.3", "azul", 0.6, hud=True, out="@sigue"),
        rot("SIGUE A PIZ", 540, 400, "@sigue", 110, "amarillo", fx=[{"at": "@multa", "do": "latir"}]),
    ]),
]

if __name__ == "__main__":
    episodio("expedientado", "Expedientado otra vez", scenes,
             {"t": 1.6, "titulo": "Expedientado otra vez", "capitulo": None},
             ["Infobae (29/10/2026): sexto expediente de la JEC a Sánchez, por el vídeo ante el Guernica; retirada del vídeo",
              "Moncloa.com (15/10/2026) y La Región (29/10/2026): expedientes anteriores y 6.600 € en multas desde 2020",
              "Esdiario (30/10/2026): Cayetana Álvarez de Toledo, «séptimo expediente»",
              "El PP cuenta siete (incluye Navantia 2024 y dic. 2025); la prensa citada cuenta seis",
              "LOREG arts. 50.2 y 53 (neutralidad institucional en periodo electoral)"],
             ("🖼️ Expedientado otra vez\n"
              "🎥 24/10: Sánchez graba un vídeo ante el Guernica\n"
              "⚖️ 29/10: la Junta Electoral ordena retirarlo y abre expediente (denuncia del PP)\n"
              "🔢 Es el sexto · 6.600 € en multas desde 2020\n"
              "🗣️ PP: «tramposo reincidente» · Moncloa: «sin peticiones de voto»\n"
              "💬 ¿Infracción o persecución? A o B 👇\n"
              "🔔 Sigue a Piz para no perderte nada antes del 29N · 📚 Fuentes en comentarios"),
             "📚 Fuentes: Infobae 29/10/2026 · Moncloa.com 15/10 · La Región 29/10 · Esdiario 30/10 · LOREG arts. 50.2 y 53. "
             "El PP cuenta siete expedientes; la prensa citada, seis. ¿Ves un error? Dínoslo.",
             ["#PedroSanchez", "#JuntaElectoral", "#Guernica", "#29N", "#EleccionesGenerales", "#pizarrapublica"],
             series_tag="EXPLICADO FÁCIL")
