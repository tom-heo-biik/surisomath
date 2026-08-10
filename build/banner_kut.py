# -*- coding: utf-8 -*-
"""고려대 전국 수학 학력평가 우수단체상 배너 · 600×1800mm.

시안은 2:3인데 배너는 1:3이다. 세로가 두 배로 길어지므로 요소 크기를 시안의
'폭 대비 비율' 그대로 옮기고, 늘어난 세로는 요소 사이 간격으로만 나눠 준다.
글자를 세로에 맞춰 키우면 월계관까지 딸려 커져서 프레임을 넘는다.

바탕은 고려대 공식 크림슨 #7C001A다. assets의 엠블럼과 같은 색이라 역상 엠블럼이
바탕에 그대로 얹힌다. 엠블럼은 595px GIF뿐이므로 vectorize로 패스를 떠서 쓴다.

비즈하우스 인쇄 규약을 맞춘다. 글자는 전부 아웃라인(패스)이라 PDF에 서체가 안
들어가고, 색은 마지막에 DeviceCMYK로 바꿔 넣는다. WeasyPrint는 RGB로만 쓰므로
다 그린 뒤 내용 스트림의 rg/RG 연산자를 k/K로 갈아 끼운다.

    python build/banner_kut.py            자료/ 에 PDF를 쓴다
    python build/banner_kut.py --rgb      화면 확인용 RGB판도 같이 쓴다
    python build/banner_kut.py --parts    프레임·월계관·장식만 크게 뽑아 본다
"""
from __future__ import annotations

import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "lib"))
sys.path.insert(0, str(ROOT / "build"))

import suriso  # noqa: E402
import vectorize  # noqa: E402

# ── 판형 ────────────────────────────────────────────────────────────────
# 단위는 전부 mm다. 자료/ 의 기존 배너 두 종과 같은 규격이다.
W, H = 600.0, 1800.0

# ── 색 ──────────────────────────────────────────────────────────────────
CRIMSON = "#7C001A"      # 고려대 공식 크림슨. assets 엠블럼에서 그대로 뽑았다
GOLD = "#FDB302"         # 우수단체상·월계관·별·프레임·괘선·장식
GOLD_LINE = GOLD         # 시안은 괘선을 반 톤 옅게 썼지만 CMYK로는 Y가 7밖에
WHITE = "#FFFFFF"        # 안 벌어져 같은 색으로 찍힌다. 그래서 하나로 합쳤다

# 인쇄 정본은 이쪽이다. RGB는 화면 확인용이고, 마지막에 이 값으로 바꿔 넣는다.
# 시스템 ICC(sRGB → U.S. Web Coated SWOP, 상대색도)로 뽑은 값을 정수로 정리했다.
# 크림슨은 4도 252%인데 실사출력에서는 넉넉히 안전한 잉크량이고, 금색은 2도라
# 비즈하우스가 권하는 '1~2도' 그대로다.
CMYK = {
    CRIMSON: (31, 98, 72, 51),
    GOLD: (0, 37, 98, 0),
    WHITE: (0, 0, 0, 0),
}

# ── 프레임 ──────────────────────────────────────────────────────────────
FRAME = 26.0             # 바깥 여백
FRAME_R = 22.0           # 모서리를 오목하게 파는 반지름
FRAME_W = 2.4            # 선 두께

# ── 세로 배치 ───────────────────────────────────────────────────────────
# 값은 전부 '잉크 윗변'이다. 글자 상자의 위가 아니라 획이 시작되는 자리.
# 묶음 사이는 106mm로 고르게 벌리고, 묶음 안(소제목-제목 55mm, 행간 85·34mm)과
# 괘선-월계관(47mm)만 좁힌다. 위 여백 130mm · 아래 153mm.
EMBLEM_TOP, EMBLEM_W = 156.0, 250.0
EYEBROW_TOP = 599.0
TITLE1_TOP = 695.0
TITLE_LEAD = 85.0        # 제목 두 줄의 잉크 윗변 사이 거리
RULE_TOP_Y = 955.0
AWARD_MID = 1071.0       # 우수단체상 잉크 한가운데
RULE_BOT_Y = 1187.0
ACADEMY_TOP = 1293.0
FLOURISH_Y = 1464.0
EN1_TOP = 1570.0
EN_LEAD = 34.0

