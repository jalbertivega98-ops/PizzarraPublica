# 🍕 Pizzaville

Mundo 3D persistente que crece con los comentarios de TikTok e Instagram. Empieza con una casa y un habitante, **Pizz**.

Todo es código propio y gratuito: React + TypeScript + Vite + React Three Fiber/Three.js + Drei + Zustand, SQLite (`node:sqlite`), Playwright + FFmpeg para el vídeo, voz de Microsoft Álvaro (edge-tts) generada en GitHub Actions.

## Cómo verlo

```bash
cd pizzaville
npm install
npm run dev            # http://localhost:5173  → mundo + panel de control
                       # http://localhost:5173/?episode=ep000  → episodio 0 en tiempo real
npm test               # 8 pruebas (países, terreno, parcelas, duplicados, persistencia)
```

## Exportar un episodio (MP4 vertical 1080×1920, 30 fps)

```bash
npm run build && npx vite preview --port 4173 &
node scripts/export.cjs ep000 --url http://localhost:4173 --out out/ep000      # ~1 h con render por software
node scripts/export.cjs ep000 --url http://localhost:4173 --from 0 --to 8      # prueba corta
```

Los fotogramas se calculan con un reloj determinista (`window.__pv.renderAt(t)`), así que cada fotograma es idéntico en cada exportación. El script añade la voz (`public/voz/<episodio>`), música y efectos originales generados por código (`scripts/audio.py`) y subtítulos con resaltado palabra a palabra (ASS + libass).

**Voz**: `voz/ep000.json` es el guion. Para regenerarla: Actions → «Voces ElevenLabs» (voces.yml) con `motor=edge` y `storyboards=pizzaville:ep000.json`, en esta rama. Si una frase cambia de texto, el episodio ignora el audio viejo hasta que se regenera.

## Estructura

| Carpeta | Qué hay |
|---|---|
| `src/world/` | Modelo puro del mundo (semilla `20261114`): terreno, río, lago, camino, parcelas, países. Compartido por el navegador y el servidor. |
| `src/scene/` | Escena 3D: terreno con malla de anillos hasta el horizonte, agua, cielo con ciclo día/noche, árboles por zonas con nivel de detalle, hierba y flores con viento, nubes, pájaros, casas procedurales por etapas, Pizz y habitantes con esqueleto y animaciones procedurales, banderas (flag-icons, MIT). |
| `src/episodes/` | Episodios guionizados. `ep000` = presentación (60 s). |
| `src/engine/` | Reloj determinista, cámaras por fotogramas clave con cortes, caminar por rutas, voz y sincronía labial. |
| `server/api.ts` | API + SQLite. Mundo **oficial** y de **pruebas** separados. |
| `data/official/world.json` | Copia del mundo oficial (se versiona en git; si falta la base SQLite, se reconstruye desde aquí). |
| `scripts/` | Capturas (`shots.cjs`), exportación (`export.cjs`), audio (`audio.py`). |

## Reglas del mundo

- Un comentario procesado dos veces no crea otra casa (`comment_id` único). Una cuenta = una vivienda principal.
- Cada habitante recibe la siguiente parcela libre junto al camino, ordenadas por distancia a la casa de Pizz. La posición se guarda y no cambia.
- La apariencia sale de un número aleatorio interno, nunca de los datos del comentario.
- Los nombres se pueden ocultar y los habitantes retirar. Las importaciones CSV entran como «pendiente» y hay que aprobarlas.
- Cada cambio escribe la base SQLite, la copia `world.json` (escritura atómica) y una copia con fecha (se guardan las 30 últimas).
- Restaurar el mundo oficial exige escribir RESTAURAR.

CSV de comentarios: `comment_id,platform,account_id,texto`.
