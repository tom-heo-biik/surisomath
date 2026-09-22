# -*- coding: utf-8 -*-
"""시험대비 · 2026학년도 2학기 중간고사 · 중3 · 원과직선 — 도형 그림 스무 장.

도우미는 surisomath-grind 스킬의 grind_figure를 쓴다. build.py가 import 경로를 잡아
주므로 이 파일은 build.py로 실행한다.

    python .claude/skills/surisomath-exam/templates/build.py build/시험대비/20262학기중간/중3/원과직선/problems.yaml

원은 g.circle, 현·접선은 g.seg, 중심은 g.dot, 길이는 연마와 같이 점선 곡선(g.dim), 직각은
corner_mark, 같은 각은 호에 획(ticks=1). 길이 곡선은 책처럼 꼭짓점에서 꼭짓점까지 잇는다(trim 없음 —
양끝을 물리면 선분 끝과 이어지지 않은 느낌이라 선생님이 되돌렸다, 2026-09-23). 그림은 단 글 너비(229pt) 안에 들어야 하고 y 범위가
배율을 정한다. 점의 자리는 책 그림(사진)을 그대로 따른다.

문제가 정하지 않는 것은 책 그림에 맞춰 골랐다: 001 위 직선의 기울기 17°, 003 현의 기울기 −40°,
004 OC의 방향 150°, 005 P의 방향 140°, 007 A·B·C의 방향 195°·45°·−15°(호 AB : 호 BC = 5 : 2),
011 DE의 접점 방향 220°, 013 P에서의 접선 길이 9와 꼭짓점의 접선 길이 6·5·3·2·1(이웃한 두 원이
공통변 위의 한 점에서 접하도록 접선 길이로 짓는다), 017 l₁·l₂의 높이 1.2·−0.8, 020 삼각형의
모양(내접원 3, 방접원 8, OO' = 13이면 AC = 12만 정해진다 — BC ≈ 16.66, AB ≈ 9.74).
색칠은 문제가 가리키는 것만(007·010·012·014). 010은 삼각형에서 원을 뺀 부분이라 구멍 있는
패스로 칠한다.
"""
from __future__ import annotations

import math

from matplotlib.patches import PathPatch
from matplotlib.path import Path

import grind_figure as g

g.setup(__file__)

R2, R3 = math.sqrt(2), math.sqrt(3)


# ── 공통 ────────────────────────────────────────────────────────────────

def dist(p, q):
    return math.hypot(p[0] - q[0], p[1] - q[1])


