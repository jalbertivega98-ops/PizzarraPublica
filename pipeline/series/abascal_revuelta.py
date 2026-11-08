#!/usr/bin/env python3
"""«Esta noche, Abascal en La Revuelta» (lunes 9/11/2026, 15:00).
Pedido por joel el 8/11/2026; estaba en el plan de la semana (9/11 15:00).
Fuentes:
  eldiario.es/Vertele 5/11/2026 (Laura Pérez): Abascal acepta y irá el lunes 9/11 a La Revuelta (La 1); Broncano lo
    anunció en directo: «nunca pensé que diría esto, Santiago Abascal»; abucheos del público. Será el primero de la
    ultraderecha con Broncano en RTVE. Sánchez (22/10): 4,4 M y 33,9 %; Montero y Rufián (27/10): 2,7 M y 21,7 %.
    Feijóo: «no hay respuesta por ahora». Recuerda las amenazas de su partido de entrar en RTVE «con motosierras y lanzallamas».
  Demócrata 5/11/2026 (fuentes de Vox a Europa Press): confirma la entrevista del lunes.
  Infobae 6/11/2026: Feijóo irá a El Hormiguero (11/11).
"""
from _mundo import *  # noqa: F401,F403

REV = {"tipo": "plato", "rotulo": "LA REVUELTA"}
F = "eldiario.es/Vertele 5/11/2026 · Demócrata 5/11/2026"

