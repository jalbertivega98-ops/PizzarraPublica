#!/usr/bin/env python3
"""«¿Por qué Marruecos reclama Ceuta y Melilla?» (16/10/2026). Segundo episodio de la saga de Ceuta (mundo dibujado).

Guion y fuentes: docs/series/cinco_mundo/guiones.md · investigación: /mnt/project-files/insta/investigacion/temas5_mundo.md
  Visita de los Reyes: Ceuta 13/10 y Melilla 14/10/2026, primera como Reyes; la anterior visita real, Juan Carlos I en
    noviembre de 2007, tras la que Rabat llamó a consultas a su embajador (AFP vía Emol 13/10, Ahram 14/10).
  Ceuta: Portugal 1415; monarquía hispánica 1580; se queda con España en 1640; Tratado de Lisboa 1668 (Euronews 11/09/2026).
  Melilla: 17/09/1497, Pedro de Estopiñán, enviado por el duque de Medina Sidonia. Dinastía alauí: desde 1666.
  Marruecos las reclama desde 1956; el 27/01/1975 lo llevó al Comité de Descolonización de la ONU y no prosperó; no
    están en la lista de territorios no autónomos (El Debate 06/08/2026, Maldita 31/07/2026).
  Estatutos de 1995 (LO 1/1995 y 2/1995). Únicos territorios de la UE en el continente africano (Exteriores 01/08/2026).
  Posturas: Gobierno (Robles: «españolísimas e intocables», Euronews 22/08); PP (Feijóo 13/10: critica que Sánchez no
    acompañara al Rey, Artículo 14); Vox (PNL autonómicas: romper relaciones si Marruecos no reconoce la soberanía, ESdiario 01/09).
Regla del proyecto: la entrada masiva de julio y sus víctimas no se usan.
"""
from _mundo import *  # noqa: F401,F403

R = "estrecho"
MAD = P(R, -3.7, 40.4)
CEUTA = P(R, -5.335, 35.895)
MELILLA = P(R, -2.94, 35.29)
LISBOA = P(R, -9.14, 38.72)
SANLUCAR = P(R, -6.35, 36.78)
RABAT = P(R, -6.84, 34.02)
ESTRECHO = P(R, -4.6, 36.2)
ORDEN = ["Spain", "Portugal", "Gibraltar", "Ceuta", "Morocco", "Melilla", "Balearic Islands", "France", "Andorra", "Algeria"]
FHIS = "Euronews 11/09/2026 · El Debate 02/08/2026 · Tratado de Lisboa (1668)"


def mapa_e(at=0.0, dibujo=1.5, acciones=(), **props):
    return mapa(R, at, dibujo, acciones, orden=ORDEN, **props)


def mar(lon, lat):
    return P(R, lon, lat)


