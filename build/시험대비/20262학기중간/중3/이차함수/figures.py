# -*- coding: utf-8 -*-
"""시험대비 · 2026학년도 2학기 중간고사 · 중3 · 이차함수 — 좌표평면 그림 열넷.

도우미는 surisomath-grind 스킬의 grind_figure를 쓴다. build.py가 import 경로를 잡아
주므로 이 파일은 build.py로 실행한다.

    python .claude/skills/surisomath-exam/templates/build.py build/시험대비/20262학기중간/중3/이차함수/problems.yaml

좌표평면은 문제의 단위가 종이 위 크기와 무관하다. 가로세로 배율이 같아야 하므로 y 범위로
배율만 정한다(연마 2026.09.12의 002·003과 같다). 축은 0.4pt에 채운 화살촉, 그래프 선은
1pt(a4 그래프 규격), 도형(사각형·삼각형·선분)은 0.7pt, 점선 0.4pt, 색칠은 잉크 10% 틴트.
축 이름 x·y는 이탤릭, 원점 O와 점 이름은 정체. y 이름은 화살촉 옆의 빈 쪽, O는 곡선·숫자가
없는 쪽에 둔다. 그림은 단 글 너비(229pt) 안에 들어야 한다.

그래프는 실제 함수식으로 그린다. 문자 계수(a, k, m, b, c)는 답이나 그림에 맞는 값을 넣었다
(006 a=-1, 005 k=1.6, 007 a=b=1, 009 m=3, 018 b=2 c=8, 020 g=-x²+4x). 모든 그림이 축척대로다.
"""
from __future__ import annotations

import math

from matplotlib.patches import Polygon

import grind_figure as g

g.setup(__file__)

HEAD = 6.0            # 화살촉 길이(pt)


# ── 공통 ────────────────────────────────────────────────────────────────

def arrow(ax, p, q, lw=g.AUX):
    """p에서 q까지의 축. q 끝에 채운 화살촉(길이 HEAD pt, 밑변 HEAD×0.7pt)."""
    L = g.pt(ax, HEAD)
    dx, dy = q[0] - p[0], q[1] - p[1]
    n = math.hypot(dx, dy)
    ux, uy = dx / n, dy / n
    base = (q[0] - ux * L, q[1] - uy * L)
    g.seg(ax, p, base, lw=lw)
    w = L * 0.35
    ax.add_patch(Polygon([q, (base[0] - uy * w, base[1] + ux * w),
                          (base[0] + uy * w, base[1] - ux * w)],
                         closed=True, facecolor=g.INK, edgecolor="none"))


def plane(ax, x0, x1, y0, y1, o=(3, -3, "left", "top"), yside="left"):
    """두 축과 이름. x는 오른쪽 화살촉 옆, y는 위 화살촉의 yside 쪽, O는 o=(dx, dy, ha, va)."""
    arrow(ax, (x0, 0), (x1, 0))
    arrow(ax, (0, y0), (0, y1))
    g.name(ax, (x1, 0), "$x$", dx=4, ha="left")
    if yside == "left":
        g.name(ax, (0, y1), "$y$", dx=-4, ha="right")
    else:
        g.name(ax, (0, y1), "$y$", dx=4, ha="left")
    dx, dy, ha, va = o
    g.name(ax, (0, 0), "O", dx=dx, dy=dy, ha=ha, va=va)


def xs_between(xa, xb, n=120):
    return [xa + (xb - xa) * i / n for i in range(n + 1)]


def curve(ax, fn, xa, xb, lw=g.STRING):
    """y = fn(x)의 그래프. 1pt."""
    xs = xs_between(xa, xb)
    ax.plot(xs, [fn(x) for x in xs], color=g.INK, linewidth=lw, solid_capstyle="round")


def pts(fn, xa, xb, n=60):
    """색칠 경계에 쓰는 곡선 위의 점 목록."""
    return [(x, fn(x)) for x in xs_between(xa, xb, n)]


def roots(a, b, c):
    """ax² + bx + c = 0의 두 근(작은 것부터)."""
    d = math.sqrt(b * b - 4 * a * c)
    r = sorted(((-b - d) / (2 * a), (-b + d) / (2 * a)))
    return r[0], r[1]


# ── 002 — 포물선과 직선 l, AC : CB = 1 : 4 ──────────────────────────────
# y = x²/4, C(0, 1), 기울기 3/4. A(-1, 1/4), B(4, 4).

