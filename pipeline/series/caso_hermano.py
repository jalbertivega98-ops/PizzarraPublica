#!/usr/bin/env python3
"""«¿Qué ha pasado con el hermano de Sánchez?» (15/10/2026), explicado fácil.

Investigación con fuentes: /mnt/project-files/insta/investigacion/caso_david_sanchez.md
  2017: la Diputación de Badajoz contrata a David Sánchez como coordinador de actividades de los conservatorios.
  2024: denuncia de Manos Limpias; la jueza Beatriz Biedma abre diligencias (10/06/2024) e imputa a David Sánchez (27/11/2024).
  07/02/2025: renuncia al puesto. Juicio en la Audiencia Provincial de Badajoz del 28/05 al 09/06/2026.
  14/07/2026: sentencia (no firme): 9 años de inhabilitación especial por prevaricación (cooperador necesario); sin prisión.
    Gallardo (expresidente de la Diputación), 18 años de inhabilitación. Los 11 acusados, absueltos de tráfico de influencias.
    El nombramiento de 2017 está prescrito: la condena es por el cambio de nombre del puesto en 2022 sin funciones nuevas.
    Da por probado que vivía en Portugal desde 2021 y más de un año sin despacho fijo. Delito fiscal descartado y archivado.
  Recursos ante el TSJ de Extremadura: David Sánchez (08/10), Fiscalía (09/10, pidió siempre la absolución) y Gallardo (13/10).
  Reacciones: Gobierno (Elma Saiz) confía en que se constate su inocencia; PP (Feijóo) «el tiempo pone las cosas en su sitio»;
  Vox, como acusación popular, pidió 6 años de prisión.
"""
from _tu_dinero import *  # noqa: F401,F403

FN = "Audiencia Provincial de Badajoz, 14/07/2026 (no firme)"

