#!/usr/bin/env python3
"""«Listas de espera» (2026): lo que se espera una operación según la comunidad.

Fuente: Ministerio de Sanidad, SISLE-SNS a 31/12/2025 (último corte publicado; nota resumen e informe por CCAA, abril 2026):
  853.509 pacientes en espera quirúrgica no urgente · 121 días de media · 21,6 % más de 6 meses.
  Especialidades: cirugía plástica 269 días, neurocirugía 172. Consultas externas (1.ª consulta): 102 días.
  Por comunidad: Andalucía 173 días (máx.), Madrid 50 (mín.) → 3,5 veces (cálculo propio).
  Matiz: datos que envía cada comunidad con criterios distintos; es la espera de quien aún no se ha operado.
"""
from _tu_dinero import *  # noqa: F401,F403

SIS = "Ministerio de Sanidad, SISLE-SNS a 31/12/2025"
reloj_els, reloj_pizon = gags.cae_del_cielo("173 DÍAS", "@173-0.5", 300, 820, scale=1.1, onomatopeya="¡PLAF!")

scenes = [
    dict(id="gancho", fondo="calle", animo="curioso", footnote=SIS, lines=[
        V("853.509 personas esperan una operación en España.", "energia"),
        V("Según dónde vivas: 50 días… o 173.", "remate", 0.2),
    ], camara=[plano(0, "general", dur=0), plano("@173", "abierto", dur=0.4)],
       elements=[
        edif("hospital", 540, 0, 0.6, id="hospital", entra="nada"),
        quien("piz", 250, "@personas", 0.62, "normal", entra="izq", acciones=[{"at": 2.6, "mira": "hospital", "cara": "pensativo"}, {"at": "@50", "salta": True, "cara": "riendo"}]),
        quien("pizon", 830, "@personas+0.3", 0.62, "preocupado", entra="der", acciones=[{"at": 3.7, "mira": "piz", "pose": "encoge"}, {"at": 4.6, "tiembla": True}, {"at": "@173", "take": True, "cara": "susto"}]),
        rot("853.509", 540, 480, "@853.509", 120, "amarillo", golpe=True, out="@vivas"),
        rot("50 DÍAS", 250, 520, "@50", 90, "verde", golpe=True),
        rot("173 DÍAS", 830, 520, "@173", 90, C, golpe=True),
    ]),
    dict(id="media", fondo="oficina", animo="tension", trans="pan", footnote=SIS, lines=[
        V("La espera media: 121 días. Cuatro meses.", "normal"),
        V("Y uno de cada cinco lleva más de medio año.", "sorpresa", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@medio", "medio", "pizon", 0.3, aire=200)],
       elements=[
        quien("pizon", 300, 0, 0.75, "normal", entra="izq", acciones=[
            {"at": "@121", "mira": "reloj", "cara": "preocupado"}, {"at": "@meses", "tiembla": True},
            {"at": "@cinco", "mira": "camara"}, {"at": "@medio", "take": True, "cara": "susto"}]),
        obj("reloj", 780, 760, "@espera", 0.8, id="reloj", entra="pop", velocidad=6),
        rot("121 DÍAS", 600, 560, "@121", 110, "amarillo", golpe=True, out="@cinco"),
        rot("1 DE CADA 5: +6 MESES", 600, 560, "@cinco", 70, C, golpe=True),
    ]),
    dict(id="especialidades", fondo="salon", animo="comico", trans="iris", footnote="SISLE-SNS 31/12/2025 · por especialidad", lines=[
        V("Lo más lento: cirugía plástica, 269 días. Neurocirugía, 172.", "normal"),
    ], camara=[plano(0, "general", dur=0), plano("@Neurocirugía", "abierto", dur=0.4)],
       elements=[
        quien("sarcastica", 270, 0, 0.72, "burla", entra="izq", acciones=[
            {"at": "@plástica", "pose": "jarras", "cara": "sorpresa"}, {"at": "@269", "take": True},
            {"at": "@172", "pose": "encoge", "cara": "esceptica"}]),
        etq("PLÁSTICA: 269 DÍAS", 720, 640, "@plástica", "rojo"),
        etq("NEUROCIRUGÍA: 172", 720, 860, "@Neurocirugía", "amarillo"),
    ]),
    dict(id="ccaa", fondo="calle", animo="tension", trans="pan", footnote="SISLE-SNS 31/12/2025 · por comunidad · cálculo propio", lines=[
        V("Por comunidades, Andalucía es la que más: 173 días.", "normal"),
        V("Madrid, la que menos: 50. Tres veces y media menos.", "sorpresa", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@media", "abierto", dur=0.4)],
       elements=[
        quien("pizon", 300, 0, 0.72, "normal", entra="izq", acciones=reloj_pizon + [{"at": "@Madrid", "mira": "piz", "cara": "triste"}]),
        *reloj_els,
        quien("piz", 1300, "@Madrid-0.3", 0.72, "riendo", entra="nada", acciones=[
            {"at": "@Madrid", "x": 800, "dur": 0.6, "corre": True}, {"at": "@50", "salta": True, "pose": "arriba"},
            {"at": "@media", "mira": "pizon", "cara": "pensativo"}]),
        rot("ANDALUCÍA: 173 DÍAS", 540, 460, "@Andalucía", 70, C, golpe=True),
        rot("MADRID: 50 DÍAS", 540, 560, "@Madrid", 70, "verde", golpe=True),
        rot("× 3,5", 540, 680, "@media", 120, "amarillo", golpe=True),
    ]),
    dict(id="consultas", fondo="rayos", animo="comico", musica="corte", trans="iris", footnote="SISLE-SNS 31/12/2025 · consultas externas: 102 días", lines=[
        V("Y eso, sin contar la espera de antes: ver al especialista, 102 días más.", "sorpresa"),
    ], camara=[plano(0, "general", dur=0), plano("@102", "medio", "pizon", 0.3, aire=220)],
       elements=[
        quien("pizon", 540, 0, 0.8, "normal", entra="pop", acciones=[
            {"at": "@antes", "cara": "confundido", "mira": "camara"}, {"at": "@especialista", "pose": "cabeza"},
            {"at": "@102", "tropieza": True, "cara": "susto"}]),
        rot("+102 DÍAS ANTES", 540, 520, "@102", 92, C, golpe=True),
        pum("¡OTRA COLA!", 760, 820, "@102+0.3"),
    ]),
    dict(id="matiz", fondo="oficina", animo="curioso", trans="pan", footnote="Cada comunidad envía sus datos con sus criterios", lines=[
        V("Ojo: cada comunidad cuenta a su manera, y es la espera de quien aún no se ha operado.", "normal"),
    ], camara=[plano(0, "general", dur=0), plano("@operado", "medio", "profe", 0.3, aire=200)],
       elements=[
        quien("profe", 300, 0, 0.75, "serio", entra="izq", pose="senala_arriba", acciones=[
            {"at": "@comunidad", "pose": "senala"}, {"at": "@manera", "mira": "camara", "cara": "pensativo"},
            {"at": "@operado", "pose": "pulgar", "cara": "normal"}]),
        obj("checklist", 760, 760, "@cuenta", 0.6, entra="pop", props={"items": ["DATOS DE CADA CCAA", "CRITERIOS DISTINTOS"], "marcas": ["si", "si"]}),
        rot("COMPARAR CON CUIDADO", 600, 480, "@Ojo", 68, "amarillo", golpe=True),
    ]),
    dict(id="final", fondo="calle", animo="final", trans="iris", footnote=SIS, lines=[
        V("¿Cuánto esperaste tú? Te leemos.", "normal"),
        V("Y síguenos: la próxima, la factura de la luz.", "energia", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@síguenos", "abierto", dur=0.4)],
       elements=[
        edif("hospital", 780, 0, 0.5, id="hospital", entra="nada"),
        quien("piz", 280, 0, 0.72, "normal", entra="nada", acciones=[
            {"at": "@esperaste", "mira": "camara", "cara": "pensativo"}, {"at": "@leemos", "pose": "senala", "cara": "ilusionado"},
            {"at": "@síguenos", "pose": "saluda", "cara": "riendo"}, {"at": "@luz", "salta": True}]),
        rot("¿CUÁNTO ESPERASTE?", 540, 470, "@esperaste", 84, "amarillo", golpe=True, out="@síguenos-0.4"),
        rot("SÍGUENOS", 540, 470, "@síguenos", 110, "amarillo", fx=[{"at": "@luz", "do": "latir"}]),
    ]),
]

if __name__ == "__main__":
    episodio("listas_espera", "Listas de espera", scenes, {"t": 3.6, "titulo": "50 días o 173: la lista de espera", "capitulo": None},
             ["Ministerio de Sanidad: SISLE-SNS, situación a 31/12/2025 (nota resumen y datos por CCAA)"],
             ("🏥 853.509 personas esperan una operación en España\n"
              "⏳ Espera media: 121 días · 1 de cada 5, más de 6 meses\n"
              "🐢 Lo más lento: cirugía plástica (269 días) y neurocirugía (172)\n"
              "🗺️ Andalucía 173 días · Madrid 50: 3,5 veces menos\n"
              "📋 Y antes, 102 días para ver al especialista\n"
              "⚖️ Cada comunidad cuenta a su manera: comparar con cuidado\n"
              "💬 ¿Cuánto esperaste tú?\n"
              "➡️ Próximo: la factura de la luz · 🔔 Síguenos · 📚 Fuentes en comentarios"),
             ("📚 Fuente: Ministerio de Sanidad, Sistema de Información sobre Listas de Espera (SISLE-SNS), situación a 31/12/2025, "
              "último corte publicado (nota resumen e informe por comunidades). Espera quirúrgica no urgente: 853.509 pacientes, 121 días de media, "
              "21,6 % más de 6 meses; consultas externas 102 días. Andalucía 173 días, Madrid 50 (cálculo propio: 3,5 veces). Los datos los envía "
              "cada comunidad y los criterios pueden diferir. ¿Ves un error? Dínoslo."),
             ["#PizarraPública", "#ListasDeEspera", "#Sanidad", "#SanidadPública", "#Datos", "#España"])
