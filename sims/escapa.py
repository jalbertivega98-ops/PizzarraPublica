"""Formato viral «¿Escapará la bola?»: anillos concéntricos que giran con un hueco.
Cada rebote toca la siguiente nota de «En la gruta del rey de la montaña» (Grieg, dominio público),
que acelera sola porque la bola va cada vez más rápido. Cada anillo que atraviesa estalla."""
import sys, math, os
import numpy as np
from common import *

OUT = sys.argv[1] if len(sys.argv) > 1 else "escapa.mp4"
DRY = os.environ.get("DRY")
SEED = int(os.environ.get("SEED", "1"))
rng = np.random.default_rng(SEED)
CX, CY = W / 2, 1010
NR = 16
R0, DR = 140, 24
GAP = math.radians(float(os.environ.get("GAPDEG", "38")))
G = 1400.0
MAXT = 45.0
SUB = 8

# melodía (MIDI) – frase repetida, como en la obra
A = [57, 59, 60, 62, 64, 60, 64, 63, 59, 63, 62, 58, 62, 57, 59, 60, 62, 64, 60, 64, 69, 67, 64, 60, 64, 67]
B = [n + 7 for n in A[:20]] + [76, 74, 71, 67, 71, 74]
MEL = (A + B) * 6

rings = []
for i in range(NR):
    rings.append(dict(r=R0 + i * DR, ang=rng.uniform(0, 2 * math.pi), w=(1.0 + 0.04 * i) * (1 if i % 2 == 0 else -1) * 1.1,
                      alive=True, hue=(i / NR * 0.85) % 1, flash=0.0))

br = 16.0
p = np.array([CX + 20.0, CY - 40.0]); v = np.array([260.0, -100.0])
note_i = 0
events = []  # (t, tipo, dato)
frags, parts = [], []
cur = 0
t = 0.0
shake = 0.0
trail = []
done_t = None

