#!/usr/bin/env python3
"""«Y Sánchez dijo sí» (domingo 25/10/2026). Cap. 3 de la saga Jordi Wild (jordi_wild.py, jordi_wild2.py, broncano_wild.py).

Wild sale con el diseño de la foto que mandó joel (pelo hacia atrás, barba corta, americana azul, chaleco gris).
Las frases de Sánchez son literales y van con la voz «tele» (S), como en sanchez_revuelta.py.

Fuentes:
  The Objective 23/10/2026: Sánchez acepta el viernes 23 por la tarde, el último día del plazo y el último de los cuatro;
    «Gracias por la invitación. Ahí estaré»; Wild: «Pues ya estaría: 4/4». Orden: Feijóo, Abascal, Colau, Sánchez.
  El Debate 23/10/2026: «¡Acuérdate de que mi lado bueno es el izquierdo!» (al realizador, Nacho Amela).
  elDiario.es 23/10/2026 (act. 24/10) y Extradigital: las cuatro se emiten el 13 de noviembre, con una hora de diferencia;
    de 50 a 90 minutos; sin edición; dos periodistas verifican datos fuera de cámara.
  elDiario.es 22/10/2026: el PSOE acepta el cara a cara con Feijóo en Mediaset el lunes 16/11; debate a cuatro el 26/11 sin
    acuerdo (PSOE: RTVE; PP: Atresmedia).
  Corrección: jordi_wild.py y jordi_wild2.py decían «desde el 9 de noviembre» (Nació Digital 20/10); ahora es el 13.
"""
from _mundo import *  # noqa: F401,F403

SILLAS = [(150, "gris", "COLAU"), (400, (225, 30, 40), "SÁNCHEZ"), (680, (0, 104, 180), "FEIJÓO"), (930, (90, 175, 40), "ABASCAL")]
FONDO_Y, FRENTE_Y = 1250, 1640
F_SI = "The Objective · El Debate 23/10/2026"
F_FORMATO = "elDiario.es 24/10/2026 · Extradigital"
F_DEBATES = "elDiario.es 22/10/2026"


def S(text, pausa=None):
    """Frase literal de Sánchez: voz del canal procesada («tele»), no imita la suya."""
    return dict(V(text, "normal", pausa), efecto_voz="tele")


def sillas(at=0.0):
    return [obj("silla", x, FONDO_Y, at, 0.5, id=f"s{i}", entra="nada", props={"color": col, "texto": tx})
            for i, (x, col, tx) in enumerate(SILLAS)]


def sentado(q, x, at=0.0, cara="normal", entra="nada", acciones=()):
    return quien(q, x, at, 0.42, cara, y=FONDO_Y + 60, entra=entra, acciones=list(acciones))


