"""Pruebas de voz con el mismo diálogo (en GitHub Actions, secreto ELEVENLABS_API_KEY).
python3 pruebas_voz.py pruebas_voz.json → ../public/voz/pruebas/<id>.mp3 + informe.txt
- eleven: text-to-dialogue (eleven_v3) con la voz candidata y la voz de referencia del otro personaje.
- diseno: crea una voz original con Voice Design (eleven_ttv_v3), la guarda y hace el mismo diálogo.
- edge: Microsoft (edge-tts, gratis), frase a frase con pausas, sin etiquetas de emoción.
Nunca reintenta una generación que ha fallado (para no gastar créditos dos veces)."""
import asyncio, base64, json, os, subprocess, sys, tempfile, urllib.request, urllib.error
KEY = os.environ.get("ELEVENLABS_API_KEY", "").strip()
API = "https://api.elevenlabs.io/v1"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "public", "voz", "pruebas"); os.makedirs(OUT, exist_ok=True)
log = []
def say(*a):
    s = " ".join(str(x) for x in a); print(s); log.append(s)

def post(path, data, raw=False):
    req = urllib.request.Request(API + path, data=json.dumps(data).encode(), headers={"xi-api-key": KEY, "Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            b = r.read(); return b if raw else json.loads(b)
    except urllib.error.HTTPError as e:
        say(f"  ERROR {path} {e.code}: {e.read().decode()[:300]}"); return None

def dialogue(cfg, voice_el, voice_ella, out, model="eleven_v3"):
    inputs = [{"text": f'{l["tag"]} {l["text"]}', "voice_id": voice_el if l["who"] == "el" else voice_ella} for l in cfg["dialogo"]]
    chars = sum(len(i["text"]) for i in inputs)
    r = post("/text-to-dialogue/with-timestamps?output_format=mp3_44100_128", {"inputs": inputs, "model_id": model})
    if r and r.get("audio_base64"):
        open(out, "wb").write(base64.b64decode(r["audio_base64"]))
        json.dump({k: r.get(k) for k in ("alignment", "voice_segments")}, open(out[:-4] + ".json", "w"))
        return chars
    b = post("/text-to-dialogue?output_format=mp3_44100_128", {"inputs": inputs, "model_id": model}, raw=True)
    if b: open(out, "wb").write(b); return chars
    return 0

def design(c):
    sample = "Oye, que no pasa nada, ¿eh? Que yo estoy tranquilo. Tranquilísimo. Lo que pasa es que llevo media hora esperando y ya me sé de memoria el pasillo de los yogures."
    r = post("/text-to-voice/design", {"voice_description": c["descripcion"], "model_id": "eleven_ttv_v3", "text": sample})
    if not r or not r.get("previews"): return None
    p = r["previews"][0]
    open(os.path.join(OUT, c["id"] + "_muestra_diseno.mp3"), "wb").write(base64.b64decode(p["audio_base_64"]))
    s = post("/text-to-voice", {"voice_name": c["nombre"], "voice_description": c["descripcion"], "generated_voice_id": p["generated_voice_id"]})
    return s and s.get("voice_id")

async def edge(cfg, v_el, v_ella, out):
    import edge_tts
    parts = []
    tmp = tempfile.mkdtemp()
    for i, l in enumerate(cfg["dialogo"]):
        f = os.path.join(tmp, f"{i}.mp3")
        await edge_tts.Communicate(l["text"], v_el if l["who"] == "el" else v_ella).save(f)
        parts.append(f)
    lst = os.path.join(tmp, "l.txt"); sil = os.path.join(tmp, "s.mp3")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", "0.6", "-b:a", "48k", sil], check=True)
    open(lst, "w").write("".join(f"file '{p}'\nfile '{sil}'\n" for p in parts))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-ar", "44100", "-b:a", "128k", out], check=True)

def main():
    cfg = json.load(open(os.path.join(HERE, sys.argv[1])))
    total = 0
    for grupo, otra in (("masculinas", "ref_ella"), ("femeninas", "ref_el")):
        for c in cfg[grupo]:
            out = os.path.join(OUT, c["id"] + ".mp3")
            if os.path.exists(out): say("ya existe", c["id"]); continue
            say("==", c["id"], c["motor"])
            if c["motor"] == "edge":
                ref = "es-ES-ElviraNeural" if grupo == "masculinas" else "es-ES-AlvaroNeural"
                asyncio.run(edge(cfg, c["voice"] if grupo == "masculinas" else ref, ref if grupo == "masculinas" else c["voice"], out))
                say("  ok (gratis)"); continue
            v = c.get("voice")
            if c["motor"] == "diseno":
                v = design(c); say("  voz diseñada:", v)
                if not v: continue
            el, ella = (v, cfg["ref_ella"]) if grupo == "masculinas" else (cfg["ref_el"], v)
            n = dialogue(cfg, el, ella, out); total += n
            say("  ok" if n else "  FALLÓ", n, "caracteres")
    say("TOTAL caracteres ElevenLabs (sin contar el diseño de voz):", total)
    open(os.path.join(OUT, "informe.txt"), "a").write("\n".join(log) + "\n")

main()
