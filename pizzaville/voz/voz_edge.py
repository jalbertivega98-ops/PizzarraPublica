"""Genera la voz de Pizz (Microsoft Álvaro, gratis vía edge-tts) para un guion.
Uso: python3 voz_edge.py ep000.json  → ../public/voz/<episode>/<id>.mp3 + <id>.json (tiempos por palabra)
Se ejecuta en GitHub Actions (el contenedor no llega a speech.platform.bing.com)."""
import asyncio, json, os, sys
import edge_tts

async def one(line, cfg, outdir):
    mp3 = os.path.join(outdir, line["id"] + ".mp3")
    words = []
    com = edge_tts.Communicate(line["text"], cfg["voice"], rate=cfg.get("rate", "+0%"), pitch=cfg.get("pitch", "+0Hz"), boundary="WordBoundary")
    with open(mp3, "wb") as f:
        async for ch in com.stream():
            if ch["type"] == "audio":
                f.write(ch["data"])
            elif ch["type"] == "WordBoundary":
                words.append({"w": ch["text"], "t": ch["offset"] / 1e7, "d": ch["duration"] / 1e7})
    json.dump({"text": line["text"], "words": words}, open(os.path.join(outdir, line["id"] + ".json"), "w"), ensure_ascii=False, indent=1)
    print("ok", line["id"], len(words), "palabras")

async def main(path):
    cfg = json.load(open(path))
    outdir = os.path.join(os.path.dirname(os.path.abspath(path)), "..", "public", "voz", cfg["episode"])
    os.makedirs(outdir, exist_ok=True)
    for line in cfg["lines"]:
        await one(line, cfg, outdir)

asyncio.run(main(sys.argv[1]))
