# -*- coding: utf-8 -*-
"""연마(硏磨) 2026. 9. 12. — 문제 그림 두 장.

도우미는 surisomath-grind 스킬의 grind_figure를 쓴다. build.py가 import 경로를 잡아
주므로 이 파일은 build.py로 실행한다.

    python .claude/skills/surisomath-grind/templates/build.py build/연마/2026.09.12/problems.yaml

도형 그림과 달리 통계 그래프·좌표평면은 문제의 단위가 종이 위의 크기와 무관하다.
001은 캔버스를 1단위 = 1pt로 잡아 pt로 바로 배치하고, 002는 1단위 = 10pt쯤이
되게 y 범위를 잡았다(좌표평면은 가로세로 배율이 같아야 한다).
"""
from __future__ import annotations

from matplotlib.patches import Polygon

import grind_figure as g

g.setup(__file__)

GRAY = "#636363"      # neutral-500. 격자만 이 색이다(a4 그래프 규격)
HEAD = 6.0            # 화살촉 길이(pt)
TICK = 3.0            # 눈금 길이(pt)


# ── 공통 ────────────────────────────────────────────────────────────────

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


def tick_x(ax, x, y, s):
    """x축 눈금(아래로)과 그 아래 숫자."""
    t = g.pt(ax, TICK)
    g.seg(ax, (x, y), (x, y - t), lw=g.AUX)
    g.label(ax, x, y - t - g.pt(ax, 3), s, va="top")


# ── 001 — 도수분포다각형과 상자 그림 ─────────────────────────────────────
# 중1 교과서·문제집 그림의 관례를 따른다.
#   다각형: 모눈 위에 그린다. 계급 한 칸 = 도수 한 칸인 격자(가로 18pt·세로 16pt). 원점은 0이고
#           y축 바로 오른쪽 첫 칸이 첫 계급 앞의 빈 계급(40~50)이라 다각형이 그 칸
#           한가운데(45)에서 x축을 딛고 시작해 마지막 계급 뒤 빈 칸 한가운데(105)에서
#           끝난다. 계급 경계는 격자선 위에 있고 첫 계급 경계부터 숫자를 적는다.
#   상자 그림: 눈금이 있는 수직선 위에 상자와 수염. 다섯 수는 상자 위에 적는다.
#   둘을 좌우로 놓는다. 상자 그림은 다각형보다 낮으니 세로 가운데에 맞춘다.

CLASSES = [50, 60, 70, 80, 90, 100]      # 계급 경계(점)
FREQ = [2, 4, 6, 6, 2]                   # 도수(명). 합 20
FIVE = (52, 66, 75, 84, 96)              # 최솟값·Q1·중앙값·Q3·최댓값

CW, RH = 18.0, 16.0                      # 모눈 한 칸의 가로·세로(pt). 가로는 계급 하나, 세로는 도수 1명.
                                         # 가로 15pt면 50~100 숫자가 붙고, 세로 18pt면 그림이 너무 길다
AX = 20.0                                # 점수 축 높이(pt). 아래 눈금 글자 자리
NX, NY = 7, 7                            # 모눈 칸 수(가로·세로)
BX0, BW = 215.0, 30.0                    # 상자 그림: 50점의 x(pt), 10점의 너비(pt). 다각형 칸(18pt)보다 넓게 — 좁으면 상자가 짧아 보인다
NL = AX + 47.0                           # 상자 그림의 수직선 높이. 다각형 그림(글자 포함)의 세로 한가운데에 맞춘 값


def px(score):
    """다각형의 x. y축(x=0)이 40점 자리다 — 첫 칸이 빈 계급 40~50."""
    return (score - 40) / 10 * CW


def bx(score):
    """상자 그림의 x."""
    return BX0 + (score - 50) / 10 * BW


