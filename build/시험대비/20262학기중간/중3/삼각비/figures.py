# -*- coding: utf-8 -*-
"""시험대비 · 2026학년도 2학기 중간고사 · 중3 · 삼각비 — 문제 그림 아홉 장.

도우미는 surisomath-grind 스킬의 grind_figure를 쓴다. build.py가 import 경로를 잡아
주므로 이 파일은 build.py로 실행한다.

    python .claude/skills/surisomath-exam/templates/build.py build/시험대비/20262학기중간/중3/삼각비/problems.yaml

그림은 단 글 너비(229pt) 안에 들어야 한다. y 범위가 배율을 정하므로 넓은 그림(001·005의
산)은 y 범위를 넉넉히 잡아 배율을 낮춘다. save()가 위아래 여백을 재서 y 범위를 일러 준다.
삽화는 없다. 산·기구·성산일출봉은 지면 선 위의 삼각형이다. 길이는 교과서처럼 변 옆에
글로 적고, 각은 호와 각도 글로 표시한다.
"""
from __future__ import annotations

import math

import grind_figure as g

g.setup(__file__)

TAN, RAD = math.tan, math.radians


def mid(p, q):
    return ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)


# ── 두 지점에서 올려다본 꼭대기(001 · 002 · 005) ────────────────────────
# 먼 점 far, 가까운 점 near가 지면 위에 있고 꼭대기 top의 발 H가 그 오른쪽에 있다.
# 지면 선 far–H, 세 변, H의 직각, 두 각(호 + 각도 글), 두 지점 사이 길이 글.

def elevation(ax, far, near, top, a_far, a_near, base_text, names):
    H = (top[0], far[1])
    g.seg(ax, far, H)
    g.seg(ax, far, top)
    g.seg(ax, near, top)
    g.seg(ax, top, H)
    g.right_angle(ax, H, -1, 1)
    g.angle(ax, far, H, top, "$%d^{\\circ}$" % a_far, r=16)
    g.angle(ax, near, H, top, "$%d^{\\circ}$" % a_near, r=11)
    g.name(ax, mid(far, near), base_text, dy=-5, va="top")
    g.name(ax, far, names[0], dy=-5, va="top")
    g.name(ax, near, names[1], dy=-5, va="top")
    g.name(ax, top, names[2], dy=5, va="bottom")
    g.name(ax, H, names[3], dy=-5, va="top")


def p1():
    """A·B가 80m, 각 35°·52°. CH = 80 / (1/tan35° − 1/tan52°) ≈ 123.6m."""
    h = 80 / (1 / TAN(RAD(35)) - 1 / TAN(RAD(52)))
    A, B = (0.0, 0.0), (80.0, 0.0)
    C = (h / TAN(RAD(35)), h)
    f, ax = g.canvas(5, -31.9, 155.6)
    elevation(ax, A, B, C, 35, 52, "80m", "ABCH")
    g.save(f, "p1.svg")


def p2():
    """B·C가 2m, 각 40°·62°, 기구 A. AH = 2 / (1/tan40° − 1/tan62°) ≈ 3.03m."""
    h = 2 / (1 / TAN(RAD(40)) - 1 / TAN(RAD(62)))
    B, C = (0.0, 0.0), (2.0, 0.0)
    A = (h / TAN(RAD(40)), h)
    f, ax = g.canvas(5, -0.78, 3.81)
    elevation(ax, B, C, A, 40, 62, "2m", "BCAH")
    g.save(f, "p2.svg")


def p5():
    """A·B가 124m, 각 27°·38°. CH ≈ 182.4m. 밑변이 길어 배율을 더 낮춘다."""
    h = 124 / (1 / TAN(RAD(27)) - 1 / TAN(RAD(38)))
    A, B = (0.0, 0.0), (124.0, 0.0)
    C = (h / TAN(RAD(27)), h)
    f, ax = g.canvas(5, -46.86, 228.50)
    elevation(ax, A, B, C, 27, 38, "124m", "ABCH")
    g.save(f, "p5.svg")


# ── 각의 이등분선(003 · 006) ─────────────────────────────────────────────
# A가 위, ∠A = 60°. AB는 240° 방향, AC는 300° 방향이라 이등분선 AD는 곧게 아래로 내려간다.
# BD : DC = AB : AC. A의 두 각에 같은 각 표시(호 + 획).

def bisector(ax, ab, ac, tb, tc):
    A = (0.0, 0.0)
    B = g.polar(A, ab, 240)
    C = g.polar(A, ac, 300)
    t = ab / (ab + ac)
    D = (B[0] + (C[0] - B[0]) * t, B[1] + (C[1] - B[1]) * t)
    g.poly(ax, [A, B, C])
    g.seg(ax, A, D)
    g.angle(ax, A, B, D, "", r=12, ticks=1)
    g.angle(ax, A, D, C, "", r=12, ticks=1)
    g.name(ax, A, "A", dy=5, va="bottom")
    g.name(ax, B, "B", dx=-4, dy=-4, ha="right", va="top")
    g.name(ax, C, "C", dx=4, dy=-4, ha="left", va="top")
    g.name(ax, D, "D", dy=-5, va="top")
    g.name(ax, mid(A, B), tb, dx=-6, dy=3, ha="right", va="bottom")
    g.name(ax, mid(A, C), tc, dx=6, dy=3, ha="left", va="bottom")