def unit(p, q):
    """p에서 q로 향하는 단위벡터."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    n = math.hypot(dx, dy)
    return dx / n, dy / n


def lerp(p, q, t):
    return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)


def mid(p, q):
    return lerp(p, q, 0.5)


def bisector(P, Q, R):
    """꼭짓점 Q에서 안쪽 각 PQR의 이등분선 방향(단위벡터)."""
    u, v = unit(Q, P), unit(Q, R)
    d = (u[0] + v[0], u[1] + v[1])
    n = math.hypot(*d)
    return d[0] / n, d[1] / n


def meet(P, d, Q, e):
    """직선 P + t·d 와 Q + s·e 의 교점."""
    det = d[0] * e[1] - d[1] * e[0]
    rx, ry = Q[0] - P[0], Q[1] - P[1]
    t = (rx * e[1] - ry * e[0]) / det
    return P[0] + t * d[0], P[1] + t * d[1]


def line_dist(P, A, B):
    """점 P에서 직선 AB까지의 거리."""
    dx, dy = B[0] - A[0], B[1] - A[1]
    return abs(dx * (P[1] - A[1]) - dy * (P[0] - A[0])) / math.hypot(dx, dy)


def incircle(A, B, C):
    """삼각형 ABC의 내심과 내접원의 반지름."""
    a, b, c = dist(B, C), dist(C, A), dist(A, B)
    s = a + b + c
    I = ((a * A[0] + b * B[0] + c * C[0]) / s, (a * A[1] + b * B[1] + c * C[1]) / s)
    return I, line_dist(I, A, B)


def incircle_quad(A, B, C, D):
    """접선사각형 ABCD의 내접원. 이웃한 두 꼭짓점 A, B의 각의 이등분선이 만나는 점이 중심이다."""
    I = meet(A, bisector(D, A, B), B, bisector(A, B, C))
    return I, line_dist(I, A, B)


def shade_minus_circle(ax, outer, c, r, n=90):
    """다각형 outer(반시계)에서 원(c, r)을 뺀 부분을 잉크 10% 틴트로 칠한다. 원을 시계 방향
    다각형으로 넣어 nonzero 규칙으로 구멍을 낸다."""
    ring = [g.polar(c, r, -360.0 * i / n) for i in range(n)]
    verts = list(outer) + [outer[0]] + ring + [ring[0]]
    codes = ([Path.MOVETO] + [Path.LINETO] * (len(outer) - 1) + [Path.CLOSEPOLY]
             + [Path.MOVETO] + [Path.LINETO] * (n - 1) + [Path.CLOSEPOLY])
    ax.add_patch(PathPatch(Path(verts, codes), facecolor=g.INK, alpha=g.TINT, edgecolor="none"))


def center(ax, p, text, dx=4.0, dy=0.0, ha="left", va="center"):
    """원의 중심: 점과 이름."""
    g.dot(ax, p)
    g.name(ax, p, text, dx=dx, dy=dy, ha=ha, va=va)


# ── 001 — 변 CD를 맞댄 두 접선사각형 ─────────────────────────────────────
# B(0, 0), C(6, 0), E(18, 0). 위 직선은 기울기 17°. A는 AB + CD = AD + BC = 14,
# CD + EF = CE + DF = 17을 만족하도록 뉴턴법으로 푼 값(문제는 A의 자리를 정하지 않는다).

def p1():
    B, C, E = (0.0, 0.0), (6.0, 0.0), (18.0, 0.0)
    A = (3.3231, 4.4688)
    u = (math.cos(math.radians(17)), math.sin(math.radians(17)))
    D = (A[0] + 8 * u[0], A[1] + 8 * u[1])
    F = (A[0] + 13 * u[0], A[1] + 13 * u[1])
    O1, r1 = incircle_quad(A, B, C, D)
    O2, r2 = incircle_quad(C, E, F, D)
    fig, ax = g.canvas(6, -2.0, 10.4)
    g.poly(ax, [A, B, E, F])
    g.seg(ax, C, D)
    g.circle(ax, O1, r1)
    g.circle(ax, O2, r2)
    center(ax, O1, "O", dx=0, dy=-5, ha="center", va="top")
    center(ax, O2, "$\\mathrm{O}'$", dx=0, dy=-5, ha="center", va="top")
    g.dim(ax, A, D, "8", side=1)
    g.dim(ax, D, F, "5", side=1)
    g.dim(ax, B, C, "6", side=-1)
    g.dim(ax, C, E, "12", side=-1)
    g.name(ax, A, "A", dx=-4, dy=2, ha="right", va="bottom")
    g.name(ax, B, "B", dx=-4, dy=-2, ha="right", va="top")
    g.name(ax, C, "C", dy=-5, va="top")
    g.name(ax, D, "D", dx=-2, dy=5, ha="right", va="bottom")
    g.name(ax, E, "E", dx=4, dy=-2, ha="left", va="top")
    g.name(ax, F, "F", dx=4, dy=2, ha="left", va="bottom")
    g.save(fig, "p1.svg")


# ── 002 — 서로 수직인 두 현 ──────────────────────────────────────────────
# E가 원점. AB는 오른쪽 아래로, CD는 왼쪽 아래로(책처럼 E가 원의 위쪽). r² = 68.
# CE = 8 − √19, ED = 8 + √19(CE·ED = AE·EB = 45).

def p2():
    a = (1 / R2, -1 / R2)
    c = (-1 / R2, -1 / R2)
    ce = 8 - math.sqrt(19)
    E = (0.0, 0.0)
    A = (-5 * a[0], -5 * a[1])
    B = (9 * a[0], 9 * a[1])
    C = (-ce * c[0], -ce * c[1])
    D = ((16 - ce) * c[0], (16 - ce) * c[1])
    O = (2 * a[0] + math.sqrt(19) * c[0], 2 * a[1] + math.sqrt(19) * c[1])
    fig, ax = g.canvas(6, -13.57, 6.14)
    g.circle(ax, O, math.sqrt(68))
    g.seg(ax, A, B)
    g.seg(ax, C, D)
    g.corner_mark(ax, E, a, c)
    g.dim(ax, A, E, "5", side=-1)
    g.dim(ax, E, B, "9", side=1)
    g.dim(ax, C, D, "16", side=1)
    g.name(ax, A, "A", dx=-3, dy=4, ha="right", va="bottom")
    g.name(ax, B, "B", dx=4, dy=-3, ha="left", va="top")
    g.name(ax, C, "C", dx=3, dy=4, ha="left", va="bottom")
    g.name(ax, D, "D", dx=-4, dy=-3, ha="right", va="top")
    g.name(ax, E, "E", dx=2, dy=7, ha="left", va="bottom")
    g.save(fig, "p2.svg")


# ── 003 — 같은 간격의 평행한 세 현 ──────────────────────────────────────
# r = 5. 중심에서 EF까지 2, CD까지 3, AB까지 4(간격 1). 현은 −40° 방향, 왼쪽 아래에 있다.

def p3():
    u = (math.cos(math.radians(-40)), math.sin(math.radians(-40)))
    n = (math.cos(math.radians(-130)), math.sin(math.radians(-130)))

    def chord(d, half):
        cx, cy = d * n[0], d * n[1]
        return (cx - half * u[0], cy - half * u[1]), (cx + half * u[0], cy + half * u[1])

    E, F = chord(2.0, math.sqrt(21))
    C, D = chord(3.0, 4.0)
    A, B = chord(4.0, 3.0)
    O = (0.0, 0.0)
    fig, ax = g.canvas(6, -6.59, 5.51)
    g.circle(ax, O, 5.0)
    for p, q in ((A, B), (C, D), (E, F)):
        g.seg(ax, p, q)
    center(ax, O, "O")
    for p, s in ((E, "E"), (C, "C"), (A, "A")):
        g.name(ax, p, s, dx=-4, ha="right")
    for p, s in ((B, "B"), (D, "D"), (F, "F")):
        g.name(ax, p, s, dy=-4, va="top")
    g.save(fig, "p3.svg")


# ── 004 — 동심원, 작은 원에 접하는 현 AC와 OC ⊥ AB ──────────────────────
# AC = 4√7, AB = 6√7. OC는 150° 방향, AB는 OC와 M(OM = 1)에서 직각.

def p4():
    O = (0.0, 0.0)
    C = g.polar(O, 8.0, 150)
    M = g.polar(O, 1.0, 150)
    d = (math.cos(math.radians(60)), math.sin(math.radians(60)))
    h = 3 * math.sqrt(7)
    A = (M[0] - h * d[0], M[1] - h * d[1])
    B = (M[0] + h * d[0], M[1] + h * d[1])
    fig, ax = g.canvas(6, -8.87, 9.73)
    g.circle(ax, O, 8.0)
    g.circle(ax, O, 6.0)
    g.seg(ax, O, C)
    g.seg(ax, A, C)
    g.seg(ax, A, B)
    g.corner_mark(ax, M, unit(M, O), unit(M, A))
    center(ax, O, "O")
    g.name(ax, A, "A", dx=-3, dy=-4, ha="right", va="top")
    g.name(ax, B, "B", dx=3, dy=3, ha="left", va="bottom")
    g.name(ax, C, "C", dx=-4, dy=3, ha="right", va="bottom")
    g.save(fig, "p4.svg")


# ── 005 — 중심에서 6 떨어진 점 P를 지나는 현 ────────────────────────────
# r = 10. P는 140° 방향. 반지름 OQ가 P를 지난다.

def p5():
    O = (0.0, 0.0)
    P = g.polar(O, 6.0, 140)
    Q = g.polar(O, 10.0, 140)
    fig, ax = g.canvas(6, -11.0, 11.0)
    g.circle(ax, O, 10.0)
    g.seg(ax, Q, O, lw=g.AUX)
    g.dot(ax, P)
    g.dot(ax, O)
    g.dim(ax, Q, O, "10", side=-1)
    g.dim(ax, P, O, "6", side=1)
    g.name(ax, P, "P", dx=1, dy=5, ha="center", va="bottom")
    g.name(ax, O, "O", dy=-5, va="top")
    g.save(fig, "p5.svg")


# ── 006 — AB : CD = 1 : √3, AH = 4 ───────────────────────────────────────
# r = √13. AB는 y = 3(A(−2, 3), B(2, 3)), CD는 y = −1(반지름 2√3). H(−2, −1). BH = 4√2.

def p6():
    A, B = (-2.0, 3.0), (2.0, 3.0)
    C, D = (-2 * R3, -1.0), (2 * R3, -1.0)
    H = (-2.0, -1.0)
    fig, ax = g.canvas(6, -4.4, 4.4)
    g.circle(ax, (0.0, 0.0), math.sqrt(13))
    g.seg(ax, A, B)
    g.seg(ax, C, D)
    g.seg(ax, A, H)
    g.seg(ax, B, H)
    g.corner_mark(ax, A, (1, 0), (0, -1))
    g.corner_mark(ax, H, (0, 1), (1, 0))
    g.dim(ax, A, H, "4", side=-1)
    g.name(ax, A, "A", dx=-4, dy=3, ha="right", va="bottom")
    g.name(ax, B, "B", dx=4, dy=3, ha="left", va="bottom")
    g.name(ax, C, "C", dx=-4, ha="right")
    g.name(ax, D, "D", dx=4, ha="left")
    g.name(ax, H, "H", dy=-5, va="top")
    g.save(fig, "p6.svg")


# ── 007 — OH = OI, 호 AB : 호 BC = 5 : 2 ──────────────────────────────────
# r = 4. 호 AB = 150°, BC = 60°, CA = 150°. A는 195°, C는 −15°, B는 45° 방향. 삼각형 색칠.

def p7():
    O = (0.0, 0.0)
    A, B, C = g.polar(O, 4.0, 195), g.polar(O, 4.0, 45), g.polar(O, 4.0, -15)
    H, I = mid(A, B), mid(A, C)
    fig, ax = g.canvas(6, -4.8, 4.8)
    g.shade(ax, [A, B, C])
    g.circle(ax, O, 4.0)
    g.poly(ax, [A, B, C])
    g.seg(ax, O, H, lw=g.AUX)
    g.seg(ax, O, I, lw=g.AUX)
    g.corner_mark(ax, H, unit(H, B), unit(H, O))
    g.corner_mark(ax, I, (1, 0), (0, 1))
    center(ax, O, "O")
    g.name(ax, A, "A", dx=-4, ha="right")
    g.name(ax, B, "B", dx=3, dy=3, ha="left", va="bottom")
    g.name(ax, C, "C", dx=4, ha="left")
    g.name(ax, H, "H", dx=-4, dy=2, ha="right", va="bottom")
    g.name(ax, I, "I", dy=-5, va="top")
    g.save(fig, "p7.svg")


# ── 008 — 직사각형 안의 사분원과 B에서 그은 접선 ──────────────────────────
# B(0, 0), C(10, 0), D(10, 6), A(0, 6). 사분원은 C 중심 반지름 6. E(8, 6).

def p8():
    B, C, D, A = (0.0, 0.0), (10.0, 0.0), (10.0, 6.0), (0.0, 6.0)
    E = (8.0, 6.0)
    fig, ax = g.canvas(6, -1.6, 7.2)
    g.rect(ax, B, 10.0, 6.0)
    g.arc(ax, C, 6.0, 90, 180)
    g.seg(ax, B, E)
    g.dim(ax, B, C, "10", side=-1)
    g.dim(ax, C, D, "6", side=-1)
    g.name(ax, A, "A", dx=-4, dy=3, ha="right", va="bottom")
    g.name(ax, B, "B", dx=-4, dy=-3, ha="right", va="top")
    g.name(ax, C, "C", dx=4, dy=-3, ha="left", va="top")
    g.name(ax, D, "D", dx=4, dy=3, ha="left", va="bottom")
    g.name(ax, E, "E", dy=5, va="bottom")
    g.save(fig, "p8.svg")


# ── 009 — 직선 l에 접하며 A에서 외접하는 두 원 ────────────────────────────
# O₁(0, 4) r = 4, O₂(4, 1) r = 1, B(0, 0), C(4, 0), A(3.2, 1.6). ∠BAC = 90°.

def p9():
    O1, O2 = (0.0, 4.0), (4.0, 1.0)
    B, C = (0.0, 0.0), (4.0, 0.0)
    A = lerp(O1, O2, 4 / 5)
    fig, ax = g.canvas(6, -1.39, 8.39)
    g.seg(ax, (-4.9, 0.0), (6.4, 0.0))
    g.circle(ax, O1, 4.0)
    g.circle(ax, O2, 1.0)
    g.poly(ax, [A, B, C])
    center(ax, O1, "$\\mathrm{O}_1$", dx=0, dy=5, ha="center", va="bottom")
    g.dot(ax, O2)
    g.leader(ax, O2, "$\\mathrm{O}_2$", dx=1, dy=1)
    g.name(ax, A, "A", dx=-4, dy=3, ha="right", va="bottom")
    g.name(ax, B, "B", dy=-5, va="top")
    g.name(ax, C, "C", dy=-5, va="top")
    g.name(ax, (6.4, 0.0), "$l$", dx=4, ha="left")
    g.save(fig, "p9.svg")


# ── 010 — 내접원을 뺀 직각삼각형 ─────────────────────────────────────────
# ∠C = 90°, AB = 13, r = 2 → BC = 12, AC = 5. B(0, 0), C(12, 0), A(12, 5). O(10, 2).

def p10():
    B, C, A = (0.0, 0.0), (12.0, 0.0), (12.0, 5.0)
    O = (10.0, 2.0)
    fig, ax = g.canvas(5, -1.4, 7.2)
    shade_minus_circle(ax, [B, C, A], O, 2.0)
    g.circle(ax, O, 2.0)
    g.poly(ax, [A, B, C])
    g.right_angle(ax, C, -1, 1)
    g.dim(ax, B, A, "13", side=1)
    center(ax, O, "O")
    g.name(ax, A, "A", dy=5, va="bottom")
    g.name(ax, B, "B", dx=-4, dy=-3, ha="right", va="top")
    g.name(ax, C, "C", dx=4, dy=-3, ha="left", va="top")
    g.save(fig, "p10.svg")


# ── 011 — 내접원에 접하는 선분 DE가 자르는 삼각형 BED ─────────────────────
# B(0, 0), C(18, 0), A(11.25, 9.92). DE는 내접원의 220° 방향 점에서의 접선(책처럼 B 쪽 귀퉁이).

def p11():
    B, C = (0.0, 0.0), (18.0, 0.0)
    A = (11.25, math.sqrt(225 - 11.25 ** 2))
    O, r = incircle(A, B, C)
    T = g.polar(O, r, 220)
    t = (-math.sin(math.radians(220)), math.cos(math.radians(220)))
    D = meet(T, t, B, unit(B, A))
    E = meet(T, t, B, (1.0, 0.0))
    fig, ax = g.canvas(7, -2.86, 11.72)
    g.poly(ax, [A, B, C])
    g.circle(ax, O, r)
    g.seg(ax, D, E)
    center(ax, O, "O")
    g.dim(ax, B, A, "15", side=1, gap=g.pt(ax, 20))
    g.dim(ax, A, C, "12", side=1)
    g.dim(ax, B, C, "18", side=-1, gap=g.pt(ax, 20))
    g.name(ax, A, "A", dy=5, va="bottom")
    g.name(ax, B, "B", dx=-4, dy=-3, ha="right", va="top")
    g.name(ax, C, "C", dx=4, dy=-3, ha="left", va="top")
    g.name(ax, D, "D", dx=-4, dy=1, ha="right")
    g.name(ax, E, "E", dy=-4, va="top")
    g.save(fig, "p11.svg")


# ── 012 — 직각이등변삼각형의 내접원과 접점 삼각형 DEF ─────────────────────
# A(0, √2), B(−√2, 0), C(√2, 0). r = 2 − √2. D는 AB 위, E(0, 0), F는 AC 위.

def p12():
    r = 2 - R2
    A, B, C = (0.0, R2), (-R2, 0.0), (R2, 0.0)
    O = (0.0, r)
    D = (-r / R2, R2 - r / R2)
    F = (r / R2, R2 - r / R2)
    E = (0.0, 0.0)
    fig, ax = g.canvas(6, -0.45, 1.95)
    g.shade(ax, [D, E, F])
    g.circle(ax, O, r)
    g.poly(ax, [A, B, C])
    g.poly(ax, [D, E, F])
    g.corner_mark(ax, A, unit(A, B), unit(A, C))
    g.dim(ax, B, A, "2", side=1, gap=g.pt(ax, 18))
    g.dim(ax, A, C, "2", side=1, gap=g.pt(ax, 18))
    center(ax, O, "O", dx=0, dy=5, ha="center", va="bottom")
    g.name(ax, A, "A", dy=5, va="bottom")
    g.name(ax, B, "B", dx=-4, dy=-3, ha="right", va="top")
    g.name(ax, C, "C", dx=4, dy=-3, ha="left", va="top")
    g.name(ax, D, "D", dx=-4, dy=2, ha="right")
    g.name(ax, F, "F", dx=4, dy=2, ha="left")
    g.name(ax, E, "E", dy=-5, va="top")
    g.save(fig, "p12.svg")


# ── 013 — 네 삼각형의 내접원과 육각형 PABCDE ──────────────────────────────
# 접선 길이로 짓는다: P에서 t = 9, A·B·C·D·E에서 6·5·3·2·1 (PA = 15, BC = 8, DE = 3).
# 변 PB·PC·PD를 이웃한 두 원이 같은 점(P에서 t)에서 접하므로 서로 접한다. 둘레 = 2(15 + 8 + 3) = 52.
# A는 205° 방향, 나머지는 P의 각을 더해 가며 시계 반대(아래를 돌아 오른쪽)로.

def p13():
    t, a, b, c, d, e = 9.0, 6.0, 5.0, 3.0, 2.0, 1.0
    sides = [(t + a, a + b, t + b), (t + b, b + c, t + c), (t + c, c + d, t + d), (t + d, d + e, t + e)]
    P = (0.0, 0.0)
    ang = 205.0
    pts = [g.polar(P, sides[0][0], ang)]                 # A
    for pa, ab, pb in sides:
        ang += math.degrees(math.acos((pa * pa + pb * pb - ab * ab) / (2 * pa * pb)))
        pts.append(g.polar(P, pb, ang))
    A, B, C, D, E = pts
    circles = [incircle(P, A, B), incircle(P, B, C), incircle(P, C, D), incircle(P, D, E)]
    fig, ax = g.canvas(7, -15.08, 2.09)
    g.poly(ax, [P, A, B, C, D, E])
    for q in (B, C, D):
        g.seg(ax, P, q)
    for k, (o, r) in enumerate(circles, 1):
        g.circle(ax, o, r)
        g.dot(ax, o)
        if k < 4:
            g.name(ax, o, f"$\\mathrm{{O}}_{k}$", dy=5, va="bottom")
    g.leader(ax, circles[3][0], "$\\mathrm{O}_4$", dx=1, dy=2)
    g.dim(ax, P, A, "15", side=-1)
    g.dim(ax, B, C, "8", side=-1)
    g.dim(ax, D, E, "3", side=-1)
    g.name(ax, P, "P", dy=5, va="bottom")
    g.name(ax, A, "A", dx=-5, ha="right")
    g.name(ax, B, "B", dx=-3, dy=-4, ha="right", va="top")
    g.name(ax, C, "C", dx=3, dy=-4, ha="left", va="top")
    g.name(ax, D, "D", dx=4, dy=-3, ha="left", va="top")
    g.name(ax, E, "E", dx=5, ha="left")
    g.save(fig, "p13.svg")


# ── 014 — 두 직각삼각형의 내접원과 평행사변형 EOFO' ──────────────────────
# AB = 12, BC = 16, AC = 20. O(4, 4), O'(12, 8). E = A에서 8, F = C에서 8. EF = 4, 넓이 16.

def p14():
    A, B, C, D = (0.0, 12.0), (0.0, 0.0), (16.0, 0.0), (16.0, 12.0)
    O, O2 = (4.0, 4.0), (12.0, 8.0)
    E, F = lerp(A, C, 8 / 20), lerp(C, A, 8 / 20)
    fig, ax = g.canvas(7, -1.6, 13.6)
    g.shade(ax, [E, O, F, O2])
    g.rect(ax, B, 16.0, 12.0)
    g.seg(ax, A, C)
    g.circle(ax, O, 4.0)
    g.circle(ax, O2, 4.0)
    g.poly(ax, [E, O, F, O2])
    g.dim(ax, O, E, "4", side=1)
    g.dim(ax, O2, F, "4", side=1)
    center(ax, O, "O", dx=-5, ha="right")
    center(ax, O2, "$\\mathrm{O}'$", dx=5, ha="left")
    g.name(ax, A, "A", dx=-4, dy=3, ha="right", va="bottom")
    g.name(ax, B, "B", dx=-4, dy=-3, ha="right", va="top")
    g.name(ax, C, "C", dx=4, dy=-3, ha="left", va="top")
    g.name(ax, D, "D", dx=4, dy=3, ha="left", va="bottom")
    # E·F는 대각선 위의 점이라 대각선 방향(왼쪽 위·오른쪽 아래)에 두면 선이 글자를 지난다.
    # 대각선의 법선 쪽 — E는 오른쪽 위(원 O 밖, 선분 O'E 위), F는 왼쪽 아래(원 O' 밖, 선분 OF 아래)
    g.name(ax, E, "E", dx=3, dy=5, ha="left", va="bottom")
    g.name(ax, F, "F", dx=-3, dy=-5, ha="right", va="top")
    g.save(fig, "p14.svg")


# ── 015 — 사각형 ABED와 삼각형 CDE의 내접원 ──────────────────────────────
# BE = 4, EC = 8, AB = 6. O(3, 3) r = 3, O'(10, 2) r = 2. 넓이의 비 9 : 4.

def p15():
    A, B, C, D = (0.0, 6.0), (0.0, 0.0), (12.0, 0.0), (12.0, 6.0)
    E = (4.0, 0.0)
    O, O2 = (3.0, 3.0), (10.0, 2.0)
    fig, ax = g.canvas(6, -1.4, 7.4)
    g.rect(ax, B, 12.0, 6.0)
    g.seg(ax, D, E)
    g.circle(ax, O, 3.0)
    g.circle(ax, O2, 2.0)
    center(ax, O, "O", dx=0, dy=-5, ha="center", va="top")
    center(ax, O2, "$\\mathrm{O}'$", dx=0, dy=-5, ha="center", va="top")
    g.name(ax, A, "A", dx=-4, dy=3, ha="right", va="bottom")
    g.name(ax, B, "B", dx=-4, dy=-3, ha="right", va="top")
    g.name(ax, C, "C", dx=4, dy=-3, ha="left", va="top")
    g.name(ax, D, "D", dx=4, dy=3, ha="left", va="bottom")
    g.name(ax, E, "E", dy=-5, va="top")
    g.save(fig, "p15.svg")


# ── 016 — 지름의 연장선과 현의 연장선이 만나는 P ──────────────────────────
# O(0, 0) r = 6, A(−6, 0), B(6, 0), D(0, −6), P(−8, 0). C는 직선 PD와 원의 다른 교점. AC = 6√2/5.

def p16():
    O, A, B, D, P = (0.0, 0.0), (-6.0, 0.0), (6.0, 0.0), (0.0, -6.0), (-8.0, 0.0)
    # 직선 PD: P + s(D − P). 원과의 교점 s는 |P|² − 36 = 28, 2P·(D−P) = 2(64 + 0)… 이차식으로 푼다
    dx, dy = D[0] - P[0], D[1] - P[1]
    qa, qb = dx * dx + dy * dy, 2 * (P[0] * dx + P[1] * dy)
    qc = P[0] ** 2 + P[1] ** 2 - 36
    s = (-qb - math.sqrt(qb * qb - 4 * qa * qc)) / (2 * qa)
    C = (P[0] + s * dx, P[1] + s * dy)
    fig, ax = g.canvas(6, -8.07, 6.61)
    g.circle(ax, O, 6.0)
    g.seg(ax, P, B)
    g.seg(ax, P, D)
    g.seg(ax, O, D)
    g.right_angle(ax, O, 1, -1)
    g.dot(ax, O)
    g.dim(ax, P, A, "2", side=1)
    g.dim(ax, A, O, "6", side=-1)
    g.name(ax, P, "P", dx=-4, ha="right")
    g.name(ax, A, "A", dx=2, dy=4, ha="left", va="bottom")
    g.name(ax, O, "O", dx=-2, dy=4, ha="right", va="bottom")
    g.name(ax, B, "B", dx=4, ha="left")
    g.name(ax, C, "C", dx=-4, dy=-2, ha="right", va="top")
    g.name(ax, D, "D", dy=-5, va="top")
    g.save(fig, "p16.svg")


# ── 017 — 평행한 두 직선이 원에서 자르는 두 현 ────────────────────────────
# r = 2. l₁은 y = 1.2, l₂는 y = −0.8(거리 2). 답(24)은 두 직선이 중심에서 같은 거리일 때다.

def p17():
    O = (0.0, 0.0)
    fig, ax = g.canvas(5, -2.5, 2.5)
    g.circle(ax, O, 2.0)
    for y, s in ((1.2, "$l_1$"), (-0.8, "$l_2$")):
        g.seg(ax, (-3.2, y), (3.2, y))
        g.name(ax, (-3.2, y), s, dx=-4, ha="right")
    center(ax, O, "O")
    g.save(fig, "p17.svg")


# ── 018 — 각 A의 이등분선 AD ─────────────────────────────────────────────
# B(0, 0), C(7, 0), A(1.5, √33.75). BD : DC = 6 : 8 → D(3, 0). AD = 6.

def p18():
    B, C = (0.0, 0.0), (7.0, 0.0)
    A = (1.5, math.sqrt(36 - 1.5 ** 2))
    D = (3.0, 0.0)
    fig, ax = g.canvas(6, -2.2, 7.2)
    g.poly(ax, [A, B, C])
    g.seg(ax, A, D)
    g.angle(ax, A, B, D, "", r=12, ticks=1)
    g.angle(ax, A, D, C, "", r=12, ticks=1)
    g.dim(ax, B, A, "6", side=1)
    g.dim(ax, A, C, "8", side=1)
    g.dim(ax, B, C, "7", side=-1, gap=g.pt(ax, 18))
    g.name(ax, A, "A", dy=5, va="bottom")
    g.name(ax, B, "B", dx=-4, dy=-3, ha="right", va="top")
    g.name(ax, C, "C", dx=4, dy=-3, ha="left", va="top")
    g.name(ax, D, "D", dy=-5, va="top")
    g.save(fig, "p18.svg")


# ── 019 — 두 원의 공통현 ─────────────────────────────────────────────────
# O₁(0, 0) r = 8, O₂(7, 0) r = 6. 교점 A(5.5, 3√15/2), B(5.5, −3√15/2). AB = 3√15.

def p19():
    O1, O2 = (0.0, 0.0), (7.0, 0.0)
    h = 3 * math.sqrt(15) / 2
    A, B = (5.5, h), (5.5, -h)
    fig, ax = g.canvas(7, -9.8, 9.8)
    g.circle(ax, O1, 8.0)
    g.circle(ax, O2, 6.0)
    g.seg(ax, A, B)
    g.seg(ax, O1, O2, lw=g.AUX)
    g.dim(ax, O1, O2, "7", side=1)
    center(ax, O1, "$\\mathrm{O}_1$", dx=-5, ha="right")
    # O₂는 현 AB(왼쪽 1.5)와 큰 원의 둘레(오른쪽 1) 사이에 끼어 있다. 이름을 점 바로 아래에 두되
    # 살짝 왼쪽으로 — 오른쪽 아래에 두면 큰 원의 둘레가 글자를 지난다(겹침 검사가 잡는다). 7칸으로
    # 배율을 키워 자리를 만든다
    center(ax, O2, "$\\mathrm{O}_2$", dx=-1.5, dy=-4, ha="center", va="top")
    g.name(ax, A, "A", dy=5, va="bottom")
    g.name(ax, B, "B", dy=-5, va="top")
    g.save(fig, "p19.svg")


# ── 020 — 내접원 O(3cm)와 방접원 O'(8cm), OO' = 13cm ──────────────────────
# B(0, 0). B에서 접선 길이는 O에 7.2, O'에 19.2(닮음비 3 : 8, 밑변 차 12). AC = 12.
# 삼각형의 모양은 정해지지 않으므로 책처럼 BC가 길게: s − a = 6 − √12, s − c = 6 + √12.

def p20():
    B = (0.0, 0.0)
    half = math.radians(math.degrees(math.atan2(3.0, 7.2)))       # ∠B의 절반
    ub = (math.cos(2 * half), math.sin(2 * half))                  # BA 방향
    s = 19.2
    a = s - (6 - math.sqrt(12))                                    # BC
    c = s - (6 + math.sqrt(12))                                    # AB
    C = (a, 0.0)
    A = (c * ub[0], c * ub[1])
    O, O2 = (7.2, 3.0), (19.2, 8.0)
    T, T2 = (7.2, 0.0), (19.2, 0.0)
    fig, ax = g.canvas(7, -2.9, 17.3)
    g.seg(ax, B, (22.0 * ub[0], 22.0 * ub[1]))
    g.seg(ax, B, (26.5, 0.0))
    g.seg(ax, A, C)
    g.circle(ax, O, 3.0)
    g.circle(ax, O2, 8.0)
    g.seg(ax, O, O2, lw=g.AUX)
    g.seg(ax, O, T, lw=g.AUX)
    g.seg(ax, O2, T2, lw=g.AUX)
    # 13cm: dim이 곡선 가운데(OO'의 중점 위)에 글을 두면 원 O'의 둘레가 글을 지난다 — 중점이 둘레에서
    # 2밖에 안 떨어져 있다. 책처럼 곡선은 글 없이 긋고 글은 O' 쪽(t = 0.66), 선분 위 9pt에 따로 둔다
    g.dim(ax, O, O2, "", side=1, gap=g.pt(ax, 26))
    n = (-5 / 13, 12 / 13)                                          # OO'의 왼쪽 법선
    q = lerp(O, O2, 0.66)
    g.name(ax, (q[0] + g.pt(ax, 9) * n[0], q[1] + g.pt(ax, 9) * n[1]), "13cm")
    g.dim(ax, O2, T2, "8cm", side=1)
    g.leader(ax, mid(O, T), "3cm", dx=-1, dy=-1)
    center(ax, O, "O", dx=-4, ha="right")
    center(ax, O2, "$\\mathrm{O}'$", dx=3, dy=4, ha="left", va="bottom")
    g.name(ax, A, "A", dx=-4, dy=2, ha="right", va="bottom")
    g.name(ax, B, "B", dx=-4, ha="right")
    g.name(ax, C, "C", dy=-5, va="top")
    g.save(fig, "p20.svg")


if __name__ == "__main__":
    print("figures/")
    p1()
    p2()
    p3()
    p4()
    p5()
    p6()
    p7()
    p8()
    p9()
    p10()
    p11()
    p12()
    p13()
    p14()
    p15()
    p16()
    p17()
    p18()
    p19()
    p20()