def p2():
    f = lambda x: x * x / 4
    A, B, C = (-1.0, 0.25), (4.0, 4.0), (0.0, 1.0)
    fig, ax = g.canvas(6, -1.72, 6.28)
    plane(ax, -4.9, 5.5, -1.4, 5.7, o=(4, -4, "left", "top"))
    curve(ax, f, -4.4, 4.6)
    g.seg(ax, (-2.6, -0.95), (5.2, 4.9), lw=g.STRING)
    for p in (A, B, C):
        g.dot(ax, p)
    g.name(ax, A, "A", dy=5, va="bottom")
    g.name(ax, B, "B", dx=-5, ha="right")
    g.name(ax, C, "C", dx=-4, dy=3, ha="right", va="bottom")
    g.name(ax, (-4.4, f(-4.4)), "$y=\\dfrac{1}{4}x^2$", dx=-4, ha="right")
    g.name(ax, (5.2, 4.9), "$l$", dx=4, ha="left")
    g.save(fig, "p2.svg")


# ── 003 — 두 포물선 사이의 한 변이 1인 정사각형 ─────────────────────────
# A(3, 9)는 y = x² 위, C(4, 8)은 y = x²/2 위. 정사각형은 13pt쯤이라 이름은 네 귀퉁이
# 바깥으로 — 책도 그렇다. B는 왼쪽 아래 조금 떨어져 y = x²가 비켜 간다.

def p3():
    f, h = (lambda x: x * x), (lambda x: x * x / 2)
    A, B, C, D = (3.0, 9.0), (3.0, 8.0), (4.0, 8.0), (4.0, 9.0)
    top = 9.7                                  # 곡선을 정사각형 바로 위에서 잘라 배율을 키운다
    xf, xh = math.sqrt(top), math.sqrt(2 * top)
    fig, ax = g.canvas(7, -1.56, 11.54)
    plane(ax, -4.9, 5.1, -1.1, 10.5, o=(-3, -3, "right", "top"))
    curve(ax, f, -xf, xf)
    curve(ax, h, -xh, xh)
    g.poly(ax, [A, B, C, D])
    # 이름은 귀퉁이에 붙인다. A 왼쪽 위, D 위(조금 왼쪽 — 오른쪽은 y = x²/2가 지난다),
    # B 아래(조금 오른쪽 — 왼쪽은 y = x²가 지난다), C 오른쪽 아래
    g.name(ax, A, "A", dx=-2, dy=3, ha="right", va="bottom")
    g.name(ax, D, "D", dx=-1, dy=3, va="bottom")
    g.name(ax, B, "B", dx=2, dy=-3, va="top")
    g.name(ax, C, "C", dx=3, dy=-3, ha="left", va="top")
    g.name(ax, (-xf, top), "$y=x^2$", dy=4, va="bottom")
    g.name(ax, (math.sqrt(12.0), 6.0), "$y=\\dfrac{1}{2}x^2$", dx=4, ha="left")
    g.save(fig, "p3.svg")


# ── 004 — 두 포물선 위의 직사각형, AB : BC = 1 : 2 ──────────────────────
# A(3/2, 3/4), B(9/2, 3/4), C(9/2, 27/4), D(3/2, 27/4). 넓이 18.

def p4():
    f3, f13 = (lambda x: 3 * x * x), (lambda x: x * x / 3)
    A, B, C, D = (1.5, 0.75), (4.5, 0.75), (4.5, 6.75), (1.5, 6.75)
    fig, ax = g.canvas(7, -1.16, 9.14)
    plane(ax, -5.3, 5.5, -0.8, 8.5, o=(-3, -4, "right", "top"))
    g.shade(ax, [A, B, C, D])
    curve(ax, f3, -1.6, 1.6)
    curve(ax, f13, -4.9, 4.9)
    g.poly(ax, [A, B, C, D])
    g.name(ax, A, "A", dx=-4, dy=4, ha="right")      # 왼쪽 위. 아래는 x축과 끼고 왼쪽 아래는 곡선이 지난다
    g.name(ax, B, "B", dx=4, ha="left")
    g.name(ax, C, "C", dx=4, ha="left")
    g.name(ax, D, "D", dx=-4, ha="right")
    g.name(ax, (1.6, f3(1.6)), "$y=3x^2$", dx=4, ha="left")
    g.name(ax, (4.9, f13(4.9)), "$y=\\dfrac{1}{3}x^2$", dx=4, ha="left")
    g.save(fig, "p4.svg")


