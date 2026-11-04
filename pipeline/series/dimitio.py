#!/usr/bin/env python3
"""«Dimitió» (cap. 2 de «¿Debe dimitir Puente?»), para el jueves 5/11/2026 a las 20:00.
Óscar Puente dimite el martes 3/11 al acabar su comparecencia por el accidente de Urda. Tema político tras una
tragedia: tono sobrio, sin gags sobre el accidente ni las víctimas, el choque no se dibuja, lazo de luto.

Aprobado por joel el 4/11/2026 21:21 UTC («Has los vídeos», propuesta 1 de /mnt/project-files/insta/guiones/propuestas_5nov.md).
Fuentes:
  The Objective 3/11/2026: dimite al final de una comparecencia de más de cuatro horas, la cuarta desde Urda; renuncia
    a encabezar la lista del PSOE por Valladolid; «un ministro no puede continuar en su puesto con un accidente de este
    tipo»; dice que lo decidió el 28/10 y lo retrasó para dejar aprobadas las primeras medidas; Moncloa había descartado
    su salida ese mediodía; todos los grupos menos PSOE y Bildu pedían su dimisión; Sánchez en X: «Políticos como él
    dignifican a nuestro país»; Adamuz (enero) 46 muertos.
  Infobae/EFE 3-4/11/2026: «no puede continuar con dos accidentes de esta gravedad en menos de un año»; 69 fallecidos.
  El Español directo 4/11/2026: Cuerpo asume Transportes de forma transitoria hasta el 29N; Vox: Cuerpo es un «fusible».
  The Objective 4/11/2026 (cita a ABC): Cuerpo destituye al presidente de Adif, Luis Pedro Marco de la Peña.
  elDiario.es enero 2026: Feijóo pide la dimisión de Puente por Adamuz.
"""
from _mundo import *  # noqa: F401,F403

R = "espana"
MAD = P(R, -3.70, 40.42)
URDA = P(R, -3.71, 39.41)
ADAMUZ = P(R, -4.52, 38.03)
VALLA = P(R, -4.72, 41.65)
NOCHE_AZUL = (28, 40, 70)
GRIS_LUTO = (210, 212, 218)
F_TO = "The Objective, 3/11/2026"


def bocata(lineas, at, out=None, x=540, y=520, scale=0.7, cola=(-1, 1)):
    d = obj("bocadillo", x, y, at, scale, hud=True, entra="pop", sfx="pop", props={"lineas": lineas, "cola": cola})
    if out:
        d["out"] = out
    return d


