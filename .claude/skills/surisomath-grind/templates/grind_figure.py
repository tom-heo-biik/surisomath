# -*- coding: utf-8 -*-
"""연마(硏磨) 학습지 그림 도우미.

단원 폴더의 figures.py가 이 모듈을 가져다 문제 그림을 그린다. 규격은
surisomath-a4를 따른다: Computer Modern(한글은 KoPub 폴백), 도형 선 0.7pt,
끈·경로 1pt, 보조선 0.4pt, 점선 2pt 등간격, 색칠은 잉크 10% 틴트, 블록 높이는
22pt의 배수. 좌표는 문제의 단위(cm, m)를 그대로 쓰고, 선 두께·글자·간격처럼
종이 위의 크기는 pt로 정한다. pt(ax, n)이 둘을 잇는다.

    import grind_figure as g                 # build.py가 import 경로를 잡아 준다
    g.setup(__file__)                        # 옆의 figures/ 가 출력 폴더
    f, ax = g.canvas(5, -3, 9)               # 높이 5칸(110pt)과 y 범위만 정한다
    g.rect(ax, (0, 0), 12, 8)                # 직사각형. 네 귀퉁이에 직각 표시
    g.dim(ax, (0, 0), (12, 0), "12cm", side=-1)   # 점선 곡선 길이 표시
    g.save(f, "p1.svg")                      # x 범위는 잉크에 맞춰 자동으로 잡는다

y 범위가 배율을 정한다(배율 = units×22 ÷ y 범위). x 범위는 save()가 잉크 기준으로
좌우 대칭이 되게 잡으므로 손댈 것이 없다. 위아래 여백이 모자라면 save()가 얼마로
바꾸라고 알려 준다.

글자는 패스로 변환되므로 결과 SVG는 폰트 설치 없이 그대로 렌더된다. 생성 시각을
빼고 해시 소금을 고정해, 같은 그림은 다시 빌드해도 바이트 단위로 같다.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
A4 = HERE.parents[1] / "surisomath-a4" / "templates"
sys.path.insert(0, str(A4))
import figure as _a4  # noqa: E402  import만으로 rcParams(CM + KoPub 폴백)가 잡힌다

import matplotlib  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Arc, Circle, Polygon, Wedge  # noqa: E402

# SVG 안 요소 id는 이 소금으로 해시한다. 비워 두면 실행마다 난수를 써서 같은 그림도
# 파일이 매번 달라진다.
matplotlib.rcParams["svg.hashsalt"] = "surisomath"

GRID = 22.0
PT = 1 / 72
WIDTH = 475.0          # 본문 영역 너비(pt). 그림은 이보다 넓을 수 없다
INK = _a4.INK          # neutral-1000
EDGE = 0.7             # 도형 선. 도형 안을 가르는 선(지름, 길의 가장자리, 안쪽 호)도 이것
STRING = 1.0           # 끈·경로(그래프 선 두께)
AUX = 0.4              # 보조선·치수선·지시선. 높이·반지름처럼 길이를 재려고 그은 선
DOT = 2.4              # 점 지름(pt)
TINT = 0.10            # 색칠한 부분
LABEL = 10.0           # 그림 글자 크기(pt)
DASH = (0, (2, 2))     # 점선 2pt 등간격
MARK = 5.5             # 직각 표시 한 변(pt)
MARGIN = 4.0           # 잉크에서 캔버스 가장자리까지 최소(pt). 잘리지 않게
LEADER = 22.0          # 지시선 길이(pt)
PAD = 2.0              # 길이 글 양옆에 비우는 점선 길이(pt)
SLACK = 22.0           # 위아래 여백이 이보다 크면 그림이 블록에 비해 작다

OUT = HERE / "figures"
WARNINGS = 0           # save()·dim()이 낸 경고 수. build.py가 종료 코드에 쓴다


def warn(msg: str) -> None:
    global WARNINGS
    WARNINGS += 1
    print(f"  ! {msg}")


def setup(script_file: str) -> Path:
    """단원 figures.py의 __file__을 받아 그 옆 figures/ 를 출력 폴더로 잡는다."""
    global OUT
    OUT = Path(script_file).resolve().parent / "figures"
    OUT.mkdir(exist_ok=True)
    return OUT


# ── 캔버스 ──────────────────────────────────────────────────────────────

def canvas(units: int, y0: float, y1: float):
    """높이 units×22pt인 캔버스. y 범위가 배율을 정한다(배율 = units×22 ÷ (y1-y0)).
    x 범위는 save()가 잉크에 맞춰 잡으므로 여기서 정하지 않는다."""
    if units < 1:
        raise ValueError("units는 1 이상이어야 한다")
    if y1 <= y0:
        raise ValueError("y1은 y0보다 커야 한다")
    scale = units * GRID / (y1 - y0)
    f = plt.figure(figsize=(WIDTH * PT, units * GRID * PT))
    f.patch.set_alpha(0)
    ax = f.add_axes((0, 0, 1, 1))
    ax.set_ylim(y0, y1)
    ax.set_xlim(0, WIDTH / scale)      # 임시. save()가 잉크 기준으로 다시 잡는다
    ax.set_aspect("equal")
    ax.axis("off")
    ax.pt = scale                      # 1단위가 몇 pt인지
    ax.units = units
    return f, ax


def pt(ax, n: float) -> float:
    """n pt를 이 캔버스의 좌표 단위로 바꾼다. 간격·길이를 pt로 정할 때 쓴다."""
    return n / ax.pt


def text_size(ax, s: str, size: float = LABEL) -> tuple[float, float]:
    """글의 너비·높이(pt). 실제 글꼴로 잰다."""
    t = ax.text(0, 0, s, fontsize=size)
    bb = t.get_window_extent(renderer=ax.figure.canvas.get_renderer())
    t.remove()
    k = 72 / ax.figure.dpi
    return bb.width * k, bb.height * k


def _pad(a) -> float:
    """이 요소가 선 두께로 얼마나 더 번지는지(pt). 테두리가 없는 색칠은 0이다."""
    lw = (getattr(a, "get_linewidth", lambda: 0)() or 0)
    get_ec = getattr(a, "get_edgecolor", None)
    if get_ec is not None:                      # 패치 — 테두리가 투명하면 안 번진다
        ec = get_ec()
        if ec is None or (hasattr(ec, "__len__") and len(ec) == 4 and ec[3] == 0):
            return 0.0
    return lw / 2


def _ink_bbox(f, ax):
    """그린 것 전부의 경계(pt, 캔버스 왼쪽 아래 기준)."""
    f.canvas.draw()
    r = f.canvas.get_renderer()
    k = 72 / f.dpi
    x0 = y0 = math.inf
    x1 = y1 = -math.inf
    for a in ax.lines + ax.patches + ax.texts:
        if not a.get_visible():
            continue
        bb = a.get_window_extent(r)
        p = _pad(a)
        x0, y0 = min(x0, bb.x0 * k - p), min(y0, bb.y0 * k - p)
        x1, y1 = max(x1, bb.x1 * k + p), max(y1, bb.y1 * k + p)
    if x0 is math.inf:
        raise ValueError("그린 것이 없다")
    return x0, y0, x1, y1


def save(f, name: str) -> Path:
    """x 범위를 잉크 기준 좌우 대칭으로 잡아 SVG로 저장한다. 위아래 여백이 모자라거나
    지나치게 남으면 y 범위를 얼마로 바꾸면 되는지 알려 준다."""
    ax = f.axes[0]
    H = ax.units * GRID
    scale = ax.pt
    X0, X1 = ax.get_xlim()
    Y0, Y1 = ax.get_ylim()
    W = f.get_size_inches()[0] * 72
    bx0, by0, bx1, by1 = _ink_bbox(f, ax)

    # x — 잉크 너비에 좌우 MARGIN을 더한 만큼으로 캔버스를 좁히고 잉크를 가운데 둔다
    cx = X0 + (bx0 + bx1) / 2 / W * (X1 - X0)
    w = bx1 - bx0 + 2 * MARGIN
    if w > WIDTH:
        warn(f"{name}: 그림 너비 {w:.0f}pt가 본문 너비 {WIDTH:.0f}pt를 넘는다. "
             "y 범위를 넓혀 배율을 줄여라")
        w = WIDTH
    f.set_size_inches(w * PT, H * PT)
    ax.set_xlim(cx - w / 2 / scale, cx + w / 2 / scale)

    # y — 배율을 바꾸는 일이라 손으로 정한다. 얼마로 바꾸면 되는지 일러 준다
    gap = min(by0, H - by1)
    if gap < MARGIN or gap > SLACK:
        cy = Y0 + (by0 + by1) / 2 / H * (Y1 - Y0)
        want = (H - 2 * (MARGIN + 1)) / (by1 - by0)          # 잉크를 이만큼 키운다
        span = (Y1 - Y0) / want
        how = "모자란다" if gap < MARGIN else "남는다"
        warn(f"{name}: 위아래 여백 {gap:.1f}pt. {how}. "
             f"y 범위를 ({cy - span / 2:.2f}, {cy + span / 2:.2f})로 잡아라")

    print(f"  {name}  ({w:.0f}×{H:.0f}pt)")
    path = OUT / name
    f.savefig(path, format="svg", transparent=True, metadata={"Date": None})
    plt.close(f)
    return path


# ── 기본 도형 ───────────────────────────────────────────────────────────
# 색칠을 먼저 하고 선을 나중에 긋는다. 순서가 곧 위아래다.

def seg(ax, p, q, lw=EDGE):
    ax.plot([p[0], q[0]], [p[1], q[1]], color=INK, linewidth=lw,
            solid_capstyle="round")


def dashed(ax, p, q, lw=AUX):
    """점선. 길이 표시(dim) 말고 점선을 쓸 일은 드물다. 도형 안의 높이·반지름은 실선이다."""
    ax.plot([p[0], q[0]], [p[1], q[1]], color=INK, linewidth=lw,
            linestyle=DASH, dash_capstyle="butt")


def circle(ax, c, r, lw=EDGE):
    ax.add_patch(Circle(c, r, facecolor="none", edgecolor=INK, linewidth=lw))


def arc(ax, c, r, t1, t2, lw=EDGE):
    """중심 c, 반지름 r, 각 t1°→t2°(반시계) 호."""
    ax.add_patch(Arc(c, 2 * r, 2 * r, angle=0, theta1=t1, theta2=t2,
                     linewidth=lw, color=INK))


def dot(ax, p):
    ax.plot([p[0]], [p[1]], marker="o", markersize=DOT, markeredgewidth=0,
            color=INK, linestyle="none", zorder=5)


def label(ax, x, y, s, ha="center", va="center", size=LABEL):
    ax.text(x, y, s, ha=ha, va=va, fontsize=size, color=INK)


def shade(ax, pts):
    """꼭짓점 목록으로 닫힌 다각형을 잉크 10% 틴트로 칠한다. 호는 arc_pts로 만든다."""
    ax.add_patch(Polygon(pts, closed=True, facecolor=INK, alpha=TINT,
                         edgecolor="none"))


def wedge(ax, c, r, t1, t2):
    """부채꼴을 잉크 10% 틴트로 칠한다."""
    ax.add_patch(Wedge(c, r, t1, t2, facecolor=INK, alpha=TINT, edgecolor="none"))


def right_angle(ax, corner, dx, dy, s=None):
    """꼭짓점 corner에서 (dx, dy) 방향(각 ±1)으로 직각 표시. 한 변 s는 생략하면 MARK pt."""
    if s is None:
        s = pt(ax, MARK)
    x, y = corner
    pts = [(x + dx * s, y), (x + dx * s, y + dy * s), (x, y + dy * s)]
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=INK, linewidth=AUX)


def poly(ax, pts, lw=EDGE):
    """꼭짓점 목록으로 닫힌 다각형(삼각형 등)을 그린다. 목록을 그대로 돌려준다."""
    for i in range(len(pts)):
        seg(ax, pts[i], pts[(i + 1) % len(pts)], lw=lw)
    return list(pts)


def rect(ax, origin, w, h, mark=True, lw=EDGE):
    """왼쪽 아래 origin에서 가로 w, 세로 h인 직사각형. mark면 네 귀퉁이 전부에 직각 표시.
    꼭짓점 네 개를 반시계로 돌려준다."""
    x, y = origin
    c = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    poly(ax, c, lw=lw)
    if mark:
        for p, (dx, dy) in zip(c, ((1, 1), (-1, 1), (-1, -1), (1, -1))):
            right_angle(ax, p, dx, dy)
    return c


def foot(ax, apex, p, q, side=-1):
    """apex에서 선분 pq에 내린 높이. 실선 0.4pt를 긋고 발에 직각 표시를 한다.
    직각 표시는 발의 side 쪽(+1 오른쪽, -1 왼쪽). 밑변이 가로일 때 쓴다.
    발의 좌표를 돌려준다."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    t = ((apex[0] - p[0]) * dx + (apex[1] - p[1]) * dy) / (dx * dx + dy * dy)
    h = (p[0] + t * dx, p[1] + t * dy)
    seg(ax, apex, h, lw=AUX)
    right_angle(ax, h, side, 1 if apex[1] > h[1] else -1)
    return h


