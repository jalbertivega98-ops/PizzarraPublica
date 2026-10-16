#!/usr/bin/env python3
"""«El 29N lo pagas tú» (16/10/2026). Mundo dibujado: el viaje de una papeleta por el mapa de España.

Guion y fuentes: docs/series/cinco_mundo/guiones.md · investigación: /mnt/project-files/insta/investigacion/temas5_mundo.md
  Coste: «más de 270 M€» (estimación de Euronews, 08/10/2026, basada en 2023). 2023: 220,8 M€ de organización
    (Correos más de 100 M€, Administración unos 80, miembros de mesa algo más de 22, recuento/web/app algo más de 13) y
    unos 58 M€ de subvenciones (Tribunal de Cuentas), citados por Euronews.
  Censo del 29N: 38.728.356 electores (INE, 09/10/2026), 2.769.645 en el extranjero.
  Dieta de mesa: 75 € (antes 70 €), Orden INT/650/2026, BOE 27/06/2026.
  Subvenciones: 21.167,64 € por escaño y 0,81 € por voto al Congreso (Orden HAC/1062/2026; RTVC 08/10/2026).
  Coste por elector: unos 7 € (cálculo propio: 270 M€ / 38,7 millones).
"""
from _mundo import *  # noqa: F401,F403

R = "espana"
MAD = P(R, -3.7, 40.4)
PROV = ["Madrid", "Barcelona", "Valencia", "Sevilla", "La Coruña", "Bizkaia", "Málaga", "Zaragoza", "Murcia", "Baleares",
        "Las Palmas", "Santa Cruz de Tenerife", "Asturias", "Badajoz", "Cáceres", "León", "Granada", "Toledo"]
TODAS = PROV + ["Alicante", "Cádiz", "Pontevedra", "Lugo", "Orense", "Cantabria", "Gipuzkoa", "Álava", "Navarra", "La Rioja",
                "Burgos", "Palencia", "Valladolid", "Zamora", "Salamanca", "Ávila", "Segovia", "Soria", "Guadalajara", "Cuenca",
                "Ciudad Real", "Albacete", "Jaén", "Córdoba", "Huelva", "Almería", "Teruel", "Huesca", "Lérida", "Gerona",
                "Tarragona", "Castellón", "Ceuta", "Melilla"]
FEURO = "Euronews 08/10/2026 (estimación basada en 2023) · Interior · Tribunal de Cuentas"
CAMINO = [(-3.7, 40.4), (-0.4, 39.5), (2.1, 41.4), (-0.9, 41.6), (-2.9, 43.2), (-8.4, 43.3), (-5.6, 42.6), (-6.0, 37.4), (-4.4, 36.7)]


def p_(lon, lat):
    return P(R, lon, lat)


