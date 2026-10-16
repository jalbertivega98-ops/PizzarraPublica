#!/usr/bin/env python3
"""«Las leyes que mueren el 29N» (16/10/2026). Mundo dibujado: el Congreso, una carretera y un cementerio de leyes.

Guion y fuentes: docs/series/cinco_mundo/guiones.md · investigación: /mnt/project-files/insta/investigacion/temas5_mundo.md
  Real Decreto 806/2026, de 5 de octubre (BOE 06/10/2026): disolución; nuevas Cortes el 23/12/2026.
  Reglamento del Congreso, art. 207: «quedarán caducados todos los asuntos pendientes…» (congreso.es).
  Cuántas: 309 (89 proyectos + 220 proposiciones), recuento de Civio citado por LegalToday 12/10/2026 → «unas 300».
  Alcohol: proposición del PSOE 0,5 → 0,2 g/l; tomada en consideración a finales de septiembre de 2026 por 173 a 168,
    con PP, Vox y UPN en contra (Motor16 11/10, Carwow 08/10). Decae.
  Velocidad: umbral del delito de +60 a +50 km/h en ciudad (delito desde 101 en una vía de 50; hoy desde 111) y de
    +80 a +70 en interurbanas (Carwow 08/10/2026). Decae.
  Otras: LO de Integridad Pública (prescripción de 5 a 7 años), nueva LECrim (instrucción al fiscal), ley de lobbies,
    condonación de deuda autonómica (LegalToday 12/10, Voz de la Verdad 05/10, Gaceta del Opositor 05/10).
"""
from _mundo import *  # noqa: F401,F403
from _tu_dinero import edif  # noqa: E402

FDIS = "Real Decreto 806/2026 (BOE 06/10/2026) · Civio vía LegalToday 12/10/2026"
FALC = "Proposición de ley del PSOE · Motor16 11/10/2026 · Carwow 08/10/2026"


def tumba(x, at, lineas, scale=0.5, **kw):
    return obj("lapida", x, 1360, at, scale, props={"texto": "R.I.P.", "lineas": lineas}, entra="abajo", sfx="golpe", **kw)


