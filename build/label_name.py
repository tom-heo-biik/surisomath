# -*- coding: utf-8 -*-
"""수리소 이름 라벨 · A4 8칸(폼텍 3108 / AL008 호환, 99.1×67.7mm).

칸마다 심볼 → 한글 워드마크 → 이름 작성란을 가운데 정렬로 세로로 쌓는다.
로고 PNG 두 장은 vectorize로 패스를 떠서 앉히고, '이름' 글자는 KoPubWorld 바탕체로
WeasyPrint가 조판한다. 가정용 프린터로 찍는 라벨이라 RGB 그대로 둔다.

칸 규격은 기존 자료/수리소_숙제라벨_8칸.pdf를 0.1mm 단위로 실측해 맞춘 값이다.
(가로 피치 101.6, 세로 피치 67.7, 왼쪽 여백 4.65, 위 여백 12.9)

    python build/label_name.py             자료/수리소_이름라벨_8칸.pdf
    python build/label_name.py --guide     칸 테두리를 회색으로 그린 확인용 판도 쓴다
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))
sys.path.insert(0, str(ROOT / "lib"))

import suriso  # noqa: E402
import vectorize  # noqa: E402

# ── 판형 (mm) ───────────────────────────────────────────────────────────
PAGE_W, PAGE_H = 210, 297
CELL_W, CELL_H = 99.1, 67.7
LEFT, TOP = 4.65, 12.9
PITCH_X, PITCH_Y = 101.6, 67.7
COLS, ROWS = 2, 4

# ── 칸 안 배치 (mm) ─────────────────────────────────────────────────────
SYMBOL_H = 22          # 심볼 높이
WORDMARK_W = 46        # 워드마크 폭
GAP_SYM_WM = 3.0       # 심볼 ↔ 워드마크
GAP_WM_NAME = 6.5      # 워드마크 ↔ 이름란
NAME_LINE_W = 52       # 이름 밑줄 길이
NAME_SIZE = 14         # '이름' 글자 크기(pt)
BLACK = "#000000"


def build(guide: bool = False) -> str:
    symbol = vectorize.svg(str(suriso.SYMBOL), fill=BLACK)
    wordmark = vectorize.svg(str(suriso.WORDMARK_KR), fill=BLACK)
    border = "0.2mm solid #BBBBBB" if guide else "0"

    cells = []
    for r in range(ROWS):
        for c in range(COLS):
            x, y = LEFT + c * PITCH_X, TOP + r * PITCH_Y
            cells.append(
                f'<div class="cell" style="left:{x}mm;top:{y}mm">'
                f'<div class="sym">{symbol}</div>'
                f'<div class="wm">{wordmark}</div>'
                f'<div class="name"><span class="lbl">이름:</span><span class="line"></span></div>'
                f'</div>'
            )

    return f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<style>
@font-face {{ font-family: B; src: url("{suriso.BATANG_MEDIUM.as_uri()}"); font-weight: 500; }}
@page {{ size: {PAGE_W}mm {PAGE_H}mm; margin: 0; }}
html, body {{ margin: 0; padding: 0; }}
body {{ width: {PAGE_W}mm; height: {PAGE_H}mm; position: relative; }}
.cell {{ position: absolute; width: {CELL_W}mm; height: {CELL_H}mm; box-sizing: border-box;
        border: {border}; display: flex; flex-direction: column; align-items: center;
        justify-content: center; }}
.sym svg {{ display: block; height: {SYMBOL_H}mm; width: auto; }}
.wm {{ margin-top: {GAP_SYM_WM}mm; }}
.wm svg {{ display: block; width: {WORDMARK_W}mm; height: auto; }}
.name {{ margin-top: {GAP_WM_NAME}mm; display: flex; align-items: flex-end;
         font: 500 {NAME_SIZE}pt/1 B; color: {BLACK}; }}
.lbl {{ margin-right: 2.2mm; padding-bottom: 0.3mm; }}
.line {{ display: block; width: {NAME_LINE_W}mm; border-bottom: 0.3mm solid {BLACK}; height: 4mm; }}
</style></head><body>{"".join(cells)}</body></html>"""


def main() -> None:
    from weasyprint import HTML

    out = ROOT / "자료" / "수리소_이름라벨_8칸.pdf"
    HTML(string=build()).write_pdf(out)
    print(f"{out.relative_to(ROOT)}  {out.stat().st_size / 1024:,.0f}KB")
    if "--guide" in sys.argv:
        g = out.with_name("수리소_이름라벨_8칸_칸확인.pdf")
        HTML(string=build(guide=True)).write_pdf(g)
        print(f"{g.relative_to(ROOT)}  (칸 테두리 확인용)")


if __name__ == "__main__":
    main()
