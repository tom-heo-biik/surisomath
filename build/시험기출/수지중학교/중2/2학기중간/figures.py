# -*- coding: utf-8 -*-
"""시험기출 2026학년도 2학기 중간고사 수지중학교 중2의 그림.

도우미는 surisomath-grind 스킬의 grind_figure를 쓴다. build.py가 import 경로를 잡아
주므로 이 파일은 build.py로 실행한다.

    python .claude/skills/surisomath-exam/templates/build.py build/시험기출/수지중학교/중2/2학기중간/problems.yaml

기출이라 그림은 원본 시험지 그림의 구성(점의 자리, 이름, 각과 길이 표시, 색칠, 지시 화살표)을
그대로 옮기고 학생이 푼 흔적(연필 선과 글씨, 채점)은 옮기지 않는다. 모양은 문제의 조건으로
축척대로 셈하고 문제가 정하지 않는 모양은 원본 그림에 맞춰 고른다. 고른 값은 그림마다 적는다.
"""
from __future__ import annotations

import math

from matplotlib.path import Path as MPath
from matplotlib.patches import PathPatch, Polygon

import grind_figure as g

g.setup(__file__)

HEAD = 6.0            # 좌표축 화살촉 길이(pt)
TIP = 4.0             # 지시 화살표 화살촉 길이(pt). 원본의 식 이름과 각도 글에서 나온 화살표


# ── 기하 ────────────────────────────────────────────────────────────────

def dist(p, q):
    return math.hypot(q[0] - p[0], q[1] - p[1])


def unit(p, q):
    d = dist(p, q)
    return ((q[0] - p[0]) / d, (q[1] - p[1]) / d)


def lerp(p, q, t):
    return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)


def mid(p, q):
    return lerp(p, q, 0.5)


def meet(P, d, Q, e):
    """점 P를 지나 방향 d인 직선과 점 Q를 지나 방향 e인 직선의 교점."""
    den = d[0] * e[1] - d[1] * e[0]
    t = ((Q[0] - P[0]) * e[1] - (Q[1] - P[1]) * e[0]) / den
    return (P[0] + d[0] * t, P[1] + d[1] * t)


def cross(P, Q, R, S):
    """직선 PQ와 직선 RS의 교점."""
    return meet(P, (Q[0] - P[0], Q[1] - P[1]), R, (S[0] - R[0], S[1] - R[1]))


def polar(c, r, deg):
    return (c[0] + r * math.cos(math.radians(deg)), c[1] + r * math.sin(math.radians(deg)))


def foot_of(P, A, B):
    """점 P에서 직선 AB에 내린 수선의 발."""
    ux, uy = unit(A, B)
    t = (P[0] - A[0]) * ux + (P[1] - A[1]) * uy
    return (A[0] + ux * t, A[1] + uy * t)


def incircle(A, B, C):
    """내심과 내접원의 반지름. 변의 길이로 가중 평균한다."""
    a, b, c = dist(B, C), dist(C, A), dist(A, B)
    s = a + b + c
    I = ((a * A[0] + b * B[0] + c * C[0]) / s, (a * A[1] + b * B[1] + c * C[1]) / s)
    return I, abs((B[0] - A[0]) * (C[1] - A[1]) - (B[1] - A[1]) * (C[0] - A[0])) / s


def circumcenter(A, B, C):
    ax_, ay = A
    bx, by = B
    cx, cy = C
    d = 2 * (ax_ * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax_**2 + ay**2) * (by - cy) + (bx**2 + by**2) * (cy - ay) + (cx**2 + cy**2) * (ay - by)) / d
    uy = ((ax_**2 + ay**2) * (cx - bx) + (bx**2 + by**2) * (ax_ - cx) + (cx**2 + cy**2) * (bx - ax_)) / d
    return (ux, uy)


# ── 화살표 ──────────────────────────────────────────────────────────────

def _head(ax, q, ux, uy, length):
    """q 끝의 채운 화살촉. (ux, uy)는 화살이 나아가는 방향, length는 pt."""
    L = g.pt(ax, length)
    base = (q[0] - ux * L, q[1] - uy * L)
    w = L * 0.35
    ax.add_patch(Polygon([q, (base[0] - uy * w, base[1] + ux * w),
                          (base[0] + uy * w, base[1] - ux * w)],
                         closed=True, facecolor=g.INK, edgecolor="none"))
    return base


def arrow(ax, p, q, lw=g.AUX):
    """좌표축. p에서 q까지, q 끝에 채운 화살촉(길이 HEAD pt)."""
    ux, uy = unit(p, q)
    base = _head(ax, q, ux, uy, HEAD)
    g.seg(ax, p, base, lw=lw)


def pointer(ax, p, q, bend=0.0, lw=g.AUX):
    """지시 화살표. 글 쪽 p에서 가리키는 곳 q까지 보조선 굵기, q 끝에 작은 화살촉(TIP pt).
    bend는 굽는 정도(현 길이에 대한 비, 양수면 p→q 진행 방향의 왼쪽으로 부푼다). 0이면 곧은 선.
    원본 그림이 식 이름이나 각도 글에서 화살표로 가리킨 것을 옮길 때 쓴다."""
    if not bend:
        ux, uy = unit(p, q)
        base = _head(ax, q, ux, uy, TIP)
        g.seg(ax, p, base, lw=lw)
        return
    L = dist(p, q)
    nx, ny = -(q[1] - p[1]) / L, (q[0] - p[0]) / L
    c = (mid(p, q)[0] + nx * bend * L, mid(p, q)[1] + ny * bend * L)     # 2차 베지에 조절점
    ux, uy = unit(c, q)                                                  # 끝의 접선 방향
    tl = g.pt(ax, TIP)
    # 화살촉 밑까지만 곡선을 긋는다. 끝 쪽 t를 촉 길이만큼 줄인다(근사)
    t1 = max(0.0, 1.0 - tl / (2 * dist(c, q) + 1e-9))
    pts = []
    for i in range(41):
        t = t1 * i / 40
        pts.append(((1 - t) ** 2 * p[0] + 2 * (1 - t) * t * c[0] + t * t * q[0],
                    (1 - t) ** 2 * p[1] + 2 * (1 - t) * t * c[1] + t * t * q[1]))
    ax.plot([x for x, _ in pts], [y for _, y in pts], color=g.INK, linewidth=lw,
            solid_capstyle="butt")
    _head(ax, q, ux, uy, TIP)


def mid_arrow(ax, p, q, t=0.55):
    """선분 PQ 위 t 자리에 P→Q 방향의 채운 화살촉(평행 표시). 선분은 따로 긋는다."""
    ux, uy = unit(p, q)
    L = g.pt(ax, TIP + 1.0)
    tip = lerp(p, q, t)
    tip = (tip[0] + ux * L / 2, tip[1] + uy * L / 2)
    _head(ax, tip, ux, uy, TIP + 1.0)


# ── 좌표평면 ────────────────────────────────────────────────────────────

def plane(ax, x0, x1, y0, y1, o=(-3, -3, "right", "top"), yside="left"):
    """두 축과 이름. x는 오른쪽 화살촉 옆, y는 위 화살촉의 yside 쪽, O는 o=(dx, dy, ha, va)."""
    arrow(ax, (x0, 0), (x1, 0))
    arrow(ax, (0, y0), (0, y1))
    g.name(ax, (x1, 0), "$x$", dx=4, ha="left")
    if yside == "left":
        g.name(ax, (0, y1), "$y$", dx=-4, ha="right")
    else:
        g.name(ax, (0, y1), "$y$", dx=4, ha="left")
    dx, dy, ha, va = o
    g.name(ax, (0, 0), "O", dx=dx, dy=dy, ha=ha, va=va)


def line_pts(a, b, c, x0, x1):
    """직선 ax + by + c = 0 위의 두 점(x0, x1에서). b = 0이면 x = -c/a인 세로선이라 쓰지 않는다."""
    return (x0, -(a * x0 + c) / b), (x1, -(a * x1 + c) / b)


# ── 그림 ────────────────────────────────────────────────────────────────

# ── 묶음 A ────────────────────────────────────────────────────────────

CLEAR = 2.0           # 식 이름 화살표의 끝을 직선 한가운데에서 이만큼(pt) 앞에 멈춘다(기본값)
TOUCH = 0.5           # 화살 끝이 직선에 닿는다. 그래프 선(1pt)의 반 굵기


def aim(ax, target, vx, vy, clear=CLEAR):
    """식 이름의 지시 화살표. 직선 위의 점 target을 향해 (vx, vy)pt 길이로 긋고 끝을 clear pt 앞에서
    멈춘다. 끝 틈은 원본대로다. 원본을 글자 높이로 재어 pt로 옮기면 003 왼쪽은 직선에 닿고(TOUCH),
    003 오른쪽은 2.3pt, 018 아래는 2~3pt(CLEAR)에서 멈춘다. 018 위는 1단위로 재어 5.3pt이고
    식 이름의 위 끝을 y축 화살촉 높이에 맞추느라 6pt로 둔다(p018).
    화살의 시작점(글 쪽)을 돌려준다."""
    n = math.hypot(vx, vy)
    ux, uy = vx / n, vy / n
    tip = (target[0] - g.pt(ax, clear * ux), target[1] - g.pt(ax, clear * uy))
    start = (tip[0] - g.pt(ax, vx), tip[1] - g.pt(ax, vy))
    pointer(ax, start, tip)
    return start


