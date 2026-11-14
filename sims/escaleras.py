"""Objetos hechos de piezas caen por una escalera infinita y se van partiendo en trozos con cada golpe."""
import sys, math, os
import numpy as np
import pymunk
from common import *

OUT = sys.argv[1] if len(sys.argv) > 1 else "escaleras.mp4"
DRY = os.environ.get("DRY")
K = float(os.environ.get("K", "60"))
DUR = float(os.environ.get("DUR", "60"))
rng = np.random.default_rng(21)
SUB = 4
SW, SH = 140, 100
NST = 260
PS = 26

space = pymunk.Space()
space.gravity = (0, 1500)
stairs = []
x, y = -400, 600
for i in range(NST):
    a = (x, y); b = (x + SW, y); d = (x + SW, y + SH)
    for p, q in ((a, b), (b, d)):
        s = pymunk.Segment(space.static_body, p, q, 3)
        s.elasticity = 0.4; s.friction = 0.7; s.collision_type = 1
        space.add(s)
    stairs.append((a, b, d))
    x += SW; y += SH


def stair_y(x):
    return 600 + math.floor((x + 400) / SW) * SH


chunks = []


def make_chunk(cells, pos, angle, vel, angv, hue, obj):
    """cells: lista de (lx, ly, tono) en coordenadas locales respecto al centroide."""
    n = len(cells)
    mom = sum(pymunk.moment_for_box(1, (PS, PS)) + (cx * cx + cy * cy) for cx, cy, _ in cells)
    b = pymunk.Body(n, mom)
    b.position = pos; b.angle = angle; b.velocity = vel; b.angular_velocity = angv
    shapes = []
    for (cx, cy, _) in cells:
        h = PS / 2 - 0.5
        s = pymunk.Poly(b, [(cx - h, cy - h), (cx + h, cy - h), (cx + h, cy + h), (cx - h, cy + h)])
        s.elasticity = 0.35; s.friction = 0.6; s.collision_type = 2
        shapes.append(s)
    space.add(b, *shapes)
    ch = dict(body=b, shapes=shapes, cells=cells, hue=hue, obj=obj, cool=0.15, flash=0.0)
    for s in shapes:
        s.chunk = ch
    chunks.append(ch)
    obj["chunks"].append(ch)
    return ch


def remove_chunk(ch):
    space.remove(ch["body"], *ch["shapes"])
    chunks.remove(ch)
    ch["obj"]["chunks"].remove(ch)


def shape_cells(kind):
    if kind == "cubo":
        g = [(i, j) for i in range(7) for j in range(7)]
    elif kind == "torre":
        g = [(i, j) for i in range(4) for j in range(11)]
    elif kind == "bola":
        g = [(i, j) for i in range(-5, 6) for j in range(-5, 6) if i * i + j * j <= 4.6 ** 2]
    elif kind == "piramide":
        g = [(i, j) for j in range(7) for i in range(-j, j + 1)]
    elif kind == "anillo":
        g = [(i, j) for i in range(-5, 6) for j in range(-5, 6) if 2.6 ** 2 <= i * i + j * j <= 5.2 ** 2]
    ci = sum(c[0] for c in g) / len(g); cj = sum(c[1] for c in g) / len(g)
    return [((i - ci) * PS, (j - cj) * PS, rng.uniform(-0.04, 0.04)) for (i, j) in g]


hits = []


def post(arb, sp, data):
    if arb.is_first_contact:
        imp = arb.total_impulse.length
        pts = arb.contact_point_set.points
        if not pts:
            return
        for sh in arb.shapes:
            if sh.collision_type == 2:
                hits.append((sh.chunk, imp, pts[0].point_a))


space.on_collision(1, 2, post_solve=post)
space.on_collision(2, 2, post_solve=post)


def split(ch, at):
    b = ch["body"]
    cells = ch["cells"]
    lp = b.world_to_local(at)
    for attempt in range(5):
        a = rng.uniform(0, math.pi)
        nx, ny = math.cos(a), math.sin(a)
        ox, oy = (lp.x, lp.y) if attempt < 2 else (0, 0)
        A = [c for c in cells if (c[0] - ox) * nx + (c[1] - oy) * ny > 0]
        B = [c for c in cells if (c[0] - ox) * nx + (c[1] - oy) * ny <= 0]
        if A and B:
            break
    else:
        return []
    remove_chunk(ch)
    out = []
    wn = pymunk.Vec2d(nx, ny).rotated(b.angle)
    for part, sg in ((A, 1), (B, -1)):
        mx = sum(c[0] for c in part) / len(part); my = sum(c[1] for c in part) / len(part)
        wp = b.local_to_world((mx, my))
        v = b.velocity_at_world_point(wp)
        kick = 90 * sg
        nc = make_chunk([(c[0] - mx, c[1] - my, c[2]) for c in part], wp, b.angle,
                        (v.x + wn.x * kick, v.y + wn.y * kick), b.angular_velocity + rng.uniform(-2, 2), ch["hue"], ch["obj"])
        nc["flash"] = 1.0
        out.append(nc)
    return out


