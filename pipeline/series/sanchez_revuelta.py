#!/usr/bin/env python3
"""«Sánchez en La Revuelta: lo mejor… con datos» (viernes 23/10/2026). Resumen de la entrevista del 22/10/2026 en La 1.

Sánchez sale como la pizarra que diseñó joel (traje azul, corbata roja, logo del PSOE). Sus frases son literales
tal y como las publicó la prensa; las indirectas del narrador siempre se apoyan en un dato.

Fuentes (detalle en docs/series/sanchez_revuelta/guion.md):
  eldiario.es/Vertele 23/10/2026: 4,4 millones y 33,9 % de cuota, récord de La Revuelta.
  Infobae 22/10/2026 · Última Hora 23/10/2026 · El Independiente 22/10/2026 · Diario de Pontevedra 23/10/2026: frases.
  SMI: 735,90 € en 2018 (RD 1077/2017) y 1.221 € en 2026 (RD 126/2026): +65,9 %.
  Idealista vía ESdiario 06/10/2026: vivienda usada +74,4 % desde junio de 2018.
  Consejo de la Juventud (Observatorio de Emancipación) vía Euronews 22/05/2026: el alquiler en solitario = 98,7 % del sueldo joven.
  eldiario.es 22/06/2026 e Infobae 14/10/2026: el Supremo condena a Ábalos a 24 años y 3 meses; rechaza su nulidad.
  Wikipedia/Europa Press: Cerdán, secretario de Organización 2021-2025, en prisión provisional del 30/06 al 19/11/2025.
  Audiencia de Badajoz 14/07/2026: David Sánchez, 9 años de inhabilitación; recurrido, no es firme.
"""
from _mundo import *  # noqa: F401,F403

FRENTE_Y = 1640
F_AUD = "eldiario.es/Vertele 23/10/2026"
F_FRASES = "Infobae 22/10 · Última Hora 23/10 · El Independiente 22/10/2026"
REV = {"tipo": "plato", "rotulo": "LA REVUELTA"}


def bocadillo(lineas, x, y, at, cola=(-1, 1), out=None, scale=1.0):
    d = obj("bocadillo", x, y, at, scale, hud=True, entra="pop", sfx="pop", props={"lineas": lineas, "cola": cola})
    if out:
        d["out"] = out
    return d


