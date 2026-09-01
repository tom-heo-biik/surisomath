# -*- coding: utf-8 -*-
"""수리소 OPEN 입간판 · 590×890mm.

자료/수리소_입간판_시안_v9.html이 정본이다. 시안은 61×100cm 비율로 그려졌지만
실제 인쇄물은 590×890mm다. 시안의 CSS가 전부 비율(크기는 폭의 %, 자리는 높이의
%)로 짜여 있으므로, 같은 규칙을 새 판형에 그대로 적용한다. 시안에 임베드된 Playfair Display
Bold(woff2)와 로고 PNG 두 장을 빌드할 때 시안에서 직접 꺼내 쓰므로, 이 스크립트에
그림 자산이 따로 없다. 시안 파일 하나만 맞으면 인쇄본이 따라온다.

시안의 CSS 조판을 브라우저와 같은 수식으로 재현한다. Chrome 렌더링을 0.25mm
단위로 실측해 검증한 값이다.

  · OPEN 크기 28.48cqw, 자간 0.03em(마지막 글자 뒤 포함), 들여쓰기 0.03em 보정
  · 기준선은 타이포 메트릭(fsSelection의 USE_TYPO_METRICS 비트가 서 있다)으로,
    line-height:1의 음수 반행간까지 그대로 계산한다
  · GPOS 커닝(OP −8, PE −5)을 빼먹으면 글줄이 2.3mm 넓어진다

시안 캡션의 "OPEN 위 14.1cm"는 캡션 계산이 틀린 것이다. 실제 렌더링은 11.2cm이고
사용자는 렌더링을 보며 자리를 잡았으므로 렌더링 쪽을 정본으로 삼는다.

비즈하우스 인쇄 규약을 맞춘다. 글자는 전부 글리프 윤곽 패스라 PDF에 서체가 안
들어가고, 로고는 저해상도 PNG를 vectorize로 떠서 패스로 앉힌다. 색은 흰 바탕에
검정 한 도뿐이라 마지막에 K100 단판으로 바꿔 넣는다. 시안의 #111(OPEN)과
#000(로고)은 화면에서도 안 갈리는 차이라 하나로 합친다.

    python build/standee_open.py            자료/ 에 PDF와 SVG를 쓴다
    python build/standee_open.py --rgb      화면 확인용 RGB판도 같이 쓴다
"""
from __future__ import annotations

import base64
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))

import vectorize  # noqa: E402

DRAFT = ROOT / "자료" / "수리소_입간판_시안_v9.html"

# ── 판형 ────────────────────────────────────────────────────────────────
W, H = 590.0, 890.0      # mm. 재단 사이즈. 시안 비율은 61:100이었다

# ── 시안의 CSS 값 ───────────────────────────────────────────────────────
OPEN_TOP = 0.0785 * H    # .open의 top:7.85% — 글상자 위, 잉크 위가 아니다
OPEN_SIZE = 0.2848 * W   # font-size:28.48cqw
TRACK = 0.03             # letter-spacing. 브라우저는 마지막 글자 뒤에도 붙인다
INDENT = 0.03            # text-indent. 자간 몫만큼 중앙을 되돌리는 보정
SYM_W, SYM_TOP = 0.541 * W, 0.355 * H
WM_W, WM_TOP = 0.672 * W, 0.702 * H

BLACK = "#111111"        # 시안의 OPEN 색. 로고 #000과 함께 K100 한 도로 찍는다
WHITE = "#FFFFFF"

CMYK = {
    BLACK: (0, 0, 0, 100),
    "#000000": (0, 0, 0, 100),
    WHITE: (0, 0, 0, 0),
}


# ── 시안에서 자산 꺼내기 ────────────────────────────────────────────────
def _draft_assets() -> tuple[bytes, bytes, bytes]:
    """(woff2, 심볼 PNG, 워드마크 PNG). 시안의 data URI를 그대로 디코드한다.

    심볼은 assets/ 의 원본과 같지만 워드마크는 시안 쪽이 다른 크롭(691×144)이다.
    시안이 정본이므로 셋 다 시안에서 꺼낸다.
    """
    src = DRAFT.read_text(encoding="utf-8")
    font = re.search(r"data:font/woff2;base64,([^)\"']+)", src)
    sym = re.search(r'class="sym" src="data:image/png;base64,([^"]+)', src)
    wm = re.search(r'class="wm"\s+src="data:image/png;base64,([^"]+)', src)
    if not (font and sym and wm):
        raise ValueError(f"시안에서 자산을 못 찾았습니다: {DRAFT}")
    return tuple(base64.b64decode(m.group(1)) for m in (font, sym, wm))


# ── 서체 ────────────────────────────────────────────────────────────────
def _kern(f, left: str, right: str) -> int:
    """GPOS 짝 커닝. PairPos 1·2형과 9형(확장) 포장을 푼다."""
    if "GPOS" not in f:
        return 0
    total = 0
    for lookup in f["GPOS"].table.LookupList.Lookup:
        if lookup.LookupType == 9:
            subs = [s.ExtSubTable for s in lookup.SubTable if s.ExtensionLookupType == 2]
        elif lookup.LookupType == 2:
            subs = lookup.SubTable
        else:
            continue
        for st in subs:
            if left not in st.Coverage.glyphs:
                continue
            if st.Format == 1:
                i = st.Coverage.glyphs.index(left)
                for pvr in st.PairSet[i].PairValueRecord:
                    if pvr.SecondGlyph == right and pvr.Value1:
                        total += getattr(pvr.Value1, "XAdvance", 0)
            elif st.Format == 2:
                c1 = st.ClassDef1.classDefs.get(left, 0)
                c2 = st.ClassDef2.classDefs.get(right, 0)
                rec = st.Class1Record[c1].Class2Record[c2]
                if rec.Value1:
                    total += getattr(rec.Value1, "XAdvance", 0)
    return total