# ── 가로 크기 ───────────────────────────────────────────────────────────
# 우수단체상만 시안의 폭 비율 그대로 두고, 나머지는 프레임 안쪽 546mm가 허락하는
# 데까지 키웠다. 잉크 높이가 우수단체상 79 > 제목 69 > 학원명 65 > 소제목 40 >
# 영문 17mm 순으로 떨어져 위계는 그대로다.
EYEBROW_W = 330.0        # 2026년도 상반기
TITLE_W = 420.0          # 수학 학력평가 (긴 줄 기준)
AWARD_W = 374.0          # 우수단체상
ACADEMY_W = 455.0        # 수리소 수학학원

# 학원명을 실제 워드마크로 앉힐지, Pretendard로 짤지. 워드마크가 정본이다.
ACADEMY_LOGO = True
EN_SIZE = 23.5           # 영문 두 줄은 크기를 고정하고 자간으로 폭을 맞춘다
EN_TRACK = 0.08          # 키운 만큼 자간을 좁혀야 아랫줄이 학원명보다 넓어지지 않는다

LAUREL_W, LAUREL_H = 58.0, 138.0   # 월계관 한 가지
LAUREL_GAP = 6.0                   # 월계관과 글자 사이
RULE_SPAN = 485.0                  # 별 괘선 전체 폭
STAR_R = 13.5
FLOURISH_W = 340.0

TEXT = {
    "eyebrow": "2026년도 상반기",
    "title1": "고려대 전국",
    "title2": "수학 학력평가",
    "award": "우수단체상",
    "academy": "수리소 수학학원",
    "en1": "KOREA UNIVERSITY",
    "en2": "MATHEMATICS EVALUATION TEST",
}

FONT = suriso.PRETENDARD[700]


# ── 서체 ────────────────────────────────────────────────────────────────
# 비즈하우스가 "아웃라인되지 않은 서체는 인쇄되지 않거나 다른 서체로 교체될 수
# 있다"고 못박아 두었다. 그래서 글자를 조판하지 않고 글리프 윤곽을 직접 패스로
# 떠서 앉힌다. 결과 PDF에는 서체가 한 벌도 안 들어간다.
_TT = None


def _tt():
    global _TT
    if _TT is None:
        from fontTools.ttLib import TTFont

        _TT = TTFont(str(FONT))
    return _TT


def _glyphs(text: str) -> list[tuple[str, int]]:
    """글자마다 (글리프 이름, 나비)를 폰트 단위로."""
    f = _tt()
    cmap, hmtx = f.getBestCmap(), f["hmtx"]
    out = []
    for ch in text:
        gname = cmap.get(ord(ch))
        if gname is None:
            raise ValueError(f"{FONT.name}에 없는 글자입니다: {ch!r}")
        out.append((gname, hmtx[gname][0]))
    return out


def _upm() -> int:
    return _tt()["head"].unitsPerEm


def advance(text: str, track: float = 0.0) -> float:
    """글줄 폭을 em으로. track은 em 단위 자간이며 글자 사이에만 들어간다."""
    return sum(a for _, a in _glyphs(text)) / _upm() + track * (len(text) - 1)


def ink(text: str) -> tuple[float, float]:
    """잉크 상자의 (윗변, 높이)를 em으로. 윗변은 기준선에서 위로 잰 값이다."""
    from fontTools.pens.boundsPen import BoundsPen

    gset = _tt().getGlyphSet()
    ys: list[float] = []
    for gname, _ in _glyphs(text):
        pen = BoundsPen(gset)
        gset[gname].draw(pen)
        if pen.bounds:
            ys += [pen.bounds[1], pen.bounds[3]]
    upm = _upm()
    return max(ys) / upm, (max(ys) - min(ys)) / upm


