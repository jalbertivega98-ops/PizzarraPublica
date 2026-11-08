#!/usr/bin/env python3
"""📜 Historia en la pizarra, cap. 2: «El 23-F» (martes 10/11/2026, 15:00).
Pedido por joel el 8/11/2026 («adelante» al plan de la semana: /mnt/project-files/insta/guiones/plan_semana_9-15nov.md).
Datos (Congreso de los Diputados, «23 de febrero de 1981»; Casa Real, mensaje del Rey; RTVE Archivo):
  23/2/1981, hacia las 18:23: el teniente coronel Antonio Tejero entra en el Congreso con guardias civiles durante la
    segunda votación de investidura de Leopoldo Calvo-Sotelo. Disparos al techo; «¡Quieto todo el mundo!».
  Gutiérrez Mellado se enfrenta a los asaltantes; Suárez y Carrillo no se tiran al suelo.
  En Valencia, Milans del Bosch saca los tanques a la calle.
  Hacia la 1:14 del 24/2 el Rey sale en televisión, con uniforme de capitán general, en defensa de la Constitución.
  El 24/2 por la mañana el golpe se rinde: unas 18 horas de secuestro. Calvo-Sotelo es investido el 25/2/1981.
  Tejero fue condenado a 30 años de prisión.
"""
from _mundo import *  # noqa: F401,F403

R = "espana"
MAD = P(R, -3.7, 40.4)
VAL = P(R, -0.38, 39.47)
F = "Congreso de los Diputados · Casa Real · RTVE Archivo"
NOCHE = (30, 28, 56)