CMEX = None           # cmex10.ttf 경로. cases_brace()가 처음 부를 때 잡는다


def _bigg():
    """cmex10의 braceleftBigg(0x28) 치수(em): 잉크 xMin, yMin, xMax, yMax와 나아가기 너비."""
    global CMEX
    from pathlib import Path
    import matplotlib
    from fontTools.ttLib import TTFont
    CMEX = Path(matplotlib.get_data_path()) / "fonts" / "ttf" / "cmex10.ttf"
    t = TTFont(str(CMEX))
    name = t.getBestCmap()[0x28]
    gl, upm = t["glyf"][name], t["head"].unitsPerEm
    return gl.xMin / upm, gl.yMin / upm, gl.xMax / upm, gl.yMax / upm, t["hmtx"][name][0] / upm


def cases_brace(ax, x, top, bot):
    """TeX cases의 왼쪽 중괄호. cmex10의 \\Bigg 중괄호(braceleftBigg) 글꼴 윤곽을 잉크가 bot부터 top까지
    (1단위 = 1pt인 캔버스) 차도록 크기를 맞춰 x에서 앉힌다. 가운데 뾰족, 양끝 말림, 굵기 변화가 글꼴
    그대로다. TeX는 12pt에서 두 줄 cases에 \\Bigg(3.0em = 36pt)를 고른다. 괄호 뒤 글이 시작할 자리
    (나아가기 너비 끝)를 돌려준다."""
    from matplotlib.font_manager import FontProperties
    from matplotlib.textpath import TextPath
    x0, y0, x1, y1, adv = _bigg()
    size = (top - bot) / (y1 - y0)                  # 이 글자 크기(pt)에서 잉크 높이가 top - bot
    ox = x - x0 * size                              # 잉크 왼끝이 x에 오게 원점을 옮긴다
    path = TextPath((ox, top - y1 * size), "(", size=size, prop=FontProperties(fname=str(CMEX)))
    ax.add_patch(PathPatch(path, facecolor=g.INK, edgecolor="none", linewidth=0))
    return ox + adv * size


def bogi_line(sx, sy, filename):
    """005 보기 ㄱ~ㄹ의 그래프 하나. 직선은 (sx, 0)과 (0, sy)를 지난다(sx, sy는 ±1, 두 절편의 부호).
    원본 넷을 절편 크기(150~180px)를 1로 재어 보니 두 절편의 크기가 같고(기울기 ±1) 축은 절편 쪽으로
    1.47~1.65, 반대쪽으로 0.36~0.7 뻗으며 직선은 두 절편 밖으로 0.3~0.38 더 나간다. 넷을 한 틀
    (L = 1.6, S = 0.5, E = 0.3)로 그려 배율과 축 길이와 선 길이가 같다. E를 0.35로 두었더니 ㄷ의
    직선 위 끝이 y 이름을 지나 0.3으로 줄이고 축을 1.6으로 늘였다. 캔버스는 3칸이고 y 범위는
    절편 쪽이 위(ㄱ, ㄷ)면 BOGI_Y, 아래(ㄴ, ㄹ)면 L - S만큼 내린 것이라 넷의 위아래 여백이 같다.
    O는 넷 다 원점 왼쪽 아래이고 원본처럼 두 축이 만나는 귀퉁이에 바짝 붙인다(1.5pt, 2pt). 머리의
    기본값(3pt, 3pt)이면 ㄹ에서 O가 내려가는 직선에 4pt까지 다가가 답답하다. 붙이면 5.8pt다."""
    L, S, E = 1.6, 0.5, 0.3
    x0, x1 = (-L, S) if sx < 0 else (-S, L)
    ya, yb = (-S, L) if sy > 0 else (-L, S)
    lo = BOGI_Y[0] if sy > 0 else BOGI_Y[0] - (L - S)
    fig, ax = g.canvas(3, lo, lo + BOGI_Y[1] - BOGI_Y[0])
    plane(ax, x0, x1, ya, yb, o=(-1.5, -2, "right", "top"))
    g.seg(ax, ((1 + E) * sx, -E * sy), (-E * sx, (1 + E) * sy), lw=g.STRING)
    g.save(fig, filename)


BOGI_Y = (-0.72, 1.99)  # 절편 쪽이 위인 보기 그림(ㄱ, ㄷ)의 y 범위. 아래인 것(ㄴ, ㄹ)은 L - S만큼 내린다


# ── 그림 ────────────────────────────────────────────────────────────────

def p003():
    """003. 두 직선 2x+y-p=0, 3x-y+q=0과 두 축의 교점 A, B, C, D.

    A(p/2, 0), B(-q/3, 0), C(0, p), D(0, q)이다. 4AO = 3BO에서 4 × (p/2) = 3 × (q/3), 곧 q = 2p이고
    CD = q - p = 3이라 p = 3, q = 6(답 ⑤ p+q = 9).
    2x+y-3=0은 y = 3-2x로 A(1.5, 0), C(0, 3)을 지나 내려가고 3x-y+6=0은 y = 3x+6으로
    B(-2, 0), D(0, 6)을 지나 올라간다. 두 직선은 (-0.6, 4.2)에서 만난다.
    원본은 가로를 늘여 그렸다(OB 280px, OA 155px인데 OC 211px, OD 392px). 여기서는 참값이다.
    정하지 않는 모양은 원본을 따른다. 두 직선은 x축 아래 1(y = -1)에서 D 위 1(y = 7)까지 뻗고
    y축은 -1에서 7.5까지, x축은 -2.9에서 2.9까지다. y축 화살촉을 직선 끝보다 0.5 올려 올라가는
    직선의 끝(1/3, 7)이 화살촉에 붙지 않게 했다(원본은 둘이 같은 높이).
    이름: A는 x축 아래 교점 왼쪽, B는 아래 오른쪽, C는 y축 오른쪽 교점 높이, D는 y축 오른쪽 교점
    바로 아래, O는 원점 왼쪽 아래(원본). 식 이름은 원본처럼 3x-y+q=0이 왼쪽에서 오른쪽 아래로,
    2x+y-p=0이 오른쪽에서 왼쪽 아래로 화살표를 내려 두 직선의 y = 1.9 자리를 가리킨다. 원본은
    y ≈ 2.2이지만 참값으로 좁아진 그림에서 오른쪽 식 이름이 C와 한 줄로 붙어 읽혀 조금 내리고
    화살표를 가로로 늘였다. 오른쪽 식 이름이 왼쪽 것보다 조금 높은 것은 원본대로다.
    화살 끝은 원본대로 왼쪽이 직선에 닿고(TOUCH) 오른쪽이 2pt 앞에서 멈춘다.
    """
    A, B, C, D = (1.5, 0.0), (-2.0, 0.0), (0.0, 3.0), (0.0, 6.0)
    top, bot = 7.0, -1.0
    fig, ax = g.canvas(6, -1.41, 8.20)
    plane(ax, -2.9, 2.9, -1.0, 7.5)
    g.seg(ax, ((bot - 6) / 3, bot), ((top - 6) / 3, top), lw=g.STRING)     # 3x - y + 6 = 0
    g.seg(ax, ((3 - top) / 2, top), ((3 - bot) / 2, bot), lw=g.STRING)     # 2x + y - 3 = 0
    g.name(ax, A, "A", dx=-1, dy=-3, ha="right", va="top")
    g.name(ax, B, "B", dx=1, dy=-3, ha="left", va="top")
    g.name(ax, C, "C", dx=3, dy=1, ha="left")
    g.name(ax, D, "D", dx=3, dy=-1, ha="left", va="top")
    yl = 1.9
    s = aim(ax, ((yl - 6) / 3, yl), 13, -5, clear=TOUCH)
    g.name(ax, s, "$3x-y+q=0$", dx=-2, dy=1, ha="right")
    s = aim(ax, ((3 - yl) / 2, yl), -14, -8)
    g.name(ax, s, "$2x+y-p=0$", dx=2, dy=2, ha="left")
    g.save(fig, "p003.svg")