def p3():
    f, ax = g.canvas(5, -10.76, 2.19)
    bisector(ax, 10.0, 8.0, "10", "8")
    g.save(f, "p3.svg")


def p6():
    f, ax = g.canvas(5, -8.7, 1.8)
    bisector(ax, 8.0, 6.0, "8cm", "6cm")
    g.save(f, "p6.svg")


# ── 004 — 정사각형의 두 중점 ─────────────────────────────────────────────
# A 왼쪽 위, B 왼쪽 아래, C 오른쪽 아래, D 오른쪽 위. M은 BC(아래 변), N은 CD(오른 변)의 중점.
# 같은 길이 표시: BM·MC 한 획, CN·ND 두 획. 4cm는 왼 변 옆에.

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
    g.name(ax, A, "A", dx=-4, dy=4, ha="right", va="bottom")
    g.name(ax, B, "B", dx=-4, dy=-4, ha="right", va="top")
    g.name(ax, C, "C", dx=4, dy=-4, ha="left", va="top")
    g.name(ax, D, "D", dx=4, dy=4, ha="left", va="bottom")
    g.name(ax, M, "M", dy=-5, va="top")
    g.name(ax, N, "N", dx=5, ha="left")
    g.name(ax, mid(A, B), "4cm", dx=-5, ha="right")
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


# ── 008 — 회전축 위의 직각삼각형 ─────────────────────────────────────────
# ∠A = 30°라 AB가 축 l 위에 있다. A가 위, B가 아래, C가 오른쪽. 축은 A 위와 B 아래로 더 뻗는다.

def p8():
    ab = 2 * math.sqrt(3)
    A, B = (0.0, ab), (0.0, 0.0)
    C = (ab * TAN(RAD(30)), 0.0)
    f, ax = g.canvas(7, -1.21, 5.06)
    g.axis(ax, (0.0, -1.0), (0.0, ab + 1.2), "$l$")
    g.poly(ax, [A, B, C])
    g.right_angle(ax, B, 1, 1)
    # ∠A는 30°라 이등분선이 축에서 15°밖에 안 떨어진다. 글을 각 안에 두면 AB에 걸리니
    # 호만 그리고 지시선으로 AC 밖에 뺀다(SKILL의 좁은 각 규칙).
    m = g.angle(ax, A, B, C, "", r=14)
    g.leader(ax, m, "$30^{\\circ}$", dx=3, dy=-1)
    g.angle(ax, C, A, B, "$60^{\\circ}$", r=11)
    g.name(ax, A, "A", dx=-5, ha="right")
    g.name(ax, B, "B", dx=-5, dy=-3, ha="right", va="top")
    g.name(ax, C, "C", dx=5, dy=-3, ha="left", va="top")
    g.name(ax, (0.0, ab / 2), "$2\\sqrt{3}$", dx=-6, ha="right")
    g.save(f, "p8.svg")


# ── 009 — 직사각형의 두 중점 ─────────────────────────────────────────────
# A 왼쪽 위, B 왼쪽 아래, C 오른쪽 아래, D 오른쪽 위. E는 AD(위 변), F는 CD(오른 변)의 중점.
# 각 x°는 B에서 BF와 BE 사이. 같은 길이 표시: AE·ED 한 획, CF·FD 두 획.

def p9():
    w, h = 6.0, 4.0
    A, B, C, D = (0.0, h), (0.0, 0.0), (w, 0.0), (w, h)
    E, F = (w / 2, h), (w, h / 2)
    f, ax = g.canvas(5, -1.03, 5.03)
    g.rect(ax, B, w, h)
    g.seg(ax, E, B)
    g.seg(ax, B, F)
    g.seg(ax, E, F)
    g.angle(ax, B, F, E, "$x^{\\circ}$", r=14)
    g.tick(ax, A, E)
    g.tick(ax, E, D)
    g.tick(ax, C, F, n=2)
    g.tick(ax, F, D, n=2)
    g.name(ax, A, "A", dx=-4, dy=4, ha="right", va="bottom")
    g.name(ax, B, "B", dx=-4, dy=-4, ha="right", va="top")
    g.name(ax, C, "C", dx=4, dy=-4, ha="left", va="top")
    g.name(ax, D, "D", dx=4, dy=4, ha="left", va="bottom")
    g.name(ax, E, "E", dy=5, va="bottom")
    g.name(ax, F, "F", dx=5, ha="left")
    g.name(ax, (w / 2, 0.0), "6", dy=-5, va="top")
    g.name(ax, (0.0, h / 2), "4", dx=-5, ha="right")
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
