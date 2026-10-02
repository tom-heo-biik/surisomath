# -*- coding: utf-8 -*-
"""선행 002(이차함수 020)의 그림. 이차함수 figures.py의 p20()과 거기서 쓰는 도우미를 그대로 옮겨
원본 p20.svg와 같은 그림을 그린다. 그림을 고치려면 원본과 함께 고친다.

f = x², g = -x² + 4x, A(2, 4)로 그린다. 직선 y = k(k = 1)와 네 교점 x₁ = -1, x₂ = 2 - √3, x₃ = 1,
x₄ = 2 + √3는 글에만 있고 그림에는 없다(2026-09-26 선생님 지시 "그림에서 y = k 자체를 없애 줘").
좌표평면은 가로세로 배율이 같고 y 범위가 배율을 정한다. 축은 0.4pt에 채운 화살촉, 그래프는 1pt다.
"""
from __future__ import annotations

import math

from matplotlib.patches import Polygon

import grind_figure as g

g.setup(__file__)

HEAD = 6.0            # 화살촉 길이(pt)


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


def roots(a, b, c):
    """ax² + bx + c = 0의 두 근(작은 것부터)."""
    d = math.sqrt(b * b - 4 * a * c)
    r = sorted(((-b - d) / (2 * a), (-b + d) / (2 * a)))
    return r[0], r[1]


def draw():
    """원점과 A에서 만나는 두 포물선."""
    f, gg = (lambda x: x * x), (lambda x: -x * x + 4 * x)
    A = (2.0, 4.0)
    xl, xr = roots(-1, 4, 1.6)              # g = -1.6인 x. 가지를 짧게 잘라 배율을 키운다
    fig, ax = g.canvas(7, -1.97, 6.00)
    plane(ax, -2.5, 5.4, -1.7, 5.5, o=(-3, -3, "right", "top"))
    curve(ax, f, -2.0, 2.3)
    curve(ax, gg, xl, xr)
    g.name(ax, A, "A", dx=4, dy=3, ha="left", va="bottom")
    g.name(ax, (-2.1, f(-2.1)), "$y=f(x)$", dx=-4, ha="right")
    g.name(ax, (2 + math.sqrt(0.8), 3.2), "$y=g(x)$", dx=4, ha="left")
    g.save(fig)


if __name__ == "__main__":
    draw()
