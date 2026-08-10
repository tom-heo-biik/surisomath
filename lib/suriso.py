# -*- coding: utf-8 -*-
"""수리소 브랜드 자산 해석기.

플러그인이 어느 PC의 어느 경로에 설치되든 이 파일의 위치를 기준으로 자산을 찾는다.
빌드 스크립트는 절대 경로를 코드에 박지 말고 여기서 가져다 쓴다.

    import sys; sys.path.insert(0, str(PLUGIN_ROOT / "lib"))
    import suriso
    f = suriso.font(500, 34)              # PIL ImageFont — KoPubWorld 바탕체 Medium
    sym = Image.open(suriso.SYMBOL)

자체 점검:  python lib/suriso.py
"""
from __future__ import annotations

from pathlib import Path

# ── 경로 ────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

# 서체 실파일은 surisomath-a4 스킬 안에 산다. 스킬 명세가 templates/fonts/ 를
# 자기 파일 목록으로 잡고 있어서, 사본을 하나 더 두지 않고 그쪽을 정본으로 본다.
FONTS = ROOT / "skills" / "surisomath-a4" / "templates" / "fonts"

# ── 서체 ────────────────────────────────────────────────────────────────
# KoPubWorld 바탕체. 무게는 웹 축(300·500·700)으로 부른다.
# 패키지 공식 CSS는 Medium을 400에 매핑하지만 비익 계열 플러그인은 500에 앉힌다.
BATANG_LIGHT = FONTS / "KoPubWorld-Batang-Light.otf"
BATANG_MEDIUM = FONTS / "KoPubWorld-Batang-Medium.otf"
BATANG_BOLD = FONTS / "KoPubWorld-Batang-Bold.otf"

BATANG = {300: BATANG_LIGHT, 500: BATANG_MEDIUM, 700: BATANG_BOLD}

# ── 로고 ────────────────────────────────────────────────────────────────
# 래스터 PNG뿐이라 확대에 한계가 있다. 원본 픽셀을 넘겨 키우면 흐려진다.
SYMBOL = ASSETS / "수리소수학학원_로고_심볼.png"
WORDMARK_KR = ASSETS / "수리소수학학원_로고_글자_한글만.png"
WORDMARK_EN = ASSETS / "수리소수학학원_로고_글자_영어만.png"
WORDMARK_FULL = ASSETS / "수리소수학학원_로고_글자_한글_영어.png"

LOGOS = {
    "symbol": SYMBOL,
    "wordmark_kr": WORDMARK_KR,
    "wordmark_en": WORDMARK_EN,
    "wordmark_full": WORDMARK_FULL,
}

LOGO_SIZE = {  # 원본 px — 1:1 인쇄 폭 계산에 쓴다
    "symbol": (439, 381),
    "wordmark_kr": (691, 98),
    "wordmark_en": (465, 26),
    "wordmark_full": (691, 144),
}

# ── 색 ──────────────────────────────────────────────────────────────────
# 순흑백 모노라인. 회색 틴트를 쓰지 않는다.
INK = (0, 0, 0)
PAPER = (255, 255, 255)
INK_HEX = "#000000"
PAPER_HEX = "#FFFFFF"

# ── 인쇄 ────────────────────────────────────────────────────────────────
DPI = 300

# A4 라벨지 8칸(2×4). 공칭값이 아니라 사용자가 자로 잰 실측값이다.
# 공칭 AL008(99.1×67.5, 상 14.5, 간격 2.5)로 앉히면 실물에서 정렬이 틀어진다.
# 검산: 4.5 + 99 + 2 + 99 + 5.5 = 210 · 13 + 68×4 + 12 = 297
LABEL_A4_8 = {
    "page": (210.0, 297.0),
    "label": (99.0, 68.0),
    "margin_top": 13.0,
    "margin_bottom": 12.0,
    "margin_left": 4.5,
    "margin_right": 5.5,
    "gap_x": 2.0,
    "gap_y": 0.0,
    "cols": 2,
    "rows": 4,
}


def mm2px(mm: float, dpi: int = DPI) -> int:
    """밀리미터를 픽셀로. 인쇄물은 300DPI가 기준."""
    return round(mm * dpi / 25.4)


def px2mm(px: float, dpi: int = DPI) -> float:
    return px * 25.4 / dpi


def natural_mm(name: str, dpi: int = DPI) -> float:
    """로고를 확대 없이 1:1로 앉혔을 때의 가로 폭(mm)."""
    return px2mm(LOGO_SIZE[name][0], dpi)


def font(weight: int = 500, size: int = 12):
    """KoPubWorld 바탕체 PIL ImageFont. size는 픽셀."""
    from PIL import ImageFont  # 필요할 때만 부른다

    try:
        path = BATANG[weight]
    except KeyError:
        raise ValueError(f"무게는 300·500·700 중 하나여야 합니다: {weight}") from None
    return ImageFont.truetype(str(path), size)


def verify() -> list[str]:
    """빠진 자산의 목록. 비어 있으면 정상."""
    return [
        str(p.relative_to(ROOT))
        for p in (*BATANG.values(), *LOGOS.values())
        if not p.exists()
    ]


if __name__ == "__main__":
    import sys

    print(f"플러그인 루트: {ROOT}")
    missing = verify()
    if missing:
        print("빠진 자산:")
        for m in missing:
            print(f"  - {m}")
        sys.exit(1)

    print(f"자산 {len(BATANG) + len(LOGOS)}종 모두 있음.")
    for name in LOGO_SIZE:
        w, h = LOGO_SIZE[name]
        print(f"  {name:14s} {w}×{h}px  1:1 = {natural_mm(name):.1f}mm @ {DPI}DPI")
    try:
        print(f"서체 적재 성공: {font(500, 40).getname()}")
    except ImportError:
        print("PIL 미설치 — 서체 적재는 건너뜀 (pip install pillow)")
