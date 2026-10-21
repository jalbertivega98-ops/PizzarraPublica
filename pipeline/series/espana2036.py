#!/usr/bin/env python3
"""«España en 2036, si seguimos así» (21/10/2026). Mundo dibujado: Piz viaja diez años al futuro.

Fuentes:
  Fotocasa / InfoJobs (Euronews 10/06/2026): comprar un piso de segunda mano de 80 m² exige 8,4 años de sueldo bruto
    íntegro en 2025, frente a 7,1 en 2024.
  Funcas (29/12/2025, datos del Ministerio de Transportes): la vivienda subió un 12,1 % interanual en el tercer
    trimestre de 2025, la mayor subida en 20 años.
  INE, Proyecciones de población 2026-2076 (17/06/2026), escenario central para 2036: 53,1 millones de habitantes,
    369.900 nacimientos y 510.400 defunciones (saldo vegetativo -140.500), 38,3 millones nacidos en España,
    saldo migratorio +319.300.
  Cálculos propios (marcados en pantalla con el sello CÁLCULO):
    vivienda 2036 = 8,4 + 10 × 1,3 (lo que subió de 2024 a 2025) ≈ 21 años → «más de 20»;
    nacidos fuera = (53,1 - 38,3) / 53,1 ≈ 28 % → «más de 1 de cada 4».
"""
from _mundo import *  # noqa: F401,F403

R = "espana"
MAD = P(R, -3.7, 40.4)
FVIV = "Fotocasa/InfoJobs (Euronews 10/06/2026) · Cálculo: +1,3 años de sueldo cada año, como de 2024 a 2025"
FINE = "INE, Proyecciones de población 2026-2076 (17/06/2026), escenario central"
SUELO = 1340


def edif(tipo, x, at, scale=1.0, acciones=(), **kw):
    return dict(type="edificio", edificio=tipo, x=x, y=SUELO, scale=scale, at=at, acciones=list(acciones), **kw)


