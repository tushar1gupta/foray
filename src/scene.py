#!/usr/bin/env python3
"""The hero scene: engineers walking toward a company.

Two layers that share one monospace grid:
  1. a static field  -> ambient glyph noise, a ground line, and a tower with lit windows
  2. walk frames     -> a stick figure rasterised from a joint model, one frame per phase

Layer 2 is plain text so the browser can swap frames with textContent, which needs
no escaping and allocates nothing.
"""
import math

COLS, ROWS = 122, 64
GROUND = 55                     # row the figures stand on
B_L, B_R, B_T = 78, 113, 13     # tower bounds
DOOR_L, DOOR_R, DOOR_T = 92, 99, 49

GLYPHS = "01<>[]{}()/\\|=+-*&%$#@!?;:,.^~_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
SPARSE = ".,:;'`^~-_ "
MID = "abcdehknopsuvxyz2345679=+*<>[]{}()/\\|"
DENSE = "@#%&WM8BQ$0OZ"


def _rng(seed):
    s = [seed]
    def r():
        s[0] = (s[0] * 1103515245 + 12345) % 2147483648
        return s[0] / 2147483648
    return r


def field():
    """Static layer. Returns HTML with run-length-encoded spans."""
    rnd = _rng(9)
    cells = [[(0, " ", "") for _ in range(COLS)] for _ in range(ROWS)]

    # ambient noise in short runs of a shared level: same texture, a quarter of the spans
    for r in range(ROWS):
        c = 0
        depth = max(0.0, (r - 8) / (ROWS - 8))
        while c < COLS:
            run = 2 + int(rnd() * 8)
            lv = 1 if rnd() < 0.20 + 0.22 * depth else 0
            if lv and rnd() < 0.30:
                lv = 2
            for k in range(min(run, COLS - c)):
                ch = GLYPHS[int(rnd() * len(GLYPHS))] if lv else SPARSE[int(rnd() * len(SPARSE))]
                cells[r][c + k] = (lv, ch, "")
            c += run

    # tower: facade fill, then edges
    for r in range(B_T, GROUND):
        for c in range(B_L, B_R):
            cells[r][c] = (2, MID[int(rnd() * len(MID))], "")
    for r in range(B_T, GROUND):
        cells[r][B_L] = (4, "|", "")
        cells[r][B_R - 1] = (4, "|", "")
    for c in range(B_L, B_R):
        cells[B_T][c] = (4, "=", "")

    # roof mast
    for r in range(B_T - 5, B_T):
        cells[r][95] = (3, "|", "")
    cells[B_T - 6][95] = (7, "*", "win")

    # window grid, a few lit
    for r in range(B_T + 3, DOOR_T - 1, 4):
        for c in range(B_L + 3, B_R - 5, 6):
            lit = rnd() < 0.22
            for k in range(3):
                cells[r][c + k] = ((7, "#", "win") if lit else (5, "=", "win"))
            for k in range(3):
                cells[r + 1][c + k] = ((6, "#", "win") if lit else (4, "-", "win"))

    # doorway, brighter than the windows so it reads as the destination
    for r in range(DOOR_T, GROUND):
        for c in range(DOOR_L, DOOR_R):
            cells[r][c] = (6, MID[int(rnd() * len(MID))], "")
    for r in range(DOOR_T + 1, GROUND):
        for c in range(DOOR_L + 1, DOOR_R - 1):
            cells[r][c] = (7, "#", "win")
    for c in range(DOOR_L, DOOR_R):
        cells[DOOR_T][c] = (7, "=", "")

    # light spilling out of the door onto the ground
    for c in range(DOOR_L - 9, DOOR_L):
        fall = (c - (DOOR_L - 9)) / 9.0
        if rnd() < 0.25 + 0.55 * fall:
            cells[GROUND - 1][c] = (3 + int(fall * 2), "-", "")

    # ground line and a little texture below it
    for c in range(COLS):
        cells[GROUND][c] = (4, "=" if rnd() < 0.75 else "-", "")
    for r in range(GROUND + 1, ROWS):
        for c in range(COLS):
            if rnd() < 0.30:
                cells[r][c] = (1, SPARSE[int(rnd() * len(SPARSE))], "")
            else:
                cells[r][c] = (0, " ", "")

    esc = lambda t: t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    rows = []
    for r in range(ROWS):
        out, cur, buf = [], (cells[r][0][0], cells[r][0][2]), []
        for lv, ch, kind in cells[r]:
            if (lv, kind) == cur:
                buf.append(ch)
            else:
                cls = f"a{cur[0]}" + (" win" if cur[1] else "")
                out.append(f'<span class="{cls}">{esc("".join(buf))}</span>')
                cur, buf = (lv, kind), [ch]
        cls = f"a{cur[0]}" + (" win" if cur[1] else "")
        out.append(f'<span class="{cls}">{esc("".join(buf))}</span>')
        rows.append("".join(out))
    return "\n".join(rows)


