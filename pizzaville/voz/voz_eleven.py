"""Voz de ElevenLabs para un guion de Pizzaville (en GitHub Actions, con el secreto ELEVENLABS_API_KEY).
  python3 voz_eleven.py saldo                 → solo consulta: créditos que quedan y voces disponibles (no gasta nada)
  python3 voz_eleven.py ep000.json VOICE_ID   → ../public/voz/<episode>_eleven/<id>.mp3 + .json (tiempos por palabra)
Antes de generar comprueba que el saldo alcanza para todo el guion; si no, no genera nada."""
import base64, json, os, sys, urllib.request, urllib.error

KEY = os.environ.get("ELEVENLABS_API_KEY", "").strip()
API = "https://api.elevenlabs.io/v1"
MODEL = os.environ.get("ELEVEN_MODEL", "eleven_multilingual_v2")

def call(path, data=None, soft=False):
    req = urllib.request.Request(API + path, data=json.dumps(data).encode() if data is not None else None,
                                 headers={"xi-api-key": KEY, "Content-Type": "application/json"}, method="POST" if data is not None else "GET")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            b = r.read()
            try: return json.loads(b or b"{}")
            except ValueError: return {"bytes": len(b)}
    except urllib.error.HTTPError as e:
        msg = f"ElevenLabs {e.code}: {e.read().decode()[:400]}"
        if soft: print(msg); return None
        sys.exit(msg)

def saldo():
    s = call("/user/subscription", soft=True)
    if s is None: print("SALDO_DESCONOCIDO (la clave no tiene permiso user_read)"); return None
    left = s.get("character_limit", 0) - s.get("character_count", 0)
    print(f"PLAN={s.get('tier')} USADOS={s.get('character_count')} LIMITE={s.get('character_limit')} QUEDAN={left} RENUEVA={s.get('next_character_count_reset_unix')}")
    return left

def main():
    if not KEY: sys.exit("Falta el secreto ELEVENLABS_API_KEY")
    left = saldo()
    if sys.argv[1] == "saldo":
        r = call(f"/text-to-speech/{sys.argv[2] if len(sys.argv) > 2 else 'Iohr8NC0THLcVZXLaHlP'}?output_format=mp3_22050_32", {"text": "Hola.", "model_id": MODEL}, soft=True)
        print("PRUEBA_TTS", "OK (hay créditos)" if r is not None else "FALLÓ")
        for v in (call("/voices", soft=True) or {}).get("voices", []):
            l = v.get("labels") or {}
            print(f"VOZ {v['voice_id']} | {v.get('name')} | {v.get('category')} | {l.get('gender','')} {l.get('age','')} {l.get('accent','')} {l.get('language','')}")
        return
    path = sys.argv[1] if os.path.exists(sys.argv[1]) else os.path.join(os.path.dirname(os.path.abspath(__file__)), sys.argv[1])
    cfg = json.load(open(path)); voice = sys.argv[2]
    need = sum(len(l["text"]) for l in cfg["lines"])
    print(f"El guion necesita {need} caracteres")
    if left is not None and need > left: sys.exit(f"NO HAY SALDO: faltan {need - left} caracteres. No genero nada.")
    out = os.path.join(os.path.dirname(os.path.abspath(path)), "..", "public", "voz", cfg["episode"] + "_eleven")
    os.makedirs(out, exist_ok=True)
    st = cfg.get("eleven", {"stability": 0.4, "similarity_boost": 0.8, "style": 0.35, "use_speaker_boost": True})
    for line in cfg["lines"]:
        r = call(f"/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_128",
                 {"text": line["text"], "model_id": MODEL, "voice_settings": st})
        open(os.path.join(out, line["id"] + ".mp3"), "wb").write(base64.b64decode(r["audio_base64"]))
        a = r.get("alignment") or {}
        words, cur, t0, t1 = [], "", None, 0
        for ch, s, e in zip(a.get("characters", []), a.get("character_start_times_seconds", []), a.get("character_end_times_seconds", [])):
            if ch.isalnum() or ch in "'-áéíóúüñÁÉÍÓÚÜÑ":
                if not cur: t0 = s
                cur += ch; t1 = e
            elif cur:
                words.append({"w": cur, "t": t0, "d": t1 - t0}); cur = ""
        if cur: words.append({"w": cur, "t": t0, "d": t1 - t0})
        json.dump({"text": line["text"], "voice": voice, "words": words}, open(os.path.join(out, line["id"] + ".json"), "w"), ensure_ascii=False, indent=1)
        print("ok", line["id"], len(words), "palabras")
    saldo()

main()
