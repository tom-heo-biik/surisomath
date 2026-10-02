# -*- coding: utf-8 -*-
"""선행 006(원과 직선 014)의 그림. 원과 직선 figures.py의 p14()와 거기서 쓰는 도우미를 그대로 옮겨
원본 p14.svg와 같은 그림을 그린다. 그림을 고치려면 원본과 함께 고친다.

PQ = 12, QR = 16, PR = 20이고 원 C의 중심 O(4, 4), 원 C'의 중심 O'(12, 8)이다. E는 P에서, F는 R에서
8만큼 떨어진 대각선 위의 점이라 EF = 4이고 사각형 EOFO'의 넓이는 16이다. 이름은 P, Q, R, S이고(책은
A, B, C, D) 두 원 C, C'과 꼭짓점 C가 겹치지 않게 했다(2026-09-29 선생님). 코드의 변수 A, B, C, D는 책의
이름 그대로다.
"""
from __future__ import annotations

import grind_figure as g

g.setup(__file__)


def lerp(p, q, t):
    return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)


def center(ax, p, text, dx=4.0, dy=0.0, ha="left", va="center"):
    """원의 중심. 점과 이름."""
    g.dot(ax, p)
    g.name(ax, p, text, dx=dx, dy=dy, ha=ha, va=va)


def draw():
    """두 직각삼각형의 내접원과 평행사변형 EOFO'."""
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
    g.dim(ax, O, E, "4", side=1)       # 반지름 OE, O'F는 변으로 그어져 있다. 길이는 책처럼 점선 호
    g.dim(ax, O2, F, "4", side=1)
    center(ax, O, "O", dx=-5, ha="right")
    center(ax, O2, "$\\mathrm{O}'$", dx=5, ha="left")
    g.name(ax, A, "P", dx=-4, dy=3, ha="right", va="bottom")
    g.name(ax, B, "Q", dx=-4, dy=-3, ha="right", va="top")
    g.name(ax, C, "R", dx=4, dy=-3, ha="left", va="top")
    g.name(ax, D, "S", dx=4, dy=3, ha="left", va="bottom")
    # E, F는 대각선 위의 점이라 대각선 방향(왼쪽 위, 오른쪽 아래)에 두면 선이 글자를 지난다.
    # 대각선의 법선 쪽에 둔다. E는 오른쪽 위(원 C 밖, 선분 O'E 위), F는 왼쪽 아래(원 C' 밖, 선분 OF 아래)
    g.name(ax, E, "E", dx=3, dy=5, ha="left", va="bottom")
    g.name(ax, F, "F", dx=-3, dy=-5, ha="right", va="top")
    # 원의 이름. C는 삼각형 PQR 안에서 원 C의 오른쪽 아래, C'은 삼각형 PSR 안에서 원 C'의 왼쪽 위
    g.name(ax, g.polar(O, 4.0, -30), "$\\mathrm{C}$", dx=3, dy=-3, ha="left", va="top")
    g.name(ax, g.polar(O2, 4.0, 150), "$\\mathrm{C}'$", dx=-3, dy=3, ha="right", va="bottom")
    g.save(fig)


if __name__ == "__main__":
    draw()
