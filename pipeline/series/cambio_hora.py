#!/usr/bin/env python3
"""«Este domingo cambia la hora… ¿la última vez?» (viernes 23/10/2026). Mundo dibujado: relojes, mapa de Europa.

Fuentes:
  Vandal / El Español 21/10/2026: domingo 25/10, a las 03:00 vuelven a ser las 02:00 (Canarias 02:00 → 01:00); el día
    dura 25 horas; no hay fecha aprobada para acabar con el cambio.
  Público 25/10/2024 y Comisión Europea (consulta 2018): 4,6 millones de respuestas, el 84 % a favor de acabar con él.
  Menorca.info / Última Hora 20/10/2025 y eldiario.es: Sánchez propone a la UE acabar con el cambio de hora en 2026
    («provoca efectos negativos en la salud»).
  DOUE 2026/1660 (Comunicación de la Comisión, 18/03/2026) y El Demócrata: calendario del horario de verano 2027-2031,
    con dos cambios al año; los Estados miembros no se ponen de acuerdo en qué horario dejar.
"""
from _mundo import *  # noqa: F401,F403

R = "mundo"
EUR = P(R, 10, 50)
UE = ["AUT", "BEL", "BGR", "HRV", "CYP", "CZE", "DNK", "EST", "FIN", "FRA", "DEU", "GRC", "HUN", "IRL", "ITA", "LVA",
      "LTU", "LUX", "MLT", "NLD", "POL", "PRT", "ROU", "SVK", "SVN", "ESP", "SWE"]
F_HOY = "Vandal / El Español 21/10/2026"
F_UE = "DOUE 2026/1660 (Comisión Europea, 18/03/2026) · El Demócrata"

