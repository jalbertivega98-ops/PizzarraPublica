#!/usr/bin/env python3
"""«El hombre que siempre renuncia» (26/10/2026). Mundo dibujado: mapa de España con Extremadura, Andalucía y Madrid,
el Senado y los tribunales. Alvise Pérez (SALF) promete no ir al Senado si PP y Vox pactan; hoy han pactado.

Guion y fuentes: /mnt/project-files/insta/guiones/alvise_renuncia.md (aprobado por joel el 26/10/2026)
  Extremadura: renuncia para no «regalar escaños claves al PSOE y Sumar» (Diario Crítico 18/11/2025, mensaje en Telegram).
  Andalucía: «renuncio» si PP o Vox firmaban cinco medidas antes del 20/03 (El Diario de Madrid 18/03/2026);
    se presentó el 17-M: 105.671 votos, 2,53 %, ningún escaño (The Objective 17/05/2026).
  Senado: «Únicamente al Senado», si PP y Vox pactan listas comunes (The Objective 09/10/2026).
  Pacto PP-Vox en el Senado: Vox se retira en 6 provincias y el PP en 3 (The Objective 26/10/2026). Listas: SIN CONFIRMAR.
  Congreso: cabeza de lista de SALF por Madrid (Libertad Digital 05/10/2026).
  Valladolid 21/10/2026: «Gano 60.000 euros al mes de vuestro dinero»; las partidas que citó suman unos 10.350 € (El Español).
  Supremo confirma la segunda condena por vulnerar el honor de Ábalos (EFE vía Público 09/10/2026): vía civil.
  Eurocámara tramita un cuarto suplicatorio (Europa Press vía Público 14/09/2026): investigación, no condena.
"""
from _mundo import *  # noqa: F401,F403

R = "espana"
EXT = P(R, -6.2, 39.2)
AND = P(R, -4.8, 37.5)
MAD = P(R, -3.7, 40.4)
ANDALUCIA = ["Huelva", "Sevilla", "Cádiz", "Málaga", "Córdoba", "Jaén", "Granada", "Almería"]


def A(text, pausa=None):
    """Frase literal de Alvise: voz del canal procesada («tele»), no imita la suya."""
    return dict(V(text, "normal", pausa), efecto_voz="tele")


