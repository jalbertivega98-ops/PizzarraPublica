# Motor «Historias por chat»

Vídeos verticales (1080x1920, 30 fps) de una conversación que se escribe sola: «escribiendo…», burbujas, mapa, avisos de grupo, tecleo en la caja de texto y tarjeta final. Todo es código y gratis. Los sonidos están sintetizados y no hay samples con copyright.

```
node chat/render.cjs chat/guiones/ep01_papa_gimnasio.json salida/          # vídeo completo
node chat/render.cjs chat/guiones/ep01_papa_gimnasio.json salida/ --preview 2,10,30   # solo capturas
```

Guion (JSON): `hook`, `chat` (nombre del chat), `yo`, `personas{id:{nombre,color}}`, `mensajes[{de, texto, tipo?: "mapa", pausa?}]` (`de: "sistema"` = aviso centrado), `final`, `marca` (opcional).
Tiempos automáticos: escribir y leer dependen de la longitud del texto, y `pausa` añade segundos tras el mensaje.
Necesita playwright (preinstalado), ffmpeg, numpy.