scenes = [
    # 1 · GANCHO: la corona viaja de Madrid a Ceuta y Melilla; Marruecos al otro lado
    dict(id="gancho", fondo="mar_mapa", limites=LIM, animo="tension", footnote="AFP 13-14/10/2026 · Casa Real", lines=[
        V("Los Reyes acaban de visitar Ceuta y Melilla: la primera visita real desde 2007.", "energia"),
        V("Aquella vez, Marruecos llamó a consultas a su embajador. ¿Por qué tanto lío?", "remate", 0.15),
    ], camara=[zoom(0, P(R, -4.4, 38.2), 1.0, 0), zoom("@Ceuta", P(R, -4.6, 36.3), 2.4, 1.0),
               zoom("@Marruecos", P(R, -5.0, 35.2), 2.0, 0.7), zoom("@lío", P(R, -4.3, 35.8), 2.6, 0.6)],
       elements=[
        mapa_e(0, 1.3, acciones=[{"at": "@Ceuta", "props": {"resalta": ["Ceuta"]}, "sfx": "pop"},
                                 {"at": "@Melilla", "props": {"resalta": ["Ceuta", "Melilla"]}, "sfx": "pop"},
                                 {"at": "@Marruecos", "props": {"resalta": ["Ceuta", "Melilla", "Morocco"]}}]),
        obj("corona", MAD[0], MAD[1], "@Reyes", 0.3, id="corona", entra="crece", sfx="estrellitas", flota=True,
            acciones=[{"at": "@visitar", "x": CEUTA[0] + 6, "y": CEUTA[1] - 40, "dur": 1.2},
                      {"at": "@Melilla", "x": MELILLA[0], "y": MELILLA[1] - 40, "dur": 0.9}]),
        obj("bandera", RABAT[0], RABAT[1], "@Marruecos-0.2", 0.35, props={"diseno": "marruecos"}, entra="crece", sfx="papel"),
        quien("piz", MELILLA[0] + 70, "@2007", 0.2, "normal", y=MELILLA[1] + 30, entra="cae", acciones=[
            {"at": "@embajador", "cara": "sorpresa", "take": True, "mira": "izq"},
            {"at": "@lío", "pose": "encoge", "cara": "confundido", "mira": "camara"}]),
        rot("PRIMERA DESDE 2007", 540, 430, "@2007", 84, "amarillo", golpe=True, out="@Aquella"),
        rot("2007: MARRUECOS RETIRA", 540, 430, "@consultas", 70, "blanco", golpe=True, out="@lío"),
        rot("A SU EMBAJADOR", 540, 520, "@embajador", 70, "blanco", golpe=True, out="@lío"),
        rot("¿POR QUÉ?", 540, 450, "@lío", 130, "amarillo", golpe=True, rot=-4),
    ]),
    # 2 · 1415-1668: la carabela portuguesa sale de Lisboa hacia Ceuta; el tratado
    dict(id="ceuta", fondo="mar_mapa", limites=LIM, animo="aventura", trans="zoom", footnote=FHIS, lines=[
        V("Empecemos en 1415: Portugal conquista Ceuta.", "normal"),
        V("En 1580 pasa a la corona española, y cuando Portugal se separa, en 1640, Ceuta se queda con España.", "normal", 0.1),
        V("El Tratado de Lisboa lo firma en 1668.", "remate", 0.1),
    ], camara=[zoom(0, P(R, -7.5, 37.4), 1.6, 0), zoom("@conquista", CEUTA, 3.6, 1.0), zoom("@1580", P(R, -5.5, 38.5), 1.2, 0.8),
               zoom("@Tratado", P(R, -5.5, 37.5), 1.3, 0.6)],
       elements=[
        mapa_e(0, 0.01, progreso=1.0, acciones=[
            {"at": "@Portugal", "props": {"resalta": ["Portugal"]}},
            {"at": "@conquista", "props": {"resalta": ["Portugal", "Ceuta"]}, "sfx": "golpe"},
            {"at": "@1580", "props": {"resalta": ["Spain", "Portugal", "Ceuta"]}},
            {"at": "@separa", "props": {"resalta": ["Spain", "Ceuta"]}}]),
        obj("carabela", LISBOA[0] - 60, LISBOA[1] + 30, 0.1, 0.3, id="nave", entra="pop", props={"cruz": "portugal"},
            acciones=[{"at": 0.4, "x": mar(-9.4, 36.6)[0], "y": mar(-9.4, 36.6)[1], "dur": 1.0},
                      {"at": "@Ceuta", "x": CEUTA[0] - 40, "y": CEUTA[1] - 4, "dur": 1.0}]),
        obj("chincheta", CEUTA[0] + 4, CEUTA[1], "@conquista", 0.24, props={"diseno": "portugal"}, entra="cae", out="@1580"),
        obj("chincheta", CEUTA[0] + 4, CEUTA[1], "@1580", 0.24, props={"diseno": "espana"}, entra="cae"),
        quien("piz", P(R, -5.6, 36.1)[0], 0.2, 0.06, "ilusionado", y=P(R, -5.6, 36.1)[1], entra="cae", acciones=[
            {"at": "@conquista", "cara": "sorpresa", "take": True}, {"at": "@separa", "pose": "senala", "cara": "riendo"}]),
        rot("1415 · PORTUGAL", 540, 430, "@1415", 84, "blanco", golpe=True, out="@1580"),
        rot("1580 · CORONA ESPAÑOLA", 540, 430, "@1580", 72, "amarillo", golpe=True, out="@1640"),
        rot("1640 · SE QUEDA CON ESPAÑA", 540, 430, "@1640", 64, "amarillo", golpe=True, out="@Tratado"),
        obj("pergamino", 540, 1180, "@Tratado", 0.75, hud=True, entra="abajo", sfx="papel",
            props={"titulo": "TRATADO DE LISBOA", "fecha": "1668"}),
    ]),
    # 3 · MELILLA 1497: la nave castellana sale de Sanlúcar; la dinastía alauí llega después
    dict(id="melilla", fondo="mar_mapa", limites=LIM, animo="aventura", trans="corte",
         footnote="Melilla: 17/09/1497, Pedro de Estopiñán (duque de Medina Sidonia) · Dinastía alauí: 1666", lines=[
        V("Melilla es española desde 1497.", "normal"),
        V("La dinastía que hoy reina en Marruecos llegó casi dos siglos después, en 1666.", "remate", 0.15),
    ], camara=[zoom(0, P(R, -4.6, 36.2), 2.0, 0), zoom("@1497", MELILLA, 3.6, 1.0), zoom("@dinastía", P(R, -5.0, 34.8), 1.6, 0.8)],
       elements=[
        mapa_e(0, 0.01, progreso=1.0, resalta=["Ceuta"], acciones=[
            {"at": "@1497", "props": {"resalta": ["Ceuta", "Melilla"]}, "sfx": "golpe"},
            {"at": "@dinastía", "props": {"resalta": ["Ceuta", "Melilla", "Morocco"]}}]),
        obj("carabela", SANLUCAR[0], SANLUCAR[1] + 20, 0, 0.26, entra="pop", props={"cruz": "castilla"},
            acciones=[{"at": 0.2, "x": mar(-4.0, 36.1)[0], "y": mar(-4.0, 36.1)[1], "dur": 1.2},
                      {"at": "@1497-0.3", "x": MELILLA[0] - 40, "y": MELILLA[1] - 10, "dur": 0.8}]),
        obj("chincheta", MELILLA[0] + 4, MELILLA[1], "@1497", 0.2, props={"diseno": "espana"}, entra="cae"),
        obj("corona", RABAT[0], RABAT[1] - 30, "@1666", 0.16, entra="crece", sfx="estrellitas"),
        quien("piz", P(R, -3.6, 35.0)[0], "@dinastía", 0.11, "pensativo", y=P(R, -3.6, 35.0)[1], entra="cae", acciones=[
            {"at": "@después", "pose": "senala_izq", "cara": "sorpresa"}]),
        rot("1497 · MELILLA", 540, 430, "@1497", 90, "amarillo", golpe=True, out="@dinastía"),
        rot("1666 · DINASTÍA ALAUÍ", 540, 430, "@1666", 76, "blanco", golpe=True),
    ]),
    # 4 · LA RECLAMACIÓN: la bandera de Marruecos, la carta a la ONU y la lista donde no aparecen
    dict(id="onu", fondo={"tipo": "plano", "color": (0, 110, 170)}, animo="curioso", trans="papel",
         footnote="ONU, Comité de Descolonización, 27/01/1975 · El Debate 06/08/2026 · Maldita 31/07/2026", lines=[
        V("Marruecos las reclama desde su independencia, en 1956.", "normal"),
        V("En 1975 lo llevó a la ONU, pero no prosperó: no están en su lista de territorios por descolonizar.", "normal", 0.15),
    ], camara=[plano(0, "general", [540, 900], 0), plano("@ONU", "general", [540, 820], 0.5, zoom=1.08),
               plano("@lista", "general", [540, 900], 0.6)],
       elements=[
        obj("bandera", 260, 1300, 0, 0.9, props={"diseno": "marruecos"}, entra="crece", sfx="papel"),
        obj("bandera", 820, 1300, "@ONU", 0.9, props={"diseno": "onu"}, entra="crece", sfx="papel"),
        obj("documento", 540, 860, "@prosperó", 1.25, entra="nada", dibujo=0.9, sfx="papel", props={
            "titulo": "TERRITORIOS NO AUTÓNOMOS", "subtitulo": "Lista de la ONU",
            "articulos": [{"id": "l", "titulo": "EN EUROPA", "lineas": ["Gibraltar"]},
                          {"id": "n", "titulo": "¿CEUTA? ¿MELILLA?", "lineas": ["No figuran"]}]},
            acciones=[{"at": "@lista", "props": {"resalta": ["n"]}}]),
        quien("piz", 1250, "@prosperó-0.4", 0.45, "pensativo", y=1560, entra="nada", objeto="lupa", pose="sostiene", acciones=[
            {"at": "@prosperó-0.4", "x": 880, "dur": 0.5}, {"at": "@lista", "cara": "sorpresa", "take": True},
            {"at": "@descolonizar", "objeto": None, "pose": "encoge", "cara": "esceptica"}]),
        rot("1956 · INDEPENDENCIA", 540, 430, "@1956", 76, "blanco", golpe=True, out="@1975"),
        rot("1975 · A LA ONU", 540, 430, "@1975", 84, "amarillo", golpe=True, out="@prosperó"),
        sello("NO PROSPERÓ", "rojo", 450, "@prosperó"),
    ]),
    # 5 · HOY: ciudades autónomas, Unión Europea en África
    dict(id="hoy", fondo="ceuta", animo="alegre", trans="zoom", footnote="LO 1/1995 y 2/1995 · Exteriores 01/08/2026", lines=[
        V("Desde 1995 son ciudades autónomas, y el único trozo de la Unión Europea en el continente africano.", "normal"),
    ], camara=[plano(0, "abierto", [400, 1000], 0), plano("@Unión", "medio", "piz", 0.6, aire=140),
               plano("@africano", "general", [540, 900], 0.5)],
       elements=[
        quien("piz", -100, 0, 0.6, "ilusionado", entra="nada", acciones=[
            {"at": 0, "x": 420, "dur": 1.4}, {"at": "@autónomas", "pose": "senala_arriba", "cara": "riendo"},
            {"at": "@Unión", "salta": True}, {"at": "@africano", "pose": "pulgar"}]),
        obj("bandera", 800, 1340, "@Unión", 0.7, props={"diseno": "ue"}, entra="crece", sfx="papel"),
        rot("1995 · CIUDADES AUTÓNOMAS", 540, 430, "@1995", 64, "blanco", golpe=True),
        rot("UE EN ÁFRICA", 540, 540, "@Unión", 96, "amarillo", golpe=True),
    ]),
    # 6 · LAS POSTURAS: tres atriles
    dict(id="posturas", fondo="calle", animo="curioso", trans="iris",
         footnote="Robles (Euronews 22/08/2026) · Feijóo (13/10/2026) · Vox (ESdiario 01/09/2026)", lines=[
        V("El Gobierno del PSOE no negocia: Robles las llama «españolísimas e intocables».", "normal"),
        V("El PP critica que Sánchez no acompañara al Rey.", "normal", 0.1),
        V("Y Vox pide romper relaciones si Marruecos no reconoce que son españolas.", "normal", 0.1),
    ], camara=[plano(0, "general", dur=0), plano("@PSOE", "medio", "p1", 0.5), plano("@PP", "medio", "p2", 0.5),
               plano("@Vox", "medio", "p3", 0.5), plano("@españolas", "general", dur=0.6)],
       elements=[
        quien("diputado", 230, 0, 0.55, "normal", id="p1", entra="pop", acciones=[
            {"at": "@negocia", "pose": "cruzados", "cara": "serio"}, {"at": "@intocables", "pose": "puno", "cara": "riendo"}]),
        quien("diputado", 540, 0.15, 0.55, "normal", id="p2", entra="pop", acciones=[{"at": "@acompañara", "pose": "senala_izq", "cara": "esceptica"}]),
        quien("diputado", 850, 0.3, 0.55, "normal", id="p3", entra="pop", acciones=[{"at": "@romper", "pose": "puno", "cara": "enfado"}]),
        *atriles(),
        rot("PSOE: «INTOCABLES»", 540, 450, "@intocables", 70, "blanco", golpe=True, out="@PP"),
        rot("PP: «NO LE HUBIERA DEJADO SOLO»", 540, 450, "@Rey", 54, "blanco", golpe=True, out="@Vox"),
        rot("VOX: ROMPER RELACIONES", 540, 450, "@romper", 66, "blanco", golpe=True),
    ]),
    # 7 · FINAL: zoom out del Estrecho con Ceuta y Melilla iluminadas
    dict(id="final", fondo="mar_mapa", limites=LIM, animo="final", trans="zoom", footnote="Te leemos en comentarios", lines=[
        V("¿Crees que Marruecos dejará de reclamarlas algún día? Te leo.", "normal"),
        V("Y síguenos para el próximo viaje de Piz.", "energia", 0.15),
    ], camara=[zoom(0, P(R, -4.2, 35.6), 3.2, 0), zoom(0.2, P(R, -3.6, 38.2), 1.0, 2.2)],
       elements=[
        mapa_e(0, 0.01, progreso=1.0, resalta=["Ceuta", "Melilla"]),
        quien("piz", 790, "@Crees", 0.6, "pensativo", y=1500, hud=True, entra="abajo", acciones=[
            {"at": "@Marruecos", "pose": "senala_izq"}, {"at": "@leo", "mira": "camara", "cara": "ilusionado"},
            {"at": "@síguenos", "pose": "saluda", "cara": "riendo"}, {"at": "@viaje", "salta": True}]),
        rot("¿ALGÚN DÍA?", 540, 450, "@algún", 120, "amarillo", golpe=True, out="@síguenos-0.3"),
        rot("SÍGUENOS", 540, 450, "@síguenos", 110, "amarillo", fx=[{"at": "@Piz", "do": "latir"}]),
    ]),
]