# ── 005 — 정사각형 A_n과 y = x²/k ────────────────────────────────────────
# n = 1로 그린다. k = 1.6이면 곡선이 아래 변(x ≈ 1.26)에서 들어와 위 변(x ≈ 1.79)으로 나간다.

def p5():
    k = 1.6
    f = lambda x: x * x / k
    fig, ax = g.canvas(6, -0.68, 3.83)
    plane(ax, -2.7, 3.0, -0.5, 3.5, o=(-3, -4, "right", "top"))
    curve(ax, f, -2.25, 2.25)
    g.rect(ax, (1.0, 1.0), 1.0, 1.0, mark=False)
    g.dashed(ax, (1.0, 0.0), (1.0, 1.0))
    g.dashed(ax, (2.0, 0.0), (2.0, 1.0))
    g.dashed(ax, (0.0, 1.0), (1.0, 1.0))
    g.dashed(ax, (0.0, 2.0), (1.0, 2.0))
    g.name(ax, (1.0, 0.0), "$n$", dy=-4, va="top")
    g.name(ax, (2.0, 0.0), "$2n$", dy=-4, va="top")
    g.name(ax, (0.0, 1.0), "$n$", dx=-4, ha="right")
    g.name(ax, (0.0, 2.0), "$2n$", dx=-4, ha="right")
    g.name(ax, (2.25, f(2.25)), "$y=\\dfrac{1}{k}x^2$", dx=4, ha="left")
    g.save(fig, "p5.svg")


# ── 006 — 평행사변형 ABCD, A·D는 y = 4x² 위, B는 y = ax² 위 ─────────────
# a = -1. A(-1/2, 1), D(1/2, 1), B(-1, -1), C(0, -1).

def p6():
    f4, fa = (lambda x: 4 * x * x), (lambda x: -x * x)
    A, B, C, D = (-0.5, 1.0), (-1.0, -1.0), (0.0, -1.0), (0.5, 1.0)
    fig, ax = g.canvas(6, -2.68, 2.26)
    plane(ax, -1.8, 2.0, -2.4, 1.9, o=(-3, -5, "right", "top"))
    curve(ax, f4, -0.66, 0.66)
    curve(ax, fa, -1.5, 1.5)
    g.poly(ax, [A, B, C, D])
    g.name(ax, A, "A", dx=-5, ha="right")
    g.name(ax, D, "D", dx=5, ha="left")
    g.name(ax, B, "B", dx=-5, dy=2, ha="right")
    g.name(ax, C, "C", dx=5, ha="left")
    g.name(ax, (0.66, f4(0.66)), "$y=4x^2$", dx=4, ha="left")
    g.name(ax, (1.5, fa(1.5)), "$y=ax^2$", dx=4, ha="left")
    g.save(fig, "p6.svg")


# ── 007 — 두 포물선이 좌표축과 만나는 네 점이 정사각형 ──────────────────
# a = b = 1. A(0, 1), B(-1, 0), C(0, -1), D(1, 0).

def p7():
    up, down = (lambda x: x * x - 1), (lambda x: -x * x + 1)
    A, B, C, D = (0.0, 1.0), (-1.0, 0.0), (0.0, -1.0), (1.0, 0.0)
    fig, ax = g.canvas(6, -2.52, 2.68)
    plane(ax, -2.1, 2.4, -2.3, 2.3, o=(3, -3, "left", "top"))
    curve(ax, up, -1.75, 1.75)
    curve(ax, down, -1.75, 1.75)
    g.poly(ax, [A, B, C, D])
    # A·C는 y축 위의 점이라 바로 위·아래에 두면 축이 글자를 지난다(겹침 검사가 잡았다). 왼쪽 위·왼쪽 아래로
    g.name(ax, A, "A", dx=-4, dy=3, ha="right", va="bottom")
    g.name(ax, B, "B", dx=-9, dy=2, ha="right", va="bottom")
    g.name(ax, C, "C", dx=-4, dy=-3, ha="right", va="top")
    g.name(ax, D, "D", dx=9, dy=2, ha="left", va="bottom")
    g.name(ax, (1.75, up(1.75)), "$y=ax^2-b$", dx=4, ha="left")
    g.name(ax, (1.75, down(1.75)), "$y=-ax^2+b$", dx=4, ha="left")
    g.save(fig, "p7.svg")


