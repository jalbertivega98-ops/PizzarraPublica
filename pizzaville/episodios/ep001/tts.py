import asyncio, json, subprocess, os
import edge_tts

SEG = [
    ("intro",   "¡Ey! ¿¡Pero qué ha pasado aquí!?"),
    ("count",   "Ayer vivía solo en este valle… y hoy ya somos sesenta y dos vecinos, de trece países."),
    ("river",   "Somos tantos, que hemos tenido que partir el valle en dos: Europa a este lado del río… y América al otro."),
    ("infra",   "Y tanta gente necesita cosas: ya tenemos supermercado, escuela, centro de salud… y tres puentes."),
    ("spain",   "Marina, de España, fuiste la primera en llamar a la puerta. Gabriel ya tiene su granja de gallinas, y Manuel, su huerto con tractor."),
    ("rodrigo", "Rodrigo quería su furgo y sus perros, al ladito del río. Hecho."),
    ("aleky",   "Y Aleky quiere ser el peluquero del pueblo… ¡peluquería abierta!"),
    ("bridge",  "Crucemos el puente."),
    ("america", "Fernando ya tiene su rancho en México, Kiker su casa de dos pisos, y Thiago, desde Argentina, su mansión con piscina."),
    ("brasil",  "¡Y atención! Matheus trae la primera bandera nueva: Brasil. Premio: ¡barrio propio!"),
    ("sweep",   "Bienvenidos también Laia, Jaume, Rafa… y todos los nuevos vecinos."),
    ("score",   "Ahora mismo gana Europa, treinta y siete a veinticinco. América… ¿le dais la vuelta?"),
    ("cta",     "¿Tu casa aquí? Comenta tu nombre, tu país y qué casa quieres, y etiqueta a alguien de tu país. ¡Te la construyo en el próximo episodio!"),
]


async def main():
    out = []
    for i, (k, t) in enumerate(SEG):
        f = f"voz/{i:02d}_{k}.mp3"
        await edge_tts.Communicate(t, "es-ES-AlvaroNeural", rate="+8%", pitch="+12Hz").save(f)
        d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).decode())
        out.append({"key": k, "text": t, "file": f, "dur": d})
    gap, t0 = 0.35, 0.6
    for s in out:
        s["start"] = round(t0, 3); t0 += s["dur"] + gap
    total = t0 + 2.0
    json.dump({"segments": out, "total": round(total, 2)}, open("timeline.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(total)

asyncio.run(main())