scenes = [
    # 1 · GANCHO: entra en el plató con el marcador de audiencia
    dict(id="gancho", fondo=REV, animo="alegre", footnote=F_AUD, lines=[
        V("Más de cuatro millones vieron a Sánchez en La Revuelta.", "energia"),
        V("Te lo resumo… con datos.", "remate", 0.1),
    ], camara=[plano(0, "general", [540, 950], 0, zoom=1.15), plano("@Sánchez", "general", [440, 980], 0.5, zoom=1.25),
               plano("@resumo", "general", [540, 950], 0.5, zoom=1.15)],
       elements=[
        quien("broncano", 790, 0, 0.72, "riendo", entra="nada", acciones=[
            {"at": 0.3, "pose": "saluda", "mira": "izq"}, {"at": "@Revuelta", "salta": True}, {"at": "@resumo", "mira": "camara"}]),
        quien("sanchez", -220, 0.05, 0.75, "ilusionado", entra="nada", acciones=[
            {"at": 0.1, "x": 330, "dur": 1.1}, {"at": "@Sánchez", "pose": "saluda", "cara": "riendo"},
            {"at": "@resumo", "mira": "camara", "cara": "burla", "pose": "senala_arriba"}]),
        rot("4,4 MILLONES", 540, 470, 0.3, 120, "amarillo", golpe=True, out="@resumo"),
        sello("RÉCORD", "rojo", 650, "@millones", out="@resumo"),
        rot("CON DATOS", 540, 470, "@datos", 110, "rojo", golpe=True),
    ]),
    # 2 · MOMENTO 1: «esta televisión es mía»… en la tele pública
    dict(id="tele", fondo=REV, animo="comico", trans="corte", footnote=F_FRASES, lines=[
        V("Nada más entrar: «Luego me dicen que esta televisión es mía».", "normal"),
        V("Lo dijo en La 1. La tele pública.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 950], 0, zoom=1.15), plano("@televisión", "medio", "sanchez", 0.5, aire=260),
               plano("@pública", "general", [540, 950], 0.5, zoom=1.15)],
       elements=[
        quien("sanchez", 330, 0, 0.75, "burla", entra="nada", acciones=[
            {"at": "@Luego", "pose": "senala", "mira": "der"}, {"at": "@mía", "mira": "camara", "cara": "riendo"},
            {"at": "@pública", "cara": "burla", "pose": "encoge"}]),
        quien("broncano", 790, 0, 0.72, "riendo", entra="nada", acciones=[
            {"at": "@mía", "salta": True}, {"at": "@pública", "mira": "izq", "pose": "jarras"}]),
        bocadillo(["«LUEGO ME DICEN QUE ESTA", "TELEVISIÓN ES MÍA»"], 560, 560, "@Luego-0.1", out="@Lo"),
        obj("tele", 560, 560, "@La#1", 0.6, hud=True, entra="crece", sfx="pop", out="@pública", props={"texto": "LA 1"}),
        rot("TELE PÚBLICA", 540, 560, "@pública", 100, "amarillo", golpe=True),
    ]),
    # 3 · MOMENTO 2: las preguntas clásicas
    dict(id="clasicas", fondo=REV, animo="comico", trans="barrido", footnote=F_FRASES, lines=[
        V("Sexo: «Tenemos una vida sexual activa y sana».", "normal"),
        V("¿Y su dinero? Al Portal de Transparencia.", "normal", 0.1),
        V("De sexo, todo. De dinero, al portal.", "remate", 0.2),
    ], camara=[plano(0, "general", [540, 950], 0, zoom=1.15), plano("@sana", "medio", "sanchez", 0.5, aire=260),
               plano("@dinero", "general", [540, 950], 0.5, zoom=1.15), plano("@todo", "general", [540, 980], 0.4, zoom=1.22)],
       elements=[
        quien("broncano", 790, 0, 0.72, "burla", entra="nada", acciones=[
            {"at": "@Sexo", "pose": "senala_izq", "mira": "izq"}, {"at": "@dinero", "pose": "senala_izq", "cara": "pensativo"},
            {"at": "@todo", "cara": "riendo", "salta": True}]),
        quien("sanchez", 330, 0, 0.75, "normal", entra="nada", acciones=[
            {"at": "@Sexo", "cara": "ilusionado", "pose": "pulgar"}, {"at": "@sana", "salta": True},
            {"at": "@dinero", "cara": "susto", "take": True}, {"at": "@Portal", "cara": "pensativo", "pose": "empuja", "mira": "der"},
            {"at": "@todo", "cara": "burla", "pose": "encoge"}]),
        bocadillo(["«TENEMOS UNA VIDA", "SEXUAL ACTIVA Y SANA»"], 560, 560, "@Tenemos-0.1", out="@dinero"),
        obj("cartel", 640, 620, "@Portal-0.2", 0.9, hud=True, entra="crece", sfx="papel", out="@todo",
            props={"lineas": ["PORTAL DE", "TRANSPARENCIA"]}),
        rot("SEXO: TODO", 540, 480, "@todo", 96, "verde", golpe=True),
        rot("DINERO: AL PORTAL", 540, 610, "@portal#2", 86, "rojo", golpe=True),
    ]),
    # 4 · MOMENTO 3: el madrazo (pose del diseño de joel: dedo arriba tras el atril)
    dict(id="madre", fondo={"tipo": "rayos", "color": "rojo"}, animo="tension", trans="zoom",
         footnote="SMI: RD 1077/2017 y RD 126/2026 · Vivienda usada: Idealista (ESdiario 06/10/2026)", lines=[
        V("El madrazo: «Se acuerdan de mi madre, yo también de las suyas cuando subo las pensiones o el salario mínimo».", "energia"),
        V("El salario mínimo ha subido un sesenta y seis por ciento. Verdad.", "normal", 0.1),
        V("Pero el piso usado, un setenta y cuatro.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@madre", "general", [400, 1000], 0.5, zoom=1.1),
               plano("@salario#2", "general", [540, 1000], 0.6), plano("@piso", "general", [540, 1000], 0.3, zoom=1.04)],
       elements=[
        obj("bandera", 110, 1160, 0, 0.8, entra="nada", props={"diseno": "espana"}),
        quien("sanchez", 260, 0, 0.75, "burla", y=1200, entra="nada", acciones=[
            {"at": 0.2, "pose": "senala_arriba"}, {"at": "@madre", "cara": "enfado"}, {"at": "@suyas", "cara": "burla", "pose": "senala_arriba"},
            {"at": "@pensiones", "cara": "ilusionado", "pose": "punos"}, {"at": "@verdad", "pose": "pulgar", "cara": "riendo"},
            {"at": "@piso", "cara": "preocupado", "tiembla": True}, {"at": "@cuatro", "pose": "encoge"}]),
        obj("atril", 260, 1420, 0, 0.62, entra="nada", props={"texto": "PSOE", "color": "psoe"}),
        bocadillo(["«SE ACUERDAN DE MI MADRE,", "YO TAMBIÉN DE LAS SUYAS…»"], 560, 430, "@Se-0.1", out="@salario#2"),
        obj("barras", 720, 640, "@salario#2", 0.62, hud=True, entra="crece", sfx="papel",
            props={"barras": [{"valor": 66, "texto": "SALARIO MÍN.", "color": "verde"},
                              {"valor": 74, "texto": "PISO USADO", "color": "rojo"}],
                   "sufijo": " %", "decimales": 0, "tope": 90, "resalta": [1]}),
        sello("CIERTO", "verde", 1000, "@verdad", out="@piso", x=620),
        rot("DESDE 2018", 720, 1000, "@piso", 72, "amarillo", golpe=True),
    ]),
    # 5 · MOMENTO 4: la vivienda y los 176 escaños
    dict(id="vivienda", fondo="calle", animo="tension", trans="barrido",
         footnote="El Independiente 22/10 · Infobae 22/10 · CJE (Euronews 22/05/2026)", lines=[
        V("Vivienda: «Comparto la preocupación, pero necesito herramientas». Pide ciento setenta y seis escaños.", "normal"),
        V("Lleva ocho años en Moncloa.", "remate", 0.1),
        V("Hoy, un joven que alquila solo se deja el noventa y ocho coma siete por ciento del sueldo.", "energia", 0.15),
    ], camara=[plano(0, "general", [540, 1050], 0), plano("@escaños", "general", [540, 900], 0.5),
               plano("@joven", "general", [700, 1100], 0.6), plano("@sueldo", "general", [600, 1050], 0.4, zoom=1.1)],
       elements=[
        quien("sanchez", 320, 0, 0.7, "pensativo", entra="nada", acciones=[
            {"at": "@Comparto", "pose": "manos_juntas", "cara": "preocupado"}, {"at": "@herramientas", "pose": "ruega", "mira": "camara"},
            {"at": "@escaños", "cara": "ilusionado", "pose": "arriba"}, {"at": "@ocho", "cara": "susto", "take": True},
            {"at": "@sueldo", "cara": "preocupado", "mira": "der"}]),
        obj("contador", 540, 480, "@Pide", 0.75, hud=True, entra="crece", sfx="calculadora", out="@ocho",
            props={"valor": 176, "sufijo": " ESCAÑOS"}),
        obj("calendario", 540, 540, "@ocho-0.1", 0.45, hud=True, entra="cae", sfx="golpe", out="@joven",
            props={"mes": "8 AÑOS", "inicio": 1, "dias": 31, "marcados": [], "colores": {}}),
        rot("8 AÑOS EN LA MONCLOA", 540, 880, "@ocho", 76, "rojo", golpe=True, out="@joven"),
        quien("piz", 1250, "@joven-0.4", 0.55, "ilusionado", y=FRENTE_Y, entra="nada", acciones=[
            {"at": "@joven", "x": 760, "dur": 0.7}, {"at": "@alquila", "cara": "preocupado"},
            {"at": "@noventa", "cara": "susto", "aplasta": True}, {"at": "@sueldo", "tiembla": True}]),
        obj("contador", 540, 480, "@noventa", 0.75, hud=True, entra="crece", sfx="calculadora",
            props={"valor": 98.7, "decimales": 1, "sufijo": " %"}),
        rot("DEL SUELDO, EN ALQUILER", 540, 640, "@sueldo-0.2", 66, "amarillo", golpe=True),
    ]),
    # 6 · MOMENTO 5: Ábalos y Cerdán (se queda helado)
    dict(id="abalos", fondo="oficina", animo="tension", trans="corte",
         footnote="Última Hora 23/10 · El Independiente 22/10 · eldiario.es 22/06/2026 · Infobae 14/10/2026", lines=[
        V("Ábalos: «Crees conocer a la gente… y te quedas helado».", "normal"),
        V("¿No lo vio venir? «De verdad que no».", "normal", 0.1),
        V("Su secretario de Organización: veinticuatro años de cárcel.", "energia", 0.1),
        V("Y Cerdán, el siguiente: casi cinco meses en prisión provisional.", "remate", 0.1),
    ], camara=[plano(0, "general", [540, 1050], 0), plano("@helado", "primero", "sanchez", 0.4),
               plano("@secretario", "general", [540, 900], 0.5), plano("@Cerdán", "general", [540, 900], 0.4, zoom=1.05)],
       elements=[
        quien("sanchez", 330, 0, 0.75, "pensativo", entra="nada", acciones=[
            {"at": "@conocer", "cara": "triste"}, {"at": "@helado", "cara": "helado", "tiembla": True, "pose": "cabeza"},
            {"at": "@vio", "cara": "normal", "pose": "normal"}, {"at": "@verdad", "cara": "serio", "pose": "cruzados"},
            {"at": "@veinticuatro", "cara": "susto", "take": True}, {"at": "@Cerdán", "cara": "preocupado", "mira": "der"}]),
        bocadillo(["«CREES CONOCER A LA GENTE…", "Y TE QUEDAS HELADO»"], 560, 480, "@Crees-0.1", out="@No"),
        bocadillo(["«DE VERDAD", "QUE NO»"], 520, 520, "@De-0.1", out="@secretario"),
        obj("cartel", 760, 560, "@secretario", 0.72, hud=True, entra="crece", sfx="papel",
            props={"lineas": ["ÁBALOS", "SECRETARIO DE", "ORGANIZACIÓN"]}),
        sello("24 AÑOS DE CÁRCEL", "rojo", 760, "@veinticuatro", x=760),
        obj("cartel", 760, 1030, "@Cerdán", 0.72, hud=True, entra="crece", sfx="papel",
            props={"lineas": ["CERDÁN", "EL SIGUIENTE"]}),
        sello("PRISIÓN PROVISIONAL 2025", "naranja", 1210, "@provisional", x=760),
        quien("critica", 120, 0, 0.42, "esceptica", y=FRENTE_Y, entra="nada", acciones=[
            {"at": "@vio", "mira": "der"}, {"at": "@verdad", "cara": "esceptica", "pose": "cruzados"},
            {"at": "@veinticuatro", "cara": "sorpresa", "salta": True}]),
    ]),
    # 7 · MOMENTO 6: su familia
    dict(id="familia", fondo="salon", animo="triste", trans="papel",
         footnote="Última Hora 23/10/2026 · Audiencia de Badajoz 14/07/2026 (recurrida)", lines=[
        V("Su hermano y su mujer: «Dos personas que son inocentes».", "normal"),
        V("Su hermano está condenado. Eso sí, la sentencia no es firme.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 1050], 0), plano("@inocentes", "medio", "sanchez", 0.4, aire=260),
               plano("@condenado", "general", [540, 950], 0.5)],
       elements=[
        quien("sanchez", 330, 0, 0.75, "serio", entra="nada", acciones=[
            {"at": "@hermano", "pose": "sostiene2"}, {"at": "@inocentes", "cara": "indignado", "pose": "punos"},
            {"at": "@condenado", "cara": "preocupado", "pose": "manos_juntas"}, {"at": "@firme", "cara": "normal", "mira": "camara"}]),
        bocadillo(["«DOS PERSONAS QUE", "SON INOCENTES»"], 560, 520, "@Dos-0.1", out="@Su"),
        sello("CONDENADO", "rojo", 560, "@condenado", x=700),
        sello("NO FIRME", "naranja", 760, "@firme", x=700),
    ]),
    # 8 · MOMENTO 7: Ceuta
    dict(id="ceuta", fondo="ceuta", animo="comico", trans="pan", footnote=F_FRASES, lines=[
        V("Ceuta: «Sin duda alguna, podríamos haberlo gestionado mejor».", "normal"),
        V("Por fin, algo en lo que estamos todos de acuerdo.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 1050], 0), plano("@mejor", "general", [400, 1050], 0.4, zoom=1.1),
               plano("@acuerdo", "general", [540, 1100], 0.4)],
       elements=[
        quien("sanchez", 230, 0, 0.72, "preocupado", entra="nada", acciones=[
            {"at": "@duda", "pose": "encoge"}, {"at": "@mejor", "cara": "triste", "pose": "caidos"},
            {"at": "@acuerdo", "mira": "der", "cara": "confundido"}]),
        bocadillo(["«PODRÍAMOS HABERLO", "GESTIONADO MEJOR»"], 560, 520, "@Sin-0.1", out="@Por"),
        quien("piz", 470, "@Por-0.3", 0.5, "esceptica", y=FRENTE_Y, entra="abajo", acciones=[{"at": "@todos", "salta": True, "cara": "riendo"}]),
        quien("critica", 670, "@Por-0.2", 0.5, "esceptica", y=FRENTE_Y, entra="abajo", acciones=[{"at": "@todos", "salta": True, "cara": "riendo"}]),
        quien("pizon", 870, "@Por-0.1", 0.5, "confundido", y=FRENTE_Y, entra="abajo", acciones=[{"at": "@todos", "salta": True, "cara": "riendo"}]),
        sello("DE ACUERDO", "verde", 700, "@acuerdo"),
    ]),
    # 9 · FINAL: ¿y Jordi Wild? «Ya responderé»
    dict(id="final", fondo=REV, animo="final", trans="iris", footnote=F_FRASES, lines=[
        V("¿Y Jordi Wild? «Ya responderé».", "normal"),
        V("¿Entrevista valiente o paseo? Te leo. Y síguenos.", "energia", 0.2),
    ], camara=[plano(0, "general", [540, 950], 0, zoom=1.15), plano("@responderé", "general", [640, 980], 0.4, zoom=1.22),
               plano("@valiente", "general", [540, 950], 0.5, zoom=1.1)],
       elements=[
        quien("sanchez", 330, 0, 0.75, "burla", entra="nada", acciones=[
            {"at": "@Wild", "cara": "susto", "take": True}, {"at": "@responderé", "cara": "burla", "pose": "saluda"},
            {"at": "@responderé+0.5", "x": 1350, "dur": 1.4, "corre": True}]),
        quien("wild", 1300, "@Wild-0.4", 0.55, "pensativo", y=FRENTE_Y, entra="nada", objeto="movil", pose="sostiene", acciones=[
            {"at": "@Wild", "x": 760, "dur": 0.6}, {"at": "@responderé", "cara": "esceptica", "mira": "izq"},
            {"at": "@paseo", "pose": "encoge", "mira": "camara"}]),
        bocadillo(["«YA RESPONDERÉ»"], 520, 560, "@Ya-0.1", out="@Entrevista"),
        rot("¿VALIENTE O PASEO?", 540, 480, "@valiente", 90, "rojo", golpe=True, out="@síguenos-0.3"),
        rot("SÍGUENOS", 540, 480, "@síguenos", 110, "rojo"),
        quien("piz", 300, "@leo-0.4", 0.5, "riendo", y=FRENTE_Y, entra="abajo", acciones=[
            {"at": "@leo", "pose": "senala", "mira": "camara"}, {"at": "@síguenos", "pose": "saluda", "salta": True}]),
    ]),
]

if __name__ == "__main__":
    episodio("sanchez_revuelta", "Sánchez en La Revuelta: lo mejor… con datos", scenes,
             {"t": 3.4, "titulo": "Sánchez en La Revuelta: lo mejor… con datos", "capitulo": None},
             ["eldiario.es/Vertele (23/10/2026): 4,4 millones de espectadores y 33,9 % de cuota",
              "Infobae (22/10/2026), Última Hora y Diario de Pontevedra (23/10/2026), El Independiente (22/10/2026): frases literales de Sánchez",
              "BOE: SMI 735,90 € en 2018 (RD 1077/2017) y 1.221 € en 2026 (RD 126/2026), +66 %",
              "Idealista vía ESdiario (06/10/2026): vivienda usada +74,4 % desde junio de 2018",
              "Consejo de la Juventud de España, Observatorio de Emancipación (Euronews 22/05/2026): alquiler en solitario = 98,7 % del sueldo joven",
              "eldiario.es (22/06/2026) e Infobae (14/10/2026): el Supremo condena a Ábalos a 24 años y 3 meses",
              "Europa Press / Wikipedia: Cerdán en prisión provisional del 30/06 al 19/11/2025",
              "Audiencia de Badajoz (14/07/2026): David Sánchez, 9 años de inhabilitación; sentencia recurrida, no firme",
              "Frases reales de la entrevista; personajes dibujados como pizarras"],
             ("📺 Sánchez en La Revuelta: 4,4 millones de personas, récord del programa\n"
              "😏 «Luego me dicen que esta televisión es mía»… dicho en La 1, la tele pública\n"
              "🛏️ Sexo: «vida sexual activa y sana». Dinero: al Portal de Transparencia\n"
              "👵 «Se acuerdan de mi madre…»: el salario mínimo ha subido un 66 %, sí. El piso usado, un 74 %\n"
              "🏠 Pide 176 escaños para la vivienda tras 8 años en Moncloa; un joven que alquila solo se deja el 98,7 % del sueldo\n"
              "🥶 Ábalos: «te quedas helado». Condenado por el Supremo a 24 años. Cerdán, casi 5 meses en prisión provisional\n"
              "⚖️ «Son inocentes»: su hermano está condenado (sentencia no firme)\n"
              "🌊 Ceuta: «podríamos haberlo gestionado mejor»\n"
              "🎙️ ¿Y Jordi Wild? «Ya responderé»\n"
              "💬 ¿Entrevista valiente o paseo? Te leo 👇\n"
              "🔔 Síguenos · 📚 Fuentes en comentarios"),
             "📚 Fuentes: eldiario.es/Vertele 23/10/2026 · Infobae 22/10/2026 · Última Hora 23/10/2026 · El Independiente 22/10/2026 · "
             "BOE (RD 1077/2017 y RD 126/2026) · Idealista (ESdiario 06/10/2026) · CJE Observatorio de Emancipación (Euronews 22/05/2026) · "
             "eldiario.es 22/06/2026 · Infobae 14/10/2026 · Audiencia de Badajoz 14/07/2026. Frases literales publicadas por la prensa. "
             "¿Ves un error? Dínoslo.",
             ["#PedroSánchez", "#LaRevuelta", "#Broncano", "#29N", "#elecciones", "#vivienda", "#pizarrapublica"],
             series_tag="EXPLICADO FÁCIL")
