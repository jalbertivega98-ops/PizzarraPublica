"""Pruebas de voz del formato «Mi novia me dice…» (GitHub Actions, secreto ELEVENLABS_API_KEY).
python3 mono_voz.py mono_voz.json → ../public/voz/pruebas2/<id>.mp3 (+ .json con tiempos) + informe.txt
Él: el monólogo interior entero con cada voz candidata. Ella: sus dos frases sueltas con cada voz.
Nunca reintenta una generación fallida."""
import base64, json, os, sys, urllib.request, urllib.error
KEY = os.environ.get("ELEVENLABS_API_KEY", "").strip()
API = "https://api.elevenlabs.io/v1"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "public", "voz", "pruebas2"); os.makedirs(OUT, exist_ok=True)
log = []
def say(*a):
    s = " ".join(str(x) for x in a); print(s); log.append(s)
def tts(voice, text, stability, out):
    if os.path.exists(out): say("  ya existe", os.path.basename(out)); return 0
    body = {"text": text, "model_id": "eleven_v3", "voice_settings": {"stability": stability}}
    req = urllib.request.Request(f"{API}/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_128", data=json.dumps(body).encode(),
                                 headers={"xi-api-key": KEY, "Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=300) as r: d = json.loads(r.read())
    except urllib.error.HTTPError as e:
        say(f"  ERROR {e.code}: {e.read().decode()[:300]}"); return 0
    open(out, "wb").write(base64.b64decode(d["audio_base64"]))
    json.dump({"alignment": d.get("alignment")}, open(out[:-4] + ".json", "w"))
    return len(text)
cfg = json.load(open(os.path.join(HERE, sys.argv[1])))
total = 0
for c in cfg["el"]:
    say("==", c["id"])
    try: n = tts(c["voice"], cfg["monologo"], c["stability"], os.path.join(OUT, c["id"] + ".mp3")); total += n; say("  ok" if n else "  sin generar", n)
    except Exception as e: say("  FALLO", e)
for c in cfg["ella"]:
    for k in ("ella_1", "ella_2"):
        say("==", c["id"], k)
        try: n = tts(c["voice"], cfg[k], c["stability"], os.path.join(OUT, f'{c["id"]}_{k[-1]}.mp3')); total += n; say("  ok" if n else "  sin generar", n)
        except Exception as e: say("  FALLO", e)
say("TOTAL caracteres:", total)
open(os.path.join(OUT, "informe.txt"), "a").write("\n".join(log) + "\n")
