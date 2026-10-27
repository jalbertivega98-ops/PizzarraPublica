#!/usr/bin/env python3
"""«128 detenidos. Convocado por TikTok» (27/10/2026). Mundo dibujado: Barcelona de noche, contenedores que arden,
el móvil de la convocatoria, la gráfica de menores y el salto a Bilbao.

Guion y fuentes: /mnt/project-files/insta/guiones/disturbios_bcn.md (aprobado por joel el 27/10/2026)
  Sábado 24/10, desde las 18:00, plaza de Catalunya: protesta no autorizada convocada por redes y TikTok con el lema
    «institutos indignados»; los Mossos la seguían desde hacía días; sin organizador identificado; unas 500 personas
    (Infobae 25/10/2026).
  Mossos: 128 detenidos, 72 menores; 23 comercios vandalizados; 14 agentes heridos, 4 graves; 33 salidas de bomberos
    (Moncloa.com 25/10/2026; Infobae da 15 heridos: decimos «más de una docena»).
  Collboni: «consecuencias para los progenitores»; Illa: «La violencia no tiene cabida en Cataluña» (Infobae 25/10).
  Feijóo (Salamanca 25/10): «Se están resistiendo a abandonar el poder con violencia»; Ferraz condena la violencia,
    apoya a la policía y rechaza el uso partidista de la seguridad (Moncloa.com 25/10/2026).
  Bilbao 26/10: tras la protesta contra la charla de Vito Quiles en Deusto (cancelada por él), coches quemados,
    19 detenidos, 7 menores (EFE vía Infobae 26/10/2026).
"""
from _mundo import *  # noqa: F401,F403

R = "espana"
BCN = P(R, 2.17, 41.39)
BIL = P(R, -2.93, 43.26)
MAD = P(R, -3.7, 40.4)
NOCHE = {"tipo": "calle", "hora": "noche"}


def F(x, at, vida, scale=0.8, y=1150):
    """Fuego sobre un contenedor (la papelera va antes, debajo)."""
    return dict(type="efecto", efecto="fuego", x=x, y=y, at=at, vida=vida, scale=scale)


def A(text, pausa=None, efecto="tele"):
    """Frase literal de un político: voz del canal procesada, no imita la suya."""
    return dict(V(text, "normal", pausa), efecto_voz=efecto)


