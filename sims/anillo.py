"""Anillo giratorio con hueco: cada bola que escapa estalla y nacen 2 bolas nuevas."""
import sys, math
import numpy as np
import pymunk
from common import *

OUT = sys.argv[1] if len(sys.argv) > 1 else "anillo.mp4"
CX, CY, R = W / 2, 1000, 430
BR = 15
DUR = 60.0
SUB = 4
GAP = math.radians(48)
MAXB = 420
rng = np.random.default_rng(7)
import os
DRY = os.environ.get('DRY')

space = pymunk.Space()
space.gravity = (0, 900)
ring = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
ring.position = (CX, CY)
ring.angle = math.pi / 2 - 1.2
ring.angular_velocity = 1.1
NSEG = 90
segs = []
for i in range(NSEG):
    a0 = GAP / 2 + (2 * math.pi - GAP) * i / NSEG
    a1 = GAP / 2 + (2 * math.pi - GAP) * (i + 1) / NSEG
    s = pymunk.Segment(ring, (R * math.cos(a0), R * math.sin(a0)), (R * math.cos(a1), R * math.sin(a1)), 6)
    s.elasticity = 1.0; s.friction = 0.0; s.collision_type = 1
    segs.append(s)
space.add(ring, *segs)

balls = []  # [body, shape, hue, trail]
uid = [0]


def spawn(x, y, hue=None):
    b = pymunk.Body(1, pymunk.moment_for_circle(1, 0, BR))
    b.position = (x, y)
    a = rng.uniform(0, 2 * math.pi); sp = rng.uniform(250, 520)
    b.velocity = (math.cos(a) * sp, math.sin(a) * sp)
    s = pymunk.Circle(b, BR)
    s.elasticity = 0.98; s.friction = 0.0; s.collision_type = 2
    uid[0] += 1
    s.uid = uid[0]
    space.add(b, s)
    balls.append([b, s, rng.random() if hue is None else hue, []])


hits = []


def post(arb, sp, data):
    if arb.is_first_contact:
        sh = arb.shapes[0] if arb.shapes[0].collision_type == 2 else arb.shapes[1]
        hits.append((sh.uid, arb.contact_point_set.points[0].point_a if arb.contact_point_set.points else None))


space.on_collision(1, 2, post_solve=post)