# ── 008 — 포물선 위의 P에서 수평으로 그어 직선과 만나는 Q ──────────────
# 책처럼 P는 오른쪽 가지에 있고 선분 PQ는 포물선 바깥(오른쪽)으로 나가 직선과 만난다.
# 답(P의 x좌표 -2, 3)과는 무관한 자리다. P 이름은 y축과 P 사이 왼쪽 위.

def p8():
    f, line = (lambda x: x * x + 1), (lambda x: x - 1)
    P = (0.7, f(0.7))
    Q = (P[1] + 1, P[1])
    fig, ax = g.canvas(6, -3.55, 5.02)
    plane(ax, -2.3, 5.1, -3.2, 4.4, o=(-4, -3, "right", "top"))
    curve(ax, f, -1.75, 1.75)
    g.seg(ax, (-1.9, line(-1.9)), (4.6, line(4.6)), lw=g.STRING)
    g.seg(ax, P, Q)
    g.dot(ax, P)
    g.dot(ax, Q)
    g.name(ax, P, "P", dx=-2, dy=5, ha="right", va="bottom")
    g.name(ax, Q, "Q", dx=4, dy=-3, ha="left", va="top")
    g.name(ax, (1.75, f(1.75)), "$y=x^2+1$", dx=4, ha="left")
    g.name(ax, (4.6, line(4.6)), "$y=x-1$", dx=4, ha="left")
    g.save(fig, "p8.svg")


# ── 009 — 직선 y = x + m과 포물선 y = (x - 3)², AC = 3AB ──────────────────
# m = 3. A(-3, 0), B(0, 3), C(6, 9).

def p9():
    f, line = (lambda x: (x - 3) ** 2), (lambda x: x + 3)
    A, B, C = (-3.0, 0.0), (0.0, 3.0), (6.0, 9.0)
    fig, ax = g.canvas(7, -1.96, 11.21)
    plane(ax, -4.4, 7.7, -1.5, 10.4, o=(3, -3, "left", "top"))
    curve(ax, f, -0.1, 6.1)
    g.seg(ax, (-3.9, line(-3.9)), (6.7, line(6.7)), lw=g.STRING)
    g.name(ax, A, "A", dx=3, dy=-3, ha="left", va="top")
    g.name(ax, B, "B", dx=-4, dy=1, ha="right")
    g.name(ax, C, "C", dx=5, dy=-4, ha="left")
    g.name(ax, (6.7, line(6.7)), "$y=x+m$", dx=4, ha="left")
    g.name(ax, (3 + math.sqrt(3), 3.0), "$y=(x-3)^2$", dx=4, ha="left")
    g.save(fig, "p9.svg")


# ── 013 — 두 포물선 사이 S와 y = x² + 2 아래 T ────────────────────────────
# A(-1, 3), B(2, 6). S는 두 곡선 사이, T는 y = x² + 2와 x = -1, x = 2, x축 사이.
# 두 부분이 곡선 하나를 맞대고 있어 같은 농도면 구분이 안 된다(선생님 지적). S는 연마 틴트
# 10%, T는 그 두 배쯤인 22%로 칠해 갈라 보인다.

TINT2 = 0.22


def shade2(ax, pts_):
    ax.add_patch(Polygon(pts_, closed=True, facecolor=g.INK, alpha=TINT2, edgecolor="none"))


def p13():
    f, h = (lambda x: x * x + 2), (lambda x: -x * x + 2 * x + 6)
    A, B = (-1.0, 3.0), (2.0, 6.0)
    fig, ax = g.canvas(7, -2.30, 9.21)
    plane(ax, -3.0, 4.6, -1.9, 8.5, o=(3, -4, "left", "top"))
    g.shade(ax, pts(h, -1, 2) + pts(f, 2, -1))
    shade2(ax, [(-1.0, 0.0)] + pts(f, -1, 2) + [(2.0, 0.0)])
    curve(ax, f, -2.4, 2.4)
    curve(ax, h, -1.9, 3.9)
    g.seg(ax, (-1.0, 0.0), A, lw=g.AUX)
    g.seg(ax, (2.0, 0.0), B, lw=g.AUX)
    g.dashed(ax, A, (0.0, 3.0))
    g.dashed(ax, B, (0.0, 6.0))
    g.name(ax, A, "A", dx=-5, ha="right")
    g.name(ax, B, "B", dx=5, ha="left")
    g.name(ax, (0.0, 3.0), "3", dx=3, ha="left")
    g.name(ax, (0.0, 6.0), "6", dx=3, dy=-3, ha="left", va="top")
    g.name(ax, (-1.0, 0.0), "$-1$", dy=-4, va="top")
    g.name(ax, (2.0, 0.0), "2", dy=-4, va="top")
    g.name(ax, (0.7, 4.6), "$S$")
    g.name(ax, (0.5, 1.2), "$T$")
    g.name(ax, (2.4, f(2.4)), "$y=x^2+2$", dx=4, ha="left")
    g.name(ax, (3.0, 3.0), "$y=-x^2+2x+6$", dx=4, ha="left")
    g.save(fig, "p13.svg")


