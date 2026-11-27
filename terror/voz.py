#!/usr/bin/env python3
"""Genera la narración de cada episodio (se ejecuta en GitHub Actions).
motor "edge" (gratis, Microsoft) o "elevenlabs" (secreto ELEVENLABS_API_KEY).
uso: python3 terror/voz.py terror/guiones/ep00.json  -> terror/voz/<ep>[_<salida>]/<id>.mp3
No regenera un mp3 que ya exista (no gasta créditos dos veces)."""
import asyncio, json, os, sys, urllib.request

def eleven(g, f, prev, nxt, dst):
    body = {'text': f['t'], 'model_id': g.get('modelo', 'eleven_multilingual_v2'), 'voice_settings': g.get('ajustes', {})}
    if prev: body['previous_text'] = prev
    if nxt: body['next_text'] = nxt
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{g['voz']}?output_format=mp3_44100_128",
        data=json.dumps(body).encode(), headers={'xi-api-key': os.environ['ELEVENLABS_API_KEY'], 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=120) as r: open(dst, 'wb').write(r.read())
    except urllib.error.HTTPError as e:
        print('ERROR', e.code, e.read().decode()[:400]); raise

async def main(path):
    g = json.load(open(path))
    base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(path))), 'voz')
    out = os.path.join(base, g['ep'] + ('_' + g['salida'] if g.get('salida') else '')); os.makedirs(out, exist_ok=True)
    fr = g['frases']
    for i, f in enumerate(fr):
        dst = os.path.join(out, f['id'] + '.mp3')
        if os.path.exists(dst): continue
        if g.get('motor') == 'elevenlabs':
            eleven(g, f, fr[i - 1]['t'] if i else None, fr[i + 1]['t'] if i + 1 < len(fr) else None, dst)
        else:
            import edge_tts
            await edge_tts.Communicate(f['t'], f.get('voz', g['voz']), rate=f.get('rate', g.get('rate', '+0%')), pitch=f.get('pitch', g.get('pitch', '+0Hz'))).save(dst)
        print('ok', dst)

for p in sys.argv[1:]: asyncio.run(main(p))
