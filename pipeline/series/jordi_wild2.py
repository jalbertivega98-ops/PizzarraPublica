#!/usr/bin/env python3
"""«Jordi Wild cambia las reglas» (martes 20/10/2026). Mundo dibujado: estudio de podcast. Actualiza jordi_wild.py.

Fuentes:
  Infobae / Europa Press 20/10/2026: Wild retira el lunes 19 el «o todos o ninguno»; Feijóo y Abascal aceptan; Colau (Frente Amplio)
    acepta el 20/10; Sánchez sin responder; plazo hasta el viernes 23; dos periodistas verifican datos fuera de cámara.
  Nació Digital 20/10/2026: entrevistas de 50 a 90 minutos, sin edición; emisión desde el 9 de noviembre.
  Just the News 29/10/2024: la entrevista de Joe Rogan a Trump, 10 millones de visualizaciones en menos de 24 horas.
  Xataka 17/09/2025: The Wild Project se acerca a los 7 millones de suscriptores.
  Espinof 11/07/2023: el cara a cara Sánchez-Feijóo de 2023, 5,91 millones, el debate electoral menos visto de la historia.
  Norma del proyecto: solo PSOE, PP y Vox; Colau aparece en una frase porque ocupa la cuarta silla.
"""
from _mundo import *  # noqa: F401,F403

SILLAS = [(150, "gris", "COLAU"), (400, (225, 30, 40), "SÁNCHEZ"), (680, (0, 104, 180), "FEIJÓO"), (930, (90, 175, 40), "ABASCAL")]
FONDO_Y, FRENTE_Y = 1250, 1640
FINF = "Infobae / Europa Press 20/10/2026"


def sillas(at=0.0, entra="nada"):
    return [obj("silla", x, FONDO_Y, at + i * 0.12 if entra != "nada" else at, 0.5, id=f"s{i}", entra=entra,
                props={"color": col, "texto": tx}) for i, (x, col, tx) in enumerate(SILLAS)]