def p004s():
    """004. 지문 안의 연립방정식(별행 수식). 2칸(44pt) 블록.

    mathtext에 cases가 없어 figures.py가 그린다. 두 식은 본문과 같은 12pt Computer Modern이고
    원본처럼 왼끝을 맞춘다(등호를 맞추지 않는다). 베이스라인은 블록 위 끝에서 14.4pt와 36.4pt라
    본문 글줄과 같은 위상이다(캔버스는 1단위 = 1pt, 아래에서 29.6pt와 7.6pt).
    중괄호는 cmex10의 \\Bigg 중괄호 윤곽이다(cases_brace). 두 줄의 수식 축(베이스라인 위 0.25em =
    3pt)의 한가운데(아래에서 21.6pt)에 가운데를 두고 잉크 높이 34pt(4.6~38.6pt)로 맞췄다. TeX가
    고르는 \\Bigg는 36pt라 위아래 여백 4pt 안에 안 들어 글자 크기 11.3pt로 줄였다. 괄호 뒤 글은
    TeX처럼 괄호의 나아가기 너비 끝에서 시작한다."""
    fig, ax = g.canvas(2, 0.0, 44.0)
    b1, b2 = 44.0 - 14.4, 44.0 - 36.4
    mid = ((b1 + 3.0) + (b2 + 3.0)) / 2
    x = cases_brace(ax, 0.0, mid + 17.0, mid - 17.0)
    g.label(ax, x, b1, "$mx-6y=6$", ha="left", va="baseline", size=12)
    g.label(ax, x, b2, "$x-3y=-12$", ha="left", va="baseline", size=12)
    g.save(fig, "p004s.svg")


def p005():
    """005. 직선 ax-by+c/a=0의 그래프. 4칸.

    기울기가 음수이고 x절편과 y절편이 양수다. 원본을 재면 두 절편이 314px, 323px로 거의 같아
    y = 1 - x(두 절편 1)로 그린다. 축은 원점에서 x는 -0.4~1.74, y는 -0.4~1.64이고 직선은
    x = -0.45(y = 1.45)에서 x = 1.42(y = -0.42)까지다(원본의 축 길이와 직선 끝을 절편 1로 잰 값).
    O는 원점 왼쪽 아래."""
    fig, ax = g.canvas(4, -0.58, 1.91)
    plane(ax, -0.40, 1.74, -0.40, 1.64)
    g.seg(ax, (-0.45, 1.45), (1.42, -0.42), lw=g.STRING)
    g.save(fig, "p005.svg")


def p005a():
    """005 보기 ㄱ. 올라가는 직선, x절편 음, y절편 양(원점이 그림 오른쪽 아래). y = x + 1."""
    bogi_line(-1, 1, "p005a.svg")


def p005b():
    """005 보기 ㄴ. 올라가는 직선, x절편 양, y절편 음(원점이 왼쪽 위). y = x - 1."""
    bogi_line(1, -1, "p005b.svg")


def p005c():
    """005 보기 ㄷ. 내려가는 직선, 두 절편 양(원점이 왼쪽 아래). y = -x + 1."""
    bogi_line(1, 1, "p005c.svg")


def p005d():
    """005 보기 ㄹ. 내려가는 직선, 두 절편 음(원점이 오른쪽 위). y = -x - 1."""
    bogi_line(-1, -1, "p005d.svg")


def p018():
    """018. 두 직선 x+ay-10=0, x+y+b=0. 7칸.

    x+y+b=0의 y절편이 4라 b = -4, 두 직선의 교점은 x좌표 6이라 (6, -2)이고
    6 - 2a - 10 = 0에서 a = -2(답 a+b = -6). x+y-4=0은 y = 4 - x로 내려가고(x절편 4),
    x-2y-10=0은 y = (x-10)/2로 올라간다(x절편 10, y절편 -5).
    원본은 축척대로다(가로 45.5px, 세로 44.5px가 1). 원본을 재어 옮긴 모양: 내려가는 직선은
    x = -4(y = 8)에서 x = 14.6(y = -10.6)까지, 올라가는 직선은 x = -4(y = -7)에서
    x = 24.5(y = 7.25)까지, x축은 -4.1에서 24.4까지, y축은 -10.4에서 9.7까지.
    y축의 4는 교점 오른쪽 위, x축의 6은 축 위, (6, 0)에서 교점까지 점선, O는 원점 왼쪽 아래.
    식 이름은 원본처럼 x+ay-10=0이 오른쪽 위에서 곧게 아래로(올라가는 직선의 x = 18.9 자리),
    x+y+b=0이 오른쪽 아래에서 왼쪽 아래로(내려가는 직선의 x = 13.9 자리) 가리킨다.
    위 식 이름은 원본처럼 글자 위 끝이 y축 화살촉과 같은 높이다. 원본을 1단위로 재면 직선에서
    화살 끝까지 5.3pt, 화살 14.3pt, 화살 밑에서 글 베이스라인까지 6.7pt이고 글자 높이가 9.1pt다.
    우리 글자는 6.4pt라 그대로 옮기면 글 위 끝이 화살촉보다 3.4pt 낮아진다. 그래서 세 칸을 같은
    비(1.1배)로 늘려 6pt, 16pt, 6.8pt(dy 4.5)로 둔다. 크롭을 재면 글 위 끝이 화살촉보다 0.5pt 낮다(원본도 0.5pt).
    아래 화살은 2pt 앞에서 멈춘다(원본 2~3pt)."""
    fall = lambda x: 4 - x
    rise = lambda x: (x - 10) / 2
    fig, ax = g.canvas(7, -11.41, 11.11)
    plane(ax, -4.1, 24.4, -10.4, 9.7)
    g.seg(ax, (-4.0, fall(-4.0)), (14.6, fall(14.6)), lw=g.STRING)
    g.seg(ax, (-4.0, rise(-4.0)), (24.5, rise(24.5)), lw=g.STRING)
    g.dashed(ax, (6.0, 0.0), (6.0, -2.0))
    g.name(ax, (0.0, 4.0), "4", dx=3, dy=2, ha="left")
    g.name(ax, (6.0, 0.0), "6", dy=3, va="bottom")
    s = aim(ax, (18.9, rise(18.9)), 0, -16, clear=6.0)
    g.name(ax, s, "$x+ay-10=0$", dy=4.5, va="bottom")
    s = aim(ax, (13.9, fall(13.9)), -14, -7.5)
    g.name(ax, s, "$x+y+b=0$", dx=2, dy=3, ha="left")
    g.save(fig, "p018.svg")

# ── 묶음 B ────────────────────────────────────────────────────────────

def pointer3(ax, p, c1, c2, q, lw=g.AUX):
    """3차 베지에 지시 화살표. p에서 q까지 조절점 c1, c2로 굽고 q 끝에 TIP pt 화살촉.
    시작과 끝의 접선을 따로 정하므로 글 아래로 곧게 내려오다 옆으로 꺾여 다시 곧게 가리키는
    갈고리 꼴(007)이나 곧게 내려오다 끝에서 비스듬히 꺾이는 꼴(006)을 옮길 수 있다.
    곡선은 화살촉 밑까지만 긋고 화살촉은 그 끝에서 q를 향한다."""
    def bez(t):
        s = 1 - t
        return (s ** 3 * p[0] + 3 * s * s * t * c1[0] + 3 * s * t * t * c2[0] + t ** 3 * q[0],
                s ** 3 * p[1] + 3 * s * s * t * c1[1] + 3 * s * t * t * c2[1] + t ** 3 * q[1])
    tl = g.pt(ax, TIP)
    lo, hi = 0.0, 1.0                          # q에서 촉 길이만큼 떨어진 t(이분법)
    for _ in range(50):
        t = (lo + hi) / 2
        if dist(bez(t), q) > tl:
            lo = t
        else:
            hi = t
    pts = [bez(lo * i / 80) for i in range(81)]
    ax.plot([x for x, _ in pts], [y for _, y in pts], color=g.INK, linewidth=lw,
            solid_capstyle="butt")
    _head(ax, q, *unit(pts[-1], q), TIP)


def callout3(ax, at, text, tip, d1, d2, dx=0.0):
    """원본의 '글에서 나온 지시 화살표'. at(글의 가운데)에 글을 두고, 글 아래 1.5pt에서 tip까지
    pointer3로 잇는다. dx는 화살표가 글 가운데에서 가로로 비키는 양(pt).
    d1은 시작점에서 첫 조절점까지, d2는 tip에서 둘째 조절점까지의 벡터(pt)다."""
    g.label(ax, at[0], at[1], text)
    _, h = g.text_size(ax, text)
    start = (at[0] + g.pt(ax, dx), at[1] - g.pt(ax, h / 2 + 1.5))
    c1 = (start[0] + g.pt(ax, d1[0]), start[1] + g.pt(ax, d1[1]))
    c2 = (tip[0] + g.pt(ax, d2[0]), tip[1] + g.pt(ax, d2[1]))
    pointer3(ax, start, c1, c2, tip)


# ── 006. 변 AC 위의 점 D. BD = BC ───────────────────────────────────────

