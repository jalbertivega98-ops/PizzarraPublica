#!/usr/bin/env python3
"""«Sí a Broncano… y a Wild, silencio» (jueves 22/10/2026). Mundo dibujado: plató de La Revuelta y estudio de podcast.

Fuentes:
  The Objective 21/10/2026: Broncano anuncia que Sánchez estará el jueves 22 en La Revuelta.
  OKdiario 22/10/2026: emisión a las 21:45 en La 1 (TVE); preguntas clásicas del programa («¿cuánto dinero tienes en el banco?»).
  Hispanidad 22/10/2026: Sánchez «aún no ha contestado» a Wild; formato de Wild: 50 a 90 minutos, sin cortes,
    preguntas no pactadas, temas no negociables.
  Infobae / Europa Press 20/10/2026: Feijóo y Abascal aceptan a Wild; plazo para Sánchez hasta el viernes 23.
  BilbaoHiria 22/10/2026: Wild «ya se quedó sin él en 2023»; Feijóo y Abascal «no han respondido a La Revuelta»;
    Broncano: «tanto Feijóo como Abascal están invitados».
  Ojo: ninguna fuente cita un «no» oficial de Sánchez a Wild; se dice «sin respuesta», no «rechaza».
  Norma del proyecto: solo PSOE, PP y Vox; preguntas abiertas al público, sin afirmar intenciones que nadie ha dicho.
"""
from _mundo import *  # noqa: F401,F403

FONDO_Y, FRENTE_Y = 1250, 1640
F_REV = "The Objective 21/10/2026 · OKdiario 22/10/2026"
F_WILD = "Hispanidad 22/10/2026 · Infobae/Europa Press 20/10/2026"
F_BIL = "BilbaoHiria 22/10/2026"
SILLAS = [(400, (225, 30, 40), "SÁNCHEZ"), (680, (0, 104, 180), "FEIJÓO"), (930, (90, 175, 40), "ABASCAL")]


def sillas(at=0.0):
    return [obj("silla", x, FONDO_Y, at, 0.5, id=f"s{i}", entra="nada", props={"color": col, "texto": tx})
            for i, (x, col, tx) in enumerate(SILLAS)]