def open_svg(woff2: bytes) -> str:
    """OPEN 글줄을 글리프 윤곽 패스로. 브라우저 조판 수식 그대로다."""
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.ttLib import TTFont

    f = TTFont(io.BytesIO(woff2))
    upm = f["head"].unitsPerEm
    os2, cmap = f["OS/2"], f.getBestCmap()
    gset, hmtx = f.getGlyphSet(), f["hmtx"]
    s = OPEN_SIZE / upm

    text = "OPEN"
    glyphs = [cmap[ord(c)] for c in text]
    kerns = [_kern(f, a, b) for a, b in zip(glyphs, glyphs[1:])] + [0]
    # 글줄 나비 = 들여쓰기 + 나비·커닝 합 + 자간 네 개(마지막 글자 뒤 포함)
    content = (INDENT * upm + sum(hmtx[g][0] for g in glyphs) + sum(kerns)
               + TRACK * upm * len(text)) * s
    x = (W - content) / 2 + INDENT * OPEN_SIZE

    # line-height:1 — 행상자 높이가 글자 크기와 같아 반행간이 음수로 들어간다
    asc, desc = os2.sTypoAscender, -os2.sTypoDescender
    baseline = OPEN_TOP + (OPEN_SIZE - (asc + desc) * s) / 2 + asc * s

    parts = []
    for g, k in zip(glyphs, kerns):
        pen = SVGPathPen(gset)
        gset[g].draw(pen)
        parts.append(f'<path transform="translate({x / s:.1f},0)" d="{pen.getCommands()}"/>')
        x += (hmtx[g][0] + k + TRACK * upm) * s
    return (
        f'<g transform="translate(0,{baseline:.3f}) scale({s:.6f},{-s:.6f})" '
        f'fill="{BLACK}">{"".join(parts)}</g>'
    )


# ── 조판 ────────────────────────────────────────────────────────────────
def placed(png: bytes, width: float, top: float) -> str:
    """PNG를 패스로 떠서 <img>처럼 앉힌다. 픽셀 상자째 가로 가운데, 위가 top."""
    import tempfile

    from PIL import Image

    px_w = Image.open(io.BytesIO(png)).size[0]
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp.write(png)
    d, _ = vectorize.trace(tmp.name)
    Path(tmp.name).unlink()
    s = width / px_w
    return (
        f'<g transform="translate({W / 2 - width / 2:.3f},{top:.3f}) scale({s:.5f})">'
        f'<path fill="#000000" fill-rule="evenodd" d="{d}"/></g>'
    )


def build() -> str:
    woff2, sym, wm = _draft_assets()
    art = "".join([
        f'<rect width="{W}" height="{H}" fill="{WHITE}"/>',
        open_svg(woff2),
        placed(sym, SYM_W, SYM_TOP),
        placed(wm, WM_W, WM_TOP),
    ])
    return f"""<meta charset="utf-8">
<style>
@page {{ size: {W}mm {H}mm; margin: 0 }}
html, body {{ margin: 0; padding: 0 }}
svg {{ position: absolute; top: 0; left: 0 }}
</style>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">{art}</svg>
"""


# ── 인쇄용 변환 ─────────────────────────────────────────────────────────
def _rgb01(hexcolor: str) -> tuple[float, float, float]:
    return tuple(int(hexcolor[i : i + 2], 16) / 255 for i in (1, 3, 5))


def to_cmyk(path: Path) -> dict[str, int]:
    """PDF 내용 스트림의 RGB 연산자를 DeviceCMYK로 갈아 끼운다.

    banner_kut와 같은 수법이다. 아는 색이 아니면 세우고 만다. 투명도 상태(gs)도
    같이 걷어낸다. 전부 불투명이라 그림은 안 바뀌고 검판 시비만 준다.
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

    name = "수리소_입간판_OPEN_59x89"
    html = build()

    if "--rgb" in sys.argv:  # 화면 확인용. 인쇄에는 쓰지 않는다
        rgb = ROOT / "자료" / f"{name}_RGB.pdf"
        HTML(string=html).write_pdf(rgb)
        print(f"{rgb.relative_to(ROOT)}  {rgb.stat().st_size / 1024:,.0f}KB  (RGB · 화면용)")

    out = ROOT / "자료" / f"{name}.pdf"
    HTML(string=html).write_pdf(out)
    used = to_cmyk(out)

    print(f"{out.relative_to(ROOT)}  {out.stat().st_size / 1024:,.0f}KB  (CMYK · 인쇄용)")
    for color, n in sorted(used.items(), key=lambda kv: -kv[1]):
        print(f"  {color:<16} {n:>3}회")

    # 웹·편집용 SVG. 그림은 PDF와 같고 색만 RGB다 (SVG는 CMYK가 없다)
    svg = ROOT / "자료" / f"{name}.svg"
    m = re.search(r"<svg .*</svg>", html, re.S)
    svg.write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + m.group(0), encoding="utf-8")
    print(f"{svg.relative_to(ROOT)}  {svg.stat().st_size / 1024:.0f}KB  (SVG · RGB)")


if __name__ == "__main__":
    main()
