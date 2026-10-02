# -*- coding: utf-8 -*-
"""선행 005(원과 직선 001)의 그림. 원과 직선 figures.py의 p1()과 거기서 쓰는 도우미를 그대로 옮겨
원본 p1.svg와 같은 그림을 그린다. 그림을 고치려면 원본과 함께 고친다.

변 CD를 맞댄 두 접선사각형 ABCD, CEFD를 그린다. B(0, 0), C(6, 0), E(18, 0)이고 위 직선은 기울기 17°다.
A는 AB + CD = AD + BC = 14, CD + EF = CE + DF = 17을 만족하도록 뉴턴법으로 푼 값이다(문제는 A의 자리를
정하지 않는다). 길이는 점선 곡선(g.dim)으로 꼭짓점에서 꼭짓점까지 잇는다.
"""
from __future__ import annotations

import math

import grind_figure as g

g.setup(__file__)


def unit(p, q):
    """p에서 q로 향하는 단위벡터."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    n = math.hypot(dx, dy)
    return dx / n, dy / n


def bisector(P, Q, R):
    """꼭짓점 Q에서 안쪽 각 PQR의 이등분선 방향(단위벡터)."""
    u, v = unit(Q, P), unit(Q, R)
    d = (u[0] + v[0], u[1] + v[1])
    n = math.hypot(*d)
    return d[0] / n, d[1] / n


def meet(P, d, Q, e):
    """직선 P + td와 Q + se의 교점."""
    det = d[0] * e[1] - d[1] * e[0]
    rx, ry = Q[0] - P[0], Q[1] - P[1]
    t = (rx * e[1] - ry * e[0]) / det
    return P[0] + t * d[0], P[1] + t * d[1]


def line_dist(P, A, B):
    """점 P에서 직선 AB까지의 거리."""
    dx, dy = B[0] - A[0], B[1] - A[1]
    return abs(dx * (P[1] - A[1]) - dy * (P[0] - A[0])) / math.hypot(dx, dy)


def incircle_quad(A, B, C, D):
    """접선사각형 ABCD의 내접원. 이웃한 두 꼭짓점 A, B의 각의 이등분선이 만나는 점이 중심이다."""
    I = meet(A, bisector(D, A, B), B, bisector(A, B, C))
    return I, line_dist(I, A, B)


def center(ax, p, text, dx=4.0, dy=0.0, ha="left", va="center"):
    """원의 중심. 점과 이름."""
    g.dot(ax, p)
    g.name(ax, p, text, dx=dx, dy=dy, ha=ha, va=va)


def draw():
    """변 CD를 맞댄 두 접선사각형."""
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
    g.save(fig)


if __name__ == "__main__":
    draw()
