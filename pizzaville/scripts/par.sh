#!/bin/bash
# render en paralelo: scripts/par.sh ep000 60 N rw rh outdir
EP=$1; DUR=$2; N=$3; RW=$4; RH=$5; OUT=$6
mkdir -p $OUT; : > $OUT/list.txt
for i in $(seq 0 $((N-1))); do
  A=$(python3 -c "print(round($DUR*$i/$N*30)/30)"); B=$(python3 -c "print(round($DUR*($i+1)/$N*30)/30)")
  node scripts/export.cjs $EP --from $A --to $B --rw $RW --rh $RH --url http://localhost:4173 --out $OUT/p$i --frames-only > $OUT/p$i.log 2>&1 &
  echo "file '$OUT/p$i/video_silent.mp4'" >> $OUT/list.txt
done
wait
ffmpeg -v error -y -f concat -safe 0 -i $OUT/list.txt -c copy $OUT/concat.mp4
node scripts/export.cjs $EP --rw $RW --rh $RH --url http://localhost:4173 --out $OUT --video $OUT/concat.mp4 2>&1 | tail -3
