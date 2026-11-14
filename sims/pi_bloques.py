"""Bloques que cuentan π: choques elásticos con pared, masas 1, 100, 10^4, 10^6, 10^8."""
import sys, math, bisect
import numpy as np
from common import *

OUT = sys.argv[1] if len(sys.argv) > 1 else "pi_bloques.mp4"
XW, FLOOR, W1 = 70, 1180, 70
MASSES = [1, 100, 10**4, 10**6, 10**8]
LABEL = ["1 kg", "100 kg", "10.000 kg", "1.000.000 kg", "100.000.000 kg"]
COLS = [NEON[0], NEON[1], NEON[3], NEON[4], NEON[2]]
INTRO, ROUND, OUTRO = 2.0, 11.0, 4.5


def events(M, x1, x2, u):
    w2 = width(M)
    st = [0.0, x1, 0.0, x2, -u]
    ev = [tuple(st) + (0,)]
    t, x1, v1, x2, v2 = st
    n = 0
    while True:
        tb = (x2 - (x1 + W1)) / (v1 - v2) if v1 > v2 else math.inf
        tw = (x1 - XW) / (-v1) if v1 < 0 else math.inf
        if tb == math.inf and tw == math.inf:
            break
        if tb <= tw:
            dt = max(tb, 0); t += dt; x1 += v1 * dt; x2 += v2 * dt
            x1 = min(x1, x2 - W1)
            m1, m2 = 1.0, float(M)
            v1, v2 = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2), ((m2 - m1) * v2 + 2 * m1 * v1) / (m1 + m2)
            kind = 1
        else:
            dt = max(tw, 0); t += dt; x1 = XW; x2 += v2 * dt; v1 = -v1
            kind = 2
        n += 1
        ev.append((t, x1, v1, x2, v2, kind))
    return ev


def width(M):
    return 90 + 40 * math.log10(M)


def state(ev, times, t):
    i = bisect.bisect_right(times, t) - 1
    i = max(i, 0)
    t0, x1, v1, x2, v2, _ = ev[i]
    dt = t - t0
    return x1 + v1 * dt, x2 + v2 * dt, i


