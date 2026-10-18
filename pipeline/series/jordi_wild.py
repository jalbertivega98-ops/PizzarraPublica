#!/usr/bin/env python3
"""«Jordi Wild invita a los candidatos: ¿quién ha dicho que sí?» (lunes 19/10/2026, 15:00). Mundo dibujado: estudio de podcast.

Guion y fuentes: /mnt/project-files/insta/guiones/lunes_martes_19_20oct.md
  Propuesta, condiciones, «cuando quiera» (Feijóo) y «Cuenta conmigo» (Abascal): Libertad Digital 09/10/2026.
  Sánchez sin respuesta; su entorno lo estudia con el equipo de campaña; «entrevista-masaje»: Extradigital 15/10/2026.
  Plazo de unos diez días y emisión desde el 9 de noviembre: El Confidencial Digital 15/10/2026.
  La cuarta silla (espacio a la izquierda del PSOE) sin cerrar: ActualTV 15/10/2026. Norma del proyecto: solo PSOE, PP y Vox.
"""
from _mundo import *  # noqa: F401,F403

SILLAS = [(150, "gris", "?"), (400, (225, 30, 40), "SÁNCHEZ"), (680, (0, 104, 180), "FEIJÓO"), (930, (90, 175, 40), "ABASCAL")]
FONDO_Y, FRENTE_Y = 1250, 1640
FLD = "Libertad Digital 09/10/2026"
FECD = "El Confidencial Digital 15/10/2026 · Extradigital 15/10/2026"


def sillas(at=0.0, ids=("s_izq", "s_psoe", "s_pp", "s_vox"), vacias=True, entra="nada", dibujo=None):
    out = []
    for i, ((x, col, tx), sid) in enumerate(zip(SILLAS, ids)):
        d = obj("silla", x, FONDO_Y, at + i * 0.12 if entra != "nada" else at, 0.5, id=sid, entra=entra,
                props={"color": col, "texto": tx})
        if dibujo:
            d["dibuja"] = dibujo
        out.append(d)
    return out


