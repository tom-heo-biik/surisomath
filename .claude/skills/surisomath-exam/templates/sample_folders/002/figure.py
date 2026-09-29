# -*- coding: utf-8 -*-
"""시험대비 새 꼴 견본 002의 그림. 새 꼴 문제의 figure.py는 이 파일을 복사해 쓴다.

g.setup(__file__)이 문제 폴더를 알아보고 단원의 figures/ 에 그린다. g.save(f)에 이름을
주지 않으면 p002.svg(폴더 번호)로 저장하고 problem.yaml의 figure도 그 이름이다. 한 문제에 그림이
둘이면 g.save(f, "p002a.svg")처럼 번호로 시작하는 이름을 준다. 여러 문제가 같이 쓰는 도우미는
단원 폴더의 figlib.py에 두고 import figlib로 부른다.

build.py가 figrun.py로 이 파일을 실행하고 grind_figure의 import 경로를 잡아 준다.
그림은 단 글 너비(229pt) 안에 들어야 한다. y 범위가 배율을 정하니 넓은 그림은 y 범위를
넉넉히 잡는다. save()가 위아래 여백을 재서 y 범위를 얼마로 잡을지 일러 준다.
"""
from __future__ import annotations

import math

import grind_figure as g

g.setup(__file__)


def draw():
    """∠B = 90°, ∠A = 30°, AC = 10인 직각삼각형. 길이는 연마와 같이 점선 곡선(g.dim)으로
    꼭짓점에서 꼭짓점까지 단다(trim 없음)."""
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
    g.dim(ax, A, C, "10", side=1)
    g.save(f)


if __name__ == "__main__":
    draw()
