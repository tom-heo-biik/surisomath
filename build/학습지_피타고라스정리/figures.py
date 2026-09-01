# -*- coding: utf-8 -*-
"""학습지 '피타고라스 정리, 어려운 두 문제' — 그림·수식·로고 SVG 생성.

surisomath-a4 규격을 따른다: Computer Modern, 도형 변 0.7pt, 보조 점선 0.4pt·2pt
등간격, 블록 높이는 22pt의 배수. 로고는 vectorize로 비트맵을 패스로 떠서 쓴다.

    python build/학습지_피타고라스정리/figures.py
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "lib"))
sys.path.insert(0, str(ROOT / "build"))
sys.path.insert(0, str(ROOT / "skills" / "surisomath-a4" / "templates"))

import suriso
import vectorize
import figure as fig  # import만으로 rcParams(CM + KoPub 폴백)가 잡힌다

import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Polygon

OUT = HERE / "figures"
OUT.mkdir(exist_ok=True)

GRID = 22.0
PT = 1 / 72
INK = "#161616"        # figure.py와 같은 잉크색
EDGE = 0.7             # 도형 변
AUX = 0.4              # 보조선
PATH = 1.0             # 최단 경로(그래프 선 두께)
DASH = (0, (2, 2))     # 점선 2pt 등간격
DOT = 2.4              # 점 지름(pt)
LABEL = 10.0


# ── 공통 ────────────────────────────────────────────────────────────────

def canvas(units: int, x0, x1, y0, y1, flip=False):
    """높이 units×22pt, 데이터 비율 그대로의 캔버스."""
    scale = units * GRID / (y1 - y0)
    w = (x1 - x0) * scale
    f = plt.figure(figsize=(w * PT, units * GRID * PT))
    f.patch.set_alpha(0)
    ax = f.add_axes((0, 0, 1, 1))
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    if flip:
        ax.invert_yaxis()
    ax.set_aspect("equal")
    ax.axis("off")
    return f, ax


def seg(ax, p, q, lw=EDGE, dashed=False):
    ax.plot([p[0], q[0]], [p[1], q[1]], color=INK, linewidth=lw,
            linestyle=DASH if dashed else "-",
            solid_capstyle="round", dash_capstyle="butt")


def dot(ax, p):
    ax.plot([p[0]], [p[1]], marker="o", markersize=DOT, markeredgewidth=0,
            color=INK, linestyle="none", zorder=5)


def label(ax, x, y, s, ha="center", va="center", size=LABEL, rotation=0):
    ax.text(x, y, s, ha=ha, va=va, fontsize=size, color=INK, rotation=rotation)


def save(f, name):
    f.savefig(OUT / name, format="svg", transparent=True)
    plt.close(f)
    print(f"  {name}")


# ── 로고 — 심볼 + 전체 워드마크 세로 조합, 높이 88pt(4칸) ──────────────

def logo():
    d_sym, (sx, sy, sw, sh) = vectorize.trace(str(suriso.SYMBOL))
    d_wm, (wx, wy, ww, wh) = vectorize.trace(str(suriso.WORDMARK_FULL))

    SYM_H, GAP, WM_H = 46.0, 14.0, 28.0          # 46+14+28 = 88 = 4칸
    s1, s2 = SYM_H / sh, WM_H / wh
    w1, w2 = sw * s1, ww * s2
    W, H = max(w1, w2), SYM_H + GAP + WM_H

    def place(d, bx, by, s, offx, offy):
        return (f'<path transform="translate({offx - bx * s:.3f},{offy - by * s:.3f}) '
                f'scale({s:.6f})" d="{d}"/>')

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.2f}pt" height="{H:.2f}pt" '
        f'viewBox="0 0 {W:.2f} {H:.2f}">'
        f'<g fill="{suriso.INK_HEX}" fill-rule="evenodd">'
        + place(d_sym, sx, sy, s1, (W - w1) / 2, 0)
        + place(d_wm, wx, wy, s2, (W - w2) / 2, SYM_H + GAP)
        + "</g></svg>"
    )
    (OUT / "logo.svg").write_text(svg, encoding="utf-8")
    print(f"  logo.svg  ({W:.0f}×{H:.0f}pt)")


# ── 문제 1 — 정사각형 ABCD ──────────────────────────────────────────────

A, B, C, D = (0, 12), (0, 0), (12, 0), (12, 12)
E, F, G = (4, 0), (12, 6), (12, 16)


def square_base(ax):
    for p, q in [(A, B), (B, C), (C, D), (D, A), (A, E), (A, F), (E, F)]:
        seg(ax, p, q)
    ax.add_patch(Arc(A, 5.6, 5.6, angle=0, theta1=-71.565, theta2=-26.565,
                     lw=AUX + 0.1, color=INK))
    label(ax, 2.55, 9.15, r"$45^\circ$", size=9)
    label(ax, -0.45, 12.4, "$A$", ha="right", va="bottom")
    label(ax, -0.45, -0.4, "$B$", ha="right", va="top")
    label(ax, 12.45, -0.4, "$C$", ha="left", va="top")
    label(ax, 12.45, 12.4, "$D$", ha="left", va="bottom")
    label(ax, 4, -0.6, "$E$", va="top")
    label(ax, 12.55, 6, "$F$", ha="left")
    label(ax, -0.6, 6, "12", ha="right")
    label(ax, 2, -0.6, "4", va="top")


def problem1():
    f, ax = canvas(8, -2.4, 13.9, -2.0, 13.8)
    square_base(ax)
    for p in (A, B, C, D, E, F):
        dot(ax, p)
    save(f, "p1.svg")


def solution1():
    f, ax = canvas(9, -2.4, 13.9, -2.0, 17.6)
    ax.add_patch(Polygon([A, E, F], closed=True, facecolor=INK, alpha=0.10,
                         edgecolor="none"))
    square_base(ax)
    seg(ax, A, G, lw=AUX, dashed=True)
    seg(ax, D, G, lw=AUX, dashed=True)
    label(ax, 12.45, 16.35, "$G$", ha="left", va="bottom")
    label(ax, 12.5, 14, "4", ha="left")
    for p in (A, B, C, D, E, F, G):
        dot(ax, p)
    save(f, "s1.svg")


# ── 문제 2 — 직육면체 창고 ──────────────────────────────────────────────

def problem2():
    ox, oy = 3.2, 3.2                       # 깊이 9m의 사선 투영
    fbl, fbr = (0, 0), (28, 0)
    ftr, ftl = (28, 7), (0, 7)
    bbl, bbr = (ox, oy), (28 + ox, oy)
    btr, btl = (28 + ox, 7 + oy), (ox, 7 + oy)

    f, ax = canvas(6, -1.9, 31.9, -1.9, 11.6)
    for p, q in [(fbl, fbr), (fbr, ftr), (ftr, ftl), (ftl, fbl),
                 (ftl, btl), (ftr, btr), (btl, btr), (fbr, bbr), (bbr, btr)]:
        seg(ax, p, q)
    for p, q in [(fbl, bbl), (bbl, bbr), (bbl, btl)]:
        seg(ax, p, q, lw=AUX, dashed=True)

    a = (1.6, 7.6)                          # 왼쪽 벽면 좌우 가운데, 천장에서 1m
    b = (29.6, 2.6)                         # 오른쪽 벽면 좌우 가운데, 바닥에서 1m
    dot(ax, a)
    dot(ax, b)
    label(ax, 1.2, 8.15, "$A$", ha="right", va="bottom")
    label(ax, 30.1, 2.15, "$B$", ha="left", va="top")
    label(ax, 14, -0.7, "28", va="top")
    label(ax, -0.7, 3.5, "7", ha="right")
    label(ax, 29.2, 9.0, "9", ha="right", va="bottom")
    save(f, "p2.svg")


# ── 풀이 2 — 다섯 면 전개도 (y축 아래 방향) ─────────────────────────────

def solution2():
    f, ax = canvas(10, -4.2, 34.4, -0.6, 25.6, flip=True)

    outline = [(-1, 0), (29, 0), (29, 16), (31, 16), (31, 25),
               (1, 25), (1, 9), (-1, 9)]
    for i in range(len(outline)):
        seg(ax, outline[i], outline[(i + 1) % len(outline)])

    for p, q in [((1, 0), (1, 9)), ((1, 9), (29, 9)),
                 ((1, 16), (29, 16)), ((29, 16), (29, 25))]:
        seg(ax, p, q, lw=AUX, dashed=True)          # 접히는 자리

    a, b = (0, 4.5), (30, 20.5)
    seg(ax, a, b, lw=PATH)
    for p, q in [((0, 0), (0, 4.5)), ((30, 0), (30, 16)),
                 ((0, 4.5), (32.6, 4.5)), ((30, 20.5), (32.6, 20.5))]:
        seg(ax, p, q, lw=AUX, dashed=True)          # 치수 보조선

    dot(ax, a)
    dot(ax, b)
    label(ax, -1.2, 4.1, "$A$", ha="right", va="bottom")
    label(ax, 30.5, 21.3, "$B$", ha="left", va="top")
    label(ax, 15.7, 11.5, "34", rotation=-28, size=9.5)
    label(ax, 15, 1.7, "30")
    label(ax, 32.9, 12.5, "16", ha="left")
    label(ax, 24, 1.7, "천장")
    label(ax, -1.8, 6.5, "벽", ha="right")
    label(ax, 8, 12.5, "옆벽")
    label(ax, 14, 20.9, "바닥")
    label(ax, 30, 17.6, "벽", size=9)
    save(f, "s2.svg")


# ── 수식 ────────────────────────────────────────────────────────────────

def equations():
    eqs = {
        "eq1.svg": r"(4+x)^2 = 8^2 + (12-x)^2",
        "eq2.svg": r"\triangle AEF = \triangle AGF"
                   r" = \frac{1}{2} \times 10 \times 12 = 60",
        "eq3.svg": r"\sqrt{37^2 + 5^2} = \sqrt{1394}",
        "eq4.svg": r"\sqrt{30^2 + 16^2} = \sqrt{1156} = 34",
    }
    for name, tex in eqs.items():
        try:
            fig.equation(tex, str(OUT / name), units=2)
        except ValueError:
            fig.equation(tex.replace(r"\triangle", r"\bigtriangleup"),
                         str(OUT / name), units=2)
        print(f"  {name}")


if __name__ == "__main__":
    print("figures/")
    logo()
    problem1()
    problem2()
    solution1()
    solution2()
    equations()
