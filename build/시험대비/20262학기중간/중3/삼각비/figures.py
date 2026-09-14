# -*- coding: utf-8 -*-
"""시험대비 · 2026학년도 2학기 중간고사 · 중3 · 삼각비 — 문제 그림 아홉 장.

도우미는 surisomath-grind 스킬의 grind_figure를 쓴다. build.py가 import 경로를 잡아
주므로 이 파일은 build.py로 실행한다.

    python .claude/skills/surisomath-exam/templates/build.py build/시험대비/20262학기중간/중3/삼각비/problems.yaml

그림은 단 글 너비(229pt) 안에 들어야 한다. y 범위가 배율을 정하므로 넓은 그림(001·005의
산)은 y 범위를 넉넉히 잡아 배율을 낮춘다. save()가 위아래 여백을 재서 y 범위를 일러 준다.
삽화는 없다. 산·기구·성산일출봉은 지면 선 위의 삼각형이다. 길이는 연마와 같이 점선
곡선(g.dim)으로 달고, 각은 호와 각도 글로 표시한다. 점 이름이 있는 꼭짓점에서는 곡선
양끝을 조금 물려(trim) 이름과 겹치지 않게 한다.
"""
from __future__ import annotations

import math

import grind_figure as g

g.setup(__file__)

TAN, RAD = math.tan, math.radians