def p006():
    """삼각형 ABC와 변 AC 위의 점 D, 선분 BD. 원본처럼 B 왼쪽, C 오른쪽 아래(BC 가로), A 위.

    모양은 각으로 정한다. ∠A = 62°, ∠C = 80°라 ∠B = 38°, ∠ABD = 18°라 ∠DBC = 20°,
    ∠BDC = 180° − 20° − 80° = 80° = ∠C라 BD = BC다.
    크기는 둘레 30에서 셈했다. 사인법칙으로 BC : CA : AB = sin62° : sin38° : sin80°라
    BC = 10.666, CA = 7.437, AB = 11.896이다.
    B(0, 0), C(10.666, 0), A는 B에서 38° 방향으로 AB만큼인 (9.375, 7.324),
    D는 B에서 20° 방향으로 BD = BC만큼인 (10.023, 3.648)이다(변 AC 위).
    이 모양에서 CD = BC×sin20°/sin80° = 3.704라 지문의 CD = 4와 조금 어긋난다. 네 각과
    둘레 30과 CD = 4를 한꺼번에 맞추는 삼각형은 없고, 문제는 BD = BC만 쓰므로 모양은 각을 따랐다.

    원본의 표시: A의 호와 62°(각 안), C의 호와 80°(각 안), B의 ∠ABD 호(글 없음)와 BA 위
    바깥의 18°에서 그 각을 가리키는 화살표, CD 오른쪽의 점선 곡선과 4.
    호의 반지름은 원본의 비(BC에 대해 A와 C는 0.08, B는 0.17)를 따라 12pt, 12pt, 26pt.
    18°의 자리와 화살표는 원본 사진을 이 그림에 닮음 변환으로 겹쳐 잰 값이다. 글 가운데는 B에서
    (32.7pt, 40.5pt). 화살표는 '8'의 왼쪽 아래에서 거의 곧게 내려와 BA를 건너고 끝에서 왼쪽으로
    꺾여 촉이 왼쪽 아래(연직에서 34°)를 가리킨다. 촉 끝은 ∠ABD의 이등분선(29°) 위 29pt로
    호 바로 바깥이다. 3차 베지에(callout3)의 조절 벡터 (−1.1, −17.5), (5.1, 7.4)pt는 원본의
    줄기와 촉 밑 네 점에 맞춘 값이다(어긋남 0.1pt 안).
    C는 원본처럼 꼭짓점 바로 오른쪽이다(글 가운데가 2pt 아래)."""
    sA, sB, sC = (math.sin(math.radians(d)) for d in (62, 38, 80))
    k = 30.0 / (sA + sB + sC)
    a, c = k * sA, k * sC                          # BC, AB
    B, C = (0.0, 0.0), (a, 0.0)
    A = polar(B, c, 38)
    D = polar(B, a, 20)                            # BD = BC
    fig, ax = g.canvas(6, -1.26, 8.65)
    g.poly(ax, [A, B, C])
    g.seg(ax, B, D)
    g.angle(ax, A, B, C, "$62^{\\circ}$", r=12)
    g.angle(ax, C, A, B, "$80^{\\circ}$", r=12)
    g.angle(ax, B, D, A, "", r=26)                 # ∠ABD. 글은 원본처럼 바깥에서 화살표로
    callout3(ax, (g.pt(ax, 32.7), g.pt(ax, 40.5)), "$18^{\\circ}$", polar(B, g.pt(ax, 29), 29),
             (-1.1, -17.5), (5.1, 7.4), dx=-2.3)
    g.dim(ax, D, C, "4", side=1)                   # D→C의 왼쪽이 바깥(오른쪽)
    g.name(ax, A, "A", dy=4, va="bottom")
    g.name(ax, B, "B", dx=-3, dy=-2, ha="right")
    g.name(ax, C, "C", dx=3, dy=-2, ha="left")     # 원본처럼 C 바로 오른쪽(가운데가 2pt 아래)
    g.name(ax, D, "D", dx=4, dy=2, ha="left", va="bottom")
    g.save(fig, "p006.svg")


# ── 007. 각 A의 이등분선 AD와 색칠한 삼각형 ADE ─────────────────────────

def p007():
    """∠B = 90°인 직각삼각형 ABC(AB 세로, BC 가로), ∠A의 이등분선 AD, 변 AC 위의 점 E,
    색칠한 삼각형 ADE.

    지문의 조건은 서로 어긋난다. △ADE = 10이고 AE : AC = 1 : 4라 △ADC = 40, 곧 DC×AB = 80이다.
    각의 이등분선의 성질로 AB : AC = BD : DC = 5 : DC라 AC = AB×DC/5 = 16이다(정답 CE = 12는
    여기서 나온다). 그런데 AC = 16인 직각삼각형에서 BD = BC×AB/(AB + AC)는 최대 4.8쯤이라
    BD = 5가 될 수 없다.
    그래서 AC = 16을 지키고 원본 생김새(AB/BC ≈ 0.63, BD/BC ≈ 0.35)에 맞춰 AB = 8.5를 골랐다.
    BC = √(16² − 8.5²) = 13.555, BD = 13.555 × 8.5/24.5 = 4.703, AE = 4라 E = A + (C − A)/4.
    이 모양에서 △ADE = 9.41이다.
    B(0, 0), A(0, 8.5), C(13.555, 0), D(4.703, 0), E(3.389, 6.375).

    원본의 표시: B의 직각, A의 같은 두 각에 점(A에서 21pt), BD 아래 점선 곡선과 5,
    AC 위 바깥의 10에서 AC를 건너 삼각형 ADE 안을 가리키는 굽은 화살표(넓이 10).
    색칠은 규칙대로 10%(원본은 진한 회색 망점).
    10과 화살표는 원본 사진을 이 그림에 닮음 변환으로 겹쳐 잰 값이다. 글 가운데는 A에서
    (35.5pt, 7.5pt). 화살표는 '1' 아래에서 곧게 내려오다 AC 바로 위에서 왼쪽으로 갈고리처럼
    꺾여 AC를 건너고 다시 거의 곧게 내려가 촉이 아래(연직에서 6°)를 가리킨다. 촉 끝은
    A에서 (24.1pt, −31.5pt). 3차 베지에(callout3)의 조절 벡터 (0, −30), (3.55, 31.8)pt는
    원본의 줄기와 갈고리 아홉 점에 맞춘 값이다(어긋남 0.4pt 안)."""
    AB, AC = 8.5, 16.0
    BC = math.sqrt(AC ** 2 - AB ** 2)
    B, A, C = (0.0, 0.0), (0.0, AB), (BC, 0.0)
    D = (BC * AB / (AB + AC), 0.0)
    E = lerp(A, C, 0.25)
    fig, ax = g.canvas(6, -1.76, 10.08)
    g.shade(ax, [A, D, E])
    g.poly(ax, [A, B, C])
    g.seg(ax, A, D)
    g.seg(ax, D, E)
    g.right_angle(ax, B, 1, 1)
    g.angle(ax, A, B, D, "", r=21, ticks=1)
    g.angle(ax, A, D, C, "", r=21, ticks=1)
    g.dim(ax, B, D, "5", side=-1)
    tip = (A[0] + g.pt(ax, 24.1), A[1] - g.pt(ax, 31.5))
    callout3(ax, (A[0] + g.pt(ax, 35.5), A[1] + g.pt(ax, 7.5)), "10", tip, (0, -30), (3.55, 31.8),
             dx=-3.1)
    g.name(ax, A, "A", dx=-1, dy=4, va="bottom")
    g.name(ax, B, "B", dx=-3, dy=-3, ha="right", va="top")
    g.name(ax, C, "C", dx=3, dy=-3, ha="left", va="top")
    g.name(ax, D, "D", dx=2, dy=-4, ha="left", va="top")
    g.name(ax, E, "E", dx=2, dy=4, ha="left", va="bottom")
    g.save(fig, "p007.svg")


# ── 008. 외심 O, ∠ABO와 ∠BOC ───────────────────────────────────────────

