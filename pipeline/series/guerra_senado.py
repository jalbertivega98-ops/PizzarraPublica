#!/usr/bin/env python3
"""«La guerra del Senado» (martes 20/10/2026, 20:00). Mundo dibujado: la papeleta sepia y el mapa de los senadores.

Guion y fuentes: /mnt/project-files/insta/guiones/lunes_martes_19_20oct.md
  Infobae 17/10/2026: PSOE y Frente Amplio, «Senado de Progreso», papeleta única en 47 circunscripciones (no en Cataluña ni en
    Canarias salvo La Gomera); 208 senadores elegidos directamente; 2023: PP 120, PSOE 72.
  El Español 18/10/2026: cada provincia elige cuatro senadores, se marcan hasta tres; el primero suele sacar tres y el segundo uno;
    el CEN de Vox decide el lunes 19/10 si negocia con el PP; tres quintos para renovar el Constitucional y el CGPJ.
  Vozpópuli: simulación con los votos de 2023, hasta 15 senadores más para las listas conjuntas.
  VOX_DECIDE: frase de la escena «vox» pendiente de la decisión del lunes 19/10.
"""
from _mundo import *  # noqa: F401,F403

R = "espana"
SEV = P(R, -5.9, 37.4)
TODAS = ['Albacete', 'Alicante', 'Almería', 'Asturias', 'Badajoz', 'Baleares', 'Barcelona', 'Bizkaia', 'Burgos', 'Cantabria',
         'Castellón', 'Ceuta', 'Ciudad Real', 'Cuenca', 'Cáceres', 'Cádiz', 'Córdoba', 'Gerona', 'Gipuzkoa', 'Granada', 'Guadalajara',
         'Huelva', 'Huesca', 'Jaén', 'La Coruña', 'La Rioja', 'Las Palmas', 'León', 'Lugo', 'Lérida', 'Madrid', 'Melilla', 'Murcia',
         'Málaga', 'Navarra', 'Orense', 'Palencia', 'Pontevedra', 'Salamanca', 'Santa Cruz de Tenerife', 'Segovia', 'Sevilla', 'Soria',
         'Tarragona', 'Teruel', 'Toledo', 'Valencia', 'Valladolid', 'Zamora', 'Zaragoza', 'Álava', 'Ávila']
FUERA = {'Barcelona', 'Tarragona', 'Lérida', 'Gerona', 'Las Palmas', 'Santa Cruz de Tenerife'}
JUNTOS = [p for p in TODAS if p not in FUERA]
FINF = "Infobae 17/10/2026"
FESP = "El Español 18/10/2026"
VOX_DECIDE = "Y el lunes, Vox decidía si negocia con el PP retirarse en algunas provincias a cambio de ir en sus listas."


def sillas_prov(at, colores, x0=330, y=1420, s=0.32, paso=140):
    return [obj("silla", x0 + i * paso, y, f"{at}+{i * 0.15:.2f}" if isinstance(at, str) else at + i * 0.15, s, entra="cae", sfx="golpe",
                props={"color": col}) for i, col in enumerate(colores)]