# ── 016 — 포물선의 세 교점과 평행사변형 ABCD ─────────────────────────────
# A(-4, 0), C(2, 0), B(0, -4), D(-2, 4).

def p16():
    f = lambda x: x * x / 2 + x - 4
    A, B, C, D = (-4.0, 0.0), (0.0, -4.0), (2.0, 0.0), (-2.0, 4.0)
    fig, ax = g.canvas(7, -5.73, 6.56)
    plane(ax, -5.9, 4.6, -5.3, 5.8, o=(-3, -3, "right", "top"))
    g.shade(ax, [A, B, C, D])
    curve(ax, f, -5.4, 3.4)
    g.poly(ax, [A, B, C, D])
    g.name(ax, A, "A", dx=-2, dy=-4, ha="right", va="top")
    g.name(ax, B, "B", dx=5, dy=-3, ha="left")
    g.name(ax, C, "C", dx=3, dy=-3, ha="left", va="top")
    g.name(ax, D, "D", dy=4, va="bottom")
    g.name(ax, (3.4, f(3.4)), "$y=\\dfrac{1}{2}x^2+x-4$", dx=4, ha="left")
    g.save(fig, "p16.svg")


# ── 017 — 꼭짓점 A와 x절편 B, C, 넓이를 이등분하는 직선 l ────────────────
# A(-2, 9), B(-5, 0), C(1, 0), D(-1/2, 9/2). l: y = x + 5.
# D는 두 직선의 교점이라 네 방향 모두 선이 가깝다. 가장 넓은 틈(왼쪽, 167° 방향)에 이름을 둔다.

def p17():
    f, line = (lambda x: -(x + 2) ** 2 + 9), (lambda x: x + 5)
    A, B, C, D = (-2.0, 9.0), (-5.0, 0.0), (1.0, 0.0), (-0.5, 4.5)
    xl, xr = roots(-1, -4, 5 + 3)           # y = -3인 x
    fig, ax = g.canvas(7, -4.13, 11.15)
    plane(ax, -6.4, 2.7, -3.4, 10.2, o=(3, -3, "left", "top"))
    g.shade(ax, [A, B, C])
    curve(ax, f, xl, xr)
    g.seg(ax, (-6.0, line(-6.0)), (2.2, line(2.2)), lw=g.STRING)
    g.poly(ax, [A, B, C])
    g.name(ax, A, "A", dy=4, va="bottom")
    g.name(ax, B, "B", dx=-3, dy=3, ha="right", va="bottom")
    g.name(ax, C, "C", dx=4, dy=3, ha="left", va="bottom")
    g.name(ax, D, "D", dx=-7, dy=2, ha="right")
    g.name(ax, (2.2, line(2.2)), "$l$", dx=4, ha="left")
    g.name(ax, (xr, -3.0), "$y=-x^2-4x+5$", dx=4, ha="left")
    g.save(fig, "p17.svg")


# ── 018 — 포물선과 직선 y = -2x + 8이 B, C에서 만난다 ─────────────────────
# b = 2, c = 8. A(-2, 0), B(4, 0), C(0, 8).

