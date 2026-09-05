# -*- coding: utf-8 -*-
"""학습지 '연마(硏磨) 원의 둘레와 넓이' — 그림·심볼 SVG 생성.

surisomath-a4 규격을 따른다: Computer Modern, 도형 선 0.7pt, 끈 1pt, 보조선 0.4pt,
블록 높이는 22pt의 배수. 색칠한 부분은 피타고라스 학습지와 같이 잉크 10% 틴트.
심볼은 vectorize로 비트맵을 패스로 떠서 쓴다.

    python build/연마_원의둘레와넓이/figures.py
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "lib"))
sys.path.insert(0, str(ROOT / "build"))
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "surisomath-a4" / "templates"))

import suriso
import vectorize
import figure as fig  # import만으로 rcParams(CM + KoPub 폴백)가 잡힌다

import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, Polygon, Wedge

OUT = HERE / "figures"
OUT.mkdir(exist_ok=True)

GRID = 22.0
PT = 1 / 72
INK = fig.INK          # neutral-1000
EDGE = 0.7             # 도형 선
STRING = 1.0           # 끈(그래프 선 두께)
AUX = 0.4              # 보조선
DOT = 2.4              # 점 지름(pt)
TINT = 0.10            # 색칠한 부분
LABEL = 10.0


# ── 공통 ────────────────────────────────────────────────────────────────

def canvas(units: int, x0, x1, y0, y1):
    """높이 units×22pt, 데이터 비율 그대로의 캔버스."""
    scale = units * GRID / (y1 - y0)
    w = (x1 - x0) * scale
    f = plt.figure(figsize=(w * PT, units * GRID * PT))
    f.patch.set_alpha(0)
    ax = f.add_axes((0, 0, 1, 1))
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.pt = scale                  # 1단위가 몇 pt인지. 치수선 눈금 길이에 쓴다
    return f, ax


def seg(ax, p, q, lw=EDGE):
    ax.plot([p[0], q[0]], [p[1], q[1]], color=INK, linewidth=lw,
            solid_capstyle="round")


def circle(ax, c, r, lw=EDGE):
    ax.add_patch(Circle(c, r, facecolor="none", edgecolor=INK, linewidth=lw))


def arc(ax, c, r, t1, t2, lw=EDGE):
    ax.add_patch(Arc(c, 2 * r, 2 * r, angle=0, theta1=t1, theta2=t2,
                     linewidth=lw, color=INK))


def dot(ax, p):
    ax.plot([p[0]], [p[1]], marker="o", markersize=DOT, markeredgewidth=0,
            color=INK, linestyle="none", zorder=5)


def label(ax, x, y, s, ha="center", va="center", size=LABEL):
    ax.text(x, y, s, ha=ha, va=va, fontsize=size, color=INK)


def shade(ax, pts):
    ax.add_patch(Polygon(pts, closed=True, facecolor=INK, alpha=TINT,
                         edgecolor="none"))


def right_angle(ax, corner, dx, dy, s):
    """꼭짓점 corner에서 (dx, dy) 방향으로 한 변 s인 직각 표시."""
    x, y = corner
    pts = [(x + dx * s, y), (x + dx * s, y + dy * s), (x, y + dy * s)]
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=INK,
            linewidth=AUX)


TICK = 3.0             # 치수선 끝 눈금 반길이(pt)


def dim(ax, p, q, text, side=1, gap=0.0, lw=AUX):
    """p에서 q까지 치수선. 양끝에 수직 눈금을 긋고 글은 side 쪽(법선 방향)에 둔다.
    gap을 주면 p·q에서 법선 방향으로 그만큼 띄운 자리에 긋는다(도형 변 옆 치수)."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    nx, ny = -uy * side, ux * side          # side 쪽 법선
    p = (p[0] + nx * gap, p[1] + ny * gap)
    q = (q[0] + nx * gap, q[1] + ny * gap)
    seg(ax, p, q, lw=lw)
    t = TICK / ax.pt
    for e in (p, q):
        seg(ax, (e[0] - nx * t, e[1] - ny * t), (e[0] + nx * t, e[1] + ny * t), lw=lw)
    if not text:
        return
    off = 7.0 / ax.pt
    m = ((p[0] + q[0]) / 2 + nx * off, (p[1] + q[1]) / 2 + ny * off)
    if abs(nx) > abs(ny):
        label(ax, m[0], m[1], text, ha="left" if nx > 0 else "right")
    else:
        label(ax, m[0], m[1], text, va="bottom" if ny > 0 else "top")


def polar(c, r, deg):
    return (c[0] + r * math.cos(math.radians(deg)),
            c[1] + r * math.sin(math.radians(deg)))


