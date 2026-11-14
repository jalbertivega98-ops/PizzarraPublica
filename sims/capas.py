"""4 bolas unidas por barras caen rompiendo capas de cuadrados. ×2 = se clona, BOOM = revienta la capa."""
import sys, math, os
import numpy as np
import pymunk
from common import *

OUT = sys.argv[1] if len(sys.argv) > 1 else "capas.mp4"
DRY = os.environ.get("DRY")
rng = np.random.default_rng(int(os.environ.get("SEED", "5")))
DUR = 60.0
SUB = 6
BR = 24
SIDE = 104
LAYER0, LSP = 900, 470
NL = 70
CELLH = 46
X0, X1 = 30, 1050

space = pymunk.Space()
space.gravity = (0, 1300)
for x in (X0, X1):
    s = pymunk.Segment(space.static_body, (x, -3000), (x, LAYER0 + LSP * NL + 3000), 10)
    s.elasticity = 0.9; s.friction = 0.2
    space.add(s)

cells = {}  # shape -> dict
layers = []
for L in range(NL):
    y = LAYER0 + L * LSP
    n = int(rng.integers(5, 9))
    w = (X1 - X0) / n
    row = []
    for k in range(n):
        r = rng.random()
        kind = "x2" if r < 0.12 else ("boom" if r < 0.19 else "n")
        hp = 1 if kind != "n" else int(rng.integers(1, 5 + min(L // 8, 3)))
        b = space.static_body
        shp = pymunk.Poly(b, [(X0 + k * w + 3, y), (X0 + (k + 1) * w - 3, y), (X0 + (k + 1) * w - 3, y + CELLH), (X0 + k * w + 3, y + CELLH)])
        shp.elasticity = 0.82; shp.friction = 0.3; shp.collision_type = 3
        space.add(shp)
        d = dict(shape=shp, x=X0 + k * w + 3, y=y, w=w - 6, hp=hp, hp0=hp, kind=kind, layer=L, alive=True, flash=0.0, touch=0)
        cells[shp] = d
        row.append(d)
    layers.append(row)

mols = []


def make_mol(cx, cy, vel=(0, 0), hue=None, ang=0.0):
    bodies = []
    for (dx, dy) in [(-1, -1), (1, -1), (1, 1), (-1, 1)]:
        ox, oy = dx * SIDE / 2, dy * SIDE / 2
        rx = ox * math.cos(ang) - oy * math.sin(ang); ry = ox * math.sin(ang) + oy * math.cos(ang)
        b = pymunk.Body(1, pymunk.moment_for_circle(1, 0, BR))
        b.position = (cx + rx, cy + ry); b.velocity = vel
        s = pymunk.Circle(b, BR); s.elasticity = 0.8; s.friction = 0.4; s.collision_type = 2
        space.add(b, s)
        bodies.append(b)
    joints = []
    for i, j in [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2), (1, 3)]:
        jn = pymunk.PinJoint(bodies[i], bodies[j]); joints.append(jn)
    space.add(*joints)
    m = dict(bodies=bodies, joints=joints, hue=rng.random() if hue is None else hue, trail=[])
    for b in bodies:
        b.mol = m
    mols.append(m)
    return m


make_mol(540, 300, (180, 0), 0.52, 0.3)

events = []


def begin(arb, sp, data):
    a, b = arb.shapes
    cell = cells.get(b) or cells.get(a)
    ball = a if a.collision_type == 2 else b
    if cell and cell["alive"]:
        cell["touch"] += 1
        speed = ball.body.velocity.length
        events.append(("hit", cell, ball.body, speed))


def separate(arb, sp, data):
    a, b = arb.shapes
    cell = cells.get(b) or cells.get(a)
    if cell:
        cell["touch"] = max(0, cell["touch"] - 1)


space.on_collision(2, 3, begin=begin, separate=separate)

aud = Audio(DUR + 1)
cv = Canvas() if not DRY else None
vid = Video(OUT) if not DRY else None
parts = []
debris = []
shock = []
cam = 400.0
nfr = int(DUR * FPS)
deepest = 0
grind = 0.0
last_snd = -1


def kill(cell, t, by=None):
    if not cell["alive"]:
        return
    cell["alive"] = False
    space.remove(cell["shape"])
    col = cellcol(cell)
    for _ in range(4):
        debris.append([cell["x"] + rng.uniform(0, cell["w"]), cell["y"] + CELLH / 2, rng.uniform(-250, 250), rng.uniform(-500, -100),
                       rng.uniform(0, 6), rng.uniform(-10, 10), cell["w"] / 3.2, col, 1.6])
    for _ in range(14):
        a = rng.uniform(0, 2 * math.pi); sp = rng.uniform(100, 600)
        parts.append([cell["x"] + cell["w"] / 2, cell["y"] + CELLH / 2, math.cos(a) * sp, math.sin(a) * sp, 1.0, col])
    aud.add(t, crack(int(t * 97)), 0.5)
    aud.add(t, bell(penta_freq(5 + cell["layer"] % 10, 220), 1.0), 0.28)
    if cell["kind"] == "x2" and by is not None and len(mols) < 7:
        m = by.mol
        cx = sum(b.position.x for b in m["bodies"]) / 4
        cy = sum(b.position.y for b in m["bodies"]) / 4
        v = by.velocity
        nx = cx + (130 if cx < 540 else -130)
        make_mol(nx, cy - 40, (-v.x * 0.6 + rng.uniform(-200, 200), min(v.y, 0) - 200), (m["hue"] + 0.17) % 1, rng.uniform(0, 3))
        for j, n in enumerate([72, 76, 79, 84]):
            aud.add(t + j * 0.06, bell(midi(n), 1.2), 0.3)
        shock.append([cx, cy, 0.0, (1, 0.85, 0.15), "×2"])
    if cell["kind"] == "boom":
        aud.add(t, thud(55, 0.7), 1.0)
        shock.append([cell["x"] + cell["w"] / 2, cell["y"], 0.0, (1, 0.25, 0.3), "BOOM"])
        for o in layers[cell["layer"]]:
            if o["alive"]:
                kill(o, t + 0.02)
        for m in mols:
            for b in m["bodies"]:
                d = b.position.y - cell["y"]
                if abs(d) < 400:
                    b.apply_impulse_at_local_point((rng.uniform(-150, 150), 250))


def cellcol(cell):
    if cell["kind"] == "x2":
        return (1.0, 0.85, 0.15)
    if cell["kind"] == "boom":
        return (1.0, 0.22, 0.3)
    return hsv(0.55 + 0.09 * (cell["hp0"] - 1), 0.75, 1)


for f in range(nfr):
    t = f / FPS
    for _ in range(SUB):
        events.clear()
        space.step(1 / FPS / SUB)
        for ev in events:
            _, cell, body, speed = ev
            if not cell["alive"]:
                continue
            if speed > 120:
                cell["hp"] -= 1
                cell["flash"] = 1.0
                if f != last_snd:
                    aud.add(t, pluck(penta_freq(cell["layer"] % 12 + 3, 196), 0.4), 0.35)
                    last_snd = f
                if cell["hp"] <= 0:
                    kill(cell, t, body)
    # desgaste por contacto continuo (para que nunca se atasque)
    grind += 1 / FPS
    if grind > 0.35:
        grind = 0
        for cell in list(cells.values()):
            if cell["alive"] and cell["touch"] > 0:
                cell["hp"] -= 1; cell["flash"] = 1.0
                aud.add(t, pluck(penta_freq(cell["layer"] % 12, 196), 0.3), 0.25)
                if cell["hp"] <= 0:
                    kill(cell, t, next(iter(m["bodies"][0] for m in mols)))
    leader = max(max(b.position.y for b in m["bodies"]) for m in mols)
    deepest = max(deepest, sum(1 for L in range(NL) if LAYER0 + L * LSP + CELLH < leader))
    cam += (leader - 150 - cam) * 0.08
    # descartar grupos muy rezagados
    for m in list(mols):
        if len(mols) > 1 and max(b.position.y for b in m["bodies"]) < cam - 1600:
            space.remove(*m["joints"]); [space.remove(b, *b.shapes) for b in m["bodies"]]
            mols.remove(m)
    if DRY:
        if f % 300 == 0:
            print(round(t), "capa", deepest, "grupos", len(mols), file=sys.stderr)
        continue
    c = cv.ctx
    cv.clear()
    c.save()
    c.translate(0, H * 0.45 - cam)
    top, bot = cam - H * 0.5, cam + H * 0.6
    # paredes
    c.set_source_rgba(0.5, 0.6, 1.0, 0.5); c.set_line_width(6)
    for x in (X0, X1):
        c.move_to(x, top); c.line_to(x, bot)
    c.stroke()
    # celdas
    for row in layers:
        if not (top - 100 < row[0]["y"] < bot + 100):
            continue
        # «tela» de fondo: rejilla fina
        y = row[0]["y"]
        c.set_source_rgba(0.6, 0.7, 1.0, 0.08); c.set_line_width(1)
        for gx in range(X0, X1, 23):
            c.move_to(gx, y); c.line_to(gx, y + CELLH)
        c.stroke()
        for cell in row:
            if not cell["alive"]:
                continue
            col = cellcol(cell)
            fl = cell["flash"]; cell["flash"] *= 0.85
            frac = cell["hp"] / cell["hp0"]
            c.set_source_rgba(*col, 0.12 + 0.25 * frac + 0.5 * fl)
            c.rectangle(cell["x"], cell["y"], cell["w"], CELLH); c.fill()
            c.set_source_rgba(*col, 0.95); c.set_line_width(4)
            c.rectangle(cell["x"] + 2, cell["y"] + 2, cell["w"] - 4, CELLH - 4); c.stroke()
            lab = "×2" if cell["kind"] == "x2" else ("BOOM" if cell["kind"] == "boom" else str(cell["hp"]))
            c.save(); c.identity_matrix()
            cv.text(lab, cell["x"] + cell["w"] / 2, cell["y"] - cam + H * 0.45 + 33, 30 if lab != "BOOM" else 24, (1, 1, 1))
            c.restore()
    # escombros
    nd = []
    for d in debris:
        d[0] += d[2] / FPS; d[1] += d[3] / FPS; d[3] += 1300 / FPS; d[4] += d[5] / FPS; d[8] -= 1 / FPS
        if d[8] > 0:
            c.save(); c.translate(d[0], d[1]); c.rotate(d[4])
            c.set_source_rgba(*d[7], min(1, d[8])); c.set_line_width(3)
            c.rectangle(-d[6] / 2, -10, d[6], 20); c.stroke(); c.restore(); nd.append(d)
    debris = nd[-300:]
    npx = []
    for p in parts:
        p[0] += p[2] / FPS; p[1] += p[3] / FPS; p[3] += 900 / FPS; p[4] -= 1.5 / FPS
        if p[4] > 0:
            c.set_source_rgba(*p[5], p[4]); c.arc(p[0], p[1], 3.5 * p[4] + 1, 0, 2 * math.pi); c.fill(); npx.append(p)
    parts = npx[-1500:]
    nsh = []
    for s in shock:
        s[2] += 1 / FPS
        if s[2] < 0.7:
            a = 1 - s[2] / 0.7
            c.set_source_rgba(*s[3], a); c.set_line_width(8)
            c.arc(s[0], s[1], 30 + s[2] * 600, 0, 2 * math.pi); c.stroke(); nsh.append(s)
    shock = nsh
    # moléculas
    for m in mols:
        col = hsv(m["hue"], 0.8, 1)
        ps = [(b.position.x, b.position.y) for b in m["bodies"]]
        cxm = sum(p[0] for p in ps) / 4; cym = sum(p[1] for p in ps) / 4
        m["trail"].append((cxm, cym)); m["trail"] = m["trail"][-25:]
        tr = m["trail"]
        for k in range(1, len(tr)):
            a = k / len(tr)
            c.set_source_rgba(*col, 0.3 * a); c.set_line_width(40 * a); c.move_to(*tr[k - 1]); c.line_to(*tr[k]); c.stroke()
        c.set_line_width(7); c.set_source_rgba(0.85, 0.9, 1.0, 0.9)
        for i, j in [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2), (1, 3)]:
            c.move_to(*ps[i]); c.line_to(*ps[j])
        c.stroke()
        for p in ps:
            c.set_source_rgb(*col); c.arc(p[0], p[1], BR, 0, 2 * math.pi); c.fill()
            c.set_source_rgba(1, 1, 1, 0.7); c.arc(p[0] - 6, p[1] - 6, BR * 0.32, 0, 2 * math.pi); c.fill()
    c.restore()
    for s in shock:
        pass
    # HUD
    c.set_source_rgba(0.02, 0.02, 0.05, 0.75); c.rectangle(0, 0, W, 200); c.fill()
    cv.text("CAPAS ROTAS", 300, 85, 34, (0.65, 0.7, 0.9), cairo.FONT_WEIGHT_NORMAL)
    cv.text(str(deepest), 300, 165, 76, (0.3, 1, 0.9))
    cv.text("GRUPOS", 780, 85, 34, (0.65, 0.7, 0.9), cairo.FONT_WEIGHT_NORMAL)
    cv.text(str(len(mols)), 780, 165, 76, (1, 0.85, 0.15))
    if t < 3.5:
        a = min(1, t / 0.4, (3.5 - t) / 0.6)
        cv.text("×2 = se clona   ·   BOOM = revienta la capa", W / 2, 1800, 36, (1, 1, 1), alpha=a)
    vid.write(glow(cv.array(), 0.85))

print("capas", deepest, "grupos", len(mols), file=sys.stderr)
if not DRY:
    vid.close(aud.master(0.3))