if __name__ == "__main__":
    episodio("ceuta_marruecos", "¿Por qué Marruecos reclama Ceuta y Melilla?", scenes,
             {"t": 2.6, "titulo": "¿Por qué Marruecos reclama Ceuta y Melilla?", "capitulo": None},
             ["Visita de los Reyes a Ceuta (13/10) y Melilla (14/10/2026): AFP vía Emol y Ahram Online",
              "Historia de Ceuta y Melilla: Euronews (11/09/2026), El Debate (02/08/2026)",
              "Comité de Descolonización de la ONU, 27/01/1975: El Debate (06/08/2026), Maldita (31/07/2026)",
              "Estatutos de Autonomía: LO 1/1995 y LO 2/1995 (BOE)",
              "Exteriores Explica (01/08/2026): Ceuta y Melilla en la UE",
              "Posturas: Euronews 22/08/2026 (Robles), Artículo 14 13/10/2026 (Feijóo), ESdiario 01/09/2026 (Vox)",
              "Mapas dibujados sobre contornos de Natural Earth (dominio público)"],
             ("👑 Los Reyes visitan Ceuta y Melilla: la primera visita real desde 2007\n"
              "⛵ Ceuta: portuguesa en 1415, con España desde 1580/1640; Tratado de Lisboa, 1668\n"
              "🏰 Melilla: española desde 1497, antes que la dinastía alauí (1666)\n"
              "🇺🇳 Marruecos las reclama desde 1956; en la ONU (1975) no prosperó\n"
              "🇪🇺 Hoy: ciudades autónomas y la UE en el continente africano\n"
              "💬 ¿Dejará Marruecos de reclamarlas algún día?\n"
              "🔔 Síguenos · 📚 Fuentes en comentarios"),
             "📚 Fuentes: AFP 13-14/10/2026 · Euronews 11/09 y 22/08 · El Debate 02/08 y 06/08 · Maldita 31/07 · "
             "Exteriores 01/08 · BOE (LO 1/1995 y 2/1995) · Artículo 14 13/10 · ESdiario 01/09. ¿Ves un error? Dínoslo.",
             ["#Ceuta", "#Melilla", "#Marruecos", "#historia", "#Reyes", "#politica", "#España", "#pizarrapublica"],
             series_tag="EXPLICADO FÁCIL")
