#!/usr/bin/env python3
"""«Se salta tres cumbres» (miércoles 11/11/2026, 15:00).
Pedido por joel el 8/11/2026 («adelante» al plan de la semana).
Fuente: EFE (Infobae, 6/11/2026), «El 29N altera la agenda exterior de Sánchez y no irá a tres cumbres de la próxima semana»:
  mié 11/11 Antalya (Turquía): jornada de líderes sobre acción climática de la COP31.
  jue 12/11 Dublín: Comunidad Política Europea. vie 13/11 Dublín: cumbre informal de los Veintisiete.
  Motivo («fuentes del Gobierno»): la cercanía de las elecciones; la campaña empieza a las 00:00 del 13.
  Precedente 2023: fue a la cumbre UE-CELAC de Bruselas en plena campaña, con un acto del PSOE en Huesca entre medias;
    canceló la cumbre MED9 de Split tras adelantar las elecciones.
  La cumbre extraordinaria de Bruselas (26-27/11) está en duda; el Gobierno «no descarta» que vaya.
  El artículo no dice quién le sustituye ni recoge reacción de PP o Vox.
"""
from _mundo import *  # noqa: F401,F403

R = "mundo"
MAD = P(R, -3.7, 40.4)
ANT = P(R, 30.7, 36.9)
DUB = P(R, -6.26, 53.35)
BRU = P(R, 4.35, 50.85)
EU = P(R, 10, 45)
F = "EFE (Infobae), 6/11/2026"

