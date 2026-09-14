# -*- coding: utf-8 -*-
"""시험대비 견본 — 문제 그림 한 장. 새 단원의 figures.py는 이 파일을 그대로 복사해 쓴다.

build.py가 grind_figure의 import 경로를 잡아 주므로 이 파일은 build.py로 실행한다.
그림은 단 글 너비(229pt) 안에 들어야 한다. y 범위가 배율을 정하니 넓은 그림은 y 범위를
넉넉히 잡는다. save()가 위아래 여백을 재서 y 범위를 얼마로 잡을지 일러 준다.
"""
from __future__ import annotations

import math

import grind_figure as g

g.setup(__file__)


def p2():
    """∠B = 90°, ∠A = 30°, AC = 10인 직각삼각형. 길이는 연마와 같이 점선 곡선(g.dim)으로 단다."""
    A = (0.0, 0.0)
    B = (10 * math.cos(math.radians(30)), 0.0)
    C = (B[0], 5.0)
    f, ax = g.canvas(5, -1.19, 6.19)
    g.poly(ax, [A, B, C])
    g.right_angle(ax, B, -1, 1)
    g.angle(ax, A, B, C, "$30^{\\circ}$", r=16)
    g.name(ax, A, "A", dx=-4, dy=-4, ha="right", va="top")
    g.name(ax, B, "B", dx=4, dy=-4, ha="left", va="top")
    g.name(ax, C, "C", dx=4, dy=4, ha="left", va="bottom")
    g.dim(ax, A, C, "10", side=1, trim=4)
    g.save(f, "p2.svg")


if __name__ == "__main__":
    print("figures/")
    p2()
