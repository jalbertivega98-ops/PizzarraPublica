#!/usr/bin/env python3
"""Voces de ElevenLabs para los storyboards (se ejecuta en GitHub Actions con el secreto ELEVENLABS_API_KEY).

Genera un MP3 por frase en voces_elevenlabs/<clave>.mp3, donde la clave depende de la voz, el modelo
y el texto. make_video.py usa esos archivos cuando el storyboard tiene "voice": {"engine": "elevenlabs"}.

  python3 tts_elevenlabs.py storyboards/impuestos_*.json --voice <voice_id>   # vídeos completos
  python3 tts_elevenlabs.py --muestras "texto de prueba"                      # una muestra por voz en voces_elevenlabs/muestras/
  python3 tts_elevenlabs.py --muestras "texto" --motor edge                   # voces gratis de Microsoft (es-ES) en muestras_microsoft/
  python3 tts_elevenlabs.py --muestras "texto" --biblioteca 8                 # voces de España de la biblioteca en muestras_es/
"""
import argparse
import glob
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "voces_elevenlabs")
API = "https://api.elevenlabs.io/v1"
MODEL = "eleven_multilingual_v2"
# voces de la biblioteca básica de ElevenLabs que hablan español con el modelo multilingüe
MUESTRAS = {"George": "JBFqnCBsd6RMkjVDRZzb", "Brian": "nPczCjzI2devNBz1zQrb", "Daniel": "onwK4e9ZLuTAKqWW03F9",
            "Liam": "TX3LPaxmHKxFdv7VOQHJ", "Sarah": "EXAVITQu4vr4xnSDxMaL", "Alice": "Xb7hH8MSUJpSbSDYk0k2"}
SETTINGS = {"stability": 0.5, "similarity_boost": 0.75, "style": 0.15, "use_speaker_boost": True}
# Estilo «viva» (docs/enganche.md): cada frase puede llevar un tono. Menos estabilidad = más expresiva.
TONOS = {
    "normal":   {"stability": 0.38, "similarity_boost": 0.8, "style": 0.35, "use_speaker_boost": True, "speed": 1.06},
    "energia":  {"stability": 0.30, "similarity_boost": 0.8, "style": 0.55, "use_speaker_boost": True, "speed": 1.10},
    "sorpresa": {"stability": 0.28, "similarity_boost": 0.8, "style": 0.60, "use_speaker_boost": True, "speed": 1.04},
    "intriga":  {"stability": 0.45, "similarity_boost": 0.8, "style": 0.45, "use_speaker_boost": True, "speed": 0.94},
    "sobrio":   {"stability": 0.62, "similarity_boost": 0.8, "style": 0.12, "use_speaker_boost": True, "speed": 0.98},
    "remate":   {"stability": 0.50, "similarity_boost": 0.8, "style": 0.40, "use_speaker_boost": True, "speed": 0.92},
}


def line_text(line):
    """ElevenLabs lee bien siglas y cifras: usa el texto del subtítulo, no la variante fonética de Piper."""
    return line["text"] if isinstance(line, dict) else line


def key(voice, model, text, tono=None):
    """tono=None conserva las claves de los vídeos antiguos; el estilo «viva» añade el tono a la clave."""
    base = f"{voice}|{model}|{text}" + (f"|viva:{tono}" if tono else "")
    return hashlib.sha1(base.encode()).hexdigest()[:16]


def line_tono(story, line):
    """Tono de una frase en el estilo «viva» (None en los storyboards antiguos)."""
    if story.get("estilo") != "viva":
        return None
    t = line.get("tono") if isinstance(line, dict) else None
    return t or story.get("tono", "normal")


