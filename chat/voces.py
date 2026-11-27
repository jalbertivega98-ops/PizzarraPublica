"""Genera la voz de cada mensaje de un guion de chat con edge-tts (voces gratis de Microsoft).
uso: python3 chat/voces.py chat/guiones/<guion>.json [...]
Solo guiones con "voces": true. Salida: chat/voz/<slug>/NN.mp3 + chat/voz/<slug>/voces.json
Voz por persona: personas[id].voz (por defecto es-ES-AlvaroNeural; mujeres: es-ES-ElviraNeural).
Se puede poner "leer" en un mensaje para que la voz diga otra cosa (p. ej. sin emojis o con pronunciación).
"""
import asyncio, json, os, re, subprocess, sys, hashlib
import edge_tts

EMO = re.compile("[\U0001F000-\U0001FAFF☀-➿️‍]+")

def limpiar(t):
    t = EMO.sub("", t).strip()
    return t

async def una(texto, voz, rate, pitch, out):
    c = edge_tts.Communicate(texto, voz, rate=rate, pitch=pitch)
    await c.save(out)

def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).decode())

async def main():
    for g_path in sys.argv[1:]:
        G = json.load(open(g_path))
        if not G.get("voces"):
            continue
        d = os.path.join("chat", "voz", G["slug"]); os.makedirs(d, exist_ok=True)
        P = G.get("personas", {})
        res = {}
        for i, m in enumerate(G["mensajes"]):
            if m.get("de") == "sistema" or m.get("tipo") == "mapa" and not m.get("leer"):
                continue
            texto = limpiar(m.get("leer", m.get("texto", "")))
            if not texto:
                continue
            per = P.get(m["de"], {})
            voz = per.get("voz", "es-ES-AlvaroNeural")
            rate = per.get("rate", "+10%"); pitch = per.get("pitch", "+0Hz")
            h = hashlib.sha1(f"{voz}|{rate}|{pitch}|{texto}".encode()).hexdigest()[:10]
            out = os.path.join(d, f"{i:02d}_{h}.mp3")
            if not os.path.exists(out):
                for intento in range(3):
                    try:
                        await una(texto, voz, rate, pitch, out); break
                    except Exception as e:
                        print("reintento", i, voz, e); await asyncio.sleep(3)
                        if intento == 1 and voz != "es-ES-ElviraNeural" and "Alvaro" not in voz:
                            voz, pitch = "es-ES-ElviraNeural", "+12Hz"   # respaldo si una voz no existe
            res[str(i)] = {"archivo": os.path.basename(out), "dur": round(dur(out), 3), "texto": texto, "voz": voz}
            print(i, voz, res[str(i)]["dur"], texto)
        # limpiar mp3 viejos
        vivos = {r["archivo"] for r in res.values()}
        for f in os.listdir(d):
            if f.endswith(".mp3") and f not in vivos:
                os.remove(os.path.join(d, f))
        json.dump(res, open(os.path.join(d, "voces.json"), "w"), ensure_ascii=False, indent=1)

asyncio.run(main())