scenes = [
    # 1 · GANCHO: el reloj gira hacia atrás y el día tiene 25 horas
    dict(id="gancho", fondo="salon", animo="tension", footnote=F_HOY, lines=[
        V("Este domingo, a las tres de la madrugada… vuelven a ser las dos.", "energia"),
        V("Ese día tendrá veinticinco horas.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@tres", "general", [700, 800], 0.5, zoom=1.1),
               plano("@dos", "general", [700, 800], 0.4, zoom=1.15), plano("@veinticinco", "general", [540, 900], 0.5)],
       elements=[
        obj("reloj", 720, 760, 0, 1.3, entra="pop", sfx="pop", props={"velocidad": -8}),
        rot("3:00", 720, 480, "@tres", 110, "rojo", golpe=True, out="@dos"),
        rot("2:00", 720, 480, "@dos", 110, "verde", golpe=True, out="@veinticinco"),
        obj("contador", 540, 480, "@veinticinco", 0.85, hud=True, entra="pop", sfx="kaching", dibujo=1.0,
            props={"valor": 25, "desde": 24, "sufijo": " HORAS", "ancho": 620}),
        quien("piz", 280, 0, 0.6, "pensativo", entra="nada", acciones=[
            {"at": "@domingo", "pose": "senala", "mira": "der"}, {"at": "@madrugada", "cara": "sorpresa"},
            {"at": "@vuelven", "take": True, "cara": "susto"}, {"at": "@dos", "pose": "piensa", "cara": "confundido"},
            {"at": "@veinticinco", "salta": True, "cara": "riendo"}, {"at": "@horas", "pose": "pulgar"}]),
    ]),
    # 2 · LO QUE NOTAS: una hora más de cama… y la tarde se hace de noche antes
    dict(id="notas", fondo={"tipo": "calle", "hora": "tarde"}, animo="curioso", trans="barrido", footnote=F_HOY, lines=[
        V("Una hora más en la cama… pero por la tarde anochecerá una hora antes.", "normal"),
        V("Y hay quien lo nota: cansancio, peor sueño, menos concentración.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@tarde", "general", [540, 900], 0.6, zoom=1.06),
               plano("@cansancio", "medio", "pizon", 0.5, aire=240)],
       elements=[
        etq("+1 HORA DE SUEÑO", 540, 520, "@cama", "azul", 0.9, hud=True, out="@tarde"),
        rot("ANOCHECE ANTES", 540, 520, "@anochecerá", 92, "naranja", golpe=True, out="@nota"),
        quien("pizon", 540, 0, 0.6, "ilusionado", entra="nada", acciones=[
            {"at": "@hora", "pose": "saluda", "cara": "riendo"}, {"at": "@cama", "salta": True},
            {"at": "@tarde", "mira": "arriba", "cara": "preocupado"}, {"at": "@antes", "pose": "encoge"},
            {"at": "@cansancio", "cara": "triste", "pose": "caidos"}, {"at": "@sueño", "tiembla": True},
            {"at": "@concentración", "cara": "confundido", "pose": "piensa"}]),
        rot("CANSANCIO · PEOR SUEÑO", 540, 520, "@cansancio", 76, "rojo", golpe=True),
    ]),
    # 3 · LA CONSULTA: el mapa de Europa se ilumina con el 84 %
    dict(id="consulta", fondo="mar_mapa", limites=LIM, animo="curioso", trans="papel",
         footnote="Comisión Europea, consulta pública de 2018", lines=[
        V("En 2018, la Unión Europea preguntó: respondieron 4,6 millones de personas.", "normal"),
        V("El 84 % pidió acabar con el cambio de hora.", "remate", 0.15),
    ], camara=[zoom(0, EUR, 2.6, 0), zoom("@preguntó", EUR, 3.4, 0.9), zoom("@84", EUR, 3.0, 0.6), zoom("@acabar", P(R, -3.7, 40.4), 4.2, 1.2)],
       elements=[
        mapa(R, 0, 1.4, acciones=[{"at": "@preguntó", "props": {"resalta": UE}, "sfx": "pop"}]),
        obj("contador", 540, 480, "@respondieron", 0.8, hud=True, entra="pop", sfx="kaching", dibujo=1.2, out="@84",
            props={"valor": 4.6, "decimales": 1, "sufijo": " MILLONES", "ancho": 700}),
        rot("84 % : QUE SE ACABE", 540, 480, "@84", 92, "amarillo", golpe=True),
        quien("profe", 840, 0.2, 0.5, "normal", y=1580, hud=True, entra="der", acciones=[
            {"at": "@preguntó", "pose": "senala_izq"}, {"at": "@millones", "cara": "sorpresa", "salta": True},
            {"at": "@84", "pose": "pulgar", "cara": "ilusionado"}, {"at": "@pidió", "salta": True}, {"at": "@acabar", "pose": "senala_izq"},
            {"at": "@cambio", "cara": "riendo"}, {"at": "@hora", "mira": "camara", "pose": "saluda"}]),
    ]),
    # 4 · ESPAÑA LO PIDE: Sánchez lo propone en Bruselas
    dict(id="espana", fondo={"tipo": "plano", "color": (28, 52, 110)}, animo="curioso", trans="corte",
         footnote="Menorca.info / Última Hora 20/10/2025 · eldiario.es", lines=[
        V("En octubre de 2025, el Gobierno pidió a la UE quitarlo ya en 2026: dice que afecta a la salud.", "normal"),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@UE", "general", [700, 950], 0.6, zoom=1.06),
               plano("@2026", "general", [540, 900], 0.5, zoom=1.1), plano("@salud", "medio", "sanchez", 0.5, aire=240)],
       elements=[
        obj("bandera", 820, 1340, "@UE-0.2", 0.8, entra="crece", sfx="pop", props={"diseno": "ue"}),
        quien("sanchez", 360, 0, 0.6, "serio", entra="nada", acciones=[
            {"at": "@octubre", "mira": "camara"}, {"at": "@Gobierno", "pose": "senala", "mira": "der"}, {"at": "@UE", "x": 420, "dur": 0.6},
            {"at": "@quitarlo", "pose": "puno"}, {"at": "@ya", "cara": "ilusionado"},
            {"at": "@2026", "salta": True}, {"at": "@dice", "pose": "piensa"}, {"at": "@afecta", "cara": "preocupado"},
            {"at": "@salud", "mira": "camara", "pose": "manos_juntas"}]),
        rot("FIN EN 2026", 540, 480, "@quitarlo", 104, "amarillo", golpe=True),
        sello("DECLARACIÓN", "naranja", 640, "@salud"),
    ]),
    # 5 · GIRO: el calendario de la UE llega hasta 2031
    dict(id="giro", fondo="oficina", animo="tension", musica="corte", trans="iris", footnote=F_UE, lines=[
        V("Pero en marzo, Bruselas publicó el calendario hasta 2031… con dos cambios de hora cada año.", "normal"),
        V("¿Por qué? Los países no se ponen de acuerdo en qué horario dejar.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 950], 0), plano("@Bruselas", "general", [600, 900], 0.6, zoom=1.04), plano("@2031", "general", [540, 800], 0.5, zoom=1.08),
               plano("@acuerdo", "general", [540, 1000], 0.5)],
       elements=[
        obj("documento", 540, 760, 0, 0.9, entra="cae", sfx="papel", dibuja=1.0, out="@Por",
            props={"titulo": "HORARIO DE VERANO", "subtitulo": "Comisión Europea · 2027-2031", "articulos": [
                {"id": "a", "titulo": "2027 · 2028 · 2029", "lineas": ["marzo: se adelanta", "octubre: se atrasa"]},
                {"id": "b", "titulo": "2030 · 2031", "lineas": ["marzo: se adelanta", "octubre: se atrasa"]}]}),
        rot("HASTA 2031", 540, 420, "@2031", 110, "rojo", golpe=True, out="@Por"),
        quien("piz", 880, 0, 0.42, "ilusionado", y=1660, entra="nada", out="@Por", acciones=[
            {"at": "@marzo", "mira": "izq", "pose": "senala_izq"}, {"at": "@Bruselas", "salta": True},
            {"at": "@calendario", "cara": "sorpresa", "pose": "piensa"}, {"at": "@2031", "take": True, "cara": "susto"},
            {"at": "@dos", "tiembla": True}, {"at": "@año", "cara": "indignado", "pose": "jarras"}]),
        sello("CONFIRMADO", "verde", 1180, "@cambios"),
        *[quien(q, x, "@Por-0.2", 0.45, "enfado", entra="nada", acciones=[
            {"at": "@países", "pose": pose, "mira": mira}, {"at": "@acuerdo", "salta": True, "cara": "indignado"}])
          for q, x, pose, mira in (("critica", 220, "jarras", "der"), ("pizon", 540, "encoge", "camara"), ("sarcastica", 860, "cruzados", "izq"))],
        rot("SIN ACUERDO", 540, 480, "@acuerdo", 104, "rojo", golpe=True),
    ]),
    # 5b · EL AHORRO: la excusa de la luz, en 6 € al año
    dict(id="ahorro", fondo="salon", animo="tension", trans="corte",
         footnote="Joan Groizard, secretario de Estado de Energía (Diari de Tarragona 20/10/2025) · Šefčovič, Comisión Europea (Reuters 14/09/2018)", lines=[
        V("¿Y el ahorro de luz, que era la excusa? El propio Gobierno lo calcula en unos seis euros al año por persona.", "normal"),
        V("Entonces… ¿a quién le interesa seguir cambiando la hora?", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@seis", "general", [540, 800], 0.5, zoom=1.1),
               plano("@interesa", "general", [540, 1000], 0.5)],
       elements=[
        obj("hucha", 760, 1250, 0, 0.8, entra="pop", sfx="pop"),
        obj("contador", 540, 480, "@seis", 0.8, hud=True, entra="pop", sfx="kaching", dibujo=1.0, out="@Entonces",
            props={"valor": 6, "sufijo": " € AL AÑO", "ancho": 640}),
        monedas("@seis", 600, 900, 3),
        sello("DECLARACIÓN", "naranja", 660, "@persona"),
        rot("¿A QUIÉN LE INTERESA?", 540, 480, "@Entonces", 84, "rojo", golpe=True),
        quien("pizon", 330, 0, 0.6, "pensativo", entra="nada", acciones=[
            {"at": "@ahorro", "pose": "senala", "mira": "der"}, {"at": "@excusa", "cara": "esceptica"},
            {"at": "@Gobierno", "pose": "piensa"}, {"at": "@seis", "cara": "sorpresa", "take": True},
            {"at": "@persona", "pose": "encoge", "cara": "burla"}, {"at": "@Entonces", "mira": "camara", "cara": "esceptica"},
            {"at": "@interesa", "pose": "jarras"}, {"at": "@hora", "salta": True}]),
    ]),
    # 6 · FINAL: verano o invierno para siempre
    dict(id="final", fondo={"tipo": "rayos", "color": "amarillo"}, animo="final", trans="zoom", footnote="Pregunta a la audiencia", lines=[
        V("¿Y tú qué prefieres para siempre: horario de verano o de invierno?", "energia"),
        V("Te leo en comentarios. Y síguenos.", "normal", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@verano", "general", [300, 950], 0.4, zoom=1.08),
               plano("@invierno", "general", [780, 950], 0.4, zoom=1.08), plano("@síguenos", "general", [540, 1000], 0.5)],
       elements=[
        obj("sol", 280, 820, "@verano-0.2", 0.8, entra="pop", sfx="pop"),
        obj("nube", 800, 820, "@invierno-0.2", 1.0, entra="pop", sfx="pop"),
        rot("¿VERANO O INVIERNO?", 540, 480, "@prefieres", 88, "rojo", golpe=True, out="@síguenos-0.3"),
        rot("SÍGUENOS", 540, 480, "@síguenos", 110, "rojo"),
        quien("piz", 540, 0, 0.6, "pensativo", entra="nada", acciones=[
            {"at": "@prefieres", "pose": "piensa"}, {"at": "@verano", "mira": "izq", "pose": "senala_izq", "cara": "ilusionado"},
            {"at": "@invierno", "mira": "der", "pose": "senala", "cara": "pensativo"}, {"at": "@leo", "mira": "camara", "cara": "riendo"},
            {"at": "@síguenos", "pose": "saluda", "salta": True}]),
    ]),
]

if __name__ == "__main__":
    episodio("cambio_hora", "Cambia la hora… ¿la última vez?", scenes,
             {"t": 1.2, "titulo": "Cambia la hora… ¿la última vez?", "capitulo": None},
             ["Vandal / El Español (21/10/2026): domingo 25/10, a las 3:00 vuelven a ser las 2:00; el día dura 25 horas",
              "Comisión Europea, consulta de 2018: 4,6 millones de respuestas, 84 % a favor de acabar con el cambio",
              "Menorca.info / Última Hora (20/10/2025): Sánchez propone a la UE acabar con el cambio de hora en 2026",
              "DOUE 2026/1660 (18/03/2026): calendario del horario de verano 2027-2031, con dos cambios al año",
              "Diari de Tarragona (20/10/2025): Groizard, secretario de Estado de Energía: ahorro de unos 6 € al año por persona",
              "Reuters (14/09/2018): Šefčovič: «el ahorro de energía es actualmente marginal»"],
             ("⏰ Este domingo 25, a las 3:00 vuelven a ser las 2:00: el día tendrá 25 horas\n"
              "😴 Una hora más de sueño… pero anochecerá una hora antes\n"
              "🗳️ En 2018, el 84 % de 4,6 millones de europeos pidió acabar con el cambio de hora\n"
              "🇪🇸 En 2025 el Gobierno pidió quitarlo ya en 2026\n"
              "📅 Pero la UE publicó el calendario hasta 2031: seguimos con dos cambios al año\n"
              "💡 ¿Y el ahorro de luz? El propio Gobierno lo calcula en unos 6 € al año por persona\n"
              "🤔 Entonces… ¿a quién le interesa seguir cambiando la hora?\n"
              "💬 ¿VERANO o INVIERNO para siempre? Te leo 👇\n"
              "🔔 Síguenos · 📚 Fuentes en comentarios"),
             "📚 Fuentes: Vandal/El Español 21/10/2026 · Comisión Europea (consulta 2018) · Última Hora 20/10/2025 · "
             "DOUE 2026/1660 (18/03/2026) · Diari de Tarragona 20/10/2025 (Groizard, 6 €/año). ¿Ves un error? Dínoslo.",
             ["#CambioDeHora", "#HorarioDeInvierno", "#25Octubre", "#UE", "#España", "#pizarrapublica"],
             series_tag="EXPLICADO FÁCIL")