def p008():
    """삼각형 ABC와 외심 O, 선분 OB, OC. 원본처럼 BC 가로, A 위(B 쪽으로 치우침).

    OA = OB = OC라 ∠OAB = ∠OBA = 52°, ∠BOC = 136°에서 ∠OBC = ∠OCB = 22°,
    ∠AOB = 180° − 104° = 76°라 ∠ACB = 38°, ∠OCA = ∠OAC = 16°다.
    그래서 ∠A = 68°, ∠B = 74°, ∠C = 38°.
    B(0, 0), C(10, 0), A는 B에서 74° 방향으로 AB = 10×sin38°/sin68° = 6.640인 (1.830, 6.383),
    O는 BC의 수직이등분선 위 (5, 5×tan22°) = (5, 2.020).

    원본의 표시: B의 호와 52°(∠ABO), O의 호와 136°(∠BOC, O 아래), C의 ∠ACO에 글 없는 호
    (묻는 각). 호의 반지름은 원본의 비(BC에 대해 B 0.125, O 0.09, C 0.2)를 따라 20pt, 15pt, 32pt.
    원본 사진의 선분 OA는 학생이 그은 것이라 옮기지 않는다. 인쇄한 선은 토너 가장자리가
    오돌토돌한데 OA는 학생의 x 글씨와 같은 매끈한 펜 선이고 O를 지나 삐져나간다.
    B와 C의 이름은 원본처럼 꼭짓점의 옆이다(B는 왼쪽, C는 오른쪽. 글 가운데가 3pt, 2pt 아래)."""
    B, C = (0.0, 0.0), (10.0, 0.0)
    A = polar(B, 10 * math.sin(math.radians(38)) / math.sin(math.radians(68)), 74)
    O = (5.0, 5 * math.tan(math.radians(22)))
    fig, ax = g.canvas(6, -1.09, 7.54)
    g.poly(ax, [A, B, C])
    g.seg(ax, O, B)
    g.seg(ax, O, C)
    g.angle(ax, B, O, A, "$52^{\\circ}$", r=20)
    g.angle(ax, O, B, C, "$136^{\\circ}$", r=15)
    g.angle(ax, C, A, O, "", r=32)                 # ∠ACO. 원본처럼 글 없는 호
    g.dot(ax, O)
    g.name(ax, O, "O", dy=4, va="bottom")
    g.name(ax, A, "A", dx=-1, dy=4, va="bottom")
    g.name(ax, B, "B", dx=-3, dy=-3, ha="right")   # 원본처럼 B 왼쪽(가운데가 3pt 아래)
    g.name(ax, C, "C", dx=3, dy=-2, ha="left")     # 원본처럼 C 바로 오른쪽(가운데가 2pt 아래)
    g.save(fig, "p008.svg")


# ── 009. 두 삼각형의 외심 O, BC ∥ OD ───────────────────────────────────

def p009():
    """삼각형 ABC와 점 D, 외심 O에서 B와 D로 선분, 선분 BD, CD. OD와 BC가 평행(화살촉).

    O(0, 0)과 외접원의 반지름 R = 5로 짓는다. ∠A = 56°라 ∠BOC = 112°이고 OB = OC라
    ∠OBC = ∠OCB = 34°다. BC를 가로로 두면 B는 214°, C는 326° 방향이다.
    D는 외접원 위에서 OD ∥ BC인 점이라 O와 같은 높이 오른쪽 (R, 0)이다(원본처럼 오른쪽).
    A는 문제가 정하지 않아 원본처럼 107° 방향에 두었다(원본에서 잰 값).
    B(−4.145, −2.796), C(4.145, −2.796), D(5, 0), A(−1.462, 4.782).

    원본의 표시: A의 호와 56°, O의 ∠BOD에 글 없는 호(묻는 각. OB에서 O 아래를 돌아 OD까지),
    OD와 BC 위 오른쪽 화살촉(원본 자리 t = 0.52, 0.57), O의 점과 이름.
    호의 반지름은 원본의 비(R에 대해 A 0.19, O 0.14)를 따라 15pt, 11pt(7칸에서 R = 79pt).
    원본 사진의 선분 OC 두 줄(하나는 구불구불), ∠BOD 호 아래 112, B 옆과 C 옆과 OC 위의
    점 셋은 학생이 그은 것이라 옮기지 않는다. 인쇄한 선(OB, OD, BD, CD, 삼각형의 변)은 토너
    가장자리가 오돌토돌한데 OC 두 줄은 매끈한 펜 선이고 C를 지나 BC 아래로 삐져나간다.
    C의 이름은 원본처럼 꼭짓점 바로 오른쪽이다(글 가운데가 2pt 아래)."""
    R = 5.0
    O = (0.0, 0.0)
    A, B, C, D = polar(O, R, 107), polar(O, R, 214), polar(O, R, 326), (R, 0.0)
    fig, ax = g.canvas(7, -3.84, 5.91)
    g.poly(ax, [A, B, C])
    g.seg(ax, O, B)
    g.seg(ax, O, D)
    g.seg(ax, B, D)
    g.seg(ax, C, D)
    mid_arrow(ax, O, D, t=0.52)
    mid_arrow(ax, B, C, t=0.57)
    g.angle(ax, A, B, C, "$56^{\\circ}$", r=15)
    g.angle(ax, O, B, D, "", r=11)                 # ∠BOD. 원본처럼 글 없는 호
    g.dot(ax, O)
    g.name(ax, O, "O", dy=4, va="bottom")
    g.name(ax, A, "A", dy=4, va="bottom")
    g.name(ax, B, "B", dx=-3, dy=-2, ha="right")
    g.name(ax, C, "C", dx=3, dy=-2, ha="left")     # 원본처럼 C 바로 오른쪽(가운데가 2pt 아래)
    g.name(ax, D, "D", dx=4, ha="left")
    g.save(fig, "p009.svg")

# ── 묶음 C ────────────────────────────────────────────────────────────

def p010():
    """010. 내접원 I와 접점 D, E, F, 사각형 BEID 색칠.

    접선 길이로 AD = AF = 5, BD = BE = 8, CE = CF = 6이라 AB = 13, BC = 14, CA = 11이다. 이 세 변으로
    그린다. 지문의 넓이 76은 세 변과 어긋난다(헤론으로 √(19×6×5×8) = √4560 ≈ 67.53). 그림은 세 변을
    따르고 넓이는 따르지 않는다. B(0, 0), C(14, 0), A(61/7, √(169 − (61/7)²)) ≈ (8.714, 9.647).
    내심 I(8, r), r = 67.53/19 ≈ 3.554. E(8, 0), D는 B에서 AB로 8, F는 C에서 CA로 6.
    원본 그림의 인쇄된 표시: 13은 AB 왼쪽 바깥, 11은 AC 오른쪽 바깥의 점선 곡선(A에서 B, A에서 C까지),
    6은 EC 아래의 점선 곡선. 사각형 BEID 색칠, 선분 ID, IE, 점 I. 5, 8, 14와 B에서 I로 그은 선은
    학생 것이라 옮기지 않는다."""
    B, C = (0.0, 0.0), (14.0, 0.0)
    ax_ = 244 / 28
    A = (ax_, math.sqrt(169 - ax_ * ax_))
    I, r = incircle(A, B, C)
    E = (I[0], 0.0)
    D = lerp(B, A, 8 / 13)
    F = lerp(C, A, 6 / 11)
    f, ax = g.canvas(6, -2.2, 11.6)
    g.shade(ax, [B, E, I, D])
    g.poly(ax, [A, B, C])
    g.circle(ax, I, r)
    g.seg(ax, I, D)
    g.seg(ax, I, E)
    g.dot(ax, I)
    g.dim(ax, B, A, "13", side=1, gap=g.pt(ax, 22))
    g.dim(ax, A, C, "11", side=1, gap=g.pt(ax, 22))
    g.dim(ax, E, C, "6", side=-1)
    g.name(ax, I, "I", dx=4, dy=1, ha="left")
    g.name(ax, A, "A", dy=5, va="bottom")
    g.name(ax, B, "B", dx=-4, dy=-2, ha="right", va="top")
    g.name(ax, C, "C", dx=4, dy=-2, ha="left", va="top")
    g.name(ax, D, "D", dx=-4, dy=3, ha="right", va="bottom")
    g.name(ax, E, "E", dy=-5, va="top")
    g.name(ax, F, "F", dx=4, dy=3, ha="left", va="bottom")
    g.save(f, "p010.svg")


def p011():
    """011. 내심 I와 세 각의 이등분선 CD, AE, BF.

    ∠AFB = 180° − A − B/2 = 78°, ∠BCD = C/2 = 20°에서 C = 40°, A + B/2 = 102°, A + B = 140°라
    A = 64°, B = 76°, C = 40°. BC = 10으로 B(0, 0), C(10, 0), A = B + AB(cos 76°, sin 76°),
    AB = 10 sin 40°/sin 64° ≈ 7.152. D는 CI와 AB, E는 AI와 BC, F는 BI와 AC의 교점.
    원본 그림의 인쇄된 표시: F의 각 AFB에 호와 78°, C의 각 BCD에 호와 20°, 점 I. A의 두 동그라미(한쪽은
    펜 획의 꼬리가 있다)와 B의 x 둘, D와 E의 호, 40, 30, 102, 58, 20, x, y는 학생 것이라 옮기지 않는다."""
    A_, B_, C_ = 64.0, 76.0, 40.0
    s = math.sin
    rad = math.radians
    B, C = (0.0, 0.0), (10.0, 0.0)
    ab = 10 * s(rad(C_)) / s(rad(A_))
    A = polar(B, ab, B_)
    I, _ = incircle(A, B, C)
    D = cross(C, I, A, B)
    E = cross(A, I, B, C)
    F = cross(B, I, A, C)
    f, ax = g.canvas(6, -1.6, 8.4)
    g.poly(ax, [A, B, C])
    g.seg(ax, C, D)
    g.seg(ax, A, E)
    g.seg(ax, B, F)
    g.dot(ax, I)
    g.angle(ax, F, A, B, "$78^{\\circ}$", r=11)           # 글이 선분 AE에 붙지 않게
    g.angle(ax, C, D, B, "$20^{\\circ}$", r=28)           # 좁은 각. 원본처럼 호를 멀리 두고 글은 호 왼쪽
    g.name(ax, I, "I", dx=-2, dy=-6, va="top")
    g.name(ax, A, "A", dy=5, va="bottom")
    g.name(ax, B, "B", dx=-4, dy=-2, ha="right", va="top")
    g.name(ax, C, "C", dx=4, dy=-2, ha="left", va="top")
    g.name(ax, D, "D", dx=-4, ha="right")
    g.name(ax, E, "E", dy=-5, va="top")
    g.name(ax, F, "F", dx=3, dy=3, ha="left", va="bottom")
    g.save(f, "p011.svg")