# ------------------------------------------------- abstract figure, walking
FW, FH = 20, 27          # figure grid
ASPECT = 0.6
RAMP = " ..::;=+ox*#%@"  # sparse to dense; density carries the shading


def _smooth(t, soft=0.34):
    """0 outside, 1 inside, soft shoulder. t is a signed inside-ness."""
    if t <= 0:
        return 0.0
    if t >= soft:
        return 1.0
    u = t / soft
    return u * u * (3 - 2 * u)


def _ellipse(x, y, cx, cy, a, b):
    t = 1.0 - ((x - cx) / a) ** 2 - ((y - cy) / b) ** 2
    return _smooth(t, 0.42)


def _column(x, y, cx, hw, y0, y1):
    """Vertical mass between y0 and y1 with half-width hw."""
    if y < y0 - 1.0 or y > y1 + 1.0:
        return 0.0
    side = _smooth(1.0 - abs(x - cx) / hw, 0.40)
    cap = _smooth(min(y - (y0 - 1.0), (y1 + 1.0) - y), 1.1)
    return side * cap


def figure(p):
    """One frame of an abstract walking body at phase p in [0,1)."""
    w = 2 * math.pi * p
    cx = FW / 2.0 - 0.5
    bob = 0.34 * math.sin(2 * w)
    swing = math.sin(w)

    head_y = 3.0 + bob
    sh_y = 7.0 + bob
    hip_y = 15.4 + bob
    foot_y = 24.4

    rows = []
    for r in range(FH):
        y = float(r)
        line = []
        for c in range(FW):
            x = float(c)
            v = 0.0

            # head: solid mass with a faint band where a face would be
            h = _ellipse(x, y, cx + 0.3, head_y, 2.4, 2.8)
            if h:
                h *= 1.0 - 0.22 * _ellipse(x, y, cx + 0.3, head_y + 0.2, 1.7, 0.55)
            v = max(v, h * 0.92)

            # neck
            v = max(v, _column(x, y, cx + 0.2, 1.05, head_y + 2.4, sh_y - 0.2) * 0.72)

            # torso tapering from shoulders to hips
            if sh_y - 0.6 <= y <= hip_y + 0.6:
                t = (y - sh_y) / max(0.1, hip_y - sh_y)
                hw = 3.5 - 1.35 * t          # wide at the shoulders, narrow at the hips
                v = max(v, _column(x, y, cx, hw, sh_y - 0.6, hip_y + 0.6) * 0.90)

            # arms swinging against the legs
            for sgn, ph in ((-1, 0.5), (1, 0.0)):
                a = math.sin(w + 2 * math.pi * ph)
                ax = cx + sgn * 3.3 + a * 1.3
                v = max(v, _column(x, y, ax, 1.15, sh_y + 0.6, hip_y + 0.8) * 0.62)

            # legs: forward leg lifts and leads, trailing leg extends back
            # side view: leg separation is fore-aft, so it lives on the x axis only.
            # the legs genuinely coincide at the passing position, as in a real walk.
            for ph in (0.0, 0.5):
                a = math.sin(w + 2 * math.pi * ph)
                lift = 1.15 * max(0.0, a)
                lx = cx + a * 2.5
                hw = 1.30 - 0.20 * max(0.0, a)      # swinging leg reads slightly thinner
                v = max(v, _column(x, y, lx, hw, hip_y, foot_y - lift) * 0.84)
                v = max(v, _ellipse(x, y, lx + a * 0.65, foot_y - lift, 1.8, 0.78) * 0.76)

            if v > 0:
                # light falls from the building on the right, so lead edges read brighter
                v *= 0.62 + 0.38 * _smooth((x - cx) / FW + 0.55, 1.0)
                # dissolve the silhouette edges into the field
                v *= 0.88 + 0.12 * (1.0 - abs(y - (FH / 2)) / (FH / 2))
            line.append(RAMP[max(0, min(len(RAMP) - 1, int(v * len(RAMP))))])
        rows.append("".join(line).rstrip())
    return "\n".join(rows)


def frames(n=10):
    return [figure(i / n) for i in range(n)]


if __name__ == "__main__":
    f = field()
    print("field:", len(f), "chars,", f.count("<span"), "spans,", f.count(chr(10)) + 1, "rows")
    fr = frames(10)
    print("frames:", len(fr), "| widest",
          max(max(len(l) for l in x.split(chr(10))) for x in fr), "| grid", FW, "x", FH)
    for i in (0, 2, 5):
        print(f"\n--- phase {i}/10 ---")
        print(fr[i])