def polar(c, r, deg):
    return (c[0] + r * math.cos(math.radians(deg)),
            c[1] + r * math.sin(math.radians(deg)))


def arc_pts(c, r, t1, t2, n=48):
    """호 위의 점 목록. shade에 이어 붙여 곡선 경계를 만든다."""
    return [polar(c, r, t1 + (t2 - t1) * i / n) for i in range(n + 1)]


# ── 길이 표시 ───────────────────────────────────────────────────────────

def dim(ax, p, q, text, side=1, gap=None, trim=0.0, lw=AUX):
    """p에서 q까지의 길이 표시. 두 점을 side 쪽으로 gap(좌표 단위)만큼 부푼 점선
    곡선으로 잇고, 곡선 한가운데를 글만큼 끊어 그 자리에 글을 앉힌다.

    side: 진행 방향의 왼쪽이 +1. 도형 둘레를 반시계로 돌 때 바깥쪽은 -1이다.
    gap: 생략하면 글이 도형에 닿지 않는 만큼 — 가로 곡선은 10pt쯤, 세로 곡선은 글이
         가로로 놓이므로 글 너비 절반 + 6pt. pt로 주려면 gap=g.pt(ax, 12).
    trim: 양끝을 안쪽으로 물리는 길이(pt). 꼭짓점에 선이 여럿 모여 붐빌 때 쓴다.
    글이 없으면(text="") 곡선만 긋고 꼭대기 좌표를 돌려준다. 글이 현의 8할을 넘으면
    곡선이 거의 다 끊기니 그렇게 하고 leader()로 글을 밖에 둔다."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    if trim:
        t = pt(ax, trim)
        p = (p[0] + ux * t, p[1] + uy * t)
        q = (q[0] - ux * t, q[1] - uy * t)
        L -= 2 * t
    nx, ny = -uy * side, ux * side          # side 쪽 법선
    w, h = text_size(ax, text) if text else (0.0, 0.0)
    if gap is None:
        gap = pt(ax, (abs(nx) * w + abs(ny) * h) / 2 + 6.0)
    mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    cx, cy = mx + nx * 2 * gap, my + ny * 2 * gap      # 2차 베지어 제어점(꼭대기가 gap)
    apex = (mx + nx * gap, my + ny * gap)

    def bez(t):
        return ((1 - t) ** 2 * p[0] + 2 * (1 - t) * t * cx + t ** 2 * q[0],
                (1 - t) ** 2 * p[1] + 2 * (1 - t) * t * cy + t ** 2 * q[1])

    def draw(t0, t1):
        pts = [bez(t0 + (t1 - t0) * i / 24) for i in range(25)]
        ax.plot([x for x, _ in pts], [y for _, y in pts], color=INK, linewidth=lw,
                linestyle=DASH, dash_capstyle="butt")

    if not text:
        draw(0, 1)
        return apex
    along = abs(ux) * w + abs(uy) * h + 2 * PAD     # 글이 현 방향으로 차지하는 길이(pt)
    if along > 0.8 * L * ax.pt:
        warn(f"길이 글 '{text}'({along:.0f}pt)가 현({L * ax.pt:.0f}pt)의 8할을 넘는다. "
             "글을 빼고 leader()로 밖에 둬라")
    hh = min(along / 2 / ax.pt / L, 0.4)         # 매개변수 t 기준 반폭. 현 방향 성분은 t에 비례한다
    draw(0, 0.5 - hh)
    draw(0.5 + hh, 1)
    label(ax, apex[0], apex[1], text)
    return apex


def leader(ax, p, text, dx=3, dy=2, length=LEADER):
    """p에서 (dx, dy) 방향으로 length pt의 지시선(보조선)을 긋고 끝에서 3pt 떨어져
    글을 둔다. dim(…, "")이 돌려준 꼭대기에서 글을 밖으로 뺄 때 쓴다."""
    n = math.hypot(dx, dy)
    ex, ey = dx / n, dy / n
    q = (p[0] + pt(ax, length) * ex, p[1] + pt(ax, length) * ey)
    seg(ax, p, q, lw=AUX)
    t = (q[0] + pt(ax, 3.0) * ex, q[1] + pt(ax, 3.0) * ey)
    ha = "left" if dx > 0 else "right" if dx < 0 else "center"
    va = "bottom" if dy > 0 else "top" if dy < 0 else "center"
    label(ax, t[0], t[1], text, ha=ha, va=va)
    return q