scenes = [
    # 1 · GANCHO: a mediodía no, por la noche sí
    dict(id="gancho", fondo={"tipo": "plano", "color": NOCHE_AZUL}, animo="tension", footnote=F_TO,
         lines=[
        V("A mediodía, Moncloa decía que no se iba. Por la noche, Óscar Puente ya había dimitido.", "intriga"),
        V("Esto es lo que pasó en el Congreso.", "remate", 0.2),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@noche", "medio", "puente", 0.4, aire=260),
               plano("@Esto", "general", [540, 1000], 0.5)],
       elements=[
        quien("puente", 540, 0, 0.6, "serio", entra="nada", acciones=[
            {"at": "@Moncloa", "pose": "cruzados"}, {"at": "@noche", "pose": "manos_juntas", "cara": "triste", "mira": "camara"},
            {"at": "@dimitido", "pose": "encoge"}]),
        obj("reloj", 230, 600, 0.2, 0.45, hud=True, entra="pop", sfx="pop", out="@noche"),
        rot("MEDIODÍA: «NO»", 540, 440, 0.1, 90, "blanco", out="@noche"),
        rot("NOCHE: DIMITE", 540, 440, "@noche", 100, "rojo", golpe=True, out="@Esto"),
        edif("congreso", 540, "@Esto", 0.42, entra="nada", dibuja=0.6),
        rot("MARTES 3 · CONGRESO", 540, 440, "@Esto", 70, "amarillo"),
        obj("lazo", 960, 220, 0, 0.3, hud=True, entra="pop"),
    ]),
    # 2 · LA RAZÓN: dos accidentes en un año (mapa, sobrio)
    dict(id="razon", fondo="mar_mapa", limites=LIM, animo="triste", trans="iris",
         footnote="Infobae/EFE 3/11 · The Objective 3/11/2026", lines=[
        V("Más de cuatro horas de comparecencia. Y al final, esta frase:", "sobrio"),
        V("«Un ministro no puede continuar con dos accidentes de esta gravedad en menos de un año».", "sobrio", 0.2),
        V("Adamuz, en enero: 46 muertos. Urda, en octubre: 69.", "sobrio", 0.2),
    ], camara=[zoom(0, MAD, 1.0, 0), zoom("@Adamuz", ADAMUZ, 1.8, 0.9), zoom("@Urda", URDA, 1.8, 0.9), zoom("@69", MAD, 1.15, 0.8)],
       elements=[
        mapa(R, 0, 1.2, acciones=[{"at": "@Adamuz", "props": {"resalta": ["Córdoba"]}}, {"at": "@Urda", "props": {"resalta": ["Córdoba", "Toledo"]}}]),
        obj("reloj", 540, 520, 0.2, 0.5, hud=True, entra="pop", sfx="pop", out="@frase"),
        rot("+4 HORAS", 540, 440, 0.3, 90, "blanco", out="@frase"),
        obj("documento", 540, 700, "@frase", 0.78, hud=True, entra="nada", dibujo=0.7, sfx="papel", out="@Adamuz", props={
            "titulo": "PUENTE:", "subtitulo": "3/11/2026", "ancho": 820,
            "articulos": [{"id": "a", "titulo": "«NO PUEDE CONTINUAR»", "lineas": []},
                          {"id": "b", "titulo": "«DOS ACCIDENTES", "lineas": ["EN MENOS DE UN AÑO»"]}]},
            acciones=[{"at": "@continuar", "props": {"resalta": ["a"]}}, {"at": "@accidentes", "props": {"resalta": ["b"]}}]),
        obj("chincheta", ADAMUZ[0] + 6, ADAMUZ[1], "@Adamuz", 0.12, props={"diseno": "espana"}, entra="cae"),
        etq("ADAMUZ · ENERO · 46", 540, 520, "@46", "blanco", 0.62, hud=True),
        obj("chincheta", URDA[0] + 6, URDA[1], "@Urda", 0.12, props={"diseno": "espana"}, entra="cae"),
        etq("URDA · OCTUBRE · 69", 540, 620, "@69", "blanco", 0.62, hud=True),
        obj("lazo", 960, 220, 0, 0.3, hud=True, entra="nada"),
        sello("DECLARACIÓN", "azul", 1240, "@gravedad"),
    ]),
    # 3 · Y SE BAJA DE LAS LISTAS
    dict(id="listas", fondo="mar_mapa", limites=LIM, animo="curioso", trans="corte", footnote=F_TO, lines=[
        V("Y se baja de las listas: ya no será el número uno del PSOE por Valladolid."),
        V("Dice que lo decidió el día del accidente, pero esperó a dejar aprobadas las primeras medidas.", "normal", 0.15),
    ], camara=[zoom(0, VALLA, 2.0, 0), zoom("@decidió", MAD, 1.0, 0.8)],
       elements=[
        mapa(R, 0, 0, acciones=[{"at": "@Valladolid", "props": {"resalta": ["Valladolid"]}}]),
        obj("documento", 540, 760, 0.1, 0.72, hud=True, id="lista", entra="nada", dibujo=0.6, sfx="papel", props={
            "titulo": "LISTA DEL PSOE", "subtitulo": "VALLADOLID · 29N", "ancho": 700,
            "articulos": [{"id": "a", "titulo": "1 · ÓSCAR PUENTE", "lineas": []}]},
            acciones=[{"at": "@número", "props": {"resalta": ["a"]}}], fx=[{"at": "@uno", "do": "tachar"}]),
        rot("VALLADOLID", 540, 440, "@Valladolid", 80, "amarillo", out="@decidió"),
        quien("puente", 860, "@decidió-0.3", 0.5, "serio", entra="der", acciones=[
            {"at": "@accidente", "pose": "manos_juntas", "cara": "triste"}, {"at": "@esperó", "pose": "senala_arriba"},
            {"at": "@medidas", "pose": "normal", "mira": "camara"}]),
        obj("calendario", 230, 520, "@decidió", 0.3, hud=True, entra="crece", sfx="papel",
            props={"mes": "OCTUBRE 2026", "inicio": 3, "dias": 31, "marcados": [28], "colores": {28: "rojo"}}),
        obj("checklist", 540, 1060, "@medidas", 0.55, hud=True, entra="pop", sfx="pop",
            props={"items": ["INVESTIGACIÓN", "PRIMERAS MEDIDAS"], "marcas": ["si", "si"]}),
        sello("SU VERSIÓN", "azul", 1240, "@decidió"),
    ]),
    # 4 · QUIÉN MANDA AHORA
    dict(id="cuerpo", fondo="oficina", animo="tension", trans="barrido",
         footnote="El Español 4/11 · The Objective 4/11 (cita a ABC)", lines=[
        V("¿Y ahora quién lleva los trenes? Carlos Cuerpo, el vicepresidente primero, hasta el 29N."),
        V("Y según ABC, su primera decisión: destituir al presidente de Adif.", "remate", 0.2),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@Cuerpo", "medio", "cuerpo", 0.5, aire=280),
               plano("@destituir", "general", [540, 1000], 0.4)],
       elements=[
        obj("cartel", 540, 640, 0, 0.8, hud=True, entra="cae", sfx="golpe", out="@Cuerpo",
            props={"texto": "MINISTERIO DE TRANSPORTES", "color": "blanco", "tinta": "tinta"}),
        rot("¿QUIÉN LLEVA LOS TRENES?", 540, 420, 0, 70, "amarillo", out="@destituir"),
        quien("cuerpo", 540, "@Cuerpo", 0.58, "serio", entra="abajo", acciones=[
            {"at": "@vicepresidente", "pose": "jarras"}, {"at": "@29N", "pose": "senala_arriba"},
            {"at": "@destituir", "pose": "senala", "mira": "der", "cara": "serio"}]),
        etq("HASTA EL 29N", 540, 560, "@29N", "azul", 0.65, hud=True, out="@destituir"),
        obj("cartel", 540, 760, "@destituir", 0.62, hud=True, entra="cae", sfx="golpe",
            props={"texto": "ADIF: PRESIDENTE FUERA", "color": "rojo", "tinta": "blanco"}),
        sello("SEGÚN ABC", "naranja", 1240, "@ABC"),
    ]),
    # 5 · REACCIONES: un párrafo por lado
    dict(id="reacciones", fondo={"tipo": "plano", "color": NOCHE_AZUL}, animo="tension", trans="corte",
         footnote=F_TO + " · El Español 4/11/2026", lines=[
        V("Sánchez: «Políticos como él dignifican a nuestro país»."),
        V("El PP pedía su dimisión desde Adamuz, en enero.", "normal", 0.1),
        V("Y Vox dice que Cuerpo es solo un fusible, y que el que tiene que irse es Sánchez.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0)],
       elements=[
        quien("sanchez", 230, 0, 0.58, "serio", entra="pop", acciones=[{"at": "@dignifican", "pose": "manos_juntas"}]),
        bocata(["SÁNCHEZ:", "«dignifican", "a nuestro país»"], "@Políticos", x=430, y=560, out="@PP"),
        quien("feijoo", 540, "@PP", 0.58, "serio", entra="pop", acciones=[{"at": "@enero", "pose": "senala"}]),
        etq("PP: DESDE ENERO", 540, 600, "@Adamuz", "azul", 0.6, hud=True, out="@Vox"),
        quien("abascal", 850, "@Vox", 0.58, "enfado", entra="pop", acciones=[{"at": "@fusible", "pose": "senala_izq"}, {"at": "@Sánchez#2", "pose": "punos"}]),
        bocata(["VOX:", "Cuerpo, un «fusible»"], "@fusible", x=640, y=480, cola=(1, 1)),
        sello("DECLARACIONES", "azul", 1240, "@Políticos"),
    ]),
    # 6 · CIERRE: pregunta A/B y sigue a Piz
    dict(id="final", fondo="calle", animo="final", trans="iris", footnote=F_TO, lines=[
        V("Todos los grupos, menos PSOE y Bildu, le pedían que se fuera."),
        V("¿Dimisión por dignidad, o por cálculo electoral? A o B, te leo.", "energia", 0.15),
        V("Y sigue a Piz: quedan veinticuatro días.", "energia", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@sigue", "medio", "piz", 0.5, aire=300)],
       elements=[
        edif("congreso", 540, 0, 0.5, entra="nada", dibuja=0.6, out="@dignidad"),
        rot("TODOS MENOS PSOE Y BILDU", 540, 440, 0.1, 64, "blanco", out="@dignidad"),
        quien("piz", 540, "@dignidad-0.4", 0.62, "pensativo", entra="abajo", acciones=[
            {"at": "@dignidad", "pose": "senala_izq", "mira": "izq"}, {"at": "@cálculo", "pose": "senala", "mira": "der"},
            {"at": "@leo", "pose": "piensa", "mira": "camara", "cara": "normal"},
            {"at": "@sigue", "pose": "saluda", "cara": "ilusionado"}, {"at": "@veinticuatro", "pose": "senala_arriba"}]),
        etq("A · DIGNIDAD", 260, 700, "@dignidad", "azul", 0.58, hud=True, out="@sigue"),
        etq("B · CÁLCULO", 820, 700, "@cálculo", "rojo", 0.58, hud=True, out="@sigue"),
        rot("¿A O B?", 540, 360, "@leo", 110, "amarillo", golpe=True, out="@sigue-0.2"),
        obj("calendario", 830, 760, "@veinticuatro", 0.3, hud=True, entra="crece", sfx="papel",
            props={"mes": "NOVIEMBRE 2026", "inicio": 6, "dias": 30, "marcados": [29], "colores": {29: "rojo"}}),
        rot("SIGUE A PIZ", 540, 440, "@sigue", 110, "amarillo", fx=[{"at": "@días", "do": "latir"}]),
    ]),
]

if __name__ == "__main__":
    episodio("dimitio", "Dimitió", scenes,
             {"t": 1.4, "titulo": "Puente dimite", "capitulo": None},
             ["The Objective (3/11/2026): dimisión tras +4 h de comparecencia, se baja de la lista por Valladolid, Sánchez en X",
              "Infobae/EFE (3-4/11/2026): «dos accidentes de esta gravedad en menos de un año»; 69 fallecidos en Urda",
              "El Español (4/11/2026): Cuerpo asume Transportes hasta el 29N; Vox: «fusible»",
              "The Objective (4/11/2026), citando a ABC: destitución del presidente de Adif",
              "Tema político tras una tragedia: tono sobrio, sin gags sobre el accidente"],
             ("🚆 Óscar Puente dimite\n"
              "🕛 A mediodía Moncloa decía que no · por la noche, dimisión\n"
              "🖤 «No puede continuar con dos accidentes en menos de un año» (Adamuz 46 · Urda 69)\n"
              "🗳️ Se baja de las listas del PSOE por Valladolid\n"
              "🚄 Cuerpo se queda Transportes hasta el 29N · según ABC, fuera el presidente de Adif\n"
              "💬 ¿Dignidad (A) o cálculo electoral (B)? Te leo 👇\n"
              "🔔 Sigue a Piz · 📚 Fuentes en comentarios"),
             "📚 Fuentes: The Objective 3/11 y 4/11/2026 (Adif, citando a ABC) · Infobae/EFE 3/11 · El Español 4/11. "
             "¿Ves un error? Dínoslo.",
             ["#OscarPuente", "#Urda", "#Adif", "#CarlosCuerpo", "#29N", "#EleccionesGenerales", "#pizarrapublica"],
             series_tag="EXPLICADO FÁCIL")
