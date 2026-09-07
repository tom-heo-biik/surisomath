# -*- coding: utf-8 -*-
"""연마(硏磨) '원의 둘레와 넓이' — 문제 그림 아홉 장.

도우미는 surisomath-grind 스킬의 grind_figure를 쓴다. build.py가 import 경로를 잡아
주므로 이 파일은 build.py로 실행한다.

    python .claude/skills/surisomath-grind/templates/build.py build/연마_원의둘레와넓이/problems.yaml
"""
from __future__ import annotations

import math

import grind_figure as g

g.setup(__file__)


# ── 004~006 — 끈으로 묶은 원 ────────────────────────────────────────────
# 끈은 원 둘레에서 살짝 띄워 1pt로 그린다. 붙여 그리면 원의 선과 겹쳐 안 보인다.

def p2():
    r, o = 8.0, 0.55
    cs = [(8, 8), (24, 8), (40, 8)]
    f, ax = g.canvas(5, -1.5, 18.0)
    for c in cs:
        g.circle(ax, c, r)
        g.dot(ax, c)
    g.seg(ax, (8, 16 + o), (40, 16 + o), lw=g.STRING)
    g.seg(ax, (8, -o), (40, -o), lw=g.STRING)
    g.arc(ax, cs[0], r + o, 90, 270, lw=g.STRING)
    g.arc(ax, cs[2], r + o, -90, 90, lw=g.STRING)
    g.seg(ax, cs[2], (48, 8), lw=g.AUX)
    g.dim(ax, cs[2], (48, 8), "8cm", gap=1.6)
    g.save(f, "p2.svg")


def p2_1():
    r, o = 5.0, 0.4
    cs = [(5, 5), (15, 5), (5, 15), (15, 15)]
    f, ax = g.canvas(6, -1.2, 21.3)
    for c in cs:
        g.circle(ax, c, r)
        g.dot(ax, c)
    g.seg(ax, (5, 20 + o), (15, 20 + o), lw=g.STRING)
    g.seg(ax, (5, -o), (15, -o), lw=g.STRING)
    g.seg(ax, (-o, 5), (-o, 15), lw=g.STRING)
    g.seg(ax, (20 + o, 5), (20 + o, 15), lw=g.STRING)
    g.arc(ax, (5, 15), r + o, 90, 180, lw=g.STRING)
    g.arc(ax, (5, 5), r + o, 180, 270, lw=g.STRING)
    g.arc(ax, (15, 5), r + o, 270, 360, lw=g.STRING)
    g.arc(ax, (15, 15), r + o, 0, 90, lw=g.STRING)
    g.seg(ax, (15, 15), (20, 15), lw=g.AUX)
    g.dim(ax, (15, 15), (20, 15), "5cm", gap=1.1)
    g.save(f, "p2_1.svg")


def p2_2():
    r, o = 10.5, 0.6
    h = 21 * math.sqrt(3) / 2
    bl, br, t = (10.5, 10.5), (31.5, 10.5), (21.0, 10.5 + h)
    f, ax = g.canvas(7, -2.1, 10.5 + h + r + 2.1)
    for c in (bl, br, t):
        g.circle(ax, c, r)
        g.dot(ax, c)
    # 끈: 바깥 접선 세 개 + 120° 호 세 개
    for a, b, deg in ((bl, br, -90), (br, t, 30), (t, bl, 150)):
        n = (math.cos(math.radians(deg)), math.sin(math.radians(deg)))
        g.seg(ax, (a[0] + n[0] * (r + o), a[1] + n[1] * (r + o)),
              (b[0] + n[0] * (r + o), b[1] + n[1] * (r + o)), lw=g.STRING)
    g.arc(ax, br, r + o, -90, 30, lw=g.STRING)
    g.arc(ax, t, r + o, 30, 150, lw=g.STRING)
    g.arc(ax, bl, r + o, 150, 270, lw=g.STRING)
    g.seg(ax, (t[0] - r, t[1]), (t[0] + r, t[1]), lw=g.AUX)
    g.dim(ax, (t[0] - r, t[1]), (t[0] + r, t[1]), "21cm", gap=2.4)
    g.save(f, "p2_2.svg")


# ── 007~009 — 색칠한 부분 ───────────────────────────────────────────────

