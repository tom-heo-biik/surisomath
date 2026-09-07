# -*- coding: utf-8 -*-
"""연마(硏磨) 견본 — 문제 그림 두 장. 새 단원의 figures.py는 이 파일을 그대로 복사해 쓴다.

build.py가 grind_figure의 import 경로를 잡아 주므로 이 파일은 build.py로 실행한다.
"""
from __future__ import annotations

import grind_figure as g

g.setup(__file__)


def circle():
    """반지름 5cm인 원. 중심에서 오른쪽 끝까지 반지름을 긋고 점선 곡선으로 길이를 단다."""
    O = (0, 0)
    f, ax = g.canvas(5, -6.5, 6.5)
    g.circle(ax, O, 5)
    g.dot(ax, O)
    g.seg(ax, O, (5, 0), lw=g.AUX)
    g.dim(ax, O, (5, 0), "5cm", gap=1.2)
    g.save(f, "circle.svg")


def square():
    """한 변 10cm인 정사각형 왼쪽 아래 귀퉁이의 사분원을 색칠한다.
    변의 길이는 변 바깥에 점선 곡선으로 단다. 세로 곡선은 글이 가로로 놓이므로
    gap 을 글 너비의 절반보다 크게 준다."""
    s, r = 10.0, 5.0
    f, ax = g.canvas(6, -3.6, 11.5)
    g.wedge(ax, (0, 0), r, 0, 90)
    g.arc(ax, (0, 0), r, 0, 90)
    g.rect(ax, (0, 0), s, s)
    g.dim(ax, (s, 0), (s, s), "10cm", side=-1, gap=2.8)    # 오른쪽 변
    g.dim(ax, (0, 0), (s, 0), "10cm", side=-1, gap=1.6)    # 아래 변
    g.dim(ax, (0, 0), (r, 0), "5cm", gap=0.9)               # 사분원 반지름
    g.save(f, "square.svg")


if __name__ == "__main__":
    print("figures/")
    circle()
    square()