scenes = [
    # 1 · GANCHO: Piz vota en el colegio… y se le cae encima el contador de lo que cuesta
    dict(id="gancho", fondo="colegio", animo="tension", footnote=FEURO, lines=[
        V("Meter este sobre en la urna parece gratis…", "energia"),
        V("pero las elecciones del 29N costarán más de 270 millones de euros.", "remate", 0.15),
    ], camara=[plano(0, "medio", "piz", 0, aire=220), plano("@urna", "medio", "urna", 0.5, aire=180),
               plano("@costarán", "general", [540, 900], 0.5), plano("@euros", "general", [540, 880], 0.4, zoom=1.06)],
       elements=[
        obj("mesa_electoral", 760, 1340, 0, 0.75, props={"texto": "MESA 1"}, entra="nada"),
        obj("urna", 760, 1020, 0, 0.55, id="urna", entra="nada", props={"llena": 0.35, "texto": "CONGRESO"}),
        quien("piz", 300, 0, 0.62, "ilusionado", entra="nada", objeto="papeleta", pose="sostiene", acciones=[
            {"at": "@sobre", "x": 520, "dur": 0.8}, {"at": "@urna", "pose": "senala", "objeto": None, "cara": "riendo"},
            {"at": "@costarán", "cara": "susto", "take": True, "mira": "arriba"}, {"at": "@euros", "tropieza": True}]),
        obj("contador", 540, 520, "@costarán", 1.0, hud=True, entra="cae", sfx="golpe", dibujo=1.6,
            props={"valor": 270, "prefijo": "+", "sufijo": " M€", "ancho": 760}),
        sello("ESTIMACIÓN", "naranja", 700, "@euros"),
    ]),
    # 2 · EL VIAJE: el camión de las elecciones recorre el mapa y las provincias se encienden
    dict(id="viaje", fondo="mar_mapa", limites=LIM, animo="aventura", trans="zoom",
         footnote="INE 09/10/2026: 38.728.356 electores · Euronews: Correos, más de 100 M€ en 2023", lines=[
        V("Hay que llevar papeletas a 38,7 millones de electores, en 52 provincias y en el extranjero.", "normal"),
        V("Solo Correos se llevó más de 100 millones en 2023.", "normal", 0.15),
    ], camara=[zoom(0, MAD, 1.0, 0), zoom("@electores", p_(-4, 40.0), 1.5, 1.0), zoom("@extranjero", p_(-6, 38), 0.8, 0.8),
               zoom("@Correos", p_(-3.6, 39.6), 1.3, 0.7)],
       elements=[
        mapa(R, 0, 1.5, orden=["Madrid"], acciones=[
            {"at": "@electores", "props": {"resalta": PROV[:6]}, "sfx": "pop"},
            {"at": "@52", "props": {"resalta": PROV}, "sfx": "pop"},
            {"at": "@provincias", "props": {"resalta": TODAS}, "sfx": "kaching"},
            {"at": "@extranjero", "props": {"lineas": [linea("fuera", [(-9.0, 38.5), (-13.5, 39.0), (-18.0, 39.5)], "azul", 0.8, discontinua=True)]}}]),
        obj("camion", MAD[0], MAD[1] + 10, 0.3, 0.16, id="camion", entra="pop", sfx="bocina", props={"texto": "ELECCIONES"},
            acciones=[{"at": 0.5 + i * 0.55, "x": p_(*q)[0], "y": p_(*q)[1] + 10, "dur": 0.5} for i, q in enumerate(CAMINO[1:])]),
        quien("piz", p_(-1.5, 38.6)[0], 0.4, 0.17, "ilusionado", y=p_(-1.5, 38.6)[1], entra="cae", acciones=[
            {"at": "@electores", "salta": True, "cara": "riendo"}, {"at": "@Correos", "cara": "sorpresa", "take": True}]),
        rot("38,7 MILLONES", 540, 430, "@38,7", 100, "amarillo", golpe=True, out="@Correos"),
        rot("CORREOS: +100 M€", 540, 430, "@Correos", 96, "amarillo", golpe=True),
        rot("(2023)", 540, 530, "@2023", 64, "blanco"),
    ]),
    # 3 · LA FACTURA DE 2023: barras de lo que costó cada cosa
    dict(id="factura", fondo={"tipo": "plano", "color": (28, 52, 110)}, animo="curioso", trans="papel",
         footnote="Elecciones de 2023 · Euronews 08/10/2026, con datos de Interior", lines=[
        V("En 2023, organizarlas costó 220,8 millones: Correos, la Administración, las mesas y el recuento.", "normal"),
    ], camara=[plano(0, "general", [540, 860], 0), plano("@Correos", "general", [540, 900], 0.6, zoom=1.08),
               plano("@recuento", "general", [540, 860], 0.5)],
       elements=[
        obj("contador", 540, 480, 0, 0.8, hud=True, entra="pop", sfx="kaching", dibujo=1.2, props={"valor": 220.8, "decimales": 1, "sufijo": " M€", "ancho": 760}),
        obj("barras", 540, 980, "@Correos-0.2", 1.05, entra="nada", dibujo=2.2, props={"sufijo": " M€", "decimales": 0, "barras": [
            {"texto": "CORREOS", "valor": 100, "color": "amarillo"}, {"texto": "ESTADO", "valor": 80, "color": "azul"},
            {"texto": "MESAS", "valor": 22, "color": "verde"}, {"texto": "RECUENTO", "valor": 13, "color": "naranja"}]},
            acciones=[{"at": "@Correos", "props": {"resalta": [0]}}]),
        quien("piz", 1250, "@mesas-0.6", 0.42, "pensativo", y=1640, entra="nada", acciones=[
            {"at": "@mesas-0.6", "x": 900, "dur": 0.5}, {"at": "@mesas", "pose": "senala_izq", "mira": "izq"},
            {"at": "@recuento", "cara": "sorpresa", "pose": "cabeza"}]),
    ]),
    # 4 · LA MESA: Piz, vocal; le pagan 75 € (cinco más que antes)
    dict(id="mesa", fondo="colegio", animo="comico", trans="iris", footnote="Orden INT/650/2026 (BOE 27/06/2026)", lines=[
        V("A cada miembro de mesa le pagan 75 euros por ese día. Desde junio, cinco más que antes.", "normal"),
        V("Ya no hay excusa para poner mala cara.", "remate", 0.2),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@75", "medio", "piz", 0.5, aire=200),
               plano("@cinco", "medio", [540, 1000], 0.5), plano("@excusa", "general", [540, 1000], 0.5)],
       elements=[
        quien("pizon", 270, 0, 0.5, "triste", entra="nada", y=1230, acciones=[{"at": "@excusa", "cara": "riendo", "pose": "pulgar"}]),
        quien("piz", 540, 0, 0.52, "vacio", entra="nada", y=1230, acciones=[
            {"at": "@75", "cara": "sorpresa", "take": True}, {"at": "@cinco", "cara": "riendo", "salta": True}]),
        quien("critica", 810, 0, 0.5, "esceptica", entra="nada", y=1230, acciones=[{"at": "@mala", "cara": "burla", "pose": "cruzados"}]),
        obj("mesa_electoral", 540, 1380, 0, 1.0, props={"texto": "MESA 1"}, entra="nada"),
        obj("billete", 540, 600, "@75", 1.2, props={"valor": "75"}, entra="cae", sfx="kaching", flota=True),
        etq("75 € DE DIETA", 540, 400, "@pagan", "amarillo", 1.0, hud=True),
        rot("+5 €", 820, 640, "@cinco", 110, "verde", golpe=True, rot=6),
    ]),
    # 5 · LOS PARTIDOS: subvención por escaño y por voto (para todos los que sacan escaño)
    dict(id="partidos", fondo="calle", animo="curioso", trans="corte",
         footnote="Orden HAC/1062/2026 · RTVC 08/10/2026 · Tribunal de Cuentas (2023)", lines=[
        V("Y los partidos cobran: 21.167 euros por cada escaño y 81 céntimos por cada voto al Congreso.", "normal"),
        V("En 2023, unos 58 millones en subvenciones.", "normal", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@escaño", "general", [540, 1000], 0.5, zoom=1.1),
               plano("@81", "general", [540, 950], 0.5), plano("@58", "general", dur=0.5)],
       elements=[
        quien("diputado", 230, 0, 0.55, "normal", id="p1", entra="pop", acciones=[{"at": "@escaño", "cara": "ilusionado", "mira": "arriba"}]),
        quien("diputado", 540, 0.15, 0.55, "normal", id="p2", entra="pop", acciones=[{"at": "@81", "cara": "ilusionado", "salta": True}]),
        quien("diputado", 850, 0.3, 0.55, "normal", id="p3", entra="pop", acciones=[{"at": "@voto", "cara": "riendo", "pose": "pulgar"}]),
        *atriles(),
        monedas("@escaño", 150, 930, 12),
        monedas("@céntimos", 150, 930, 10),
        etq("21.167 € / ESCAÑO", 540, 420, "@escaño", "amarillo", 1.0, hud=True, out="@58"),
        etq("0,81 € / VOTO", 540, 560, "@81", "verde", 1.0, hud=True, out="@58"),
        rot("2023: ~58 M€", 540, 480, "@58", 110, "amarillo", golpe=True),
    ]),
    # 6 · FINAL: el mapa entero iluminado, la cuenta por cabeza y la pregunta
    dict(id="final", fondo="mar_mapa", limites=LIM, animo="final", trans="zoom", footnote="Cálculo propio: 270 M€ / 38,7 millones de electores", lines=[
        V("Total: unos 7 euros por cada elector.", "normal"),
        V("¿Caro o barato para elegir quién gobierna? Te leo.", "normal", 0.15),
        V("Y síguenos para el próximo viaje de Piz.", "energia", 0.15),
    ], camara=[zoom(0, MAD, 2.6, 0), zoom(0.3, MAD, 0.95, 2.2)],
       elements=[
        mapa(R, 0, 0.01, progreso=1.0, resalta=TODAS),
        obj("contador", 540, 520, "@7", 0.9, hud=True, entra="pop", sfx="kaching", props={"valor": 7, "prefijo": "~", "sufijo": " €", "ancho": 520}),
        sello("CÁLCULO PROPIO", "azul", 700, "@elector"),
        quien("piz", 790, "@Caro", 0.6, "pensativo", y=1500, hud=True, entra="abajo", acciones=[
            {"at": "@barato", "pose": "piensa"}, {"at": "@leo", "mira": "camara", "cara": "ilusionado"},
            {"at": "@síguenos", "pose": "saluda", "cara": "riendo"}, {"at": "@viaje", "salta": True}]),
        rot("¿CARO O BARATO?", 540, 1000, "@Caro", 100, "amarillo", golpe=True, out="@síguenos-0.3"),
        rot("SÍGUENOS", 540, 1000, "@síguenos", 110, "amarillo", fx=[{"at": "@Piz", "do": "latir"}]),
    ]),
]

if __name__ == "__main__":
    episodio("coste_29n", "El 29N lo pagas tú", scenes,
             {"t": 2.6, "titulo": "El 29N lo pagas tú", "capitulo": None},
             ["Euronews (08/10/2026): el 29N superará los 270 M€; desglose de 2023 con datos de Interior y del Tribunal de Cuentas",
              "INE (09/10/2026): censo electoral del 29N, 38.728.356 electores",
              "Orden INT/650/2026, BOE 27/06/2026: dieta de 75 € por miembro de mesa",
              "Orden HAC/1062/2026: subvenciones electorales (RTVC, 08/10/2026)",
              "Coste por elector: cálculo propio de Pizarra Pública",
              "Mapas dibujados sobre contornos de Natural Earth (dominio público)"],
             ("🗳️ Votar parece gratis… pero el 29N costará más de 270 M€ (estimación)\n"
              "🚚 Papeletas para 38,7 millones de electores en 52 provincias y el extranjero\n"
              "📮 En 2023, solo Correos se llevó más de 100 M€\n"
              "💶 Cada miembro de mesa cobra 75 € (5 más que antes)\n"
              "🏛️ Partidos: 21.167 € por escaño y 0,81 € por voto\n"
              "💬 Unos 7 € por elector: ¿caro o barato?\n"
              "🔔 Síguenos · 📚 Fuentes en comentarios"),
             "📚 Fuentes: Euronews 08/10/2026 · INE 09/10/2026 · BOE 27/06/2026 (Orden INT/650/2026) · Orden HAC/1062/2026 (RTVC 08/10) · "
             "7 €/elector: cálculo propio. ¿Ves un error? Dínoslo.",
             ["#29N", "#elecciones", "#EleccionesGenerales", "#dinero", "#impuestos", "#politica", "#España", "#pizarrapublica"],
             series_tag="EXPLICADO FÁCIL")