def arc_pts(c, r, t1, t2, n=48):
    return [polar(c, r, t1 + (t2 - t1) * i / n) for i in range(n + 1)]


def save(f, name):
    f.savefig(OUT / name, format="svg", transparent=True)
    plt.close(f)
    print(f"  {name}")


# ── 심볼 — 모든 쪽 본문 영역 오른쪽 아래 칸, 높이 22pt(한 칸) ──────────────────────────────

def symbol():
    d, (bx, by, bw, bh) = vectorize.trace(str(suriso.SYMBOL))
    H = GRID
    s = H / bh
    W = bw * s
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.2f}pt" height="{H:.2f}pt" '
        f'viewBox="0 0 {W:.2f} {H:.2f}">'
        f'<path fill="{suriso.INK_HEX}" fill-rule="evenodd" '
        f'transform="translate({-bx * s:.3f},{-by * s:.3f}) scale({s:.6f})" d="{d}"/>'
        "</svg>"
    )
    (OUT / "symbol.svg").write_text(svg, encoding="utf-8")
    print(f"  symbol.svg  ({W:.0f}×{H:.0f}pt)")


# ── 문제 2 묶음 — 끈으로 묶은 원 ────────────────────────────────────────
# 끈은 원 둘레에서 살짝 띄워 1pt로 그린다. 붙여 그리면 원의 선과 겹쳐 안 보인다.

def p2():
    r, o = 8.0, 0.55
    cs = [(8, 8), (24, 8), (40, 8)]
    f, ax = canvas(5, -1.5, 52.5, -1.5, 18.0)
    for c in cs:
        circle(ax, c, r)
        dot(ax, c)
    seg(ax, (8, 16 + o), (40, 16 + o), lw=STRING)
    seg(ax, (8, -o), (40, -o), lw=STRING)
    arc(ax, cs[0], r + o, 90, 270, lw=STRING)
    arc(ax, cs[2], r + o, -90, 90, lw=STRING)
    dim(ax, cs[2], (48, 8), "8cm")
    save(f, "p2.svg")


def p2_1():
    r, o = 5.0, 0.4
    cs = [(5, 5), (15, 5), (5, 15), (15, 15)]
    f, ax = canvas(6, -1.2, 24.0, -1.2, 21.3)
    for c in cs:
        circle(ax, c, r)
        dot(ax, c)
    seg(ax, (5, 20 + o), (15, 20 + o), lw=STRING)
    seg(ax, (5, -o), (15, -o), lw=STRING)
    seg(ax, (-o, 5), (-o, 15), lw=STRING)
    seg(ax, (20 + o, 5), (20 + o, 15), lw=STRING)
    arc(ax, (5, 15), r + o, 90, 180, lw=STRING)
    arc(ax, (5, 5), r + o, 180, 270, lw=STRING)
    arc(ax, (15, 5), r + o, 270, 360, lw=STRING)
    arc(ax, (15, 15), r + o, 0, 90, lw=STRING)
    dim(ax, (15, 15), (20, 15), "5cm")
    save(f, "p2_1.svg")


def p2_2():
    r, o = 10.5, 0.6
    h = 21 * math.sqrt(3) / 2
    bl, br, t = (10.5, 10.5), (31.5, 10.5), (21.0, 10.5 + h)
    f, ax = canvas(7, -1.5, 43.5, -1.8, 10.5 + h + r + 1.8)
    for c in (bl, br, t):
        circle(ax, c, r)
        dot(ax, c)
    # 끈: 바깥 접선 세 개 + 120° 호 세 개
    for a, b, deg in ((bl, br, -90), (br, t, 30), (t, bl, 150)):
        n = (math.cos(math.radians(deg)), math.sin(math.radians(deg)))
        seg(ax, (a[0] + n[0] * (r + o), a[1] + n[1] * (r + o)),
            (b[0] + n[0] * (r + o), b[1] + n[1] * (r + o)), lw=STRING)
    arc(ax, br, r + o, -90, 30, lw=STRING)
    arc(ax, t, r + o, 30, 150, lw=STRING)
    arc(ax, bl, r + o, 150, 270, lw=STRING)
    dim(ax, (t[0] - r, t[1]), (t[0] + r, t[1]), "21cm")
    save(f, "p2_2.svg")


# ── 문제 3 묶음 — 색칠한 부분 ───────────────────────────────────────────