aud = Audio(MAXT + 4) if not DRY else None
cv = Canvas() if not DRY else None
vid = Video(OUT) if not DRY else None
f = 0
while True:
    t = f / FPS
    if done_t is not None and t > done_t + 3.2:
        break
    if t > MAXT:
        break
    for _ in range(SUB):
        dt = 1 / FPS / SUB
        v[1] += G * dt
        p += v * dt
        for rg in rings:
            rg["ang"] += rg["w"] * dt
        if cur < NR:
            rg = rings[cur]
            d = p - [CX, CY]
            dist = math.hypot(*d)
            if dist + br >= rg["r"]:
                a = math.atan2(d[1], d[0])
                rel = (a - rg["ang"]) % (2 * math.pi)
                in_gap = rel < GAP / 2 or rel > 2 * math.pi - GAP / 2
                if in_gap:
                    if dist - br > rg["r"] + 4:
                        # ¡atraviesa! el anillo estalla
                        rg["alive"] = False
                        events.append((t, "rompe", cur))
                        col = hsv(rg["hue"], 0.8, 1)
                        if not DRY:
                            for k in range(60):
                                aa = rg["ang"] + GAP / 2 + (2 * math.pi - GAP) * (k + 0.5) / 60
                                sp = rng.uniform(150, 650)
                                frags.append([CX + rg["r"] * math.cos(aa), CY + rg["r"] * math.sin(aa),
                                              math.cos(aa) * sp, math.sin(aa) * sp - 200, aa + math.pi / 2, rng.uniform(-9, 9), col, 1.5])
                            for k in range(40):
                                aa = rng.uniform(0, 2 * math.pi); sp = rng.uniform(100, 900)
                                parts.append([p[0], p[1], math.cos(aa) * sp, math.sin(aa) * sp, 1.0, col])
                            shake = 1.0
                            aud.add(t, thud(55, 0.6), 0.9)
                            aud.add(t, crack(cur), 0.8)
                            aud.add(t, bell(midi(84 + [0, 2, 4, 7, 9][cur % 5]), 1.5), 0.3)
                        cur += 1
                        br += 1.2
                        if cur == NR:
                            done_t = t
                else:
                    n = d / dist
                    vn = v @ n
                    if vn > 0:
                        v -= 2 * vn * n
                        # pequeño empujón aleatorio para que no se repita
                        tang = np.array([-n[1], n[0]])
                        v += tang * rng.uniform(-40, 40)
                        sp = math.hypot(*v)
                        target = min(2300, max(sp * 1.01, 1150))
                        v *= target / sp
                        p[:] = [CX, CY] + n * (rg["r"] - br - 0.5)
                        events.append((t, "rebote", note_i))
                        rg["flash"] = 1.0
                        if not DRY:
                            m = MEL[note_i % len(MEL)]
                            aud.add(t, bell(midi(m + 12), 1.0, 0.6), 0.55)
                            aud.add(t, pluck(midi(m), 0.35), 0.25)
                            for k in range(8):
                                aa = math.atan2(-n[1], -n[0]) + rng.uniform(-1, 1); s2 = rng.uniform(80, 400)
                                parts.append([p[0] + n[0] * br, p[1] + n[1] * br, math.cos(aa) * s2, math.sin(aa) * s2, 0.8, hsv(rg["hue"], 0.6, 1)])
                        note_i += 1
        if done_t is not None:
            # bola libre: se aleja con gravedad
            pass
    if DRY:
        f += 1
        continue
    # ---------- dibujo ----------
    cv.clear()
    c = cv.ctx
    sx = (rng.uniform(-1, 1) * 18 * shake); sy = (rng.uniform(-1, 1) * 18 * shake)
    shake *= 0.85
    g = cairo.RadialGradient(CX, CY, 50, CX, CY, 1100)
    g.add_color_stop_rgb(0, 0.07, 0.04, 0.16); g.add_color_stop_rgb(1, 0.01, 0.01, 0.03)
    c.set_source(g); c.paint()
    c.save(); c.translate(sx, sy)
    for i, rg in enumerate(rings):
        if not rg["alive"]:
            continue
        col = hsv(rg["hue"] + t * 0.05, 0.85, 1)
        fl = rg["flash"]; rg["flash"] *= 0.8
        active = (i == cur)
        lw = 9 if active else 6
        c.set_line_width(lw + 6 * fl)
        c.set_source_rgba(*col, 1.0 if active else 0.75)
        c.new_path()
        c.arc(CX, CY, rg["r"], rg["ang"] + GAP / 2, rg["ang"] + 2 * math.pi - GAP / 2)
        c.stroke()
    # fragmentos
    nf = []
    for fr in frags:
        fr[0] += fr[2] / FPS; fr[1] += fr[3] / FPS; fr[3] += 1400 / FPS; fr[4] += fr[5] / FPS; fr[7] -= 1 / FPS
        if fr[7] > 0 and fr[1] < H + 50:
            dx, dy = math.cos(fr[4]) * 11, math.sin(fr[4]) * 11
            c.set_source_rgba(*fr[6], min(1, fr[7])); c.set_line_width(6)
            c.move_to(fr[0] - dx, fr[1] - dy); c.line_to(fr[0] + dx, fr[1] + dy); c.stroke(); nf.append(fr)
    frags = nf[-3000:]
    npx = []
    for q in parts:
        q[0] += q[2] / FPS; q[1] += q[3] / FPS; q[3] += 900 / FPS; q[4] -= 1.6 / FPS
        if q[4] > 0:
            c.set_source_rgba(*q[5], q[4]); c.arc(q[0], q[1], 4 * q[4] + 1, 0, 2 * math.pi); c.fill(); npx.append(q)
    parts = npx[-2500:]
    # estela arcoíris + bola
    trail.append((p[0], p[1])); trail = trail[-22:]
    for k in range(1, len(trail)):
        a = k / len(trail)
        c.set_source_rgba(*hsv(t * 0.3 + k * 0.03, 0.8, 1), 0.55 * a); c.set_line_width(br * 2 * a)
        c.move_to(*trail[k - 1]); c.line_to(*trail[k]); c.stroke()
    c.new_path(); c.set_source_rgb(1, 1, 1); c.arc(p[0], p[1], br, 0, 2 * math.pi); c.fill()
    c.restore()
    # textos
    left = NR - cur
    if done_t is None:
        cv.text("¿ESCAPARÁ LA BOLA?", W / 2, 250, 78, (1, 1, 1))
        cv.text(f"{left}", W / 2, 420, 140, hsv(rings[min(cur, NR - 1)]["hue"] + t * 0.05, 0.6, 1))
        cv.text("anillos" if left != 1 else "¡ÚLTIMO ANILLO!", W / 2, 480, 44 if left != 1 else 56, (0.75, 0.8, 1.0), cairo.FONT_WEIGHT_NORMAL if left != 1 else cairo.FONT_WEIGHT_BOLD)
        cv.text("espera al último anillo…", W / 2, 1640, 42, (0.75, 0.8, 1.0), cairo.FONT_WEIGHT_NORMAL, alpha=0.9)
    else:
        a = ease((t - done_t) / 0.4)
        cv.text("¡ESCAPÓ!", W / 2, 360, 150, (1, 0.9, 0.2), alpha=a)
        cv.text(f"en {done_t:.1f} segundos", W / 2, 450, 50, (1, 1, 1), cairo.FONT_WEIGHT_NORMAL, alpha=a)
    vid.write(glow(cv.array(), 1.0))
    f += 1

nb = sum(1 for e in events if e[1] == "rebote")
print(f"seed {SEED}: escapa en {done_t}, rebotes {nb}, anillos {cur}, tiempos {[round(e[0],1) for e in events if e[1]=="rompe"]}", file=sys.stderr)
if not DRY:
    if done_t is not None:
        for j, n in enumerate([57, 64, 69, 72, 76, 81]):
            aud.add(done_t + 0.05 + j * 0.07, bell(midi(n), 2.5), 0.35)
    vid.close(aud.master(0.3))