def p3():
    R = 6.0
    O, L, Rr = (0, 0), (-3, 0), (3, 0)
    f, ax = g.canvas(6, -7.6, 7.6)
    g.shade(ax, g.arc_pts(O, R, 180, 360) + g.arc_pts(Rr, 3, 0, 180)
            + g.arc_pts(L, 3, 0, -180))
    g.circle(ax, O, R)
    g.seg(ax, (-R, 0), (R, 0))
    g.arc(ax, Rr, 3, 0, 180)
    g.arc(ax, L, 3, 180, 360)
    for p in (O, L, Rr):
        g.dot(ax, p)
    g.dim(ax, (-R, 0), (0, 0), "6cm", gap=1.3)
    g.save(f, "p3.svg")



def p3_1():
    s, r = 18.0, 9.0
    f, ax = g.canvas(6, -4.6, 19.5)
    corners = [(0, 0), (s, 0), (s, s), (0, s)]
    for c, t1 in zip(corners, (0, 90, 180, 270)):
        g.wedge(ax, c, r, t1, t1 + 90)
    for c, t1 in zip(corners, (0, 90, 180, 270)):
        g.arc(ax, c, r, t1, t1 + 90)
    g.rect(ax, (0, 0), s, s)
    for c in corners:
        g.dot(ax, c)
    g.dim(ax, (s, 0), (s, s), "18cm", side=-1, gap=3.0)    # 오른쪽 변. 글 너비만큼 부풀린다
    g.dim(ax, (0, 0), (s, 0), "18cm", side=-1, gap=1.8)    # 아래 변
    g.save(f, "p3_1.svg")


def p3_2():
    s, r = 20.0, 10.0
    A, B = (20, 10), (10, 0)             # 오른쪽 반원·아래 반원의 중심
    f, ax = g.canvas(6, -4.9, 21.5)
    # 두 반원 바깥의 왼쪽 위 조각
    g.shade(ax, [(0, 0), (0, s), (s, s)] + g.arc_pts(A, r, 90, 180)
            + g.arc_pts(B, r, 90, 180))
    # 두 반원이 겹치는 렌즈
    g.shade(ax, g.arc_pts(A, r, 180, 270) + g.arc_pts(B, r, 0, 90))
    g.arc(ax, A, r, 90, 270)
    g.arc(ax, B, r, 0, 180)
    g.rect(ax, (0, 0), s, s)
    g.dot(ax, A)
    g.dot(ax, B)
    g.dim(ax, (s, 0), (s, s), "20cm", side=-1, gap=3.4)
    g.dim(ax, (0, 0), (s, 0), "20cm", side=-1, gap=2.0)
    g.save(f, "p3_2.svg")


# ── 010~012 — 원주와 넓이 사이 ──────────────────────────────────────────

def p4():
    O = (0, 0)
    f, ax = g.canvas(5, -7.4, 7.4)
    g.circle(ax, O, 6)
    g.circle(ax, O, 4)
    g.seg(ax, (-6, 0), (6, 0))
    g.dot(ax, O)
    apex = g.dim(ax, (4, 0), (6, 0), "", gap=0.9)   # 고리 폭. 글은 지시선으로 밖에
    g.leader(ax, apex, "2cm")
    g.save(f, "p4.svg")


def p4_1():
    O, S = (0, 0), (-5, 0)
    f, ax = g.canvas(5, -11.6, 11.6)
    g.circle(ax, O, 10)
    g.circle(ax, S, 5)
    g.seg(ax, (-10, 0), (10, 0))
    g.dot(ax, O)
    g.dot(ax, S)
    g.save(f, "p4_1.svg")


def p4_2():
    O = (0, 0)
    f, ax = g.canvas(6, -10.5, 10.5)
    g.circle(ax, O, 9)
    for c in ((0, 6), (0, 0), (0, -6)):
        g.circle(ax, c, 3)
        g.dot(ax, c)
    g.seg(ax, (0, -9), (0, 9))
    g.save(f, "p4_2.svg")


if __name__ == "__main__":
    print("figures/")
    p2()
    p2_1()
    p2_2()
    p3()
    p3_1()
    p3_2()
    p4()
    p4_1()
    p4_2()
