# -*- coding: utf-8 -*-
"""시험대비 · 2026학년도 2학기 중간고사 · 중3 · 삼각비 — 도형 그림 스물아홉 장(008은 그림이 없다).

도우미는 surisomath-grind 스킬의 grind_figure를 쓴다. build.py가 import 경로를 잡아
주므로 이 파일은 build.py로 실행한다.

    python .claude/skills/surisomath-exam/templates/build.py build/시험대비/20262학기중간/중3/삼각비/problems.yaml

도형 선 0.7pt, 보조선 0.4pt, 길이는 연마와 같이 점선 곡선(g.dim, 꼭짓점에서 꼭짓점까지 — trim 없음),
각은 호와 각도 글, 같은 각은 점(ticks=1, 두 쌍이면 ×도), 같은 길이는 g.tick. 좁은 각의 글은 지시선으로 밖에
(005 θ₁°, 004 θ°, 013 θ°, 014 θ₃°~θ₅°, 024 30°). 각의 크기 문자는 θ°(둘이면 θ₁°·θ₂°, 수열이면 θₙ°. 육십분법이라 문자에도 ° — 2026-09-26 선생님 지시). 그림은 단 글 너비(229pt) 안에 들어야 하고 y 범위가
배율을 정한다. 점의 자리는 책 그림(사진)을 그대로 따른다.

삽화(2026-09-23 선생님 결정): 001 지구·달·태양은 이름 붙은 세 점 — 88°와 태양의 2°를 실제 각으로 그리고
먼 거리는 "…"로 끊는다. 009 도로 표지판은 실물 도안(assets/KR_road_sign_116.svg, 퍼블릭 도메인)을
래스터로 심는다. 026 관람차는 살·곤돌라·A자 기둥·지면 띠까지 선화로. 013 정사각뿔은 투시도(perspective).

문제가 정하지 않는 것은 책 그림에 맞춰 골랐다: 002 AR = 3(RD = RB = 5는 문제가 정한다),
003 A의 자리(sin x = 1/3 → AB = 18), 007 r = 1(r' = 3, AB = 3 + 3√3), 013 정사각뿔의 눈 자리
(EYE·LOOK·FOCAL)와 P = VC의 0.55 지점, 015 AE = CD = 1.8(한 변 6), 019 P = AC의 중점,
021 삼각형의 모양(∠A = 45°, DE = 8이면 AD = 4√6, AE ≈ 10.93로 정해진다), 024 D의 자리(BD : DC = 3 : 2),
025 A·P·Q의 자리, 027 DE·DF의 방향(200°·230°, DG = 6, DH = 5, 30°에 맞춰 평행사변형을 역산),
028 b = 5(a ≈ 7.66), 029 C의 방향 120°(∠B = 30°), D = 호 AC의 가운데.
색칠은 문제가 가리키는 것만(027 사각형 EFHG, 029 사각형 ABCD, 030 겹쳐지는 부분).
"""
from __future__ import annotations

import math
from pathlib import Path

from matplotlib.patches import Circle, Polygon

import grind_figure as g

g.setup(__file__)

R2, R3 = math.sqrt(2), math.sqrt(3)
HEAD = 6.0             # 축 화살촉 길이(pt). 연마 2026.09.12·이차함수와 같다


# ── 공통 ────────────────────────────────────────────────────────────────

def dist(p, q):
    return math.hypot(p[0] - q[0], p[1] - q[1])