def p18():
    f, line = (lambda x: -(x - 1) ** 2 + 9), (lambda x: -2 * x + 8)
    A, B, C = (-2.0, 0.0), (4.0, 0.0), (0.0, 8.0)
    xl, xr = roots(-1, 2, 8 + 2.5)          # y = -2.5인 x
    fig, ax = g.canvas(7, -3.51, 11.10)
    plane(ax, -3.1, 5.7, -3.0, 10.2, o=(3, -3, "left", "top"))
    curve(ax, f, xl, xr)
    g.seg(ax, (-0.7, line(-0.7)), (5.0, line(5.0)), lw=g.STRING)
    g.name(ax, A, "A", dx=-4, dy=3, ha="right", va="bottom")
    g.name(ax, B, "B", dx=4, dy=3, ha="left", va="bottom")
    g.name(ax, C, "C", dx=-5, ha="right")
    g.name(ax, (1.5, 9.0), "$y=-x^2+bx+c$", dx=4, dy=3, ha="left", va="bottom")
    g.name(ax, (5.0, line(5.0)), "$y=-2x+8$", dx=4, ha="left")
    g.save(fig, "p18.svg")


# ── 019 — (1, 0)을 지나는 세 포물선 ──────────────────────────────────────
# f = (x-1)(x-2), g = (x-1)(x-3), h = (x-1)(x-4). 끝을 층층이 잘라(2.2·3.2·4.2) 이름을
# 끝의 왼쪽 위에 둔다 — 책도 셋을 층층이 그렸다. x축 숫자 1은 세 곡선이 오른쪽 아래로 내려가니
# 조금 왼쳑에.

def p19():
    fs = [(lambda x: (x - 1) * (x - 2), 2.2, "$y=f(x)$"),
          (lambda x: (x - 1) * (x - 3), 3.2, "$y=g(x)$"),
          (lambda x: (x - 1) * (x - 4), 4.2, "$y=h(x)$")]
    fig, ax = g.canvas(7, -3.09, 5.29)
    plane(ax, -0.7, 5.9, -2.8, 4.7, o=(-3, -4, "right", "top"))
    for i, (fn, top, text) in enumerate(fs):
        r2 = 2 + i                                 # 다른 근
        xl, xr = roots(1, -(1 + r2), r2 - top)     # y = top인 x
        curve(ax, fn, xl, xr)
        g.name(ax, (xr, top), text, dx=-3, dy=3, ha="right", va="bottom")
    g.name(ax, (0.85, 0.0), "1", dy=-4, va="top")
    for n in (2, 3, 4):
        g.name(ax, (float(n), 0.0), str(n), dy=-4, va="top")
    g.save(fig, "p19.svg")


# ── 020 — 폭이 같은 두 포물선과 수평선 위의 네 점 ─────────────────────────
# f = x², g = -x² + 4x, A(2, 4). 수평선 y = 1: P(-1), Q(2-√3), R(1), S(2+√3).
# Q는 y축과 g 사이에 끼어 이름을 위쪽 틈(y축 오른쪽, g 왼왱)에 둔다 — 책도 그렇다.

def p20():
    f, gg = (lambda x: x * x), (lambda x: -x * x + 4 * x)
    r3 = math.sqrt(3)
    A = (2.0, 4.0)
    P, Q, R, S = (-1.0, 1.0), (2 - r3, 1.0), (1.0, 1.0), (2 + r3, 1.0)
    xl, xr = roots(-1, 4, 1.6)              # g = -1.6인 x. 가지를 짧게 잘라 배율을 키운다 — Q 이름 자리
    fig, ax = g.canvas(7, -1.97, 6.00)
    plane(ax, -2.5, 5.4, -1.7, 5.5, o=(-3, -3, "right", "top"))
    curve(ax, f, -2.0, 2.3)
    curve(ax, gg, xl, xr)
    g.seg(ax, (-2.4, 1.0), (5.0, 1.0))
    g.name(ax, A, "A", dx=4, dy=3, ha="left", va="bottom")
    g.name(ax, P, "P", dx=-2, dy=-4, ha="right", va="top")
    g.name(ax, (0.04, 2.1), "Q", ha="left")
    g.name(ax, R, "R", dx=3, dy=-3, ha="left", va="top")
    g.name(ax, S, "S", dx=-3, dy=-3, ha="right", va="top")
    g.name(ax, (-2.1, f(-2.1)), "$y=f(x)$", dx=-4, ha="right")
    g.name(ax, (2 + math.sqrt(0.8), 3.2), "$y=g(x)$", dx=4, ha="left")
    g.save(fig, "p20.svg")


if __name__ == "__main__":
    print("figures/")
    p2()
    p3()
    p4()
    p5()
    p6()
    p7()
    p8()
    p9()
    p13()
    p16()
    p17()
    p18()
    p19()
    p20()
