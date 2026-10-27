#!/usr/bin/env python3
"""«¿Qué ha destapado Alvise?» (27/10/2026). Verificador: lo que se le atribuye, caso por caso, con su sello.
Mundo dibujado: periódico de 2020, mapa del Estrecho hasta Marruecos, casa de Carmena, juzgado y marcador final.

Idea de un seguidor («los casos de corrupción que ha destapado Alvise»), aprobada por joel el 27/10/2026.
Guion y fuentes: /mnt/project-files/insta/guiones/alvise_destapes.md
  Caso Koldo: lo publicó Vozpópuli el 14/04/2020, según su entonces director, Álvaro Nieto (X, nov. 2024; The Objective
    24/11/2024), que corrigió a quien se lo atribuía a Alvise.
  Bank of Africa: en junio de 2025 acusó a Sánchez y Begoña Gómez de cobrar comisiones en cuentas en Marruecos, sin
    pruebas documentales concluyentes (El Distrito 19/06/2025). No consta confirmación: SIN CONFIRMAR.
  Carmena: 31/03/2020 tuiteó que tenía un respirador privado en casa; falso; condena a pagar 5.000 € (08/03/2023),
    confirmada el 25/10/2024 (Maldita 06/05/2026).
  Newtral: condenado en 2023 por insinuar irregularidades de la empresa de Ana Pastor; el Supremo anuló la condena:
    sus afirmaciones «se apoyan en una base fáctica adecuada» (eldiario.es 09/02/2024).
  Le han ganado juicios civiles: Carmena (honor), Ana Pastor (intimidad, 7.000 €, Supremo jun. 2024), Ábalos (honor,
    2.ª condena confirmada por el Supremo, EFE vía Público 09/10/2026).
  Seis causas abiertas en el Supremo (financiación de SALF, acoso a la fiscal Gisbert, acoso y revelación de secretos a
    Junco y Solier, amenazas al alcalde de Algeciras, PCR falsa atribuida a Illa, desórdenes); ninguna condena penal
    (El Constitucional 05/10/2026).
"""
from _mundo import *  # noqa: F401,F403

RE = "estrecho"
MAD_E = P(RE, -3.7, 40.4)
MARR = P(RE, -6.3, 34.3)


def mapa_e(at=0.0, dibujo=1.3, acciones=()):
    return mapa(RE, at, dibujo, acciones=acciones)