scenes = [
    # 1 · GANCHO: el estudio con cuatro sillas vacías; Jordi al micro
    dict(id="gancho", fondo="estudio", animo="tension", footnote=FLD, lines=[
        V("Un youtuber ha puesto a los candidatos contra las cuerdas:", "energia"),
        V("o vienen todos… o no viene nadie.", "remate", 0.15),
    ], camara=[plano(0, "medio", "wild", 0, aire=200), plano("@cuerdas", "general", [540, 1150], 0.7),
               plano("@todos", "general", [540, 1150], 0.4, zoom=1.08), plano("@nadie", "medio", "wild", 0.4, aire=200)],
       elements=[
        *sillas(0.3, entra="crece"),
        obj("microfono", 700, 1330, 0, 0.5, id="micro", entra="nada", props={"encendido": True}),
        quien("wild", 540, 0, 0.6, "burla", y=FRENTE_Y, entra="nada", acciones=[
            {"at": "@candidatos", "pose": "senala", "mira": "der"}, {"at": "@todos", "pose": "jarras", "cara": "serio"},
            {"at": "@nadie", "pose": "encoge", "cara": "burla", "mira": "camara"}]),
        rot("¿TODOS O NADIE?", 540, 420, "@todos", 100, "amarillo", golpe=True),
    ]),
    # 2 · LA INVITACIÓN: las tres condiciones salen volando como cartas
    dict(id="condiciones", fondo="calle", animo="curioso", trans="papel", footnote=FLD, lines=[
        V("Jordi Wild ha invitado a los cuatro candidatos a The Wild Project.", "normal"),
        V("Tres condiciones: sin preguntas pactadas, sin sustitutos…", "normal", 0.1),
        V("y si uno dice que no, no hay entrevistas para nadie.", "remate", 0.1),
    ], camara=[plano(0, "general", dur=0), plano("@condiciones", "general", [540, 760], 0.6, zoom=1.05),
               plano("@dice", "medio", "piz", 0.5, aire=220)],
       elements=[
        quien("piz", -200, 0, 0.55, "ilusionado", entra="nada", objeto="papeleta", pose="sostiene", acciones=[
            {"at": 0.2, "x": 300, "dur": 0.9, "corre": True}, {"at": "@Project", "pose": "saluda", "cara": "riendo"},
            {"at": "@dice", "cara": "susto", "take": True}, {"at": "@nadie", "tropieza": True}]),
        *[obj("invitacion", 160 + i * 250, 520 - (i % 2) * 60, "@cuatro+%.2f" % (i * 0.15), 0.5, id=f"inv{i}", entra="cae",
              sfx="papel", props={"texto": "INVITACIÓN"}, flota=True) for i in range(4)],
        obj("cartel", 540, 760, "@condiciones", 0.8, hud=True, entra="crece", sfx="pop",
            props={"lineas": ["SIN PREGUNTAS PACTADAS", "SIN SUSTITUTOS", "O TODOS O NADIE"]}, dibuja=1.4),
    ]),
    # 3 · LOS DOS SÍ: Feijóo y Abascal llegan corriendo a sus sillas
    dict(id="si", fondo="estudio", animo="alegre", trans="iris", footnote=FLD, lines=[
        V("Feijóo contestó a las pocas horas: «cuando quiera».", "normal"),
        V("Abascal, en X: «Cuenta conmigo».", "normal", 0.15),
    ], camara=[plano(0, "general", [600, 1150], 0), plano("@quiera", "medio", "feijoo", 0.5, aire=220),
               plano("@Abascal", "general", [700, 1150], 0.5), plano("@conmigo", "medio", "abascal", 0.4, aire=220)],
       elements=[
        *sillas(0),
        quien("feijoo", 1300, 0, 0.42, "ilusionado", y=FONDO_Y + 60, entra="nada", acciones=[
            {"at": 0.1, "x": 680, "y": FONDO_Y + 60, "dur": 1.0, "corre": True}, {"at": "@quiera", "pose": "pulgar", "cara": "riendo"},
            {"at": "@Abascal", "mira": "der"}]),
        quien("abascal", 1300, "@Abascal-0.3", 0.42, "normal", y=FONDO_Y + 60, entra="nada", acciones=[
            {"at": "@Abascal", "x": 930, "dur": 0.9, "corre": True}, {"at": "@Cuenta", "pose": "saluda", "cara": "riendo"},
            {"at": "@conmigo", "salta": True}]),
        sello("ACEPTA", "verde", 1450, "@quiera", x=680),
        sello("ACEPTA", "verde", 1560, "@conmigo", x=900),
        obj("bocadillo", 700, 420, "@contestó", 0.7, hud=True, entra="pop", props={"texto": "«Cuando quiera»"}, out="@Abascal"),
        obj("bocadillo", 760, 420, "@Cuenta", 0.7, hud=True, entra="pop", props={"texto": "«Cuenta conmigo»"}),
    ]),
    # 4 · SÁNCHEZ, PENDIENTE: con la invitación en la mano, el reloj corre
    dict(id="sanchez", fondo="oficina", animo="tension", trans="corte", footnote=FECD, lines=[
        V("¿Y Sánchez? Su entorno dice que lo está estudiando con el equipo de campaña.", "normal"),
        V("Según El Confidencial Digital, Wild le da unos diez días.", "normal", 0.15),
        V("Y avisa: no será una entrevista-masaje.", "remate", 0.15),
    ], camara=[plano(0, "medio", "sanchez", 0, aire=220), plano("@estudiando", "general", [540, 1000], 0.6),
               plano("@diez", "general", [540, 900], 0.5, zoom=1.06), plano("@será", "medio", "wild", 0.4, aire=200)],
       elements=[
        quien("sanchez", 360, 0, 0.55, "pensativo", entra="nada", acciones=[
            {"at": 0.1, "pose": "piensa"}, {"at": "@estudiando", "mira": "invitacion"},
            {"at": "@diez", "cara": "preocupado", "mira": "reloj"}, {"at": "@será", "cara": "susto", "take": True}]),
        obj("invitacion", 620, 900, 0.2, 0.5, id="invitacion", entra="pop", sfx="papel", props={"texto": "INVITACIÓN"}, flota=True),
        sello("PENDIENTE", "naranja", 560, "@estudiando", x=380),
        obj("reloj", 800, 600, "@diez", 0.8, id="reloj", entra="cae", sfx="golpe", props={"velocidad": 4}),
        etq("~10 DÍAS", 800, 340, "@días", "amarillo", 0.9, hud=True),
        quien("wild", 1300, "@avisa-0.4", 0.5, "burla", entra="nada", acciones=[
            {"at": "@avisa", "x": 860, "dur": 0.6}, {"at": "@será", "pose": "senala_izq", "mira": "sanchez"}]),
        sello("DECLARACIÓN", "azul", 760, "@será", x=760),
    ]),
    # 5 · LA CUARTA SILLA Y LA FECHA: la silla gris sigue vacía; noviembre se marca con rotulador
    dict(id="fecha", fondo={"tipo": "plano", "color": (28, 52, 110)}, animo="curioso", trans="papel",
         footnote="ActualTV 15/10/2026 · El Confidencial Digital 15/10/2026", lines=[
        V("La cuarta silla, la de la izquierda, tampoco está cerrada.", "normal"),
        V("Si sale adelante, las entrevistas se emitirían a partir del 9 de noviembre.", "normal", 0.15),
    ], camara=[plano(0, "general", [540, 1100], 0), plano("@emitirían", "general", [540, 960], 0.7)],
       elements=[
        obj("silla", 300, 1560, 0, 0.55, entra="nada", props={"color": "gris", "texto": "?"}, acciones=[{"at": "@cerrada", "tiembla": True}]),
        quien("pizon", 700, 0, 0.5, "confundido", y=1560, entra="nada", acciones=[
            {"at": "@cuarta", "mira": "izq", "pose": "encoge"}, {"at": "@emitirían", "mira": "arriba", "cara": "ilusionado"}]),
        obj("calendario", 540, 760, "@Si", 0.62, entra="nada", dibuja=1.0,
            props={"marcados": [9], "colores": {9: "rojo"}}),
        rot("DESDE EL 9N", 540, 1130, "@9", 96, "amarillo", golpe=True),
        sello("SI SALE ADELANTE", "naranja", 1420, "@adelante"),
    ]),
    # 6 · FINAL: tres sillas llenas y una que espera
    dict(id="final", fondo="estudio", animo="final", trans="zoom", footnote="Pregunta a la audiencia", lines=[
        V("¿Crees que Sánchez irá? Escribe SÍ o NO, te leo.", "normal"),
        V("Y síguenos para saber si la silla se llena.", "energia", 0.15),
    ], camara=[plano(0, "general", [540, 1150], 0), plano("@SÍ", "general", [450, 1100], 0.5, zoom=1.08),
               plano("@síguenos", "general", [540, 1150], 0.5)],
       elements=[
        *sillas(0),
        quien("feijoo", 680, 0, 0.42, "normal", y=FONDO_Y + 60, entra="nada", acciones=[{"at": "@Sánchez", "mira": "izq"}]),
        quien("abascal", 930, 0, 0.42, "normal", y=FONDO_Y + 60, entra="nada", acciones=[{"at": "@Sánchez", "mira": "izq"}]),
        obj("microfono", 720, 1330, 0, 0.5, entra="nada"),
        quien("wild", 520, 0, 0.6, "pensativo", y=FRENTE_Y, entra="nada", acciones=[
            {"at": "@irá", "mira": "camara", "pose": "piensa"}, {"at": "@síguenos", "pose": "saluda", "cara": "riendo"}]),
        rot("¿SÍ O NO?", 540, 560, "@SÍ", 110, "amarillo", golpe=True, out="@síguenos-0.3", fx=[{"at": "@leo", "do": "latir"}]),
        rot("SÍGUENOS", 540, 560, "@síguenos", 110, "amarillo", fx=[{"at": "@silla", "do": "latir"}]),
    ]),
]