def fit(text: str, target_w: float, track: float = 0.0) -> float:
    """글줄이 target_w(mm)가 되는 글자 크기(mm)."""
    return target_w / advance(text, track)


def text_svg(text: str, size: float, top: float, fill: str, track: float = 0.0) -> str:
    """글줄을 패스로. 가로 가운데, 잉크 윗변이 top에 오도록 앉힌다.

    글리프 좌표는 기준선이 0이고 y가 위로 자란다. SVG는 y가 아래로 자라므로
    바깥 그룹에서 y를 뒤집는다.
    """
    from fontTools.pens.svgPathPen import SVGPathPen

    gset = _tt().getGlyphSet()
    upm = _upm()
    s = size / upm
    x0 = W / 2 - advance(text, track) * size / 2
    baseline = top + ink(text)[0] * size

    parts, x = [], 0.0
    for gname, adv in _glyphs(text):
        pen = SVGPathPen(gset)
        gset[gname].draw(pen)
        d = pen.getCommands()
        if d:  # 빈칸은 윤곽이 없다. 나비만 먹고 지나간다
            parts.append(f'<path transform="translate({x:.1f},0)" d="{d}"/>')
        x += adv + track * upm
    return (
        f'<g transform="translate({x0:.3f},{baseline:.3f}) scale({s:.6f},{-s:.6f})" '
        f'fill="{fill}">{"".join(parts)}</g>'
    )


# ── 도형 ────────────────────────────────────────────────────────────────
def frame_path() -> str:
    """네 모서리를 안쪽으로 오목하게 판 사각 테두리.

    모서리 원의 중심이 사각형 꼭짓점에 있다. 그래서 호가 꼭짓점에서 멀어지는
    쪽으로 부풀어 옴폭 파인다. 중심이 안쪽 대각점에 있으면 흔한 둥근 모서리다.
    """
    x0, y0, x1, y1 = FRAME, FRAME, W - FRAME, H - FRAME
    r = FRAME_R
    # 두 끝점 사이가 r√2라 원 중심이 두 군데 나온다. sweep=0이 꼭짓점 쪽 중심을
    # 골라서 호가 안으로 옴폭 들어간다. sweep=1은 흔한 둥근 모서리가 된다.
    a = f"A{r},{r} 0 0 0 "
    return (
        f"M{x0 + r},{y0} L{x1 - r},{y0} {a}{x1},{y0 + r} "
        f"L{x1},{y1 - r} {a}{x1 - r},{y1} "
        f"L{x0 + r},{y1} {a}{x0},{y1 - r} "
        f"L{x0},{y0 + r} {a}{x0 + r},{y0} Z"
    )


def star_path(cx: float, cy: float, r: float, inner: float = 0.42) -> str:
    """꼭짓점이 위를 보는 정오각별."""
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * inner
        pts.append(f"{cx + rad * math.cos(ang):.2f},{cy + rad * math.sin(ang):.2f}")
    return "M" + " L".join(pts) + " Z"


def _leaf(length: float, width: float) -> str:
    """월계수 잎 하나. 원점에서 +x 방향으로 뻗고 끝이 뾰족하다."""
    ll, w = length, width / 2
    return (
        f"M0,0 C{ll * 0.22:.2f},{-w * 1.26:.2f} {ll * 0.72:.2f},{-w * 0.92:.2f} {ll:.2f},0 "
        f"C{ll * 0.72:.2f},{w * 0.92:.2f} {ll * 0.22:.2f},{w * 1.26:.2f} 0,0 Z"
    )