scenes = [
    # 1 · GANCHO
    dict(id="gancho", fondo="calle", animo="tension", footnote=F, lines=[
        V("Esta semana hay tres cumbres internacionales. Y Sánchez no va a ir a ninguna.", "intriga"),
        V("¿El motivo? El 29N.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@ninguna", "general", [540, 960], 0.4, zoom=1.08)],
       elements=[
        obj("calendario", 540, 560, 0, 0.62, hud=True, entra="pop", sfx="papel",
            props={"mes": "NOVIEMBRE 2026", "inicio": 6, "dias": 30, "marcados": [11, 12, 13], "colores": {11: "verde", 12: "azul", 13: "azul"}},
            fx=[{"at": "@ninguna", "do": "tachar"}]),
        quien("sanchez", 760, "@Sánchez-0.3", 0.5, "normal", entra="der", acciones=[
            {"at": "@ninguna", "pose": "cruzados", "mira": "camara"}, {"at": "@29N", "pose": "senala_arriba", "cara": "riendo"}]),
        quien("piz", 260, 0.2, 0.45, "pensativo", entra="izq", acciones=[{"at": "@ninguna", "cara": "sorpresa", "take": True}, {"at": "@motivo", "pose": "piensa"}]),
        rot("29N", 540, 960, "@29N", 140, "amarillo", golpe=True),
    ]),
    # 2 · EL MAPA: ANTALYA Y DUBLÍN
    dict(id="mapa", fondo="mar_mapa", limites=LIM, animo="aventura", trans="zoom", footnote=F, lines=[
        V("Hoy, en Antalya, Turquía: los líderes del mundo en la cumbre del clima."),
        V("El jueves, en Dublín, la Comunidad Política Europea. Y el viernes, también en Dublín, los veintisiete de la Unión.", "normal", 0.1),
    ], camara=[zoom(0, EU, 2.2, 0), zoom("@Antalya", ANT, 4.0, 0.9), zoom("@jueves", DUB, 4.0, 1.0), zoom("@viernes", EU, 2.4, 0.9)],
       elements=[
        mapa(R, 0, 1.4, lineas=[linea("r1", [(-3.7, 40.4), (14, 44), (30.7, 36.9)], "gris", 0.9, discontinua=True, ancho=5),
                                 linea("r2", [(-3.7, 40.4), (-8, 47), (-6.26, 53.35)], "gris", 0.9, discontinua=True, ancho=5)],
            acciones=[{"at": "@Antalya", "props": {"resalta": ["TUR"]}, "sfx": "pop"}, {"at": "@Dublín", "props": {"resalta": ["TUR", "IRL"]}, "sfx": "pop"}]),
        obj("chincheta", MAD[0], MAD[1], 0.4, 0.4, entra="cae", sfx="pop", props={"diseno": "espana"}),
        obj("sol", ANT[0] + 40, ANT[1] - 50, "@clima", 0.12, entra="pop", sfx="pop"),
        obj("bandera", DUB[0], DUB[1], "@Europea", 0.25, entra="crece", sfx="pop", props={"diseno": "ue"}),
        etq("11 · COP31", 540, 480, "@Antalya", "verde", 0.65, hud=True, out="@jueves"),
        etq("12 · COMUNIDAD POLÍTICA EUROPEA", 540, 480, "@jueves", "azul", 0.55, hud=True, out="@viernes"),
        etq("13 · LOS 27", 540, 480, "@viernes", "azul", 0.65, hud=True),
        sello("NO VA", "rojo", 1240, "@Unión"),
    ]),
    # 3 · EL MOTIVO
    dict(id="motivo", fondo="oficina", animo="curioso", trans="barrido", footnote=F, lines=[
        V("Según fuentes del Gobierno, es por la cercanía de las elecciones."),
        V("La campaña empieza a las doce de la noche del jueves al viernes.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@campaña", "general", [540, 940], 0.4, zoom=1.06)],
       elements=[
        sello("DECLARACIÓN", "azul", 520, "@Gobierno"),
        obj("reloj", 540, 720, "@campaña", 0.6, hud=True, entra="pop", sfx="pop"),
        rot("00:00 DEL 13", 540, 980, "@doce", 110, "amarillo", golpe=True),
        quien("piz", 860, 0.2, 0.45, "normal", y=1560, entra="der", acciones=[
            {"at": "@cercanía", "pose": "senala_izq", "mira": "izq"}, {"at": "@noche", "cara": "idea"}]),
        quien("pizon", 220, "@campaña", 0.42, "confundido", y=1560, entra="izq", acciones=[{"at": "@viernes", "pose": "encoge"}]),
    ]),
    # 4 · EL PRECEDENTE DE 2023
    dict(id="precedente", fondo="calle", animo="curioso", trans="papel", footnote=F, lines=[
        V("¿Y en 2023? En plena campaña sí fue a una cumbre en Bruselas, con un mitin en Huesca entre medias."),
        V("Y queda otra: Bruselas, el 26 y 27, tres días antes de votar. Esa, el Gobierno no la descarta.", "normal", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@queda", "general", [540, 960], 0.4, zoom=1.05)],
       elements=[
        etq("2023 · SÍ FUE", 540, 480, "@2023", "verde", 0.65, hud=True, out="@queda"),
        obj("avion", 300, 700, "@Bruselas", 0.5, hud=True, entra="izq", sfx="whoosh", out="@queda"),
        obj("microfono", 780, 720, "@mitin", 0.45, hud=True, entra="pop", sfx="pop", out="@queda"),
        obj("calendario", 540, 640, "@queda", 0.58, hud=True, entra="pop", sfx="papel",
            props={"mes": "NOVIEMBRE 2026", "inicio": 6, "dias": 30, "marcados": [26, 27, 29], "colores": {26: "azul", 27: "azul", 29: "rojo"}}),
        sello("EN DUDA", "amarillo", 1100, "@descarta"),
        quien("sanchez", 540, "@2023", 0.45, "normal", y=1560, entra="abajo", acciones=[
            {"at": "@Huesca", "pose": "saluda", "cara": "riendo"}, {"at": "@queda", "pose": "piensa", "cara": "pensativo"}]),
    ]),
    # 5 · CIERRE
    dict(id="final", fondo="calle", animo="final", trans="iris", footnote="Te leemos en comentarios", lines=[
        V("¿Tú qué ves bien: Europa o campaña? Te leo."),
        V("Y sigue a Piz para no perderte nada antes del 29N.", "energia", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@sigue", "medio", "piz", 0.5, aire=300)],
       elements=[
        etq("EUROPA", 300, 640, "@Europa", "azul", 0.7, hud=True, out="@sigue"),
        etq("CAMPAÑA", 780, 640, "@campaña", "rojo", 0.7, hud=True, out="@sigue"),
        quien("piz", 540, 0, 0.6, "pensativo", y=1500, entra="abajo", acciones=[
            {"at": "@Europa", "mira": "izq", "pose": "senala_izq"}, {"at": "@campaña", "mira": "der", "pose": "senala"},
            {"at": "@leo", "cara": "ilusionado", "mira": "camara", "pose": "normal"}, {"at": "@sigue", "pose": "saluda", "cara": "riendo"}]),
        rot("SIGUE A PIZ", 540, 420, "@sigue", 110, "amarillo", fx=[{"at": "@29N", "do": "latir"}]),
    ]),
]

if __name__ == "__main__":
    episodio("tres_cumbres", "Se salta tres cumbres", scenes,
             {"t": 3.2, "titulo": "Sánchez se salta tres cumbres", "capitulo": None},
             ["EFE (Infobae, 6/11/2026): Sánchez no irá a la COP31 (Antalya, 11/11), a la Comunidad Política Europea (Dublín, 12/11) "
              "ni a la cumbre informal de los 27 (Dublín, 13/11) por la cercanía del 29N; precedente UE-CELAC 2023; Bruselas 26-27/11 en duda"],
             ("✈️ Sánchez se salta tres cumbres esta semana\n"
              "🌍 11N Antalya: cumbre del clima (COP31)\n"
              "🇪🇺 12N Dublín: Comunidad Política Europea · 13N Dublín: los 27\n"
              "🗳️ El motivo, según el Gobierno: el 29N (la campaña empieza el 13 a las 00:00)\n"
              "🕰️ En 2023 sí fue a Bruselas en plena campaña · el 26-27 está en duda\n"
              "💬 ¿Europa o campaña? Te leo 👇\n"
              "🔔 Sigue a Piz · 📚 Fuentes en comentarios"),
             "📚 Fuentes: EFE vía Infobae, 6/11/2026 («El 29N altera la agenda exterior de Sánchez»). ¿Ves un error? Dínoslo.",
             ["#29N", "#Sánchez", "#COP31", "#UE", "#PolíticaEspañola", "#pizarrapublica"],
             series_tag="EXPLICADO FÁCIL")