scenes = [
    # 1 · GANCHO
    dict(id="gancho", fondo=REV, animo="tension", footnote=F, lines=[
        V("Esta noche pasa algo que hace un año parecía imposible.", "intriga"),
        V("Abascal se sienta con Broncano. En La Revuelta. En la tele pública.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 950], 0, zoom=1.15), plano("@Abascal", "general", [440, 980], 0.5, zoom=1.25),
               plano("@pública", "general", [540, 950], 0.5, zoom=1.15)],
       elements=[
        quien("broncano", 790, 0, 0.72, "normal", entra="nada", acciones=[
            {"at": "@imposible", "cara": "sorpresa"}, {"at": "@Broncano", "pose": "saluda", "mira": "izq"},
            {"at": "@pública", "mira": "camara", "cara": "riendo"}]),
        quien("abascal", -220, "@Abascal-0.3", 0.75, "serio", entra="nada", acciones=[
            {"at": "@Abascal-0.3", "x": 330, "dur": 1.0}, {"at": "@sienta", "pose": "saluda", "cara": "normal"},
            {"at": "@pública", "mira": "camara", "pose": "cruzados"}]),
        rot("ESTA NOCHE", 540, 470, 0.2, 120, "amarillo", golpe=True, out="@Revuelta"),
        rot("LA 1 · RTVE", 540, 470, "@Revuelta", 110, "blanco", golpe=True),
        sello("CONFIRMADO", "verde", 650, "@pública"),
    ]),
    # 2 · EL ANUNCIO: abucheos
    dict(id="anuncio", fondo=REV, animo="comico", trans="corte", footnote=F, lines=[
        V("Broncano lo anunció así: «Nunca pensé que diría esto: Santiago Abascal».", "normal"),
        V("Y el público… abucheó.", "remate", 0.2),
    ], camara=[plano(0, "medio", "broncano", 0, aire=260), plano("@público", "general", [540, 950], 0.4, zoom=1.1)],
       elements=[
        quien("broncano", 600, 0, 0.75, "normal", entra="nada", acciones=[
            {"at": "@Nunca", "pose": "manos_juntas", "cara": "confundido"}, {"at": "@Santiago", "pose": "senala", "cara": "riendo"},
            {"at": "@abucheó", "cara": "susto", "pose": "encoge"}]),
        obj("bocadillo", 360, 560, "@Nunca", 0.9, hud=True, entra="pop", sfx="pop", out="@público",
            props={"lineas": ["NUNCA PENSÉ", "QUE DIRÍA ESTO…"], "cola": (1, 1)}),
        pum("¡UUUH!", 300, 760, "@abucheó", 0.9),
        pum("¡BUUU!", 780, 640, "@abucheó+0.25", 0.8),
    ]),
    # 3 · LA PARADOJA: motosierras
    dict(id="paradoja", fondo={"tipo": "rayos", "color": "rojo"}, animo="tension", trans="zoom", footnote=F, lines=[
        V("Lo curioso: su partido amenazó con entrar en RTVE con «motosierras y lanzallamas».", "normal"),
        V("Y ahora va a su programa estrella.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@estrella", "general", [540, 920], 0.5, zoom=1.06)],
       elements=[
        obj("tele", 540, 760, 0, 0.9, hud=True, entra="pop", sfx="pop", props={"texto": "RTVE"}),
        quien("abascal", 540, "@estrella-0.6", 0.55, "normal", y=1580, entra="abajo", acciones=[
            {"at": "@estrella", "pose": "pulgar", "cara": "ilusionado", "mira": "camara"}]),
        rot("«MOTOSIERRAS Y LANZALLAMAS»", 540, 440, "@motosierras", 70, "amarillo", golpe=True),
        sello("SEGÚN ELDIARIO.ES", "naranja", 1180, "@lanzallamas"),
    ]),
    # 4 · EL LISTÓN: audiencias
    dict(id="liston", fondo={"tipo": "plano", "color": (40, 30, 70)}, animo="curioso", trans="barrido", footnote=F, lines=[
        V("Y el listón está alto. Sánchez hizo 4,4 millones de espectadores: récord del programa.", "normal"),
        V("Montero y Rufián, 2,7 millones.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@Montero", "general", [540, 920], 0.4, zoom=1.05)],
       elements=[
        rot("AUDIENCIA", 540, 420, 0, 110, "amarillo"),
        obj("barras", 540, 880, "@Sánchez", 1.05, hud=True, entra="nada", dibujo=1.6,
            props={"sufijo": " M", "decimales": 1, "tope": 5, "barras": [
                {"texto": "SÁNCHEZ", "valor": 4.4, "color": "psoe"}, {"texto": "MONTERO Y RUFIÁN", "valor": 2.7, "color": "gris"},
                {"texto": "ABASCAL", "valor": 0.0, "color": "vox"}]}),
        sello("RÉCORD", "rojo", 1250, "@récord"),
        etq("¿?", 860, 1080, "@Montero+0.6", "vox", 0.8, hud=True),
    ]),
    # 5 · ¿Y FEIJÓO?
    dict(id="feijoo", fondo=REV, animo="comico", trans="corte", footnote="eldiario.es 5/11 · Infobae 6/11/2026", lines=[
        V("¿Y Feijóo? A Broncano, de momento, no le ha contestado.", "normal"),
        V("Él ha elegido El Hormiguero, el miércoles.", "remate", 0.1),
    ], camara=[plano(0, "general", [540, 950], 0, zoom=1.1), plano("@Hormiguero", "general", [540, 950], 0.4, zoom=1.15)],
       elements=[
        quien("broncano", 790, 0, 0.72, "normal", entra="nada", acciones=[
            {"at": "@contestado", "pose": "encoge", "cara": "confundido", "mira": "izq"}]),
        obj("silla", 330, 1340, 0, 0.8, entra="nada", props={"color": "gris", "texto": "FEIJÓO"}),
        quien("feijoo", -250, "@Hormiguero-0.5", 0.55, "riendo", y=1580, entra="nada", acciones=[
            {"at": "@Hormiguero-0.5", "x": 300, "dur": 0.6}, {"at": "@miércoles", "pose": "saluda", "mira": "camara"}]),
        sello("SILLA VACÍA", "naranja", 640, "@momento"),
    ]),
    # 6 · FINAL
    dict(id="final", fondo=REV, animo="final", trans="iris", footnote="Te leemos en comentarios", lines=[
        V("¿Superará a Sánchez? Apuesta: más o menos de 4,4 millones."),
        V("Y sigue a Piz: mañana te contamos cómo fue.", "energia", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@sigue", "medio", "piz", 0.5, aire=300)],
       elements=[
        quien("piz", 540, 0, 0.6, "pensativo", y=1500, entra="abajo", acciones=[
            {"at": "@Superará", "pose": "piensa", "mira": "camara"}, {"at": "@Apuesta", "cara": "ilusionado", "pose": "senala"},
            {"at": "@sigue", "pose": "saluda", "cara": "riendo"}]),
        etq("MÁS", 300, 700, "@más", "verde", 0.7, hud=True, out="@sigue"),
        etq("MENOS", 780, 700, "@menos", "rojo", 0.7, hud=True, out="@sigue"),
        rot("4,4 MILLONES", 540, 420, 0, 110, "amarillo", golpe=True, out="@sigue-0.2"),
        rot("SIGUE A PIZ", 540, 420, "@sigue", 110, "amarillo", fx=[{"at": "@fue", "do": "latir"}]),
    ]),
]

if __name__ == "__main__":
    episodio("abascal_revuelta", "Esta noche, Abascal en La Revuelta", scenes,
             {"t": 4.0, "titulo": "Esta noche, Abascal en La Revuelta", "capitulo": None},
             ["eldiario.es/Vertele 5/11/2026: Abascal acepta ir a La Revuelta el lunes 9/11; audiencias de Sánchez y de Montero y Rufián; Feijóo sin respuesta",
              "Demócrata 5/11/2026 (fuentes de Vox a Europa Press): confirma la entrevista",
              "Infobae 6/11/2026: Feijóo, en El Hormiguero"],
             ("📺 Esta noche, Abascal con Broncano en La Revuelta (La 1)\n"
              "🙉 Broncano lo anunció… y el público abucheó\n"
              "🪚 Su partido habló de entrar en RTVE con «motosierras y lanzallamas»\n"
              "📊 El listón: Sánchez 4,4 millones · Montero y Rufián 2,7\n"
              "🪑 ¿Y Feijóo? Sin respuesta a Broncano; va a El Hormiguero\n"
              "💬 ¿Más o menos de 4,4 millones? Apuesta 👇\n"
              "🔔 Sigue a Piz · 📚 Fuentes en comentarios"),
             "📚 Fuentes: eldiario.es/Vertele 5/11/2026 · Demócrata/Europa Press 5/11 · Infobae 6/11. ¿Ves un error? Dínoslo.",
             ["#Abascal", "#LaRevuelta", "#Broncano", "#Vox", "#29N", "#pizarrapublica"],
             series_tag="EXPLICADO FÁCIL")
