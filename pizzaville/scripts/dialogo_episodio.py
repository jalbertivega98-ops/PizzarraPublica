"""Convierte un diálogo de ElevenLabs (text-to-dialogue/with-timestamps) en líneas de episodio de pareja.
python3 scripts/dialogo_episodio.py <dialogo.json> <episodio> <voice_id_de_ella> [lead=0.5]
→ public/voz/<episodio>/lNN.json (palabras) + src/episodes/<episodio>_data.ts (texto, inicio, quién habla).
Quita las etiquetas [..] y los «...» sueltos; el audio se usa entero con export.cjs --audio <mp3> --audio-at <lead>."""
import json, os, re, sys
src, ep, her = sys.argv[1:4]; LEAD = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
d = json.load(open(src)); al = d['alignment']
ch, st, en = al['characters'], al['character_start_times_seconds'], al['character_end_times_seconds']
os.makedirs(f'public/voz/{ep}', exist_ok=True)
out = []
for k, s in enumerate(d['voice_segments']):
    words, cur, tag = [], None, False
    for i in range(s['character_start_index'], s['character_end_index']):
        c = ch[i]
        if c == '[': tag = True; continue
        if c == ']': tag = False; continue
        if tag: continue
        if c.isspace():
            if cur: words.append(cur); cur = None
            continue
        if cur is None: cur = {'w': '', 't': st[i], 'e': en[i]}
        cur['w'] += c; cur['e'] = en[i]
    if cur: words.append(cur)
    words = [w for w in words if re.search(r'\w', w['w'])]
    if not words: continue
    t0 = words[0]['t']; lid = f'l{len(out) + 1:02d}'; text = ' '.join(w['w'] for w in words)
    W = [{'w': re.sub(r'[^\wáéíóúüñÁÉÍÓÚÑ]', '', w['w']), 't': round(w['t'] - t0, 3), 'd': round(max(0.05, w['e'] - w['t']), 3)} for w in words]
    json.dump({'text': text, 'words': W}, open(f'public/voz/{ep}/{lid}.json', 'w'), ensure_ascii=False)
    out.append({'id': lid, 'text': text, 'at': round(t0 + LEAD, 3), 'her': s['voice_id'] == her})
open(f'src/episodes/{ep}_data.ts', 'w').write(f'// generado por scripts/dialogo_episodio.py desde {os.path.relpath(src)}\nexport const CONV = ' + json.dumps(out, ensure_ascii=False, indent=1) + ' as const\n')
for o in out: print(o)
