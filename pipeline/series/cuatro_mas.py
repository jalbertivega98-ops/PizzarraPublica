#!/usr/bin/env python3
"""«¿Cuatro más?» (domingo 25/10/2026). Sánchez sale a correr con Carlos Cuerpo en su vídeo electoral; Piz le para
antes de «cuatro más» para repasar cómo fueron los ocho: dos tramos a favor (sueldo mínimo, empleo), dos en contra
(vivienda, Ábalos) y la meta del 29N con Feijóo y Abascal calentando.

Personajes: sanchez_corre (el Sánchez de joel con chándal azul y logo del PSOE) y cuerpo (chapa, sin caricatura).
Las frases de Sánchez y Cuerpo son literales y van con voz de «tele» (S, C); no imitan la suya.

Fuentes:
  elDiario.es directo 25/10/2026: vídeo electoral; Sánchez: «Todavía nos queda carrera. ¿Qué hacemos? ¿Cuatro más?»;
    Cuerpo: «Yo creo que sí. Estamos preparados»; «Llevamos ocho ya» (km = años en Moncloa).
  La7 TV / Europa Press 25/10/2026 (entrevista en El País): subirá el SMI antes del 29N; su mayor error en ocho años,
    «no ver la corrupción de Ábalos».
  Consejo de Ministros (nota de prensa, feb. 2026): SMI 2026 = 1.221 €/mes en 14 pagas; +66 % desde 2018 (735,90 €).
  INE, EPA 2T 2018 (paro 15,28 %, 19,34 M ocupados) y 2T 2026 (paro 9,87 %, 22,78 M ocupados).
  Idealista vía ESdiario 6/10/2026: vivienda usada +74,4 % desde junio de 2018; alquiler +45,2 %.
  Tribunal Supremo 22/06/2026: Ábalos condenado a 24 años y 3 meses.
  29/11/2026 − 25/10/2026 = 35 días.
"""
from _mundo import *  # noqa: F401,F403

F_VIDEO = "Vídeo de Sánchez en redes · elDiario.es 25/10/2026"
F_SMI = "Consejo de Ministros (feb. 2026) · El País 25/10/2026"
F_EPA = "INE · EPA 2º trimestre 2018 y 2026"
F_VIV = "Idealista (vía ESdiario 6/10/2026) · jun. 2018 - sep. 2026"
F_ABALOS = "Tribunal Supremo 22/06/2026 · El País / Europa Press 25/10/2026"
SUELO = 1340
ESC = 0.56


def S(text, pausa=None):
    """Frase literal de Sánchez: voz del canal procesada («tele»), no imita la suya."""
    return dict(V(text, "normal", pausa), efecto_voz="tele")


def C(text, pausa=None):
    """Frase literal de Carlos Cuerpo: la otra voz de «tele» (más aguda) para que no se confunda con Sánchez."""
    return dict(V(text, "normal", pausa), efecto_voz="tele2")


def corredor(q, x, at=0.0, cara="normal", acciones=(), scale=ESC, trota=True, **kw):
    return quien(q, x, at, scale, cara, y=SUELO, entra=kw.pop("entra", "nada"), trota=trota, acciones=list(acciones), **kw)