def _stem(w: float, h: float):
    """줄기 삼차 베지에의 네 점. 밑동이 오른쪽 아래, 끝이 오른쪽 위다."""
    p0 = (w * 0.94, h * 1.00)
    p1 = (-w * 0.14, h * 0.78)
    p2 = (-w * 0.14, h * 0.22)
    p3 = (w * 0.80, h * 0.00)
    return p0, p1, p2, p3


def _bezier(p0, p1, p2, p3, t):
    u = 1 - t
    x = u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0]
    y = u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1]
    dx = 3 * u * u * (p1[0] - p0[0]) + 6 * u * t * (p2[0] - p1[0]) + 3 * t * t * (p3[0] - p2[0])
    dy = 3 * u * u * (p1[1] - p0[1]) + 6 * u * t * (p2[1] - p1[1]) + 3 * t * t * (p3[1] - p2[1])
    return (x, y), math.atan2(dy, dx)


def laurel(w: float, h: float, leaves: int = 12) -> tuple[str, str]:
    """월계수 가지 한 짝. (줄기 패스, 잎 패스)를 돌려준다.

    왼쪽 가지 기준이다. 오른쪽은 이것을 그대로 좌우로 뒤집어 쓴다.
    """
    p0, p1, p2, p3 = _stem(w, h)
    stem = (
        f"M{p0[0]:.2f},{p0[1]:.2f} C{p1[0]:.2f},{p1[1]:.2f} "
        f"{p2[0]:.2f},{p2[1]:.2f} {p3[0]:.2f},{p3[1]:.2f}"
    )

    lmax = h * 0.34
    out = []
    for i in range(leaves):
        t = 0.06 + 0.88 * i / (leaves - 1)
        (px, py), tangent = _bezier(p0, p1, p2, p3, t)
        # 밑동 쪽이 크고 끝으로 갈수록 작아진다. 맨 밑은 조금 줄여 뿌리를 만든다
        taper = 0.40 + 0.60 * (1 - t) ** 0.85
        ll = lmax * taper * (0.72 if i == 0 else 1.0)
        side = -1 if i % 2 == 0 else 1  # 번갈아 바깥·안쪽
        ang = tangent + side * math.radians(46)
        deg = math.degrees(ang)
        out.append(
            f'<path transform="translate({px:.2f},{py:.2f}) rotate({deg:.2f})" '
            f'd="{_leaf(ll, ll * 0.37)}"/>'
        )
    return stem, "".join(out)


def _spiral(cx, cy, r0, r1, a0, a1, n=72) -> str:
    """로그 나선 한 가닥. 장식의 소용돌이에 쓴다."""
    pts = []
    for i in range(n + 1):
        t = i / n
        a = math.radians(a0 + (a1 - a0) * t)
        r = r0 * (r1 / r0) ** t
        pts.append(f"{cx + r * math.cos(a):.2f},{cy + r * math.sin(a):.2f}")
    return "M" + " L".join(pts)


def flourish(width: float, k: float = 1.38) -> str:
    """가운데 소용돌이 장식과 좌우로 뻗는 가는 괘선. 원점이 한가운데다.

    k는 장식만 키우는 배율이다. 괘선 길이는 width가 정하므로, 배너가 커져도
    장식이 실처럼 가늘어 보이지 않게 이쪽만 따로 부풀린다.
    """
    half = width / 2
    core = 51.0 * k
    g = [
        f'<path d="M{-half:.1f},0 L{-core:.1f},0" stroke-width="1.3"/>',
        f'<path d="M{core:.1f},0 L{half:.1f},0" stroke-width="1.3"/>',
    ]
    for s in (1, -1):
        g.append(
            f'<g transform="scale({s * k:.3f},{k:.3f})">'
            # 바깥에서 안으로 크게 감아 들어오는 소용돌이
            f'<path d="{_spiral(30, 1.5, 22, 3.2, 8, 300)}" stroke-width="{1.55 / k:.3f}"/>'
            # 그 안쪽에서 반대로 말리는 작은 소용돌이
            f'<path d="{_spiral(13.5, 5.0, 11, 2.0, 250, -70)}" stroke-width="{1.35 / k:.3f}"/>'
            # 위로 뻗어 올라가는 덩굴
            f'<path d="M6,-2 C12,-13 22,-15 25,-8" stroke-width="{1.35 / k:.3f}"/>'
            f"</g>"
        )
    # 한가운데 창끝 모양
    g.append(
        f'<g transform="scale({k:.3f})"><path stroke="none" fill="{GOLD_LINE}" d="'
        "M0,-20 C2.6,-11 4.7,-6 4.7,-1 C4.7,4 2.6,9 0,18 "
        "C-2.6,9 -4.7,4 -4.7,-1 C-4.7,-6 -2.6,-11 0,-20 Z"
        '"/></g>'
    )
    return "".join(g)


