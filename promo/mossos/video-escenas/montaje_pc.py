# Monta el video de Mossos: escenas s01..s10.png + voz-01..10.mp3 (una frase por escena).
# Uso: python montaje_pc.py <carpeta_escenas> <carpeta_voz> <salida.mp4>   (necesita ffmpeg y ffprobe en el PATH)
import subprocess, sys, os, json

esc, voz, out = sys.argv[1], sys.argv[2], sys.argv[3]
PRE, POST, X = 0.25, 0.45, 0.3


def dur(f):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", f],
                       capture_output=True, text=True, check=True).stdout
    return float(json.loads(r)["format"]["duration"])


mp3 = [os.path.join(voz, f"voz-{i:02d}.mp3") for i in range(1, 11)]
durs = [round(dur(f) + PRE + POST, 2) for f in mp3]
args = ["ffmpeg", "-y", "-loglevel", "error"]
for i, d in enumerate(durs, 1):
    args += ["-loop", "1", "-t", f"{d + X:.2f}", "-i", os.path.join(esc, f"s{i:02d}.png")]
for f in mp3:
    args += ["-i", f]
n = len(durs)
flt, prev, off = [], "[0:v]", 0
for i in range(1, n):
    off += durs[i - 1]
    flt.append(f"{prev}[{i}:v]xfade=transition=fade:duration={X}:offset={off:.2f}[v{i}]")
    prev = f"[v{i}]"
flt.append(f"{prev}format=yuv420p,scale=1080:1920[vout]")
for i, d in enumerate(durs):
    flt.append(f"[{n + i}:a]aresample=44100,adelay={int(PRE * 1000)}:all=1,apad=whole_dur={d}[a{i}]")
flt.append("".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1,apad=pad_dur={X}[aout]")
args += ["-filter_complex", ";".join(flt), "-map", "[vout]", "-map", "[aout]", "-r", "30",
         "-c:v", "libx264", "-crf", "21", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", out]
subprocess.run(args, check=True)
print(out, round(sum(durs) + X, 1), "s")