scenes = [
    # 1 · GANCHO: Piz recibe el encargo del seguidor y saca la lupa; Alvise posa con su megáfono de pizarra
    dict(id="gancho", fondo="calle", animo="curioso", footnote="Petición de un seguidor en comentarios", lines=[
        V("Un seguidor nos pide: «los casos de corrupción que ha destapado Alvise».", "energia"),
        V("Lo hemos comprobado. Uno por uno.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@Alvise", "medio", "alvise", 0.5, aire=260),
               plano("@comprobado", "medio", "piz", 0.5, aire=260), plano("@Uno", "general", [540, 1000], 0.4, zoom=1.06)],
       elements=[
        obj("movil", 300, 820, 0, 0.5, entra="pop", sfx="pop", out="@comprobado",
            props={"pantalla": "sms", "remite": "SEGUIDOR", "lineas": ["¿Y los casos", "que destapó", "Alvise?"], "suena": True}),
        quien("piz", 300, 0, 0.58, "pensativo", entra="nada", acciones=[
            {"at": "@pide", "pose": "sostiene", "cara": "sorpresa"}, {"at": "@comprobado", "cara": "serio", "mira": "camara", "pose": "jarras"},
            {"at": "@Uno", "pose": "senala", "cara": "ilusionado"}]),
        quien("alvise", 1300, "@Alvise", 0.58, "ilusionado", entra="nada", acciones=[
            {"at": "@Alvise", "x": 790, "dur": 0.6}, {"at": "@destapado", "pose": "arriba", "cara": "riendo", "mira": "camara"},
            {"at": "@comprobado", "cara": "sorpresa", "mira": "izq"}]),
        obj("lupa", 380, 920, "@comprobado", 0.6, entra="pop", sfx="pop"),
        rot("¿QUÉ HA DESTAPADO ALVISE?", 540, 400, "@destapado", 84, "amarillo", golpe=True),
    ]),
    # 2 · EL CASO KOLDO: el periódico de 2020 se dibuja con su fecha
    dict(id="koldo", fondo={"tipo": "plano", "color": (28, 52, 110)}, animo="curioso", trans="papel",
         footnote="Álvaro Nieto, exdirector de Vozpópuli (X, 22/11/2024)", lines=[
        V("Uno: el caso Koldo. Mucha gente se lo atribuye a él.", "normal"),
        V("Pero lo publicó el periódico Vozpópuli, en abril de 2020, según su director de entonces.", "normal", 0.15),
    ], camara=[plano(0, "general", [540, 900], 0), plano("@publicó", "general", [540, 760], 0.6, zoom=1.1),
               plano("@director", "general", [540, 900], 0.5)],
       elements=[
        rot("1 · CASO KOLDO", 540, 400, 0, 96, "amarillo", golpe=True, out="@publicó"),
        quien("alvise", 790, 0.1, 0.48, "ilusionado", y=1500, entra="pop", acciones=[
            {"at": "@atribuye", "pose": "pulgar", "cara": "riendo"}, {"at": "@Pero", "cara": "sorpresa", "mira": "izq", "pose": "normal"}]),
        obj("documento", 540, 700, "@publicó", 0.85, id="periodico", entra="nada", dibujo=1.0, sfx="papel", props={
            "titulo": "VOZPÓPULI", "subtitulo": "14 de abril de 2020",
            "articulos": [{"id": "k", "titulo": "Primera noticia", "lineas": ["sobre Koldo García"]}]},
            acciones=[{"at": "@abril", "props": {"resalta": ["k"]}}]),
        quien("piz", -200, "@publicó", 0.42, "pensativo", y=1500, entra="nada", acciones=[
            {"at": "@publicó", "x": 230, "dur": 0.6}, {"at": "@abril", "pose": "senala", "mira": "der"}]),
        sello("NO FUE EL PRIMERO", "naranja", 1180, "@director"),
    ]),
    # 3 · BANK OF AFRICA: mapa del Estrecho hasta Marruecos; la flecha de la acusación y el sello
    dict(id="marruecos", fondo="mar_mapa", limites=LIM, animo="tension", trans="zoom", footnote="El Distrito 19/06/2025", lines=[
        V("Dos: en 2025 acusó a Sánchez y a Begoña Gómez de cobrar comisiones en un banco de Marruecos.", "normal"),
        V("No presentó pruebas concluyentes. Y nadie lo ha confirmado.", "remate", 0.15),
    ], camara=[zoom(0, MAD_E, 1.1, 0), zoom("@Marruecos", MARR, 2.0, 1.0), zoom("@pruebas", P(RE, -5.0, 37.0), 1.4, 0.6)],
       elements=[
        mapa_e(0, 1.2, acciones=[{"at": "@Marruecos", "props": {"resalta": ["Morocco"]}, "sfx": "pop"}]),
        rot("2 · BANCO EN MARRUECOS", 540, 400, 0, 72, "amarillo", golpe=True, out="@pruebas"),
        obj("chincheta", MARR[0], MARR[1], "@banco", 0.14, entra="cae"),
        obj("saco", MARR[0] + 90, MARR[1] - 30, "@banco+0.2", 0.16, entra="cae", sfx="kaching"),
        quien("alvise", MAD_E[0], 0.3, 0.12, "serio", y=MAD_E[1] + 20, entra="cae", acciones=[
            {"at": "@acusó", "pose": "senala", "cara": "enfado"}, {"at": "@pruebas", "pose": "encoge", "cara": "normal"}]),
        sello("SIN CONFIRMAR", "naranja", 1320, "@confirmado"),
    ]),
    # 4 · CARMENA: el bulo del respirador; casa de Carmena y la jueza con la multa
    dict(id="carmena", fondo="calle", animo="comico", trans="barrido", footnote="Maldita.es 06/05/2026", lines=[
        V("Tres: en 2020 dijo que Manuela Carmena tenía un respirador privado en casa.", "normal"),
        V("Era falso. Le condenaron a pagarle 5.000 euros, y la condena se confirmó en 2024.", "normal", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@falso", "general", [540, 980], 0.4, zoom=1.08),
               plano("@condenaron", "general", [540, 1000], 0.5)],
       elements=[
        rot("3 · EL RESPIRADOR", 540, 400, 0, 96, "amarillo", golpe=True, out="@falso"),
        edif("casa", 300, 0, 0.55, entra="nada", dibuja=0.7, acciones=[{"at": "@falso", "cara": "enfado"}]),
        quien("alvise", 760, 0.2, 0.55, "burla", entra="pop", acciones=[
            {"at": "@respirador", "pose": "senala_izq", "mira": "izq"}, {"at": "@falso", "cara": "susto", "take": True},
            {"at": "@5.000", "cara": "triste", "pose": "caidos"}]),
        obj("bocadillo", 760, 640, "@respirador", 0.6, entra="pop", sfx="pop", out="@falso",
            props={"lineas": ["«Respirador", "privado en casa»"]}),
        sello("BULO", "rojo", 900, "@falso", out="@condenaron"),
        obj("contador", 540, 520, "@5.000", 0.75, hud=True, entra="pop", sfx="kaching",
            props={"valor": 5000, "sufijo": " €", "ancho": 700}),
        quien("jueza", -200, "@condenaron", 0.45, "serio", y=1500, entra="nada", hud=True, acciones=[
            {"at": "@condenaron", "x": 200, "dur": 0.5}, {"at": "@confirmó", "pose": "senala"}]),
        sello("CONDENA CONFIRMADA", "rojo", 1650, "@2024", x=620),
    ]),
    # 5 · NEWTRAL: el giro; aquí el Supremo le da la razón
    dict(id="newtral", fondo={"tipo": "plano", "color": (34, 110, 70)}, animo="curioso", trans="iris",
         footnote="eldiario.es 09/02/2024", lines=[
        V("Pero ojo, no todo fue bulo. Insinuó irregularidades en Newtral, la empresa de Ana Pastor.", "normal"),
        V("Le condenaron, y el Supremo anuló esa condena en 2024: lo que dijo tenía una base adecuada en hechos.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 950], 0), plano("@Supremo", "general", [540, 900], 0.5, zoom=1.08),
               plano("@hechos", "general", [540, 950], 0.4)],
       elements=[
        rot("4 · NEWTRAL", 540, 400, 0, 96, "amarillo", golpe=True, out="@Supremo"),
        quien("piz", 300, 0, 0.5, "sorpresa", y=1500, entra="nada", acciones=[
            {"at": "@ojo", "pose": "senala_arriba", "mira": "camara"}, {"at": "@anuló", "cara": "sorpresa", "take": True},
            {"at": "@hechos", "cara": "pensativo", "pose": "piensa"}]),
        quien("alvise", 790, "@Insinuó", 0.5, "serio", y=1500, entra="pop", acciones=[
            {"at": "@condenaron", "cara": "triste"}, {"at": "@anuló", "cara": "riendo", "pose": "punos", "salta": True}]),
        obj("documento", 540, 720, "@Supremo", 0.75, entra="nada", dibujo=0.8, sfx="papel", hud=True, props={
            "titulo": "TRIBUNAL SUPREMO", "subtitulo": "Febrero de 2024",
            "articulos": [{"id": "a", "titulo": "Fallo", "lineas": ["Se anula la condena:", "había base en hechos"]}]},
            acciones=[{"at": "@base", "props": {"resalta": ["a"]}}]),
        sello("LE DIERON LA RAZÓN", "verde", 1020, "@hechos"),
    ]),
    # 6 · EL JUZGADO: quién le ha ganado y qué tiene pendiente
    dict(id="juzgado", fondo={"tipo": "plano", "color": (28, 52, 110)}, animo="tension", trans="corte",
         footnote="Maldita 06/05/2026 · Público 09/10/2026 · El Constitucional 05/10/2026", lines=[
        V("En los juzgados, tres personas le han ganado por su honor o su intimidad: Carmena, Ana Pastor y Ábalos.", "normal"),
        V("Y tiene seis causas abiertas en el Supremo: financiación de su partido, acoso a una fiscal, una PCR falsa de Illa…", "normal", 0.15),
        V("Investigado, sí. Condenado penalmente, ninguna vez.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 900], 0), plano("@seis", "general", [540, 820], 0.6, zoom=1.06),
               plano("@Investigado", "general", [540, 900], 0.5, zoom=1.04)],
       elements=[
        obj("checklist", 540, 640, 0.2, 0.75, hud=True, entra="pop", sfx="papel", out="@seis",
            props={"items": ["Carmena: honor", "Ana Pastor: intimidad", "Ábalos: honor"], "marcas": [None, None, None]},
            acciones=[{"at": "@Carmena", "props": {"marcas": ["no", None, None]}},
                      {"at": "@Pastor", "props": {"marcas": ["no", "no", None]}},
                      {"at": "@Ábalos", "props": {"marcas": ["no", "no", "no"]}}]),
        obj("contador", 540, 520, "@seis", 0.75, hud=True, entra="pop", sfx="golpe", out="@Investigado",
            props={"valor": 6, "sufijo": " CAUSAS ABIERTAS", "ancho": 900}),
        obj("documento", 540, 900, "@financiación", 0.7, hud=True, entra="nada", dibujo=0.8, sfx="papel", out="@Investigado",
            props={"titulo": "SUPREMO", "subtitulo": "Algunas causas", "articulos": [
                {"id": "f", "titulo": "Financiación", "lineas": ["100.000 € de un empresario"]},
                {"id": "a", "titulo": "Acoso", "lineas": ["a una fiscal"]},
                {"id": "p", "titulo": "PCR", "lineas": ["falsa atribuida a Illa"]}]},
            acciones=[{"at": "@financiación", "props": {"resalta": ["f"]}}, {"at": "@fiscal", "props": {"resalta": ["a"]}},
                      {"at": "@PCR", "props": {"resalta": ["p"]}}]),
        quien("alvise", 540, "@Investigado-0.2", 0.55, "serio", y=1420, entra="abajo", acciones=[
            {"at": "@Condenado", "pose": "cruzados", "mira": "camara"}]),
        sello("INVESTIGADO", "naranja", 560, "@Investigado", x=300),
        sello("0 CONDENAS PENALES", "verde", 760, "@ninguna", x=640),
    ]),
    # 7 · VEREDICTO: Piz cierra la lupa; lo que hemos encontrado
    dict(id="veredicto", fondo="salon", animo="final", trans="iris", footnote="Revisión de Pizarra Pública, 27/10/2026", lines=[
        V("Resumen: grandes casos de corrupción destapados primero por él… no hemos encontrado ninguno.", "normal"),
        V("Si conoces uno, pásanos la fuente y lo revisamos.", "normal", 0.15),
        V("¿Destapa o difunde? Te leo en comentarios. Y síguenos para más verificaciones.", "energia", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@ninguno", "medio", "piz", 0.5, aire=280),
               plano("@Destapa", "general", [540, 1000], 0.5), plano("@síguenos", "medio", "piz", 0.5, aire=300)],
       elements=[
        quien("piz", 540, 0, 0.62, "pensativo", entra="nada", acciones=[
            {"at": "@Resumen", "pose": "sostiene"}, {"at": "@ninguno", "cara": "serio", "pose": "encoge", "mira": "camara"},
            {"at": "@fuente", "pose": "senala", "cara": "ilusionado"}, {"at": "@Destapa", "pose": "senala_izq", "mira": "izq", "cara": "pensativo"},
            {"at": "@difunde", "pose": "senala", "mira": "der"}, {"at": "@síguenos", "pose": "saluda", "cara": "riendo"}]),
        obj("lupa", 640, 980, 0, 0.55, entra="nada"),
        etq("¿DESTAPA?", 260, 880, "@Destapa", "verde", 0.7, out="@síguenos"),
        etq("¿DIFUNDE?", 820, 880, "@difunde", "rojo", 0.7, out="@síguenos"),
        rot("CASOS DESTAPADOS PRIMERO: 0", 540, 430, "@ninguno", 76, "amarillo", golpe=True, out="@Destapa"),
        rot("¿TÚ QUÉ CREES?", 540, 430, "@Destapa", 110, "amarillo", golpe=True, out="@síguenos-0.3"),
        rot("SÍGUENOS", 540, 430, "@síguenos", 110, "amarillo"),
    ]),
]

if __name__ == "__main__":
    episodio("alvise_destapes", "¿Qué ha destapado Alvise?", scenes,
             {"t": 3.5, "titulo": "¿Qué ha destapado Alvise?", "capitulo": None},
             ["Álvaro Nieto, exdirector de Vozpópuli (X, 22/11/2024; The Objective 24/11/2024): el caso Koldo se publicó el 14/04/2020",
              "El Distrito (19/06/2025): acusación de Alvise sobre el Bank of Africa, sin pruebas documentales concluyentes",
              "Maldita.es (06/05/2026): bulo del respirador de Carmena, condena de 5.000 € (2023) confirmada el 25/10/2024",
              "eldiario.es (09/02/2024): el Supremo anula su condena por lo de Newtral",
              "Supremo (06/2024): 7.000 € por la foto de Ana Pastor (intimidad)",
              "EFE vía Público (09/10/2026): segunda condena civil por el honor de Ábalos",
              "El Constitucional (05/10/2026): seis causas abiertas en el Supremo, ninguna condena penal",
              "Personajes dibujados como pizarras, sin caricatura"],
             ("🔎 Nos pedís «los casos de corrupción que ha destapado Alvise». Lo hemos comprobado\n"
              "📰 Caso Koldo: lo publicó Vozpópuli en abril de 2020\n"
              "🇲🇦 «Comisiones en un banco de Marruecos»: sin confirmar\n"
              "❌ Respirador de Carmena: bulo, 5.000 € de condena\n"
              "✅ Newtral: el Supremo le dio la razón\n"
              "⚖️ 6 causas abiertas en el Supremo, 0 condenas penales\n"
              "💬 ¿Destapa o difunde? ¿Conoces un caso que se nos escape? Pásanos la fuente 👇\n"
              "🔔 Síguenos · 📚 Fuentes en comentarios"),
             "📚 Fuentes: Álvaro Nieto (exdirector de Vozpópuli) · El Distrito 19/06/2025 · Maldita 06/05/2026 · eldiario.es 09/02/2024 · "
             "EFE vía Público 09/10/2026 · El Constitucional 05/10/2026. ¿Ves un error? Dínoslo.",
             ["#Alvise", "#SALF", "#verificación", "#bulos", "#29N", "#elecciones", "#pizarrapublica"],
             series_tag="VERDAD O BULO")