# ── 조판 ────────────────────────────────────────────────────────────────
def placed(src, width: float, top: float, fill: str = WHITE, **kw) -> str:
    """로고 비트맵을 패스로 떠서 가로 가운데에, 잉크 윗변을 top에 맞춰 앉힌다."""
    d, (bx, by, bw, _) = vectorize.trace(str(src), **kw)
    s = width / bw
    return (
        f'<g transform="translate({W / 2 - width / 2 - bx * s:.3f},{top - by * s:.3f}) '
        f'scale({s:.5f})"><path fill="{fill}" fill-rule="evenodd" d="{d}"/></g>'
    )


def page_svg() -> str:
    """배너의 모든 그림. 글자는 이 위에 HTML로 얹는다."""
    g = [f'<rect width="{W}" height="{H}" fill="{CRIMSON}"/>']

    # 프레임
    g.append(
        f'<path d="{frame_path()}" fill="none" stroke="{GOLD_LINE}" '
        f'stroke-width="{FRAME_W}"/>'
    )

    # 고려대 엠블럼 — 저해상도 GIF를 패스로 뜬 것
    g.append(placed(suriso.ASSETS / "고려대학교" / "crimson1negative.gif", EMBLEM_W, EMBLEM_TOP, trim=2))

    # 수리소 워드마크 — 691px PNG를 패스로 뜬 것
    if ACADEMY_LOGO:
        g.append(placed(suriso.WORDMARK_KR, ACADEMY_W, ACADEMY_TOP))

    # 별 괘선 두 줄
    gap = STAR_R + 10
    for y in (RULE_TOP_Y, RULE_BOT_Y):
        x0, x1 = W / 2 - RULE_SPAN / 2, W / 2 + RULE_SPAN / 2
        g.append(
            f'<g fill="{GOLD_LINE}" stroke="{GOLD_LINE}" stroke-width="1.4">'
            f'<path d="M{x0},{y} L{W / 2 - gap:.1f},{y}"/>'
            f'<path d="M{W / 2 + gap:.1f},{y} L{x1},{y}"/></g>'
            f'<path fill="{GOLD}" d="{star_path(W / 2, y, STAR_R)}"/>'
        )

    # 월계관 — 글자 좌우에 한 짝씩, 오른쪽은 좌우 반전
    stem, leaves = laurel(LAUREL_W, LAUREL_H)
    ltop = AWARD_MID - LAUREL_H / 2
    inner = AWARD_W / 2 + LAUREL_GAP          # 글자 바깥쪽 끝
    for sign in (-1, 1):
        lx = W / 2 - sign * (inner + LAUREL_W)
        g.append(
            f'<g transform="translate({lx:.2f},{ltop:.2f}) scale({sign},1)" fill="{GOLD}">'
            f'<path d="{stem}" fill="none" stroke="{GOLD}" stroke-width="1.5" '
            f'stroke-linecap="round"/>{leaves}</g>'
        )

    # 장식
    g.append(
        f'<g transform="translate({W / 2},{FLOURISH_Y})" fill="none" '
        f'stroke="{GOLD_LINE}" stroke-linecap="round">{flourish(FLOURISH_W)}</g>'
    )

    # 글자 — 조판이 아니라 글리프 윤곽이다
    size_title = fit(TEXT["title2"], TITLE_W)
    size_award = fit(TEXT["award"], AWARD_W, -0.03)
    g += [
        text_svg(TEXT["eyebrow"], fit(TEXT["eyebrow"], EYEBROW_W, 0.02), EYEBROW_TOP, GOLD, 0.02),
        text_svg(TEXT["title1"], size_title, TITLE1_TOP, WHITE),
        text_svg(TEXT["title2"], size_title, TITLE1_TOP + TITLE_LEAD, WHITE),
        text_svg(
            TEXT["award"], size_award,
            AWARD_MID - ink(TEXT["award"])[1] * size_award / 2, GOLD, -0.03,
        ),
        text_svg(TEXT["en1"], EN_SIZE, EN1_TOP, WHITE, EN_TRACK),
        text_svg(TEXT["en2"], EN_SIZE, EN1_TOP + EN_LEAD, WHITE, EN_TRACK),
    ]
    if not ACADEMY_LOGO:
        g.append(text_svg(TEXT["academy"], fit(TEXT["academy"], ACADEMY_W), ACADEMY_TOP, WHITE))

    return (
        f'<svg class="art" xmlns="http://www.w3.org/2000/svg" '
        f'width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">{"".join(g)}</svg>'
    )


