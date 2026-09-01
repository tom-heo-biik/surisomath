# -*- coding: utf-8 -*-
"""수리소 상장 · A4 1200DPI, 학교안심 상장체, 심볼 직인.

C:/허문영/수리소/수리소_상장/build_certificate.py(2026-1학기 기말 12장을 만든
원본)의 조판 로직을 그대로 이식한 판이다. 좌표계는 A4 300dpi(2480×3508)로 잡고
4배로 그려 1200DPI로 저장한다. 크기 4단계: 상장(제목) > 원장 성명 > 그 외 > 제호.
상장 번호는 학년도 안에서 이어 붙인다(1학기 기말이 001~012호, 이번이 013호부터).

학생·상 이름·문안·날짜는 AWARDS·ROSTER·DATE·SERIAL_START만 고치면 된다.

    python build/award.py     자료/수리소_상장_*.pdf 낱장 + 합본
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "lib"))

from PIL import Image, ImageDraw, ImageFont  # noqa: E402

import suriso  # noqa: E402

# ── 판형 ────────────────────────────────────────────────────────────────
W, H = 2480, 3508          # 좌표계 (A4 @ 300dpi 기준)
SS = 4                     # 출력 배율 → 9920×14032px = A4 @ 1200dpi
DPI = 1200
RED = (218, 41, 28)        # PANTONE 485 C (#DA291C)
INK = (15, 15, 15)
ML, MR = 380, 380          # 좌우 안전 여백 (기성 상장 용지 테두리 회피)

# ── 크기 4단계 ──────────────────────────────────────────────────────────
SZ_TITLE = 250             # 1. 상장 (제목)
SZ_NAME = 140              # 2. 최명주 (원장 성명)
SZ_BODY = 90               # 3. 그 외 (상 구분·소속·수상자·본문·날짜·직함)
SZ_SERIAL = 60             # 4. 제호

# ── 내용 ────────────────────────────────────────────────────────────────
YEAR = 2026
DATE = f"{YEAR}년 9월 1일"
SERIAL_START = 13          # 제 2026 - 013호부터

AWARDS = {
    "자습왕상": [f"위 학생은 {YEAR}학년도 여름 방학 동안",
                "수리소에서 자습을 70시간 이상 수행하였으므로",
                "이 상장을 수여합니다."],
    "열정왕상": [f"위 학생은 {YEAR}학년도 여름 방학 동안",
                "수리소에서 자습을 60시간 이상 수행하였으므로",
                "이 상장을 수여합니다."],
}

ROSTER = [
    ("자습왕상", "홍천중학교 1학년", "이다인"),   # 자습 70시간 이상
    ("자습왕상", "수지중학교 1학년", "유세희"),   # 자습 70시간 이상
    ("열정왕상", "수지중학교 1학년", "김도윤"),   # 자습 60시간 이상
]

BUNDLE = f"수리소_상장_{YEAR}_여름방학_{len(ROSTER)}장.pdf"


def F(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(suriso.SANGJANG), int(size * SS))


def s(v: float) -> int:
    return int(round(v * SS))


def measure(d, text, font, tr):
    w = 0.0
    for i, ch in enumerate(text):
        w += d.textlength(ch, font=font)
        if i != len(text) - 1:
            w += s(tr)
    return w


def draw_tracked(d, x, baseline, text, font, tr, fill=INK):
    for i, ch in enumerate(text):
        d.text((x, baseline), ch, font=font, fill=fill, anchor="ls")
        x += d.textlength(ch, font=font)
        if i != len(text) - 1:
            x += s(tr)
    return x


def baseline_of(font, cy):
    asc, desc = font.getmetrics()
    return s(cy) + (asc + desc) / 2 - desc


def text_c(d, cx, cy, text, size, tr=0, fill=INK):
    f = F(size)
    tw = measure(d, text, f, tr)
    draw_tracked(d, s(cx) - tw / 2, baseline_of(f, cy), text, f, tr, fill)


def text_r(d, rx, cy, text, size, tr=0, fill=INK):
    f = F(size)
    tw = measure(d, text, f, tr)
    draw_tracked(d, s(rx) - tw, baseline_of(f, cy), text, f, tr, fill)


def text_l(d, lx, cy, text, size, tr=0, fill=INK):
    draw_tracked(d, s(lx), baseline_of(F(size), cy), text, F(size), tr, fill)


def recolor_red(img):
    a = img.split()[3]
    out = Image.new("RGBA", img.size, RED + (0,))
    out.putalpha(a)
    return out


def build_seal(size: int) -> Image.Image:
    sl = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(sl)
    bw = max(3, int(size * 0.035))
    d.rounded_rectangle([bw // 2, bw // 2, size - bw // 2, size - bw // 2],
                        radius=int(size * 0.08), outline=RED, width=bw)
    sym = recolor_red(Image.open(suriso.SYMBOL).convert("RGBA"))
    pad = int(size * 0.13)
    tw = size - pad * 2
    th = int(round(tw * sym.height / sym.width))
    sym = sym.resize((tw, th), Image.LANCZOS)
    sl.alpha_composite(sym, (pad, (size - th) // 2))
    return sl


def render(award, no, school_grade, name, y_off=0.0, include_seal=True):
    """y_off(최종px)만큼 전체 내용을 내려 그린 SS 캔버스를 반환."""
    im = Image.new("RGB", (W * SS, H * SS), "white")
    d = ImageDraw.Draw(im)
    CX = W / 2
    Y = lambda v: v + y_off  # noqa: E731

    # 제호 — 좌상단
    text_l(d, ML, Y(575), f"제 {YEAR} - {no:03d}호", SZ_SERIAL, tr=2)

    # 대제목 "상 장" — 중앙
    text_c(d, CX, Y(1005), "상장", SZ_TITLE, tr=260)

    # 우측 블록: 소속(위) / 수상자(아래) — 우측 정렬
    text_r(d, W - MR, Y(1465), school_grade, SZ_BODY, tr=6)
    text_r(d, W - MR, Y(1620), name, SZ_BODY, tr=48)

    # 상 구분 — 좌측, 소속 줄과 같은 높이
    text_l(d, ML, Y(1465), award, SZ_BODY, tr=20)

    # 본문 — 중앙 3행
    y = Y(1935)
    for line in AWARDS[award]:
        text_c(d, CX, y, line, SZ_BODY, tr=3)
        y += 185

    # 날짜
    text_c(d, CX, Y(2615), DATE, SZ_BODY, tr=4)

    # 수여자 — 직함 + 성명, 직인은 성명 위 오른쪽 걸침
    p1, p2 = "수리소 수학학원 원장", "최 명 주"
    f1, f2 = F(SZ_BODY), F(SZ_NAME)
    tr1, tr2 = 8, 42
    gap = s(64)
    w1 = measure(d, p1, f1, tr1)
    w2 = measure(d, p2, f2, tr2)
    cy_iss = Y(2960)
    base1 = baseline_of(f1, cy_iss)
    x0 = s(CX) - (w1 + gap + w2) / 2
    draw_tracked(d, x0, base1, p1, f1, tr1)
    name_x1 = draw_tracked(d, x0 + w1 + gap, base1, p2, f2, tr2)

    im_rgba = im.convert("RGBA")
    if include_seal:
        seal_sz = s(320)
        seal = build_seal(seal_sz)
        seal_cx = name_x1 - s(52)
        seal_cy = s(cy_iss) - s(46)
        im_rgba.alpha_composite(seal, (int(seal_cx - seal_sz / 2),
                                       int(seal_cy - seal_sz / 2)))
    return im_rgba.convert("RGB")


def center_offset() -> float:
    """제호~최하단 글줄이 세로 중앙에 오는 오프셋. 전 장 공통이라 한 번만 잰다."""
    import numpy as np

    award, school_grade, name = ROSTER[0]
    probe = render(award, SERIAL_START, school_grade, name, include_seal=False)
    arr = np.array(probe.convert("L"))
    rows = np.where((arr < 245).any(axis=1))[0]
    ymin, ymax = int(rows[0]), int(rows[-1])
    return ((H * SS - (ymax - ymin)) / 2 - ymin) / SS


def main() -> None:
    from pypdf import PdfWriter

    out_dir = ROOT / "자료"
    y_off = center_offset()
    print(f"중앙 오프셋 {y_off:+.1f}px")

    writer = PdfWriter()
    for i, (award, school_grade, name) in enumerate(ROSTER):
        im = render(award, SERIAL_START + i, school_grade, name, y_off)
        out = out_dir / f"수리소_상장_{award}_{name}.pdf"
        im.save(out, "PDF", resolution=float(DPI))
        del im
        writer.append(str(out))
        print(f"{out.relative_to(ROOT)}  {out.stat().st_size / 1024:,.0f}KB")

    bundle = out_dir / BUNDLE
    with open(bundle, "wb") as f:
        writer.write(f)
    writer.close()
    print(f"{bundle.relative_to(ROOT)}  {bundle.stat().st_size / 1024:,.0f}KB")


if __name__ == "__main__":
    main()