def p3():
    R = 6.0
    O, L, Rr = (0, 0), (-3, 0), (3, 0)
    f, ax = canvas(6, -7.6, 7.6, -7.6, 7.6)
    shade(ax, arc_pts(O, R, 180, 360) + arc_pts(Rr, 3, 0, 180)
          + arc_pts(L, 3, 0, -180))
    circle(ax, O, R)
    seg(ax, (-R, 0), (R, 0))
    arc(ax, Rr, 3, 0, 180)
    arc(ax, L, 3, 180, 360)
    for p in (O, L, Rr):
        dot(ax, p)
    dim(ax, (-R, 0), (0, 0), "6cm", gap=1.1)
    save(f, "p3.svg")


def p3_1():
    s, r = 18.0, 9.0
    corners = [(0, 0), (s, 0), (s, s), (0, s)]
    f, ax = canvas(6, -1.5, 29.5, -4.6, 19.5)
    for c, t1 in zip(corners, (0, 90, 180, 270)):
        ax.add_patch(Wedge(c, r, t1, t1 + 90, facecolor=INK, alpha=TINT,
                           edgecolor="none"))
    for c, t1 in zip(corners, (0, 90, 180, 270)):
        arc(ax, c, r, t1, t1 + 90)
    for i in range(4):
        seg(ax, corners[i], corners[(i + 1) % 4])
    for c in corners:
        dot(ax, c)
    m = 1.0
    right_angle(ax, (0, 0), 1, 1, m)
    right_angle(ax, (s, 0), -1, 1, m)
    right_angle(ax, (s, s), -1, -1, m)
    right_angle(ax, (0, s), 1, -1, m)
    dim(ax, (s, 0), (s, s), "18cm", side=-1, gap=1.4)    # 오른쪽 변
    dim(ax, (0, 0), (s, 0), "18cm", side=-1, gap=1.4)    # 아래 변
    save(f, "p3_1.svg")


def p3_2():
    s, r = 20.0, 10.0
    A, B = (20, 10), (10, 0)             # 오른쪽 반원·아래 반원의 중심
    f, ax = canvas(6, -1.5, 32.0, -4.9, 21.5)
    # 두 반원 바깥의 왼쪽 위 조각
    shade(ax, [(0, 0), (0, s), (s, s)] + arc_pts(A, r, 90, 180)
          + arc_pts(B, r, 90, 180))
    # 두 반원이 겹치는 렌즈
    shade(ax, arc_pts(A, r, 180, 270) + arc_pts(B, r, 0, 90))
    arc(ax, A, r, 90, 270)
    arc(ax, B, r, 0, 180)
    corners = [(0, 0), (s, 0), (s, s), (0, s)]
    for i in range(4):
        seg(ax, corners[i], corners[(i + 1) % 4])
    dot(ax, A)
    dot(ax, B)
    m = 1.1
    right_angle(ax, (0, 0), 1, 1, m)
    right_angle(ax, (s, 0), -1, 1, m)
    right_angle(ax, (s, s), -1, -1, m)
    right_angle(ax, (0, s), 1, -1, m)
    dim(ax, (s, 0), (s, s), "20cm", side=-1, gap=1.5)
    dim(ax, (0, 0), (s, 0), "20cm", side=-1, gap=1.5)
    save(f, "p3_2.svg")


# ── 문제 4 묶음 — 원주와 넓이 사이 ──────────────────────────────────────

def p4():
    O = (0, 0)
    f, ax = canvas(5, -7.4, 11.6, -7.4, 7.4)
    circle(ax, O, 6)
    circle(ax, O, 4)
    seg(ax, (-6, 0), (6, 0))
    dot(ax, O)
    dim(ax, (4, 0), (6, 0), "", gap=0.8)    # 고리 안, 지름선 위에 띄운 치수선
    seg(ax, (5, 1.1), (7.6, 2.6), lw=AUX)   # 글은 지시선으로 밖에
    label(ax, 7.9, 2.9, "2cm", ha="left", va="bottom")
    save(f, "p4.svg")


def p4_1():
    O, S = (0, 0), (-5, 0)
    f, ax = canvas(5, -11.6, 11.6, -11.6, 11.6)
    circle(ax, O, 10)
    circle(ax, S, 5)
    seg(ax, (-10, 0), (10, 0))
    dot(ax, O)
    dot(ax, S)
    save(f, "p4_1.svg")


def p4_2():
    O = (0, 0)
    f, ax = canvas(6, -10.5, 10.5, -10.5, 10.5)
    circle(ax, O, 9)
    for c in ((0, 6), (0, 0), (0, -6)):
        circle(ax, c, 3)
        dot(ax, c)
    seg(ax, (0, -9), (0, 9))
    save(f, "p4_2.svg")


if __name__ == "__main__":
    print("figures/")
    symbol()
    p2()
    p2_1()
    p2_2()
    p3()
    p3_1()
    p3_2()
    p4()
    p4_1()
    p4_2()
