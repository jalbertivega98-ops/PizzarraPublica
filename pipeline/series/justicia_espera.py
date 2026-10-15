#!/usr/bin/env python3
"""«¿Cuánto tarda la justicia?» (2026): asuntos pendientes en los juzgados.

Fuente: CGPJ, «Situación de los órganos judiciales 2025» (nota del 30/03/2026): 4.673.596 asuntos pendientes a 31/12/2025 (+3,4 %);
  civil 2.672.464 · penal 1.255.950 · social 525.652 (+9,4 %) · contencioso 219.492.
Tiempo para resolver lo pendiente al ritmo de 2025 (pendientes / resueltos × 12, indicador «disposition time» del CEPEJ, cálculo propio):
  social 13,6 meses · contencioso 12,4 · civil 9,7 · penal 4,4. No es la duración oficial de un juicio.
"""
from _tu_dinero import *  # noqa: F401,F403

CG = "CGPJ, situación de los órganos judiciales 2025 (nota 30/03/2026)"
CEPEJ = "Cálculo propio: pendientes ÷ resueltos en 2025 (indicador del CEPEJ)"
pila_els, pila_pizon = gags.cae_del_cielo("4,7 MILLONES", "@millones-0.5", 330, 820, scale=1.1, onomatopeya="¡PATAPLAF!")