def p1():
    f, ax = g.canvas(7, 0, 154)          # 1단위 = 1pt

    # 모눈. 회색 실선 0.4pt. 축은 검정으로 그 위에 긋는다
    for i in range(NX + 1):
        ax.plot([i * CW] * 2, [AX, AX + NY * RH], color=GRAY, linewidth=g.AUX, zorder=0)
    for j in range(NY + 1):
        ax.plot([0, NX * CW], [AX + j * RH] * 2, color=GRAY, linewidth=g.AUX, zorder=0)
    arrow(ax, (0, AX), (NX * CW + 12, AX))
    arrow(ax, (0, AX), (0, AX + NY * RH + 12))
    g.label(ax, -3, AX - 3, "0", ha="right", va="top")
    g.label(ax, NX * CW + 16, AX, "(점)", ha="left")
    g.label(ax, -4, AX + NY * RH + 12, "(명)", ha="right")
    for n in (2, 4, 6):
        g.label(ax, -4, AX + n * RH, str(n), ha="right")
    for c in CLASSES:
        g.label(ax, px(c), AX - 4, str(c), va="top")
    mids = [45] + [c + 5 for c in CLASSES[:-1]] + [105]
    ys = [0] + FREQ + [0]
    ax.plot([px(m) for m in mids], [AX + y * RH for y in ys], color=g.INK,
            linewidth=g.STRING, solid_joinstyle="round", solid_capstyle="round")
    for m, y in zip(mids, ys):
        g.dot(ax, (px(m), AX + y * RH))

    # 상자 그림 — 수직선 y=NL. 상자는 그 위 10~26pt, 다섯 값은 상자 위에 적는다
    B0, B1 = NL + 10, NL + 26
    arrow(ax, (bx(45), NL), (bx(105), NL))          # 100 뒤 꼬리는 짧게. 길면 상자가 왼쪽에 몰려 보인다
    g.label(ax, bx(105) + 4, NL, "(점)", ha="left")
    for c in CLASSES:
        tick_x(ax, bx(c), NL, str(c))
    lo, q1, med, q3, hi = FIVE
    mid = (B0 + B1) / 2
    g.rect(ax, (bx(q1), B0), bx(q3) - bx(q1), B1 - B0, mark=False)
    g.seg(ax, (bx(med), B0), (bx(med), B1))
    g.seg(ax, (bx(lo), mid), (bx(q1), mid))
    g.seg(ax, (bx(q3), mid), (bx(hi), mid))
    for v in (lo, hi):
        g.seg(ax, (bx(v), mid - 4), (bx(v), mid + 4))
    for v in FIVE:
        g.label(ax, bx(v), B1 + 4, str(v), va="bottom")

    g.save(f, "p1.svg")


# ── 002 — 정비례·반비례 그래프의 교점 ────────────────────────────────────

def p2():
    a, b, P = 2.0, 8.0, (2.0, 4.0)
    R = 7.0                              # 축 반길이(좌표 단위). 쌍곡선 가지 끝이 축에 바짝(b/R² ≈ 0.16) 붙어야
                                         # 납작한 호로 보이지 않는다. R=5이면 끝이 축에서 1.6이나 떨어진다
    f, ax = g.canvas(8, -8.13, 9.54)
    arrow(ax, (-R - 0.6, 0), (R + 0.8, 0))
    arrow(ax, (0, -R - 0.6), (0, R + 0.8))
    g.label(ax, R + 1.1, 0, "$x$", ha="left")
    g.label(ax, 0, R + 1.1, "$y$", va="bottom")
    g.label(ax, 0.3, -0.3, "O", ha="left", va="top")      # 직선이 제3사분면으로 내려가니 오른쪽 아래

    # y = ax. |y| ≤ R 안에서 그린다
    t = R / a
    g.seg(ax, (-t, -R), (t, R), lw=g.STRING)
    # y = b/x. 두 가지
    xs = [b / R + (R - b / R) * i / 80 for i in range(81)]
    for sgn in (1, -1):
        ax.plot([sgn * x for x in xs], [sgn * b / x for x in xs], color=g.INK,
                linewidth=g.STRING, solid_capstyle="round")

    # 교점 P와 두 축까지의 점선, 좌표
    g.dashed(ax, P, (P[0], 0))
    g.dashed(ax, P, (0, P[1]))
    g.dot(ax, P)
    # P 이름: 직선(위로)과 곡선(오른쪽 아래로) 사이 넓은 쪽, 곧 점의 바로 오른쪽.
    # va=center는 글꼴 상자 기준이라 글자가 위로 뜬다. 베이스라인으로 앉힌다
    g.label(ax, P[0] + 0.45, P[1] - 0.28, "P", ha="left", va="baseline")
    g.label(ax, P[0], -0.35, "2", va="top")
    g.label(ax, -0.35, P[1], "4", ha="right")

    # 그래프 이름. 직선은 위 끝 오른쪽, 곡선은 제1사분면 가지 끝 위
    g.label(ax, t + 0.3, R - 0.2, "$y=ax$", ha="left")
    g.label(ax, 4.3, 2.4, r"$y=\dfrac{b}{x}$", ha="left", va="bottom")

    g.save(f, "p2.svg")


if __name__ == "__main__":
    print("figures/")
    p1()
    p2()