def synth_tiempos(text, voice, model, api_key, tono):
    """MP3 + tiempo de cada palabra [{"w","t0","t1"}] (endpoint /with-timestamps)."""
    import base64
    body = {"text": text, "model_id": model, "language_code": "es", "voice_settings": TONOS.get(tono, TONOS["normal"])}
    req = urllib.request.Request(f"{API}/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_128",
                                 data=json.dumps(body).encode(), method="POST",
                                 headers={"xi-api-key": api_key, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            res = json.loads(r.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"ElevenLabs respondió HTTP {e.code}: {e.read().decode()[:500]}")
    al = res.get("alignment") or res.get("normalized_alignment")
    words, w, t0, t1 = [], "", None, None
    for ch, a, b in zip(al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]):
        if ch.isspace():
            if w:
                words.append({"w": w, "t0": t0, "t1": t1})
            w, t0 = "", None
            continue
        if t0 is None:
            t0 = a
        w, t1 = w + ch, b
    if w:
        words.append({"w": w, "t0": t0, "t1": t1})
    return base64.b64decode(res["audio_base64"]), words


def get_json(url, api_key, data=None):
    req = urllib.request.Request(url, data=json.dumps(data).encode() if data is not None else None,
                                 headers={"xi-api-key": api_key, "Content-Type": "application/json"},
                                 method="POST" if data is not None else "GET")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read() or b"{}")