scenes = [
    dict(id="gancho", fondo="calle", animo="curioso", footnote="Sentencia no firme: está recurrida", lines=[
        V("¿Qué ha pasado con el hermano de Pedro Sánchez?", "energia"),
        V("En un minuto y fácil.", "normal", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@fácil", "abierto", dur=0.4)],
       elements=[
        quien("piz", 300, 0, 0.75, "pensativo", entra="izq", acciones=[
            {"at": "@hermano", "mira": "david", "cara": "sorpresa"}, {"at": "@minuto", "mira": "camara", "pose": "senala_arriba"},
            {"at": "@fácil", "pose": "pulgar", "cara": "riendo", "salta": True}]),
        quien("david", 800, "@hermano", 0.72, "normal", entra="pop", acciones=[{"at": "@minuto", "mira": "piz"}]),
        rot("EL CASO DAVID SÁNCHEZ", 540, 480, "@hermano", 72, "amarillo", golpe=True),
        rot("EN 1 MINUTO", 540, 590, "@minuto", 84, "blanco", golpe=True),
    ]),
    dict(id="contrato", fondo="oficina", animo="alegre", trans="pan", footnote="Diputación de Badajoz, 2017", lines=[
        V("2017. La Diputación de Badajoz le contrata para la música de sus conservatorios.", "normal"),
        V("La preside Miguel Ángel Gallardo.", "normal", 0.1),
    ], camara=[plano(0, "general", dur=0), plano("@Gallardo", "abierto", dur=0.4)],
       elements=[
        quien("gallardo", 290, 0, 0.72, "normal", entra="izq", pose="sostiene", objeto={"tipo": "contrato", "titulo": "CONTRATO", "hojas": 1},
              acciones=[{"at": "@contrata", "salta": True, "cara": "riendo"}, {"at": "@conservatorios", "objeto": None, "pose": "pulgar"},
                        {"at": "@Gallardo", "mira": "camara"}]),
        quien("david", 790, 0, 0.72, "ilusionado", entra="der", acciones=[
            {"at": "@contrata", "pose": "arriba", "cara": "riendo"}, {"at": "@música", "salta": True}]),
        rot("2017", 540, 470, "@2017", 120, "amarillo", golpe=True, out="@Gallardo"),
        rot("PRESIDENTE: GALLARDO", 540, 470, "@Gallardo", 70, "blanco", golpe=True),
    ]),
    dict(id="denuncia", fondo="oficina", animo="tension", trans="iris", footnote="Denuncia de 2024 · jueza Beatriz Biedma", lines=[
        V("2024. Manos Limpias le denuncia: dice que la plaza se hizo a dedo para él.", "sorpresa"),
        V("Una jueza empieza a investigar.", "remate", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@jueza", "medio", "jueza", 0.3, aire=220)],
       elements=[
        quien("david", 290, 0, 0.72, "normal", entra="nada", acciones=[
            {"at": "@denuncia", "take": True, "cara": "susto"}, {"at": "@dedo", "cara": "preocupado"}, {"at": "@investigar", "tiembla": True}]),
        obj("contrato", 780, 760, "@denuncia", 0.7, entra="cae", props={"titulo": "DENUNCIA", "hojas": 1}, sfx="papel",
            acciones=[{"at": "@jueza", "sale": "der"}]),
        quien("jueza", 1300, "@jueza-0.3", 0.75, "serio", entra="nada", acciones=[{"at": "@jueza", "x": 790, "dur": 0.7},
                                                                              {"at": "@investigar", "pose": "senala"}]),
        rot("«A DEDO»", 600, 480, "@dedo", 110, C, golpe=True, out="@jueza"),
        rot("INVESTIGACIÓN", 600, 480, "@jueza", 84, "amarillo", golpe=True),
    ]),
    dict(id="portugal", fondo={"tipo": "playa", "variante": "ria"}, animo="comico", trans="pan", footnote=FN, lines=[
        V("El juicio da por probado que vivía en Portugal y pasó más de un año sin despacho fijo.", "normal"),
        V("Lo de Hacienda se archivó.", "normal", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@despacho", "abierto", dur=0.4)],
       elements=[
        quien("david", 540, 0, 0.75, "normal", entra="izq", acciones=[
            {"at": "@Portugal", "mira": "der", "cara": "normal"}, {"at": "@despacho", "pose": "encoge", "cara": "confundido"},
            {"at": "@Hacienda", "mira": "camara"}, {"at": "@archivó", "salta": True, "cara": "riendo"}]),
        rot("VIVÍA EN PORTUGAL", 540, 470, "@Portugal", 80, "amarillo", golpe=True, out="@Hacienda"),
        rot("+1 AÑO SIN DESPACHO", 540, 580, "@despacho", 70, "blanco", golpe=True, out="@Hacienda"),
        rot("HACIENDA: ARCHIVADO", 540, 470, "@archivó", 76, "verde", golpe=True),
    ]),
    dict(id="sentencia", fondo="rayos", animo="tension", musica="corte", trans="iris", footnote=FN, lines=[
        V("Julio de 2026: condenado a nueve años sin poder ocupar un cargo público.", "sorpresa"),
        V("No entra en prisión. Gallardo, 18 años.", "normal", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@prisión", "abierto", dur=0.4)],
       elements=[
        quien("david", 300, 0, 0.75, "normal", entra="pop", acciones=[
            {"at": "@condenado", "take": True, "cara": "susto"}, {"at": "@público", "cara": "triste", "pose": "caidos"},
            {"at": "@prisión", "mira": "camara", "cara": "pensativo"}]),
        quien("gallardo", 800, "@Gallardo-0.2", 0.72, "normal", entra="pop", acciones=[{"at": "@18", "take": True, "cara": "triste"}]),
        rot("9 AÑOS INHABILITADO", 540, 470, "@nueve", 76, C, golpe=True),
        rot("SIN PRISIÓN", 540, 580, "@prisión", 80, "blanco", golpe=True),
        rot("GALLARDO: 18 AÑOS", 540, 690, "@18", 70, C, golpe=True),
    ]),
    dict(id="porque", fondo="oficina", animo="curioso", trans="pan", footnote="Condena por prevaricación · " + FN, lines=[
        V("¿Por el contrato de 2017? No, eso prescribió.", "normal"),
        V("Por cambiarle el nombre al puesto en 2022 sin funciones nuevas. Del tráfico de influencias, absueltos.", "normal", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@absueltos", "medio", "profe", 0.3, aire=200)],
       elements=[
        quien("profe", 300, 0, 0.75, "normal", entra="izq", pose="senala_arriba", acciones=[
            {"at": 0.9, "mira": "camara", "cara": "pensativo"}, {"at": "@2017", "salta": True}, {"at": "@prescribió", "pose": "senala", "cara": "serio"}, {"at": "@nombre", "mira": "contrato"},
            {"at": "@nuevas", "cara": "pensativo"}, {"at": "@absueltos", "pose": "pulgar", "mira": "camara"}]),
        obj("contrato", 780, 780, "@nombre", 0.7, id="contrato", entra="pop", props={"titulo": "NUEVO NOMBRE", "hojas": 1}, sfx="papel"),
        rot("2017: PRESCRITO", 600, 470, "@prescribió", 80, "blanco", golpe=True, out="@nombre"),
        rot("2022: CAMBIO DE NOMBRE", 600, 470, "@nombre", 70, "amarillo", golpe=True, out="@absueltos"),
        rot("TRÁFICO DE INFLUENCIAS:", 600, 460, "@absueltos", 60, "verde", golpe=True),
        rot("ABSUELTOS", 600, 560, "@absueltos", 90, "verde", golpe=True),
    ]),
    dict(id="recurso", fondo="oficina", animo="tension", trans="iris", footnote="Recursos al TSJ de Extremadura, octubre de 2026 (EFE)", lines=[
        V("Ojo: no es firme. Han recurrido él, Gallardo y la Fiscalía, que pidió la absolución.", "normal"),
        V("Decide el Tribunal Superior de Extremadura.", "normal", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@Extremadura", "abierto", dur=0.4)],
       elements=[
        quien("david", 250, 0, 0.62, "normal", entra="nada", objeto={"tipo": "contrato", "titulo": "RECURSO", "hojas": 1}, pose="sostiene",
              acciones=[{"at": "@recurrido", "salta": True}]),
        quien("gallardo", 540, "@Gallardo", 0.62, "normal", entra="pop", acciones=[{"at": "@recurrido", "salta": True}]),
        quien("profe", 830, "@Fiscalía", 0.62, "serio", entra="pop", acciones=[{"at": "@absolución", "pose": "senala_arriba"}, {"at": "@recurrido", "salta": True}]),
        rot("NO ES FIRME", 540, 470, "@firme", 100, "amarillo", golpe=True, out="@Decide"),
        rot("DECIDE EL TSJ", 540, 470, "@Tribunal", 90, "blanco", golpe=True),
    ]),
    dict(id="partidos", fondo="calle", animo="curioso", trans="pan", footnote="Elma Saiz (Gobierno) · Feijóo (PP) · Vox en el juicio", lines=[
        V("El Gobierno confía en su inocencia.", "normal"),
        V("El PP: «el tiempo pone las cosas en su sitio». Vox, que acusaba, pedía seis años de cárcel.", "normal", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@cárcel", "abierto", dur=0.4)],
       elements=[
        quien("sanchez", 230, "@Gobierno", 0.6, "normal", entra="pop", acciones=[{"at": "@inocencia", "pose": "pulgar"}]),
        quien("feijoo", 540, "@PP", 0.6, "normal", entra="pop", acciones=[{"at": "@sitio", "pose": "senala_arriba"}]),
        quien("abascal", 850, "@Vox", 0.6, "normal", entra="pop", acciones=[{"at": "@cárcel", "pose": "senala"}]),
        rot("GOBIERNO: «INOCENCIA»", 540, 470, "@Gobierno", 66, "blanco", golpe=True, out="@PP"),
        rot("PP: «EL TIEMPO PONE", 540, 460, "@PP", 62, "blanco", golpe=True, out="@Vox"),
        rot("LAS COSAS EN SU SITIO»", 540, 550, "@PP", 62, "blanco", golpe=True, out="@Vox"),
        rot("VOX PEDÍA 6 AÑOS DE CÁRCEL", 540, 470, "@Vox", 56, "blanco", golpe=True),
    ]),
    dict(id="final", fondo="calle", animo="final", trans="iris", footnote="Presunción de inocencia hasta sentencia firme", lines=[
        V("¿Qué opinas? Te leemos.", "normal"),
        V("Y síguenos para saber qué decide el tribunal.", "energia", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@síguenos", "abierto", dur=0.4)],
       elements=[
        quien("piz", 300, 0, 0.72, "normal", entra="nada", acciones=[
            {"at": "@opinas", "mira": "camara", "cara": "pensativo"}, {"at": "@leemos", "pose": "senala", "cara": "ilusionado"},
            {"at": "@síguenos", "pose": "saluda", "cara": "riendo"}, {"at": "@tribunal", "salta": True}]),
        quien("pizon", 790, 0, 0.72, "normal", entra="nada", acciones=[{"at": "@opinas", "cara": "pensativo"}, {"at": "@tribunal", "take": True}]),
        rot("¿QUÉ OPINAS?", 540, 470, "@opinas", 100, "amarillo", golpe=True, out="@síguenos-0.4"),
        rot("SÍGUENOS", 540, 470, "@síguenos", 110, "amarillo", fx=[{"at": "@tribunal", "do": "latir"}]),
    ]),
]

if __name__ == "__main__":
    episodio("caso_hermano", "El caso del hermano de Sánchez", scenes,
             {"t": 3.0, "titulo": "El caso del hermano de Sánchez", "capitulo": None},
             ["Audiencia Provincial de Badajoz: sentencia de 14/07/2026 (no firme), vía EFE y Europa Press",
              "Recursos ante el TSJ de Extremadura (EFE, 8, 9 y 13/10/2026)"],
             ("⚖️ El caso del hermano de Pedro Sánchez, explicado fácil\n"
              "🎻 2017: la Diputación de Badajoz le contrata para los conservatorios\n"
              "📄 2024: denuncia de Manos Limpias y una jueza investiga\n"
              "🏛️ Julio 2026: 9 años de inhabilitación por prevaricación, sin prisión · Gallardo, 18\n"
              "🔎 2017 prescrito · condena por el cambio de puesto de 2022 · absueltos de tráfico de influencias\n"
              "⏳ No es firme: han recurrido él, Gallardo y la Fiscalía\n"
              "💬 ¿Qué opinas?\n"
              "🔔 Síguenos para saber qué decide el tribunal · 📚 Fuentes en comentarios"),
             ("📚 Audiencia Provincial de Badajoz, sentencia del 14/07/2026 (no firme): 9 años de inhabilitación especial por prevaricación "
              "como cooperador necesario; Gallardo, 18; absolución por tráfico de influencias; el nombramiento de 2017 está prescrito. Recursos ante "
              "el TSJ de Extremadura de David Sánchez (08/10), la Fiscalía (09/10) y Gallardo (13/10), según EFE. Delito fiscal descartado y archivado. "
              "Rige la presunción de inocencia hasta sentencia firme. ¿Ves un error? Dínoslo."),
             ["#PizarraPública", "#DavidSánchez", "#Justicia", "#Badajoz", "#ExplicadoFácil", "#Política"],
             series_tag="EXPLICADO FÁCIL")
