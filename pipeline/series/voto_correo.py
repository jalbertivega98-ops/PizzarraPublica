#!/usr/bin/env python3
"""«Voto por correo: las 3 fechas que no te puedes saltar» (lunes 19/10/2026, 20:00). Mundo dibujado: el viaje del sobre.

Guion y fuentes: /mnt/project-files/insta/guiones/lunes_martes_19_20oct.md
  La Moncloa / Interior: solicitud hasta el 19/11 (Correos o en línea con DNIe o certificado), documentación desde el 9/11,
    envío por correo certificado gratuito antes del 25/11 identificándose con el DNI; residentes temporales en el extranjero:
    solicitud en el consulado hasta el 31/10.
  Infobae 18/10/2026: no meter ningún documento de identidad dentro del sobre de votación (se anula).
"""
from _mundo import *  # noqa: F401,F403

R = "espana"
MAD = P(R, -3.7, 40.4)
SEV = P(R, -6.0, 37.4)
FMON = "La Moncloa / Ministerio del Interior · Infobae 18/10/2026"


def cal(at, marcados, colores=None, tachados=(), y=470, s=0.42, **kw):
    return obj("calendario", 540, y, at, s, hud=True, entra="nada", dibuja=0.8,
               props={"marcados": marcados, "colores": colores or {}, "tachados": list(tachados)}, **kw)