scenes = [
    # 1 · GANCHO: el marcador de años corre hasta 2036
    dict(id="gancho", fondo={"tipo": "rayos", "color": "amarillo", "color2": (120, 200, 255)}, animo="tension",
         footnote="Proyecciones oficiales y cálculos con datos de hoy", lines=[
        V("Viajamos diez años al futuro: España, 2036.", "energia"),
        V("¿Cómo será tu vida si todo sigue como hoy?", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 900], 0), plano("@España", "general", [540, 700], 0.5, zoom=1.1),
               plano("@vida", "general", [540, 1000], 0.6)],
       elements=[
        obj("contador", 540, 600, 0, 1.0, hud=True, entra="pop", sfx="kaching", dibujo=1.6,
            props={"valor": 2036, "miles": "", "desde": 2026, "prefijo": "AÑO ", "ancho": 760}),
        rot("¿Y SI SEGUIMOS ASÍ?", 540, 860, "@vida", 92, "rojo", golpe=True),
        quien("piz", 540, 0, 0.62, "ilusionado", y=1600, entra="nada", acciones=[
            {"at": 0.3, "salta": True, "cara": "sorpresa"}, {"at": "@futuro", "pose": "senala_arriba", "mira": "arriba"},
            {"at": "@España", "salta": True, "cara": "riendo"}, {"at": "@2036", "tiembla": True},
            {"at": "@Cómo", "pose": "piensa", "cara": "pensativo"}, {"at": "@vida", "mira": "camara", "pose": "senala"},
            {"at": "@hoy", "pose": "encoge", "cara": "confundido"}]),
        sello("PROYECCIÓN", "naranja", 1180, "@sigue"),
    ]),
    # 2 · VIVIENDA: años de sueldo para comprar un piso
    dict(id="vivienda", fondo="calle", animo="tension", trans="barrido", footnote=FVIV, lines=[
        V("Hoy, comprar un piso cuesta 8,4 años de sueldo íntegro. Hace un año, 7,1.", "normal"),
        V("A ese ritmo, en 2036 harían falta más de veinte años de sueldo.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@8,4", "general", [540, 800], 0.5, zoom=1.06),
               plano("@ritmo", "general", [540, 900], 0.5), plano("@veinte", "general", [700, 1000], 0.5, zoom=1.12)],
       elements=[
        edif("casa", 790, 0, 0.9, entra="crece"),
        obj("contador", 540, 520, "@piso", 0.85, hud=True, entra="pop", sfx="kaching", dibujo=1.2, out="@ritmo",
            props={"valor": 8.4, "decimales": 1, "sufijo": " AÑOS", "ancho": 620}),
        etq("2025: 7,1 AÑOS", 540, 700, "@Hace", "azul", 0.85, hud=True, out="@ritmo"),
        rot("MÁS DE 20 AÑOS", 540, 520, "@veinte", 104, "rojo", golpe=True),
        sello("CÁLCULO", "naranja", 720, "@harían"),
        quien("piz", 300, 0, 0.55, "ilusionado", entra="nada", acciones=[
            {"at": "@comprar", "pose": "senala", "mira": "der"}, {"at": "@cuesta", "cara": "sorpresa", "take": True},
            {"at": "@íntegro", "pose": "piensa", "cara": "preocupado"}, {"at": "@Hace", "mira": "arriba"},
            {"at": "@ritmo", "x": 420, "dur": 0.6}, {"at": "@2036", "cara": "preocupado", "mira": "der"},
            {"at": "@veinte", "cara": "susto", "salta": True}, {"at": "@sueldo#2", "tiembla": True}]),
    ]),
    # 3 · POBLACIÓN: el mapa de España se llena hasta 53,1 millones
    dict(id="poblacion", fondo="mar_mapa", limites=LIM, animo="curioso", trans="papel", footnote=FINE, lines=[
        V("Según el INE, en 2036 seremos 53 millones de personas.", "normal"),
    ], camara=[zoom(0, MAD, 1.0, 0), zoom("@INE", P(R, -3.5, 40.0), 1.15, 0.8), zoom("@millones", MAD, 1.0, 0.6)],
       elements=[
        mapa(R, 0, 1.4, colores={"espana": (240, 236, 226)}, acciones=[
            {"at": "@seremos", "props": {"colores": {"espana": (250, 214, 140)}}, "sfx": "pop"}]),
        rot("53,1 MILLONES", 540, 400, "@53", 104, "amarillo", golpe=True),
        sello("PROYECCIÓN", "naranja", 560, "@personas"),
        quien("profe", 830, 0.2, 0.55, "normal", y=1580, hud=True, entra="der", acciones=[
            {"at": "@INE", "pose": "senala_izq"}, {"at": "@2036", "mira": "camara", "cara": "idea"},
            {"at": "@53", "salta": True}, {"at": "@personas", "pose": "pulgar"}]),
    ]),
    # 4 · NACEN Y MUEREN: barras que no cuadran
    dict(id="nacen", fondo={"tipo": "plano", "color": (246, 236, 214)}, animo="tension", trans="corte", footnote=FINE, lines=[
        V("Pero ese año nacerán unos 370.000 bebés… y morirán 510.000 personas.", "normal"),
        V("Cada año, 140.000 menos.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 900], 0), plano("@morirán", "general", [540, 950], 0.6, zoom=1.05),
               plano("@140.000", "general", [540, 800], 0.4, zoom=1.1)],
       elements=[
        obj("barras", 540, 960, "@nacerán-0.2", 1.1, hud=True, entra="nada", dibujo=2.6,
            props={"sufijo": ".000", "decimales": 0, "tope": 600, "barras": [
                {"texto": "NACEN", "valor": 370, "color": "verde"}, {"texto": "MUEREN", "valor": 510, "color": "rojo"}]}),
        rot("−140.000 AL AÑO", 540, 420, "@140.000", 100, "rojo", golpe=True),
        quien("pizon", 880, 0, 0.45, "confundido", y=1640, entra="nada", acciones=[
            {"at": "@nacerán", "mira": "arriba", "cara": "ilusionado"}, {"at": "@bebés", "salta": True},
            {"at": "@morirán", "cara": "preocupado", "pose": "piensa"}, {"at": "@510.000", "take": True, "cara": "susto"},
            {"at": "@Cada", "mira": "camara"}, {"at": "@menos", "pose": "encoge", "tiembla": True}]),
    ]),
    # 5 · LOS QUE LLEGAN: gente con maletas entra en escena
    dict(id="llegan", fondo="calle", animo="curioso", trans="iris",
         footnote="INE 2026-2076: 38,3 M nacidos en España de 53,1 M en 2036 (cálculo: ~28 % nacidos fuera)", lines=[
        V("Entonces, ¿por qué crecemos? Por la gente que llega de fuera.", "normal"),
        V("En 2036, más de uno de cada cuatro habitantes habrá nacido en otro país.", "normal", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@llega", "general", [700, 1050], 0.6),
               plano("@cuatro", "general", [540, 900], 0.5, zoom=1.06)],
       elements=[
        quien("piz", 260, 0, 0.55, "pensativo", entra="nada", acciones=[
            {"at": "@Entonces", "pose": "piensa"}, {"at": "@crecemos", "mira": "camara", "cara": "confundido"},
            {"at": "@llega", "mira": "der", "cara": "sorpresa"}, {"at": "@fuera", "pose": "saluda", "cara": "ilusionado"},
            {"at": "@cuatro", "pose": "senala_arriba", "mira": "arriba"}, {"at": "@nacido", "salta": True}, {"at": "@país", "cara": "idea"}]),
        *[quien(q, 1300, "@llega-0.3", 0.45, "ilusionado", entra="nada", objeto="maleta", pose="sostiene", acciones=[
            {"at": "@llega", "x": x, "dur": 0.9}, {"at": "@habitantes", "mira": "camara"}, {"at": "@país", "salta": True}])
          for q, x in (("critica", 560), ("sarcastica", 740), ("indignada", 920))],
        rot("MÁS DE 1 DE CADA 4", 540, 520, "@cuatro", 96, "amarillo", golpe=True),
        sello("CÁLCULO", "naranja", 700, "@habitantes"),
    ]),
    # 6 · FINAL: nada está escrito
    dict(id="final", fondo={"tipo": "rayos", "color": "amarillo"}, animo="final", trans="zoom", footnote="Pregunta a la audiencia", lines=[
        V("Nada de esto está escrito: depende de lo que hagamos… y de lo que votemos el 29N.", "normal"),
        V("¿Qué te preocupa más de 2036? Te leo. Y síguenos.", "energia", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@votemos", "general", [540, 900], 0.5, zoom=1.08),
               plano("@síguenos", "general", [540, 1000], 0.5)],
       elements=[
        obj("urna", 780, 1300, "@votemos-0.3", 0.6, entra="cae", sfx="golpe"),
        rot("29N", 780, 820, "@29N", 120, "rojo", golpe=True, out="@preocupa"),
        rot("¿QUÉ TE PREOCUPA MÁS?", 540, 520, "@preocupa", 86, "rojo", golpe=True, out="@síguenos-0.3"),
        rot("SÍGUENOS", 540, 520, "@síguenos", 110, "rojo"),
        quien("piz", 330, 0, 0.6, "serio", entra="nada", acciones=[
            {"at": "@escrito", "pose": "piensa", "mira": "camara"}, {"at": "@hagamos", "pose": "senala"},
            {"at": "@votemos", "mira": "der", "pose": "senala"}, {"at": "@29N", "salta": True, "cara": "ilusionado"},
            {"at": "@preocupa", "pose": "piensa", "cara": "pensativo"}, {"at": "@leo", "cara": "riendo"},
            {"at": "@síguenos", "pose": "saluda", "salta": True}]),
    ]),
]

if __name__ == "__main__":
    episodio("espana2036", "España en 2036, si seguimos así", scenes,
             {"t": 13.8, "titulo": "España en 2036, si seguimos así", "capitulo": None},
             ["Fotocasa / InfoJobs (Euronews, 10/06/2026): 8,4 años de sueldo bruto para un piso de 80 m² en 2025; 7,1 en 2024",
              "Funcas (29/12/2025): la vivienda subió un 12,1 % en el tercer trimestre de 2025, la mayor subida en 20 años",
              "INE, Proyecciones de población 2026-2076 (17/06/2026): 53,1 millones en 2036; 369.900 nacimientos y 510.400 defunciones",
              "INE: 38,3 millones nacidos en España en 2036 (cálculo propio: ~28 % nacidos fuera)",
              "Cálculo propio: 8,4 + 10 × 1,3 ≈ 21 años de sueldo en 2036 si se mantiene el ritmo de 2024-2025"],
             ("🔮 Viajamos a 2036: así sería España si todo sigue como hoy\n"
              "🏠 Hoy un piso cuesta 8,4 años de sueldo íntegro; a este ritmo, en 2036 serían más de 20 (cálculo)\n"
              "👥 Seremos 53,1 millones, según el INE\n"
              "📉 Pero morirán 140.000 personas más de las que nacen cada año\n"
              "🧳 Crecemos por la gente que llega: más de 1 de cada 4 habrá nacido fuera\n"
              "🗳️ Nada está escrito: depende de lo que votemos el 29N\n"
              "💬 ¿Qué te preocupa más de 2036? Te leo 👇\n"
              "🔔 Síguenos · 📚 Fuentes en comentarios"),
             "📚 Fuentes: INE, Proyecciones de población 2026-2076 (17/06/2026) · Fotocasa/InfoJobs (Euronews 10/06/2026) · "
             "Funcas 29/12/2025. Las cifras de vivienda 2036 y nacidos fuera son cálculos propios con esos datos. ¿Ves un error? Dínoslo.",
             ["#España2036", "#29N", "#elecciones", "#vivienda", "#INE", "#demografía", "#pizarrapublica"],
             series_tag="EXPLICADO FÁCIL")