def build() -> str:
    return f"""<meta charset="utf-8">
<style>
@page {{ size: {W}mm {H}mm; margin: 0 }}
html, body {{ margin: 0; padding: 0; background: {CRIMSON} }}
.art {{ position: absolute; top: 0; left: 0 }}
</style>
{page_svg()}
"""


def parts_sheet() -> str:
    """프레임 모서리·월계관·별 괘선·장식만 크게 뽑아 보는 A3 시트."""
    stem, leaves = laurel(LAUREL_W, LAUREL_H)
    return f"""<meta charset="utf-8">
<style>@page {{ size: 297mm 420mm; margin: 0 }} body {{ margin:0; background:{CRIMSON} }}</style>
<svg xmlns="http://www.w3.org/2000/svg" width="297mm" height="420mm" viewBox="0 0 297 420">
  <rect width="297" height="420" fill="{CRIMSON}"/>
  <g transform="translate({-FRAME * 2.2 + 12},{-FRAME * 2.2 + 12}) scale(2.2)">
    <path d="{frame_path()}" fill="none" stroke="{GOLD_LINE}" stroke-width="{FRAME_W}"/>
  </g>
  <g transform="translate(40,180) scale(1.35)" fill="{GOLD}">
    <path d="{stem}" fill="none" stroke="{GOLD}" stroke-width="1.5" stroke-linecap="round"/>{leaves}
  </g>
  <g transform="translate(210,180) scale(-1.35,1.35)" fill="{GOLD}">
    <path d="{stem}" fill="none" stroke="{GOLD}" stroke-width="1.5" stroke-linecap="round"/>{leaves}
  </g>
  <g fill="{GOLD_LINE}" stroke="{GOLD_LINE}" stroke-width="1.4">
    <path d="M40,370 L{148.5 - STAR_R - 10},370"/><path d="M{148.5 + STAR_R + 10},370 L257,370"/>
  </g>
  <path fill="{GOLD}" d="{star_path(148.5, 370, STAR_R)}"/>
  <g transform="translate(148.5,400)" fill="none" stroke="{GOLD_LINE}" stroke-linecap="round">
    {flourish(FLOURISH_W * 0.7)}
  </g>
</svg>
"""


# ── 인쇄용 변환 ─────────────────────────────────────────────────────────
def _rgb01(hexcolor: str) -> tuple[float, float, float]:
    return tuple(int(hexcolor[i : i + 2], 16) / 255 for i in (1, 3, 5))


