#!/bin/bash
# par.sh <ep> <outdir> [workers] — render paralelo de fotogramas + vídeo mudo
EP=$1; OUT=$(realpath -m $2); NW=${3:-3}; FPS=30
mkdir -p $OUT
DUR=$(node -e "console.log(Math.round(+require('fs').readFileSync('/dev/stdin','utf8')*$FPS))" <<< "$(grep -oP 'DUR = \K[0-9.]+' $(dirname $0)/$EP.js 2>/dev/null || echo 20.5)")
N=$DUR; STEP=$(( (N + NW - 1) / NW ))
for i in $(seq 0 $((NW-1))); do node $(dirname $0)/render.cjs $EP --out $OUT --from $((i*STEP)) --to $(( (i+1)*STEP < N ? (i+1)*STEP : N )) > $OUT/w$i.log 2>&1 & done
wait
ffmpeg -y -loglevel error -framerate $FPS -i $OUT/frames/f%05d.jpg -c:v libx264 -pix_fmt yuv420p -preset slow -b:v 8M -maxrate 9M -bufsize 16M $OUT/mudo.mp4
echo done $N frames
