# -*- coding: utf-8 -*-
"""선행 003(삼각비 017)의 그림. 삼각비 figures.py의 p17()을 그대로 옮겨 원본 p17.svg와 같은 그림을
그린다. 그림을 고치려면 원본과 함께 고친다.

∠AOB = 90°, OA = OB = 4인 부채꼴 OAB와 ∠POA = 60°(∠POB = 30°)인 현 AP, 세 선분 OA, OB, AP에 접하는
원 C(반지름 2√3 - 2)를 그린다. 선생님 문장(2026-09-27)이 4를 "…인" 절에 두어 4는 그림에(OA 아래 바깥)
달고 원 이름 C는 원 안에 둔다.
"""
from __future__ import annotations

import math

import grind_figure as g

g.setup(__file__)

R3 = math.sqrt(3)


def draw():
    """부채꼴 OAB와 선분 AP에 접하는 원."""
    O, A, B = (0.0, 0.0), (4.0, 0.0), (0.0, 4.0)
    P = g.polar(O, 4.0, 60)
    r = 2 * R3 - 2
    fig, ax = g.canvas(6, -0.81, 4.65)
    g.seg(ax, O, A)
    g.seg(ax, O, B)
    g.arc(ax, O, 4.0, 0, 90)
    g.seg(ax, A, P)
    g.circle(ax, (r, r), r)
    g.right_angle(ax, O, 1, 1)
    g.dot(ax, P)
    g.dim(ax, O, A, "4", side=-1)
    g.name(ax, (r, r), "$\\mathrm{C}$")
    g.name(ax, O, "O", dx=-4, dy=-3, ha="right", va="top")
    g.name(ax, A, "A", dx=4, dy=-3, ha="left", va="top")
    g.name(ax, B, "B", dx=-4, dy=2, ha="right", va="bottom")
    g.name(ax, P, "P", dx=3, dy=4, ha="left", va="bottom")
    g.save(fig)


if __name__ == "__main__":
    draw()