spawn(CX, CY - 150, 0.5)
aud = Audio(DUR + 1)
cv = Canvas(); c = cv.ctx
vid = Video(OUT)
particles = []
escaped = 0
nfr = int(DUR * FPS)
shatter_t = 54.0
shattered = False
ring_frag = []
sound_budget = 0
last_count = 1
for f in range(nfr):
    t = f / FPS
    # el anillo acelera poco a poco
    ring.angular_velocity = 1.1 + 0.9 * math.sin(t * 0.21) ** 2
    hits.clear()
    for _ in range(SUB):
        space.step(1 / FPS / SUB)
    # sonidos de rebote (limitados por frame)
    nsnd = 0
    for (u, p) in hits:
        if nsnd >= 3:
            break
        nsnd += 1
        aud.add(t + nsnd * 0.004, pluck(penta_freq(u % 15, 220)), 0.35)
    # escapes
    keep = []
    newb = []
    for bl in balls:
        b = bl[0]
        d = math.hypot(b.position.x - CX, b.position.y - CY)
        if d > R + 40 and not shattered:
            space.remove(b, bl[1])
            escaped += 1
            col = hsv(bl[2], 0.85, 1)
            for _ in range(16):
                a = rng.uniform(0, 2 * math.pi); sp = rng.uniform(100, 500)
                particles.append([b.position.x, b.position.y, math.cos(a) * sp, math.sin(a) * sp, 1.0, col])
            if escaped < 60 or rng.random() < 0.15:
                aud.add(t, bell(penta_freq(10 + escaped % 10, 220), 0.9), 0.45)
            newb.append(bl[2])
            if len(balls) + len(newb) < MAXB:
                newb.append((bl[2] + 0.13) % 1)
        elif d > 2500:
            space.remove(b, bl[1])
        else:
            keep.append(bl)
    balls = keep
    for hue in newb:
        spawn(CX + rng.uniform(-40, 40), CY + rng.uniform(-40, 40), hue)
    # final: el anillo se rompe
    if t >= shatter_t and not shattered:
        shattered = True
        space.remove(*segs)
        for i in range(NSEG):
            a = ring.angle + GAP / 2 + (2 * math.pi - GAP) * (i + 0.5) / NSEG
            x, y = CX + R * math.cos(a), CY + R * math.sin(a)
            ring_frag.append([x, y, math.cos(a) * rng.uniform(200, 700), math.sin(a) * rng.uniform(200, 700) - 300, a, rng.uniform(-8, 8)])
        aud.add(t, thud(60, 0.8), 1.2)
        for j in range(12):
            aud.add(t + j * 0.03, crack(j), 0.9)
        for j, n in enumerate([60, 64, 67, 72, 76]):
            aud.add(t + 0.2 + j * 0.09, bell(midi(n), 2.2), 0.4)
    if DRY:
        if f % 300 == 0: print(round(t), len(balls), file=sys.stderr)
        continue
    # ---- dibujo ----
    cv.clear()
    # fondo radial
    c.save()
    g = cairo.RadialGradient(CX, CY, 0, CX, CY, 900)
    g.add_color_stop_rgba(0, 0.08, 0.05, 0.18, 1); g.add_color_stop_rgba(1, 0.02, 0.02, 0.05, 1)
    c.set_source(g); c.paint(); c.restore()
    # trails
    for bl in balls:
        p = bl[0].position
        tr = bl[3]; tr.append((p.x, p.y))
        if len(tr) > 10:
            tr.pop(0)
        col = hsv(bl[2], 0.85, 1)
        if len(tr) > 2:
            for k in range(1, len(tr)):
                a = k / len(tr)
                c.set_source_rgba(*col, 0.35 * a); c.set_line_width(BR * 1.6 * a)
                c.move_to(*tr[k - 1]); c.line_to(*tr[k]); c.stroke()
    for bl in balls:
        p = bl[0].position
        col = hsv(bl[2], 0.85, 1)
        c.set_source_rgb(*col); c.arc(p.x, p.y, BR, 0, 2 * math.pi); c.fill()
        c.set_source_rgba(1, 1, 1, 0.75); c.arc(p.x - 4, p.y - 4, BR * 0.35, 0, 2 * math.pi); c.fill()
    # anillo
    if not shattered:
        hue = (t * 0.05) % 1
        for lw, al in [(22, 0.18), (10, 1.0)]:
            c.set_line_width(lw)
            c.set_source_rgba(*hsv(hue, 0.7, 1), al)
            c.arc(CX, CY, R + 4, ring.angle + GAP / 2, ring.angle + 2 * math.pi - GAP / 2); c.stroke()
        # marcas del hueco
        for s in (1, -1):
            a = ring.angle + s * GAP / 2
            c.set_source_rgb(1, 1, 1)
            c.arc(CX + (R + 4) * math.cos(a), CY + (R + 4) * math.sin(a), 9, 0, 2 * math.pi); c.fill()
    else:
        col = hsv((t * 0.05) % 1, 0.7, 1)
        c.set_line_width(10); c.set_source_rgb(*col)
        for fr in ring_frag:
            fr[0] += fr[2] / FPS; fr[1] += fr[3] / FPS; fr[3] += 900 / FPS; fr[4] += fr[5] / FPS
            dx, dy = -math.sin(fr[4]) * 15, math.cos(fr[4]) * 15
            c.move_to(fr[0] - dx, fr[1] - dy); c.line_to(fr[0] + dx, fr[1] + dy)
        c.stroke()
    # partículas
    nps = []
    for p in particles:
        p[0] += p[2] / FPS; p[1] += p[3] / FPS; p[3] += 600 / FPS; p[4] -= 1.4 / FPS
        if p[4] > 0:
            c.set_source_rgba(*p[5], p[4]); c.arc(p[0], p[1], 4 * p[4] + 1, 0, 2 * math.pi); c.fill()
            nps.append(p)
    particles = nps[-2500:]
    # contador
    n = len(balls)
    cv.text("BOLAS", W / 2, 250, 44, (0.65, 0.7, 0.9), cairo.FONT_WEIGHT_NORMAL)
    cv.text(str(n), W / 2, 420, 160, hsv((t * 0.05) % 1, 0.6, 1))
    cv.text("cada bola que escapa = 2 nuevas", W / 2, 1640, 40, (0.65, 0.7, 0.9), cairo.FONT_WEIGHT_NORMAL)
    if t < 2.5:
        cv.text("¿Cuántas habrá en 1 minuto?", W / 2, 1720, 50, (1, 1, 1), alpha=min(1, (2.5 - t) / 0.5))
    vid.write(glow(cv.array(), 0.9))

print("bolas finales", len(balls), "escapes", escaped, file=sys.stderr)
if not DRY: vid.close(aud.master(0.3))
