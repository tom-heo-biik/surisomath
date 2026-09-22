# -*- coding: utf-8 -*-
"""수행평가 · 수지중학교 · 중1 · 2026. 9. 17. — 문제 그림 한 장(001 좌표평면).

도우미는 surisomath-grind 스킬의 grind_figure를 쓴다. build.py가 import 경로를 잡아
주므로 이 파일은 build.py로 실행한다.

    python .claude/skills/surisomath-assess/templates/build.py build/수행평가/20262학기/수지중학교/중1/2026.09.17/problems.yaml

좌표평면은 가로세로 배율이 같아야 하므로 y 범위로 배율만 정한다(연마 2026.09.12 002와
같은 방식). 축·화살촉·좌표 글자 규격도 그 그림을 따른다.
"""
from __future__ import annotations

from matplotlib.patches import Polygon

import grind_figure as g

g.setup(__file__)

HEAD = 6.0            # 화살촉 길이(pt)


def arrow(ax, p, q, lw=g.AUX):
    """p에서 q까지의 축. q 끝에 채운 화살촉(길이 HEAD pt, 밑변 HEAD×0.7pt)."""
    L = g.pt(ax, HEAD)
    dx, dy = q[0] - p[0], q[1] - p[1]
    n = (dx * dx + dy * dy) ** 0.5
    ux, uy = dx / n, dy / n
    base = (q[0] - ux * L, q[1] - uy * L)
    g.seg(ax, p, base, lw=lw)
    w = L * 0.35
    ax.add_patch(Polygon([q, (base[0] - uy * w, base[1] + ux * w),
                          (base[0] + uy * w, base[1] - ux * w)],
                         closed=True, facecolor=g.INK, edgecolor="none"))


# ── 001 — 정비례·반비례 그래프의 교점 ────────────────────────────────────
# P(-4, 1)에서 만나므로 a = -1/4, b = -4. 직선은 제2·4사분면을 지나 오른쪽 아래로 내려가고
# 쌍곡선도 제2·4사분면에 있다. 직선 위의 점 (8, -2)도 표시한다(md의 그림 설명).
#   축 반길이: x축 9.5, y축 6.5. 가지 끝이 x축에서 4/9.5 = 0.42, y축에서 4/6.5 = 0.62 떨어져
#   축에 바짝 붙는다. x축이 긴 까닭은 점 (8, -2)가 축 안에 들어야 해서다.
#   좌표 글은 점의 반대쪽 축 옆에 둔다(교과서 관례): P는 제2사분면이라 -4는 x축 아래, 1은
#   y축 오른쪽. (8, -2)는 제4사분면이라 8은 x축 위, -2는 y축 왼쪽.
#   O는 제3사분면(-2 글자 위쪽 빈 자리), y 이름은 제1사분면(비어 있다) 쪽 축 끝 옆.

def p1():
    a, b = -0.25, -4.0
    P, Q = (-4.0, 1.0), (8.0, -2.0)
    RX, RY = 9.5, 6.5
    f, ax = g.canvas(8, -7.9, 8.2)
    arrow(ax, (-RX - 0.6, 0), (RX + 0.8, 0))
    arrow(ax, (0, -RY - 0.6), (0, RY + 0.8))
    g.label(ax, RX + 1.1, 0, "$x$", ha="left")
    g.label(ax, 0.45, RY + 0.55, "$y$", ha="left")
    g.label(ax, -0.3, -0.3, "O", ha="right", va="top")

    # y = ax. |x| ≤ RX
    g.seg(ax, (-RX, a * -RX), (RX, a * RX), lw=g.STRING)
    # y = b/x. 두 가지. x는 |b|/RY(가지 끝이 y축 옆)부터 RX(x축 옆)까지, 축 옆에서 촘촘히
    x0, x1 = -b / RY, RX
    xs = [x0 + (x1 - x0) * (i / 160) ** 1.6 for i in range(161)]
    for sgn in (1, -1):
        ax.plot([-sgn * x for x in xs], [sgn * -b / x for x in xs], color=g.INK,
                linewidth=g.STRING, solid_capstyle="round")

    # 교점 P와 두 축까지의 점선, 좌표
    g.dashed(ax, P, (P[0], 0))
    g.dashed(ax, P, (0, P[1]))
    g.dot(ax, P)
    g.label(ax, P[0] - 0.3, P[1] + 0.45, "P", va="baseline")
    g.label(ax, P[0], -0.35, "$-4$", va="top")
    g.label(ax, 0.35, P[1], "1", ha="left")

    # 직선 위의 점 (8, -2)와 두 축까지의 점선, 좌표
    g.dashed(ax, Q, (Q[0], 0))
    g.dashed(ax, Q, (0, Q[1]))
    g.dot(ax, Q)
    g.label(ax, Q[0], 0.35, "8", va="bottom")
    g.label(ax, -0.35, Q[1], "$-2$", ha="right")

    # 그래프 이름. 직선은 왼쪽 위 끝의 위, 곡선은 제2사분면 가지 위 끝의 왼쪽
    g.label(ax, -RX + 0.5, a * -RX + 0.45, "$y=ax$", va="bottom")
    g.label(ax, -1.2, RY - 0.5, r"$y=\dfrac{b}{x}$", ha="right")

    g.save(f, "p1.svg")


if __name__ == "__main__":
    print("figures/")
    p1()
