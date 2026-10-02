# -*- coding: utf-8 -*-
"""선행 004(삼각비 030)의 그림. 삼각비 figures.py의 p30()과 거기서 쓰는 도우미를 그대로 옮겨 원본
p30.svg와 같은 그림을 그린다. 그림을 고치려면 원본과 함께 고친다.

한 변이 10인 정사각형 ABCD와 점 A를 중심으로 34° 돌린 정사각형 AB'C'D'을 그린다. E는 두 변 B'C', CD의
교점이고 겹쳐지는 부분 AB'ED만 색칠한다. 두 정사각형의 귀퉁이에 모두 직각 표시를 한다.
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


def meet(P, d, Q, e):
    """직선 P + td와 Q + se의 교점."""
    det = d[0] * e[1] - d[1] * e[0]
    rx, ry = Q[0] - P[0], Q[1] - P[1]
    t = (rx * e[1] - ry * e[0]) / det
    return P[0] + t * d[0], P[1] + t * d[1]


def cross(P, Q, R, S):
    """선분 PQ와 RS가 놓인 두 직선의 교점."""
    return meet(P, (Q[0] - P[0], Q[1] - P[1]), R, (S[0] - R[0], S[1] - R[1]))


def draw():
    """34° 돌린 정사각형과 겹치는 부분."""
    s = 10.0
    A, B, C, D = (0.0, 0.0), (s, 0.0), (s, s), (0.0, s)
    B2 = g.polar(A, s, 34)
    D2 = g.polar(A, s, 124)
    C2 = (B2[0] + D2[0], B2[1] + D2[1])
    E = cross(B2, C2, D, C)
    fig, ax = g.canvas(7, -2.32, 16.31)
    g.shade(ax, [A, B2, E, D])
    g.rect(ax, A, s, s)
    g.poly(ax, [A, B2, C2, D2])
    for p, (u, v) in ((B2, (unit(B2, A), unit(B2, C2))), (C2, (unit(C2, B2), unit(C2, D2))),
                      (D2, (unit(D2, C2), unit(D2, A)))):
        g.corner_mark(ax, p, u, v)
    g.angle(ax, A, B, B2, "$34^{\\circ}$", r=16)
    g.dim(ax, A, B, "10", side=-1)
    g.name(ax, A, "A", dx=-2, dy=-5, va="top")
    g.name(ax, B, "B", dx=4, dy=-3, ha="left", va="top")
    g.name(ax, C, "C", dx=5, ha="left")
    g.name(ax, D, "D", dx=-4, dy=-3, ha="right", va="top")    # 위쪽은 변 D'C'이 지나 그 위의 점처럼 보인다
    g.name(ax, B2, "$\\mathrm{B}'$", dx=2, dy=-5, va="top")   # 오른쪽은 변 BC가 지난다
    g.name(ax, C2, "$\\mathrm{C}'$", dy=5, va="bottom")
    g.name(ax, D2, "$\\mathrm{D}'$", dx=-5, ha="right")
    g.name(ax, E, "E", dx=3, dy=4, ha="left", va="bottom")   # 지문이 E를 부른다. 책처럼 교점 위 오른쪽, 두 정사각형 밖
    g.save(fig)


if __name__ == "__main__":
    draw()
