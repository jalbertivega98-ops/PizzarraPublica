#!/usr/bin/env python3
"""«Alcalde y diputado a la vez» (19/10/2026). Mundo dibujado: mapa de España, Congreso, Badalona y las dos gorras de Albiol.

Guion y fuentes: /mnt/project-files/insta/guiones/albiol_barcelona.md (aprobado por joel el 19/10/2026)
  El PP anuncia a Albiol como candidato al Congreso por Barcelona (El Independiente 17/10/2026).
  Mitin del 18/10 en Barcelona: Feijóo le proclama número 1 y le encarga ser ponente de la ley antiokupación
    (pp.es, Infobae, El Debate 18/10/2026); «el político peatonal de Cataluña». Contenido de la ley: sin publicar.
  Barcelona elige 32 diputados el 29N; Madrid 38 (Artículo14 06/10/2026, con el BOE).
  Badalona, cuarta ciudad de Cataluña; mayoría absoluta en 2023 con 18 de 27 concejales (Infobae, ElNacional).
  Desalojo del B9 (diciembre de 2025): vivían unas 400 personas (agencias 17/12/2025, Ara).
  «No me voy de Badalona», «no es para calentar ninguna silla» (Servimedia / Diario Siglo XXI, Pressdigital 18/10/2026).
  Estatutos del PP art. 12.1.c y 12.2 (ElNacional, Diario Siglo XXI); excepción del Comité Ejecutivo Nacional: no publicada.
  PSC de Badalona pide un alcalde accidental hasta el 29N (Metrópoli Abierta 19/10/2026).
"""
from _mundo import *  # noqa: F401,F403

R = "espana"
BCN = P(R, 2.17, 41.39)
MAD = P(R, -3.7, 40.4)
CAB = 520  # de los pies a lo alto de la pizarra (escala 1)
F18 = "pp.es · Infobae · El Debate (18/10/2026)"


def gorras(x, y, s, at1, at2, ids=("g_alc", "g_dip"), escala=0.45, **kw):
    """Las dos gorras sobre la cabeza de un personaje (x, y = pies; s = escala del personaje)."""
    top = y - CAB * s - 10
    return [obj("gorra", x, top, at1, escala, id=ids[0], entra="cae", sfx="pop", props={"texto": "ALCALDE", "color": "naranja"}, **kw),
            obj("gorra", x, top - 70 * escala / 0.45, at2, escala, id=ids[1], entra="cae", sfx="pop",
                props={"texto": "DIPUTADO", "color": "azul"}, **kw)]