scenes = [
    dict(id="gancho", fondo="oficina", animo="curioso", footnote=CG, lines=[
        V("Hay 4,7 millones de casos esperando en los juzgados de España.", "energia"),
        V("Una montaña de papeles.", "remate", 0.2),
    ], camara=[plano(0, "general", dur=0), plano("@montaña", "abierto", dur=0.4)],
       elements=[
        quien("pizon", 330, 0, 0.75, "normal", entra="izq", acciones=pila_pizon + [{"at": "@papeles", "cara": "confundido"}]),
        *pila_els,
        dict(type="efecto", efecto="lluvia", objeto="contrato", n=9, x0=520, x1=960, at="@montaña", vida=2.0),
        rot("4.673.596 CASOS", 600, 480, "@millones", 84, C, golpe=True),
    ]),
    dict(id="tipos", fondo="oficina", animo="curioso", trans="pan", footnote=CG, lines=[
        V("En lo civil, 2,7 millones. En lo penal, 1,3.", "normal"),
        V("En lo social, que son despidos, bajas o pensiones, 526.000.", "normal", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@526.000", "medio", "profe", 0.3, aire=200)],
       elements=[
        quien("profe", 280, 0, 0.75, "normal", entra="izq", pose="senala_arriba", acciones=[
            {"at": "@civil", "pose": "senala"}, {"at": "@penal", "mira": "camara"}, {"at": "@social", "salta": True},
            {"at": "@despidos", "cara": "serio"}, {"at": "@526.000", "pose": "pulgar"}]),
        etq("CIVIL: 2,7 M", 760, 600, "@civil", "amarillo"),
        etq("PENAL: 1,3 M", 760, 780, "@penal", "blanco"),
        etq("SOCIAL: 526.000", 760, 960, "@social", "rojo"),
    ]),
    dict(id="ritmo", fondo="rayos", animo="tension", musica="corte", trans="iris", footnote=CEPEJ, lines=[
        V("Al ritmo de 2025, lo social tardaría casi 14 meses en ponerse al día.", "sorpresa"),
        V("Lo contencioso, 12. Lo penal, 4.", "normal", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@14", "medio", "pizon", 0.3, aire=220)],
       elements=[
        quien("pizon", 300, 0, 0.78, "preocupado", entra="pop", acciones=[
            {"at": "@social", "mira": "reloj"}, {"at": "@14", "take": True, "cara": "susto"},
            {"at": "@contencioso", "tiembla": True}, {"at": "@4", "cara": "pensativo"}]),
        obj("reloj", 780, 760, "@ritmo", 0.8, id="reloj", entra="pop", velocidad=8),
        rot("SOCIAL: 13,6 MESES", 600, 480, "@14", 76, C, golpe=True),
        rot("CONTENCIOSO: 12,4", 600, 590, "@contencioso", 64, "amarillo", golpe=True),
        rot("PENAL: 4,4", 600, 690, "@penal", 64, "verde", golpe=True),
    ]),
    dict(id="pizon", fondo="calle", animo="triste", trans="pan", footnote=CEPEJ + " · jurisdicción social", lines=[
        V("Si a Pizón le despiden y reclama, la cola que tiene delante es la más larga.", "normal"),
    ], camara=[plano(0, "general", dur=0), plano("@larga", "abierto", dur=0.4)],
       elements=[
        quien("pizon", 820, 0, 0.72, "normal", entra="der", objeto={"tipo": "contrato", "titulo": "DEMANDA", "hojas": 1}, pose="sostiene",
              acciones=[{"at": "@despiden", "take": True, "cara": "susto"}, {"at": "@reclama", "cara": "indignado"},
                        {"at": "@cola", "mira": "izq", "cara": "triste"}, {"at": "@larga", "tropieza": True}]),
        quien("piz", 200, "@cola", 0.55, "normal", entra="izq", acciones=[{"at": "@larga", "pose": "encoge"}]),
        quien("sarcastica", 420, "@cola+0.2", 0.55, "burla", entra="izq"),
        rot("LA COLA MÁS LARGA", 540, 480, "@cola", 84, "amarillo", golpe=True),
    ]),
    dict(id="crece", fondo="oficina", animo="tension", trans="iris", footnote=CG + " · pendientes +3,4 % (social +9,4 %)", lines=[
        V("Y la pila crece: un 3,4 % más que el año anterior. Lo social, un 9,4.", "sorpresa"),
    ], camara=[plano(0, "general", dur=0), plano("@9,4", "abierto", dur=0.4)],
       elements=[
        quien("profe", 300, 0, 0.75, "serio", entra="izq", acciones=[
            {"at": "@crece", "mira": "grafica", "pose": "senala"}, {"at": "@3,4", "take": True}, {"at": "@9,4", "cara": "sorpresa"}]),
        obj("grafica", 760, 800, "@pila", 0.85, id="grafica", entra="pop", props={"valores": [1, 1.2, 1.5, 1.9], "color": "rojo"}),
        rot("+3,4 %", 600, 480, "@3,4", 110, C, golpe=True, out="@9,4"),
        rot("SOCIAL: +9,4 %", 600, 480, "@9,4", 90, C, golpe=True),
    ]),
    dict(id="matiz", fondo="oficina", animo="curioso", trans="pan", footnote="No es la duración oficial de un juicio: es pendientes ÷ resueltos", lines=[
        V("Ojo: no es lo que dura un juicio. Es lo que tardarían en vaciar la mesa sin que entrara nada nuevo.", "normal"),
    ], camara=[plano(0, "general", dur=0), plano("@nuevo", "medio", "profe", 0.3, aire=200)],
       elements=[
        quien("profe", 300, 0, 0.75, "normal", entra="nada", pose="senala_arriba", acciones=[
            {"at": "@juicio", "pose": "senala", "cara": "serio"}, {"at": "@vaciar", "mira": "camara"},
            {"at": "@nuevo", "pose": "pulgar", "cara": "normal"}]),
        obj("contrato", 780, 800, "@mesa", 0.7, entra="pop", props={"titulo": "PENDIENTES", "hojas": 3}, sfx="papel"),
        rot("≠ DURACIÓN DE UN JUICIO", 600, 480, "@Ojo", 64, "amarillo", golpe=True),
    ]),
    dict(id="final", fondo="calle", animo="final", trans="iris", footnote=CG, lines=[
        V("¿Has esperado un juicio? Te leemos.", "normal"),
        V("Y síguenos: la próxima, los jóvenes que se van de España.", "energia", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@síguenos", "abierto", dur=0.4)],
       elements=[
        quien("piz", 300, 0, 0.72, "normal", entra="nada", acciones=[
            {"at": "@esperado", "mira": "camara", "cara": "pensativo"}, {"at": "@leemos", "pose": "senala", "cara": "ilusionado"},
            {"at": "@síguenos", "pose": "saluda", "cara": "riendo"}, {"at": "@España", "salta": True}]),
        quien("pizon", 790, 0, 0.72, "normal", entra="nada", acciones=[{"at": "@juicio", "cara": "triste"}, {"at": "@España", "take": True}]),
        rot("¿HAS ESPERADO?", 540, 470, "@esperado", 90, "amarillo", golpe=True, out="@síguenos-0.4"),
        rot("SÍGUENOS", 540, 470, "@síguenos", 110, "amarillo", fx=[{"at": "@España", "do": "latir"}]),
    ]),
]

if __name__ == "__main__":
    episodio("justicia_espera", "¿Cuánto tarda la justicia?", scenes, {"t": 3.4, "titulo": "4,7 millones de casos esperando", "capitulo": None},
             ["CGPJ: situación de los órganos judiciales 2025 (nota del 30/03/2026)", "CEPEJ (Consejo de Europa): indicador «disposition time»"],
             ("⚖️ 4,7 millones de casos esperan en los juzgados de España\n"
              "📂 Civil 2,7 M · penal 1,3 M · social 526.000 · contencioso 219.000\n"
              "⏳ Al ritmo de 2025: lo social tardaría 13,6 meses en ponerse al día; el penal, 4,4\n"
              "📈 La pila crece un 3,4 % (lo social, un 9,4 %)\n"
              "⚠️ No es lo que dura un juicio: es lo que tardarían en vaciar la mesa\n"
              "💬 ¿Has esperado un juicio?\n"
              "➡️ Próximo: los jóvenes que se van · 🔔 Síguenos · 📚 Fuentes en comentarios"),
             ("📚 Fuente: CGPJ, «Situación de los órganos judiciales 2025» (nota del 30/03/2026): 4.673.596 asuntos pendientes a 31/12/2025; "
              "civil 2.672.464, penal 1.255.950, social 525.652, contencioso 219.492. Los meses son cálculo propio con el indicador del CEPEJ "
              "(pendientes ÷ resueltos en 2025 × 12): no es la duración oficial de un juicio, que el CGPJ publica por tipo de juzgado. "
              "¿Ves un error? Dínoslo."),
             ["#PizarraPública", "#Justicia", "#Juzgados", "#CGPJ", "#Datos", "#España"])