def unit(p, q):
    """p에서 q로 향하는 단위벡터."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    n = math.hypot(dx, dy)
    return dx / n, dy / n


# ── 두 지점에서 올려다본 꼭대기(001 · 002 · 005) ────────────────────────
# 먼 점 far, 가까운 점 near가 지면 위에 있고 꼭대기 top의 발 H가 그 오른쪽에 있다.
# 지면 선 far–H, 세 변, H의 직각, 두 각(호 + 각도 글), 두 지점 사이 길이(지면 아래 점선 곡선).
# 점 이름은 지면 아래 5pt. 곡선은 이름을 피해 양끝을 4pt 물린다.

def elevation(ax, far, near, top, a_far, a_near, base_text, names):
    H = (top[0], far[1])
    g.seg(ax, far, H)
    g.seg(ax, far, top)
    g.seg(ax, near, top)
    g.seg(ax, top, H)
    g.right_angle(ax, H, -1, 1)
    g.angle(ax, far, H, top, "$%d^{\\circ}$" % a_far, r=16)
    g.angle(ax, near, H, top, "$%d^{\\circ}$" % a_near, r=11)
    g.dim(ax, far, near, base_text, side=-1, trim=4)
    g.name(ax, far, names[0], dy=-5, va="top")
    g.name(ax, near, names[1], dy=-5, va="top")
    g.name(ax, top, names[2], dy=5, va="bottom")
    g.name(ax, H, names[3], dy=-5, va="top")


def p1():
    """A·B가 80m, 각 35°·52°. CH = 80 / (1/tan35° − 1/tan52°) ≈ 123.6m."""
    h = 80 / (1 / TAN(RAD(35)) - 1 / TAN(RAD(52)))
    A, B = (0.0, 0.0), (80.0, 0.0)
    C = (h / TAN(RAD(35)), h)
    f, ax = g.canvas(5, -34.47, 156.34)
    elevation(ax, A, B, C, 35, 52, "80m", "ABCH")
    g.save(f, "p1.svg")


def p2():
    """B·C가 2m, 각 40°·62°, 기구 A. AH = 2 / (1/tan40° − 1/tan62°) ≈ 3.03m."""
    h = 2 / (1 / TAN(RAD(40)) - 1 / TAN(RAD(62)))
    B, C = (0.0, 0.0), (2.0, 0.0)
    A = (h / TAN(RAD(40)), h)
    f, ax = g.canvas(5, -0.85, 3.83)
    elevation(ax, B, C, A, 40, 62, "2m", "BCAH")
    g.save(f, "p2.svg")


def p5():
    """A·B가 124m, 각 27°·38°. CH ≈ 182.4m. 밑변이 길어 배율을 더 낮춘다."""
    h = 124 / (1 / TAN(RAD(27)) - 1 / TAN(RAD(38)))
    A, B = (0.0, 0.0), (124.0, 0.0)
    C = (h / TAN(RAD(27)), h)
    f, ax = g.canvas(5, -50.52, 229.51)
    elevation(ax, A, B, C, 27, 38, "124m", "ABCH")
    g.save(f, "p5.svg")


# ── 각의 이등분선(003 · 006) ─────────────────────────────────────────────
# BC가 수평(원문 지시). B가 왼쪽 아래, C가 오른쪽 아래, A가 위. ∠A = 60°이고 AB > AC라
# A는 BC의 가운데보다 오른쪽에 온다. BD : DC = AB : AC. A의 두 각에 같은 각 표시(호 + 획).
# 두 변의 길이는 변 바깥에 점선 곡선으로.

def bisector(ax, ab, ac, tb, tc):
    bc = math.sqrt(ab * ab + ac * ac - ab * ac)          # 코사인 법칙, cos60° = 1/2
    B, C = (0.0, 0.0), (bc, 0.0)
    ax_ = (ab * ab - ac * ac + bc * bc) / (2 * bc)
    A = (ax_, math.sqrt(ab * ab - ax_ * ax_))
    D = (bc * ab / (ab + ac), 0.0)
    g.poly(ax, [A, B, C])
    g.seg(ax, A, D)
    g.angle(ax, A, B, D, "", r=12, ticks=1)
    g.angle(ax, A, D, C, "", r=12, ticks=1)
    g.dim(ax, B, A, tb, side=1, trim=4)
    g.dim(ax, A, C, tc, side=1, trim=4)
    g.name(ax, A, "A", dy=5, va="bottom")
    g.name(ax, B, "B", dx=-3, dy=-4, ha="right", va="top")
    g.name(ax, C, "C", dx=3, dy=-4, ha="left", va="top")
    g.name(ax, D, "D", dy=-5, va="top")


def p3():
    f, ax = g.canvas(5, -1.95, 9.51)
    bisector(ax, 10.0, 8.0, "10", "8")
    g.save(f, "p3.svg")


def p6():
    f, ax = g.canvas(5, -1.49, 7.25)
    bisector(ax, 8.0, 6.0, "8cm", "6cm")
    g.save(f, "p6.svg")


# ── 004 — 정사각형의 두 중점 ─────────────────────────────────────────────
# A 왼쪽 위, B 왼쪽 아래, C 오른쪽 아래, D 오른쪽 위. M은 BC(아래 변), N은 CD(오른 변)의 중점.
# 같은 길이 표시: BM·MC 한 획, CN·ND 두 획. 4cm는 왼 변 바깥에 점선 곡선으로.

def p4():
    s = 4.0
    A, B, C, D = (0.0, s), (0.0, 0.0), (s, 0.0), (s, s)
    M, N = (s / 2, 0.0), (s, s / 2)
    f, ax = g.canvas(6, -0.9, 4.9)
    g.rect(ax, B, s, s)
    g.seg(ax, A, M)
    g.seg(ax, A, N)
    g.seg(ax, M, N)
    g.angle(ax, A, M, N, "$x$", r=14)
    g.tick(ax, B, M)
    g.tick(ax, M, C)
    g.tick(ax, C, N, n=2)
    g.tick(ax, N, D, n=2)
    g.dim(ax, A, B, "4cm", side=-1, trim=3)
    g.name(ax, A, "A", dx=-4, dy=4, ha="right", va="bottom")
    g.name(ax, B, "B", dx=-4, dy=-4, ha="right", va="top")
    g.name(ax, C, "C", dx=4, dy=-4, ha="left", va="top")
    g.name(ax, D, "D", dx=4, dy=4, ha="left", va="bottom")
    g.name(ax, M, "M", dy=-5, va="top")
    g.name(ax, N, "N", dx=5, ha="left")
    g.save(f, "p4.svg")


# ── 007 — 변을 줄이고 늘인 직각삼각형 ────────────────────────────────────
# B가 직각. A'는 BA 위(0.7배), C'는 BC의 연장 위(1.4배). ABC는 10% 틴트, A'BC'은 점선.

def p7():
    A, B, C = (0.0, 4.0), (0.0, 0.0), (5.0, 0.0)
    A2, C2 = (0.0, 4.0 * 0.7), (5.0 * 1.4, 0.0)
    f, ax = g.canvas(5, -1.04, 4.46)
    g.shade(ax, [A, B, C])
    g.poly(ax, [A, B, C])
    g.poly(ax, [A2, B, C2], dashed=True)
    g.right_angle(ax, B, 1, 1)
    g.name(ax, A, "A", dx=-4, ha="right")
    g.name(ax, B, "B", dx=-4, dy=-4, ha="right", va="top")
    g.name(ax, C, "C", dy=-5, va="top")
    g.name(ax, A2, "$\\mathrm{A}'$", dx=-4, ha="right")
    g.name(ax, C2, "$\\mathrm{C}'$", dy=-5, va="top")
    g.save(f, "p7.svg")


# ── 008 — 회전축 위의 한 꼭짓점 ───────────────────────────────────────────
# 원문: 점 A만 직선 l 위에 있고 AB는 l 위에 있지 않다. AC가 l과 30°를 이루며 오른쪽 아래로
# 내려가고, ∠ACB = 60°, ∠ABC = 90°라 ∠BAC = 30°. AB는 l에서 60° 방향이라 B는 AC의
# 오른쪽 위에 있다. AB = 2√3이면 AC = 4, BC = 2. 회전체는 팽이꼴(원뿔 + 원뿔대 − 원뿔).

def p8():
    ab = 2 * math.sqrt(3)
    A = (0.0, 0.0)
    B = g.polar(A, ab, -30)             # l(아래 방향)에서 60°
    C = g.polar(A, ab / math.cos(RAD(30)), -60)   # l에서 30°
    f, ax = g.canvas(7, -4.57, 1.37)
    g.axis(ax, (0.0, C[1] - 0.9), (0.0, 1.0), "$l$")
    g.poly(ax, [A, B, C])
    g.corner_mark(ax, B, unit(B, A), unit(B, C))
    # l과 AC 사이의 30°. 좁은 각이라 글을 각 안에 두면 l과 AC에 끼니 호만 그리고
    # 지시선으로 l 왼쪽에 뺀다(좁은 각 규칙). 지시선이 축을 가로지른다
    m = g.angle(ax, A, (0.0, -1.0), C, "", r=14)
    g.leader(ax, m, "$30^{\\circ}$", dx=-3, dy=-1)
    g.angle(ax, C, B, A, "$60^{\\circ}$", r=11)
    g.dim(ax, A, B, "$2\\sqrt{3}$", side=1, trim=4)
    g.name(ax, A, "A", dx=-5, ha="right")
    g.name(ax, B, "B", dx=5, ha="left")
    g.name(ax, C, "C", dx=4, dy=-4, ha="left", va="top")
    g.save(f, "p8.svg")


# ── 009 — 직사각형의 두 중점 ─────────────────────────────────────────────
# A 왼쪽 위, B 왼쪽 아래, C 오른쪽 아래, D 오른쪽 위. E는 AD(위 변), F는 CD(오른 변)의 중점.
# 각 x°는 B에서 BF와 BE 사이. 같은 길이 표시: AE·ED 한 획, CF·FD 두 획.
# 가로 6은 아래 변 아래에, 세로 4는 왼 변 왼쪽에 점선 곡선으로.

def p9():
    w, h = 6.0, 4.0
    A, B, C, D = (0.0, h), (0.0, 0.0), (w, 0.0), (w, h)
    E, F = (w / 2, h), (w, h / 2)
    f, ax = g.canvas(5, -1.35, 5.03)
    g.rect(ax, B, w, h)
    g.seg(ax, E, B)
    g.seg(ax, B, F)
    g.seg(ax, E, F)
    g.angle(ax, B, F, E, "$x^{\\circ}$", r=14)
    g.tick(ax, A, E)
    g.tick(ax, E, D)
    g.tick(ax, C, F, n=2)
    g.tick(ax, F, D, n=2)
    g.dim(ax, B, C, "6", side=-1, trim=3)
    g.dim(ax, A, B, "4", side=-1, trim=3)
    g.name(ax, A, "A", dx=-4, dy=4, ha="right", va="bottom")
    g.name(ax, B, "B", dx=-4, dy=-4, ha="right", va="top")
    g.name(ax, C, "C", dx=4, dy=-4, ha="left", va="top")
    g.name(ax, D, "D", dx=4, dy=4, ha="left", va="bottom")
    g.name(ax, E, "E", dy=5, va="bottom")
    g.name(ax, F, "F", dx=5, ha="left")
    g.save(f, "p9.svg")


if __name__ == "__main__":
    print("figures/")
    p1()
    p2()
    p3()
    p4()
    p5()
    p6()
    p7()
    p8()
    p9()