scenes = [
    # 1 · GANCHO: el marcador se dispara a 10 millones
    dict(id="gancho", fondo="estudio", animo="tension", footnote="Just the News 29/10/2024", lines=[
        V("Diez millones de visualizaciones en menos de veinticuatro horas.", "energia"),
        V("Eso logró la entrevista de Joe Rogan a Trump… y Jordi Wild quiere repetirlo en España.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@veinticuatro", "general", [540, 800], 0.5, zoom=1.08),
               plano("@Rogan", "general", [540, 1100], 0.5), plano("@Wild", "medio", "wild", 0.4, aire=200)],
       elements=[
        obj("contador", 540, 640, 0, 1.0, hud=True, entra="pop", sfx="kaching", dibuja=1.6,
            props={"valor": 10000000, "ancho": 860}, out="@Rogan"),
        rot("EN 24 HORAS", 540, 860, "@veinticuatro", 92, "amarillo", golpe=True, out="@Rogan"),
        etq("JOE ROGAN × TRUMP", 540, 560, "@Rogan", "rojo", 0.9, hud=True),
        obj("microfono", 760, 1330, 0, 0.5, entra="nada", props={"encendido": True}),
        quien("wild", 540, 0, 0.6, "pensativo", y=FRENTE_Y, entra="nada", acciones=[
            {"at": 0.4, "cara": "sorpresa", "take": True}, {"at": "@millones", "salta": True}, {"at": "@visualizaciones", "mira": "arriba"},
            {"at": "@menos", "pose": "piensa"}, {"at": "@veinticuatro", "pose": "senala", "mira": "arriba"},
            {"at": "@entrevista", "mira": "izq"}, {"at": "@Rogan", "pose": "senala_izq"}, {"at": "@Trump", "pose": "jarras", "cara": "burla"}, {"at": "@Wild", "salta": True, "cara": "riendo"},
            {"at": "@España", "pose": "senala", "mira": "camara"}]),
    ]),
    # 2 · EL TAMAÑO: casi 7 millones de suscriptores frente al cara a cara de 2023
    dict(id="tamano", fondo={"tipo": "plano", "color": (28, 52, 110)}, animo="curioso", trans="barrido",
         footnote="Xataka 17/09/2025 · Espinof 11/07/2023", lines=[
        V("Su canal tiene casi siete millones de suscriptores.", "normal"),
        V("Y el último cara a cara en la tele lo vieron 5,9 millones: el debate menos visto de la historia.", "normal", 0.15),
    ], camara=[plano(0, "general", [540, 900], 0), plano("@siete", "general", [540, 700], 0.6, zoom=1.08), plano("@cara", "general", [540, 1000], 0.6, zoom=1.04),
               plano("@historia", "general", [540, 1000], 0.5, zoom=1.08)],
       elements=[
        rot("CASI 7 MILLONES", 540, 430, "@canal", 110, "amarillo", golpe=True, out="@cara"),
        etq("DE SUSCRIPTORES", 540, 600, "@suscriptores", "rojo", 0.9, hud=True, out="@cara"),
        obj("tele", 540, 980, "@cara", 1.05, entra="cae", sfx="golpe", props={"texto": "CARA A CARA 2023"}),
        rot("5,9 MILLONES", 540, 430, "@vieron", 110, "amarillo", golpe=True),
        sello("EL MENOS VISTO", "naranja", 1460, "@menos"),
        quien("pizon", 900, 0, 0.5, "confundido", y=1660, entra="nada", acciones=[
            {"at": "@canal", "mira": "arriba", "pose": "senala"}, {"at": "@suscriptores", "cara": "sorpresa", "salta": True}, {"at": "@tele", "mira": "izq", "pose": "piensa"},
            {"at": "@último", "mira": "izq"}, {"at": "@vieron", "pose": "senala_izq"}, {"at": "@menos", "tiembla": True}, {"at": "@historia", "cara": "susto", "take": True}]),
    ]),
    # 3 · LAS REGLAS CAMBIAN: el cartel «o todos o nadie» se rompe
    dict(id="reglas", fondo="calle", animo="tension", trans="papel", footnote=FINF, lines=[
        V("Y Wild acaba de cambiar las reglas: ya no hace falta que vayan todos.", "normal"),
        V("Se lo pidieron sus seguidores.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@reglas", "general", [540, 800], 0.5, zoom=1.06),
               plano("@todos", "general", [540, 900], 0.4, zoom=1.1), plano("@seguidores", "general", [540, 1050], 0.5)],
       elements=[
        obj("cartel", 540, 700, 0, 1.6, hud=True, entra="crece", sfx="papel", dibuja=0.8,
            props={"lineas": ["O TODOS", "O NADIE"]}, out="@ya"),
        rot("YA NO", 540, 700, "@ya", 160, "rojo", golpe=True),
        quien("wild", 300, 0, 0.55, "serio", entra="nada", acciones=[
            {"at": "@cambiar", "pose": "senala", "mira": "der"}, {"at": "@ya", "pose": "encoge", "cara": "riendo"}, {"at": "@falta", "x": 380, "dur": 0.5}, {"at": "@todos", "salta": True, "mira": "camara"}]),
        *[quien(q, 1300, "@seguidores-0.2", 0.4, "ilusionado", y=1600, entra="nada", acciones=[
            {"at": "@seguidores", "x": x, "dur": 0.8, "corre": True}, {"at": "@seguidores+0.4", "pose": "saluda", "salta": True}])
          for q, x in (("piz", 620), ("critica", 780), ("pizon", 940))],
    ]),
    # 4 · QUIÉN DICE SÍ: Feijóo, Abascal… y la cuarta silla se llena
    dict(id="si", fondo="estudio", animo="alegre", trans="iris", footnote=FINF, lines=[
        V("Feijóo y Abascal siguen dentro.", "normal"),
        V("Y hoy ha aceptado Ada Colau, del Frente Amplio.", "normal", 0.1),
    ], camara=[plano(0, "general", [700, 1150], 0), plano("@Abascal", "general", [760, 1150], 0.5, zoom=1.05), plano("@hoy", "general", [540, 1150], 0.5), plano("@Colau", "general", [300, 1150], 0.6, zoom=1.05)],
       elements=[
        *sillas(0),
        quien("feijoo", 680, 0, 0.42, "ilusionado", y=FONDO_Y + 60, entra="nada", acciones=[{"at": "@Feijóo", "pose": "pulgar"}, {"at": "@siguen", "salta": True}, {"at": "@hoy", "mira": "izq"}]),
        quien("abascal", 930, 0, 0.42, "ilusionado", y=FONDO_Y + 60, entra="nada", acciones=[{"at": "@Abascal", "pose": "saluda"}, {"at": "@dentro", "salta": True}, {"at": "@hoy", "mira": "izq"}]),
        sello("DENTRO", "verde", 1450, "@dentro", x=800),
        quien("colau", -200, "@aceptado-0.4", 0.42, "ilusionado", y=FONDO_Y + 60, entra="nada", acciones=[
            {"at": "@aceptado", "x": 150, "dur": 0.8, "corre": True}, {"at": "@Frente", "pose": "saluda", "cara": "riendo"}]),
        sello("ACEPTA", "verde", 1450, "@Colau", x=220),
    ]),
    # 5 · SÁNCHEZ: el calendario con el viernes 23 marcado en rojo
    dict(id="sanchez", fondo="oficina", animo="tension", trans="corte", footnote=FINF, lines=[
        V("¿Y Sánchez? Sigue sin responder.", "normal"),
        V("Wild le pone fecha: hasta este viernes 23. Si no contesta, se queda fuera.", "remate", 0.15),
    ], camara=[plano(0, "medio", "sanchez", 0, aire=220), plano("@fecha", "general", [540, 900], 0.5),
               plano("@fuera", "medio", "sanchez", 0.4, aire=220)],
       elements=[
        quien("sanchez", 340, 0, 0.55, "pensativo", entra="nada", acciones=[
            {"at": "@Sánchez", "pose": "piensa"}, {"at": "@responder", "mira": "camara", "pose": "encoge"},
            {"at": "@viernes", "mira": "calendario", "cara": "preocupado"}, {"at": "@fuera", "cara": "susto", "take": True}]),
        sello("PENDIENTE", "naranja", 520, "@responder", x=380),
        obj("calendario", 760, 760, "@fecha", 0.5, id="calendario", entra="cae", sfx="golpe",
            props={"mes": "OCTUBRE", "inicio": 3, "dias": 31, "marcados": [23], "colores": {23: "rojo"}}),
        rot("VIERNES 23", 760, 1180, "@23", 84, "amarillo", golpe=True),
        obj("reloj", 220, 1100, "@contesta", 0.6, entra="pop", sfx="pop", props={"velocidad": 6}),
    ]),
    # 6 · EL FORMATO
    dict(id="formato", fondo={"tipo": "plano", "color": (28, 52, 110)}, animo="curioso", trans="papel",
         footnote="Nació Digital 20/10/2026 · Infobae 20/10/2026", lines=[
        V("Hasta hora y media, sin cortes y con dos periodistas verificando datos.", "normal"),
        V("Se emitirán desde el 9 de noviembre.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 900], 0), plano("@periodistas", "general", [540, 850], 0.6, zoom=1.05),
               plano("@9", "general", [540, 1000], 0.5)],
       elements=[
        obj("cartel", 540, 700, 0, 1.5, hud=True, entra="crece", sfx="papel", dibuja=2.4,
            props={"lineas": ["HASTA 90 MINUTOS", "SIN CORTES", "2 PERIODISTAS VERIFICAN"]}),
        rot("DESDE EL 9N", 400, 1180, "@noviembre-0.3", 96, "amarillo", golpe=True),
        quien("piz", 850, 0, 0.5, "pensativo", y=1560, entra="nada", acciones=[
            {"at": "@hora", "pose": "senala", "mira": "arriba"}, {"at": "@cortes", "cara": "sorpresa"},
            {"at": "@periodistas", "pose": "piensa"}, {"at": "@verificando", "cara": "idea", "mira": "camara"}, {"at": "@emitirán", "pose": "senala"}, {"at": "@noviembre", "salta": True, "cara": "riendo"}]),
    ]),
    # 7 · FINAL: tres sillas llenas, una vacía
    dict(id="final", fondo="estudio", animo="final", trans="zoom", footnote="Pregunta a la audiencia", lines=[
        V("¿Llenará Sánchez su silla? Escribe SÍ o NO, te leo.", "normal"),
        V("Y síguenos.", "energia", 0.15),
    ], camara=[plano(0, "general", [540, 1150], 0), plano("@SÍ", "general", [400, 1100], 0.5, zoom=1.08),
               plano("@síguenos", "general", [540, 1150], 0.5)],
       elements=[
        *sillas(0),
        quien("colau", 150, 0, 0.42, "normal", y=FONDO_Y + 60, entra="nada", acciones=[{"at": "@Sánchez", "mira": "der"}]),
        quien("feijoo", 680, 0, 0.42, "normal", y=FONDO_Y + 60, entra="nada", acciones=[{"at": "@Sánchez", "mira": "izq"}]),
        quien("abascal", 930, 0, 0.42, "normal", y=FONDO_Y + 60, entra="nada", acciones=[{"at": "@Sánchez", "mira": "izq"}]),
        quien("wild", 520, 0, 0.6, "pensativo", y=FRENTE_Y, entra="nada", acciones=[
            {"at": "@silla", "mira": "camara", "pose": "piensa"}, {"at": "@síguenos", "pose": "saluda", "cara": "riendo"}]),
        rot("¿SÍ O NO?", 540, 560, "@SÍ", 110, "amarillo", golpe=True, out="@síguenos-0.3", fx=[{"at": "@leo", "do": "latir"}]),
        rot("SÍGUENOS", 540, 560, "@síguenos", 110, "amarillo"),
    ]),
]

if __name__ == "__main__":
    episodio("jordi_wild2", "Jordi Wild cambia las reglas", scenes,
             {"t": 2.0, "titulo": "Jordi Wild cambia las reglas", "capitulo": None},
             ["Infobae / Europa Press (20/10/2026): Wild retira el «o todos o ninguno»; aceptan Feijóo, Abascal y Colau; plazo hasta el 23",
              "Nació Digital (20/10/2026): entrevistas de 50 a 90 minutos sin edición; emisión desde el 9 de noviembre",
              "Just the News (29/10/2024): Rogan-Trump, 10 millones de visualizaciones en menos de 24 horas",
              "Xataka (17/09/2025): The Wild Project, cerca de 7 millones de suscriptores",
              "Espinof (11/07/2023): cara a cara de 2023, 5,91 millones, el debate menos visto",
              "Personajes dibujados como pizarras, sin caricatura"],
             ("📈 10 millones de visualizaciones en 24 horas: eso hizo la entrevista de Joe Rogan a Trump\n"
              "🎙️ Jordi Wild quiere repetirlo: su canal tiene casi 7 millones de suscriptores (el cara a cara de 2023 lo vieron 5,9 millones)\n"
              "🔄 Cambia las reglas: ya no hace falta que vayan todos\n"
              "✅ Feijóo, Abascal y Colau aceptan\n"
              "⏳ Sánchez no responde: tiene hasta el viernes 23\n"
              "🎥 Hasta 90 minutos, sin cortes y con verificadores; desde el 9 de noviembre\n"
              "💬 ¿Llenará Sánchez su silla? SÍ o NO 👇\n"
              "🔔 Síguenos · 📚 Fuentes en comentarios"),
             "📚 Fuentes: Infobae/Europa Press 20/10/2026 · Nació Digital 20/10/2026 · Just the News 29/10/2024 · Xataka 17/09/2025 · "
             "Espinof 11/07/2023. ¿Ves un error? Dínoslo.",
             ["#JordiWild", "#TheWildProject", "#29N", "#elecciones", "#Sánchez", "#Feijóo", "#Abascal", "#pizarrapublica"],
             series_tag="EXPLICADO FÁCIL")
