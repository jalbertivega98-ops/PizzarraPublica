"""Una bola cae rebotando en tubos; cada rebote toca una nota de «Para Elisa» (Beethoven, dominio público)."""
import sys, math
import numpy as np
from common import *

OUT = sys.argv[1] if len(sys.argv) > 1 else "bola_musical.mp4"
rng = np.random.default_rng(11)
G = 2600.0
DT = 0.32
BR = 18
PADL, PADT = 120, 20
T0 = 1.3  # primera nota

pick = [[76], [75]]
m1 = [[76], [75], [76], [71], [74], [72]]
m2 = [[69, 45], [52], [57], [60], [64], [69]]
m3 = [[71, 40], [52], [56], [64], [68], [71]]
m4 = [[72, 45], [52], [57], [64], [76], [75]]
m7 = [[71, 40], [52], [56], [64], [72], [71]]
m8a = [[69, 45], [52], [57], None, [76], [75]]
m8b = [[69, 45], [52], [57], [71], [72], [74]]
m9 = [[76, 48], [55], [60], [67], [77], [76]]
m10 = [[74, 43], [55], [59], [65], [76], [74]]
m11 = [[72, 45], [52], [57], [64], [74], [72]]
m12 = [[71, 40], [52], [56], None, [76], [75]]
fin = [[69, 45, 57], None, None]
A = m1 + m2 + m3 + m4 + m1 + m2 + m7
SEQ = pick + A + m8a + A + m8b + m9 + m10 + m11 + m12 + A + fin

# ---- notas -> tiempos ----
notes = []  # (t, [midis])
for i, s in enumerate(SEQ):
    if s:
        notes.append((T0 + i * DT, s))
N = len(notes)

# ---- trayectoria determinista ----
P = [(540.0, 700.0)]
VOUT = []
x, y = P[0]
direc = 1
for i in range(N):
    T = notes[i + 1][0] - notes[i][0] if i + 1 < N else 0.9
    mag = rng.uniform(140, 300) * min(T / DT, 1.6)
    nx = x + direc * mag
    if nx < 150 or nx > 930:
        direc = -direc; nx = x + direc * mag
    nx = min(max(nx, 150), 930)
    vx = (nx - x) / T
    vy0 = -0.33 * G * T
    VOUT.append((vx, vy0, T))
    ny = y + vy0 * T + 0.5 * G * T * T
    if i + 1 < N:
        P.append((nx, ny))
    x, y = nx, ny
    direc = -direc if rng.random() < 0.8 else direc
# velocidad de llegada al primer tubo: caída libre desde arriba
FALL = 0.62
VIN = [(0.0, G * FALL)]
for i in range(N - 1):
    vx, vy0, T = VOUT[i]
    VIN.append((vx, vy0 + G * T))
pads = []
for i in range(N):
    vin, vo = VIN[i], VOUT[i][:2]
    nx_, ny_ = vo[0] - vin[0], vo[1] - vin[1]
    l = math.hypot(nx_, ny_); nx_, ny_ = nx_ / l, ny_ / l
    cx, cy = P[i][0] - nx_ * (BR + PADT / 2), P[i][1] - ny_ * (BR + PADT / 2)
    m = notes[i][1][0]
    pads.append(dict(c=(cx, cy), n=(nx_, ny_), hue=((m % 12) / 12 * 0.85 + 0.5) % 1, t=notes[i][0]))


def ball_pos(t):
    if t < notes[0][0]:
        tt = max(0.0, t - (notes[0][0] - FALL))
        return P[0][0], P[0][1] - 0.5 * G * FALL ** 2 + 0.5 * G * tt * tt
    i = min(int(np.searchsorted([n[0] for n in notes], t, side="right")) - 1, N - 1)
    vx, vy0, T = VOUT[i]
    dt = t - notes[i][0]
    return P[i][0] + vx * dt, P[i][1] + vy0 * dt + 0.5 * G * dt * dt


TEND = notes[-1][0]
ZOOM0, ZOOMD = TEND + 0.9, 2.8
DUR = ZOOM0 + ZOOMD + 3.0
ys = [p[1] for p in P]
print(f"{N} notas, dur {DUR:.1f}s, altura {max(ys)-min(ys):.0f}px", file=sys.stderr)

# ---- audio ----
aud = Audio(DUR)
for (t, ms) in notes:
    for m in ms:
        if m >= 60:
            aud.add(t, bell(midi(m), 1.8, 0.5), 0.55)
        else:
            aud.add(t, bell(midi(m), 1.4, 0.3), 0.32)
    aud.add(t, click(int(t * 100), 0.02, 4000), 0.05)
aud.add(ZOOM0 + 0.3, bell(midi(81), 3.0), 0.25)
audio = aud.master(0.4)