def biblioteca(texto, n, model, api_key):
    """Busca en la biblioteca pública voces con acento de España, las añade a la cuenta y genera una muestra de cada una."""
    out_dir = os.path.join(CACHE, "muestras_es")
    os.makedirs(out_dir, exist_ok=True)
    vistas, cands = set(), []
    for q in ("language=es&accent=peninsular", "language=es&locale=es-ES", "language=es&search=spain", "language=es&search=castellano"):
        try:
            data = get_json(f"{API}/shared-voices?page_size=100&sort=cloned_by_count&{q}", api_key)
        except urllib.error.HTTPError as e:
            print(f"shared-voices {q}: HTTP {e.code} {e.read().decode()[:300]}")
            continue
        for v in data.get("voices", []):
            txt = " ".join(str(v.get(k) or "") for k in ("accent", "locale", "description", "name")).lower()
            if v["voice_id"] in vistas or not re.search(r"peninsular|castilian|es-es|spain|españa|castellano|madrid|españ", txt):
                continue
            if re.search(r"latin|mexic|argentin|colombi|venezol|chile|peru|caribe", txt):
                continue
            vistas.add(v["voice_id"])
            cands.append(v)
    cands.sort(key=lambda v: -(v.get("cloned_by_count") or 0))
    # mitad hombres, mitad mujeres
    elegidas = [v for v in cands if v.get("gender") == "male"][: (n + 1) // 2] + [v for v in cands if v.get("gender") == "female"][: n // 2]
    resumen = []
    for v in elegidas:
        name = re.sub(r"\W+", "_", v.get("name", v["voice_id"])).strip("_")[:40]
        info = {k: v.get(k) for k in ("name", "voice_id", "public_owner_id", "gender", "age", "accent", "locale",
                                     "description", "use_case", "cloned_by_count", "preview_url")}
        vid = v["voice_id"]
        try:
            added = get_json(f"{API}/voices/add/{v['public_owner_id']}/{v['voice_id']}", api_key, {"new_name": v.get("name", "es")})
            vid = added.get("voice_id", vid)
        except urllib.error.HTTPError as e:
            info["error_add"] = f"HTTP {e.code} {e.read().decode()[:300]}"
        info["voice_id_cuenta"] = vid
        try:
            open(os.path.join(out_dir, name + ".mp3"), "wb").write(synth(texto, vid, model, api_key, salir=False))
            info["muestra"] = f"voces_elevenlabs/muestras_es/{name}.mp3"
        except urllib.error.HTTPError as e:
            info["error_tts"] = f"HTTP {e.code} {e.read().decode()[:300]}"
        print(json.dumps(info, ensure_ascii=False))
        resumen.append(info)
    json.dump({"candidatas": len(cands), "voces": resumen}, open(os.path.join(out_dir, "voces.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)


EDGE_RATE = "+8%"


def edge_model(rate=EDGE_RATE):
    return f"edge{rate}"


def synth_edge(text, voice, model):
    """Voces neuronales gratis de Microsoft (paquete edge-tts). model = "edge+8%" lleva la velocidad."""
    import asyncio
    import edge_tts

    async def run():
        audio = b""
        async for chunk in edge_tts.Communicate(text, voice, rate=model[4:] or "+0%").stream():
            if chunk["type"] == "audio":
                audio += chunk["data"]
        return audio
    return asyncio.run(run())


def muestras_edge(texto):
    import asyncio
    import edge_tts

    out_dir = os.path.join(CACHE, "muestras_microsoft")
    os.makedirs(out_dir, exist_ok=True)
    voces = [v["ShortName"] for v in asyncio.run(edge_tts.list_voices()) if v["Locale"] == "es-ES"]
    for v in voces:
        path = os.path.join(out_dir, v.replace("es-ES-", "").replace("Neural", "") + ".mp3")
        open(path, "wb").write(synth_edge(texto, v, edge_model()))
        print("→", os.path.relpath(path, HERE), v)


def synth(text, voice, model, api_key, salir=True):
    if model.startswith("edge"):
        return synth_edge(text, voice, model)
    req = urllib.request.Request(
        f"{API}/text-to-speech/{voice}?output_format=mp3_44100_128",
        data=json.dumps({"text": text, "model_id": model, "language_code": "es", "voice_settings": SETTINGS}).encode(),
        headers={"xi-api-key": api_key, "Content-Type": "application/json", "Accept": "audio/mpeg"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        if not salir:
            raise
        sys.exit(f"ElevenLabs respondió HTTP {e.code}: {e.read().decode()[:500]}")


def voces_espanol(api_key):
    """Voces de la cuenta con acento de España (añadidas desde la biblioteca de voces)."""
    req = urllib.request.Request(f"{API}/voices", headers={"xi-api-key": api_key})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as e:  # la clave puede no tener permiso de lectura de voces
        print(f"No se pudieron listar las voces de la cuenta (HTTP {e.code}): {e.read().decode()[:300]}")
        return {}
    out = {}
    for v in data.get("voices", []):
        labels = " ".join(str(x) for x in (v.get("labels") or {}).values()).lower()
        if v.get("category") != "premade" and re.search(r"spain|castilian|españa|peninsular|spanish", labels + v.get("name", "").lower()):
            out[v["name"]] = v["voice_id"]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("storyboards", nargs="*")
    ap.add_argument("--voice")
    ap.add_argument("--model", default=MODEL)
    ap.add_argument("--muestras")
    ap.add_argument("--motor", default="elevenlabs", choices=["elevenlabs", "edge"])
    ap.add_argument("--biblioteca", type=int, default=0, help="con --muestras: probar N voces de España de la biblioteca")
    a = ap.parse_args()
    if a.motor == "edge" and a.muestras:
        return muestras_edge(a.muestras)
    api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not api_key and a.motor != "edge":
        sys.exit("Falta el secreto ELEVENLABS_API_KEY")

    if a.muestras and a.biblioteca:
        return biblioteca(a.muestras, a.biblioteca, a.model, api_key)
    if a.muestras:
        os.makedirs(os.path.join(CACHE, "muestras"), exist_ok=True)
        voces = {**MUESTRAS, **voces_espanol(api_key)}
        for name, vid in voces.items():
            path = os.path.join(CACHE, "muestras", re.sub(r"\W+", "_", name).strip("_") + ".mp3")
            open(path, "wb").write(synth(a.muestras, vid, a.model, api_key))
            print("→", os.path.relpath(path, HERE), vid)
        return

    files = [f for pat in a.storyboards for f in sorted(glob.glob(pat))]
    n = 0
    for f in files:
        story = json.load(open(f, encoding="utf-8"))
        vcfg = story.get("voice", {})
        voice = a.voice or vcfg.get("voice_id")
        model = vcfg.get("model") or (edge_model() if vcfg.get("engine") == "edge" else a.model)
        os.makedirs(CACHE, exist_ok=True)
        for sc in story["scenes"]:
            for line in sc["lines"]:
                text = line_text(line)
                tono = line_tono(story, line)
                vid = (line.get("voice_id") if isinstance(line, dict) else None) or voice
                path = os.path.join(CACHE, key(vid, model, text, tono) + ".mp3")
                if os.path.exists(path):
                    continue
                if tono and not model.startswith("edge"):
                    audio, words = synth_tiempos(text, vid, model, api_key, tono)
                    open(path, "wb").write(audio)
                    json.dump(words, open(path[:-4] + ".json", "w", encoding="utf-8"), ensure_ascii=False)
                else:
                    open(path, "wb").write(synth(text, vid, model, api_key))
                n += len(text)
        print("✓", os.path.relpath(f, HERE))
    print(f"{n} caracteres enviados a ElevenLabs")


if __name__ == "__main__":
    main()
