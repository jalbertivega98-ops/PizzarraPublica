"""Ronda 3 de voces (solo audio, sin efectos). GitHub Actions, secreto ELEVENLABS_API_KEY.
python3 voces3.py voces3.json → ../public/voz/pruebas4/<id>.mp3 + informe.txt
Cada trabajo: {"id", "tipo": "tts"|"dialogo", "voz", "texto", "estabilidad"} o {"id","tipo":"dialogo","lineas":[[voz, texto],...]}.
Nunca reintenta una generación fallida."""
import base64, json, os, sys, urllib.request, urllib.error
KEY = os.environ.get("ELEVENLABS_API_KEY", "").strip()
API = "https://api.elevenlabs.io/v1"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "public", "voz", "pruebas4")
log = []
def say(*a):
    s = " ".join(str(x) for x in a); print(s); log.append(s)
def post(path, data):
    req = urllib.request.Request(API + path, data=json.dumps(data).encode(), headers={"xi-api-key": KEY, "Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=300) as r: return json.loads(r.read())
    except urllib.error.HTTPError as e:
        say(f"  ERROR {e.code}: {e.read().decode()[:300]}"); return None
cfg = json.load(open(os.path.join(HERE, sys.argv[1])))
voces = cfg["voces"]
total = 0
for j in cfg["trabajos"]:
    out = os.path.join(OUT, j["id"] + ".mp3"); os.makedirs(os.path.dirname(out), exist_ok=True)
    say("==", j["id"])
    if os.path.exists(out): say("  ya existe"); continue
    try:
        if j["tipo"] == "tts":
            n = len(j["texto"])
            r = post(f'/text-to-speech/{voces[j["voz"]]}/with-timestamps?output_format=mp3_44100_128',
                     {"text": j["texto"], "model_id": "eleven_v3", "voice_settings": {"stability": j.get("estabilidad", 0.5)}})
        else:
            inputs = [{"text": t, "voice_id": voces[v]} for v, t in j["lineas"]]
            n = sum(len(i["text"]) for i in inputs)
            body = {"inputs": inputs, "model_id": "eleven_v3"}
            if "estabilidad" in j: body["settings"] = {"stability": j["estabilidad"]}
            r = post("/text-to-dialogue/with-timestamps?output_format=mp3_44100_128", body)
        if r and r.get("audio_base64"):
            open(out, "wb").write(base64.b64decode(r["audio_base64"]))
            json.dump({k: r.get(k) for k in ("alignment", "voice_segments")}, open(out[:-4] + ".json", "w"))
            total += n; say("  ok", n)
        else: say("  sin generar")
    except Exception as e: say("  FALLO", e)
say("TOTAL caracteres:", total)
os.makedirs(OUT, exist_ok=True); open(os.path.join(OUT, "informe.txt"), "a").write("\n".join(log) + "\n")