scenes = [
    # 1 · GANCHO: Sánchez trotando, «¿Cuatro más?», y Piz le para
    dict(id="gancho", fondo={"tipo": "parque", "velocidad": 340}, animo="alegre", footnote=F_VIDEO, lines=[
        V("Pedro Sánchez ha salido a correr… y lo ha subido a sus redes.", "energia"),
        S("«Todavía nos queda carrera. ¿Qué hacemos? ¿Cuatro más?»", 0.05),
        V("¡Para, para! Antes de cuatro más… ¿cómo han ido los ocho?", "remate", 0.1),
    ], camara=[plano(0, "general", [640, 1120], 0, zoom=1.3), plano("@Todavía", "general", [600, 1100], 0.6, zoom=1.2),
               plano("@Para", "general", [480, 1050], 0.4, zoom=1.05)],
       elements=[
        corredor("sanchez_corre", 640, 0, "riendo", acciones=[
            {"at": "@correr", "salta": True}, {"at": "@subido", "pose": "saluda", "mira": "camara"}, {"at": "@redes", "pose": "normal"}, {"at": "@Todavía", "cara": "ilusionado"}, {"at": "@Cuatro", "pose": "saluda", "cara": "riendo"},
            {"at": "@Para", "trota": False, "cara": "sorpresa", "take": True, "mira": "izq"}, {"at": "@ocho", "pose": "encoge", "cara": "pensativo"}]),
        corredor("piz", 250, 0, "preocupado", acciones=[
            {"at": 0.1, "objeto": "reloj"}, {"at": "@correr", "cara": "sorpresa"}, {"at": "@redes", "cara": "preocupado", "mira": "der"},
            {"at": "@Cuatro", "cara": "susto"},
            {"at": "@Para", "trota": False, "pose": "arriba", "cara": "indignado", "salta": True, "objeto": None},
            {"at": "@Antes", "pose": "senala", "cara": "pensativo", "mira": "der"}, {"at": "@ocho", "mira": "camara", "pose": "jarras"}]),
        rot("¿CUATRO MÁS?", 540, 470, "@Cuatro", 124, "amarillo", golpe=True, out="@Para-0.1"),
        pum("¡STOP!", 330, 820, "@Para", 0.9),
        rot("¿Y LOS OCHO?", 540, 470, "@ocho-0.2", 112, "blanco", golpe=True),
    ]),
    # 2 · LA SALIDA: Cuerpo se apunta; «llevamos ocho ya»
    dict(id="salida", fondo="parque", animo="comico", trans="corte", footnote=F_VIDEO, lines=[
        V("Va con Carlos Cuerpo, su vicepresidente.", "normal"),
        C("«Yo creo que sí. Estamos preparados».", 0.05),
        V("Y bromean: «Llevamos ocho ya». Ocho kilómetros… y ocho años en la Moncloa.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@Yo", "medio", "cuerpo", 0.5, aire=240),
               plano("@bromean", "general", [540, 950], 0.5), plano("@Moncloa", "general", [700, 1000], 0.6, zoom=1.05)],
       elements=[
        obj("arco", 540, SUELO - 20, 0, 0.92, entra="nada", dibuja=1.2, sfx="rotulador",
            props={"texto": "SALIDA", "sub": "JUNIO DE 2018", "color": "rojo"}),
        corredor("sanchez_corre", 420, 0, "ilusionado", trota=False, acciones=[
            {"at": "@Cuerpo", "mira": "der"}, {"at": "@preparados", "pose": "pulgar", "cara": "riendo"},
            {"at": "@ocho", "pose": "saluda", "mira": "camara"},
            {"at": "@Moncloa", "x": 1500, "corre": True, "dur": 1.1}]),
        corredor("cuerpo", 1400, 0, "normal", trota=False, acciones=[
            {"at": "@Cuerpo", "x": 680, "corre": True, "dur": 0.7}, {"at": "@Yo", "pose": "pulgar", "mira": "camara", "cara": "ilusionado"},
            {"at": "@bromean", "cara": "riendo", "mira": "izq"},
            {"at": "@Moncloa", "x": 1700, "corre": True, "dur": 1.1}]),
        corredor("piz", 160, 0, "pensativo", trota=False, acciones=[
            {"at": "@Cuerpo", "mira": "der"}, {"at": "@kilómetros", "pose": "piensa"}, {"at": "@años", "cara": "idea", "salta": True},
            {"at": "@Moncloa", "x": 1300, "corre": True, "dur": 1.4, "cara": "preocupado"}]),
        rot("8 KM = 8 AÑOS", 540, 420, "@kilómetros", 110, "amarillo", golpe=True),
    ]),
    # 3 · KM 1: el salario mínimo
    dict(id="smi", fondo="parque", animo="curioso", trans="barrido", footnote=F_SMI, lines=[
        V("Primer poste: el salario mínimo.", "normal"),
        V("En 2018, 736 euros al mes. Hoy, 1.221. Un 66 % más.", "energia", 0.1),
        V("Y promete otra subida antes del 29N.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@Hoy", "general", [560, 950], 0.5, zoom=1.04),
               plano("@promete", "medio", "sanchez_corre", 0.5, aire=280)],
       elements=[
        obj("poste", 860, SUELO, 0, 0.7, entra="nada", dibuja=0.8, props={"texto": "SUELDO", "numero": "KM 1"}),
        corredor("sanchez_corre", -300, 0, "ilusionado", trota=False, acciones=[
            {"at": 0.05, "x": 520, "corre": True, "dur": 0.8}, {"at": "@poste", "mira": "der"},
            {"at": "@Hoy", "objeto": "billete", "pose": "sostiene", "cara": "riendo"}, {"at": "@66", "pose": "arriba", "salta": True},
            {"at": "@promete", "objeto": None, "pose": "senala_arriba", "mira": "camara"}]),
        corredor("piz", -500, 0, "preocupado", trota=False, acciones=[
            {"at": 0.3, "x": 190, "corre": True, "dur": 0.9}, {"at": "@salario", "pose": "caidos", "cara": "preocupado"},
            {"at": "@2018", "mira": "arriba", "cara": "normal", "pose": "normal"}, {"at": "@66", "cara": "sorpresa", "take": True},
            {"at": "@promete", "cara": "pensativo", "mira": "der"}]),
        rot("SALARIO MÍNIMO", 540, 420, "@salario", 96, "blanco", golpe=True),
        etq("2018: 736 €", 540, 600, "@2018", "blanco", 0.95, hud=True, out="@Hoy-0.05"),
        obj("contador", 540, 600, "@Hoy", 0.95, hud=True, entra="pop", sfx="kaching", dibujo=1.3,
            props={"valor": 1221, "desde": 736, "sufijo": " €", "ancho": 640}),
        etq("+66 %", 540, 800, "@66", "verde", 0.9, hud=True),
        sello("PROMESA", "naranja", 960, "@29N", x=540),
    ]),
    # 4 · KM 2: el paro
    dict(id="paro", fondo="parque", animo="alegre", trans="barrido", footnote=F_EPA, lines=[
        V("Segundo poste: el paro.", "normal"),
        V("Del 15,3 % al 9,9 %. Y 3,4 millones de personas más trabajando.", "energia", 0.1),
        V("Este tramo… cuesta abajo.", "remate", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@millones", "general", [540, 960], 0.5, zoom=1.04),
               plano("@cuesta", "medio", "piz", 0.4, aire=260)],
       elements=[
        obj("poste", 880, SUELO, 0, 0.7, entra="nada", dibuja=0.8, props={"texto": "EMPLEO", "numero": "KM 2", "color": "verde"}),
        corredor("cuerpo", -300, 0, "normal", trota=False, acciones=[
            {"at": 0.05, "x": 600, "corre": True, "dur": 0.9}, {"at": "@paro", "pose": "senala_arriba", "mira": "arriba"},
            {"at": "@9,9", "cara": "ilusionado", "pose": "pulgar"}, {"at": "@trabajando", "mira": "camara", "pose": "saluda"}]),
        corredor("sanchez_corre", -600, 0, "riendo", trota=False, acciones=[
            {"at": 0.2, "x": 370, "corre": True, "dur": 0.9}, {"at": "@millones", "pose": "arriba", "salta": True}]),
        corredor("piz", -800, 0, "normal", trota=False, acciones=[
            {"at": 0.4, "x": 140, "corre": True, "dur": 0.9}, {"at": "@paro", "mira": "arriba"}, {"at": "@millones", "cara": "sorpresa"},
            {"at": "@cuesta", "cara": "riendo", "salta": True, "pose": "pulgar", "mira": "camara"}]),
        rot("PARO", 540, 400, "@paro", 104, "blanco", golpe=True),
        obj("barras", 540, 690, "@Del", 0.7, hud=True, entra="pop", sfx="pop", props={
            "barras": [{"texto": "2018", "valor": 15.3, "color": "gris"}, {"texto": "2026", "valor": 9.9, "color": "verde"}],
            "sufijo": " %", "tope": 18, "resalta": [1]}),
        etq("+3,4 MILLONES TRABAJANDO", 540, 1010, "@millones", "verde", 0.72, hud=True),
    ]),
    # 5 · LA CUESTA: la vivienda
    dict(id="cuesta", fondo={"tipo": "parque", "velocidad": 120}, animo="tension", trans="corte", footnote=F_VIV, lines=[
        V("Pero entonces llega la cuesta: la vivienda.", "tension"),
        V("Un piso usado cuesta hoy un 74 % más que en 2018. El alquiler, un 45 % más.", "normal", 0.1),
        V("Y aquí mucha gente se ha quedado sin aliento.", "remate", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@cuesta", "general", [540, 1000], 0.7, inclina=-7),
               plano("@aliento", "medio", "piz", 0.5, aire=240, inclina=-7)],
       elements=[
        corredor("sanchez_corre", 760, 0, "normal", trota="anda", acciones=[
            {"at": "@cuesta", "cara": "preocupado"}, {"at": "@74", "mira": "arriba"}]),
        corredor("cuerpo", 980, 0, "normal", trota="anda", acciones=[{"at": "@cuesta", "cara": "preocupado"}]),
        corredor("piz", 200, 0, "preocupado", trota="anda", acciones=[
            {"at": "@cuesta", "pose": "empuja", "cara": "preocupado"}, {"at": "@74", "cara": "susto"},
            {"at": "@alquiler", "cara": "indignado"}, {"at": "@aliento", "cara": "triste", "pose": "caidos", "trota": False}]),
        edif("casa", 470, 0, 0.32, cara="preocupado", acciones=[{"at": "@74", "cara": "susto"}, {"at": "@aliento", "cara": "triste"}]),
        rot("VIVIENDA", 540, 410, "@vivienda", 104, "blanco", golpe=True),
        etq("PISO +74 %", 300, 580, "@74", "rojo", 0.78, hud=True),
        etq("ALQUILER +45 %", 300, 740, "@45", "naranja", 0.78, hud=True),
        obj("grafica", 820, 660, "@usado", 0.85, hud=True, entra="pop", sfx="pop",
            dibujo=2.2, props={"valores": (1, 1.15, 1.3, 1.55, 1.74), "color": "rojo"}),
    ]),
    # 6 · LA PIEDRA: Ábalos
    dict(id="piedra", fondo="parque", animo="tension", trans="barrido", footnote=F_ABALOS, lines=[
        V("Y en el camino, una piedra: Ábalos. Su exministro, condenado por el Supremo a 24 años.", "tension"),
        V("Hoy, en El País, Sánchez dice que su mayor error en estos ocho años fue…", "normal", 0.1),
        S("«no ver la corrupción de Ábalos».", 0.05),
        V("Lo dice él.", "remate", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@condenado", "general", [600, 1050], 0.5, zoom=1.08),
               plano("@corrupción", "medio", "sanchez_corre", 0.5, aire=260), plano("@Lo", "general", [540, 1000], 0.4)],
       elements=[
        obj("piedra", 740, SUELO, 0, 0.62, entra="nada", dibuja=0.7, props={"texto": "ÁBALOS"}),
        corredor("sanchez_corre", -300, 0, "ilusionado", trota=False, acciones=[
            {"at": 0.05, "x": 470, "corre": True, "dur": 1.0}, {"at": "@piedra", "tropieza": True}, {"at": "@exministro", "mira": "der", "cara": "susto"},
            {"at": "@condenado", "cara": "preocupado", "mira": "der"}, {"at": "@País", "cara": "triste", "pose": "cabeza"},
            {"at": "@corrupción", "cara": "serio", "pose": "manos_juntas", "mira": "camara"}]),
        corredor("piz", -600, 0, "normal", trota=False, acciones=[
            {"at": 0.3, "x": 180, "corre": True, "dur": 1.0}, {"at": "@piedra", "cara": "sorpresa", "take": True},
            {"at": "@condenado", "cara": "serio", "mira": "der"}, {"at": "@error", "cara": "pensativo", "pose": "piensa"},
            {"at": "@Lo", "mira": "camara", "pose": "senala", "cara": "esceptica"}]),
        rot("CONDENADO A 24 AÑOS", 540, 440, "@condenado", 78, "rojo", golpe=True, out="@País-0.1"),
        obj("bocadillo", 540, 470, "@corrupción-0.2", 0.95, hud=True, entra="pop", sfx="pop",
            props={"lineas": ["MI MAYOR ERROR:", "NO VER LA CORRUPCIÓN", "DE ÁBALOS"], "cola": (0, 1)}),
        sello("DECLARACIÓN", "azul", 720, "@Lo", x=540),
    ]),
    # 7 · LA META: 29N, Feijóo y Abascal calentando
    dict(id="meta", fondo="parque", animo="tension", trans="iris", footnote="Elecciones generales: 29 de noviembre de 2026", lines=[
        V("Y al fondo, la meta: el 29 de noviembre.", "normal"),
        V("Allí ya esperan Feijóo y Abascal… calentando.", "comico", 0.1),
        V("Quedan 35 días de carrera.", "remate", 0.1),
    ], camara=[plano(0, "general", [540, 900], 0, zoom=0.9), plano("@Allí", "general", [540, 1050], 0.6, zoom=1.08),
               plano("@Quedan", "general", [540, 950], 0.5)],
       elements=[
        obj("arco", 540, SUELO - 20, 0, 0.92, entra="nada", dibuja=1.0, sfx="rotulador",
            props={"texto": "META", "sub": "29 DE NOVIEMBRE", "color": "verde", "cuadros": True}),
        corredor("feijoo", 380, "@Allí-0.2", "serio", trota=False, entra="pop", acciones=[
            {"at": "@Feijóo", "pose": "arriba", "salta": True}, {"at": "@Abascal", "pose": "jarras", "mira": "izq"},
            {"at": "@calentando", "salta": True, "pose": "punos"}, {"at": "@Quedan", "mira": "camara", "cara": "burla"}]),
        corredor("abascal", 700, "@Abascal-0.2", "serio", trota=False, entra="pop", acciones=[
            {"at": "@Abascal", "pose": "punos", "salta": True}, {"at": "@calentando", "pose": "arriba", "salta": True},
            {"at": "@Quedan", "mira": "camara", "pose": "jarras", "cara": "burla"}]),
        rot("29N", 540, 440, "@noviembre", 150, "amarillo", golpe=True, out="@Allí"),
        obj("contador", 540, 440, "@Quedan-0.1", 0.8, hud=True, entra="pop", sfx="pop", dibujo=1.0,
            props={"valor": 35, "desde": 0, "sufijo": " DÍAS", "ancho": 640}),
    ]),
    # 8 · FINAL: ¿cuatro más o relevo?
    dict(id="final", fondo={"tipo": "parque", "velocidad": 340}, animo="final", trans="zoom", footnote="Pregunta a la audiencia", lines=[
        V("Él pide cuatro años más. ¿Se los das… o toca relevo? Te leo.", "energia"),
        V("Y síguenos: hasta el 29N, te lo contamos con datos.", "normal", 0.15),
    ], camara=[plano(0, "general", [540, 1050], 0), plano("@relevo", "general", [540, 1000], 0.5, zoom=1.06),
               plano("@síguenos", "medio", "piz", 0.5, aire=260)],
       elements=[
        corredor("sanchez_corre", 520, 0, "riendo", acciones=[{"at": "@cuatro", "pose": "saluda"}, {"at": "@relevo", "mira": "izq", "cara": "burla"}]),
        corredor("cuerpo", 800, 0, "ilusionado", acciones=[{"at": "@relevo", "mira": "izq", "cara": "pensativo"}]),
        corredor("piz", 220, 0, "pensativo", acciones=[
            {"at": 0.1, "objeto": "reloj"}, {"at": "@relevo", "cara": "idea", "mira": "camara"},
            {"at": "@síguenos", "objeto": None, "pose": "saluda", "cara": "riendo"}, {"at": "@datos", "salta": True}]),
        rot("¿CUATRO MÁS…", 540, 430, "@cuatro", 108, "amarillo", golpe=True),
        rot("…O RELEVO?", 540, 570, "@relevo", 108, "blanco", golpe=True, fx=[{"at": "@leo", "do": "latir"}]),
    ]),
]

if __name__ == "__main__":
    episodio("cuatro_mas", "¿Cuatro más?", scenes,
             {"t": 3.6, "titulo": "¿Cuatro más?", "capitulo": None},
             ["Vídeo electoral de Sánchez con Carlos Cuerpo (elDiario.es, 25/10/2026): «¿Cuatro más?», «Estamos preparados», «Llevamos ocho ya»",
              "Entrevista de Sánchez en El País (Europa Press, 25/10/2026): SMI antes del 29N y su mayor error, «no ver la corrupción de Ábalos»",
              "Consejo de Ministros (feb. 2026): SMI 2026 1.221 €/mes, +66 % desde 2018 (735,90 €)",
              "INE, EPA 2T 2018 y 2T 2026: paro 15,28 % → 9,87 %; ocupados 19,34 M → 22,78 M",
              "Idealista vía ESdiario (6/10/2026): vivienda usada +74,4 % y alquiler +45,2 % desde junio de 2018",
              "Tribunal Supremo (22/06/2026): Ábalos, 24 años y 3 meses",
              "Personajes dibujados como pizarras, sin caricatura; las frases de Sánchez y Cuerpo son literales y con otra voz"],
             ("🏃 Sánchez sale a correr con Cuerpo: «¿Qué hacemos? ¿Cuatro más?»\n"
              "💶 Km 1, salario mínimo: de 736 € a 1.221 € (+66 %)\n"
              "📉 Km 2, paro: del 15,3 % al 9,9 % y 3,4 millones más trabajando\n"
              "🏠 La cuesta: piso +74 % y alquiler +45 % desde 2018\n"
              "🪨 La piedra: Ábalos, condenado a 24 años; Sánchez: su mayor error, «no ver la corrupción de Ábalos»\n"
              "🏁 En la meta del 29N esperan Feijóo y Abascal\n"
              "💬 ¿Cuatro más o relevo? Te leo 👇\n"
              "🔔 Síguenos · 📚 Fuentes en comentarios"),
             "📚 Fuentes: elDiario.es 25/10/2026 · El País/Europa Press 25/10/2026 · Consejo de Ministros (SMI 2026) · INE EPA · "
             "Idealista (vía ESdiario 6/10/2026) · Tribunal Supremo. ¿Ves un error? Dínoslo.",
             ["#Sánchez", "#CarlosCuerpo", "#29N", "#elecciones", "#salariominimo", "#vivienda", "#Feijóo", "#Abascal", "#pizarrapublica"],
             series_tag="EXPLICADO FÁCIL")