scenes = [
    # 1 · GANCHO: el PSOE y el Frente Amplio se dan la mano… solo delante de la puerta del Senado
    dict(id="gancho", fondo="calle", animo="tension", footnote=FINF, lines=[
        V("Por primera vez, el PSOE y el Frente Amplio van juntos…", "energia"),
        V("pero solo al Senado. ¿Por qué?", "remate", 0.1),
    ], camara=[plano(0, "medio", "sanchez", 0, aire=220), plano("@juntos", "general", [540, 1000], 0.5),
               plano("@Senado", "general", [540, 950], 0.4, zoom=1.06), plano("@Por", "medio", "piz", 0.4, aire=200)],
       elements=[
        edif("congreso", 540, "@Senado", 0.55, dibuja=0.9),
        quien("sanchez", -200, 0, 0.5, "ilusionado", entra="nada", acciones=[
            {"at": 0.1, "x": 380, "dur": 0.8}, {"at": "@juntos", "pose": "saluda", "mira": "der"}]),
        quien("pizon", 1300, 0, 0.5, "ilusionado", entra="nada", id="fa", acciones=[
            {"at": 0.1, "x": 700, "dur": 0.8}, {"at": "@juntos", "pose": "saluda", "mira": "izq"}]),
        etq("FRENTE AMPLIO", 700, 1520, "@Frente", "rojo", 0.6),
        rot("SOLO AL SENADO", 540, 520, "@Senado", 96, "amarillo", golpe=True),
        quien("piz", 540, "@Por-0.3", 0.4, "confundido", y=1700, hud=True, entra="abajo", acciones=[{"at": "@qué", "pose": "encoge"}]),
    ]),
    # 2 · CÓMO SE VOTA: papeleta sepia, tres cruces, y el reparto 3 + 1 en una provincia
    dict(id="reglas", fondo="colegio", animo="curioso", trans="papel", footnote=FESP, lines=[
        V("Porque en el Senado casi todas las provincias eligen cuatro senadores,", "normal"),
        V("tú marcas hasta tres,", "normal", 0.05),
        V("y lo normal es que el primero se lleve tres y el segundo, uno.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@tres", "general", [540, 820], 0.5, zoom=1.08),
               plano("@primero", "general", [540, 1200], 0.6)],
       elements=[
        obj("cartel", 540, 760, "@marcas", 0.85, entra="crece", sfx="papel", dibuja=1.0, props={
            "lineas": ["SENADO", "X  CANDIDATO A", "X  CANDIDATO B", "X  CANDIDATO C", "    CANDIDATO D"],
            "color": (236, 214, 176)}),
        obj("contador", 540, 460, "@cuatro", 0.6, hud=True, entra="pop", sfx="kaching",
            props={"valor": 4, "sufijo": " SENADORES", "ancho": 760}, out="@marcas"),
        rot("MARCAS 3", 540, 460, "@marcas", 96, "amarillo", golpe=True, out="@primero"),
        *sillas_prov("@primero", ["rojo", "rojo", "rojo", "azul"]),
        rot("3 + 1", 540, 460, "@segundo", 120, "amarillo", golpe=True),
        quien("piz", 120, 0, 0.42, "pensativo", y=1640, entra="nada", acciones=[
            {"at": "@tres", "pose": "senala", "cara": "idea"}, {"at": "@segundo", "cara": "sorpresa", "take": True}]),
    ]),
    # 3 · 2023: si la izquierda se divide, el primero suele ser el PP
    dict(id="2023", fondo={"tipo": "plano", "color": (28, 52, 110)}, animo="curioso", trans="barrido", footnote=FINF, lines=[
        V("Si la izquierda se divide, el primero suele ser el PP.", "normal"),
        V("En 2023 sacó 120 de los 208 senadores que se votan; el PSOE, 72.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@120", "general", [540, 900], 0.5, zoom=1.06)],
       elements=[
        obj("barras", 540, 980, "@2023-0.2", 1.0, entra="nada", dibuja=1.6, props={"tope": 208, "decimales": 0, "barras": [
            {"texto": "PP", "valor": 120, "color": "pp"}, {"texto": "PSOE", "valor": 72, "color": "psoe"}]}),
        rot("DE 208", 540, 420, "@208", 100, "amarillo", golpe=True),
        quien("critica", 900, 0, 0.42, "esceptica", y=1640, entra="nada", acciones=[
            {"at": "@divide", "pose": "cruzados"}, {"at": "@PP", "cara": "sorpresa"}, {"at": "@72", "mira": "izq", "cara": "pensativo"}]),
    ]),
    # 4 · SENADO DE PROGRESO: el mapa se pinta de una sola papeleta en 47 circunscripciones
    dict(id="mapa", fondo="mar_mapa", limites=LIM, animo="aventura", trans="zoom", footnote=FINF, lines=[
        V("Por eso ahora van juntos con el nombre de «Senado de Progreso», en 47 provincias.", "normal"),
    ], camara=[zoom(0, P(R, -3.7, 40.0), 1.0, 0), zoom("@47", P(R, -3.7, 40.0), 1.12, 0.8)],
       elements=[
        mapa(R, 0, 1.0, acciones=[{"at": "@juntos", "props": {"resalta": JUNTOS[:20]}, "sfx": "pop"},
                                  {"at": "@Progreso", "props": {"resalta": JUNTOS}, "sfx": "kaching"}]),
        rot("«SENADO DE PROGRESO»", 540, 330, "@nombre", 80, "amarillo", golpe=True, hud=True),
        obj("contador", 540, 1200, "@47", 0.6, hud=True, entra="pop", sfx="kaching", props={"valor": 47, "sufijo": " CIRCUNSCRIPCIONES", "ancho": 860}),
    ]),
    # 5 · LA RESPUESTA DE PP Y VOX
    dict(id="vox", fondo="calle", animo="tension", trans="pan", footnote=FESP, lines=[
        V(VOX_DECIDE, "normal"),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@PP", "general", [540, 950], 0.6, zoom=1.06)],
       elements=[
        quien("feijoo", 330, 0, 0.5, "pensativo", entra="nada", acciones=[{"at": "@Vox", "mira": "abascal"}, {"at": "@listas", "pose": "pulgar"}]),
        quien("abascal", 760, 0, 0.5, "pensativo", entra="nada", acciones=[{"at": "@Vox", "pose": "piensa"}, {"at": "@listas", "mira": "feijoo"}]),
        sello("PENDIENTE", "naranja", 600, "@decidía"),
    ]),
    # 6 · LA SIMULACIÓN: hasta 15 senadores
    dict(id="simulacion", fondo="mar_mapa", limites=LIM, animo="tension", trans="zoom", footnote="Vozpópuli (simulación con los votos de 2023)", lines=[
        V("Con los votos de 2023, juntos podrían quitarle a la izquierda hasta 15 senadores.", "normal"),
    ], camara=[zoom(0, SEV, 2.2, 0), zoom("@15", P(R, -3.7, 40.0), 1.0, 1.2)],
       elements=[
        mapa(R, 0, 0.01, progreso=1.0, acciones=[{"at": "@juntos", "props": {"resalta": ["Sevilla", "Badajoz", "Cáceres", "Huelva", "Valencia",
                                                                                          "Santa Cruz de Tenerife", "Las Palmas", "Baleares",
                                                                                          "Barcelona", "Tarragona", "Álava", "Navarra"]}, "sfx": "pop"}]),
        obj("contador", 540, 1200, "@15", 0.6, hud=True, entra="pop", sfx="kaching", props={"valor": 15, "prefijo": "HASTA ", "sufijo": " SENADORES", "ancho": 860}),
        sello("SIMULACIÓN", "naranja", 1400, "@senadores"),
    ]),
    # 7 · QUÉ ESTÁ EN JUEGO: los tres quintos
    dict(id="juego", fondo={"tipo": "plano", "color": (28, 52, 110)}, animo="tension", trans="papel", footnote=FESP, lines=[
        V("¿Qué está en juego? Los tres quintos del Senado,", "normal"),
        V("necesarios para renovar el Constitucional y el CGPJ sin el otro bloque.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@Constitucional", "general", [540, 1000], 0.5, zoom=1.06)],
       elements=[
        rot("3/5", 540, 520, "@quintos", 200, "amarillo", golpe=True),
        obj("libro", 330, 1050, "@Constitucional", 0.8, entra="cae", sfx="golpe", props={"titulo": "CONSTITUCIONAL", "color": "rojo"}),
        obj("libro", 750, 1050, "@CGPJ", 0.8, entra="cae", sfx="golpe", props={"titulo": "CGPJ", "color": "azul"}),
        quien("pizon", 540, 0, 0.42, "confundido", y=1660, entra="nada", acciones=[
            {"at": "@juego", "pose": "encoge"}, {"at": "@Constitucional", "mira": "izq"}, {"at": "@CGPJ", "mira": "der", "cara": "sorpresa"}]),
    ]),
    # 8 · PREGUNTA
    dict(id="final", fondo="colegio", animo="final", trans="iris", footnote="Pregunta a la audiencia", lines=[
        V("¿Juntos o por separado? Te leo.", "normal"),
        V("Y síguenos.", "energia", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@síguenos", "medio", "piz", 0.4, aire=220)],
       elements=[
        obj("papeleta", 540, 900, 0, 1.3, entra="nada", props={"color": "sepia", "texto": "SENADO"}, flota=True),
        quien("piz", 540, 0, 0.55, "pensativo", y=1640, entra="nada", acciones=[
            {"at": "@separado", "mira": "camara", "pose": "piensa"}, {"at": "@síguenos", "pose": "saluda", "cara": "riendo", "salta": True}]),
        rot("¿JUNTOS O SEPARADOS?", 540, 480, "@Juntos", 90, "amarillo", golpe=True, out="@síguenos-0.2", fx=[{"at": "@leo", "do": "latir"}]),
        rot("SÍGUENOS", 540, 480, "@síguenos", 110, "amarillo"),
    ]),
]

if __name__ == "__main__":
    episodio("guerra_senado", "La guerra del Senado", scenes,
             {"t": 2.0, "titulo": "La guerra del Senado", "capitulo": None},
             ["Infobae (17/10/2026): PSOE y Frente Amplio, «Senado de Progreso», en 47 circunscripciones; resultados de 2023",
              "El Español (18/10/2026): cómo se vota al Senado, decisión de Vox y tres quintos",
              "Vozpópuli: simulación de listas conjuntas PP-Vox con los votos de 2023",
              "Mapas dibujados sobre contornos de Natural Earth (dominio público)"],
             ("🏛️ Por primera vez, PSOE y Frente Amplio van juntos… pero solo al Senado\n"
              "🗳️ Cada provincia elige 4 senadores y tú marcas hasta 3: el primero suele llevarse 3\n"
              "📊 2023: PP 120 de 208 senadores elegidos; PSOE 72\n"
              "🤝 «Senado de Progreso» en 47 circunscripciones\n"
              "🔄 PP y Vox estudian su respuesta; con los votos de 2023 podrían quitar hasta 15 senadores (simulación)\n"
              "⚖️ En juego: los tres quintos para renovar el Constitucional y el CGPJ\n"
              "💬 ¿Juntos o por separado? Te leemos 👇\n"
              "🔔 Síguenos · 📚 Fuentes en comentarios"),
             "📚 Fuentes: Infobae 17/10/2026 · El Español 18/10/2026 · Vozpópuli (simulación). ¿Ves un error? Dínoslo.",
             ["#29N", "#Senado", "#elecciones", "#PSOE", "#PP", "#Vox", "#politica", "#pizarrapublica"],
             series_tag="EXPLICADO FÁCIL")