scenes = [
    # 1 · GANCHO: Alvise levanta el cartel «RENUNCIO»… otra vez; Piz cuenta con los dedos
    dict(id="gancho", fondo="calle", animo="comico", footnote="Diario Crítico 18/11/2025 · El Diario de Madrid 18/03/2026 · The Objective 09/10/2026", lines=[
        V("Alvise acaba de decir «renuncio»… otra vez.", "energia"),
        V("Y ya van tres.", "remate", 0.1),
    ], camara=[plano(0, "medio", "alvise", 0, aire=260), plano("@otra", "general", [540, 1000], 0.5),
               plano("@tres", "general", [540, 1020], 0.4, zoom=1.06)],
       elements=[
        quien("alvise", 700, 0, 0.62, "ilusionado", entra="nada", acciones=[
            {"at": "@renuncio", "pose": "arriba", "cara": "riendo", "mira": "camara"}, {"at": "@otra", "salta": True},
            {"at": "@tres", "pose": "pulgar", "cara": "burla"}]),
        quien("piz", -200, "@otra-0.4", 0.55, "sorpresa", entra="nada", acciones=[
            {"at": "@otra-0.4", "x": 260, "dur": 0.6}, {"at": "@Y", "cara": "confundido", "pose": "encoge", "mira": "der"},
            {"at": "@tres", "cara": "susto", "take": True, "mira": "camara"}]),
        obj("cartel", 700, 760, "@renuncio", 1.0, entra="cae", sfx="golpe", props={"texto": "RENUNCIO"}),
        rot("3 VECES", 540, 380, "@tres", 120, "amarillo", golpe=True),
    ]),
    # 2 · EXTREMADURA: se ilumina en el mapa; sello CONFIRMADO
    dict(id="extremadura", fondo="mar_mapa", limites=LIM, animo="curioso", trans="zoom", footnote="Diario Crítico 18/11/2025 (mensaje de Alvise en Telegram)", lines=[
        V("Primera: noviembre de 2025. Renuncia a presentarse en Extremadura…", "normal"),
        V("para no «regalar escaños» al PSOE.", "normal", 0.1),
    ], camara=[zoom(0, MAD, 1.0, 0), zoom("@Extremadura", EXT, 2.4, 1.0), zoom("@PSOE", EXT, 2.0, 0.6)],
       elements=[
        mapa(R, 0, 1.4, acciones=[{"at": "@Extremadura", "props": {"resalta": ["Badajoz", "Cáceres"]}, "sfx": "pop"}]),
        quien("alvise", EXT[0], "@Extremadura+0.3", 0.11, "normal", y=EXT[1] + 20, entra="cae", acciones=[
            {"at": "@regalar", "x": EXT[0] + 120, "dur": 0.8}, {"at": "@PSOE", "cara": "serio", "mira": "camara"}]),
        rot("1 · EXTREMADURA", 540, 430, "@Primera", 90, "amarillo", golpe=True),
        etq("NOV. 2025", 540, 600, "@noviembre", "azul", 0.7, hud=True, out="@regalar"),
        sello("SE RETIRA", "verde", 1500, "@regalar"),
    ]),
    # 3 · ANDALUCÍA: «renuncio»… con condiciones; no firman; se presenta; contador a cero
    dict(id="andalucia", fondo="mar_mapa", limites=LIM, animo="tension", trans="corte",
         footnote="El Diario de Madrid 18/03/2026 · The Objective 17/05/2026", lines=[
        V("Segunda: marzo de 2026. «Renuncio a Andalucía»… si PP o Vox le firmaban cinco medidas.", "normal"),
        V("No firmaron. Se presentó: 105.671 votos, un 2,5 %…", "normal", 0.15),
        V("y cero escaños.", "remate", 0.1),
    ], camara=[zoom(0, AND, 2.0, 0), zoom("@cinco", AND, 2.4, 0.6), zoom("@presentó", AND, 1.8, 0.6),
               zoom("@cero", AND, 2.2, 0.5)],
       elements=[
        mapa(R, 0, 0.01, acciones=[{"at": 0, "props": {"resalta": ANDALUCIA}}]),
        rot("2 · ANDALUCÍA", 540, 430, 0, 90, "amarillo", golpe=True, out="@cinco"),
        etq("MAR. 2026", 540, 600, "@marzo", "azul", 0.7, hud=True, out="@cinco"),
        quien("alvise", AND[0] - 60, 0.2, 0.11, "ilusionado", y=AND[1] + 20, entra="cae", acciones=[
            {"at": "@Renuncio", "pose": "arriba"}, {"at": "@Andalucía", "salta": True, "cara": "riendo"}, {"at": "@si", "pose": "senala", "cara": "burla"}, {"at": "@firmaron", "cara": "sorpresa", "take": True},
            {"at": "@presentó", "salta": True, "cara": "riendo"}, {"at": "@cero", "cara": "triste", "pose": "caidos"}]),
        obj("checklist", 540, 560, "@cinco", 0.6, hud=True, entra="pop", sfx="papel", out="@presentó",
            props={"items": ["5 medidas: ¿firma PP?", "5 medidas: ¿firma Vox?"], "marcas": [None, None]},
            acciones=[{"at": "@firmaron", "props": {"marcas": ["no", "no"]}}]),
        sello("NO FIRMARON", "naranja", 1480, "@firmaron", out="@presentó"),
        obj("contador", 540, 470, "@105.671", 0.8, hud=True, entra="pop", sfx="kaching", out="@cero",
            props={"valor": 105671, "sufijo": " VOTOS", "ancho": 820}),
        etq("2,5 %", 540, 640, "@2,5", "naranja", 0.8, hud=True, out="@cero"),
        obj("contador", 540, 470, "@cero", 0.9, hud=True, entra="pop", sfx="golpe", props={"valor": 0, "sufijo": " ESCAÑOS", "ancho": 820}),
        sello("CONFIRMADO", "verde", 1480, "@escaños"),
    ]),
    # 4 · EL SENADO: la promesa de octubre y el pacto de hoy entre PP y Vox
    dict(id="senado", fondo={"tipo": "plano", "color": (110, 34, 40)}, animo="tension", trans="iris",
         footnote="The Objective 09/10/2026 y 26/10/2026", lines=[
        V("Tercera: en octubre promete no ir al Senado si PP y Vox van juntos.", "normal"),
        V("Y hoy, PP y Vox han cerrado su pacto para el Senado.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@Senado", "general", [540, 900], 0.6, zoom=1.08),
               plano("@hoy", "general", [540, 1050], 0.5), plano("@pacto", "general", [540, 1000], 0.4, zoom=1.05)],
       elements=[
        edif("congreso", 540, 0, 0.62, texto="SENADO", entra="nada", dibuja=0.8, acciones=[
            {"at": "@juntos", "cara": "pensativo"}, {"at": "@pacto", "cara": "sorpresa"}]),
        quien("alvise", 540, 0.2, 0.42, "normal", y=1420, entra="pop", acciones=[
            {"at": "@promete", "pose": "manos_juntas", "cara": "ilusionado", "mira": "camara"}, {"at": "@juntos", "pose": "senala_arriba"},
            {"at": "@hoy", "mira": "izq", "cara": "sorpresa", "take": True}, {"at": "@pacto", "mira": "der"},
            {"at": "@Senado.", "mira": "camara", "cara": "pensativo", "pose": "piensa"}]),
        rot("3 · EL SENADO", 540, 380, 0, 90, "amarillo", golpe=True, out="@hoy"),
        quien("feijoo", -200, "@hoy", 0.5, "riendo", y=1460, entra="nada", acciones=[
            {"at": "@hoy", "x": 250, "dur": 0.7}, {"at": "@pacto", "pose": "pulgar", "mira": "der"}]),
        quien("abascal", 1280, "@hoy", 0.5, "riendo", y=1460, entra="nada", acciones=[
            {"at": "@hoy", "x": 830, "dur": 0.7}, {"at": "@pacto", "pose": "pulgar", "mira": "izq"}]),
        sello("PROMESA", "azul", 520, "@juntos", out="@hoy"),
        sello("PACTO PP-VOX: CONFIRMADO", "verde", 520, "@pacto"),
    ]),
    # 5 · EL GIRO: al Congreso sí va; Madrid se enciende; Piz no entiende nada
    dict(id="giro", fondo="mar_mapa", limites=LIM, animo="comico", trans="zoom", footnote="Libertad Digital 05/10/2026", lines=[
        V("Pero al Congreso sí va: número uno de SALF por Madrid.", "normal"),
        V("Entonces… ¿renuncia o no renuncia?", "remate", 0.15),
    ], camara=[zoom(0, MAD, 1.2, 0), zoom("@Madrid", MAD, 2.8, 0.8), zoom("@Entonces", MAD, 2.2, 0.5)],
       elements=[
        mapa(R, 0, 0.01, acciones=[{"at": "@Madrid", "props": {"resalta": ["Madrid"]}, "sfx": "pop"}]),
        obj("chincheta", MAD[0] + 10, MAD[1], "@Madrid", 0.16, props={"diseno": "espana"}, entra="cae"),
        quien("alvise", MAD[0] - 30, "@uno", 0.11, "ilusionado", y=MAD[1] + 14, entra="cae", acciones=[{"at": "@Madrid", "salta": True}]),
        rot("Nº 1 POR MADRID", 540, 430, "@número", 96, "amarillo", golpe=True, out="@Entonces"),
        quien("piz", 540, "@Entonces", 0.42, "confundido", y=1640, entra="abajo", hud=True, acciones=[
            {"at": "@renuncia", "pose": "encoge", "mira": "camara"}, {"at": "@no", "cara": "pensativo", "pose": "piensa"}]),
        sello("SENADO: SIN CONFIRMAR", "naranja", 640, "@renuncia"),
    ]),
    # 6 · LO HEAVY 1: los 60.000 € de Valladolid y la calculadora de Piz
    dict(id="sueldo", fondo="calle", animo="tension", trans="barrido", footnote="El Español 21/10/2026 (acto de recogida de avales en Valladolid)", lines=[
        V("Y hay más. Hace cinco días, recogiendo firmas en Valladolid, soltó esto:", "normal"),
        A("«Gano 60.000 euros al mes de vuestro dinero».", 0.1),
        V("Las cuentas que dio después suman unos 10.000.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@Gano", "medio", "alvise", 0.5, aire=260),
               plano("@cuentas", "general", [540, 1000], 0.5), plano("@10.000", "general", [540, 960], 0.4, zoom=1.08)],
       elements=[
        quien("alvise", -200, 0, 0.6, "normal", entra="nada", acciones=[
            {"at": "@cinco", "x": 360, "dur": 0.8}, {"at": "@Valladolid", "pose": "saluda", "mira": "camara"}, {"at": "@Gano", "pose": "senala", "cara": "burla"},
            {"at": "@dinero", "pose": "jarras", "cara": "riendo"}, {"at": "@10.000", "cara": "sorpresa", "mira": "der"}]),
        rot("HACE 5 DÍAS", 540, 420, "@más", 96, "amarillo", golpe=True, out="@Valladolid"),
        etq("VALLADOLID", 540, 600, "@Valladolid", "azul", 0.7, hud=True, out="@Gano"),
        obj("bocadillo", 540, 520, "@Gano", 0.75, hud=True, entra="pop", sfx="pop", out="@cuentas",
            props={"lineas": ["«Gano 60.000 euros al mes", "de vuestro dinero»"]}),
        dict(monedas("@euros", 120, 960, 12)),
        quien("piz", 1300, "@cuentas", 0.55, "pensativo", entra="nada", acciones=[
            {"at": "@cuentas", "x": 800, "dur": 0.6}, {"at": "@suman", "pose": "sostiene", "cara": "pensativo"},
            {"at": "@10.000", "cara": "confundido", "mira": "camara"}]),
        obj("calculadora", 800, 880, "@suman", 0.7, entra="pop", sfx="calculadora", props={"texto": "10.350"}),
        etq("DIETAS + ASISTENCIA + 350 €", 540, 420, "@suman", "naranja", 0.7, hud=True),
        sello("DECLARACIÓN", "azul", 1500, "@dinero", out="@cuentas"),
    ]),
    # 7 · LO HEAVY 2: los tribunales, cada cosa con su sello
    dict(id="tribunales", fondo={"tipo": "plano", "color": (28, 52, 110)}, animo="tension", trans="papel",
         footnote="EFE vía Público 09/10/2026 · Europa Press vía Público 14/09/2026", lines=[
        V("En los tribunales: el Supremo ha confirmado su segunda condena por vulnerar el honor de Ábalos. Es una condena civil.", "normal"),
        V("Y la Eurocámara tramita un cuarto suplicatorio para quitarle la inmunidad. Eso es una investigación, no una condena.", "normal", 0.15),
    ], camara=[plano(0, "general", [540, 900], 0), plano("@segunda", "general", [540, 760], 0.6, zoom=1.08),
               plano("@cuarto", "general", [540, 900], 0.6, zoom=1.1), plano("@investigación", "general", [540, 900], 0.5)],
       elements=[
        obj("documento", 540, 680, 0.2, 0.9, id="doc", entra="nada", dibujo=1.0, sfx="papel", props={
            "titulo": "TRIBUNALES", "subtitulo": "Alvise Pérez",
            "articulos": [{"id": "hon", "titulo": "Supremo", "lineas": ["2.ª condena: honor de Ábalos", "(vía civil)"]},
                          {"id": "sup", "titulo": "Eurocámara", "lineas": ["4.º suplicatorio:", "pedir quitar la inmunidad"]}]},
            acciones=[{"at": "@Supremo", "props": {"resalta": ["hon"]}}, {"at": "@Eurocámara", "props": {"resalta": ["sup"]}}]),
        quien("jueza", -200, "@Supremo", 0.42, "serio", y=1340, entra="nada", acciones=[{"at": "@Supremo", "x": 190, "dur": 0.6}, {"at": "@civil", "pose": "senala"}]),
        quien("alvise", 1300, "@honor", 0.42, "normal", y=1340, entra="nada", acciones=[
            {"at": "@honor", "x": 890, "dur": 0.6}, {"at": "@civil", "cara": "serio", "pose": "cruzados"},
            {"at": "@inmunidad", "cara": "preocupado", "mira": "arriba"}, {"at": "@condena+0.3", "cara": "normal", "mira": "camara"}]),
        sello("CONDENA CIVIL", "rojo", 1040, "@civil", out="@Eurocámara"),
        sello("INVESTIGACIÓN, NO CONDENA", "naranja", 1040, "@investigación"),
    ]),
    # 8 · FINAL: Piz con dos carteles y la pregunta
    dict(id="final", fondo="salon", animo="final", trans="iris", footnote="Pregunta a la audiencia", lines=[
        V("¿Estratega que une a la derecha… o candidato que divide el voto?", "normal"),
        V("Te leo en comentarios. Y síguenos: el 29N saldremos de dudas.", "energia", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@voto", "general", [540, 1000], 0.5, zoom=1.05),
               plano("@síguenos", "medio", "piz", 0.5, aire=300)],
       elements=[
        quien("piz", 540, 0, 0.62, "pensativo", entra="nada", acciones=[
            {"at": "@Estratega", "pose": "senala_izq", "mira": "izq"}, {"at": "@candidato", "pose": "senala", "mira": "der"},
            {"at": "@voto", "cara": "pensativo", "pose": "piensa", "mira": "camara"}, {"at": "@leo", "cara": "ilusionado", "pose": "senala"},
            {"at": "@síguenos", "pose": "saluda", "cara": "riendo"}, {"at": "@dudas", "salta": True}]),
        etq("¿UNE?", 280, 880, "@Estratega", "verde", 0.7, out="@leo"),
        etq("¿DIVIDE?", 800, 880, "@candidato", "rojo", 0.7, out="@leo"),
        rot("¿TÚ QUÉ CREES?", 540, 440, "@voto", 110, "amarillo", golpe=True, out="@síguenos-0.3", fx=[{"at": "@leo", "do": "latir"}]),
        rot("SÍGUENOS", 540, 440, "@síguenos", 110, "amarillo"),
    ]),
]

if __name__ == "__main__":
    episodio("alvise_renuncia", "El hombre que siempre renuncia", scenes,
             {"t": 3.0, "titulo": "El hombre que siempre renuncia", "capitulo": None},
             ["Diario Crítico (18/11/2025): Alvise renuncia a Extremadura",
              "El Diario de Madrid (18/03/2026): las cinco condiciones para no ir en Andalucía",
              "The Objective (17/05/2026): SALF en las andaluzas, 105.671 votos, 2,53 %, 0 escaños",
              "The Objective (09/10/2026): renuncia al Senado si PP y Vox pactan",
              "The Objective (26/10/2026): pacto PP-Vox para el Senado",
              "Libertad Digital (05/10/2026): cabeza de lista de SALF por Madrid",
              "El Español (21/10/2026): «Gano 60.000 euros al mes de vuestro dinero»",
              "EFE vía Público (09/10/2026): el Supremo confirma la segunda condena por el honor de Ábalos",
              "Europa Press vía Público (14/09/2026): cuarto suplicatorio en la Eurocámara",
              "Personajes dibujados como pizarras, sin caricatura; la frase de Alvise es literal y con otra voz"],
             ("🙋 Alvise acaba de decir «renuncio»… y ya van tres\n"
              "🗺️ Extremadura (2025): se retira para no «regalar escaños» al PSOE\n"
              "🗳️ Andalucía (2026): «renuncio»… pero se presentó: 2,5 % y 0 escaños\n"
              "🏛️ Senado: lo promete si PP y Vox pactan; hoy han pactado\n"
              "📍 Pero al Congreso sí va: nº 1 por Madrid\n"
              "💶 «Gano 60.000 euros al mes de vuestro dinero»\n"
              "💬 ¿Estratega que une a la derecha o candidato que divide el voto? Te leemos 👇\n"
              "🔔 Síguenos · 📚 Fuentes en comentarios"),
             "📚 Fuentes: Diario Crítico 18/11/2025 · El Diario de Madrid 18/03/2026 · The Objective 17/05, 09/10 y 26/10/2026 · "
             "Libertad Digital 05/10/2026 · El Español 21/10/2026 · EFE y Europa Press vía Público. ¿Ves un error? Dínoslo.",
             ["#Alvise", "#SALF", "#SeAcabóLaFiesta", "#29N", "#Senado", "#elecciones", "#pizarrapublica"],
             series_tag="EXPLICADO FÁCIL")