scenes = [
    # 1 · GANCHO: Piz con la maleta; el 29 tachado en el calendario
    dict(id="gancho", fondo="calle", animo="aventura", footnote=FMON, lines=[
        V("¿El 29N no vas a estar?", "energia"),
        V("Puedes votar sin pisar el colegio… si no te saltas tres fechas.", "normal", 0.1),
        V("Y al final te hago una pregunta.", "normal", 0.1),
    ], camara=[plano(0, "medio", "piz", 0, aire=220), plano("@votar", "general", [540, 1000], 0.6),
               plano("@tres", "general", [540, 900], 0.4, zoom=1.06), plano("@pregunta", "medio", "piz", 0.5, aire=200)],
       elements=[
        quien("piz", 400, 0, 0.6, "preocupado", entra="nada", objeto="maleta", pose="sostiene", acciones=[
            {"at": "@estar", "mira": "camara"}, {"at": "@votar", "cara": "ilusionado", "salta": True},
            {"at": "@tres", "cara": "sorpresa", "take": True}, {"at": "@pregunta", "pose": "senala", "cara": "riendo", "mira": "camara"}]),
        cal("@estar", [], tachados=[29], y=520, s=0.5),
        rot("3 FECHAS", 540, 1080, "@tres", 120, "amarillo", golpe=True),
        obj("avion", 1250, 380, "@colegio", 0.5, entra="nada", acciones=[{"at": "@colegio", "x": -200, "dur": 2.2}]),
    ]),
    # 2 · FECHA UNO: hasta el 19 de noviembre, en Correos o por internet
    dict(id="fecha1", fondo="calle", animo="curioso", trans="barrido", footnote="La Moncloa / Interior: plazo de solicitud", lines=[
        V("Fecha uno: hasta el 19 de noviembre para pedirlo,", "normal"),
        V("en Correos o por internet con DNI electrónico o certificado digital.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 900], 0), plano("@Correos", "general", [700, 1050], 0.6),
               plano("@internet", "general", [540, 1000], 0.5)],
       elements=[
        cal(0, [19], {19: "rojo"}),
        obj("cartel", 800, 1000, "@Correos-0.3", 1.1, entra="crece", sfx="pop", dibuja=0.8,
            props={"texto": "CORREOS", "color": "amarillo"}),
        quien("piz", 200, 0, 0.5, "ilusionado", entra="nada", acciones=[
            {"at": "@pedirlo", "x": 560, "dur": 0.9}, {"at": "@Correos", "pose": "senala", "mira": "der"},
            {"at": "@internet", "objeto": "movil", "pose": "sostiene", "cara": "idea"}]),
        rot("1 · HASTA EL 19N", 540, 760, "@19", 92, "amarillo", golpe=True),
        etq("DNIe O CERTIFICADO", 540, 1180, "@electrónico", "verde", 0.7, hud=True),
    ]),
    # 3 · FECHA DOS: desde el 9 de noviembre el camión trae las papeletas por el mapa
    dict(id="fecha2", fondo="mar_mapa", limites=LIM, animo="aventura", trans="zoom", footnote="La Moncloa / Interior: envío de la documentación",
         lines=[V("Fecha dos: desde el 9 de noviembre te llegan a casa las papeletas y los sobres.", "normal")],
       camara=[zoom(0, MAD, 1.0, 0), zoom("@llegan", P(R, -4.9, 38.9), 1.6, 1.0), zoom("@sobres", SEV, 2.0, 0.6)],
       elements=[
        mapa(R, 0, 1.2),
        obj("camion", MAD[0], MAD[1] + 10, 0.3, 0.16, id="camion", entra="pop", sfx="bocina",
            props={"texto": "CORREOS", "color": "amarillo"},
            acciones=[{"at": "@llegan", "x": SEV[0], "y": SEV[1] + 10, "dur": 1.6}]),
        quien("piz", SEV[0] + 60, "@casa", 0.17, "ilusionado", y=SEV[1] + 40, entra="cae", acciones=[
            {"at": "@papeletas", "salta": True, "cara": "riendo"}]),
        obj("papeleta", SEV[0] - 40, SEV[1] - 70, "@sobres", 0.18, entra="pop", sfx="papel", flota=True),
        rot("2 · DESDE EL 9N", 540, 1180, "@9", 92, "amarillo", golpe=True, hud=True),
    ]),
    # 4 · FECHA TRES: certificado, gratis, con DNI, antes del 25
    dict(id="fecha3", fondo="calle", animo="curioso", trans="pan", footnote="La Moncloa / Interior: envío del voto", lines=[
        V("Fecha tres: envíalo por correo certificado antes del 25 de noviembre.", "normal"),
        V("Es gratis, y tienes que llevar tu DNI.", "normal", 0.15),
    ], camara=[plano(0, "general", [540, 900], 0), plano("@gratis", "medio", "piz", 0.5, aire=220), plano("@DNI", "general", [600, 1000], 0.5)],
       elements=[
        cal(0, [9, 19, 25], {9: "verde", 19: "verde", 25: "rojo"}),
        obj("cartel", 800, 1000, 0, 1.1, entra="nada", props={"texto": "CORREOS", "color": "amarillo"}),
        quien("piz", 420, 0, 0.5, "ilusionado", entra="nada", objeto="papeleta", pose="sostiene", acciones=[
            {"at": "@certificado", "x": 600, "dur": 0.7}, {"at": "@gratis", "cara": "riendo", "salta": True},
            {"at": "@DNI", "pose": "senala", "objeto": None, "mira": "der"}]),
        rot("3 · ANTES DEL 25N", 540, 760, "@25", 92, "amarillo", golpe=True),
        etq("GRATIS", 300, 1150, "@gratis", "verde", 0.8, hud=True),
        etq("DNI", 780, 1150, "@DNI", "amarillo", 0.8, hud=True),
    ]),
    # 5 · EL TRUCO: el DNI dentro del sobre anula el voto
    dict(id="truco", fondo={"tipo": "plano", "color": (28, 52, 110)}, animo="comico", trans="iris", footnote="Infobae 18/10/2026", lines=[
        V("Truco: dentro del sobre, nunca metas tu DNI…", "normal"),
        V("o el voto se anula.", "remate", 0.1),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@anula", "general", [540, 900], 0.3, zoom=1.1)],
       elements=[
        obj("papeleta", 540, 760, 0, 1.4, id="sobre", entra="pop", sfx="papel", props={"texto": "VOTO"}),
        etq("DNI", 900, 520, "@DNI", "amarillo", 0.9, acciones=[{"at": "@anula-0.6", "x": 560, "y": 740, "dur": 0.5}]),
        quien("critica", 230, 0, 0.5, "esceptica", y=1500, entra="nada", acciones=[
            {"at": "@nunca", "pose": "senala", "mira": "sobre", "cara": "indignado"}, {"at": "@anula", "pose": "cabeza", "cara": "susto"}]),
        sello("VOTO NULO", "rojo", 1100, "@anula"),
    ]),
    # 6 · FUERA DE ESPAÑA: consulado y 31 de octubre en el mapa del mundo
    dict(id="fuera", fondo="mar_mapa", limites=LIM, animo="tension", trans="zoom",
         footnote="La Moncloa / Interior: españoles temporalmente en el extranjero", lines=[
        V("¿Estás fuera de España de forma temporal?", "normal"),
        V("Ojo: tu plazo para pedirlo acaba el 31 de octubre, en el consulado.", "normal", 0.1),
    ], camara=[zoom(0, P("mundo", -3.7, 40.4), 1.0, 0), zoom("@Ojo", P("mundo", 5, 48), 2.2, 1.0)],
       elements=[
        mapa("mundo", 0, 1.2, resalta=["ESP"]),
        quien("piz", P("mundo", 13.4, 52.5)[0], "@fuera", 0.1, "preocupado", y=P("mundo", 13.4, 52.5)[1] + 20, entra="cae",
              objeto="maleta", pose="sostiene", acciones=[{"at": "@Ojo", "cara": "susto", "take": True}]),
        obj("chincheta", P("mundo", 13.4, 52.5)[0], P("mundo", 13.4, 52.5)[1] - 40, "@consulado", 0.05, entra="cae",
            props={"diseno": "espana"}),
        rot("HASTA EL 31 DE OCTUBRE", 540, 1180, "@31", 84, "amarillo", golpe=True, hud=True),
    ]),
    # 7 · PREGUNTA: ¿correo o colegio?
    dict(id="pregunta", fondo="colegio", animo="final", trans="iris", footnote="Pregunta a la audiencia", lines=[
        V("Y ahora tú: ¿votarías por correo, o prefieres ir al colegio en persona?", "normal"),
        V("Escribe CORREO o COLEGIO en comentarios.", "energia", 0.1),
        V("Compártelo con quien no vaya a estar el 29N. Y síguenos.", "normal", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@CORREO", "general", [540, 900], 0.4, zoom=1.06),
               plano("@Compártelo", "medio", "piz", 0.5, aire=220), plano("@síguenos", "general", [540, 1000], 0.4)],
       elements=[
        obj("urna", 830, 1080, 0, 0.75, entra="nada", props={"llena": 0.4, "texto": "COLEGIO"}),
        obj("papeleta", 240, 1000, 0, 1.4, entra="nada", props={"texto": "CORREO"}, flota=True),
        quien("piz", 540, 0, 0.55, "confundido", entra="nada", acciones=[
            {"at": "@correo", "mira": "izq", "pose": "piensa"}, {"at": "@colegio", "mira": "der"},
            {"at": "@Escribe", "mira": "camara", "cara": "ilusionado", "pose": "senala"},
            {"at": "@Compártelo", "cara": "riendo", "pose": "saluda"}, {"at": "@29N", "salta": True, "cara": "ilusionado"},
            {"at": "@síguenos", "salta": True}]),
        rot("¿CORREO O COLEGIO?", 540, 480, "@Escribe", 96, "amarillo", golpe=True, out="@síguenos-0.3", fx=[{"at": "@comentarios", "do": "latir"}]),
        rot("SÍGUENOS", 540, 480, "@síguenos", 110, "amarillo"),
    ]),
]

if __name__ == "__main__":
    episodio("voto_correo", "Voto por correo: las 3 fechas", scenes,
             {"t": 3.2, "titulo": "Voto por correo: las 3 fechas", "capitulo": None},
             ["La Moncloa / Ministerio del Interior: cómo solicitar el voto por correo en las elecciones generales del 29N",
              "Infobae (18/10/2026): fechas, documentos y pasos del voto por correo",
              "Mapas dibujados sobre contornos de Natural Earth (dominio público)"],
             ("✈️ ¿El 29N no vas a estar? Puedes votar por correo\n"
              "1️⃣ Hasta el 19 de noviembre: pídelo en Correos o por internet (DNIe o certificado)\n"
              "2️⃣ Desde el 9 de noviembre: te llegan las papeletas a casa\n"
              "3️⃣ Antes del 25 de noviembre: envíalo certificado (gratis, con tu DNI)\n"
              "⚠️ Nunca metas el DNI dentro del sobre: el voto se anula\n"
              "🌍 ¿Fuera de España temporalmente? Hasta el 31 de octubre en el consulado\n"
              "💬 ¿CORREO o COLEGIO? Te leemos 👇\n"
              "🔔 Síguenos · 📚 Fuentes en comentarios"),
             "📚 Fuentes: La Moncloa / Ministerio del Interior (voto por correo 29N) · Infobae 18/10/2026. ¿Ves un error? Dínoslo.",
             ["#29N", "#VotoPorCorreo", "#elecciones", "#EleccionesGenerales", "#Correos", "#politica", "#España", "#pizarrapublica"],
             series_tag="EXPLICADO FÁCIL")
