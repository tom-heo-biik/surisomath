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

본문 안 수식은 inline()이 그린다. build.py가 problems.yaml의 $…$를 찾아 부른다.
"""
from __future__ import annotations

import math
import os
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
DASH = (0, (2, 2))     # 점선. matplotlib이 선 두께를 곱하므로 0.4pt 선에서 0.8pt 등간격이 된다
DASHDOT = (6, 2, 1, 2) # 일점쇄선(pt): 긴 획 6, 빈 2, 점 1, 빈 2. 회전축
TICK = 5.0             # 같은 길이 표시 획의 길이(pt)
MARK = 5.5             # 직각 표시 한 변(pt)
MARGIN = 4.0           # 잉크에서 캔버스 가장자리까지 최소(pt). 잘리지 않게
LEADER = 22.0          # 지시선 길이(pt)
PAD = 2.0              # 길이 글 양옆에 비우는 점선 길이(pt)
SLACK = 22.0           # 위아래 여백이 이보다 크면 그림이 블록에 비해 작다

OUT = None             # setup()이 단원 폴더의 figures/ 로 잡는다

# dfrac에서 분자 기준선을 올리는 양과 분모 기준선을 내리는 양(em). 22pt 글줄 상자
# (KoPub 12pt: 베이스라인 위 14.4pt·아래 7.6pt)에 분수가 통째로 들도록 잡은 값이다.
# 12pt에서 b/x가 위 13.8pt·아래 4.8pt, 20/100이 위 13.3pt·아래 6.9pt, 가장 큰 b/y가
# 22pt. TeX 디스플레이 규격(num1 0.677·denom1 0.686em)은 25.8pt라 22pt 행간에서
# 잇단 줄의 분수가 3.8pt 겹친다. 환경 변수 GRIND_FRAC="0.68,0.69"처럼 주면 다른
# 값을 시험할 수 있다
FRAC_NUM, FRAC_DEN = (float(s) for s in os.environ.get("GRIND_FRAC", "0.46,0.40").split(","))
FRAC_RULE = 0.04       # 분수 가로줄 두께(em). TeX 규격. mathtext의 밑줄 두께(0.075em)는 굵고,
                       # 최소 간격(3θ)까지 부풀려 분수가 22pt를 넘게 만든다


def warn(msg: str) -> None:
    """경고 한 줄. build.py가 이 '!' 줄을 세어 종료 코드를 정한다."""
    print(f"  ! {msg}")


def setup(script_file: str) -> Path:
    """단원 figures.py의 __file__을 받아 그 옆 figures/ 를 출력 폴더로 잡는다.
    figures.py 첫머리에서 반드시 부른다."""
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


LABEL_TOL = 1.5        # 글자 상자를 안쪽으로 이만큼(pt) 줄인 뒤 선·다른 글자와 겹치는지 본다.
                       # 각도 글이 좁은 각의 두 변에 스치는 것은 봐주고, 선이 글자 한가운데를
                       # 지나는 것만 잡는다


def _check_labels(f, ax, filename: str) -> int:
    """글자가 선(Line2D)·테두리가 보이는 패치(원·호)·다른 글자와 겹치면 경고한다. 이차함수
    그림에서 점 이름이 곡선 위에 앉거나 곡선 이름끼리 겹친 것을 눈으로만 잡았다 — 이건 기계가
    잴 수 있는 일이다. 원은 Circle 패치라 선만 보던 때는 놓쳤다(원과직선 019의 O₂ 이름 위로
    큰 원의 둘레가, 020의 13cm 위로 원 O'의 둘레가 지났다). 색칠·화살촉처럼 테두리가 없는
    패치는 보지 않는다 — 색칠은 글 뒤에 깔린다. 각도 글은 호에서 pad만큼 떨어져 있어 안 걸린다."""
    r = f.canvas.get_renderer()
    k = 72 / f.dpi
    boxes = []
    for t in ax.texts:
        if not t.get_visible() or not t.get_text():
            continue
        bb = t.get_window_extent(r)
        x0, y0, x1, y1 = bb.x0 * k + LABEL_TOL, bb.y0 * k + LABEL_TOL, bb.x1 * k - LABEL_TOL, bb.y1 * k - LABEL_TOL
        if x1 > x0 and y1 > y0:
            boxes.append((t.get_text(), x0, y0, x1, y1))
    bad = 0
    for i, (s, a0, b0, a1, b1) in enumerate(boxes):
        for u, c0, d0, c1, d1 in boxes[i + 1:]:
            if a0 < c1 and c0 < a1 and b0 < d1 and d0 < b1:
                warn(f"{filename}: 글 '{s}'와 '{u}'가 겹친다. 한쪽을 옮겨라")
                bad += 1
    strokes = []                                        # (종류, 꺾은선 목록) — 선과 테두리가 보이는 패치
    for line in ax.lines:
        if not line.get_visible() or line.get_linestyle() in ("None", "none", " ", ""):
            continue                                    # 점(marker)만 있는 것
        strokes.append(("선", [line.get_transform().transform_path(line.get_path()).vertices]))
    for p in ax.patches:
        if not p.get_visible() or not (p.get_linewidth() or 0):
            continue
        ec = p.get_edgecolor()
        if ec is None or (len(ec) == 4 and ec[3] == 0):
            continue                                    # 색칠·화살촉 — 테두리가 없다
        path = p.get_transform().transform_path(p.get_path())
        strokes.append(("원", path.to_polygons(closed_only=False)))   # 원·호를 꺾은선으로 편다
    for kind, polys in strokes:
        pts = []
        for verts in polys:
            for (px, py), (qx, qy) in zip(verts[:-1], verts[1:]):
                px, py, qx, qy = px * k, py * k, qx * k, qy * k
                n = max(1, int(math.hypot(qx - px, qy - py) / 0.5))   # 0.5pt마다 한 점
                pts.extend((px + (qx - px) * j / n, py + (qy - py) * j / n) for j in range(n + 1))
        for s, a0, b0, a1, b1 in boxes:
            if any(a0 <= x <= a1 and b0 <= y <= b1 for x, y in pts):
                hint = "글을 옮기거나 선을 잘라라" if kind == "선" else "글을 옮겨라"
                warn(f"{filename}: 글 '{s}'를 {kind}이 지난다. {hint}")
                bad += 1
    return bad


def _stroke_points(ax, k: float) -> list:
    """선(Line2D)과 테두리가 보이는 패치(원·호)를 0.5pt 간격의 점으로 편다(pt, 캔버스 기준)."""
    polys = []
    for line in ax.lines:
        if not line.get_visible() or line.get_linestyle() in ("None", "none", " ", ""):
            continue
        polys.append(line.get_transform().transform_path(line.get_path()).vertices)
    for p in ax.patches:
        if not p.get_visible() or not (p.get_linewidth() or 0):
            continue
        ec = p.get_edgecolor()
        if ec is None or (len(ec) == 4 and ec[3] == 0):
            continue
        polys.extend(p.get_transform().transform_path(p.get_path()).to_polygons(closed_only=False))
    pts = []
    for verts in polys:
        for (px, py), (qx, qy) in zip(verts[:-1], verts[1:]):
            px, py, qx, qy = px * k, py * k, qx * k, qy * k
            n = max(1, int(math.hypot(qx - px, qy - py) / 0.5))
            pts.extend((px + (qx - px) * j / n, py + (qy - py) * j / n) for j in range(n + 1))
    return pts


SHADE_TOL = 0.8        # 색칠 경계의 표본점이 이 거리(pt) 안에 선이 없으면 "선 없는 변"이다
SHADE_MIN = 3.0        # 이보다 짧은 변은 보지 않는다(곡선 경계의 잔 토막, 기둥 꼭대기)


def _check_shades(f, ax, filename: str) -> int:
    """색칠한 부분(테두리 없는 반투명 패치)의 변마다 실제로 선이 그어져 있는지 잰다. 삼각비2 027에서
    사각형 EFHG를 칠하고 변 EF를 안 그어 색칠 경계 한 변이 비었는데 눈 검토가 놓쳤다(2026-09-23
    선생님 지적). gid가 "noedge"인 패치(지면 띠 같은 장식)는 보지 않는다."""
    k = 72 / f.dpi
    strokes = None
    bad = 0
    for p in ax.patches:
        if not p.get_visible() or p.get_gid() == "noedge":
            continue
        fc = p.get_facecolor()
        if fc is None or len(fc) < 4 or fc[3] == 0 or fc[3] >= 0.99:
            continue                                    # 색칠은 반투명 틴트. 화살촉·검은 쐐기는 불투명
        ec = p.get_edgecolor()
        if ec is not None and len(ec) == 4 and ec[3] > 0 and (p.get_linewidth() or 0):
            continue                                    # 제 테두리가 있다
        if strokes is None:
            strokes = _stroke_points(ax, k)
        for verts in p.get_transform().transform_path(p.get_path()).to_polygons():
            for (px, py), (qx, qy) in zip(verts, list(verts[1:]) + [verts[0]]):
                px, py, qx, qy = px * k, py * k, qx * k, qy * k
                L = math.hypot(qx - px, qy - py)
                if L < SHADE_MIN:
                    continue
                for j in range(1, 6):                   # 변 안쪽 다섯 점
                    x, y = px + (qx - px) * j / 6, py + (qy - py) * j / 6
                    if not any(abs(x - sx) <= SHADE_TOL and abs(y - sy) <= SHADE_TOL for sx, sy in strokes):
                        warn(f"{filename}: 색칠한 부분의 변(({px:.0f}, {py:.0f})~({qx:.0f}, {qy:.0f})pt)에 "
                             "선이 없다. 경계를 그어라")
                        bad += 1
                        break
                else:
                    continue
                break
    return bad


def _names(texts: list) -> list:
    """그림 글자 목록에서 점 이름(대문자, 프라임·첨자 포함)만 뽑는다. 'A', "$\\mathrm{O}'$", "$\\mathrm{O}_2$" →
    A, O', O2. 한글·숫자·소문자 변수·각도는 뺀다."""
    import re
    out = []
    for s in texts:
        s = s.strip()
        if re.fullmatch(r"[A-Z]'?", s):
            out.append(s)
            continue
        for m in NAME_RX.finditer(s):
            letters, suffix = m.group(1), (m.group(3) or ("'" if m.group(2) == "'" else ""))
            if suffix.isalpha():                        # \mathrm{A}_n — 수열 이름(정사각형 Aₙ)이지 점이 아니다
                continue
            if suffix:                                  # \mathrm{AB}' → A, B'
                out.extend(letters[:-1])
                out.append(letters[-1] + suffix)
            else:
                out.extend(letters)
    return out


NAME_RX = __import__("re").compile(r"\\mathrm\{([A-Z]+)\}('|_\{?([0-9a-z])\}?)?")   # 점 이름: 대문자, 프라임, 첨자


def save(f, filename: str) -> Path:
    """x 범위를 잉크 기준 좌우 대칭으로 잡아 SVG로 저장한다. 위아래 여백이 모자라거나
    지나치게 남으면 y 범위를 얼마로 바꾸면 되는지 알려 준다. 글자가 선이나 다른 글자와
    겹치면(_check_labels), 색칠한 부분의 변에 선이 없으면(_check_shades) 경고한다. 그림의 점
    이름 목록을 SVG 끝에 주석(<!-- names: … -->)으로 남겨 build.py가 지문의 점 이름과 맞춰 본다."""
    if OUT is None:
        raise RuntimeError("g.setup(__file__)을 먼저 불러라. 출력 폴더가 정해지지 않았다")
    ax = f.axes[0]
    H = ax.units * GRID
    scale = ax.pt
    X0, X1 = ax.get_xlim()
    Y0, Y1 = ax.get_ylim()
    W = f.get_size_inches()[0] * 72
    bx0, by0, bx1, by1 = _ink_bbox(f, ax)
    _check_labels(f, ax, filename)
    _check_shades(f, ax, filename)
    names = _names([t.get_text() for t in ax.texts if t.get_visible()])

    # x — 잉크 너비에 좌우 MARGIN을 더한 만큼으로 캔버스를 좁히고 잉크를 가운데 둔다
    cx = X0 + (bx0 + bx1) / 2 / W * (X1 - X0)
    w = bx1 - bx0 + 2 * MARGIN
    if w > WIDTH:
        warn(f"{filename}: 그림 너비 {w:.0f}pt가 본문 너비 {WIDTH:.0f}pt를 넘는다. "
             "y 범위를 넓혀 배율을 줄여라")
        w = WIDTH
    f.set_size_inches(w * PT, H * PT)
    ax.set_xlim(cx - w / 2 / scale, cx + w / 2 / scale)

    # y — 배율을 바꾸는 일이라 손으로 정한다. 얼마로 바꾸면 되는지 일러 준다.
    # 도형은 배율을 따라 커지지만 글자와 선 두께는 pt로 고정이다. 둘을 갈라 셈해야
    # 알려 준 값이 한 번에 맞는다. 뭉뚱그리면 글이 많은 그림에서 범위가 0으로 빨려 든다.
    gap = min(by0, H - by1)
    if gap < MARGIN or gap > SLACK:
        cy = Y0 + (by0 + by1) / 2 / H * (Y1 - Y0)
        shape = ax.dataLim.height                 # 배율을 따라 커지는 몫(좌표 단위)
        if not math.isfinite(shape):              # 도형이 하나도 없으면 무한대로 온다
            shape = 0.0
        fixed = (by1 - by0) - shape * scale       # pt로 고정인 몫(글자·선 두께)
        room = H - fixed - 2 * (MARGIN + 1)
        how = "모자란다" if gap < MARGIN else "남는다"
        if shape > 0 and room > 0:
            span = shape * H / room
            warn(f"{filename}: 위아래 여백 {gap:.1f}pt. {how}. "
                 f"y 범위를 ({cy - span / 2:.2f}, {cy + span / 2:.2f})로 잡아라")
        else:
            warn(f"{filename}: 위아래 여백 {gap:.1f}pt. {how}. 글자와 선만으로 "
                 f"{fixed:.0f}pt를 차지한다. units를 {'키워라' if gap < MARGIN else '줄여라'}")

    print(f"  {filename}  ({w:.0f}×{H:.0f}pt)")
    path = OUT / filename
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        f.savefig(fh, format="svg", transparent=True, metadata={"Date": None})
    plt.close(f)
    with open(path, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(f"<!-- names: {' '.join(sorted(set(names)))} -->\n")
    return path


# ── 본문 안 수식 ────────────────────────────────────────────────────────

def inline(tex: str, path: Path, size: float = 12.0, color: str = INK,
           pad: float = 0.5) -> tuple[float, float, float]:
    """수식 한 토막($ 없이)을 Computer Modern로 그려 SVG로 저장한다. 상자는 잉크에
    pad pt 여백을 두고 딱 맞춘다. (너비, 높이, 깊이)를 pt로 돌려준다. 깊이는
    베이스라인이 상자 바닥에서 얼마나 위인지다 — HTML에서 img에 height와
    vertical-align: -깊이 를 주면 글줄의 베이스라인에 앉는다.

    글자와 선 두께처럼 배율이 없는 그림이라 TextPath로 잉크 경계를 잰다.
    Text.get_window_extent는 글꼴 상자를 돌려줘 실제 잉크보다 위아래로 3pt쯤
    크다. 그 값으로 앉히면 수식이 베이스라인 위에 떠 보인다.

    분수는 \\dfrac을 쓴다. 배치는 _tex_fraction()이 바꿔 두어 12pt에서 b/x가 위 13.8pt·
    아래 4.8pt, 가장 큰 b/y가 22pt로 KoPub 12pt 글줄 상자(위 14.4pt·아래 7.6pt) 안에
    든다. 그래서 분수 줄이 잇달아도 안 겹친다. 상자를 넘는 수식(겹분수,
    큰 괄호)은 build.py가 img에 음수 여백을 줘 글줄만은 22pt로 지킨다. \\frac은
    분자·분모가 7할로 줄어 교과서와 다르다. mathtext에는 \\tfrac이 없다."""
    from matplotlib.font_manager import FontProperties
    from matplotlib.patches import PathPatch
    from matplotlib.textpath import TextPath

    prop = FontProperties(size=size)
    s = f"${tex}$"
    x0, y0, x1, y1 = TextPath((0, 0), s, size=size, prop=prop).get_extents().extents
    W, H = x1 - x0 + 2 * pad, y1 - y0 + 2 * pad
    D = pad - y0
    f = plt.figure(figsize=(W * PT, H * PT))
    f.patch.set_alpha(0)
    ax = f.add_axes((0, 0, 1, 1))
    ax.axis("off")
    ax.set_aspect("equal")
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.add_patch(PathPatch(TextPath((pad - x0, D), s, size=size, prop=prop),
                           facecolor=color, edgecolor="none", linewidth=0))
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        f.savefig(fh, format="svg", transparent=True, metadata={"Date": None})
    plt.close(f)
    return W, H, D


def _tex_fraction() -> None:
    """mathtext의 분수 배치를 TeX 방식으로 바꿔 끼운다.

    matplotlib은 분자·분모를 가로줄에서 선 두께의 두 배(1pt)만 띄워 분수가 납작하다.
    TeX처럼 분자 기준선을 올리고 분모 기준선을 내리되(디스플레이 스타일 dfrac은
    FRAC_NUM·FRAC_DEN, 텍스트 스타일 frac은 cmsy num2·denom2), 가로줄과 최소 3θ
    (frac은 θ)를 띄우고 가로줄을 = 의 한가운데(축 높이)에 둔다. 올리고 내리는 양은
    TeX 디스플레이 값이 아니라 22pt 글줄 안에 드는 값이다(FRAC_NUM 주석). 12pt에서
    분자와 가로줄 사이 2.3pt, 가로줄과 분모 사이 2.4pt — 교과서 본문 속 분수처럼 선다.
    가로줄 두께도 TeX 규격(FRAC_RULE)이다. mathtext의 밑줄 두께로 3θ를 띄우면 키 큰
    분모(숫자, b)가 22pt를 넘긴다.

    matplotlib 3.10의 Parser._genfrac을 바꾼다. 안의 상자 클래스가 없는 판에서는
    그대로 둔다."""
    import matplotlib._mathtext as mt

    if getattr(mt.Parser._genfrac, "_tex", False):
        return
    try:
        HCentered, Vlist, Vbox, Hrule, Hlist, Hbox = (
            mt.HCentered, mt.Vlist, mt.Vbox, mt.Hrule, mt.Hlist, mt.Hbox)
    except AttributeError:
        return

    def _genfrac(self, ldelim, rdelim, rule, style, num, den):
        state = self.get_state()
        em = state.fontsize * state.dpi / 72.0
        theta = FRAC_RULE * em                        # 가로줄 두께. TeX 규격 0.04em
        t = 0.0 if rule == 0 else theta               # binom처럼 줄이 없으면 0
        for _ in range(style.value):
            num.shrink()
            den.shrink()
        cnum, cden = HCentered([num]), HCentered([den])
        width = max(num.width, den.width)
        cnum.hpack(width, "exactly")
        cden.hpack(width, "exactly")
        m = state.fontset.get_metrics(state.font, matplotlib.rcParams["mathtext.default"],
                                      "=", state.fontsize, state.dpi)
        axis = (m.ymax + m.ymin) / 2                  # = 의 한가운데
        if style.value == 0:                          # 디스플레이 스타일(dfrac)
            u, v, phi = FRAC_NUM * em, FRAC_DEN * em, 3 * theta
        else:                                         # 텍스트 스타일(frac)
            u, v, phi = 0.393732 * em, 0.344841 * em, theta
        gap_num = max(u - cnum.depth - (axis + t / 2), phi)
        gap_den = max((axis - t / 2) - (cden.height - v), phi)
        vlist = Vlist([cnum, Vbox(0, gap_num), Hrule(state, t), Vbox(0, gap_den), cden])
        vlist.shift_amount = cden.height + gap_den + t / 2 - axis
        result = [Hlist([vlist, Hbox(0.12 * em)])]    # 뒤 여백. TeX nulldelimiterspace
        if ldelim or rdelim:
            return self._auto_sized_delimiter(ldelim or ".", result, rdelim or ".")
        return result

    _genfrac._tex = True
    mt.Parser._genfrac = _genfrac


def _tex_sqrt() -> None:
    """mathtext의 근호 배치를 TeX 방식으로 바꿔 끼운다.

    matplotlib은 근호 안 내용의 양옆에 밑줄 두께의 두 배(12pt에서 2pt)씩 빈 상자를 붙이고
    그 위까지 가로줄을 긋는다. 그래서 √3 뒤가 2pt쯤 비어 "√3 일 때", "1 : √3 ,"처럼
    글자·쉼표가 떨어져 보인다(2026-09-26 독립 검토 셋이 세 단원에서 다 잡았다). TeX는
    가로줄을 내용의 너비만큼만 긋는다(The TeXbook 부록 G 규칙 11). 오른쪽 상자를 없애고
    왼쪽은 근호 획과 내용이 붙지 않게 밑줄 두께 하나만 둔다. 나머지는 matplotlib 3.10의
    Parser.sqrt 그대로다. 안의 상자 클래스가 없는 판에서는 그대로 둔다."""
    import matplotlib._mathtext as mt

    if getattr(mt.Parser.sqrt, "_tex", False):
        return
    try:
        AutoHeightChar, Hlist, Hbox, Vlist, Hrule, Glue, Box, Kern = (
            mt.AutoHeightChar, mt.Hlist, mt.Hbox, mt.Vlist, mt.Hrule, mt.Glue, mt.Box, mt.Kern)
    except AttributeError:
        return

    def sqrt(self, toks):
        root = toks.get("root")
        body = toks["value"]
        state = self.get_state()
        thickness = state.get_current_underline_thickness()
        height = body.height - body.shift_amount + thickness * 5.0
        depth = body.depth + body.shift_amount
        check = AutoHeightChar(r"\__sqrt__", height, depth, state, always=True)
        height = check.height - check.shift_amount
        depth = check.depth + check.shift_amount
        padded_body = Hlist([Hbox(thickness), body])          # TeX처럼 오른쪽 여백 없음
        rightside = Vlist([Hrule(state), Glue("fill"), padded_body])
        rightside.vpack(height + (state.fontsize * state.dpi) / (100.0 * 12.0), "exactly", depth)
        if not root:
            root = Box(check.width * 0.5, 0.0, 0.0)
        else:
            root = Hlist(root)
            root.shrink()
            root.shrink()
        root_vlist = Vlist([Hlist([root])])
        root_vlist.shift_amount = -height * 0.6
        return [Hlist([root_vlist, Kern(-check.width * 0.5), check, rightside])]

    sqrt._tex = True
    mt.Parser.sqrt = sqrt
    try:                                                      # 이미 만든 파서가 있으면 새로 만들게
        import matplotlib.mathtext as mathtext
        mathtext.MathTextParser._parser = None
    except AttributeError:
        pass


_tex_fraction()
_tex_sqrt()


# ── 기본 도형 ───────────────────────────────────────────────────────────
# 색칠을 먼저 하고 선을 나중에 긋는다. 순서가 곧 위아래다.

def seg(ax, p, q, lw=EDGE, dashed=False):
    """선분. dashed면 점선 도형의 변 — 대시 2pt 간격 2pt. matplotlib이 대시 길이에
    선 두께를 곱하므로 나눠서 준다."""
    style = (dict(linestyle=(0, (2 / lw, 2 / lw)), dash_capstyle="butt") if dashed
             else dict(solid_capstyle="round"))
    ax.plot([p[0], q[0]], [p[1], q[1]], color=INK, linewidth=lw, **style)


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
            linewidth=0, color=INK, linestyle="none", zorder=5)


def label(ax, x, y, s, ha="center", va="center", size=LABEL):
    ax.text(x, y, s, ha=ha, va=va, fontsize=size, color=INK)


def shade(ax, pts):
    """꼭짓점 목록으로 닫힌 다각형을 잉크 10% 틴트로 칠한다. 호는 arc_pts로 만든다."""
    ax.add_patch(Polygon(pts, closed=True, facecolor=INK, alpha=TINT,
                         edgecolor="none"))


def wedge(ax, c, r, t1, t2):
    """부채꼴을 잉크 10% 틴트로 칠한다."""
    ax.add_patch(Wedge(c, r, t1, t2, facecolor=INK, alpha=TINT, edgecolor="none"))


def corner_mark(ax, corner, u, v, s=None):
    """corner에서 방향 u와 v(단위벡터 둘)로 한 변 s인 직각 표시. 축에 나란하지 않아도 된다."""
    if s is None:
        s = pt(ax, MARK)
    x, y = corner
    a = (x + u[0] * s, y + u[1] * s)
    c = (x + v[0] * s, y + v[1] * s)
    b = (a[0] + v[0] * s, a[1] + v[1] * s)
    ax.plot([a[0], b[0], c[0]], [a[1], b[1], c[1]], color=INK, linewidth=AUX)


def right_angle(ax, corner, dx, dy, s=None):
    """꼭짓점 corner에서 (dx, dy) 방향(각 ±1)으로 직각 표시. 한 변 s는 생략하면 MARK pt."""
    corner_mark(ax, corner, (dx, 0), (0, dy), s)


def poly(ax, pts, lw=EDGE, dashed=False):
    """꼭짓점 목록으로 닫힌 다각형(삼각형 등)을 그린다. dashed면 점선 도형(007의 A'BC').
    목록을 그대로 돌려준다."""
    for i in range(len(pts)):
        seg(ax, pts[i], pts[(i + 1) % len(pts)], lw=lw, dashed=dashed)
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
    직각 표시는 밑변을 따라 side 쪽(+1은 p→q 방향, -1은 그 반대)에 둔다.
    밑변이 기울어도 표시가 두 선에 붙는다. 발의 좌표를 돌려준다."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    t = ((apex[0] - p[0]) * dx + (apex[1] - p[1]) * dy) / (L * L)
    h = (p[0] + t * dx, p[1] + t * dy)
    seg(ax, apex, h, lw=AUX)
    n = math.hypot(apex[0] - h[0], apex[1] - h[1])
    if n > 0:
        corner_mark(ax, h, (dx / L * side, dy / L * side),
                    ((apex[0] - h[0]) / n, (apex[1] - h[1]) / n))
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


# ── 각 · 같은 길이 · 회전축 · 이름 ──────────────────────────────────────

def angle(ax, v, p, q, text="", r=12.0, ticks=0, lw=AUX, pad=3.0):
    """각 표시. 꼭짓점 v에서 p 방향부터 q 방향까지(반시계) 반지름 r pt의 호를 긋고,
    글을 각 안쪽 이등분선 위, 호에서 pad pt 떨어진 자리에 앉힌다. 각도 글은
    '$35^{\\circ}$'처럼 수식으로 준다(cmr10에는 °가 없다). ticks는 같은 각 표시 — 교과서처럼 호 없이
    이등분선 위 r pt 자리에 ticks=1이면 점(•) 하나, ticks=2이면 × 하나를 찍는다(같은 각이 두 쌍이면
    한 쌍은 점, 다른 쌍은 ×. 2026-09-23 선생님 지시 — 호에 획을 긋던 것을 바꿨다). 글 없이 호만
    그리려면 text="". 글 자리(글이 없으면 호 한가운데)를 돌려준다. 좁은 각에서 글이 변에 끼면
    text=""로 두고 그 자리에서 g.leader로 글을 밖에 뺀다."""
    t1 = math.degrees(math.atan2(p[1] - v[1], p[0] - v[0]))
    t2 = math.degrees(math.atan2(q[1] - v[1], q[0] - v[0]))
    while t2 <= t1:
        t2 += 360.0
    if t2 - t1 > 180.0:
        warn(f"각 {t2 - t1:.0f}°: p→q 반시계가 우각이다. p와 q를 바꿔라")
    R = pt(ax, r)
    m = math.radians((t1 + t2) / 2)
    ux, uy = math.cos(m), math.sin(m)
    if ticks:
        cx, cy = v[0] + R * ux, v[1] + R * uy
        if ticks == 1:                                  # 점: 지름 2.2pt
            ax.add_patch(Circle((cx, cy), pt(ax, 1.1), facecolor=INK, edgecolor="none"))
        else:                                           # ×: 3pt 획 둘
            s = pt(ax, 1.5)
            seg(ax, (cx - s, cy - s), (cx + s, cy + s), lw=lw)
            seg(ax, (cx - s, cy + s), (cx + s, cy - s), lw=lw)
        return cx, cy
    arc(ax, v, R, t1, t2, lw=lw)
    if text:
        w, h = text_size(ax, text)
        d = r + pad + (abs(ux) * w + abs(uy) * h) / 2
        tx, ty = v[0] + pt(ax, d) * ux, v[1] + pt(ax, d) * uy
        label(ax, tx, ty, text)
        return tx, ty
    return v[0] + R * ux, v[1] + R * uy


def tick(ax, p, q, n=1, lw=AUX):
    """같은 길이 표시. 선분 pq 한가운데에 선분과 직각인 짧은 획(TICK pt) n개, 획 사이 2pt.
    한 쌍은 n=1, 다른 쌍은 n=2로 구분한다(중점 표시)."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    half, step = pt(ax, TICK) / 2, pt(ax, 2.0)
    mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    for i in range(n):
        k = (i - (n - 1) / 2) * step
        cx, cy = mx + ux * k, my + uy * k
        seg(ax, (cx - nx * half, cy - ny * half), (cx + nx * half, cy + ny * half), lw=lw)


def axis(ax, p, q, text="", lw=AUX):
    """회전축. 교과서대로 일점쇄선 0.4pt. text(축 이름 '$l$')는 q 끝의 오른쪽 3pt."""
    ax.plot([p[0], q[0]], [p[1], q[1]], color=INK, linewidth=lw,
            linestyle=(0, tuple(d / lw for d in DASHDOT)), dash_capstyle="butt")
    if text:
        label(ax, q[0] + pt(ax, 3.0), q[1], text, ha="left", va="center")


def name(ax, p, s, dx=0.0, dy=0.0, ha="center", va="center"):
    """점 이름·변의 길이 글. p에서 (dx, dy) pt 떨어진 자리에 10pt 정체로 앉힌다.
    시험대비처럼 변의 길이를 교과서식으로 변 옆에 적을 때 쓴다. 연마의 길이 표시는
    dim 그대로다. 점을 세로로 맞출 땐 va="baseline"."""
    label(ax, p[0] + pt(ax, dx), p[1] + pt(ax, dy), s, ha=ha, va=va)