scenes = [
    # 1 · GANCHO: calle de noche, contenedores ardiendo; Piz llega y se lleva el susto
    dict(id="gancho", fondo=NOCHE, animo="tension", footnote="Mossos d'Esquadra vía Moncloa.com 25/10/2026",
         luz=[{"at": "@detenidos", "tipo": "alarma"}], lines=[
        V("128 detenidos en una sola noche.", "energia"),
        V("Y la convocatoria llegó… por TikTok.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@noche", "general", [540, 980], 0.5, zoom=1.06),
               plano("@convocatoria", "medio", "piz", 0.5, aire=280), plano("@TikTok", "general", [540, 1000], 0.4, zoom=1.08)],
       elements=[
        obj("papelera", 200, 1340, 0, 0.75, entra="nada"),
        obj("papelera", 880, 1340, 0, 0.75, entra="nada"),
        F(200, 0.05, 4.2), F(880, 0.4, 3.9),
        quien("piz", -200, 0.2, 0.6, "sorpresa", entra="nada", acciones=[
            {"at": 0.2, "x": 520, "dur": 0.9}, {"at": "@detenidos", "cara": "susto", "take": True, "mira": "camara"},
            {"at": "@convocatoria", "cara": "confundido", "pose": "encoge"}, {"at": "@TikTok", "cara": "sorpresa", "pose": "sostiene"}]),
        obj("movil", 700, 900, "@TikTok-0.2", 0.55, entra="pop", sfx="pop",
            props={"pantalla": "sms", "remite": "REDES", "lineas": ["#institutos", "indignados", "sáb · 18:00"], "suena": True}),
        rot("128 DETENIDOS", 540, 400, "@128", 120, "amarillo", golpe=True),
    ]),
    # 2 · EL MAPA: España se dibuja, zoom a Barcelona; sábado, plaza de Catalunya
    dict(id="mapa", fondo="mar_mapa", limites=LIM, animo="aventura", trans="zoom", footnote="Infobae 25/10/2026", lines=[
        V("Barcelona, sábado 24 de octubre. Plaza de Catalunya, seis de la tarde.", "normal"),
    ], camara=[zoom(0, MAD, 1.0, 0), zoom("@Barcelona", BCN, 2.8, 1.0), zoom("@Catalunya", BCN, 3.4, 0.7)],
       elements=[
        mapa(R, 0, 1.3, orden=["Barcelona"], acciones=[{"at": "@Barcelona", "props": {"resalta": ["Barcelona"]}, "sfx": "pop"}]),
        obj("chincheta", BCN[0] + 6, BCN[1], "@Barcelona+0.3", 0.12, props={"diseno": "espana"}, entra="cae"),
        etq("SÁB. 24 OCT · 18:00", 540, 430, "@sábado", "azul", 0.8, hud=True),
    ]),
    # 3 · LA CONVOCATORIA: el móvil, el lema y nadie al otro lado
    dict(id="convocatoria", fondo={"tipo": "plano", "color": (28, 52, 110)}, animo="curioso", trans="iris",
         footnote="Infobae 25/10/2026 (fuentes de los Mossos)", lines=[
        V("La protesta no estaba autorizada. Se convocó en redes con un lema: «institutos indignados».", "normal"),
        V("Los Mossos la vigilaban desde hacía días. Pero nadie sabe quién la organizó.", "normal", 0.15),
    ], camara=[plano(0, "general", [540, 950], 0), plano("@lema", "general", [540, 820], 0.6, zoom=1.12),
               plano("@Mossos", "general", [540, 1000], 0.5), plano("@nadie", "general", [540, 980], 0.4, zoom=1.06)],
       elements=[
        obj("movil", 540, 760, 0, 0.95, hud=True, entra="pop", sfx="pop",
            props={"pantalla": "sms", "remite": "REDES", "lineas": ["#institutos", "indignados", "sáb · 18:00", "pl. Catalunya"]},
            acciones=[{"at": "@lema", "props": {"suena": True}}, {"at": "@Mossos", "props": {"suena": False}}]),
        sello("NO AUTORIZADA", "rojo", 1180, "@autorizada", out="@Mossos"),
        quien("piz", 1300, "@Mossos", 0.45, "pensativo", y=1640, entra="nada", hud=True, acciones=[
            {"at": "@Mossos", "x": 800, "dur": 0.6}, {"at": "@vigilaban", "pose": "prismaticos"},
            {"at": "@nadie", "cara": "confundido", "pose": "encoge", "mira": "camara"}]),
        obj("lupa", 300, 1440, "@organizó", 0.6, hud=True, entra="pop", sfx="pop"),
        sello("ORGANIZADOR: SIN IDENTIFICAR", "naranja", 1180, "@organizó"),
    ]),
    # 4 · LA NOCHE: fuegos que se encienden uno tras otro y los contadores del destrozo
    dict(id="noche", fondo=NOCHE, animo="tension", trans="corte", footnote="Mossos d'Esquadra vía Moncloa.com e Infobae 25/10/2026",
         luz=[{"at": "@mossos", "tipo": "alarma"}], lines=[
        V("Unas 500 personas. Contenedores ardiendo, 23 comercios destrozados y 33 salidas de los bomberos.", "normal"),
        V("Y más de una docena de mossos heridos. Cuatro, graves.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@Contenedores", "general", [540, 1060], 0.6, zoom=1.08),
               plano("@mossos", "general", [540, 1000], 0.5), plano("@graves", "general", [540, 980], 0.4, zoom=1.06)],
       elements=[
        obj("papelera", 160, 1340, 0, 0.7, entra="nada"),
        obj("papelera", 920, 1340, 0, 0.7, entra="nada"),
        obj("papelera", 540, 1340, 0, 0.6, entra="nada"),
        F(160, "@Contenedores", 7.5), F(920, "@Contenedores+0.35", 7.2), F(540, "@Contenedores+0.7", 6.8, 0.7, 1180),
        obj("contador", 540, 520, "@500", 0.75, hud=True, entra="pop", sfx="kaching", out="@23",
            props={"valor": 500, "sufijo": " PERSONAS", "ancho": 820}),
        obj("contador", 540, 520, "@23", 0.75, hud=True, entra="pop", sfx="golpe", out="@33",
            props={"valor": 23, "sufijo": " COMERCIOS", "ancho": 820}),
        obj("contador", 540, 520, "@33", 0.75, hud=True, entra="pop", sfx="golpe", out="@mossos",
            props={"valor": 33, "sufijo": " BOMBEROS", "ancho": 820}),
        obj("contador", 540, 520, "@mossos", 0.75, hud=True, entra="pop", sfx="golpe",
            props={"valor": 14, "sufijo": " HERIDOS", "ancho": 820}),
        etq("4 GRAVES", 540, 700, "@Cuatro", "rojo", 0.85, hud=True),
        quien("piz", 540, "@docena", 0.5, "susto", y=1420, entra="abajo", acciones=[
            {"at": "@heridos", "pose": "cabeza"}, {"at": "@graves", "cara": "triste", "pose": "caidos"}]),
    ]),
    # 5 · EL DATO: más de la mitad, menores; la gráfica crece y Piz no se lo cree
    dict(id="menores", fondo={"tipo": "plano", "color": "amarillo"}, animo="tension", trans="barrido",
         footnote="Mossos d'Esquadra vía Moncloa.com 25/10/2026", lines=[
        V("Ahora, el dato que más pesa: de los 128 detenidos, 72 son menores de edad.", "normal"),
        V("Más de la mitad.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 950], 0), plano("@72", "general", [540, 900], 0.5, zoom=1.08),
               plano("@mitad", "general", [540, 960], 0.4)],
       elements=[
        obj("barras", 540, 960, "@128", 1.15, hud=True, entra="nada", dibujo=1.4,
            props={"sufijo": "", "decimales": 0, "tope": 90, "resalta": [0], "barras": [
                {"texto": "MENORES", "valor": 72, "color": "rojo"}, {"texto": "ADULTOS", "valor": 56, "color": "gris"}]}),
        quien("piz", 1300, "@menores", 0.45, "sorpresa", y=1660, entra="nada", hud=True, acciones=[
            {"at": "@menores", "x": 930, "dur": 0.5}, {"at": "@edad", "cara": "susto", "take": True},
            {"at": "@mitad", "pose": "cabeza", "cara": "triste", "mira": "camara"}]),
        rot("72 DE 128", 540, 420, "@72", 110, "rojo", golpe=True),
        sello("CONFIRMADO · MOSSOS", "verde", 580, "@mitad"),
    ]),
    # 6 · LAS REACCIONES: PSC, PP y PSOE, cada uno con su frase
    dict(id="reacciones", fondo={"tipo": "plano", "color": (110, 34, 40)}, animo="tension", trans="papel",
         footnote="Infobae 25/10/2026 · Moncloa.com 25/10/2026", lines=[
        V("El alcalde, Collboni, avisa: habrá consecuencias para los padres. Illa: la violencia no tiene cabida en Cataluña.", "normal"),
        V("Feijóo culpa al Gobierno:", "normal", 0.15),
        A("«Se están resistiendo a abandonar el poder con violencia».", 0.1),
        V("Y el PSOE condena la violencia y rechaza usarla como arma electoral.", "normal", 0.15),
    ], camara=[plano(0, "general", [540, 950], 0), plano("@Feijóo", "medio", "feijoo", 0.5, aire=280),
               plano("@PSOE", "general", [540, 950], 0.5)],
       elements=[
        obj("bocadillo", 540, 560, 0.2, 0.72, hud=True, entra="pop", sfx="pop", out="@Illa",
            props={"lineas": ["COLLBONI (PSC):", "«consecuencias para", "los progenitores»"]}),
        obj("bocadillo", 540, 560, "@Illa", 0.72, hud=True, entra="pop", sfx="pop", out="@Feijóo",
            props={"lineas": ["ILLA (PSC):", "«La violencia no tiene", "cabida en Cataluña»"]}),
        quien("feijoo", -220, "@Feijóo", 0.55, "serio", entra="nada", acciones=[
            {"at": "@Feijóo", "x": 400, "dur": 0.6}, {"at": "@resistiendo", "pose": "senala", "cara": "enfado", "mira": "camara"},
            {"at": "@PSOE", "x": 260, "dur": 0.5, "mira": "der", "pose": "cruzados"}]),
        obj("bocadillo", 600, 520, "@resistiendo", 0.72, hud=True, entra="pop", sfx="pop", out="@PSOE",
            props={"lineas": ["FEIJÓO (PP):", "«Se están resistiendo", "a abandonar el poder", "con violencia»"]}),
        obj("bocadillo", 540, 520, "@PSOE", 0.72, hud=True, entra="pop", sfx="pop",
            props={"lineas": ["PSOE:", "condena la violencia", "y rechaza usarla", "en campaña"]}),
        quien("sanchez", 1300, "@PSOE", 0.55, "serio", entra="nada", acciones=[
            {"at": "@PSOE", "x": 800, "dur": 0.6, "mira": "izq"}, {"at": "@condena", "pose": "manos_juntas"},
            {"at": "@electoral", "pose": "senala_izq"}]),
        sello("DECLARACIONES", "azul", 1180, "@violencia+0.2", out="@Feijóo"),
    ]),
    # 7 · BILBAO: el mapa sube al norte; el lunes, otra noche igual
    dict(id="bilbao", fondo="mar_mapa", limites=LIM, animo="tension", trans="zoom", footnote="EFE vía Infobae 26/10/2026", lines=[
        V("Y no fue solo Barcelona. El lunes, en Bilbao, tras la protesta contra una charla de Vito Quiles, que él canceló:", "normal"),
        V("coches quemados y 19 detenidos. Siete, menores.", "remate", 0.1),
    ], camara=[zoom(0, BCN, 2.2, 0), zoom("@Bilbao", BIL, 2.8, 1.1), zoom("@coches", BIL, 3.4, 0.5)],
       elements=[
        mapa(R, 0, 0.01, acciones=[{"at": 0, "props": {"resalta": ["Barcelona"]}},
                                   {"at": "@Bilbao", "props": {"resalta": ["Barcelona", "Bizkaia"]}, "sfx": "pop"}]),
        obj("chincheta", BCN[0] + 6, BCN[1], 0, 0.12, props={"diseno": "espana"}, entra="nada"),
        obj("chincheta", BIL[0] + 6, BIL[1], "@Bilbao+0.4", 0.12, props={"diseno": "espana"}, entra="cae"),
        F(BIL[0] + 40, "@coches", 3.2, 0.11, BIL[1] - 10),
        obj("contador", 540, 560, "@19", 0.75, hud=True, entra="pop", sfx="golpe", props={"valor": 19, "sufijo": " DETENIDOS", "ancho": 820}),
        etq("7 MENORES", 540, 740, "@Siete", "rojo", 0.8, hud=True),
        etq("LUNES 26 · BILBAO", 540, 420, "@lunes", "azul", 0.75, hud=True),
    ]),
    # 8 · FINAL: Piz en la calle ya apagada, con la pregunta
    dict(id="final", fondo=NOCHE, animo="final", trans="iris", footnote="Pregunta a la audiencia", lines=[
        V("A un mes del 29N, la pregunta: ¿quién debe pagar esto? ¿Los chavales, sus padres… o quien lo convoca?", "normal"),
        V("Te leo en comentarios. Y síguenos: hasta el 29N te lo contamos con datos.", "energia", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@chavales", "general", [540, 1000], 0.5, zoom=1.05),
               plano("@leo", "medio", "piz", 0.5, aire=300)],
       elements=[
        obj("papelera", 200, 1340, 0, 0.7, entra="nada"),
        quien("piz", 560, 0, 0.62, "pensativo", entra="nada", acciones=[
            {"at": "@pagar", "pose": "piensa", "mira": "camara"}, {"at": "@chavales", "pose": "senala_izq", "mira": "izq"},
            {"at": "@padres", "pose": "senala", "mira": "der"}, {"at": "@convoca", "pose": "sostiene", "cara": "serio"},
            {"at": "@leo", "cara": "ilusionado", "pose": "senala"}, {"at": "@síguenos", "pose": "saluda", "cara": "riendo"}]),
        obj("movil", 820, 960, "@convoca", 0.45, entra="pop", sfx="pop", out="@leo",
            props={"pantalla": "sms", "remite": "REDES", "lineas": ["#institutos", "indignados"], "suena": True}),
        etq("¿CHAVALES?", 270, 700, "@chavales", "azul", 0.65, hud=True, out="@leo"),
        etq("¿PADRES?", 810, 700, "@padres", "verde", 0.65, hud=True, out="@leo"),
        rot("¿QUIÉN PAGA?", 540, 440, "@pagar", 110, "amarillo", golpe=True, out="@síguenos-0.3", fx=[{"at": "@leo", "do": "latir"}]),
        rot("SÍGUENOS", 540, 440, "@síguenos", 110, "amarillo"),
    ]),
]

if __name__ == "__main__":
    episodio("disturbios_bcn", "128 detenidos. Convocado por TikTok", scenes,
             {"t": 1.2, "titulo": "128 detenidos. Convocado por TikTok", "capitulo": None},
             ["Infobae (25/10/2026): convocatoria «institutos indignados» por redes y TikTok, unas 500 personas, sin organizador",
              "Moncloa.com (25/10/2026), con datos de los Mossos: 128 detenidos, 72 menores, 23 comercios, 14 agentes heridos (4 graves), 33 salidas de bomberos",
              "Infobae (25/10/2026): declaraciones de Collboni e Illa",
              "Moncloa.com (25/10/2026): Feijóo en Salamanca y respuesta de Ferraz",
              "EFE vía Infobae (26/10/2026): Bilbao, 19 detenidos, 7 menores, charla de Vito Quiles cancelada",
              "Personajes dibujados como pizarras, sin caricatura; la frase de Feijóo es literal y con otra voz"],
             ("🔥 128 detenidos en una noche… y la convocatoria llegó por TikTok\n"
              "📱 «Institutos indignados»: protesta no autorizada y sin organizador conocido\n"
              "🚒 23 comercios destrozados, 33 salidas de bomberos, 14 mossos heridos\n"
              "🧒 72 de los 128 detenidos son menores\n"
              "🗣️ Collboni, Illa, Feijóo y el PSOE: qué ha dicho cada uno\n"
              "📍 El lunes, Bilbao: 19 detenidos\n"
              "💬 ¿Quién debe pagar: los chavales, sus padres o quien lo convoca? Te leemos 👇\n"
              "🔔 Síguenos · 📚 Fuentes en comentarios"),
             "📚 Fuentes: Mossos d'Esquadra (vía Moncloa.com 25/10) · Infobae 25/10 · EFE vía Infobae 26/10. ¿Ves un error? Dínoslo.",
             ["#Barcelona", "#disturbios", "#Mossos", "#Bilbao", "#29N", "#elecciones", "#pizarrapublica"],
             series_tag="EXPLICADO FÁCIL")
