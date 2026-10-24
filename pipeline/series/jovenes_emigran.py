#!/usr/bin/env python3
"""«Los jóvenes que se van» (2026): españoles que emigran al extranjero.

Fuente: INE, Estadística de Migraciones y Cambios de Residencia 2024 (definitiva, 11/12/2025), tablas 69703, 69705 y 69706:
  137.719 emigraciones de españoles; 88.243 nacidos en España (49.476 nacidos fuera).
  20-39 años: 49.942 (cálculo propio con las edades quinquenales). 25-34 nacidos en España: 17.792.
  Destinos (todas las edades): Francia 16.353, Reino Unido 15.349, EE. UU. 13.185, Alemania 12.509.
  Saldo de españoles: +6.616; de nacidos en España: −25.521.
  Matiz: el Padrón infravalora las salidas (muchos no se dan de baja). Datos de 2024 (los de 2025 salen en diciembre de 2026).
"""
from _tu_dinero import *  # noqa: F401,F403

INE = "INE, Estadística de Migraciones 2024"

scenes = [
    dict(id="gancho", fondo="calle", animo="curioso", footnote=INE + " · españoles de 20 a 39 años", lines=[
        V("En 2024 se fueron de España casi 50.000 españoles de entre 20 y 39 años.", "energia"),
        V("¿Adónde?", "remate", 0.2),
    ], camara=[plano(0, "general", dur=0), plano("@Adónde", "abierto", dur=0.4)],
       elements=[
        quien("piz", 300, 0, 0.72, "normal", entra="izq", objeto="saco", pose="sostiene", acciones=[
            {"at": "@fueron", "mira": "avion", "cara": "sorpresa"}, {"at": "@50.000", "take": True},
            {"at": "@Adónde", "mira": "camara", "pose": "encoge", "cara": "pensativo", "objeto": None}]),
        obj("avion", 1300, 560, "@fueron", 0.65, id="avion", entra="nada", acciones=[{"at": "@fueron", "x": 760, "dur": 1.2},
                                                                                     {"at": "@Adónde", "x": -400, "dur": 1.6}]),
        rot("≈ 50.000", 600, 480, "@50.000", 120, C, golpe=True),
        rot("20-39 AÑOS", 600, 620, "@39", 80, "amarillo", golpe=True),
    ]),
    dict(id="destinos", fondo={"tipo": "playa", "variante": "montana"}, animo="alegre", trans="pan", footnote=INE + " · destinos, todas las edades", lines=[
        V("Primero, Francia: 16.353. Después, Reino Unido, Estados Unidos y Alemania.", "normal"),
    ], camara=[plano(0, "general", dur=0), plano("@Alemania", "abierto", dur=0.4)],
       elements=[
        quien("pizon", 280, 0, 0.72, "ilusionado", entra="izq", objeto="saco", pose="sostiene", acciones=[
            {"at": 0.9, "mira": "der"}, {"at": "@Francia", "salta": True, "cara": "riendo"}, {"at": "@16.353", "pose": "arriba"}, {"at": "@Reino", "mira": "der"},
            {"at": "@Unidos", "cara": "sorpresa"}, {"at": "@Alemania", "pose": "arriba", "objeto": None}]),
        rot("1. FRANCIA: 16.353", 600, 460, "@Francia", 66, "blanco", golpe=True),
        rot("2. REINO UNIDO: 15.349", 600, 550, "@Reino", 66, "amarillo", golpe=True),
        rot("3. EE. UU.: 13.185", 600, 640, "@Unidos", 66, "blanco", golpe=True),
        rot("4. ALEMANIA: 12.509", 600, 730, "@Alemania", 66, "amarillo", golpe=True),
    ]),
    dict(id="nacidos", fondo="rayos", animo="comico", musica="corte", trans="iris", footnote="INE 2024 · 49.476 de 137.719 nacieron fuera", lines=[
        V("Pero ojo: un tercio de los que se van nacieron fuera.", "sorpresa"),
        V("Españoles nacionalizados que vuelven a su país o se mudan a otro.", "normal", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@tercio", "medio", "profe", 0.3, aire=220)],
       elements=[
        quien("profe", 320, 0, 0.78, "normal", entra="pop", pose="senala_arriba", acciones=[
            {"at": "@tercio", "take": True, "cara": "sorpresa"}, {"at": "@nacionalizados", "pose": "senala", "cara": "normal"},
            {"at": "@vuelven", "mira": "camara"}]),
        quien("critica", 800, "@nacieron", 0.72, "esceptica", entra="der", acciones=[{"at": "@país", "cara": "pensativo", "pose": "encoge"}]),
        rot("1 DE CADA 3 NACIÓ FUERA", 540, 480, "@tercio", 66, "amarillo", golpe=True),
    ]),
    dict(id="saldo", fondo="calle", animo="tension", trans="pan", footnote=INE + " · saldo de españoles nacidos en España", lines=[
        V("Solo los nacidos aquí: se fueron 88.243 y volvieron muchos menos.", "normal"),
        V("Perdimos 25.521 en un año.", "remate", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@25.521", "medio", "piz", 0.3, aire=220)],
       elements=[
        quien("piz", 800, 0, 0.72, "normal", entra="der", acciones=[
            {"at": "@88.243", "mira": "izq", "cara": "sorpresa"}, {"at": "@volvieron", "cara": "preocupado"},
            {"at": "@25.521", "take": True, "cara": "triste"}]),
        quien("pizon", 300, "@fueron", 0.62, "normal", entra="nada", acciones=[{"at": "@fueron", "x": -300, "dur": 1.4, "corre": True}]),
        rot("SE VAN: 88.243", 540, 480, "@88.243", 80, "amarillo", golpe=True, out="@Perdimos"),
        rot("− 25.521", 540, 480, "@25.521", 120, C, golpe=True),
    ]),
    dict(id="edad", fondo="salon", animo="triste", trans="iris", footnote=INE + " · nacidos en España de 25 a 34 años", lines=[
        V("El grupo que más se va: de 25 a 34 años. 17.792 nacidos en España.", "normal"),
    ], camara=[plano(0, "general", dur=0), plano("@17.792", "medio", "piz", 0.3, aire=200)],
       elements=[
        quien("piz", 320, 0, 0.75, "normal", entra="nada", objeto="saco", pose="sostiene", acciones=[
            {"at": "@25", "mira": "camara"}, {"at": "@34", "salta": True}, {"at": "@nacidos", "mira": "camara", "cara": "pensativo"}, {"at": "@España", "tiembla": True}, {"at": "@17.792", "cara": "triste", "pose": "caidos", "objeto": None}]),
        rot("25-34 AÑOS", 600, 480, "@25", 96, "amarillo", golpe=True, out="@17.792"),
        rot("17.792", 600, 480, "@17.792", 120, C, golpe=True),
    ]),
    dict(id="padron", fondo="oficina", animo="curioso", trans="pan", footnote="El Padrón infravalora las salidas · datos de 2024", lines=[
        V("Y seguramente son más: muchos no se dan de baja en el padrón.", "sorpresa"),
    ], camara=[plano(0, "general", dur=0), plano("@padrón", "medio", "sarcastica", 0.3, aire=200)],
       elements=[
        quien("sarcastica", 320, 0, 0.75, "burla", entra="izq", acciones=[
            {"at": "@más", "pose": "jarras"}, {"at": "@baja", "take": True, "cara": "sorpresa"}, {"at": "@padrón", "cara": "riendo"}]),
        obj("contrato", 780, 800, "@baja", 0.7, entra="pop", props={"titulo": "PADRÓN", "hojas": 1}, sfx="papel"),
        rot("PROBABLEMENTE MÁS", 600, 480, "@más", 76, "amarillo", golpe=True),
    ]),
    dict(id="final", fondo="calle", animo="final", trans="iris", footnote=INE, lines=[
        V("¿Tienes a alguien fuera? Te leemos.", "normal"),
        V("Y síguenos: cada semana, datos que te tocan.", "energia", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@síguenos", "abierto", dur=0.4)],
       elements=[
        quien("piz", 300, 0, 0.72, "normal", entra="nada", acciones=[
            {"at": "@alguien", "mira": "camara", "cara": "pensativo"}, {"at": "@leemos", "pose": "senala", "cara": "ilusionado"},
            {"at": "@síguenos", "pose": "saluda", "cara": "riendo"}, {"at": "@tocan", "salta": True}]),
        obj("avion", -300, 560, "@alguien", 0.5, entra="nada", acciones=[{"at": "@alguien", "x": 1400, "dur": 3.0}]),
        rot("¿ALGUIEN FUERA?", 540, 470, "@alguien", 90, "amarillo", golpe=True, out="@síguenos-0.4"),
        rot("SÍGUENOS", 540, 470, "@síguenos", 110, "amarillo", fx=[{"at": "@tocan", "do": "latir"}]),
    ]),
]

if __name__ == "__main__":
    episodio("jovenes_emigran", "Los jóvenes que se van", scenes, {"t": 3.4, "titulo": "Los jóvenes que se van", "capitulo": None},
             ["INE: Estadística de Migraciones y Cambios de Residencia 2024 (11/12/2025)"],
             ("✈️ En 2024 se fueron casi 50.000 españoles de 20 a 39 años\n"
              "🌍 Destinos: Francia 16.353 · Reino Unido 15.349 · EE. UU. 13.185 · Alemania 12.509\n"
              "🔎 Ojo: 1 de cada 3 españoles que se van nació fuera\n"
              "🇪🇸 Nacidos en España: se fueron 88.243 y el saldo fue −25.521\n"
              "🎒 El grupo que más se va: 25-34 años (17.792 nacidos aquí)\n"
              "📋 Seguramente son más: muchos no se dan de baja en el padrón\n"
              "💬 ¿Tienes a alguien fuera?\n"
              "🔔 Síguenos · 📚 Fuentes en comentarios"),
             ("📚 Fuente: INE, Estadística de Migraciones y Cambios de Residencia 2024, definitiva (11/12/2025): 137.719 emigraciones de españoles, "
              "88.243 de nacidos en España; saldo de españoles +6.616 y de nacidos en España −25.521. 20-39 años: 49.942 (suma propia de edades). "
              "Destinos de todas las edades. Parte del Padrón, que infravalora las salidas. Los datos de 2025 salen en diciembre de 2026. "
              "¿Ves un error? Dínoslo."),
             ["#PizarraPública", "#Emigración", "#Jóvenes", "#INE", "#Datos", "#España", "#Trabajo"])