def main():
    rounds = []
    for k, M in enumerate(MASSES):
        x1 = 330
        x2 = 600
        u = 230
        ev = events(M, x1, x2, u)
        times = [e[0] + 0.9 for e in ev]  # empieza a moverse a 0.9s del inicio de ronda
        ev = [(times[i],) + e[1:] for i, e in enumerate(ev)]
        ev[0] = (0.0,) + ev[0][1:]
        times[0] = 0.0
        # antes de 0.9 s quietos: estado inicial con velocidad 0 hasta 0.9
        ev.insert(1, (0.9, x1, 0.0, x2, -u, 0))
        ev[0] = (0.0, x1, 0.0, x2, 0.0, 0)
        times = [e[0] for e in ev]
        coll = [e[0] for e in ev if e[5] in (1, 2)]
        print(f"M={M}: {len(coll)} choques, último a {coll[-1]:.2f}s", file=sys.stderr)
        rounds.append((M, ev, times, np.array(coll)))

    total = INTRO + ROUND * len(MASSES) + OUTRO
    nfr = int(total * FPS)
    aud = Audio(total)
    for k, (M, ev, times, coll) in enumerate(rounds):
        t0 = INTRO + k * ROUND
        # densidad para no saturar
        lo = np.searchsorted(coll, coll - 0.012); hi = np.searchsorted(coll, coll + 0.012)
        dens = hi - lo
        for j, tc in enumerate(coll):
            g = 0.9 / math.sqrt(dens[j])
            aud.add(t0 + tc, click(j, tone=2200 + 300 * (j % 3)), g)
    # campanas de resultado y final
    for k in range(len(MASSES)):
        aud.add(INTRO + k * ROUND + rounds[k][3][-1] + 0.5, bell(midi(72 + [0, 4, 7, 11, 12][k]), 1.6), 0.5)
    for j, n in enumerate([72, 76, 79, 84, 88]):
        aud.add(INTRO + len(MASSES) * ROUND + 0.4 + j * 0.12, bell(midi(n), 2.5), 0.45)
    audio = aud.master(0.2)

    cv = Canvas(); c = cv.ctx
    vid = Video(OUT)
    sparks = []
    flash = [0.0, 0.0]
    last_i = 0
    rng = np.random.default_rng(3)
    for f in range(nfr):
        t = f / FPS
        cv.clear()
        # rejilla tenue
        c.set_line_width(1); c.set_source_rgba(0.3, 0.4, 0.9, 0.07)
        for gx in range(0, W, 60):
            c.move_to(gx, 0); c.line_to(gx, H)
        for gy in range(0, H, 60):
            c.move_to(0, gy); c.line_to(W, gy)
        c.stroke()
        k = int((t - INTRO) // ROUND) if t >= INTRO else -1
        cv.text("¿CUÁNTOS CHOQUES?", W / 2, 230, 64, (0.85, 0.9, 1.0))
        # historial
        done = []
        for j in range(len(MASSES)):
            if t >= INTRO + j * ROUND + rounds[j][3][-1] + 0.5:
                done.append(j)
        for j in done:
            y = 1420 + j * 82
            col = COLS[j]
            cv.text(f"1 kg  vs  {LABEL[j]}", 120, y, 40, (0.75, 0.78, 0.9), cairo.FONT_WEIGHT_NORMAL, "left")
            cv.text(f"{len(rounds[j][3]):,}".replace(",", "."), 960, y, 50, col, align="right")
        if 0 <= k < len(MASSES):
            M, ev, times, coll = rounds[k]
            tr = t - INTRO - k * ROUND
            x1, x2, i = state(ev, times, tr)
            n = int(np.searchsorted(coll, tr, side="right"))
            # chispas por eventos nuevos
            if i > last_i:
                newev = ev[last_i + 1:i + 1]
                for e in newev[-6:]:
                    if e[5] == 1:
                        flash[0] = flash[1] = 1.0
                        px = e[1] + W1
                    elif e[5] == 2:
                        flash[0] = 1.0; px = XW
                    else:
                        continue
                    for _ in range(6):
                        a = rng.uniform(-math.pi, 0)
                        sp = rng.uniform(150, 600)
                        sparks.append([px, FLOOR - rng.uniform(5, 60), math.cos(a) * sp, math.sin(a) * sp, 1.0, COLS[k]])
            last_i = i
            fade = min(1, tr / 0.3, (ROUND - tr) / 0.3)
            w2 = width(M)
            # suelo y pared
            c.set_source_rgba(0.6, 0.7, 1.0, 0.9); c.set_line_width(5)
            c.move_to(XW, FLOOR - 520); c.line_to(XW, FLOOR); c.line_to(W - 20, FLOOR); c.stroke()
            c.set_source_rgba(0.6, 0.7, 1.0, 0.25); c.set_line_width(2)
            for yy in range(int(FLOOR - 520), int(FLOOR), 28):
                c.move_to(XW, yy); c.line_to(XW - 26, yy + 26)
            c.stroke()
            # bloques
            for (bx, bw, col, fl, lab) in [(x1, W1, (0.9, 0.95, 1.0), flash[0], "1 kg"), (x2, w2, COLS[k], flash[1], LABEL[k])]:
                if bx > W + 50:
                    continue
                c.set_source_rgba(*col, (0.15 + 0.5 * fl) * fade)
                c.rectangle(bx, FLOOR - bw, bw, bw); c.fill()
                c.set_source_rgba(*col, fade); c.set_line_width(6)
                c.rectangle(bx + 3, FLOOR - bw + 3, bw - 6, bw - 6); c.stroke()
                fs = 22 if bw < 120 else min(44, bw / 7.5)
                cv.text(lab, bx + bw / 2, FLOOR - bw - 18, fs, col, alpha=fade)
            flash[0] *= 0.82; flash[1] *= 0.82
            # contador
            cv.text("CHOQUES", W / 2, 420, 46, (0.6, 0.65, 0.85), cairo.FONT_WEIGHT_NORMAL)
            cv.text(f"{n:,}".replace(",", "."), W / 2, 600, 190, COLS[k])
            cv.text(f"masa ×{LABEL[k].replace(' kg','')}", W / 2, 690, 40, (0.6, 0.65, 0.85), cairo.FONT_WEIGHT_NORMAL, alpha=fade)
        elif k < 0:
            a = ease(t / 0.8)
            cv.text("1 kg contra…", W / 2, 640, 80, NEON[0], alpha=a)
            cv.text("cada vez 100 veces más", W / 2, 740, 50, (0.7, 0.75, 0.95), cairo.FONT_WEIGHT_NORMAL, alpha=ease((t - 0.8) / 0.8))
        else:
            to = t - INTRO - len(MASSES) * ROUND
            a = ease(to / 1.0)
            cv.text("π = 3,14159…", W / 2, 760, 150, NEON[3], alpha=a)
            cv.text("los choques escriben pi", W / 2, 870, 50, (0.75, 0.8, 1.0), cairo.FONT_WEIGHT_NORMAL, alpha=ease((to - 1) / 1))
        # chispas
        ns = []
        for s in sparks:
            s[0] += s[2] / FPS; s[1] += s[3] / FPS; s[3] += 1500 / FPS; s[4] -= 1.8 / FPS
            if s[4] > 0 and s[1] < FLOOR:
                c.set_source_rgba(*s[5], s[4]); c.arc(s[0], s[1], 3.5, 0, 2 * math.pi); c.fill()
                ns.append(s)
        sparks = ns[-400:]
        vid.write(glow(cv.array()))
    vid.close(audio)


if __name__ == "__main__":
    main()
