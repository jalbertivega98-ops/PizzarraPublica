#!/usr/bin/env python3
"""«La guerra de los debates» (martes 20/10/2026, 15:00). Mundo dibujado: platós de tele y el calendario de noviembre.

Guion y fuentes: /mnt/project-files/insta/guiones/lunes_martes_19_20oct.md
  Propuestas de las cadenas (Libertad Digital 05/10/2026): RTVE cara a cara 17/11, portavoces 23/11, a cuatro 26/11;
    Atresmedia a cuatro 18/11 y cara a cara 23/11; Mediaset un cara a cara.
  Carta del PP (Alerta Siete 10/10/2026, Infobae 09/10/2026): cara a cara en Mediaset el 16/11, debate a varias bandas
    en Atresmedia el 26/11 y en RTVE solo el de portavoces (23/11). Solo el PP ha confirmado esas fechas.
  En 2023 Feijóo no acudió al debate a cuatro (Moncloa.com 09/10/2026).
  PSOE (Infobae 09/10/2026; El Constitucional): Sánchez irá a todos y Feijóo no decide dónde ni con quién.
  Vox (Moncloa.com 09/10/2026): los debates deben reflejar el mapa parlamentario; 33 diputados.
  Noviembre de 2026: el día 1 es domingo (16 y 23 lunes, 26 jueves).
"""
from _mundo import *  # noqa: F401,F403

RTVE, ATRES, MEDIA = (40, 90, 170), (230, 120, 30), (60, 150, 90)
CADENAS = [(200, "RTVE", RTVE), (540, "ATRESMEDIA", ATRES), (880, "MEDIASET", MEDIA)]
FLD = "Libertad Digital 05/10/2026 · propuestas de las cadenas"
FPP = "Alerta Siete 10/10/2026 · Infobae 09/10/2026 (carta del PP)"


def teles(at=0.0, y=800, s=0.42, entra="nada", ids=("t_rtve", "t_atres", "t_media")):
    return [obj("tele", x, y, at if entra == "nada" else at + i * 0.2, s, id=tid, entra=entra, sfx="pop" if entra != "nada" else None,
                props={"texto": tx, "color": col}) for i, ((x, tx, col), tid) in enumerate(zip(CADENAS, ids))]


def cal(at, marcados, colores, tachados=(), y=620, s=0.5, **kw):
    return obj("calendario", 540, y, at, s, hud=True, entra="nada", dibuja=0.8,
               props={"marcados": marcados, "colores": colores, "tachados": list(tachados)}, **kw)