scenes = [
    # 1 · GANCHO
    dict(id="gancho", fondo={"tipo": "plano", "color": NOCHE}, animo="tension", footnote=F, lines=[
        V("23 de febrero de 1981. Seis y veinte de la tarde.", "intriga"),
        V("En el Congreso se vota un presidente. Y de repente, disparos.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@Congreso", "general", [540, 1000], 0.5, zoom=1.06),
               plano("@disparos", "general", [540, 900], 0.3, zoom=1.15)],
       elements=[
        rot("HISTORIA EN LA PIZARRA", 540, 430, 0, 70, "blanco"),
        rot("23-F · 1981", 540, 560, 0.2, 130, "amarillo", golpe=True),
        obj("reloj", 860, 760, "@Seis", 0.45, hud=True, entra="pop", sfx="pop"),
        edif("congreso", 540, "@Congreso-0.3", 0.55, entra="crece", sfx="pop", dibuja=0.8, id="cong",
             acciones=[{"at": "@disparos", "cara": "susto"}]),
        quien("piz", 860, "@presidente", 0.42, "normal", y=1560, entra="der", acciones=[
            {"at": "@repente", "mira": "cong", "cara": "pensativo"}, {"at": "@disparos", "cara": "susto", "take": True, "pose": "cabeza"}]),
        pum("¡BANG!", 540, 760, "@disparos", 1.0),
    ]),
    # 2 · DENTRO DEL CONGRESO
    dict(id="dentro", fondo="oficina", animo="tension", trans="barrido", footnote=F, lines=[
        V("Entra el teniente coronel Tejero con guardias civiles. «¡Quieto todo el mundo!»."),
        V("Casi todos los diputados se tiran al suelo. Suárez se queda sentado.", "normal", 0.1),
        V("Y el vicepresidente, Gutiérrez Mellado, les planta cara.", "remate", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@Suárez", "medio", "suarez", 0.5, aire=250),
               plano("@Gutiérrez", "general", [540, 1000], 0.5)],
       elements=[
        obj("bocadillo", 540, 520, "@Quieto", 0.8, hud=True, entra="pop", sfx="golpe",
            props={"lineas": ["¡QUIETO TODO", "EL MUNDO!"], "cola": (0, 1)}, out="@diputados"),
        quien("diputado", 200, 0, 0.5, "normal", entra="nada", id="dip1", acciones=[{"at": "@suelo", "cara": "susto", "pose": "cabeza", "y": 1500, "dur": 0.4}]),
        quien("diputado", 880, 0, 0.5, "normal", entra="nada", id="dip2", acciones=[{"at": "@suelo", "cara": "susto", "pose": "cabeza", "y": 1500, "dur": 0.4}]),
        quien("suarez", 540, "@diputados", 0.62, "serio", entra="abajo", acciones=[{"at": "@sentado", "pose": "cruzados", "mira": "camara"}]),
        etq("SE QUEDA SENTADO", 540, 560, "@sentado", "amarillo", 0.65, hud=True, out="@Gutiérrez"),
        etq("GUTIÉRREZ MELLADO", 540, 560, "@Gutiérrez", "blanco", 0.65, hud=True),
        sello("CONFIRMADO", "verde", 1240, "@cara"),
    ]),
    # 3 · VALENCIA: LOS TANQUES
    dict(id="valencia", fondo="mar_mapa", limites=LIM, animo="aventura", trans="zoom", footnote=F, lines=[
        V("Mientras, en Valencia, el general Milans del Bosch saca los tanques a la calle."),
        V("Durante horas, nadie sabe quién manda en España.", "intriga", 0.15),
    ], camara=[zoom(0, P(R, -2.5, 40), 1.0, 0), zoom("@Valencia", VAL, 3.2, 0.9), zoom("@nadie", P(R, -2.5, 40), 1.1, 0.9)],
       elements=[
        mapa(R, 0, 1.4, lineas=[linea("ruta", [(-3.7, 40.4), (-0.38, 39.47)], "rojo", 0.9, discontinua=True, ancho=6)]),
        obj("chincheta", MAD[0], MAD[1], 0.6, 0.5, entra="cae", sfx="pop", props={"diseno": "espana"}),
        obj("chincheta", VAL[0], VAL[1], "@Valencia", 0.5, entra="cae", sfx="pop", props={"diseno": "espana"}),
        pum("TANQUES", VAL[0], VAL[1] - 60, "@tanques", 0.5),
        rot("¿QUIÉN MANDA?", 540, 430, "@nadie", 100, "amarillo", golpe=True),
        quien("piz", 860, "@horas", 0.4, "preocupado", y=1600, entra="der", hud=True, acciones=[{"at": "@manda", "pose": "encoge", "cara": "confundido"}]),
    ]),
    # 4 · EL REY EN LA TELE
    dict(id="rey", fondo="salon", animo="curioso", trans="papel", footnote="Casa Real: mensaje del 24/2/1981", lines=[
        V("A la una y cuarto de la madrugada, el Rey sale en televisión."),
        V("Con uniforme militar, defiende la Constitución. Y el golpe se queda solo.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@Constitución", "general", [540, 900], 0.5, zoom=1.08)],
       elements=[
        obj("tele", 540, 820, 0, 0.8, entra="nada", dibuja=0.7, sfx="rotulador", props={"texto": "MENSAJE DEL REY"}),
        obj("corona", 540, 560, "@Rey", 0.45, hud=True, entra="cae", sfx="golpe"),
        obj("reloj", 860, 460, "@una", 0.4, hud=True, entra="pop", sfx="pop", out="@uniforme"),
        obj("libro", 260, 560, "@Constitución", 0.5, hud=True, entra="pop", sfx="papel", props={"titulo": "CONSTITUCIÓN", "color": "rojo"}),
        quien("piz", 860, 0.3, 0.45, "pensativo", y=1520, entra="der", acciones=[
            {"at": "@televisión", "mira": "izq", "cara": "sorpresa"}, {"at": "@Constitución", "cara": "ilusionado", "pose": "pulgar"},
            {"at": "@solo", "salta": True}]),
    ]),
    # 5 · EL FINAL DEL GOLPE
    dict(id="fin", fondo={"tipo": "plano", "color": (60, 40, 20)}, animo="final", trans="barrido", footnote=F, lines=[
        V("Por la mañana se rinden. Unas dieciocho horas de secuestro."),
        V("Dos días después, Calvo-Sotelo es investido presidente. Y Tejero, condenado a treinta años.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@Calvo-Sotelo", "general", [540, 1000], 0.5, zoom=1.04)],
       elements=[
        obj("contador", 540, 600, "@dieciocho", 0.9, hud=True, entra="pop", sfx="kaching", props={"valor": 18, "sufijo": " HORAS", "ancho": 640}),
        quien("calvo_sotelo", 540, "@Calvo-Sotelo-0.2", 0.5, "normal", entra="abajo", acciones=[{"at": "@investido", "pose": "saluda"}]),
        etq("INVESTIDO 25/2/1981", 540, 820, "@investido", "verde", 0.6, hud=True, out="@Tejero"),
        etq("TEJERO: 30 AÑOS", 540, 820, "@condenado", "rojo", 0.65, hud=True),
    ]),
    # 6 · CIERRE
    dict(id="final", fondo="calle", animo="final", trans="iris", footnote="Te leemos en comentarios", lines=[
        V("¿Tus padres o abuelos lo vivieron? Cuéntame dónde estaban esa noche."),
        V("Y sigue a Piz: próximo capítulo, la única moción de censura que ha ganado.", "energia", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@sigue", "medio", "piz", 0.5, aire=300)],
       elements=[
        quien("piz", 540, 0, 0.6, "pensativo", y=1500, entra="abajo", acciones=[
            {"at": "@abuelos", "pose": "piensa", "mira": "camara"}, {"at": "@Cuéntame", "cara": "ilusionado", "pose": "senala"},
            {"at": "@sigue", "pose": "saluda", "cara": "riendo"}]),
        rot("23-F", 540, 420, 0, 130, "amarillo", golpe=True, out="@sigue-0.2"),
        rot("SIGUE A PIZ", 540, 420, "@sigue", 110, "amarillo", fx=[{"at": "@moción", "do": "latir"}]),
        etq("PRÓXIMO: LA MOCIÓN", 540, 620, "@capítulo", "blanco", 0.6, hud=True),
    ]),
]

if __name__ == "__main__":
    episodio("veintitres_f", "El 23-F", scenes,
             {"t": 3.0, "titulo": "El 23-F: la tarde que entraron en el Congreso", "capitulo": "📜 Historia en la pizarra · Cap. 2"},
             ["Congreso de los Diputados: «23 de febrero de 1981» (asalto durante la votación de investidura de Calvo-Sotelo)",
              "Casa Real: mensaje de S. M. el Rey, madrugada del 24/2/1981",
              "RTVE Archivo: 23-F, 18 horas de secuestro; condena de Tejero (30 años)"],
             ("📜 Historia en la pizarra · Cap. 2\n"
              "⚡ 23-F de 1981, 18:20: disparos en el Congreso\n"
              "🪖 Tejero: «¡Quieto todo el mundo!» · Suárez no se tira al suelo\n"
              "🗺️ En Valencia, los tanques salen a la calle\n"
              "📺 A la 1:14, el Rey en la tele defiende la Constitución\n"
              "💬 ¿Dónde estaban tus padres o abuelos esa noche? 👇\n"
              "🔔 Sigue a Piz · Próximo: la única moción que ganó · 📚 Fuentes en comentarios"),
             "📚 Fuentes: Congreso de los Diputados (23-F) · Casa Real (mensaje del 24/2/1981) · RTVE Archivo. ¿Ves un error? Dínoslo.",
             ["#23F", "#HistoriaDeEspaña", "#Transición", "#Congreso", "#AprendeEnTikTok", "#pizarrapublica"],
             series_tag="HISTORIA EN LA PIZARRA")