scenes = [
    # 1 · GANCHO: último día del plazo, la silla de Sánchez vacía y el reloj corriendo
    dict(id="gancho", fondo="estudio", animo="tension", footnote=F_SI, lines=[
        V("Viernes 23. Último día del plazo… y la silla de Sánchez seguía vacía.", "energia"),
        V("Hasta que llegó el mensaje.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 1150], 0), plano("@silla", "general", [400, 1150], 0.5, zoom=1.12),
               plano("@mensaje", "medio", "wild", 0.4, aire=220)],
       elements=[
        *sillas(0),
        sentado("colau", 150, acciones=[{"at": "@vacía", "mira": "der"}]),
        sentado("feijoo", 680, acciones=[{"at": "@vacía", "mira": "izq"}]),
        sentado("abascal", 930, acciones=[{"at": "@vacía", "mira": "izq"}]),
        obj("reloj", 400, 1000, 0.2, 0.55, entra="pop", sfx="pop", props={"velocidad": 8}, out="@mensaje"),
        rot("ÚLTIMO DÍA", 540, 560, "@Último", 100, "rojo", golpe=True, out="@mensaje"),
        obj("microfono", 760, 1330, 0, 0.5, entra="nada", props={"encendido": True}),
        quien("wild", 540, 0, 0.6, "preocupado", y=FRENTE_Y, entra="nada", acciones=[
            {"at": "@plazo", "mira": "arriba", "pose": "manos_juntas"}, {"at": "@vacía", "mira": "izq", "cara": "triste"},
            {"at": "@mensaje", "cara": "sorpresa", "take": True, "objeto": {"tipo": "movil", "pantalla": "sms", "suena": True,
                                                                          "remite": "SÁNCHEZ", "texto": "…"}}]),
    ]),
    # 2 · EL SÍ: «Ahí estaré» y el gag del lado bueno
    dict(id="si", fondo="oficina", animo="comico", trans="corte", footnote=F_SI, lines=[
        V("Sánchez contestó en X:", "normal"),
        S("«Gracias por la invitación. Ahí estaré».", 0.05),
        V("Y al realizador le dejó un recado:", "normal", 0.15),
        S("«Acuérdate de que mi lado bueno es el izquierdo».", 0.05),
    ], camara=[plano(0, "medio", "sanchez", 0, aire=240), plano("@realizador", "general", [540, 1000], 0.5),
               plano("@izquierdo", "primero", "sanchez", 0.4, aire=160)],
       elements=[
        quien("sanchez", 420, 0, 0.62, "ilusionado", id="sanchez", entra="nada", acciones=[
            {"at": 0.1, "objeto": {"tipo": "movil", "pantalla": "sms", "remite": "SÁNCHEZ", "lineas": ["Gracias por la", "invitación.", "Ahí estaré"]}},
            {"at": "@Gracias", "mira": "camara"}, {"at": "@estaré", "pose": "pulgar", "cara": "riendo", "objeto": None},
            {"at": "@recado", "pose": "senala", "mira": "der"},
            {"at": "@bueno", "giro": -0.8, "cara": "burla"}, {"at": "@izquierdo", "pose": "jarras", "salta": True}]),
        obj("bocadillo", 760, 640, "@estaré-0.3", 0.9, hud=True, entra="pop", sfx="pop",
            props={"lineas": ["AHÍ ESTARÉ"], "cola": (-1, 1)}, out="@recado"),
        quien("wild", 1300, "@realizador-0.3", 0.5, "riendo", y=1660, entra="nada", acciones=[
            {"at": "@realizador", "x": 880, "dur": 0.7}, {"at": "@bueno", "cara": "burla", "pose": "encoge"},
            {"at": "@izquierdo", "cara": "riendo", "salta": True}]),
        sello("SU LADO BUENO", "naranja", 1480, "@izquierdo", x=420),
    ]),
    # 3 · 4 DE 4: entran en el orden en que aceptaron
    dict(id="cuatro", fondo="estudio", animo="alegre", trans="iris", footnote=F_SI, lines=[
        V("Wild lo celebró: «Pues ya estaría. Cuatro de cuatro».", "energia"),
        V("Primero dijo sí Feijóo, luego Abascal, luego Colau… y Sánchez, el último.", "normal", 0.1),
    ], camara=[plano(0, "medio", "wild", 0, aire=220), plano("@Primero", "general", [540, 1150], 0.5),
               plano("@último", "general", [400, 1150], 0.4, zoom=1.12)],
       elements=[
        *sillas(0),
        sentado("feijoo", 680, "@Feijóo-0.1", "ilusionado", entra="pop", acciones=[{"at": "@Feijóo", "pose": "saluda"}]),
        sentado("abascal", 930, "@Abascal-0.1", "ilusionado", entra="pop", acciones=[{"at": "@Abascal", "pose": "pulgar"}]),
        sentado("colau", 150, "@Colau-0.1", "ilusionado", entra="pop", acciones=[{"at": "@Colau", "pose": "saluda"}]),
        sentado("sanchez", 400, "@Sánchez-0.1", "riendo", entra="cae", acciones=[{"at": "@último", "pose": "saluda", "salta": True}]),
        etq("1º", 680, 1000, "@Feijóo", "verde", 0.6),
        etq("2º", 930, 1000, "@Abascal", "verde", 0.6),
        etq("3º", 150, 1000, "@Colau", "verde", 0.6),
        etq("4º", 400, 1000, "@Sánchez", "rojo", 0.6),
        pum("¡4/4!", 540, 1250, "@celebró", 0.8),
        rot("4/4", 540, 520, "@Cuatro", 170, "amarillo", golpe=True, fx=[{"at": "@último", "do": "latir"}]),
        quien("wild", 540, 0, 0.6, "riendo", y=FRENTE_Y, entra="nada", acciones=[
            {"at": 0.1, "cara": "sorpresa", "take": True}, {"at": "@celebró", "salta": True, "pose": "arriba", "cara": "riendo"},
            {"at": "@estaría", "pose": "pulgar", "mira": "camara"}, {"at": "@Primero", "mira": "arriba", "pose": "normal"},
            {"at": "@último", "cara": "burla", "pose": "senala_izq"}]),
    ]),
    # 4 · LAS REGLAS: el 13 de noviembre, y corregimos el 9
    dict(id="reglas", fondo={"tipo": "plano", "color": (28, 52, 110)}, animo="curioso", trans="papel", footnote=F_FORMATO, lines=[
        V("Las cuatro saldrán el mismo día: el 13 de noviembre, una cada hora.", "normal"),
        V("Ojo: no el 9, como se dijo al principio.", "remate", 0.1),
        V("Hasta noventa minutos, sin cortes y con dos periodistas verificando datos.", "normal", 0.15),
    ], camara=[plano(0, "general", [540, 900], 0), plano("@Ojo", "general", [540, 1000], 0.4, zoom=1.06),
               plano("@noventa", "general", [540, 850], 0.5)],
       elements=[
        rot("LAS 4, EL MISMO DÍA", 540, 460, 0.15, 84, "blanco", golpe=True, out="@13-0.1"),
        rot("13 DE NOVIEMBRE", 540, 460, "@13", 104, "amarillo", golpe=True, out="@noventa-0.2"),
        etq("UNA CADA HORA", 540, 640, "@hora", "rojo", 0.85, hud=True, out="@noventa-0.2"),
        rot("EL 9", 300, 900, "@9", 120, "blanco", golpe=True, out="@noventa-0.2"),
        sello("CORREGIDO", "rojo", 1000, "@principio", x=300, out="@noventa-0.2"),
        obj("cartel", 540, 700, "@noventa-0.1", 1.5, hud=True, entra="crece", sfx="papel", dibuja=2.2,
            props={"lineas": ["HASTA 90 MINUTOS", "SIN CORTES", "2 PERIODISTAS VERIFICAN"]}),
        quien("piz", 820, 0, 0.62, "ilusionado", y=1600, entra="nada", acciones=[
            {"at": 0.2, "pose": "saluda", "mira": "camara"}, {"at": "@mismo", "pose": "senala_arriba", "mira": "arriba"},
            {"at": "@13", "salta": True, "pose": "senala", "mira": "arriba"}, {"at": "@Ojo", "cara": "pensativo", "pose": "senala_izq", "mira": "izq"},
            {"at": "@principio", "cara": "burla"}, {"at": "@noventa", "cara": "sorpresa", "mira": "arriba"},
            {"at": "@verificando", "cara": "idea", "objeto": "lupa", "mira": "camara"}]),
    ]),
    # 5 · NO ES LO ÚNICO: el calendario de noviembre
    dict(id="calendario", fondo="oficina", animo="tension", trans="barrido", footnote=F_DEBATES, lines=[
        V("Y no es lo único que ha aceptado esta semana.", "normal"),
        V("El 16, cara a cara con Feijóo en Telecinco y Cuatro.", "normal", 0.1),
        V("El 26, el debate a cuatro… que aún no tiene cadena: el PSOE quiere RTVE y el PP, Atresmedia.", "normal", 0.1),
        V("Y el 29, votas tú.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 950], 0), plano("@16", "general", [540, 900], 0.5, zoom=1.05),
               plano("@26", "general", [540, 950], 0.5, zoom=1.05), plano("@29", "general", [540, 950], 0.5)],
       elements=[
        obj("calendario", 540, 760, 0.2, 0.55, id="calendario", entra="cae", sfx="golpe",
            props={"mes": "NOVIEMBRE", "inicio": 6, "dias": 30, "marcados": [13], "colores": {13: "amarillo"}}),
        {**obj("calendario", 540, 760, "@16", 0.55, entra="nada",
               props={"mes": "NOVIEMBRE", "inicio": 6, "dias": 30, "marcados": [13, 16], "colores": {13: "amarillo", 16: "rojo"}}), "out": "@26"},
        {**obj("calendario", 540, 760, "@26", 0.55, entra="nada",
               props={"mes": "NOVIEMBRE", "inicio": 6, "dias": 30, "marcados": [13, 16, 26],
                      "colores": {13: "amarillo", 16: "rojo", 26: "naranja"}}), "out": "@29"},
        obj("calendario", 540, 760, "@29", 0.55, entra="nada",
            props={"mes": "NOVIEMBRE", "inicio": 6, "dias": 30, "marcados": [13, 16, 26, 29],
                   "colores": {13: "amarillo", 16: "rojo", 26: "naranja", 29: "verde"}}),
        etq("16 · CARA A CARA", 540, 1160, "@16", "rojo", 0.75, out="@26"),
        etq("26 · ¿RTVE O ATRESMEDIA?", 540, 1160, "@26", "naranja", 0.75, out="@29"),
        etq("29 · VOTAS TÚ", 540, 1160, "@29", "verde", 0.85),
        quien("sanchez", 250, 0, 0.55, "normal", y=1640, entra="nada", acciones=[
            {"at": 0.2, "pose": "senala_arriba", "mira": "arriba"}, {"at": "@aceptado", "pose": "pulgar", "cara": "ilusionado"}, {"at": "@Feijóo", "mira": "der", "pose": "jarras"},
            {"at": "@cadena", "cara": "pensativo", "pose": "encoge"}, {"at": "@29", "cara": "sorpresa", "mira": "camara"}]),
        quien("feijoo", 1300, "@Feijóo-0.4", 0.55, "serio", y=1640, entra="nada", acciones=[
            {"at": "@Feijóo", "x": 830, "dur": 0.6}, {"at": "@Telecinco", "mira": "izq", "pose": "jarras"},
            {"at": "@Atresmedia", "pose": "senala", "cara": "burla"}, {"at": "@29", "mira": "camara", "cara": "sorpresa"}]),
    ]),
    # 6 · FINAL: sin cortes, ¿quién sale mejor parado?
    dict(id="final", fondo="estudio", animo="final", trans="zoom", footnote="Pregunta a la audiencia", lines=[
        V("Noventa minutos sin cortes y con verificadores. ¿Quién saldrá mejor parado? Te leo.", "normal"),
        V("Y síguenos: el 13, te lo contamos con datos.", "energia", 0.15),
    ], camara=[plano(0, "general", [540, 1150], 0), plano("@parado", "general", [540, 1100], 0.5, zoom=1.06),
               plano("@síguenos", "medio", "wild", 0.5, aire=240)],
       elements=[
        *sillas(0),
        sentado("colau", 150, acciones=[{"at": "@parado", "cara": "pensativo"}]),
        sentado("sanchez", 400, acciones=[{"at": "@parado", "cara": "burla", "giro": -0.8}]),
        sentado("feijoo", 680, acciones=[{"at": "@parado", "cara": "serio"}]),
        sentado("abascal", 930, acciones=[{"at": "@parado", "cara": "esceptica"}]),
        obj("microfono", 760, 1330, 0, 0.5, entra="nada", props={"encendido": True}),
        quien("wild", 540, 0, 0.6, "ilusionado", y=FRENTE_Y, entra="nada", acciones=[
            {"at": "@verificadores", "pose": "senala", "mira": "arriba"}, {"at": "@parado", "mira": "camara", "pose": "piensa"},
            {"at": "@síguenos", "pose": "saluda", "cara": "riendo"}, {"at": "@datos", "salta": True}]),
        rot("¿QUIÉN GANA?", 540, 560, "@parado", 110, "amarillo", golpe=True, out="@síguenos-0.3", fx=[{"at": "@leo", "do": "latir"}]),
        rot("SÍGUENOS", 540, 560, "@síguenos", 110, "amarillo"),
    ]),
]

if __name__ == "__main__":
    episodio("sanchez_acepta_wild", "Y Sánchez dijo sí", scenes,
             {"t": 9.1, "titulo": "Y Sánchez dijo sí", "capitulo": None},
             ["The Objective (23/10/2026): Sánchez acepta el último día; «Ahí estaré»; Wild: «4/4»; orden de aceptación",
              "El Debate (23/10/2026): «Acuérdate de que mi lado bueno es el izquierdo»",
              "elDiario.es (23/10/2026, act. 24/10) y Extradigital: emisión el 13/11, una cada hora, 50-90 min, sin edición, dos verificadores",
              "elDiario.es (22/10/2026): cara a cara en Mediaset el 16/11; debate a cuatro el 26/11 sin cadena acordada",
              "Corrige la fecha «desde el 9 de noviembre» de los capítulos anteriores",
              "Personajes dibujados como pizarras, sin caricatura; las frases de Sánchez son literales y con otra voz"],
             ("✅ Último día del plazo y Sánchez dice SÍ: «Gracias por la invitación. Ahí estaré»\n"
              "😂 Y al realizador: «Acuérdate de que mi lado bueno es el izquierdo»\n"
              "🎙️ Jordi Wild: «Pues ya estaría: 4/4» (Feijóo, Abascal, Colau y Sánchez)\n"
              "📅 Las cuatro entrevistas, el 13 de noviembre, una cada hora (ojo: no el 9)\n"
              "⏱️ Hasta 90 minutos, sin cortes y con 2 periodistas verificando datos\n"
              "🗓️ 16N cara a cara en Mediaset · 26N debate a cuatro (¿RTVE o Atresmedia?) · 29N votas tú\n"
              "💬 ¿Quién saldrá mejor parado sin cortes? Te leo 👇\n"
              "🔔 Síguenos · 📚 Fuentes en comentarios"),
             "📚 Fuentes: The Objective 23/10/2026 · El Debate 23/10/2026 · elDiario.es 22 y 24/10/2026 · Extradigital. "
             "¿Ves un error? Dínoslo.",
             ["#JordiWild", "#TheWildProject", "#Sánchez", "#29N", "#elecciones", "#debate", "#Feijóo", "#Abascal", "#pizarrapublica"],
             series_tag="EXPLICADO FÁCIL")