# ---- render ----
cv = Canvas(); c = cv.ctx
vid = Video(OUT)
cam = P[0][1] - 0.5 * G * FALL ** 2 + 300
trail = []
path = []
parts = []
ripples = []
nfr = int(DUR * FPS)
next_hit = 0
miny, maxy = min(ys) - 400, max(ys) + 300
for f in range(nfr):
    t = f / FPS
    bx, by = ball_pos(t)
    if t > TEND + 0.9:
        bx, by = P[-1][0] + VOUT[-1][0] * 0.9, P[-1][1] + VOUT[-1][1] * 0.9 + 0.5 * G * 0.81
    cam += (by - cam) * 0.12
    while next_hit < N and notes[next_hit][0] <= t:
        p = pads[next_hit]
        col = hsv(p["hue"], 0.8, 1)
        for _ in range(14):
            a = rng.uniform(0, 2 * math.pi); sp = rng.uniform(150, 520)
            parts.append([P[next_hit][0], P[next_hit][1], math.cos(a) * sp + p["n"][0] * 200, math.sin(a) * sp + p["n"][1] * 200, 1.0, col])
        ripples.append([p["c"][0], p["c"][1], 0.0, col])
        next_hit += 1
    path.append((bx, by))
    # transformación de cámara
    z = ease((t - ZOOM0) / ZOOMD)
    fit = min(1.0, (H - 260) / (maxy - miny))
    scale = 1 + (fit - 1) * z
    cy_world = cam + ((miny + maxy) / 2 - cam) * z
    cv.clear()
    c.save()
    c.translate(W / 2, H * 0.47 + (H * 0.5 - H * 0.47) * z)
    c.scale(scale, scale)
    c.translate(-W / 2, -cy_world)
    lw = 1 / max(scale, 0.25)
    # recorrido tenue
    if len(path) > 2:
        c.set_line_width(3 * lw); c.set_source_rgba(0.6, 0.7, 1.0, 0.18)
        c.move_to(*path[0])
        for q in path[1::2]:
            c.line_to(*q)
        c.stroke()
    # tubos
    vis_top = cy_world - H / 2 / scale - 200
    vis_bot = cy_world + H / 2 / scale + 200
    for i, p in enumerate(pads):
        if not (vis_top < p["c"][1] < vis_bot):
            continue
        nx_, ny_ = p["n"]
        tx, ty = -ny_, nx_
        x0, y0 = p["c"][0] - tx * PADL / 2, p["c"][1] - ty * PADL / 2
        x1, y1 = p["c"][0] + tx * PADL / 2, p["c"][1] + ty * PADL / 2
        col = hsv(p["hue"], 0.75, 1)
        if t < p["t"]:
            a = 0.35; fl = 0
        else:
            fl = math.exp(-(t - p["t"]) * 5)
            a = 0.75 + 0.25 * fl
        c.set_line_width(PADT + 10 * fl); c.set_source_rgba(*col, a)
        c.move_to(x0, y0); c.line_to(x1, y1); c.stroke()
        c.set_line_width(PADT * 0.35); c.set_source_rgba(1, 1, 1, 0.25 + 0.6 * fl)
        c.move_to(x0 + tx * 8, y0 + ty * 8); c.line_to(x1 - tx * 8, y1 - ty * 8); c.stroke()
    # ondas
    nr = []
    for r in ripples:
        r[2] += 1 / FPS
        if r[2] < 0.6:
            c.set_line_width(4 * lw); c.set_source_rgba(*r[3], 1 - r[2] / 0.6)
            c.arc(r[0], r[1], 20 + r[2] * 220, 0, 2 * math.pi); c.stroke(); nr.append(r)
    ripples = nr
    # partículas
    npx = []
    for q in parts:
        q[0] += q[2] / FPS; q[1] += q[3] / FPS; q[3] += 1200 / FPS; q[4] -= 1.6 / FPS
        if q[4] > 0:
            c.set_source_rgba(*q[5], q[4]); c.arc(q[0], q[1], 4 * q[4] + 1.5, 0, 2 * math.pi); c.fill(); npx.append(q)
    parts = npx[-1500:]
    # estela + bola
    trail.append((bx, by)); trail = trail[-14:]
    for k in range(1, len(trail)):
        a = k / len(trail)
        c.set_source_rgba(1, 1, 1, 0.4 * a); c.set_line_width(BR * 1.8 * a)
        c.move_to(*trail[k - 1]); c.line_to(*trail[k]); c.stroke()
    if z < 1:
        c.set_source_rgb(1, 1, 1); c.arc(bx, by, BR, 0, 2 * math.pi); c.fill()
    c.restore()
    if t < 3.2:
        a = min(1, t / 0.4, (3.2 - t) / 0.6)
        cv.text("Para Elisa", W / 2, 260, 84, (1, 1, 1), alpha=a)
        cv.text("Beethoven · solo con rebotes", W / 2, 330, 40, (0.7, 0.75, 0.95), cairo.FONT_WEIGHT_NORMAL, alpha=a)
    if z > 0.6:
        a = ease((t - ZOOM0 - ZOOMD * 0.6) / 1.0)
        cv.text(f"{N} rebotes · {N} notas", W / 2, 120, 50, (1, 1, 1), alpha=a)
    vid.write(glow(cv.array(), 1.0))
vid.close(audio)