def unit(p, q):
    """p에서 q로 향하는 단위벡터."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    n = math.hypot(dx, dy)
    return dx / n, dy / n


def lerp(p, q, t):
    return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)


def mid(p, q):
    return lerp(p, q, 0.5)


def meet(P, d, Q, e):
    """직선 P + t·d 와 Q + s·e 의 교점."""
    det = d[0] * e[1] - d[1] * e[0]
    rx, ry = Q[0] - P[0], Q[1] - P[1]
    t = (rx * e[1] - ry * e[0]) / det
    return P[0] + t * d[0], P[1] + t * d[1]


def cross(P, Q, R, S):
    """선분 PQ와 RS가 놓인 두 직선의 교점."""
    return meet(P, (Q[0] - P[0], Q[1] - P[1]), R, (S[0] - R[0], S[1] - R[1]))


def arrow(ax, p, q, lw=g.AUX):
    """p에서 q까지의 축·반직선. q 끝에 채운 화살촉(길이 HEAD pt, 밑변 HEAD×0.7pt)."""
    L = g.pt(ax, HEAD)
    ux, uy = unit(p, q)
    base = (q[0] - ux * L, q[1] - uy * L)
    g.seg(ax, p, base, lw=lw)
    w = L * 0.35
    ax.add_patch(Polygon([q, (base[0] - uy * w, base[1] + ux * w),
                          (base[0] + uy * w, base[1] - ux * w)],
                         closed=True, facecolor=g.INK, edgecolor="none"))


def plane(ax, x0, x1, y0, y1, o=(3, -3, "left", "top")):
    """두 축과 이름. x는 오른쪽 화살촉 옆, y는 위 화살촉 왼쪽, O는 o=(dx, dy, ha, va)."""
    arrow(ax, (x0, 0), (x1, 0))
    arrow(ax, (0, y0), (0, y1))
    g.name(ax, (x1, 0), "$x$", dx=4, ha="left")
    g.name(ax, (0, y1), "$y$", dx=-4, ha="right")
    dx, dy, ha, va = o
    g.name(ax, (0, 0), "O", dx=dx, dy=dy, ha=ha, va=va)


def center(ax, p, text, dx=4.0, dy=0.0, ha="left", va="center"):
    """원의 중심·이름 있는 점: 점과 이름."""
    g.dot(ax, p)
    g.name(ax, p, text, dx=dx, dy=dy, ha=ha, va=va)


# ── 001 — 지구·달·태양 ───────────────────────────────────────────────────
# 달이 원점, 지구가 그 위. 각은 양 끝 다 실제 크기로 그린다 — 지구에서 88°(지구→태양 시선은
# 수평에서 2° 아래, 달→태양 시선은 수평), 태양에서 2°(두 시선이 태양에서 2°로 벌어진 가는 쐐기).
# 실제 비율(1 : 28.6)로는 태양이 지면 밖이라 두 시선을 중간에 끊고(생략 표시 …) 태양 쪽은
# 태양에서 2°로 모이는 부분만 그린다. 과학 교과서의 천체 거리 그림 관례다(2026-09-23 선생님).

def p1():
    M, E = (0.0, 0.0), (0.0, 1.0)
    t2 = math.tan(math.radians(2))
    x_cut, gap, L = 2.4, 0.7, 3.0                          # 지구 쪽 길이, 끊긴 틈, 태양 쪽 길이
    x_back = x_cut + gap
    S = (x_back + L, 0.0)
    E2 = g.polar(S, L, 178)                                # 태양에서 본 지구 방향(수평에서 2° 위)
    fig, ax = g.canvas(3, -0.4, 1.65)                      # 표가 있는 문제라 3칸 — 풀 자리 8칸을 지킨다
    g.seg(ax, E, M)
    g.seg(ax, E, (x_cut, 1.0 - x_cut * t2))               # 지구의 시선: 2° 아래
    g.seg(ax, M, (x_cut, 0.0))                             # 달의 시선: 수평
    g.seg(ax, E2, S)                                       # 태양에서 2°로 모이는 두 시선
    g.seg(ax, (x_back, 0.0), S)
    # 생략 표시: 끊긴 자리에 점 셋(…). 학생에게 익숙한 표기라 빗금(//) 대신 쓴다(2026-09-23 선생님)
    for y0, y1 in ((1.0 - x_cut * t2, E2[1]), (0.0, 0.0)):
        for k in (1, 2, 3):
            t = k / 4
            ax.add_patch(Circle((x_cut + (x_back - x_cut) * t, y0 + (y1 - y0) * t),
                                g.pt(ax, 0.7), facecolor=g.INK, edgecolor="none"))
    g.right_angle(ax, M, 1, 1)
    g.angle(ax, E, M, (x_cut, 1.0 - x_cut * t2), "$88^{\\circ}$", r=14)
    for p in (E, M, S):
        g.dot(ax, p)
    g.name(ax, E, "지구", dy=5, va="bottom")
    g.name(ax, M, "달", dx=-5, ha="right")
    g.name(ax, S, "태양", dy=5, va="bottom")
    g.save(fig, "p1.svg")


# ── 002 — 접은 색종이 ───────────────────────────────────────────────────
# B(0, 0), C(8, 0), D(8, 4), A(0, 4). RD = RB = 5라 R(3, 4), RQ ⊥ BD라 Q(5, 0). P는 C를 RQ에 대칭.

def p2():
    A, B, C, D = (0.0, 4.0), (0.0, 0.0), (8.0, 0.0), (8.0, 4.0)
    R, Q = (3.0, 4.0), (5.0, 0.0)
    P = (3.2, -2.4)
    fig, ax = g.canvas(6, -3.79, 6.15)
    for p, q in ((A, B), (A, R), (R, B), (R, Q), (Q, P), (P, B)):
        g.seg(ax, p, q)
    for p, q in ((R, D), (D, C), (C, Q), (B, Q)):
        g.seg(ax, p, q, dashed=True)
    g.angle(ax, R, B, Q, "$\\theta^{\\circ}$", r=14)
    g.dim(ax, A, D, "8cm", side=1, gap=g.pt(ax, 20))     # R 이름 위로 곡선이 지나가게 높인다
    g.dim(ax, A, B, "4cm", side=-1)
    g.name(ax, A, "A", dx=-4, dy=2, ha="right", va="bottom")
    g.name(ax, B, "B", dx=-4, dy=-2, ha="right", va="top")
    g.name(ax, C, "C", dx=4, dy=-2, ha="left", va="top")
    g.name(ax, D, "D", dx=4, dy=2, ha="left", va="bottom")
    g.name(ax, R, "R", dy=5, va="bottom")
    g.name(ax, Q, "Q", dx=4, dy=-3, ha="left", va="top")
    g.name(ax, P, "P", dy=-5, va="top")
    g.save(fig, "p2.svg")


# ── 003 — 직각삼각형과 빗변 아닌 변의 중점을 잇는 선분 ──────────────────────
# C(0, 0), A(0, 12√2), D(−6, 0), B(−12, 0). D는 변 BC의 중점. 책의 점 E(B에서 직선 AD에 내린
# 수선의 발)와 직각삼각형 ADE는 선생님이 뺐다(2026. 9. 26.) — 문제를 세우는 데 필요 없고 푸는 도구라서.
# 책과 견주면 B와 D의 이름이 맞바뀌어 있다(선생님 지시).

def p3():
    C, D, B = (0.0, 0.0), (-6.0, 0.0), (-12.0, 0.0)
    A = (0.0, 12 * R2)
    fig, ax = g.canvas(7, -1.5, 19.5)
    g.poly(ax, [A, B, C])
    g.seg(ax, A, D)
    g.right_angle(ax, C, -1, 1)
    g.tick(ax, B, D)
    g.tick(ax, D, C)
    g.angle(ax, A, D, C, "$\\theta_1^{\\circ}$", r=30)
    m = g.angle(ax, A, B, D, "", r=16)                  # 각이 16°라 θ₂°가 안에 안 든다 — 지시선으로 왼쪽 밖에
    g.leader(ax, m, "$\\theta_2^{\\circ}$", dx=-1, dy=0.25)
    g.name(ax, A, "A", dy=5, va="bottom")
    g.name(ax, B, "B", dx=-5, ha="right")
    g.name(ax, C, "C", dx=5, ha="left")
    g.name(ax, D, "D", dx=-2, dy=4, ha="right", va="bottom")
    g.save(fig, "p3.svg")


# ── 004 — 좌표평면의 세 점 ───────────────────────────────────────────────

def p4():
    A, B, C = (6.0, 6.0), (-2.0, 2.0), (2.0, -1.0)
    fig, ax = g.canvas(6, -2.74, 8.19)
    plane(ax, -3.6, 7.6, -2.3, 7.4, o=(-3, -2, "right", "top"))
    g.poly(ax, [A, B, C])
    g.dashed(ax, A, (6.0, 0.0))
    g.dashed(ax, A, (0.0, 6.0))
    g.dashed(ax, B, (-2.0, 0.0))
    g.dashed(ax, B, (0.0, 2.0))
    g.dashed(ax, C, (2.0, 0.0))
    g.dashed(ax, C, (0.0, -1.0))
    g.name(ax, (6.0, 0.0), "6", dy=-4, va="top")
    g.name(ax, (0.0, 6.0), "6", dx=-4, ha="right")
    g.name(ax, (-2.0, 0.0), "$-2$", dy=-4, va="top")
    g.name(ax, (0.0, 2.0), "2", dx=4, dy=1, ha="left")
    g.name(ax, (2.0, 0.0), "2", dy=4, va="bottom")
    g.leader(ax, (0.0, -1.0), "$-1$", dx=-1, dy=-0.5, length=12)       # 책처럼 지시선으로 y축 왼쪽에(오른쪽이면 C와 붙어 읽힌다)
    m = g.angle(ax, B, C, A, "", r=12)
    g.leader(ax, m, "$\\theta^{\\circ}$", dx=-0.4, dy=1)
    g.name(ax, A, "A", dx=2, dy=5, va="bottom")
    g.name(ax, B, "B", dx=-5, ha="right")
    g.name(ax, C, "C", dy=-5, va="top")
    g.save(fig, "p4.svg")


# ── 005 — 변 BC를 넷으로 나눈 직각삼각형 ────────────────────────────────

def p5():
    C, A = (0.0, 0.0), (0.0, R2)
    F, E, D, B = (-1.0, 0.0), (-2.0, 0.0), (-3.0, 0.0), (-4.0, 0.0)
    fig, ax = g.canvas(5, -0.8, 1.9)
    g.poly(ax, [A, B, C])
    for p in (D, E, F):
        g.seg(ax, A, p)
    g.right_angle(ax, C, -1, 1)
    for p, q in ((B, D), (D, E), (E, F), (F, C)):
        g.tick(ax, p, q)
    g.dim(ax, A, C, "$\\sqrt{2}$", side=1)
    g.dim(ax, F, C, "1", side=-1)
    m = g.angle(ax, B, C, A, "", r=12)
    g.leader(ax, m, "$\\theta_1^{\\circ}$", dx=-0.3, dy=1)
    g.angle(ax, E, F, A, "$\\theta_2^{\\circ}$", r=24)  # θ₂°가 넓어 r=12에선 EA와 겹친다
    g.name(ax, A, "A", dy=5, va="bottom")
    g.name(ax, B, "B", dx=-5, ha="right")
    g.name(ax, C, "C", dx=4, dy=-4, ha="left", va="top")
    for p, s in ((D, "D"), (E, "E"), (F, "F")):
        g.name(ax, p, s, dy=-5, va="top")
    g.save(fig, "p5.svg")


# ── 006 — 정사각형 안의 사분원과 귀퉁이의 원 ────────────────────────────
# B(0, 0), C(2, 0), O(2, 2), A(0, 2). 원 O'의 반지름 6 − 4√2, 중심 (r, r).

def p6():
    B, C, O, A = (0.0, 0.0), (2.0, 0.0), (2.0, 2.0), (0.0, 2.0)
    r = 6 - 4 * R2
    fig, ax = g.canvas(6, -0.45, 2.7)
    g.rect(ax, B, 2.0, 2.0)
    g.arc(ax, O, 2.0, 180, 270)
    g.circle(ax, (r, r), r)
    g.dot(ax, (r, r))
    g.leader(ax, (r, r), "$\\mathrm{O}'$", dx=1, dy=1)   # 원이 작아(지름 30pt) 이름을 밖에 — 지시선이 호를 가로지른다
    g.dim(ax, A, O, "2", side=1)
    g.name(ax, A, "A", dx=-4, dy=2, ha="right", va="bottom")
    g.name(ax, O, "O", dx=4, dy=2, ha="left", va="bottom")
    g.name(ax, B, "B", dx=-4, dy=-2, ha="right", va="top")
    g.name(ax, C, "C", dx=4, dy=-2, ha="left", va="top")
    g.save(fig, "p6.svg")


# ── 007 — 빗변 위의 두 반원 ─────────────────────────────────────────────
# r = 1, r' = 3. O'(3, 3)이 AC 위에 있고 A = O' + 2r'·(−1/2, √3/2). O = A + 2r·(1/2, −√3/2).

def p7():
    r, r2 = 1.0, 3.0
    d = (0.5, -R3 / 2)
    A = (0.0, r2 * (1 + R3))
    O = (A[0] + 2 * r * d[0], A[1] + 2 * r * d[1])
    O2 = (A[0] + 2 * r2 * d[0], A[1] + 2 * r2 * d[1])
    B = (0.0, 0.0)
    C = (A[1] / R3, 0.0)
    D, E = (0.0, O[1]), (0.0, O2[1])
    fig, ax = g.canvas(7, -1.16, 9.49)
    g.poly(ax, [A, B, C])
    g.arc(ax, O, r, 120, 300)
    g.arc(ax, O2, r2, 120, 300)
    g.right_angle(ax, B, 1, 1)
    m = g.angle(ax, A, B, C, "", r=14)                    # 좁은 각. 글은 빗변 오른쪽 밖에
    g.leader(ax, m, "$30^{\\circ}$", dx=1, dy=0.3)
    center(ax, O, "O", dx=4, dy=1)
    center(ax, O2, "$\\mathrm{O}'$", dx=4, dy=1)
    # 반지름은 선분(0.4pt)을 긋고("직선으로", 2026-09-23 선생님) 길이는 책처럼 그 아래 점선 호에 글
    g.seg(ax, D, O, lw=g.AUX)
    g.seg(ax, E, O2, lw=g.AUX)
    g.dim(ax, D, O, "$r$", side=-1, gap=g.pt(ax, 6))     # 반원 O 안에 든다
    g.dim(ax, E, O2, "$r'$", side=-1)
    g.name(ax, A, "A", dy=5, va="bottom")
    g.name(ax, B, "B", dx=-4, dy=-3, ha="right", va="top")
    g.name(ax, C, "C", dx=4, dy=-3, ha="left", va="top")
    g.name(ax, D, "D", dx=-5, ha="right")
    g.name(ax, E, "E", dx=-5, ha="right")
    g.save(fig, "p7.svg")


# ── 009 — 도로 표지판(실물 도안) ────────────────────────────────────────
# assets/KR_road_sign_116.svg — 도로교통법 시행규칙 별표 6의 116번 '오르막 경사' 안전표지. 위키미디어
# 공용(File:KR_road_sign_116.svg), 대한민국 정부 저작물이라 퍼블릭 도메인. 선생님 지시(2026-09-23)로
# 선화 대신 실물 도안을 넣는다. pymupdf로 300dpi 래스터로 만들어 캔버스에 앉힌다(빨강 테두리·노랑
# 바탕 — 이 학습지에서 유일한 색). 그림 안 잉크 경계는 선·패치·글만 재므로 같은 자리에 테두리 없는
# 빈 사각형을 하나 깔아 너비 재기와 가운데 맞춤이 이미지를 보게 한다.

SIGN = Path(__file__).resolve().parent / "assets" / "KR_road_sign_116.svg"


def p9():
    import fitz
    import numpy as np
    from matplotlib.patches import Rectangle

    page = fitz.open(str(SIGN))[0]
    pix = page.get_pixmap(dpi=300, alpha=True)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    h = 4.0
    w = h * pix.width / pix.height
    fig, ax = g.canvas(5, -0.5, 4.5)
    # interpolation="none"이라야 SVG에 원본 픽셀이 그대로 들어간다(다른 보간은 72dpi로 줄여 뭉갠다)
    ax.imshow(img, extent=(0.0, w, 0.0, h), interpolation="none", zorder=1)
    ax.add_patch(Rectangle((0.0, 0.0), w, h, facecolor="none", edgecolor="none", linewidth=0))
    g.save(fig, "p9.svg")


# ── 010 — 두 각으로 재는 높이 ───────────────────────────────────────────
# B(0, 0), C(100, 0). tan28° = h/BH, tan42° = h/CH, BH − CH = 100 → h ≈ 129.85.

def p10():
    t28, t42 = math.tan(math.radians(28)), math.tan(math.radians(42))
    h = 100 / (1 / t28 - 1 / t42)
    B, C = (0.0, 0.0), (100.0, 0.0)
    H = (h / t28, 0.0)
    A = (H[0], h)
    fig, ax = g.canvas(5, -34.79, 162.99)                  # 표가 있는 문제라 5칸 — 풀 자리 8칸을 지킨다
    g.seg(ax, B, H)
    g.seg(ax, B, A)
    g.seg(ax, C, A)
    g.seg(ax, A, H)
    g.right_angle(ax, H, -1, 1)
    g.angle(ax, B, C, A, "$28^{\\circ}$", r=16)
    g.angle(ax, C, H, A, "$42^{\\circ}$", r=14)
    g.dim(ax, B, C, "100m", side=-1)
    g.name(ax, B, "B", dx=-5, ha="right")
    g.name(ax, C, "C", dx=2, dy=-5, va="top")
    g.name(ax, H, "H", dx=5, dy=-2, ha="left", va="top")
    g.name(ax, A, "A", dy=5, va="bottom")
    g.save(fig, "p10.svg")


# ── 011 — 꼭지각 36°의 이등변삼각형과 각 B의 이등분선 ───────────────────
# BC = 2, AB = AC = 1/sin18°. BD = AD = BC = 2.

def p11():
    ab = 1 / math.sin(math.radians(18))
    B, C = (-1.0, 0.0), (1.0, 0.0)
    A = (0.0, math.sqrt(ab * ab - 1))
    u = unit(A, C)
    D = (A[0] + 2 * u[0], A[1] + 2 * u[1])
    fig, ax = g.canvas(6, -0.65, 3.69)
    g.poly(ax, [A, B, C])
    g.seg(ax, B, D)
    g.angle(ax, A, B, C, "", r=14)                        # 36°는 좁아 글을 책처럼 왼쪽 밖에
    g.name(ax, A, "$36^{\\circ}$", dx=-6, dy=-16, ha="right")
    g.angle(ax, B, C, D, "", r=12, ticks=1)
    g.angle(ax, B, D, A, "", r=12, ticks=1)
    g.dim(ax, B, C, "2", side=-1)
    g.name(ax, A, "A", dy=5, va="bottom")
    g.name(ax, B, "B", dx=-4, dy=-2, ha="right", va="top")
    g.name(ax, C, "C", dx=4, dy=-2, ha="left", va="top")
    g.name(ax, D, "D", dx=5, ha="left")
    g.save(fig, "p11.svg")


# ── 012 — 각 C의 이등분선 AC와 수선 DH ──────────────────────────────────
# C(0, 0), B(−12, 0), A(−12, 6). tan∠ACB = 1/2라 cos∠ACD = 3/5, sin = 4/5 → D(−7.2, 9.6).

def p12():
    C, B, A = (0.0, 0.0), (-12.0, 0.0), (-12.0, 6.0)
    D = (-12 * 0.6, 12 * 0.8)
    fig, ax = g.canvas(6, -1.9, 11.5)
    g.poly(ax, [A, B, C, D])
    g.seg(ax, A, C)
    H = g.foot(ax, D, B, C)
    E = cross(A, C, D, H)
    g.right_angle(ax, B, 1, 1)
    g.corner_mark(ax, D, unit(D, A), unit(D, C))
    g.angle(ax, C, A, B, "", r=12, ticks=1)
    g.angle(ax, C, D, A, "", r=12, ticks=1)
    g.angle(ax, D, H, C, "$\\theta^{\\circ}$", r=14)
    g.dim(ax, A, D, "6", side=1)
    g.dim(ax, D, C, "12", side=1)
    g.name(ax, A, "A", dx=-5, ha="right")
    g.name(ax, B, "B", dx=-4, dy=-3, ha="right", va="top")
    g.name(ax, C, "C", dx=4, dy=-3, ha="left", va="top")
    g.name(ax, D, "D", dy=5, va="bottom")
    g.name(ax, H, "H", dy=-5, va="top")
    g.name(ax, E, "E", dx=4, dy=3, ha="left", va="bottom")
    g.save(fig, "p12.svg")


# ── 013 — 정사각뿔 V-ABCD와 모서리 VC 위의 점 P ─────────────────────────
# 투시도(선생님 지시, 2026-09-23 — 교과서 겨냥도 대신). 밑면의 정사각형을 위에서 볼 때 A·B·C·D가
# 195°·285°·15°·105° 방향에 오게 돌려 놓고(B가 앞, D가 뒤), 앞쪽 위의 눈 EYE에서 핀홀 투영한다.
# 평행한 모서리가 소실점 쪽으로 모인다. 눈 높이는 꼭짓점 V보다 조금 위라 D가 윤곽 안에 숨는다.

EYE = (0.45, -3.4, 1.15)       # 눈의 자리(밑면 중심이 원점, 모서리 1)
LOOK = (0.0, 0.0, 0.28)        # 바라보는 점
FOCAL = 3.0                    # 초점 거리(투영 배율)


def perspective(p):
    """세계 좌표 p를 EYE에서 LOOK을 바라보는 핀홀 카메라로 투영한 (X, Y)."""
    f = [LOOK[i] - EYE[i] for i in range(3)]
    n = math.sqrt(sum(c * c for c in f))
    f = [c / n for c in f]
    up = (0.0, 0.0, 1.0)
    r = [f[1] * up[2] - f[2] * up[1], f[2] * up[0] - f[0] * up[2], f[0] * up[1] - f[1] * up[0]]
    n = math.sqrt(sum(c * c for c in r))
    r = [c / n for c in r]
    u = [r[1] * f[2] - r[2] * f[1], r[2] * f[0] - r[0] * f[2], r[0] * f[1] - r[1] * f[0]]
    d = [p[i] - EYE[i] for i in range(3)]
    x = sum(d[i] * r[i] for i in range(3))
    y = sum(d[i] * u[i] for i in range(3))
    z = sum(d[i] * f[i] for i in range(3))
    return (FOCAL * x / z, FOCAL * y / z)


def p13():
    s = R2 / 2

    def base(deg):
        return perspective((s * math.cos(math.radians(deg)), s * math.sin(math.radians(deg)), 0.0))

    V = perspective((0.0, 0.0, s))
    A, B, C, D = base(195), base(285), base(15), base(105)
    t = 0.55
    P = perspective((t * s * math.cos(math.radians(15)), t * s * math.sin(math.radians(15)), (1 - t) * s))
    fig, ax = g.canvas(5, -0.67, 0.57)
    for p, q in ((V, A), (V, B), (V, C), (A, B), (B, C), (D, P)):
        g.seg(ax, p, q)
    for p, q in ((V, D), (D, A), (D, C), (D, B)):
        g.seg(ax, p, q, dashed=True)
    m = g.angle(ax, D, B, P, "", r=12)
    g.leader(ax, m, "$\\theta^{\\circ}$", dx=1, dy=-0.69, length=12)     # 대각선 DB와 모서리 DC 사이, 모서리 VB 오른쪽으로
    g.dim(ax, V, A, "1", side=-1)
    g.dot(ax, P)
    g.name(ax, V, "V", dy=5, va="bottom")
    g.name(ax, A, "A", dx=-4, dy=-2, ha="right", va="top")
    g.name(ax, B, "B", dy=-5, va="top")
    g.name(ax, C, "C", dx=5, ha="left")
    g.name(ax, D, "D", dx=-1, dy=-6, va="top")             # 위·왼쪽은 모서리 VA가 10pt 옆을 지난다. 아래(DA·DB 사이)로
    g.name(ax, P, "P", dx=4, dy=3, ha="left", va="bottom")
    g.save(fig, "p13.svg")


# ── 014 — 테오도로스 나선(직각삼각형 여섯) ──────────────────────────────
# O(0, 0), A₁(−1, 0). 다음 점 Aₙ₊₁은 O에서 본 방향을 시계 방향으로 직각 돌린 쪽으로 1cm.
# 이름은 O, A₁~A₇(2026-09-26 선생님 지시 — A, B, C, …가 어색하니 첨자로). 각은 θ₁°~θ₆°(처음엔 x₁~x₆).

def p14():
    O = (0.0, 0.0)
    pts = [(-1.0, 0.0)]
    for _ in range(6):
        vx, vy = pts[-1]
        n = math.hypot(vx, vy)
        pts.append((vx + vy / n, vy - vx / n))
    fig, ax = g.canvas(7, -0.78, 2.40)
    for p in pts:
        g.seg(ax, O, p)
    for p, q in zip(pts, pts[1:]):
        g.seg(ax, p, q)
        g.corner_mark(ax, p, unit(p, O), unit(p, q))
        g.dim(ax, p, q, "1cm", side=1)
    g.dim(ax, pts[0], O, "1cm", side=-1)
    # O의 각 θ₁°~θ₆°. 좁은 θ₃°·θ₄°·θ₅°는 지시선으로 밖에
    for k in range(6):
        p, q = pts[k], pts[k + 1]
        text = "$\\theta_%d^{\\circ}$" % (k + 1)
        if k in (2, 3, 4, 5):                            # θ₆°(22°)도 θ° 글자가 넓어 지시선으로 밑변 아래에
            m = g.angle(ax, O, q, p, "", r=16)
            dxy = {2: (0.15, 1), 3: (0.9, 1), 4: (1.2, 0.6), 5: (1, -0.8)}[k]
            g.leader(ax, m, text, dx=dxy[0], dy=dxy[1])
        else:
            g.angle(ax, O, q, p, text, r=16)
    sub = ["$\\mathrm{A}_%d$" % (k + 1) for k in range(7)]
    g.name(ax, O, "O", dy=-5, va="top")
    g.name(ax, pts[0], sub[0], dx=-3, dy=-5, va="top")
    g.name(ax, pts[1], sub[1], dx=-5, ha="right")
    g.name(ax, pts[2], sub[2], dx=-4, dy=3, ha="right", va="bottom")
    g.name(ax, pts[3], sub[3], dy=5, va="bottom")
    g.name(ax, pts[4], sub[4], dx=4, dy=3, ha="left", va="bottom")
    g.name(ax, pts[5], sub[5], dx=4, dy=3, ha="left", va="bottom")
    g.name(ax, pts[6], sub[6], dx=5, ha="left")
    g.name(ax, pts[6], "$\\vdots$", dx=2, dy=-9, va="top")
    g.save(fig, "p14.svg")


# ── 015 — 정삼각형 안의 두 선분 BE, AD ──────────────────────────────────

def p15():
    B, C = (0.0, 0.0), (6.0, 0.0)
    A = (3.0, 3 * R3)
    E = lerp(A, C, 1.8 / 6)
    D = (6.0 - 1.8, 0.0)
    P = cross(B, E, A, D)
    fig, ax = g.canvas(6, -1.02, 6.22)
    g.poly(ax, [A, B, C])
    g.seg(ax, B, E)
    g.seg(ax, A, D)
    g.tick(ax, A, E, n=2)
    g.tick(ax, D, C, n=2)
    g.angle(ax, P, B, D, "$\\theta^{\\circ}$", r=12)
    g.name(ax, A, "A", dy=5, va="bottom")
    g.name(ax, B, "B", dx=-4, dy=-3, ha="right", va="top")
    g.name(ax, C, "C", dx=4, dy=-3, ha="left", va="top")
    g.name(ax, D, "D", dy=-5, va="top")
    g.name(ax, E, "E", dx=5, ha="left")
    g.name(ax, P, "P", dx=-5, dy=2, ha="right", va="bottom")
    g.save(fig, "p15.svg")


# ── 016 — ∠AEC = 60°, AE = ED인 두 직각삼각형 ───────────────────────────
# C(0, 0), A(0, √3), E(−1, 0). D = E + 2·(EA를 90° 돌린 방향). B는 직선 AD와 x축의 교점.

def p16():
    C, A, E = (0.0, 0.0), (0.0, R3), (-1.0, 0.0)
    D = (E[0] - R3, E[1] + 1.0)
    B = meet(A, (D[0] - A[0], D[1] - A[1]), (0.0, 0.0), (1.0, 0.0))
    fig, ax = g.canvas(5, -0.9, 2.75)
    g.poly(ax, [A, B, C])
    g.seg(ax, A, E)
    g.seg(ax, E, D)
    g.right_angle(ax, C, -1, 1)
    g.corner_mark(ax, E, unit(E, A), unit(E, D))
    g.angle(ax, E, C, A, "$60^{\\circ}$", r=12)
    g.tick(ax, A, E, n=2)
    g.tick(ax, E, D, n=2)
    g.dim(ax, E, C, "1", side=-1)
    g.name(ax, A, "A", dy=5, va="bottom")
    g.name(ax, B, "B", dx=-5, ha="right")
    g.name(ax, C, "C", dx=4, dy=-3, ha="left", va="top")
    g.name(ax, D, "D", dy=5, va="bottom")
    g.name(ax, E, "E", dx=-2, dy=-5, va="top")
    g.save(fig, "p16.svg")


# ── 017 — 부채꼴 OAB와 선분 AP에 접하는 원 ──────────────────────────────

def p17():
    O, A, B = (0.0, 0.0), (4.0, 0.0), (0.0, 4.0)
    P = g.polar(O, 4.0, 60)
    r = 2 * R3 - 2
    fig, ax = g.canvas(6, -0.67, 4.63)
    g.seg(ax, O, A)
    g.seg(ax, O, B)
    g.arc(ax, O, 4.0, 0, 90)
    g.seg(ax, A, P)
    g.circle(ax, (r, r), r)
    g.right_angle(ax, O, 1, 1)
    g.dot(ax, P)
    g.name(ax, O, "O", dx=-4, dy=-3, ha="right", va="top")
    g.name(ax, A, "A", dx=4, dy=-3, ha="left", va="top")
    g.name(ax, B, "B", dx=-4, dy=2, ha="right", va="bottom")
    g.name(ax, P, "P", dx=3, dy=4, ha="left", va="bottom")
    g.save(fig, "p17.svg")


# ── 018 — AB = BC = AD, ∠BAD = 90°인 사각형 ─────────────────────────────
# A(0, 0), B·D는 45° 아래. ∠CBD = 15°, ∠CDB = 30°, BC = 6.

def p18():
    A = (0.0, 0.0)
    B = g.polar(A, 6.0, 225)
    D = g.polar(A, 6.0, 315)
    C = g.polar(B, 6.0, -15)
    fig, ax = g.canvas(6, -6.94, 1.15)
    g.poly(ax, [A, B, C, D])
    g.seg(ax, B, D)
    g.corner_mark(ax, A, unit(A, B), unit(A, D))
    g.tick(ax, A, B, n=2)
    g.tick(ax, A, D, n=2)
    g.tick(ax, B, C, n=2)
    g.dim(ax, A, D, "6", side=1)
    g.name(ax, A, "A", dy=5, va="bottom")
    g.name(ax, B, "B", dx=-5, ha="right")
    g.name(ax, C, "C", dy=-5, va="top")
    g.name(ax, D, "D", dx=5, ha="left")
    g.save(fig, "p18.svg")


# ── 019 — 빗변 위를 움직이는 점 P ───────────────────────────────────────

def p19():
    B, C = (0.0, 0.0), (0.0, 4.0)
    A = (-4 * R3, 0.0)
    P = mid(A, C)
    fig, ax = g.canvas(6, -0.68, 4.68)
    g.poly(ax, [A, B, C])
    g.seg(ax, B, P)
    g.right_angle(ax, B, -1, 1)
    g.angle(ax, A, B, C, "$30^{\\circ}$", r=16)
    g.dim(ax, B, C, "4", side=-1)
    g.dot(ax, P)
    g.name(ax, A, "A", dx=-5, ha="right")
    g.name(ax, B, "B", dx=4, dy=-3, ha="left", va="top")
    g.name(ax, C, "C", dx=4, dy=3, ha="left", va="bottom")
    g.name(ax, P, "P", dx=-3, dy=4, ha="right", va="bottom")
    g.save(fig, "p19.svg")


# ── 020 — 밑변의 삼등분점 ───────────────────────────────────────────────

def p20():
    B, C = (0.0, 0.0), (6 * R3, 0.0)
    A = (3 * R3, 3.0)
    D = (2 * R3, 0.0)
    fig, ax = g.canvas(4, -1.11, 4.11)                     # 밑변이 길어 4칸 — 5칸이면 단 너비를 넘는다
    g.poly(ax, [A, B, C])
    g.seg(ax, A, D)
    g.angle(ax, B, C, A, "$30^{\\circ}$", r=16)
    g.tick(ax, B, A, n=2)
    g.tick(ax, A, C, n=2)
    g.dim(ax, B, A, "6", side=1)
    g.name(ax, A, "A", dy=5, va="bottom")
    g.name(ax, B, "B", dx=-5, ha="right")
    g.name(ax, C, "C", dx=5, ha="left")
    g.name(ax, D, "D", dy=-5, va="top")
    g.save(fig, "p20.svg")


# ── 021 — 두 변의 중점을 이은 선분 ──────────────────────────────────────
# DE = 8, ∠A = 45°, ∠AED = 60° → AD = 4√6, AE = 8 sin75°/sin45°. BC = 16이 가로.

def p21():
    ad = 4 * math.sqrt(6)
    ae = 8 * math.sin(math.radians(75)) / math.sin(math.radians(45))
    ab, ac = 2 * ad, 2 * ae
    x1 = (ab * ab - ac * ac + 256) / 32
    h = math.sqrt(ab * ab - x1 * x1)
    A = (0.0, 0.0)
    B, C = (-x1, -h), (16 - x1, -h)
    D, E = mid(A, B), mid(A, C)
    fig, ax = g.canvas(7, -22.03, 2.95)
    g.poly(ax, [A, B, C])
    g.seg(ax, D, E)
    g.angle(ax, A, B, C, "$45^{\\circ}$", r=14)
    g.angle(ax, E, A, D, "$60^{\\circ}$", r=12)
    g.dim(ax, B, C, "16", side=-1)
    g.name(ax, A, "A", dy=5, va="bottom")
    g.name(ax, B, "B", dx=-4, dy=-3, ha="right", va="top")
    g.name(ax, C, "C", dx=4, dy=-3, ha="left", va="top")
    g.name(ax, D, "D", dx=-5, ha="right")
    g.name(ax, E, "E", dx=5, ha="left")
    g.save(fig, "p21.svg")


# ── 022 — 정삼각형의 중선 위의 중점 ─────────────────────────────────────

def p22():
    B, C = (0.0, 0.0), (4.0, 0.0)
    A = (2.0, 2 * R3)
    D = mid(A, C)
    E = mid(B, D)
    fig, ax = g.canvas(6, -1.58, 4.3)
    g.poly(ax, [A, B, C])
    g.seg(ax, B, D)
    g.seg(ax, C, E)
    g.tick(ax, A, D, n=2)
    g.tick(ax, D, C, n=2)
    g.tick(ax, B, E)
    g.tick(ax, E, D)
    m = g.angle(ax, C, E, B, "", r=16)                 # 각이 19°라 호가 짧다. 책처럼 x는 지시선 없이 밑변 아래에
    g.name(ax, (m[0], C[1]), "$\\theta^{\\circ}$", dy=-4, va="top")   # (지시선을 호 한가운데서 내리면 호와 한 줄로 보인다 — 독립 검토)
    g.name(ax, A, "A", dy=5, va="bottom")
    g.name(ax, B, "B", dx=-4, dy=-3, ha="right", va="top")
    g.name(ax, C, "C", dx=4, dy=-3, ha="left", va="top")
    g.name(ax, D, "D", dx=5, ha="left")
    g.name(ax, E, "E", dx=-4, dy=3, ha="right", va="bottom")
    g.save(fig, "p22.svg")


# ── 023 — 서로 수직인 두 지름과 반직선 AE ───────────────────────────────

def p23():
    O = (0.0, 0.0)
    A, B, C, D = (-12.0, 0.0), (12.0, 0.0), (0.0, 12.0), (0.0, -12.0)
    E = (0.0, 8.0)
    t = 288 / 208
    F = (-12 + 12 * t, 8 * t)
    fig, ax = g.canvas(6, -16.75, 16.75)                   # 지문이 일곱 줄이라 6칸(풀 자리 8칸)
    g.circle(ax, O, 12.0)
    g.seg(ax, A, B)
    g.seg(ax, C, D)
    g.seg(ax, A, F)
    g.seg(ax, O, F)                                        # 책은 반지름 OF를 긋는다(BF가 아니다 — 독립 검토가 잡았다)
    g.right_angle(ax, O, -1, 1)
    g.dim(ax, A, O, "12", side=-1)
    center(ax, O, "O", dx=4, dy=-4, va="top")
    g.dot(ax, E)
    g.name(ax, A, "A", dx=-5, ha="right")
    g.name(ax, B, "B", dx=5, ha="left")
    g.name(ax, C, "C", dx=-1, dy=5, va="bottom")
    g.name(ax, D, "D", dy=-5, va="top")
    g.name(ax, E, "E", dx=-4, dy=2, ha="right", va="bottom")
    g.name(ax, F, "F", dx=3, dy=4, ha="left", va="bottom")
    g.save(fig, "p23.svg")


# ── 024 — ∠A를 45°와 30°로 나누는 선분 AD ───────────────────────────────
# AB = 12, AC = 8√2, ∠A = 75°. BC가 가로. BD : DC = 3 : 2.

def p24():
    ab, ac = 12.0, 8 * R2
    bc = math.sqrt(ab * ab + ac * ac - 2 * ab * ac * math.cos(math.radians(75)))
    x1 = (ab * ab - ac * ac + bc * bc) / (2 * bc)
    h = math.sqrt(ab * ab - x1 * x1)
    A = (0.0, 0.0)
    B, C = (-x1, -h), (bc - x1, -h)
    D = lerp(B, C, 0.6)
    fig, ax = g.canvas(7, -10.72, 1.48)
    g.poly(ax, [A, B, C])
    g.seg(ax, A, D)
    g.angle(ax, A, B, D, "$45^{\\circ}$", r=14)
    m = g.angle(ax, A, D, C, "", r=14)
    g.leader(ax, m, "$30^{\\circ}$", dx=0.15, dy=-1)      # AD와 AC 사이로 거의 곧게 내린다
    g.dim(ax, A, B, "12", side=-1)
    g.dim(ax, A, C, "$8\\sqrt{2}$", side=1)
    g.name(ax, A, "A", dy=5, va="bottom")
    g.name(ax, B, "B", dx=-4, dy=-3, ha="right", va="top")
    g.name(ax, C, "C", dx=4, dy=-3, ha="left", va="top")
    g.name(ax, D, "D", dy=-5, va="top")
    g.save(fig, "p24.svg")


# ── 025 — 각의 안쪽 점 A와 두 변 위의 점 P, Q ───────────────────────────

def p25():
    O = (0.0, 0.0)
    X_end = g.polar(O, 7.5, 60)
    Y_end = (8.0, 0.0)
    X, Y = g.polar(O, 6.6, 60), (7.2, 0.0)
    A = g.polar(O, 6.0, 33)
    P = g.polar(O, 4.2, 60)
    Q = (5.0, 0.0)
    fig, ax = g.canvas(7, -0.9, 6.77)
    arrow(ax, O, X_end)
    arrow(ax, O, Y_end)
    g.poly(ax, [A, P, Q])
    g.angle(ax, O, Y_end, X_end, "", r=16)                # 60° 글은 OA 점선을 피해 OY 쪽 아래 틈에
    g.name(ax, O, "$60^{\\circ}$", dx=40 * math.cos(math.radians(16.5)),
           dy=40 * math.sin(math.radians(16.5)))
    g.dashed(ax, O, A)                                     # 책처럼 OA는 점선 직선, 6cm는 그 옆에(반지름 규칙과 같다)
    g.leader(ax, lerp(O, A, 0.55), "6cm", dx=-0.4, dy=1, length=10)   # 글만 두면 OP의 길이로 읽힌다(재검토). 책도 지시선
    for p in (X, Y, A):
        g.dot(ax, p)
    g.name(ax, O, "O", dx=-4, dy=-3, ha="right", va="top")
    g.name(ax, X, "X", dx=-5, ha="right")
    g.name(ax, Y, "Y", dy=-5, va="top")
    g.name(ax, A, "A", dx=5, ha="left")
    g.name(ax, P, "P", dx=-5, ha="right")
    g.name(ax, Q, "Q", dy=-5, va="top")
    g.save(fig, "p25.svg")


# ── 026 — 관람차 ─────────────────────────────────────────────────────────
# 중심 (0, 8), 반지름 6. 책 그림의 구성을 흑백 선화로: 살 12개(0.4pt), 곤돌라 12개(테두리 원),
# A자 기둥(10% 틴트), 지면 띠. A는 꼭대기, Q는 A에서 시계 반대 방향으로 120°(210° 방향).
# 2m는 원의 아래 끝에서 치수 보조선을 오른쪽으로 뽑아 그 끝에 단다(교과서 방식).

def p26():
    M = (0.0, 8.0)
    P = (0.0, 0.0)
    A = (0.0, 14.0)
    Q = g.polar(M, 6.0, 210)
    L = (-6.0, 8.0)
    cab = 0.5                                              # 곤돌라 반지름
    fig, ax = g.canvas(6, -4.2, 17.9)                      # 지문이 길어 6칸 — 풀 자리 8칸을 지킨다
    # 지면 띠와 기둥
    ax.add_patch(Polygon([(-9.0, -0.9), (9.0, -0.9), (9.0, 0.0), (-9.0, 0.0)],
                         closed=True, facecolor=g.INK, alpha=g.TINT, edgecolor="none", gid="noedge"))
    g.seg(ax, (-9.0, 0.0), (9.0, 0.0))
    g.shade(ax, [(-0.8, 0.0), (0.8, 0.0), (0.15, 8.0), (-0.15, 8.0)])
    g.seg(ax, (-0.8, 0.0), (-0.15, 8.0))
    g.seg(ax, (0.8, 0.0), (0.15, 8.0))
    # 바퀴: 살 12개, 테, 곤돌라 12개
    for k in range(12):
        R = g.polar(M, 6.0, 90 + 30 * k)
        if k == 3:                                         # 9시 방향 살은 6m 글 자리를 비우고 두 토막으로
            g.seg(ax, M, (-1.9, 8.0), lw=g.AUX)
            g.seg(ax, (-4.1, 8.0), R, lw=g.AUX)
        else:
            g.seg(ax, M, R, lw=g.AUX)
        g.circle(ax, R, cab, lw=g.AUX)
    g.circle(ax, M, 6.0)
    g.dot(ax, M)
    # 6m: 책처럼 9시 방향 살(반지름) 위에 — 살을 글만큼 끊고 그 자리에 쓴다(반지름은 선분 + 이름).
    # 2m: 아래 끝에서 보조선을 오른쪽으로 뽑아 그 끝에 점선 곡선, 글은 옆에
    g.name(ax, (-3.0, 8.0), "6m")
    g.seg(ax, (0.0, 2.0), (2.2, 2.0), lw=g.AUX)
    g.dim(ax, (2.2, 2.0), (2.2, 0.0), "", side=1, gap=g.pt(ax, 4))
    g.name(ax, (2.2, 1.0), "2m", dx=8, ha="left")
    # P에서 Q를 올려다본 각
    g.seg(ax, P, Q)
    g.angle(ax, P, Q, (-1.0, 0.0), "$\\theta^{\\circ}$", r=16)
    for p in (A, Q, P):
        g.dot(ax, p)
    g.name(ax, A, "A", dy=10, va="bottom")
    g.name(ax, Q, "Q", dx=-10, ha="right")
    g.name(ax, P, "P", dy=-11, va="top")
    g.name(ax, (9.0, 0.0), "지면", dx=-2, dy=-11, ha="right", va="top")
    g.save(fig, "p26.svg")


# ── 027 — 평행사변형과 두 중점, 대각선 ──────────────────────────────────
# D가 원점. E = 9·(200° 방향), F = 7.5·(230° 방향)이면 DG = 6, DH = 5, ∠EDF = 30°.
# E = (A+B)/2, F = (B+C)/2, A + C = B + D에서 B = (2E + 2F − D)/3.

def p27():
    D = (0.0, 0.0)
    E = g.polar(D, 9.0, 200)
    F = g.polar(D, 7.5, 230)
    B = ((2 * E[0] + 2 * F[0]) / 3, (2 * E[1] + 2 * F[1]) / 3)
    A = (2 * E[0] - B[0], 2 * E[1] - B[1])
    C = (2 * F[0] - B[0], 2 * F[1] - B[1])
    # 밑변 BC가 가로가 되게 전체를 돌린다(책처럼)
    th = -math.atan2(C[1] - B[1], C[0] - B[0])
    rot = lambda p: (p[0] * math.cos(th) - p[1] * math.sin(th), p[0] * math.sin(th) + p[1] * math.cos(th))
    A, B, C, D, E, F = (rot(p) for p in (A, B, C, D, E, F))
    G = lerp(D, E, 2 / 3)
    H = lerp(D, F, 2 / 3)
    fig, ax = g.canvas(6, -6.85, 0.93)
    g.shade(ax, [E, F, H, G])
    g.poly(ax, [A, B, C, D])
    g.seg(ax, A, C)
    g.seg(ax, D, E)
    g.seg(ax, D, F)
    g.seg(ax, E, F)                                        # 사각형 EFHG의 변 EF — 없으면 색칠 경계 한 변이 빈다(선생님 지적)
    g.tick(ax, A, E)
    g.tick(ax, E, B)
    g.tick(ax, B, F, n=2)
    g.tick(ax, F, C, n=2)
    g.angle(ax, D, E, F, "", r=14)                        # 30°는 좁아 글을 이등분선 위 38pt에 따로 앉힌다
    bis = math.radians(215) + th
    g.name(ax, D, "$30^{\\circ}$", dx=38 * math.cos(bis), dy=38 * math.sin(bis))
    g.dim(ax, D, G, "6", side=-1)
    g.dim(ax, D, H, "5", side=1)
    g.name(ax, A, "A", dx=-4, dy=2, ha="right", va="bottom")
    g.name(ax, B, "B", dx=-4, dy=-2, ha="right", va="top")
    g.name(ax, C, "C", dx=4, dy=-2, ha="left", va="top")
    g.name(ax, D, "D", dx=4, dy=2, ha="left", va="bottom")
    g.name(ax, E, "E", dx=-5, ha="right")
    g.name(ax, F, "F", dy=-5, va="top")
    g.name(ax, G, "G", dx=-1, dy=5, va="bottom")
    g.name(ax, H, "H", dx=1, dy=-5, va="top")
    g.save(fig, "p27.svg")


# ── 028 — ∠B = 40°, AB = AC + CD인 삼각형 ───────────────────────────────
# ∠A = 60°, ∠C = 80°. b = 5, a = 5 sin80°/sin40°, BC = 5 sin60°/sin40°. BD : DC = a : b.

def p28():
    s40, s60, s80 = (math.sin(math.radians(t)) for t in (40, 60, 80))
    b = 5.0
    a = b * s80 / s40
    bc = b * s60 / s40
    B, C = (0.0, 0.0), (bc, 0.0)
    A = g.polar(B, a, 40)
    D = (bc * a / (a + b), 0.0)
    fig, ax = g.canvas(6, -0.97, 5.9)
    g.poly(ax, [A, B, C])
    g.seg(ax, A, D)
    g.angle(ax, B, C, A, "$40^{\\circ}$", r=16)
    g.angle(ax, A, B, D, "", r=12, ticks=1)
    g.angle(ax, A, D, C, "", r=12, ticks=1)
    g.dim(ax, B, A, "$a$", side=1)
    g.dim(ax, A, C, "$b$", side=1)
    g.name(ax, A, "A", dy=5, va="bottom")
    g.name(ax, B, "B", dx=-4, dy=-3, ha="right", va="top")
    g.name(ax, C, "C", dx=4, dy=-3, ha="left", va="top")
    g.name(ax, D, "D", dy=-5, va="top")
    g.save(fig, "p28.svg")


# ── 029 — 지름 AB 위의 내접사각형 ───────────────────────────────────────

def p29():
    O = (0.0, 0.0)
    A, B = (-3.0, 0.0), (3.0, 0.0)
    C = g.polar(O, 3.0, 120)
    D = g.polar(O, 3.0, 150)
    fig, ax = g.canvas(6, -3.7, 3.6)
    g.shade(ax, [A, B, C, D])
    g.circle(ax, O, 3.0)
    g.poly(ax, [A, B, C, D])
    g.angle(ax, B, C, A, "$30^{\\circ}$", r=16)
    g.tick(ax, A, D)
    g.tick(ax, D, C)
    g.dim(ax, A, O, "3", side=-1)
    center(ax, O, "O", dx=3, dy=-4, va="top")
    g.name(ax, A, "A", dx=-5, ha="right")
    g.name(ax, B, "B", dx=5, ha="left")
    g.name(ax, C, "C", dx=-2, dy=4, ha="right", va="bottom")
    g.name(ax, D, "D", dx=-5, ha="right")
    g.save(fig, "p29.svg")


# ── 030 — 34° 돌린 정사각형과 겹치는 부분 ───────────────────────────────

def p30():
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
    g.dim(ax, A, B, "10cm", side=-1)
    g.name(ax, A, "A", dx=-2, dy=-5, va="top")
    g.name(ax, B, "B", dx=4, dy=-3, ha="left", va="top")
    g.name(ax, C, "C", dx=5, ha="left")
    g.name(ax, D, "D", dx=-4, dy=-3, ha="right", va="top")    # 위쪽은 변 D'C'이 지나 그 위의 점처럼 보인다
    g.name(ax, B2, "$\\mathrm{B}'$", dx=2, dy=-5, va="top")   # 오른쪽은 변 BC가 지난다
    g.name(ax, C2, "$\\mathrm{C}'$", dy=5, va="bottom")
    g.name(ax, D2, "$\\mathrm{D}'$", dx=-5, ha="right")   # 교점 E는 지문이 부르지 않아 이름을 안 붙인다
    g.save(fig, "p30.svg")


if __name__ == "__main__":
    print("figures/")
    for fn in (p1, p2, p3, p4, p5, p6, p7, p9, p10, p11, p12, p13, p14, p15, p16, p17,
               p18, p19, p20, p21, p22, p23, p24, p25, p26, p27, p28, p29, p30):
        fn()