scenes = [
    # 1 · GANCHO: Sánchez entra en el plató de La Revuelta; Wild, con el móvil, esperando
    dict(id="gancho", fondo={"tipo": "plato", "rotulo": "LA REVUELTA"}, animo="tension", footnote=F_REV, lines=[
        V("Esta noche, Pedro Sánchez se sienta con Broncano en La Revuelta.", "energia"),
        V("¿Y Jordi Wild? Sigue esperando su respuesta.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 1100], 0), plano("@Broncano", "general", [540, 1050], 0.5, zoom=1.08),
               plano("@Wild", "medio", "wild", 0.4, aire=220), plano("@respuesta", "general", [540, 1000], 0.5)],
       elements=[
        quien("broncano", 770, 0, 0.75, "riendo", entra="nada", acciones=[
            {"at": 0.3, "pose": "saluda"}, {"at": "@sienta", "mira": "izq", "cara": "ilusionado"}, {"at": "@Broncano", "salta": True},
            {"at": "@Revuelta", "pose": "pulgar"}]),
        quien("sanchez", -200, 0.1, 0.75, "ilusionado", entra="nada", acciones=[
            {"at": 0.2, "x": 340, "dur": 1.0}, {"at": "@sienta", "pose": "saluda", "cara": "riendo"},
            {"at": "@Revuelta", "mira": "der"}, {"at": "@Wild", "mira": "camara", "cara": "pensativo"}]),
        rot("ESTA NOCHE · LA 1", 540, 520, "@noche", 84, "amarillo", golpe=True, out="@Wild"),
        quien("wild", 1300, "@Wild-0.3", 0.5, "pensativo", y=FRENTE_Y, entra="nada", objeto="movil", pose="sostiene", acciones=[
            {"at": "@Wild", "x": 540, "dur": 0.6, "corre": True}, {"at": "@esperando", "cara": "preocupado", "mira": "arriba"},
            {"at": "@respuesta", "tiembla": True}]),
        rot("¿Y WILD?", 540, 520, "@Wild", 110, "rojo", golpe=True),
        sello("SIN RESPUESTA", "naranja", 720, "@respuesta"),
    ]),
    # 2 · EL FORMATO DE WILD: dos sillas llenas, una vacía
    dict(id="wild", fondo="estudio", animo="tension", trans="barrido", footnote=F_WILD, lines=[
        V("En The Wild Project: hasta noventa minutos, sin cortes y sin preguntas pactadas.", "normal"),
        V("Feijóo y Abascal ya han dicho que sí.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 900], 0), plano("@cortes", "general", [540, 850], 0.5, zoom=1.05),
               plano("@Feijóo", "general", [700, 1150], 0.6), plano("@sí", "general", [560, 1150], 0.4, zoom=1.06)],
       elements=[
        obj("cartel", 540, 620, 0, 1.12, hud=True, entra="crece", sfx="papel", dibuja=2.4, out="@Feijóo",
            props={"lineas": ["HASTA 90 MINUTOS", "SIN CORTES", "SIN PREGUNTAS PACTADAS"]}),
        *sillas(0),
        quien("feijoo", 680, "@Feijóo-0.3", 0.42, "ilusionado", y=FONDO_Y + 60, entra="cae", acciones=[{"at": "@Abascal", "pose": "pulgar"}, {"at": "@sí", "salta": True}]),
        quien("abascal", 930, "@Abascal-0.3", 0.42, "ilusionado", y=FONDO_Y + 60, entra="cae", acciones=[{"at": "@dicho", "pose": "saluda"}, {"at": "@sí", "salta": True}]),
        sello("DENTRO", "verde", 1450, "@sí", x=800),
        rot("?", 400, 1080, "@sí", 150, "rojo", golpe=True),
        quien("pizon", 130, 0, 0.42, "confundido", y=1660, entra="nada", acciones=[
            {"at": "@noventa", "cara": "sorpresa", "mira": "arriba"}, {"at": "@cortes", "pose": "piensa"},
            {"at": "@pactadas", "cara": "idea", "salta": True}, {"at": "@Feijóo", "mira": "der"}, {"at": "@sí", "pose": "senala"}]),
    ]),
    # 3 · LA REVUELTA: programa de humor en la tele pública
    dict(id="revuelta", fondo={"tipo": "plato", "rotulo": "LA REVUELTA"}, animo="comico", trans="papel", footnote=F_REV, lines=[
        V("En La Revuelta: humor, en La 1, la tele pública.", "normal"),
        V("Y una pregunta que es un clásico: ¿cuánto dinero tienes en el banco?", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 1050], 0), plano("@pública", "general", [540, 950], 0.5, zoom=1.05),
               plano("@cuánto", "general", [540, 1000], 0.5, zoom=1.1)],
       elements=[
        quien("broncano", 770, 0, 0.75, "riendo", entra="nada", acciones=[
            {"at": "@humor", "salta": True, "cara": "riendo"}, {"at": "@pública", "pose": "senala_izq"},
            {"at": "@clásico", "cara": "burla", "pose": "jarras"}, {"at": "@cuánto", "pose": "senala_izq", "mira": "izq"}]),
        quien("sanchez", 310, 0, 0.75, "ilusionado", entra="nada", acciones=[
            {"at": "@humor", "cara": "riendo"}, {"at": "@La#2", "mira": "der"}, {"at": "@pregunta", "pose": "piensa"},
            {"at": "@dinero", "cara": "susto", "take": True}, {"at": "@banco", "tiembla": True}]),
        rot("HUMOR · LA 1", 540, 480, "@humor", 92, "amarillo", golpe=True, out="@clásico"),
        obj("bocadillo", 700, 620, "@cuánto-0.2", 0.9, hud=True, entra="pop", sfx="pop",
            props={"lineas": ["¿CUÁNTO DINERO", "TIENES EN EL BANCO?"], "cola": (1, 1)}),
    ]),
    # 4 · EL PLAZO: calendario con el viernes 23
    dict(id="plazo", fondo="oficina", animo="tension", trans="corte", footnote="Infobae/Europa Press 20/10/2026 · " + F_BIL, lines=[
        V("Wild le da hasta mañana, viernes 23.", "normal"),
        V("Y en 2023 ya se quedó sin él.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 900], 0), plano("@viernes", "general", [700, 800], 0.4, zoom=1.08),
               plano("@2023", "medio", "wild", 0.5, aire=220)],
       elements=[
        obj("calendario", 760, 760, 0, 0.5, entra="cae", sfx="golpe",
            props={"mes": "OCTUBRE", "inicio": 3, "dias": 31, "marcados": [23], "colores": {23: "rojo"}}),
        rot("VIERNES 23", 760, 1180, "@23", 84, "amarillo", golpe=True, out="@2023"),
        obj("reloj", 220, 700, "@mañana", 0.6, entra="pop", sfx="pop", props={"velocidad": 6}),
        quien("wild", 340, 0, 0.55, "pensativo", entra="nada", acciones=[
            {"at": "@hasta", "pose": "senala", "mira": "der"}, {"at": "@viernes", "mira": "calendario"},
            {"at": "@2023", "cara": "triste", "pose": "encoge"}, {"at": "@él", "mira": "camara", "cara": "burla"}]),
        sello("2023: NO FUE", "rojo", 1180, "@2023", x=760),
    ]),
    # 5 · GIRO: Broncano también invitó a Feijóo y a Abascal… y no le han contestado
    dict(id="giro", fondo={"tipo": "plato", "rotulo": "LA REVUELTA"}, animo="comico", musica="corte", trans="iris", footnote=F_BIL, lines=[
        V("Pero ojo: Broncano también ha invitado a Feijóo y a Abascal…", "normal"),
        V("y ellos tampoco le han contestado.", "remate", 0.1),
    ], camara=[plano(0, "general", [540, 1050], 0), plano("@Feijóo", "general", [700, 1050], 0.6, zoom=1.05),
               plano("@tampoco", "general", [540, 1000], 0.4, zoom=1.1)],
       elements=[
        quien("broncano", 260, 0, 0.75, "ilusionado", entra="nada", acciones=[
            {"at": "@ojo", "pose": "senala", "mira": "camara"}, {"at": "@invitado", "pose": "saluda", "mira": "der"},
            {"at": "@tampoco", "cara": "burla", "pose": "jarras"}, {"at": "@contestado", "salta": True}]),
        quien("feijoo", 1300, "@Feijóo-0.4", 0.68, "normal", entra="nada", acciones=[
            {"at": "@Feijóo", "x": 640, "dur": 0.7}, {"at": "@tampoco", "mira": "arriba", "pose": "encoge"}]),
        quien("abascal", 1400, "@Abascal-0.4", 0.68, "normal", entra="nada", acciones=[
            {"at": "@Abascal", "x": 890, "dur": 0.7}, {"at": "@tampoco", "mira": "izq", "pose": "encoge"}]),
        sello("SIN RESPUESTA", "naranja", 560, "@contestado"),
    ]),
    # 6 · FINAL: la pregunta que divide
    dict(id="final", fondo={"tipo": "rayos", "color": "amarillo"}, animo="final", trans="zoom", footnote="Pregunta a la audiencia", lines=[
        V("¿Entrevista cómoda o valiente? ¿Broncano o Wild?", "energia"),
        V("Te leo en comentarios. Y síguenos.", "normal", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@Broncano", "general", [540, 900], 0.5, zoom=1.08),
               plano("@síguenos", "general", [540, 1000], 0.5)],
       elements=[
        rot("¿CÓMODA O VALIENTE?", 540, 480, 0.2, 78, "rojo", golpe=True, out="@Broncano"),
        rot("¿BRONCANO O WILD?", 540, 480, "@Broncano", 88, "rojo", golpe=True, out="@síguenos-0.3"),
        rot("SÍGUENOS", 540, 480, "@síguenos", 110, "rojo"),
        quien("broncano", 280, 0, 0.65, "riendo", entra="nada", acciones=[
            {"at": "@cómoda", "pose": "saluda"}, {"at": "@Broncano", "salta": True}, {"at": "@comentarios", "mira": "camara"}]),
        quien("wild", 800, 0, 0.65, "serio", entra="nada", acciones=[
            {"at": "@valiente", "pose": "jarras"}, {"at": "@Wild", "salta": True}, {"at": "@comentarios", "mira": "camara"}]),
        quien("piz", 540, 0, 0.45, "pensativo", y=1660, entra="nada", acciones=[
            {"at": "@Entrevista", "mira": "izq"}, {"at": "@valiente", "mira": "der"}, {"at": "@leo", "pose": "senala", "cara": "riendo"},
            {"at": "@síguenos", "pose": "saluda", "salta": True}]),
    ]),
]

if __name__ == "__main__":
    episodio("broncano_wild", "Sí a Broncano… y a Wild, silencio", scenes,
             {"t": 3.6, "titulo": "Sí a Broncano… y a Wild, silencio", "capitulo": None},
             ["The Objective (21/10/2026): Sánchez estará el jueves 22 en La Revuelta",
              "OKdiario (22/10/2026): 21:45 en La 1; preguntas clásicas del programa",
              "Hispanidad (22/10/2026): Sánchez aún no ha contestado a Wild; formato sin cortes ni preguntas pactadas",
              "Infobae / Europa Press (20/10/2026): Feijóo y Abascal aceptan a Wild; plazo hasta el viernes 23",
              "BilbaoHiria (22/10/2026): en 2023 Wild se quedó sin Sánchez; Feijóo y Abascal no han respondido a La Revuelta",
              "Personajes dibujados como pizarras, sin caricatura"],
             ("📺 Esta noche Sánchez se sienta con Broncano en La Revuelta (21:45, La 1)\n"
              "🎙️ ¿Y Jordi Wild? Sigue sin respuesta: tiene hasta mañana, viernes 23\n"
              "⏱️ Wild ofrece hasta 90 minutos, sin cortes y sin preguntas pactadas; Feijóo y Abascal ya dijeron que sí\n"
              "😂 La Revuelta: humor en la tele pública y la pregunta clásica, ¿cuánto dinero tienes en el banco?\n"
              "👀 Pero ojo: Feijóo y Abascal tampoco han contestado a Broncano\n"
              "💬 ¿Entrevista cómoda o valiente? ¿BRONCANO o WILD? Te leo 👇\n"
              "🔔 Síguenos · 📚 Fuentes en comentarios"),
             "📚 Fuentes: The Objective 21/10/2026 · OKdiario 22/10/2026 · Hispanidad 22/10/2026 · Infobae/Europa Press 20/10/2026 · "
             "BilbaoHiria 22/10/2026. ¿Ves un error? Dínoslo.",
             ["#Broncano", "#LaRevuelta", "#JordiWild", "#Sánchez", "#29N", "#elecciones", "#pizarrapublica"],
             series_tag="EXPLICADO FÁCIL")