scenes = [
    # 1 · GANCHO: delante del Congreso brotan lápidas; Piz se asusta
    dict(id="gancho", fondo="calle", animo="tension", footnote=FDIS, lines=[
        V("El 6 de octubre murieron unas 300 leyes a medio hacer.", "energia"),
        V("Y dos te afectaban al volante.", "remate", 0.2),
    ], camara=[plano(0, "general", [540, 900], 0), plano("@murieron", "general", [540, 1050], 0.5, zoom=1.12),
               plano("@volante", "medio", "piz", 0.5, aire=180)],
       elements=[
        edif("congreso", 540, 0, 0.8, entra="nada", acciones=[{"at": "@murieron", "cara": "triste"}]),
        tumba(170, "@murieron", ["LEY"], 0.48),
        tumba(400, "@unas", ["LEY"], 0.48),
        tumba(680, "@300", ["LEY"], 0.48),
        tumba(910, "@leyes", ["LEY"], 0.48),
        quien("piz", -150, 0, 0.6, "normal", entra="nada", acciones=[
            {"at": 0.2, "x": 260, "dur": 1.0}, {"at": "@murieron", "cara": "susto", "take": True, "mira": "der"},
            {"at": "@volante", "pose": "senala", "mira": "camara", "cara": "sorpresa"}]),
        rot("~300 LEYES", 540, 420, "@300", 120, "amarillo", golpe=True),
        rot("A MEDIO HACER", 540, 540, "@medio", 80, "blanco", golpe=True),
        obj("coche", 860, 1250, "@volante", 0.6, entra="der", sfx="bocina", props={"color": "azul", "cara": "susto"}),
    ]),
    # 2 · POR QUÉ: el reglamento del Congreso, artículo 207
    dict(id="porque", fondo={"tipo": "plano", "color": (28, 52, 110)}, animo="curioso", trans="papel",
         footnote="Reglamento del Congreso, art. 207 · RD 806/2026", lines=[
        V("Al disolver las Cortes para el 29N, el Reglamento del Congreso es claro: todo lo pendiente caduca.", "normal"),
    ], camara=[plano(0, "general", [540, 820], 0), plano("@caduca", "general", [540, 760], 0.5, zoom=1.12)],
       elements=[
        obj("documento", 540, 800, 0.2, 1.35, entra="nada", dibujo=1.0, sfx="papel", props={
            "titulo": "REGLAMENTO DEL CONGRESO", "subtitulo": "Artículo 207",
            "articulos": [{"id": "a207", "titulo": "AL DISOLVERSE LA CÁMARA",
                           "lineas": ["quedarán caducados todos", "los asuntos pendientes"]}]},
            acciones=[{"at": "@pendiente", "props": {"resalta": ["a207"]}}]),
        quien("piz", 1250, "@claro-0.5", 0.5, "pensativo", y=1580, entra="nada", acciones=[
            {"at": "@claro-0.5", "x": 900, "dur": 0.5}, {"at": "@pendiente", "pose": "senala_izq"},
            {"at": "@caduca", "cara": "susto", "take": True}]),
        sello("CADUCADO", "rojo", 1260, "@caduca"),
    ]),
    # 3 · LA CARRETERA: Piz al volante y el alcoholímetro que no llega a cambiar
    dict(id="alcohol", fondo="carretera", animo="aventura", trans="zoom", footnote=FALC, lines=[
        V("Como bajar la tasa de alcohol al volante de 0,5 a 0,2.", "normal"),
        V("Era una propuesta del PSOE y pasó el primer voto, 173 a 168, con PP y Vox en contra.", "normal", 0.1),
        V("Ahora decae: la tasa sigue en 0,5.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@0,2", "general", [540, 1050], 0.5, zoom=1.1),
               plano("@173", "general", [540, 950], 0.5), plano("@decae", "general", [540, 1050], 0.5, zoom=1.08)],
       elements=[
        obj("coche", 540, 1450, 0, 0.9, entra="abajo", props={"color": "rojo", "cara": "ilusionado"},
            acciones=[{"at": "@decae", "cara": "sorpresa"}]),
        obj("alcoholimetro", 210, 950, "@tasa", 1.0, hud=True, entra="pop", sfx="pop", props={"texto": "0,5"},
            acciones=[{"at": "@0,2", "props": {"texto": "0,2"}, "tiembla": True}, {"at": "@decae", "props": {"texto": "0,5"}, "salta": True}]),
        rot("DE 0,5 A 0,2 g/l", 600, 430, "@0,2", 100, "amarillo", golpe=True, out="@PSOE"),
        rot("PSOE PROPONE", 540, 430, "@PSOE", 90, "blanco", golpe=True, out="@173"),
        rot("173 SÍ · 168 NO", 540, 430, "@173", 100, "amarillo", golpe=True, out="@decae"),
        rot("PP Y VOX: EN CONTRA", 540, 540, "@contra", 66, "blanco", out="@decae"),
        sello("DECAE", "rojo", 450, "@decae"),
        rot("SIGUE EN 0,5", 540, 600, "@sigue", 90, "amarillo", golpe=True),
    ]),
    # 4 · LA SEÑAL: cuándo correr es delito (y lo que no cambia)
    dict(id="velocidad", fondo={"tipo": "carretera", "velocidad": 2.0}, animo="tension", trans="corte", footnote="Carwow 08/10/2026", lines=[
        V("Lo mismo con la velocidad: ir 50 por encima del límite en ciudad iba a ser delito, en vez de 60.", "normal"),
        V("Hoy, en una calle de 50, el delito empieza en 111.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 950], 0), plano("@delito", "general", [600, 950], 0.5, zoom=1.06),
               plano("@111", "general", [540, 950], 0.5)],
       elements=[
        obj("senal", 820, 760, 0, 0.9, id="senal", entra="crece", sfx="golpe", props={"numero": 50}),
        obj("coche", 380, 1500, 0.2, 0.8, entra="abajo", props={"color": "verde", "cara": "riendo"},
            acciones=[{"at": "@delito", "tiembla": True, "cara": "susto"}]),
        rot("+50 = DELITO", 420, 430, "@delito", 100, "rojo", golpe=True, out="@Hoy"),
        rot("(ANTES +60)", 420, 540, "@60", 70, "blanco", out="@Hoy"),
        sello("DECAE", "rojo", 450, "@Hoy", x=400),
        rot("DELITO DESDE 111", 420, 600, "@111", 84, "amarillo", golpe=True),
    ]),
    # 5 · EL CEMENTERIO: más lápidas con nombre delante del Congreso
    dict(id="cementerio", fondo={"tipo": "calle", "hora": "tarde"}, animo="triste", trans="iris",
         footnote="LegalToday 12/10/2026 · Voz de la Verdad 05/10/2026 · Gaceta del Opositor 05/10/2026", lines=[
        V("También caen la ley de Integridad Pública contra la corrupción, la que daba la instrucción a los fiscales,", "normal"),
        V("el registro de lobbies y la condonación de deuda a las comunidades.", "normal", 0.05),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@fiscales", "general", [540, 1050], 0.6, zoom=1.08),
               plano("@condonación", "general", [540, 1000], 0.6)],
       elements=[
        edif("congreso", 540, 0, 0.7, entra="nada", acciones=[{"at": 0.1, "cara": "triste"}]),
        tumba(150, "@Integridad", ["INTEGRIDAD", "PÚBLICA"], 0.6),
        tumba(400, "@fiscales", ["LEY DE", "ENJUICIAMIENTO"], 0.6),
        tumba(660, "@lobbies", ["REGISTRO DE", "LOBBIES"], 0.6),
        tumba(920, "@condonación", ["DEUDA", "AUTONÓMICA"], 0.6),
        quien("piz", 540, "@caen", 0.5, "triste", y=1560, entra="abajo", acciones=[
            {"at": "@fiscales", "pose": "manos_juntas"}, {"at": "@comunidades", "pose": "cabeza", "cara": "preocupado"}]),
        rot("CORRUPCIÓN: PRESCRIPCIÓN DE 5 A 7 AÑOS", 540, 420, "@corrupción", 46, "blanco", out="@fiscales"),
    ]),
    # 6 · FINAL: la fecha de las nuevas Cortes y la pregunta
    dict(id="final", fondo="calle", animo="final", trans="zoom", footnote="Las nuevas Cortes se constituyen el 23/12/2026", lines=[
        V("Las nuevas Cortes nacen el 23 de diciembre y tendrán que empezar de cero.", "normal"),
        V("¿Cuál resucitarías tú? Te leo.", "normal", 0.15),
        V("Y síguenos para el próximo viaje de Piz.", "energia", 0.15),
    ], camara=[plano(0, "general", [540, 900], 0), plano("@cero", "general", [540, 950], 0.5, zoom=1.08),
               plano("@resucitarías", "general", [540, 900], 0.5)],
       elements=[
        edif("congreso", 540, 0, 0.8, entra="nada", acciones=[{"at": "@nacen", "cara": "ilusionado"}]),
        obj("cartel", 540, 420, "@23", 0.9, hud=True, entra="cae", sfx="golpe",
            props={"texto": "23 DE DICIEMBRE", "color": "blanco"}, out="@resucitarías"),
        quien("piz", 790, "@resucitarías", 0.6, "pensativo", y=1500, hud=True, entra="abajo", acciones=[
            {"at": "@resucitarías+0.2", "pose": "piensa"}, {"at": "@leo", "mira": "camara", "cara": "ilusionado"},
            {"at": "@síguenos", "pose": "saluda", "cara": "riendo"}, {"at": "@viaje", "salta": True}]),
        rot("¿CUÁL RESUCITARÍAS?", 540, 450, "@resucitarías", 90, "amarillo", golpe=True, out="@síguenos-0.3"),
        rot("SÍGUENOS", 540, 450, "@síguenos", 110, "amarillo", fx=[{"at": "@Piz", "do": "latir"}]),
    ]),
]

if __name__ == "__main__":
    episodio("leyes_mueren", "Las leyes que mueren el 29N", scenes,
             {"t": 2.0, "titulo": "Las leyes que mueren el 29N", "capitulo": None},
             ["Real Decreto 806/2026, de 5 de octubre (BOE 06/10/2026)",
              "Reglamento del Congreso, art. 207 (congreso.es)",
              "Civio: 309 iniciativas decaídas (LegalToday, 12/10/2026)",
              "Tasa de alcohol y delito de velocidad: Motor16 (11/10/2026), Carwow (08/10/2026)",
              "Otras leyes decaídas: LegalToday 12/10, Voz de la Verdad 05/10, Gaceta del Opositor 05/10/2026"],
             ("🪦 El 6 de octubre murieron unas 300 leyes a medio hacer\n"
              "📜 Al disolverse las Cortes, todo lo pendiente caduca (art. 207 del Reglamento)\n"
              "🍷 La tasa de alcohol iba a bajar de 0,5 a 0,2: sigue en 0,5\n"
              "🚗 El delito por velocidad en ciudad iba a empezar en +50: sigue en +60\n"
              "⚖️ También caen Integridad Pública, la nueva LECrim, los lobbies y la deuda autonómica\n"
              "💬 ¿Cuál resucitarías tú?\n"
              "🔔 Síguenos · 📚 Fuentes en comentarios"),
             "📚 Fuentes: RD 806/2026 (BOE 06/10) · Reglamento del Congreso art. 207 · Civio (LegalToday 12/10) · "
             "Motor16 11/10 · Carwow 08/10. ¿Ves un error? Dínoslo.",
             ["#29N", "#leyes", "#DGT", "#alcohol", "#Congreso", "#politica", "#España", "#pizarrapublica"],
             series_tag="EXPLICADO FÁCIL")
