# Motor TERROR — «La casa» (serie interactiva)
Casa 3D en primera persona con linterna (Three.js), postproceso VHS (grano, viñeta, aberración), textos tipo máquina de escribir, sonido 100 % sintetizado (sonido.py, sin licencias). Gratis, sin créditos.

- Episodio = `epXX.js` (escena + cámara por keyframes + EVENTS de sonido + textos). Motor común en `engine.js`.
- Prueba de fotogramas: `node render.cjs ep00 --snap 1.5,7.5 --out out`
- Render completo: `npm i; ./par.sh ep00 out/ep00 3` (~20 min para 20 s con 3 procesos) → `out/ep00/frames` + `mudo.mp4`
- Audio: `python3 sonido.py out/ep00/timeline.json out/ep00/audio.wav` y mezclar con ffmpeg (-b:v 8M para quedar < 25 MB).
- Portada: `python3 portada.py <fotograma> portada.png "EPISODIO N" "linea roja" "linea 2"`