if __name__ == "__main__":
    episodio("jordi_wild", "Jordi Wild invita a los candidatos", scenes,
             {"t": 2.0, "titulo": "Jordi Wild invita a los candidatos", "capitulo": None},
             ["Libertad Digital (09/10/2026): Feijóo y Abascal aceptan la invitación de Jordi Wild; condiciones del formato",
              "El Confidencial Digital (15/10/2026): plazo de unos diez días a Sánchez y emisión desde el 9 de noviembre",
              "Extradigital (15/10/2026): el entorno de Sánchez lo estudia; «no será una entrevista-masaje»",
              "ActualTV (15/10/2026): el candidato del espacio a la izquierda del PSOE, sin cerrar",
              "Personajes dibujados como pizarras, sin caricatura"],
             ("🎙️ Jordi Wild ha invitado a los candidatos a The Wild Project\n"
              "📜 Sus condiciones: sin preguntas pactadas, sin sustitutos… y o vienen todos o no viene nadie\n"
              "✅ Feijóo: «cuando quiera» · ✅ Abascal: «Cuenta conmigo»\n"
              "⏳ Sánchez: su entorno lo estudia; Wild le da unos 10 días\n"
              "📅 Si sale adelante, desde el 9 de noviembre\n"
              "💬 ¿Irá Sánchez? SÍ o NO 👇\n"
              "🔔 Síguenos · 📚 Fuentes en comentarios"),
             "📚 Fuentes: Libertad Digital 09/10/2026 · El Confidencial Digital 15/10/2026 · Extradigital 15/10/2026 · ActualTV 15/10/2026. "
             "¿Ves un error? Dínoslo.",
             ["#JordiWild", "#TheWildProject", "#29N", "#elecciones", "#Sánchez", "#Feijóo", "#Abascal", "#pizarrapublica"],
             series_tag="EXPLICADO FÁCIL")
