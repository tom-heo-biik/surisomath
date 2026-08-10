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
FONTS = ASSETS / "fonts"

# KoPubWorld 바탕체만 스킬 안에 산다. surisomath-a4 명세가 templates/fonts/ 를
# 자기 파일 목록으로 잡고 있어서, 사본을 하나 더 두지 않고 그쪽을 정본으로 본다.
BATANG_DIR = ROOT / "skills" / "surisomath-a4" / "templates" / "fonts"

# ── 서체 ────────────────────────────────────────────────────────────────
# 무게는 웹 축(300~700)으로 부른다. KoPubWorld 공식 CSS는 Medium을 400에
# 매핑하지만 비익 계열 플러그인은 500에 앉힌다.
BATANG_LIGHT = BATANG_DIR / "KoPubWorld-Batang-Light.otf"
BATANG_MEDIUM = BATANG_DIR / "KoPubWorld-Batang-Medium.otf"
BATANG_BOLD = BATANG_DIR / "KoPubWorld-Batang-Bold.otf"

BATANG = {300: BATANG_LIGHT, 500: BATANG_MEDIUM, 700: BATANG_BOLD}

PRETENDARD = {
    300: FONTS / "Pretendard-Light.otf",
    400: FONTS / "Pretendard-Regular.otf",
    500: FONTS / "Pretendard-Medium.otf",
    600: FONTS / "Pretendard-SemiBold.otf",
    700: FONTS / "Pretendard-Bold.otf",
}

# 학교안심 상장체. 상장에만 쓴다. 무게가 하나뿐이다.
SANGJANG = FONTS / "HakgyoansimSangjangR.ttf"

FAMILIES = {
    "batang": BATANG,
    "pretendard": PRETENDARD,
    "sangjang": {400: SANGJANG},
}

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


def font(weight: int = 500, size: int = 12, family: str = "batang"):
    """PIL ImageFont. size는 픽셀. family는 batang·pretendard·sangjang."""
    from PIL import ImageFont  # 필요할 때만 부른다

    try:
        faces = FAMILIES[family]
    except KeyError:
        raise ValueError(f"서체는 {'·'.join(FAMILIES)} 중 하나여야 합니다: {family}") from None
    try:
        path = faces[weight]
    except KeyError:
        have = "·".join(str(w) for w in faces)
        raise ValueError(f"{family}의 무게는 {have} 중 하나여야 합니다: {weight}") from None
    return ImageFont.truetype(str(path), size)


def _all_assets():
    for faces in FAMILIES.values():
        yield from faces.values()
    yield from LOGOS.values()


def verify() -> list[str]:
    """빠진 자산의 목록. 비어 있으면 정상."""
    return [str(p.relative_to(ROOT)) for p in _all_assets() if not p.exists()]


if __name__ == "__main__":
    import sys

    print(f"플러그인 루트: {ROOT}")
    missing = verify()
    if missing:
        print("빠진 자산:")
        for m in missing:
            print(f"  - {m}")
        sys.exit(1)

    print(f"자산 {len(list(_all_assets()))}종 모두 있음.\n")
    for name in LOGO_SIZE:
        w, h = LOGO_SIZE[name]
        print(f"  {name:14s} {w}×{h}px  1:1 = {natural_mm(name):.1f}mm @ {DPI}DPI")

    print()
    try:
        for fam, faces in FAMILIES.items():
            for weight in faces:
                got = font(weight, 40, fam).getname()
                print(f"  {fam:11s} {weight}  {got[0]} {got[1]}")
    except ImportError:
        print("PIL 미설치 — 서체 적재는 건너뜀 (pip install pillow)")