def p012():
    """012. 직각삼각형(B 직각)의 내심 I와 빗변의 중점 M.

    ∠A = 70°, ∠C = 20°. B(0, 0), C(10, 0), A(0, 10/tan 70°) ≈ (0, 3.640). 내심 I(r, r),
    r = (AB + BC − AC)/2 ≈ 1.499. M은 AC의 중점(5, 1.820). ∠IBM = 45° − 20° = 25°.
    원본 그림의 인쇄된 표시: A의 호와 70°, AM과 MC의 획 둘, B의 직각 표시, 선분 BI, BM, 점 I.
    I에서 M, C로 가는 구불구불한 선, A에서 I로 그은 선, B의 큰 호와 A의 바깥 호, 35, 25, 45, 20, 10은
    학생 것이라 옮기지 않는다."""
    B, C = (0.0, 0.0), (10.0, 0.0)
    A = (0.0, 10 / math.tan(math.radians(70)))
    I, r = incircle(A, B, C)
    M = mid(A, C)
    f, ax = g.canvas(5, -0.9, 4.7)
    g.poly(ax, [A, B, C])
    g.seg(ax, B, I)
    g.seg(ax, B, M)
    g.dot(ax, I)
    g.right_angle(ax, B, 1, 1)
    g.tick(ax, A, M, 2)
    g.tick(ax, M, C, 2)
    g.angle(ax, A, B, C, "$70^{\\circ}$", r=10)
    g.name(ax, I, "I", dy=5, va="bottom")
    g.name(ax, M, "M", dx=2, dy=5, va="bottom")
    g.name(ax, A, "A", dy=5, va="bottom")
    g.name(ax, B, "B", dx=-4, dy=-2, ha="right", va="top")
    g.name(ax, C, "C", dx=4, ha="left")
    g.save(f, "p012.svg")


def p013():
    """013. 이등변삼각형(AB = AC)의 외심 O와 내심 I, O에서 AB, AC에 내린 수선의 발 D, E.

    꼭지각은 원본 사진(원해상도)에서 재어 43°로 골랐다. 변 AB, AC, BC와 선분 OB, OC, IB, IC를 직선으로
    맞추고 교점으로 A, O, I를 잡았다. 점에서 BC까지의 거리 ÷ 높이는 삼각형의 무게중심 좌표라 사진의
    가로세로 찌그러짐에 흔들리지 않는다. 이등변삼각형(꼭지각 2α)에서 O는 cos 2α/(1 + cos 2α),
    I는 sin α/(1 + sin α)이다. 원본에서 O 0.426 → 42.0°, I 0.277 → 45.1°, 차 OI 0.149 → 43.6°이고
    둘을 함께 맞추면 43.7°다. 43°와 44°가 이 폭 안에서 같이 가까운데(이 배율에서 O, I 자리가 원본과
    0.8pt 안) 43°라야 O 이름이 O 점, I 점, 선분 OB, OC에서 모두 0.8pt 남짓 떨어진다. 44°는 0.55pt,
    45°는 이름 O의 아래가 I 점에 닿았다. 높이와 밑변의 반의 비로 재면 46°가 나오지만 가로와 세로를
    섞은 비라 사진의 찌그러짐을 탄다. 밑각은 68.5°.
    B(−1, 0), C(1, 0), A(0, 1/tan 21.5°) ≈ (0, 2.539). 외심 O(0, h − R), R = 1/sin 43° ≈ 1.466이라
    O ≈ (0, 1.072). 내심 I(0, tan 34.25°) ≈ (0, 0.681). O가 I 위다(꼭지각이 60°보다 작다).
    D, E는 O에서 내린 수선의 발이라 AB, AC의 중점이다.
    원본 그림의 인쇄된 표시: 선분 AO, OD, OE, OB, OC, IB, IC, 점 O, I, D와 E의 직각 표시(A 쪽). O의 이름은
    O와 I 사이. A의 두 점, B와 C의 점과 x, AO와 OB, OC 위의 획, D와 E 아래의 ㄴ 꼴, 4는 학생 것이라
    옮기지 않는다."""
    half = math.radians(21.5)
    B, C = (-1.0, 0.0), (1.0, 0.0)
    A = (0.0, 1 / math.tan(half))
    O = circumcenter(A, B, C)
    I, _ = incircle(A, B, C)
    D = foot_of(O, A, B)
    E = foot_of(O, A, C)
    f, ax = g.canvas(5, -0.38, 3.105)
    g.poly(ax, [A, B, C])
    for p, q in ((A, O), (O, D), (O, E), (O, B), (O, C), (I, B), (I, C)):
        g.seg(ax, p, q)
    g.corner_mark(ax, D, unit(D, A), unit(D, O))
    g.corner_mark(ax, E, unit(E, A), unit(E, O))
    g.dot(ax, O)
    g.dot(ax, I)
    g.name(ax, O, "O", dy=-3.2, va="top")                # O 점, I 점, OB, OC에서 고루 0.8pt 남짓 뜬다
    g.name(ax, I, "I", dy=-4, va="top")
    g.name(ax, A, "A", dy=5, va="bottom")
    g.name(ax, B, "B", dx=-4, dy=-3, ha="right")          # 원본처럼 꼭짓점 옆, 조금 아래
    g.name(ax, C, "C", dx=4, dy=-3, ha="left")
    g.name(ax, D, "D", dx=-4, ha="right")
    g.name(ax, E, "E", dx=4, ha="left")
    g.save(f, "p013.svg")

# ── 묶음 D ────────────────────────────────────────────────────────────

def p014():
    """014. 평행사변형 ABCD와 ∠C의 이등분선 CE.

    셈. B(0, 0), C(42, 0), ∠B = 40°, AB = 36이라 A = 36(cos 40°, sin 40°) = (27.58, 23.14),
    D = A + (42, 0) = (69.58, 23.14). ∠C = 140°를 CE가 이등분하므로 ∠BCE = ∠ECD = 70°이고
    AD ∥ BC라 ∠CED = ∠BCE = 70°(엇각). 그래서 DE = DC = 36, AE = 42 − 36 = 6, E = A + (6, 0).
    x = 6, y = 70, x + y = 76(④). 모양은 조건이 다 정한다.
    원본은 축척이 아니다(AE : ED를 3 : 7쯤으로 그렸다). 축척대로 AE : ED = 1 : 6이라 E가 A에 붙는다.

    인쇄된 것(옮겼다). 평행사변형 ABCD, 선분 CE, A, B, C, D, E. B의 40° 호와 글, E의 y° 호와 글(∠CED),
    C의 두 같은 각 점(∠BCE, ∠ECD). 점선 곡선 42(A에서 D, 위), 36(B에서 A, 왼쪽 위), x(A에서 E, 아래).
    학생 흔적(뺐다). E 옆과 y° 옆의 큰 먹점, ED 위의 획 둘과 D 옆의 획 하나, DC 위의 × 꼴 획,
    손글씨 36과 C 옆의 호, E 오른쪽 위의 연한 〃, 빨간 채점 곡선, 풀이 글씨(y = 70°, x = 6).

    배치. 배율은 1 = 2.46pt라 AE가 종이에서 15pt뿐이다. x 글이 그 가운데 9.5pt를 끊으니 x 곡선은 양끝
    토막만 남는다. 곡선을 깊게 해도 가로로 보이는 토막은 늘지 않아서 배율을 5칸 안에서 되도록 키웠다.
    깊이는 13.5pt다. 원본은 x 글이 y° 글과 같은 높이에 있고 x가 글자 높이의 1할쯤 아래다. 13.5pt면
    x가 y의 몸통보다 1할 남짓 내려앉고 A와 E에서 x로 모이는 토막이 8pt쯤 된다. 11pt에서는 x가 y°보다
    몸통 4할만큼 떠 보이고 토막이 틱 둘처럼 짧았다(검토 지적). 42 곡선은 26pt로 띄워 원본처럼
    A와 E 이름 사이로 지나가게 하고 A와 E 이름을 같은 높이에 두되 곡선에서 비켜 A는 왼쪽, E는 오른쪽으로
    조금 옮겼다. 36 곡선은 원본처럼 왼쪽 위로 크게 부풀렸다(20pt). 40° 호는 원본 호가 커서 r = 16pt다.
    """
    B, C = (0.0, 0.0), (42.0, 0.0)
    A = polar(B, 36.0, 40.0)
    D = (A[0] + 42.0, A[1])
    E = (A[0] + 6.0, A[1])
    f, ax = g.canvas(5, -7.53, 37.14)
    g.poly(ax, [A, B, C, D])
    g.seg(ax, C, E)
    g.angle(ax, B, C, A, "$40^{\\circ}$", r=16)
    g.angle(ax, E, C, D, "$y^{\\circ}$", r=12)
    g.angle(ax, C, E, B, "", r=12, ticks=1)
    g.angle(ax, C, D, E, "", r=12, ticks=1)
    g.dim(ax, A, D, "42", side=1, gap=g.pt(ax, 26))
    g.dim(ax, B, A, "36", side=1, gap=g.pt(ax, 20))
    g.dim(ax, A, E, "$x$", side=-1, gap=g.pt(ax, 13.5))
    g.name(ax, A, "A", dx=-4.5, dy=1, va="bottom")
    g.name(ax, B, "B", dx=-2, dy=-5, ha="right", va="top")
    g.name(ax, C, "C", dy=-5, va="top")
    g.name(ax, D, "D", dx=4, ha="left")
    g.name(ax, E, "E", dx=1.5, dy=1, va="bottom")
    g.save(f, "p014.svg")