PLAN = [(0.0, "cubo", 0.52), (12.0, "piramide", 0.85), (24.0, "bola", 0.12), (36.0, "torre", 0.32), (47.5, "anillo", 0.72)]
NAMES = {"cubo": "CUBO", "piramide": "PIRÁMIDE", "bola": "BOLA", "torre": "TORRE", "anillo": "ANILLO"}
aud = Audio(DUR + 1)
cv = Canvas() if not DRY else None
vid = Video(OUT) if not DRY else None
camx, camy = 300.0, 800.0
nfr = int(DUR * FPS)
plan_i = 0
sparks = []
nsplits = 0
cur = None
for f in range(nfr):
    t = f / FPS
    if plan_i < len(PLAN) and t >= PLAN[plan_i][0]:
        _, kind, hue = PLAN[plan_i]
        sx = camx + 150 if cur else 150
        cur = dict(chunks=[], t=t, kind=kind, hue=hue)
        make_chunk(shape_cells(kind), (sx, stair_y(sx) - 420), 0.0, (360, -200), float(rng.choice([-2.5, 2.5])), hue, cur)
        plan_i += 1
        aud.add(t, bell(midi(64 + plan_i * 3), 1.4), 0.2)
    nsp = 0
    loud = []
    for _ in range(SUB):
        hits.clear()
        space.step(1 / FPS / SUB)
        done = set()
        for (ch, imp, at) in sorted(hits, key=lambda h: -h[1]):
            if id(ch) in done or ch not in chunks:
                continue
            loud.append(imp)
            n = len(ch["cells"])
            if n > 1 and ch["cool"] <= 0 and imp > K * n ** 0.75:
                done.add(id(ch))
                parts = split(ch, at)
                if parts:
                    nsp += 1
                    for p in parts:
                        p["cool"] = 0.12
                        done.add(id(p))
                    for _ in range(10):
                        a = rng.uniform(0, 2 * math.pi); s = rng.uniform(100, 500)
                        sparks.append([at.x, at.y, math.cos(a) * s, math.sin(a) * s, 1.0, hsv(ch["hue"], 0.4, 1)])
    for ch in chunks:
        ch["cool"] -= 1 / FPS
    nsplits += nsp
    for k, imp in enumerate(sorted(loud, reverse=True)[:2]):
        if imp > 150:
            aud.add(t + k * 0.007, thud(65 + rng.uniform(0, 90), 0.25), min(0.8, imp / 4000))
    for k in range(min(nsp, 3)):
        aud.add(t + k * 0.01, crack(f + k), 0.55)
        aud.add(t + k * 0.01, pluck(penta_freq(int(rng.integers(5, 15)), 220), 0.5), 0.12)
    if cur and cur["chunks"]:
        pts = sorted(((c["body"].position.x, c["body"].position.y, len(c["cells"])) for c in cur["chunks"]))
        tot = sum(p[2] for p in pts); acc = 0
        for p in pts:
            acc += p[2]
            if acc >= tot * 0.6:
                tx, ty = p[0], p[1]; break
        camx += (tx - camx) * 0.06
        camy += (ty - camy) * 0.06
    if f % 30 == 0:
        for ch in list(chunks):
            pp = ch["body"].position
            if pp.x < camx - 1500 or pp.y > camy + 2500:
                remove_chunk(ch)
    if DRY:
        if f % 180 == 0:
            print(round(t), "splits", nsplits, "trozos", len(chunks), int(camx), int(camy), file=sys.stderr)
        continue
    c = cv.ctx
    cv.clear()
    c.save()
    c.translate(W / 2 - camx, H * 0.5 - camy)
    lx0, lx1 = camx - W, camx + W
    for (a, b, d) in stairs:
        if b[0] < lx0 or a[0] > lx1:
            continue
        g = cairo.LinearGradient(0, a[1], 0, a[1] + 500)
        g.add_color_stop_rgba(0, 0.3, 0.4, 1.0, 0.13); g.add_color_stop_rgba(1, 0.3, 0.4, 1.0, 0)
        c.set_source(g); c.rectangle(a[0], a[1] + 2, SW, 500); c.fill()
    c.set_line_width(5); c.set_source_rgba(0.55, 0.65, 1.0, 0.95)
    first = True
    for (a, b, d) in stairs:
        if b[0] < lx0 or a[0] > lx1:
            continue
        if first:
            c.move_to(*a); first = False
        c.line_to(*b); c.line_to(*d)
    c.stroke()
    for ch in chunks:
        b = ch["body"]
        fl = ch["flash"]; ch["flash"] *= 0.85
        c.save(); c.translate(b.position.x, b.position.y); c.rotate(b.angle)
        for (cx, cy, dh) in ch["cells"]:
            col = hsv(ch["hue"] + dh, 0.75, 1)
            c.set_source_rgba(*col, 0.3 + 0.6 * fl); c.rectangle(cx - PS / 2, cy - PS / 2, PS, PS); c.fill()
            c.set_source_rgba(*col, 1); c.set_line_width(2.5)
            c.rectangle(cx - PS / 2 + 2, cy - PS / 2 + 2, PS - 4, PS - 4); c.stroke()
        c.restore()
    ns = []
    for s in sparks:
        s[0] += s[2] / FPS; s[1] += s[3] / FPS; s[3] += 1200 / FPS; s[4] -= 2 / FPS
        if s[4] > 0:
            c.set_source_rgba(*s[5], s[4]); c.arc(s[0], s[1], 3, 0, 2 * math.pi); c.fill(); ns.append(s)
    sparks = ns[-1200:]
    c.restore()
    cv.text("ROTURAS", W / 2, 150, 38, (0.65, 0.7, 0.9), cairo.FONT_WEIGHT_NORMAL)
    cv.text(str(nsplits), W / 2, 270, 110, (1, 0.45, 0.2))
    if cur:
        a = min(1, (t - cur["t"]) / 0.3, max(0, (cur["t"] + 3 - t) / 0.5))
        if a > 0:
            cv.text(NAMES[cur["kind"]], W / 2, 1720, 70, hsv(cur["hue"], 0.7, 1), alpha=a)
    vid.write(glow(cv.array(), 0.85))

print("splits", nsplits, file=sys.stderr)
if not DRY:
    vid.close(aud.master(0.25))