scenes = [
    # 1 · GANCHO: tres teles escupen invitaciones; el contador sube a 6
    dict(id="gancho", fondo="plato", animo="tension", footnote=FLD, lines=[
        V("Tres cadenas, seis debates propuestos…", "energia"),
        V("y todavía nadie sabe cuáles habrá.", "remate", 0.1),
        V("Quédate, que al final eliges tú.", "normal", 0.15),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@seis", "general", [540, 1000], 0.5, zoom=1.05),
               plano("@nadie", "medio", "piz", 0.5, aire=220), plano("@eliges", "general", [540, 1000], 0.4)],
       elements=[
        *teles(0.1, entra="cae"),
        obj("contador", 540, 1180, "@seis", 0.7, hud=True, entra="pop", sfx="kaching", props={"valor": 6, "sufijo": " DEBATES", "ancho": 760}),
        quien("piz", 540, 0, 0.5, "sorpresa", y=1560, entra="nada", acciones=[
            {"at": "@cadenas", "mira": "arriba"}, {"at": "@nadie", "cara": "confundido", "pose": "encoge", "mira": "camara"},
            {"at": "@eliges", "pose": "senala", "cara": "riendo", "mira": "camara"}]),
        *[obj("invitacion", x, 1000, "@propuestos+%.1f" % (i * 0.2), 0.3, entra="cae", sfx="papel", flota=True,
              props={"texto": "DEBATE"}) for i, (x, _, _) in enumerate(CADENAS)],
    ]),
    # 2 · RTVE propone tres fechas
    dict(id="rtve", fondo="plato", animo="curioso", trans="corte", footnote=FLD, lines=[
        V("RTVE propuso tres: cara a cara el 17, portavoces el 23 y debate a cuatro el 26 de noviembre.", "normal"),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@portavoces", "general", [540, 900], 0.6, zoom=1.06)],
       elements=[
        cal(0, [17, 23, 26], {17: RTVE, 23: RTVE, 26: RTVE}),
        obj("tele", 540, 1200, 0, 0.55, id="t_rtve", entra="nada", props={"texto": "RTVE", "color": RTVE},
            acciones=[{"at": "@17", "salta": True}, {"at": "@23", "salta": True}, {"at": "@26", "salta": True}]),
        etq("CARA A CARA · 17", 260, 1560, "@17", "azul", 0.55, hud=True),
        etq("PORTAVOCES · 23", 540, 1660, "@23", "azul", 0.55, hud=True),
        etq("A CUATRO · 26", 820, 1560, "@26", "azul", 0.55, hud=True),
    ]),
    # 3 · Atresmedia y Mediaset
    dict(id="privadas", fondo="plato", animo="curioso", trans="barrido", footnote=FLD, lines=[
        V("Atresmedia, dos: debate a cuatro el 18 y cara a cara el 23.", "normal"),
        V("Mediaset, un cara a cara.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@Mediaset", "general", [700, 1000], 0.5)],
       elements=[
        cal(0, [17, 18, 23, 26], {17: RTVE, 18: ATRES, 23: ATRES, 26: RTVE}),
        obj("tele", 300, 1200, 0, 0.5, entra="nada", props={"texto": "ATRESMEDIA", "color": ATRES},
            acciones=[{"at": "@18", "salta": True}, {"at": "@23", "salta": True}]),
        obj("tele", 790, 1200, "@Mediaset", 0.5, entra="cae", sfx="golpe", props={"texto": "MEDIASET", "color": MEDIA},
            acciones=[{"at": "@cara#2", "tiembla": True}]),
        rot("¿FECHA?", 790, 1560, "@un", 80, "amarillo", golpe=True),
    ]),
    # 4 · Feijóo elige con su rotulador
    dict(id="feijoo", fondo="oficina", animo="tension", trans="iris", footnote=FPP, lines=[
        V("Feijóo ha elegido: cara a cara en Mediaset el 16, debate a cuatro en Atresmedia el 26…", "normal"),
        V("y en RTVE, solo el de portavoces.", "remate", 0.1),
    ], camara=[plano(0, "medio", "feijoo", 0, aire=220), plano("@Mediaset", "general", [540, 900], 0.6),
               plano("@RTVE", "general", [540, 900], 0.4, zoom=1.06)],
       elements=[
        cal("@elegido", [16, 23, 26], {16: MEDIA, 23: RTVE, 26: ATRES}, tachados=[17, 18], y=560, s=0.55),
        quien("feijoo", 840, 0, 0.5, "ilusionado", y=1560, entra="nada", acciones=[
            {"at": "@elegido", "pose": "senala_izq", "mira": "izq"}, {"at": "@16", "cara": "riendo"},
            {"at": "@26", "pose": "pulgar"}, {"at": "@portavoces", "cara": "serio", "pose": "cruzados"}]),
        sello("SOLO LO CONFIRMA EL PP", "naranja", 1180, "@solo"),
    ]),
    # 5 · Primera vez con Abascal (en 2023 no fue)
    dict(id="abascal", fondo="plato", animo="comico", trans="corte", footnote="Alerta Siete 10/10/2026 · Moncloa.com 09/10/2026", lines=[
        V("Y por primera vez acepta debatir con Abascal,", "normal"),
        V("después de no ir al debate a cuatro de 2023.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 1050], 0), plano("@Abascal", "general", [700, 1050], 0.4, zoom=1.06),
               plano("@2023", "general", [540, 1000], 0.5)],
       elements=[
        quien("feijoo", 360, 0, 0.5, "normal", y=1290, entra="nada", acciones=[{"at": "@Abascal", "mira": "abascal", "cara": "serio"}]),
        quien("abascal", 1300, "@debatir", 0.5, "riendo", y=1290, entra="nada", acciones=[
            {"at": "@debatir", "x": 740, "dur": 0.8}, {"at": "@Abascal", "mira": "feijoo", "pose": "saluda"}]),
        obj("atril", 360, SUELO_ATRIL + 60, 0, 0.55, entra="nada", props={"texto": "PP", "color": "pp"}),
        obj("atril", 740, SUELO_ATRIL + 60, "@debatir", 0.55, entra="crece", sfx="pop", props={"texto": "VOX", "color": "vox"}),
        rot("2023: NO FUE", 540, 600, "@2023", 96, "amarillo", golpe=True),
        sello("PRIMERA VEZ", "verde", 760, "@vez"),
    ]),
    # 6 · El PSOE: a todos, pero no decide Feijóo
    dict(id="psoe", fondo="plato", animo="tension", trans="pan", footnote="Infobae 09/10/2026 · El Constitucional", lines=[
        V("El PSOE dice que Sánchez irá a todos…", "normal"),
        V("pero que dónde y con quién no lo decide Feijóo.", "remate", 0.1),
    ], camara=[plano(0, "medio", "sanchez", 0, aire=220), plano("@dónde", "general", [540, 1000], 0.5)],
       elements=[
        *teles(0, y=760, s=0.36),
        quien("sanchez", 400, 0, 0.5, "ilusionado", y=1500, entra="nada", acciones=[
            {"at": "@todos", "pose": "arriba", "cara": "riendo"}, {"at": "@dónde", "pose": "senala", "mira": "der", "cara": "serio"}]),
        quien("feijoo", 1300, "@dónde-0.4", 0.42, "sorpresa", y=1500, entra="nada", acciones=[
            {"at": "@dónde", "x": 820, "dur": 0.5}, {"at": "@Feijóo", "take": True}]),
        obj("bocadillo", 540, 980, "@dónde", 0.7, hud=True, entra="pop", props={"lineas": ["«¿Dónde y con quién?", "No lo decide Feijóo»"]}),
        sello("DECLARACIÓN", "azul", 1180, "@decide"),
    ]),
    # 7 · Vox: que reflejen el Congreso (33 diputados)
    dict(id="vox", fondo={"tipo": "plano", "color": (28, 52, 110)}, animo="curioso", trans="papel", footnote="Moncloa.com 09/10/2026", lines=[
        V("Vox pide que los debates reflejen el Congreso, donde es la tercera fuerza, con 33 diputados.", "normal"),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@33", "general", [540, 900], 0.5, zoom=1.08)],
       elements=[
        edif("congreso", 540, 0, 0.7, dibuja=1.0),
        quien("abascal", 820, 0, 0.45, "normal", y=1560, entra="nada", acciones=[
            {"at": "@reflejen", "pose": "senala_izq", "mira": "izq"}, {"at": "@33", "cara": "ilusionado", "pose": "pulgar"}]),
        rot("3.ª FUERZA", 540, 500, "@tercera", 96, "amarillo", golpe=True),
        obj("contador", 540, 680, "@33", 0.6, hud=True, entra="pop", sfx="kaching", props={"valor": 33, "sufijo": " DIPUTADOS", "ancho": 760}),
    ]),
    # 8 · PREGUNTA: ¿2 o 4?
    dict(id="pregunta", fondo="salon", animo="final", trans="iris", footnote="Pregunta a la audiencia", lines=[
        V("Y ahora tú: si solo pudieras ver uno, ¿cuál verías: el cara a cara o el debate a cuatro?", "normal"),
        V("Escribe 2 o 4 en comentarios.", "energia", 0.1),
        V("Síguenos y te contamos cuándo se cierran las fechas.", "normal", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@cara", "general", [300, 950], 0.5, zoom=1.08),
               plano("@cuatro", "general", [780, 950], 0.5, zoom=1.08), plano("@Escribe", "general", [540, 1000], 0.4),
               plano("@Síguenos", "medio", "piz", 0.5, aire=220)],
       elements=[
        obj("tele", 290, 860, 0, 0.55, entra="nada", props={"texto": "2", "color": "pp"}),
        obj("tele", 790, 860, 0, 0.55, entra="nada", props={"texto": "4", "color": "naranja"}),
        quien("piz", 540, 0, 0.62, "pensativo", y=1640, entra="nada", acciones=[
            {"at": "@cara", "mira": "izq", "pose": "piensa"}, {"at": "@cuatro", "mira": "der"},
            {"at": "@Escribe", "mira": "camara", "cara": "ilusionado", "pose": "senala"},
            {"at": "@Síguenos", "pose": "saluda", "cara": "riendo"}, {"at": "@fechas", "salta": True}]),
        rot("¿2 O 4?", 540, 480, "@Escribe", 130, "amarillo", golpe=True, out="@Síguenos-0.3", fx=[{"at": "@comentarios", "do": "latir"}]),
        rot("SÍGUENOS", 540, 480, "@Síguenos", 110, "amarillo"),
    ]),
]

if __name__ == "__main__":
    episodio("guerra_debates", "La guerra de los debates", scenes,
             {"t": 2.4, "titulo": "La guerra de los debates", "capitulo": None},
             ["Libertad Digital (05/10/2026): propuestas de RTVE, Atresmedia y Mediaset para el 29N",
              "Alerta Siete (10/10/2026) e Infobae (09/10/2026): carta del PP con las fechas que acepta",
              "Infobae (09/10/2026) y El Constitucional: el PSOE irá a todos los debates",
              "Moncloa.com (09/10/2026): posición de Vox y antecedente de 2023",
              "Personajes dibujados como pizarras, sin caricatura"],
             ("📺 Tres cadenas, seis debates propuestos… y todavía nadie sabe cuáles habrá\n"
              "🔵 RTVE: cara a cara el 17, portavoces el 23 y a cuatro el 26\n"
              "🟠 Atresmedia: a cuatro el 18 y cara a cara el 23 · 🟢 Mediaset: un cara a cara\n"
              "✍️ El PP elige: Mediaset el 16, Atresmedia el 26 y en RTVE solo portavoces\n"
              "🗣️ PSOE: «irá a todos», pero no decide Feijóo dónde · Vox: que reflejen el Congreso\n"
              "💬 ¿Verías el cara a cara (2) o el debate a cuatro (4)? Te leemos 👇\n"
              "🔔 Síguenos · 📚 Fuentes en comentarios"),
             "📚 Fuentes: Libertad Digital 05/10/2026 · Alerta Siete 10/10/2026 · Infobae 09/10/2026 · El Constitucional · "
             "Moncloa.com 09/10/2026. ¿Ves un error? Dínoslo.",
             ["#29N", "#debate", "#DebateElectoral", "#elecciones", "#Sánchez", "#Feijóo", "#Abascal", "#pizarrapublica"],
             series_tag="EXPLICADO FÁCIL")