def p015():
    """015. 평행사변형 ABCD, AD의 연장선 위의 E(AD = DE), 대각선의 교점 O, 선분 EO, EC.

    셈. 삼각형 ACE로 본다. D는 AE의 중점, O는 AC의 중점이라 DO ∥ EC이고 ∠DOE = ∠OEC = 26° = ∠DEO에서
    DO = DE = AD. 곧 D가 삼각형 AOE의 외심이라 ∠AOE = 90°, EO는 AC의 수직이등분선이고 EA = EC,
    ∠AEC = 52°. x = ∠ADO = ∠DOE + ∠DEO = 52, y = ∠BCO = ∠OAE(엇각) = (180 − 52)/2 = 64.
    E(0, 0), A(−2, 0), D(−1, 0), C = 2(cos 232°, sin 232°) = (−1.231, −1.576), O = (A + C)/2,
    B = A + C − D = (−2.231, −1.576). ∠ADO = 52°, ∠BCO = 64°라 x + y = 116(②).
    원본은 축척이 아니다(가로로 누운 평행사변형, E의 두 각을 17°쯤으로 그렸다). 축척대로 그리면
    AD = 1, AB ≈ 1.59인 세로로 선 평행사변형이 된다. 배치(A 왼쪽 위, D 오른쪽 위, E는 D 오른쪽,
    B 왼쪽 아래, C 오른쪽 아래)와 표시는 원본대로다.

    인쇄된 것(옮겼다). 변 AB, BC, CD, 선분 AE(AD와 DE), 대각선 AC, BD, 선분 EO(O에서 멈춘다), EC.
    A, B, C, D, E. AD와 DE 가운데의 같은 길이 획 둘(원본이 획 둘이라 그대로 n = 2). D의 x° 호와 글(∠ADO),
    C의 y° 호와 글(∠BCO), E의 두 작은 호(∠DEO, ∠CEO)와 바깥 26° 글 둘에서 굽어 들어오는 화살표.
    O는 원본 그림에 이름이 인쇄되어 있지 않다(교점 둘레 네 틈 어디에도 없다). 그래서 넣지 않았다.
    학생 흔적(뺐다). O의 직각 표시(펜으로 그린 삐뚠 네모), BO 위의 획, OD 위의 × 꼴 획, BC 아래의 11,
    교점 왼쪽의 x+y와 Ø, D 옆의 호와 128, C 둘레의 빗금과 26 26 52, C에서 오른쪽으로 그은 긴 곡선,
    B 옆의 호와 x, 52, 5, 64, 빨간 채점 곡선.

    배치. E의 두 호는 원본처럼 반지름이 달라 EO 위에서 계단이 진다. 안쪽이 ∠DEO(r = 22pt), 바깥쪽이
    ∠OEC(r = 25pt)다. 원해상도 사진에서 E부터 잰 호가 AE의 0.166배와 0.195배라 AE 130pt에 맞췄다.
    한 반지름으로 이으면 ∠DEC 하나에 화살표 둘을 단 것처럼 읽혀 26°인 각이 둘이라는 것이 흐려진다.
    26° 글은 원본처럼 하나는 AE 위, 하나는 EC 오른쪽 아래에 두고 화살표를 서쪽으로 부풀려 C 꼴로
    굽혔다. 위 화살표는 안쪽 호, 아래 화살표는 바깥 호의 가운데에 닿는다.
    """
    E, A, D = (0.0, 0.0), (-2.0, 0.0), (-1.0, 0.0)
    C = polar(E, 2.0, 232.0)
    B = (A[0] + C[0] - D[0], A[1] + C[1] - D[1])
    O = mid(A, C)
    f, ax = g.canvas(7, -1.87, 0.50)
    k = g.pt(ax, 1)                               # 1pt
    g.seg(ax, A, E)
    g.seg(ax, A, B)
    g.seg(ax, B, C)
    g.seg(ax, C, D)
    g.seg(ax, A, C)
    g.seg(ax, B, D)
    g.seg(ax, E, O)
    g.seg(ax, E, C)
    g.tick(ax, A, D, 2)
    g.tick(ax, D, E, 2)
    g.angle(ax, D, A, O, "$x^{\\circ}$", r=12)
    g.angle(ax, C, O, B, "$y^{\\circ}$", r=12)
    m1 = g.angle(ax, E, D, O, "", r=22)
    m2 = g.angle(ax, E, O, C, "", r=25)
    t1 = (-6 * k, 22 * k)
    t2 = (-2 * k, -40 * k)
    g.label(ax, t1[0], t1[1], "$26^{\\circ}$")
    g.label(ax, t2[0], t2[1], "$26^{\\circ}$")
    w = g.text_size(ax, "$26^{\\circ}$")[0]
    pointer(ax, (t1[0] - (w / 2 + 2) * k, t1[1]), m1, bend=-0.5)
    pointer(ax, (t2[0] - (w / 2 + 2) * k, t2[1]), m2, bend=0.5)
    g.name(ax, A, "A", dx=-3, dy=3, ha="right", va="bottom")
    g.name(ax, B, "B", dx=-3, dy=-3, ha="right", va="top")
    g.name(ax, C, "C", dy=-5, va="top")
    g.name(ax, D, "D", dy=5, va="bottom")
    g.name(ax, E, "E", dx=4, ha="left")
    g.save(f, "p015.svg")


def p016():
    """016. 사각형 ABCD와 두 대각선의 교점 O.

    모양. 문제가 모양을 정하지 않는다(평행사변형이 되는 조건을 고르는 문제라 그림은 일반 사각형이다).
    원본 그림의 꼭짓점을 원해상도 사진에서 재어 그대로 옮겼다. B(0, 1.75), A(1.95, 7.65),
    D(8.45, 7.75), C(8.5, 0). AD는 거의 수평, DC는 거의 수직이고 AD ≈ 6.50, BC ≈ 8.68, AB ≈ 6.21,
    DC ≈ 7.75라 평행사변형이 아니다. O는 두 대각선의 교점(셈)이고 이름은 원본처럼 아래 틈에 둔다.

    인쇄된 것(옮겼다). 사각형 ABCD, 대각선 AC, BD, A, B, C, D, O.
    학생 흔적(뺐다). AB 위의 4와 A 꼴 글씨, DC 위의 획과 4 꼴 글씨, AD 위의 작은 획 둘, BC 아래의 획 둘,
    OC 위의 연한 획, 빨간 채점 곡선.
    """
    B, A, D, C = (0.0, 1.75), (1.95, 7.65), (8.45, 7.75), (8.5, 0.0)
    O = cross(A, C, B, D)
    f, ax = g.canvas(5, -1.6, 9.4)
    g.poly(ax, [A, B, C, D])
    g.seg(ax, A, C)
    g.seg(ax, B, D)
    g.name(ax, A, "A", dx=-3, dy=3, ha="right", va="bottom")
    g.name(ax, B, "B", dx=-4, dy=-2, ha="right", va="top")
    g.name(ax, C, "C", dx=3, dy=-3, ha="left", va="top")
    g.name(ax, D, "D", dx=3, dy=3, ha="left", va="bottom")
    g.name(ax, O, "O", dx=-2, dy=-9, va="top")
    g.save(f, "p016.svg")

# ── 묶음 E ────────────────────────────────────────────────────────────

# ── 017. 평행사변형 ABCD, CD 위의 E, BE 위의 P(BP : PE = 2 : 3) ─────────────