scenes = [
    # 1 · GANCHO: Piz se pone la gorra de alcalde… y encima la de diputado, que se tambalea
    dict(id="gancho", fondo="calle", animo="comico", footnote="El Independiente 17/10/2026 · Infobae 18/10/2026", lines=[
        V("¿Se puede ser alcalde y diputado a la vez?", "energia"),
        V("Xavier García Albiol dice que sí.", "normal", 0.1),
        V("Y Feijóo acaba de ficharle.", "remate", 0.1),
    ], camara=[plano(0, "medio", "piz", 0, aire=260), plano("@Albiol", "general", [540, 1000], 0.5),
               plano("@ficharle", "general", [540, 1020], 0.4, zoom=1.05)],
       elements=[
        quien("piz", 540, 0, 0.6, "ilusionado", entra="nada", acciones=[
            {"at": "@alcalde", "mira": "arriba"}, {"at": "@diputado", "cara": "sorpresa", "take": True},
            {"at": "@vez", "cara": "confundido", "pose": "encoge", "mira": "camara"},
            {"at": "@Albiol", "x": 300, "dur": 0.5}, {"at": "@sí", "mira": "der", "cara": "sorpresa"}]),
        *[dict(g, acciones=[{"at": "@Albiol", "x": 300, "dur": 0.5}] + ([{"at": "@vez", "tiembla": True}] if g["id"] == "g_dip" else []))
          for g in gorras(540, 1340, 0.6, "@alcalde", "@diputado")],
        quien("albiol", 1300, "@García", 0.66, "ilusionado", entra="nada", acciones=[
            {"at": "@García", "x": 760, "dur": 0.7}, {"at": "@sí", "pose": "pulgar", "cara": "riendo", "mira": "camara"},
            {"at": "@ficharle", "mira": "izq"}]),
        quien("feijoo", 760, "@Feijóo", 0.42, "riendo", y=1650, entra="abajo", hud=True, acciones=[
            {"at": "@ficharle", "pose": "pulgar"}]),
        rot("¿LAS DOS A LA VEZ?", 540, 430, "@vez", 96, "amarillo", golpe=True, out="@ficharle"),
        rot("FICHAJE DEL PP", 540, 430, "@ficharle", 100, "amarillo", golpe=True),
    ]),
    # 2 · EL MAPA: Barcelona se enciende; 32 escaños, segunda tras Madrid
    dict(id="mapa", fondo="mar_mapa", limites=LIM, animo="aventura", trans="zoom",
         footnote="El Independiente 17/10/2026 · Artículo14 06/10/2026 (BOE)", lines=[
        V("El sábado, el PP le anunció como número uno por Barcelona para el 29 de noviembre.", "normal"),
        V("Barcelona reparte 32 escaños: la segunda provincia con más, tras Madrid.", "normal", 0.15),
    ], camara=[zoom(0, MAD, 1.0, 0), zoom("@Barcelona", BCN, 2.6, 1.0), zoom("@segunda", [720, 700], 1.4, 0.8)],
       elements=[
        mapa(R, 0, 1.4, orden=["Barcelona"], acciones=[
            {"at": "@Barcelona", "props": {"resalta": ["Barcelona"]}, "sfx": "pop"},
            {"at": "@Madrid", "props": {"resalta": ["Barcelona", "Madrid"]}, "sfx": "pop"}]),
        obj("chincheta", BCN[0] + 6, BCN[1], "@Barcelona+0.3", 0.12, props={"diseno": "espana"}, entra="cae"),
        quien("albiol", BCN[0] - 22, "@Barcelona+0.5", 0.07, "ilusionado", y=BCN[1] + 14, entra="cae", acciones=[
            {"at": "@noviembre", "salta": True}, {"at": "@Madrid", "mira": "izq", "cara": "sorpresa"}]),
        rot("Nº 1 POR BARCELONA", 540, 430, "@número", 96, "amarillo", golpe=True, out="@32"),
        obj("contador", 540, 470, "@32", 0.8, hud=True, entra="pop", sfx="kaching", props={"valor": 32, "sufijo": " ESCAÑOS", "ancho": 760}),
        etq("MADRID: 38", 540, 640, "@Madrid", "azul", 0.8, hud=True),
    ]),
    # 3 · EL ENCARGO: Feijóo le pasa el pergamino de la ley; sello PONENTE
    dict(id="encargo", fondo={"tipo": "plano", "color": (28, 52, 110)}, animo="tension", trans="iris", footnote=F18, lines=[
        V("Y el domingo, en Barcelona, Feijóo le hizo un encargo:", "normal"),
        V("«Vas a ser el ponente de la ley. La vamos a aprobar contigo».", "normal", 0.1),
        V("Es decir, el que la defiende en el Congreso. Del texto, aún no hay detalles.", "normal", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@Barcelona", "medio", "feijoo", 0.6, aire=260), plano("@encargo", "general", [540, 1000], 0.5),
               plano("@ponente", "medio", [600, 1050], 0.5, aire=240),
               plano("@Congreso", "general", [540, 950], 0.6), plano("@detalles", "general", [540, 980], 0.4, zoom=1.06)],
       elements=[
        edif("congreso", 540, "@defiende-0.3", 0.6, entra="crece", sfx="pop", dibuja=0.8, acciones=[{"at": "@detalles", "cara": "confundido"}]),
        quien("feijoo", 280, 0, 0.55, "normal", entra="nada", acciones=[
            {"at": "@domingo", "pose": "saluda", "cara": "riendo", "mira": "camara"}, {"at": "@Barcelona", "salta": True},
            {"at": "@encargo", "pose": "senala", "mira": "der", "cara": "ilusionado"}, {"at": "@aprobar", "pose": "pulgar", "cara": "riendo"}]),
        quien("albiol", 800, 0, 0.62, "normal", entra="nada", acciones=[
            {"at": "@domingo", "mira": "izq"}, {"at": "@hizo", "cara": "sorpresa", "take": True}, {"at": "@ponente", "cara": "ilusionado", "salta": True},
            {"at": "@defiende", "pose": "sostiene"}, {"at": "@detalles", "cara": "pensativo", "mira": "camara"}]),
        obj("pergamino", 330, 900, "@encargo", 0.42, id="ley", entra="pop", sfx="papel", props={"titulo": "LEY ANTIOKUPACIÓN", "lineas": ["…", "…"]},
            acciones=[{"at": "@ponente", "x": 760, "y": 880, "dur": 0.6}, {"at": "@detalles", "tiembla": True}]),
        obj("bocadillo", 540, 520, "@Vas", 0.8, hud=True, entra="pop", out="@decir",
            props={"lineas": ["«Vas a ser el ponente.", "La vamos a aprobar contigo»"]}),
        sello("PONENTE", "azul", 560, "@decir", out="@texto"),
        sello("TEXTO: SIN DETALLES", "naranja", 560, "@texto"),
    ]),
    # 4 · QUIÉN ES: el Ayuntamiento de Badalona y la mayoría absoluta
    dict(id="quien", fondo="calle", animo="curioso", trans="barrido", footnote="Infobae 18/10/2026 · ElNacional (resultado de 2023)", lines=[
        V("¿Por qué él? Es alcalde de Badalona, la cuarta ciudad de Cataluña.", "normal"),
        V("En 2023 ganó con mayoría absoluta: 18 de 27 concejales.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@alcalde", "medio", "albiol", 0.5, aire=260),
               plano("@2023", "general", [540, 950], 0.5), plano("@18", "general", [540, 900], 0.4, zoom=1.06)],
       elements=[
        edif("ayuntamiento", 540, 0, 0.62, texto="BADALONA", entra="nada", dibuja=0.8, acciones=[{"at": "@absoluta", "cara": "ilusionado"}]),
        quien("albiol", 1250, 0.1, 0.6, "normal", entra="nada", acciones=[
            {"at": 0.1, "x": 760, "dur": 0.8}, {"at": "@alcalde", "pose": "senala_izq", "mira": "izq", "cara": "ilusionado"},
            {"at": "@absoluta", "salta": True, "cara": "riendo", "pose": "arriba"}]),
        obj("gorra", 1250, 1340 - CAB * 0.6 - 10, 0.1, 0.45, entra="nada", props={"texto": "ALCALDE", "color": "naranja"},
            acciones=[{"at": 0.1, "x": 760, "dur": 0.8}, {"at": "@absoluta", "salta": True}]),
        rot("4.ª CIUDAD DE CATALUÑA", 540, 430, "@cuarta", 64, "amarillo", golpe=True, out="@2023"),
        obj("contador", 540, 460, "@18", 0.8, hud=True, entra="pop", sfx="kaching", props={"valor": 18, "sufijo": " DE 27", "ancho": 640}),
        etq("MAYORÍA ABSOLUTA", 540, 620, "@absoluta", "verde", 0.8, hud=True),
    ]),
    # 5 · EL B9: el edificio desalojado y «el político peatonal»
    dict(id="b9", fondo="calle", animo="tension", trans="corte", footnote="Agencias 17/12/2025 · Ara · Infobae 18/10/2026", lines=[
        V("Y en diciembre de 2025 pidió y logró el desalojo del antiguo instituto B9, donde vivían unas 400 personas.", "normal"),
        V("Feijóo le llama «el político peatonal de Cataluña».", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@desalojo", "general", [540, 900], 0.6, zoom=1.12),
               plano("@400", "general", [540, 950], 0.5, zoom=1.06),
               plano("@Feijóo", "general", [540, 1050], 0.5)],
       elements=[
        edif("abandonado", 540, 0, 0.62, texto="B9", entra="nada", dibuja=0.8, acciones=[
            {"at": "@desalojo", "cara": "susto", "tiembla": True}, {"at": "@instituto", "cara": "triste"}]),
        rot("DIC. 2025", 540, 430, "@diciembre", 100, "amarillo", golpe=True, out="@400"),
        etq("ANTIGUO INSTITUTO", 540, 780, "@instituto", "naranja", 0.8, hud=True, out="@Feijóo"),
        obj("contador", 540, 450, "@400", 0.8, hud=True, entra="pop", sfx="golpe", props={"valor": 400, "prefijo": "~", "sufijo": " PERSONAS", "ancho": 760}),
        sello("CONFIRMADO", "verde", 610, "@personas"),
        quien("albiol", -200, "@peatonal-0.6", 0.5, "ilusionado", y=1500, entra="nada", acciones=[
            {"at": "@peatonal-0.6", "x": 1300, "dur": 2.4}]),
        quien("feijoo", 860, "@Feijóo", 0.42, "riendo", y=1650, entra="abajo", hud=True, acciones=[{"at": "@peatonal", "pose": "senala_izq", "mira": "izq"}]),
        obj("bocadillo", 540, 820, "@llama", 0.75, hud=True, entra="pop", props={"lineas": ["«El político peatonal", "de Cataluña»"]}),
    ]),
    # 6 · EL LÍO: Albiol promete quedarse y corre entre el Ayuntamiento y el Congreso
    dict(id="lio", fondo={"tipo": "plano", "color": (34, 40, 60)}, animo="comico", trans="iris",
         footnote="Servimedia / Diario Siglo XXI · Pressdigital (18/10/2026)", lines=[
        V("Ahora, el lío. Albiol promete: «No me voy de Badalona».", "normal"),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@promete", "medio", [300, 1050], 0.5, aire=260),
               plano("@Badalona", "general", [540, 1000], 0.5)],
       elements=[
        edif("ayuntamiento", 270, 0, 0.5, texto="BADALONA", entra="nada", acciones=[{"at": "@Badalona", "cara": "ilusionado"}]),
        edif("congreso", 820, 0, 0.46, entra="nada", acciones=[{"at": "@Badalona+0.5", "cara": "sorpresa"}]),
        quien("albiol", 300, 0, 0.5, "normal", y=1440, entra="nada", acciones=[
            {"at": "@lío", "x": 780, "dur": 0.6, "corre": True}, {"at": "@promete", "x": 320, "dur": 0.6, "corre": True},
            {"at": "@Badalona", "mira": "camara", "pose": "senala_izq", "cara": "serio"}]),
        obj("bocadillo", 540, 520, "@No", 0.8, hud=True, entra="pop", props={"lineas": ["«No me voy de Badalona»"]}),
        sello("DECLARACIÓN", "azul", 680, "@Badalona"),
    ]),
    # 7 · LAS NORMAS: los estatutos del PP lo prohíben… salvo excepción
    dict(id="estatutos", fondo={"tipo": "plano", "color": (28, 52, 110)}, animo="tension", trans="papel",
         footnote="Estatutos del PP, art. 12 (citados por ElNacional y Diario Siglo XXI)", lines=[
        V("Pero los estatutos de su propio partido dicen que ser diputado es incompatible con ser alcalde de una ciudad de más de 20.000 habitantes.", "normal"),
        V("Hay una salida: el comité nacional del PP puede aprobar una excepción.", "normal", 0.15),
        V("Si la ha aprobado, no se ha hecho público. La ley sí permite tener las dos cosas.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 860], 0), plano("@incompatible", "general", [540, 760], 0.6, zoom=1.1),
               plano("@20.000", "general", [540, 720], 0.6, zoom=1.16), plano("@salida", "general", [540, 900], 0.5),
               plano("@excepción", "general", [540, 960], 0.6, zoom=1.1), plano("@ley", "general", [540, 900], 0.5)],
       elements=[
        obj("documento", 540, 840, 0.2, 1.05, id="doc", entra="nada", dibujo=1.0, sfx="papel", props={
            "titulo": "ESTATUTOS DEL PP", "subtitulo": "Artículo 12",
            "articulos": [{"id": "a121", "titulo": "12.1.c", "lineas": ["diputado: incompatible con", "alcalde de más de 20.000 hab."]},
                          {"id": "a122", "titulo": "12.2", "lineas": ["excepciones: las aprueba", "el Comité Ejecutivo Nacional"]}]},
            acciones=[{"at": "@incompatible", "props": {"resalta": ["a121"]}}, {"at": "@excepción", "props": {"resalta": ["a121", "a122"]}}]),
        quien("albiol", 1250, "@diputado", 0.45, "normal", y=1420, entra="nada", hud=True, acciones=[
            {"at": "@diputado", "x": 880, "dur": 0.6}, {"at": "@incompatible", "cara": "susto", "take": True},
            {"at": "@alcalde", "pose": "cabeza"}, {"at": "@20.000", "cara": "preocupado", "mira": "arriba"},
            {"at": "@salida", "cara": "idea", "salta": True},
            {"at": "@excepción", "cara": "pensativo", "pose": "piensa"}, {"at": "@permite", "cara": "riendo", "pose": "pulgar"}]),
        rot("+20.000 HABITANTES", 540, 330, "@20.000", 80, "amarillo", golpe=True, out="@salida"),
        sello("¿EXCEPCIÓN? SIN CONFIRMAR", "naranja", 1480, "@público", out="@ley"),
        sello("LA LEY: SÍ", "verde", 1480, "@permite"),
    ]),
    # 8 · LAS POSTURAS: el PSC pide un alcalde en funciones; Albiol, que no va a «calentar ninguna silla»
    dict(id="posturas", fondo="calle", animo="tension", trans="corte",
         footnote="Metrópoli Abierta 19/10/2026 · Pressdigital 18/10/2026", lines=[
        V("El PSC de Badalona le pide que deje un alcalde en funciones durante la campaña: «La ciudad necesita plena dedicación».", "normal"),
        V("Albiol responde que no va al Congreso «a calentar ninguna silla».", "normal", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@alcalde", "general", [300, 1000], 0.6, zoom=1.1),
               plano("@campaña", "general", [540, 1000], 0.5), plano("@dedicación", "general", [300, 1000], 0.5, zoom=1.06),
               plano("@Albiol", "general", [760, 1000], 0.5, zoom=1.06), plano("@silla", "general", [540, 1000], 0.4)],
       elements=[
        obj("atril", 280, SUELO_ATRIL, 0, 0.75, entra="nada", props={"texto": "PSC", "color": "psoe"}),
        quien("albiol", 790, "@Albiol-0.3", 0.7, "normal", y=1260, entra="pop", acciones=[
            {"at": "@responde", "mira": "camara", "pose": "senala", "cara": "serio"}, {"at": "@calentar", "pose": "cruzados", "cara": "riendo"}]),
        obj("atril", 790, SUELO_ATRIL, "@Albiol-0.3", 0.75, entra="pop", props={"texto": "PP", "color": "pp"}),
        etq("¿ALCALDE EN FUNCIONES?", 540, 420, "@funciones", "naranja", 0.8, hud=True, out="@ciudad"),
        obj("bocadillo", 300, 560, "@ciudad", 0.7, hud=True, entra="pop", props={"lineas": ["«La ciudad necesita", "plena dedicación»"]}, out="@Albiol"),
        obj("bocadillo", 760, 560, "@Congreso", 0.7, hud=True, entra="pop", props={"lineas": ["«No voy a calentar", "ninguna silla»"]}),
        obj("silla", 540, 1700, "@silla", 0.3, hud=True, entra="cae", sfx="golpe", props={"color": "azul", "texto": "ESCAÑO"},
            acciones=[{"at": "@silla+0.3", "tiembla": True}]),
        sello("DECLARACIONES", "azul", 1000, "@dedicación", out="@Albiol"),
    ]),
    # 9 · FINAL: Piz con una gorra en cada mano
    dict(id="final", fondo="salon", animo="final", trans="iris", footnote="Pregunta a la audiencia", lines=[
        V("¿Alcalde y diputado a la vez: suma o resta? Te leo.", "normal"),
        V("Y síguenos, que hasta el 29N quedan muchos fichajes.", "energia", 0.15),
    ], camara=[plano(0, "medio", "piz", 0, aire=260), plano("@suma", "general", [540, 1000], 0.5),
               plano("@síguenos", "medio", "piz", 0.5, aire=260)],
       elements=[
        quien("piz", 540, 0, 0.62, "pensativo", entra="nada", acciones=[
            {"at": "@Alcalde", "pose": "arriba", "mira": "izq"}, {"at": "@diputado", "mira": "der"},
            {"at": "@suma", "cara": "pensativo", "pose": "piensa", "mira": "camara"}, {"at": "@leo", "cara": "ilusionado", "pose": "senala"},
            {"at": "@síguenos", "pose": "saluda", "cara": "riendo"}, {"at": "@fichajes", "salta": True}]),
        obj("gorra", 230, 1050, "@Alcalde", 0.55, entra="pop", sfx="pop", flota=True, props={"texto": "ALCALDE", "color": "naranja"}),
        obj("gorra", 850, 1050, "@diputado", 0.55, entra="pop", sfx="pop", flota=True, props={"texto": "DIPUTADO", "color": "azul"}),
        rot("¿SUMA O RESTA?", 540, 440, "@suma", 120, "amarillo", golpe=True, out="@síguenos-0.3", fx=[{"at": "@leo", "do": "latir"}]),
        rot("SÍGUENOS", 540, 440, "@síguenos", 110, "amarillo"),
    ]),
]

if __name__ == "__main__":
    episodio("albiol_barcelona", "Alcalde y diputado a la vez", scenes,
             {"t": 3.8, "titulo": "Alcalde y diputado a la vez", "capitulo": None},
             ["El Independiente (17/10/2026): el PP anuncia a Albiol como candidato por Barcelona",
              "pp.es, Infobae y El Debate (18/10/2026): número 1 y ponente de la ley antiokupación",
              "Servimedia / Diario Siglo XXI y Pressdigital (18/10/2026): «No me voy de Badalona»",
              "ElNacional: estatutos del PP, art. 12.1.c y 12.2; resultado de 2023",
              "Artículo14 (06/10/2026): 32 escaños en Barcelona, 38 en Madrid",
              "Agencias (17/12/2025) y Ara: desalojo del B9",
              "Metrópoli Abierta (19/10/2026): el PSC de Badalona pide un alcalde accidental",
              "Personajes dibujados como pizarras, sin caricatura"],
             ("🧢 ¿Se puede ser alcalde y diputado a la vez? Albiol dice que sí\n"
              "🗳️ Feijóo le ficha como número 1 del PP por Barcelona para el 29N\n"
              "📜 Y le encarga ser el ponente de la ley antiokupación (aún sin texto)\n"
              "🏛️ Promete: «No me voy de Badalona»\n"
              "⚖️ Los estatutos del PP lo ven incompatible, salvo excepción\n"
              "💬 ¿Alcalde y diputado a la vez: suma o resta? Te leemos 👇\n"
              "🔔 Síguenos · 📚 Fuentes en comentarios"),
             "📚 Fuentes: El Independiente 17/10/2026 · pp.es, Infobae y El Debate 18/10/2026 · Servimedia 18/10/2026 · "
             "ElNacional · Artículo14 06/10/2026 · Metrópoli Abierta 19/10/2026. ¿Ves un error? Dínoslo.",
             ["#29N", "#Albiol", "#Badalona", "#Barcelona", "#Feijóo", "#PP", "#elecciones", "#pizarrapublica"],
             series_tag="EXPLICADO FÁCIL")