def to_cmyk(path: Path) -> dict[str, int]:
    """PDF 내용 스트림의 RGB 연산자를 DeviceCMYK로 갈아 끼운다.

    WeasyPrint는 RGB로만 쓴다. 다행히 이 배너가 쓰는 색은 세 가지뿐이고 전부
    `r g b rg` 꼴의 민낯 연산자로 나오므로, 값을 찾아 `c m y k k`로 바꾸면 된다.
    아는 색이 아니면 세우고 만다. 모르는 색을 조용히 흘려보내면 그게 사고다.

    투명도 상태(gs)도 같이 걷어낸다. 전부 불투명(ca=1)이라 지워도 그림이 안
    바뀌는데, 남겨 두면 인쇄소 검판에서 투명 효과로 잡힐 수 있다.
    """
    import fitz

    table = {tuple(round(v, 6) for v in _rgb01(h)): c for h, c in CMYK.items()}
    used: dict[str, int] = {}

    doc = fitz.open(path)
    for page in doc:
        for xref in page.get_contents():
            data = doc.xref_stream(xref).decode("latin-1")

            def swap(m: re.Match) -> str:
                rgb = tuple(round(float(v), 6) for v in m.group(1, 2, 3))
                hit = min(table, key=lambda t: sum(abs(a - b) for a, b in zip(t, rgb)))
                if sum(abs(a - b) for a, b in zip(hit, rgb)) > 0.004:
                    raise ValueError(f"CMYK 표에 없는 색입니다: {rgb}")
                c, mm, y, k = table[hit]
                used[f"C{c} M{mm} Y{y} K{k}"] = used.get(f"C{c} M{mm} Y{y} K{k}", 0) + 1
                op = "k" if m.group(4) == "rg" else "K"
                return f"{c / 100:g} {mm / 100:g} {y / 100:g} {k / 100:g} {op}"

            data = re.sub(r"([\d.]+) ([\d.]+) ([\d.]+) (rg|RG)\b", swap, data)
            data = re.sub(r"/[Aa]\d[\d.]* gs\s*", "", data)
            doc.update_stream(xref, data.encode("latin-1"))
        doc.xref_set_key(page.xref, "Resources/ExtGState", "null")

    tmp = path.with_suffix(".tmp.pdf")  # PyMuPDF는 열어 둔 파일에 덮어쓰지 못한다
    doc.save(tmp, deflate=True, garbage=4, clean=True)
    doc.close()
    tmp.replace(path)
    return used


def main() -> None:
    from weasyprint import HTML

    if "--parts" in sys.argv:
        out = Path(__file__).resolve().parent / "_parts.pdf"
        HTML(string=parts_sheet()).write_pdf(out)
        print(f"부품 시트: {out}")
        return

    name = "수리소_배너_KUT우수단체상_크림슨_60x180"
    html = build()

    if "--rgb" in sys.argv:  # 화면 확인용. 인쇄에는 쓰지 않는다
        rgb = ROOT / "자료" / f"{name}_RGB.pdf"
        HTML(string=html, base_url=str(ROOT)).write_pdf(rgb)
        print(f"{rgb.relative_to(ROOT)}  {rgb.stat().st_size / 1024:,.0f}KB  (RGB · 화면용)")

    out = ROOT / "자료" / f"{name}.pdf"
    HTML(string=html, base_url=str(ROOT)).write_pdf(out)
    used = to_cmyk(out)

    print(f"{out.relative_to(ROOT)}  {out.stat().st_size / 1024:,.0f}KB  (CMYK · 인쇄용)")
    for color, n in sorted(used.items(), key=lambda kv: -kv[1]):
        print(f"  {color:<22} {n:>4}회   총잉크 {sum(int(v[1:]) for v in color.split()):>3}%")
    print(f"  제목 {fit(TEXT['title2'], TITLE_W):.1f}mm · "
          f"우수단체상 {fit(TEXT['award'], AWARD_W, -0.03):.1f}mm")


if __name__ == "__main__":
    main()