def p017():
    """평행사변형 ABCD(B 왼쪽 아래, BC 가로, A와 D 위에서 오른쪽으로 밀림)와 변 CD 위의 점 E,
    선분 BE 위의 점 P, 선분 AE, AP, PC, PD. 색칠한 삼각형 ABP.

    문제는 평행사변형의 모양과 E의 자리를 정하지 않는다. 원본 사진(2525px)의 인쇄 선을 맞춰
    꼭짓점을 교점으로 잡았다. BC 837.6px, 높이 621.8px, 위 변이 오른쪽으로 415.8px 밀려
    밑변 : 높이 : 밀림 = 1.35 : 1 : 0.67이다. 그래서 높이 6에 B(0, 0), C(8, 0), A(4, 6), D(12, 6).
    E는 사진에서 DE : DC = 0.334(AE와 CD의 교점 0.339, BE와 CD의 교점 0.331)라 DC의 D 쪽
    삼등분점으로 E = D + (C − D)/3 = (10.667, 4)로 골랐다.
    P는 조건 BP : PE = 2 : 3으로 P = B + 0.4(E − B) = (4.267, 1.6). 사진의 P(교점 530, 567px)와 맞는다.
    넓이는 그림에 적지 않으니 크기는 비만 따른다(이 모양의 평행사변형 넓이는 48, 문제의 넓이는 160).

    인쇄로 본 선: 네 변, BE, AE, AP, PC, PD(선을 따라 곧게 편 띠에서 인쇄 선의 톱니 가장자리가
    끝까지 곧게 이어진다). AC와 BD 자리에는 인쇄 선이 없다. 색칠은 원본의 망점(삼각형 ABP)을
    규칙대로 10%로 옮겼다. 학생 흔적(연필 덧선과 빗금, 파란 세로줄, 빨간 빗금, P에서 오른쪽으로
    그은 선과 점, 2+ 3+ 2• 3• 같은 넓이 글, 48, A6 7)은 뺐다.
    이름의 자리는 원본대로 A 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래, E 오른쪽 아래, P 아래."""
    B, C, A, D = (0.0, 0.0), (8.0, 0.0), (4.0, 6.0), (12.0, 6.0)
    E = lerp(D, C, 1 / 3)
    P = lerp(B, E, 0.4)
    fig, ax = g.canvas(6, -1.1, 7.15)
    g.shade(ax, [A, B, P])
    g.poly(ax, [A, B, C, D])
    g.seg(ax, B, E)
    g.seg(ax, A, E)
    g.seg(ax, A, P)
    g.seg(ax, P, C)
    g.seg(ax, P, D)
    g.name(ax, A, "A", dx=-1, dy=4, va="bottom")
    g.name(ax, B, "B", dx=-3, dy=-2, ha="right", va="top")
    g.name(ax, C, "C", dx=3, dy=-2, ha="left", va="top")
    g.name(ax, D, "D", dx=3, dy=2, ha="left", va="bottom")
    g.name(ax, E, "E", dx=4, dy=-1, ha="left", va="top")
    g.name(ax, P, "P", dy=-5, va="top")
    g.save(fig, "p017.svg")


# ── 019. 직각삼각형 ABC, AD = AC, DE ⊥ AB ──────────────────────────────────

def p019():
    """∠C = 90°인 직각삼각형 ABC(B 왼쪽, C 오른쪽 아래, A는 C 바로 위)와 변 AB 위의 점 D,
    변 BC 위의 점 E, 선분 DE(D에서 AB와 직각).

    모양은 조건으로 다 정해진다. RHS 합동으로 CE = DE = 3이라 BE = 7, 직각삼각형 BDE에서
    BD = √(7² − 3²) = 2√10이다. △BDE ∽ △BCA(∠B 공통, ∠BDE = ∠BCA = 90°)라
    AC = BC×DE/BD = 30/(2√10) = 1.5√10 ≈ 4.743, AB = √(100 + 22.5) ≈ 11.068,
    AD = AC ≈ 4.743, BD ≈ 6.325 = 2√10으로 맞는다.
    C(0, 0), B(−10, 0), A(0, 4.743), D = A + (B − A)×AC/AB ≈ (−4.285, 2.711), E(−3, 0).
    원본 사진은 AC/BC = 0.53으로 참값 0.474보다 조금 높게 그렸지만 축척은 참값을 따랐다.
    사진은 2.5° 기울어 있어 BC를 가로로 세웠다.

    인쇄로 본 것: 세 변, 선분 DE, D의 직각 표시(∠ADE 쪽), C의 직각 표시, AD와 AC 한가운데의
    두 획(둘 다 두 획이라 n=2로 원본대로), DE의 B 쪽 점선 곡선과 3, BC 아래 점선 곡선과 10.
    10의 곡선은 원본처럼 깊게 늘어져 E 이름 아래를 지나므로 gap 18pt로 E 이름을 비켰다.
    학생 흔적(A와 E를 잇는 두 겹 선, E에서 오른쪽으로 끈 곡선과 손글씨 3, C 옆 빗금 한 획,
    빨간 채점 동그라미와 7)은 뺐다."""
    AC = 1.5 * math.sqrt(10)
    C, B, A = (0.0, 0.0), (-10.0, 0.0), (0.0, AC)
    D = lerp(A, B, AC / dist(A, B))
    E = (-3.0, 0.0)
    fig, ax = g.canvas(6, -1.6, 5.75)
    g.poly(ax, [A, B, C])
    g.seg(ax, D, E)
    g.corner_mark(ax, D, unit(D, A), unit(D, E))
    g.right_angle(ax, C, -1, 1)
    g.tick(ax, A, D, 2)
    g.tick(ax, A, C, 2)
    g.dim(ax, D, E, "3", side=-1)                  # D→E의 오른쪽(B 쪽)
    g.dim(ax, B, C, "10", side=-1, gap=g.pt(ax, 18))
    g.name(ax, A, "A", dx=1, dy=4, va="bottom")
    g.name(ax, B, "B", dx=-3, dy=-1, ha="right", va="top")
    g.name(ax, C, "C", dx=3, dy=-1, ha="left", va="center")   # 원본처럼 꼭짓점 바로 오른쪽
    g.name(ax, D, "D", dx=-2, dy=3, ha="right", va="bottom")
    g.name(ax, E, "E", dy=-4, va="top")
    g.save(fig, "p019.svg")


# ── 020. 평행사변형 ABCD, AB와 CD의 중점 E, F ───────────────────────────────

def p020():
    """평행사변형 ABCD(B 왼쪽 아래, BC 가로, 위 변이 오른쪽으로 밀림)와 변 AB의 중점 E,
    변 CD의 중점 F, 선분 ED, BF. 색칠한 사각형 EBFD.

    문제는 평행사변형의 모양을 정하지 않는다. 원본 사진(2470px)의 인쇄 선을 맞춰 꼭짓점을
    교점으로 잡았다. BC 946px, 높이 539px, 위 변이 오른쪽으로 251px 밀려
    밑변 : 높이 : 밀림 = 1.755 : 1 : 0.466이다. 그래서 높이 4에 B(0, 0), C(7, 0),
    A(1.86, 4), D(8.86, 4). E = (A + B)/2 = (0.93, 2), F = (C + D)/2 = (7.93, 2).
    사진의 E, F(ED와 AB, BF와 CD의 교점)도 두 변의 한가운데에 있다.

    인쇄로 본 것: 네 변, ED, BF, AE와 EB의 한 획, DF와 FC의 두 획, 사각형 EBFD의 망점
    색칠(규칙대로 10%). 학생 흔적(빨간 채점 곡선, 손글씨 EB = DF, EB // DF)은 뺐다."""
    h, b, s = 4.0, 7.0, 1.86
    B, C, A, D = (0.0, 0.0), (b, 0.0), (s, h), (s + b, h)
    E, F = mid(A, B), mid(C, D)
    fig, ax = g.canvas(5, -0.73, 4.73)
    g.shade(ax, [E, B, F, D])
    g.poly(ax, [A, B, C, D])
    g.seg(ax, E, D)
    g.seg(ax, B, F)
    g.tick(ax, A, E, 1)
    g.tick(ax, E, B, 1)
    g.tick(ax, D, F, 2)
    g.tick(ax, F, C, 2)
    g.name(ax, A, "A", dx=-3, dy=1, ha="right", va="bottom")
    g.name(ax, B, "B", dx=-3, dy=-1, ha="right", va="top")
    g.name(ax, C, "C", dx=3, dy=-1, ha="left", va="top")
    g.name(ax, D, "D", dx=4, ha="left")
    g.name(ax, E, "E", dx=-4, dy=2, ha="right")
    g.name(ax, F, "F", dx=3, dy=-1, ha="left", va="top")
    g.save(fig, "p020.svg")


if __name__ == "__main__":
    p003()
    p004s()
    p005()
    p005a()
    p005b()
    p005c()
    p005d()
    p006()
    p007()
    p008()
    p009()
    p010()
    p011()
    p012()
    p013()
    p014()
    p015()
    p016()
    p017()
    p018()
    p019()
    p020()
