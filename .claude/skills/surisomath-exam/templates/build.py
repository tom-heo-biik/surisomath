# -*- coding: utf-8 -*-
"""시험대비 학습지 빌드 — 단원 하나로 그림·수식·HTML·PDF·검사까지.

    python build.py 단원폴더                     → 같은 폴더에 HTML과 PDF
    python build.py 단원폴더/problems.yaml       (옛 꼴은 yaml 경로를 주어도 된다)
    python build.py 단원폴더 --no-figures          그림은 다시 그리지 않는다
    python build.py 단원폴더 --no-check            그리드 검사를 건너뛴다

두 꼴(munhang/templates/unit.py가 읽는다)
  옛 꼴: 단원/problems.yaml, figures.py → PDF 하나(학생 쪽 뒤에 선생님 쪽). 20262학기중간 세 단원, 시험기출, 견본.
  새 꼴: 단원/001/problem.yaml, 001/figure.py … (문제마다 폴더, 번호는 폴더 이름) → PDF 둘.
         {학습지 이름}_문제.pdf(학생 쪽)와 {학습지 이름}_정답.pdf(선생님 쪽, 쪽번호 1부터). 2026-09-30 선생님.

하는 일
  1. 옛 꼴은 단원 폴더의 figures.py를, 새 꼴은 문제 폴더마다의 figure.py를(figrun.py가 한 프로세스에서)
     실행해 figures/ 에 SVG를 뽑는다. grind_figure를 찾도록 연마 templates 폴더를 PYTHONPATH에 넣어 준다.
  2. problems.yaml을 읽어 한 쪽에 문제 둘(두 단, 단마다 하나)인 HTML을 쓴다. 그림은 SVG
     높이가 22의 배수인지, 너비가 단 글 너비(229pt) 안인지 본다. 칸 수는 높이가 정한다.
  3. 지문·선지·정답·풀이의 $…$는 연마 build.py의 rich()가 Computer Modern SVG로 그린다.
  4. 선지는 너비를 재서 5열·3열·1열을 고른다(수능·모의고사 관례). 분수처럼 키 큰 선지가 두 줄
     이상 쌓이면 항목마다 두 칸을 주고 둘씩 들면 2열.
  5. 학생 쪽 뒤에 선생님 쪽을 같은 짝으로 붙인다. 풀 자리 첫 줄에 정답, solution이 있으면
     그 아래 풀이. 없으면 정답 줄만(정답표).
  6. surisomath-a4/templates/render.py 로 PDF를 뽑고 --check 로 그리드를 검사한다.
  7. 풀 자리의 위 끝(학생 쪽 div.work.box.n<번호>, 선생님 쪽 .t<번호>)을 받아 가장 좁은 단의
     남은 칸을 알려 주고, 밀린 문제를 짚는다. 넘친 내용을 WeasyPrint는 바닥 아래로 흘리지 않고 쪽을
     쪼개므로 상자가 있어야 할 쪽보다 뒤에 있으면 그 문제가 단을 넘친 것이다. 풀 자리가
     8칸 아래면, 정답 줄이나 1열 선지가 단보다 넓으면, 머리줄이 이름 칸과 겹치면,
     잇단 줄의 수식이 겹치면(단마다 따로 본다) 경고.

경고가 하나라도 있으면 종료 코드가 1이다. PDF는 그래도 나온다.

problems.yaml
  exam: 2026학년도 2학기 중간고사   # 생략하면 시험 폴더 이름(20262학기중간)에서 만든다
  grade: 중3                       # 생략하면 학년 폴더 이름
  unit: 삼각비                      # 생략하면 단원 폴더 이름
  file: 수리소_시험대비_…            # 생략하면 수리소_시험대비_2026_2학기중간_중3_삼각비
  date: 2026.09.01                 # PDF의 만든 날짜. 생략하면 학기 첫날(1학기 3. 1., 2학기 9. 1.).
                                   # 폴더 꼴이 안 맞으면 yaml 수정 시각 — 그때는 PDF가 재현되지 않는다
  problems:
    - text: 그림과 같이 …          # 지문. 표기 규칙은 SKILL.md. ": "가 들어가면 따옴표로 감싼다
      figure: p1.svg               # figures/ 안의 그림. units는 없다 — SVG 높이가 칸 수를 정한다
      alt: …                       # 그림 설명. PDF에는 안 찍힌다
      conditions:                  # 있으면 조건 상자(평가원 꼴). (가) (나) 항목. 지문 뒤, 그림 앞
        - $f(0)=1$
      after: $f(4)$의 값을 구하시오.  # 조건 상자 뒤에 오는 문단
      table:                       # 있으면 삼각비의 표(격자). 그림 뒤, 보기 상자 앞. 칸은 작은따옴표로
        head: ['각도', '$\\sin$', '$\\cos$', '$\\tan$']
        rows:
          - ['$1^{\\circ}$', '0.0175', '0.9998', '0.0175']
      notes:                       # 있으면 보기 상자. ㄱ. ㄴ. ㄷ. 항목. 그림 뒤, 선지 앞
        - 점 $(1,\\,1)$을 지난다.
      choices:                     # 있으면 객관식. 다섯 개
        - $\\dfrac{80}{\\tan 52^{\\circ}+\\tan 35^{\\circ}}$
      answer: ④                    # 정답. 객관식은 번호만, 서술형은 값만(단위 없이, 각의 °와 %만). 필수. 선생님 쪽 정답 줄
      solution: |                  # 선생님 풀이(선택). 줄마다 한 칸. 빈 줄은 한 칸을 비운다
        주어진 그림에서 …
    - "no": "004"                  # 번호를 직접 줄 때. 키까지 따옴표로(YAML은 no를 거짓으로 읽는다)

시험기출(학교 기출 시험지를 원문 그대로 옮긴 것)만 쓰는 것
  series: 시험기출                  # 머리줄 첫 낱말과 파일 이름. 생략하면 시험대비
  school: 수지중학교                # 있으면 머리줄이 시리즈 · 시험 · 학교 · 학년이고 단원이 없다
  verbatim: true                   # 원문 그대로. 평가원 표기 검사(notation.py)를 하지 않는다
  problems:
    - label: 논술형 1              # 번호 자리에 찍을 글. 생략하면 번호. 파일 이름과 검사는 번호로 한다
      text: 연립방정식 [[p04s.svg]] 의 해가 …   # [[…]]는 figures.py가 그린 별행 수식. 그 자리에서 줄이 바뀐다
      notes:                       # 보기가 그래프면 항목마다 figure. 두 열, 그림 너비 84pt 안
        - figure: p05a.svg
      min_rows: 4                  # 원문 분량이라 풀 자리 8칸을 못 지키는 문제만. 그 문제의 하한
      unnamed: [O]                 # 지문이 부르지만 원본 그림에 이름이 인쇄되지 않은 점. 이름 대조에서 뺀다
"""
from __future__ import annotations

import argparse
import calendar
import html
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
SKILLS = HERE.parents[1]
A4 = SKILLS / "surisomath-a4" / "templates"
GRIND = SKILLS / "surisomath-grind" / "templates"
MUNHANG = SKILLS / "surisomath-munhang" / "templates"
RENDER = A4 / "render.py"
BASE_CSS = A4 / "base.css"
EXAM_CSS = HERE / "exam.css"
KOPUB = A4 / "fonts" / "KoPubWorld-Batang-Light.otf"

sys.path.insert(0, str(GRIND))
import grind_figure as g  # noqa: E402  본문 안 수식을 그린다


def _grind_build():
    """연마 build.py를 모듈로 읽는다(__main__ 가드가 있다). 수식 조판(rich)·상대 경로·
    SVG 높이·수식 겹침 검사를 빌려 쓴다. 같은 코드를 복사하지 않는다.

    gb는 sys.modules에 안 오르므로 연마 build.py에 모듈 수준 부작용을 더하지 말 것."""
    spec = importlib.util.spec_from_file_location("grind_build", GRIND / "build.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


gb = _grind_build()
rich, rel, svg_height, check_overlap = gb.rich, gb.rel, gb.svg_height, gb.check_overlap

SERIES = "시험대비"
GRID = 22.0
BOTTOM = 754.0         # 본문 영역 아래 끝(842 - 88). 풀 자리가 여기서 끝난다
COL_W = 229.0          # 단 글 너비(pt). 왼 단 229, 오른 단 230 — 좁은 쪽으로 잰다
MARK_W = 14.8          # 선지 마커 칸(exam.css의 ol.n7 --pad). ① 10.8pt + 4pt
GUTTER = 6.0           # 여러 열일 때 칸마다 남겨야 하는 여백(pt). 칸에 딱 맞으면 다음 마커와 붙어 보인다
                       # (2026-09-26 근호가 좁아지며 삼각비 016·018이 3열에 0.3pt 차로 들어 ②와 ③이 붙었다)
MIN_ROWS = 8           # 풀 자리 최소 칸 수
NOTE_FIG_W = 84.0      # 그림 보기 한 칸의 그림 너비(pt). (229 - 16) / 2 - 22
TALL = 16.0            # 선지 수식의 잉크 높이(pt)가 이보다 크면 키 큰 선지 — 분수. 두 줄 이상 쌓이면 두 칸 간격
CAPTION = gb.CAPTION   # neutral-500. 정답 줄
MATH = gb.MATH
FOLDER = re.compile(r"(\d{4})(\d)학기(중간|기말)")
_KOPUB = None


# ── 너비 재기 ───────────────────────────────────────────────────────────

def svg_width(path: Path) -> float | None:
    """SVG의 width(pt). 높이는 연마의 svg_height가 읽는다."""
    m = re.search(r'<svg[^>]*\swidth="([\d.]+)pt"', path.read_text(encoding="utf-8")[:4000])
    return float(m.group(1)) if m else None


def kopub_width(s: str, size: float) -> float:
    """KoPub 바탕 Light로 조판한 글의 너비(pt). 자간은 a4 규격(12pt -0.03em, 10pt -0.02em)."""
    global _KOPUB
    if _KOPUB is None:
        from fontTools.ttLib import TTFont
        f = TTFont(str(KOPUB))
        _KOPUB = (f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm)
    cmap, hmtx, upem = _KOPUB
    track = -0.02 if size < 12 else -0.03
    w = 0.0
    for ch in s:
        gid = cmap.get(ord(ch))
        w += (hmtx[gid][0] if gid else upem / 2) / upem * size + track * size
    return w


def width_of(s: str, size: float = 12.0) -> float:
    """조판한 글의 너비(pt). $…$는 Computer Modern 잉크 너비, 나머지는 KoPub 폭."""
    from matplotlib.font_manager import FontProperties
    from matplotlib.textpath import TextPath
    w = 0.0
    for i, piece in enumerate(MATH.split(s)):
        if not piece:
            continue
        if i % 2:                                   # 홀수째 조각이 수식이다
            x0, _, x1, _ = TextPath((0, 0), f"${piece}$", size=size,
                                    prop=FontProperties(size=size)).get_extents().extents
            w += float(x1 - x0) + 1.0
        else:
            w += kopub_width(piece, size)
    return w


def height_of(s: str, size: float = 12.0) -> float:
    """조판한 글 안 수식의 잉크 높이(pt). 글자 조각은 0 — 글줄에 꽉 차는 것은 분수뿐이다."""
    from matplotlib.font_manager import FontProperties
    from matplotlib.textpath import TextPath
    h = 0.0
    for i, piece in enumerate(MATH.split(s)):
        if not piece or not i % 2:                  # 홀수째 조각이 수식이다
            continue
        _, y0, _, y1 = TextPath((0, 0), f"${piece}$", size=size,
                                prop=FontProperties(size=size)).get_extents().extents
        h = max(h, float(y1 - y0))
    return h


def choice_layout(choices: list) -> tuple[int, bool]:
    """(열 수, 두 칸 간격 여부). 다섯이 한 줄에 들면 5열, 셋씩 들면 3열, 아니면 1열 — 수능·모의고사
    관례. 칸 너비가 같아 ④가 ① 아래 온다. 한 칸 = 마커 칸 22pt + 글 너비.
    분수처럼 글줄에 꽉 차는 수식(잉크 높이 TALL 초과)이 든 선지가 두 줄 이상 쌓이면 잇단 줄의
    분수가 닿으므로 항목마다 두 칸을 주고, 그때는 둘씩 들면 2열로 줄 수를 아낀다."""
    widths = [MARK_W + width_of(str(c).strip()) for c in choices]
    tall = max(height_of(str(c).strip()) for c in choices) > TALL
    for n in (5, 3, 2, 1):
        if n == 2 and not tall:
            continue
        if all(w + (GUTTER if n > 1 else 0) <= COL_W / n for w in widths):
            rows = -(-len(choices) // n)
            return n, tall and rows > 1
    return 1, tall


def choice_cols(choices: list) -> int:
    return choice_layout(choices)[0]


# ── 제목 · 파일 이름 · 날짜 ─────────────────────────────────────────────

def meta(data: dict, out_dir: Path) -> dict:
    """머리줄·파일 이름·PDF 날짜. 폴더 build/시험대비/<시험>/<학년>/<단원>/ 에서 만들고
    yaml의 exam·grade·unit·file·date가 있으면 그것이 이긴다.

    시험기출은 폴더가 build/시험기출/<학교>/<학년>/<시험>/ 이라 위 꼴이 아니다. yaml에 series(시험기출),
    exam, school, grade, file, date를 적는다. 단원이 없고 머리줄은 시리즈 · 시험 · 학교 · 학년이다."""
    m = FOLDER.fullmatch(out_dir.parents[1].name) if len(out_dir.parents) > 1 else None
    series = str(data.get("series") or SERIES)
    exam = data.get("exam") or (m and f"{m[1]}학년도 {m[2]}학기 {m[3]}고사")
    grade = data.get("grade") or (m and out_dir.parent.name)
    school = data.get("school")
    unit = data.get("unit") or (m and out_dir.name)
    if not (exam and grade and (unit or school)):
        raise SystemExit("폴더가 build/시험대비/<YYYY><N>학기<중간|기말>/<학년>/<단원>/ 꼴이 아니다. "
                         "problems.yaml(새 꼴은 unit.yaml)에 exam·grade·unit을 적어라(시험기출이면 series·exam·school·grade)")
    if m:
        stem = f"수리소_{series}_{m[1]}_{m[2]}학기{m[3]}_{grade}_{unit}"
        epoch = calendar.timegm((int(m[1]), 3 if m[2] == "1" else 9, 1, 0, 0, 0))
    else:
        stem = "_".join(["수리소", series, str(exam)] + ([str(school)] if school else [])
                        + [str(grade)] + ([str(unit)] if unit else [])).replace(" ", "")
        epoch = None
    if data.get("date"):
        d = re.fullmatch(r"(\d{4})\.(\d{1,2})\.(\d{1,2})", str(data["date"]).strip())
        if not d:
            raise SystemExit(f"date는 YYYY.MM.DD 꼴로 적어라: {data['date']}")
        epoch = calendar.timegm((int(d[1]), int(d[2]), int(d[3]), 0, 0, 0))
    head = [series, str(exam)] + ([str(school)] if school else []) + [str(grade)] + ([str(unit)] if unit else [])
    return {"exam": str(exam), "grade": str(grade), "unit": str(unit or ""),
            "file": str(data.get("file") or stem), "epoch": epoch,
            "head": " · ".join(head)}


# ── HTML ────────────────────────────────────────────────────────────────

def svg_units(no: str, svg: Path, width: float = COL_W, where: str = "단 글 너비") -> int:
    """그림 SVG의 칸 수. 높이가 22의 배수가 아니거나 너비가 자리를 넘으면 멈춘다."""
    if not svg.is_file():
        raise SystemExit(f"{no}: 그림 파일이 없다: {svg}")
    h, w = svg_height(svg), svg_width(svg)
    if h is None or w is None:
        raise SystemExit(f"{no}: {svg.name}의 크기를 읽을 수 없다. grind_figure.save()로 만든 SVG여야 한다")
    units = round(h / GRID)
    if abs(h - units * GRID) > 0.05:
        raise SystemExit(f"{no}: {svg.name} 높이 {h:g}pt가 22의 배수가 아니다. g.canvas의 units를 보라")
    if w > width:
        raise SystemExit(f"{no}: {svg.name} 너비 {w:.0f}pt가 {where} {width:.0f}pt를 넘는다. "
                         f"y 범위를 {w / width:.2f}배 넓혀 배율을 줄여라")
    return units


def figure_html(no: str, p: dict, fig_dir: Path) -> str:
    if not p.get("figure"):
        return ""
    svg = fig_dir / str(p["figure"])
    units = svg_units(no, svg)
    alt = html.escape(str(p.get("alt", "")))
    check_names(no, p, svg)
    return (f'      <div class="figure" style="--u:{units}">'
            f'<img src="figures/{svg.name}" alt="{alt}"></div>\n')


DISPLAY = re.compile(r"\[\[([^\[\]]+\.svg)\]\]")    # 지문 안의 별행 수식 그림 [[p04s.svg]]


def text_html(no: str, p: dict, fig_dir: Path) -> str:
    """지문. 보통은 한 문단이다. 연립방정식처럼 mathtext가 못 그리는 별행 수식은 figures.py가 그린
    SVG를 지문 안에 [[이름.svg]]로 적는다. 그 자리에서 문단을 끊어 수식 블록(단 가운데, 칸 수는
    SVG 높이)을 두고 뒤 글이 다음 줄에서 이어진다. 문장 하나라 블록 앞뒤에 빈 칸을 두지 않는다."""
    parts = DISPLAY.split(str(p["text"]).strip())
    if len(parts) == 1:
        return f'      <p>{rich(parts[0], f"m{no}", fig_dir, 12.0, g.INK)}</p>\n'
    out, k = [], 0
    for i, piece in enumerate(parts):
        if i % 2:                                   # 홀수째 조각이 별행 수식 그림 이름이다
            units = svg_units(no, fig_dir / piece)
            out.append(f'      <div class="figure disp" style="--u:{units}">'
                       f'<img src="figures/{piece}" alt=""></div>\n')
        elif piece.strip():
            k += 1
            last = i == len(parts) - 1
            out.append(f'      <p{"" if last else " class=\"run\""}>'
                       f'{rich(piece.strip(), f"m{no}" if k == 1 else f"m{no}_{k}", fig_dir, 12.0, g.INK)}</p>\n')
    return "".join(out)


_nspec = importlib.util.spec_from_file_location("munhang_notation", MUNHANG / "notation.py")
notation = importlib.util.module_from_spec(_nspec)
_nspec.loader.exec_module(notation)                     # 표기 검사(surisomath-munhang)
_sspec = importlib.util.spec_from_file_location("munhang_seal", MUNHANG / "seal.py")
seal = importlib.util.module_from_spec(_sspec)
_sspec.loader.exec_module(seal)                         # 확정 문항 봉인 대조(surisomath-munhang)

NAME_WARNINGS = 0

def check_notation(no: str, p: dict) -> None:
    """표기 규칙 검사(surisomath-munhang/templates/notation.py). 무엇을 잡는지는 그 머리글의 (가)~(라)에 있다."""
    global NAME_WARNINGS
    for msg in notation.check(notation.problem_fields(p)):
        print(f"  ! {no}: {msg}")
        NAME_WARNINGS += 1


def text_names(p: dict) -> set:
    """지문·조건·뒷문장·보기에 나오는 점 이름(\\mathrm{…}의 대문자, 프라임·첨자 포함).
    "(단, O는 원점이다.)"의 O도 이름이다."""
    fields = [p.get("text", ""), p.get("after", "")]
    for key in ("conditions", "notes"):
        fields += [str(x) for x in (p.get(key) or [])]
    names = set(g._names(fields))
    if any("O는 원점" in str(t) for t in fields):
        names.add("O")
    return names


def seq_letters(p: dict) -> set:
    """지문이 첨자 문자로 부른 이름의 글자. $\\mathrm{A}_n$, $\\mathrm{OA}_{n+1}$ → A."""
    fields = [str(p.get("text", "")), str(p.get("after", ""))]
    for key in ("conditions", "notes"):
        fields += [str(x) for x in (p.get(key) or [])]
    return {m.group(1) for s in fields for m in re.finditer(r"\\mathrm\{[A-Z]*([A-Z])\}_\{?[a-z]", s)}


def check_names(no: str, p: dict, svg: Path) -> None:
    """그림의 점 이름(grind_figure.save가 SVG 끝에 남긴 <!-- names: … -->)과 지문의 점 이름을 맞춰 본다.
    지문에 있는데 그림에 없으면 경고 — 이름을 빠뜨렸거나 지문이 그림에 없는 점을 부른다. 그림에만 있는
    이름은 알려만 준다. 지문이 Aₙ으로 부른 이름의 A₄, A₅ 같은 점은 "…"로 이어지는 이름이라 넘긴다(삼각비 014의 옛 그림이 본이었다)."""
    global NAME_WARNINGS
    m = re.search(r"<!-- names: ([^>]*) -->", svg.read_text(encoding="utf-8")[-2000:])
    if not m:
        return
    fig = set(m.group(1).split())
    # 시험기출에서 지문은 부르지만 원본 그림에 이름이 인쇄되지 않은 점(015의 두 대각선의 교점 O)은
    # yaml의 unnamed에 적어 대조에서 뺀다. 원본 그림에 없는 이름을 더하지 않기 위해서다
    want = text_names(p) - {str(x) for x in (p.get("unnamed") or [])}
    seq = seq_letters(p)
    missing = sorted(want - fig)
    extra = sorted(e for e in fig - want if not (e[:1] in seq and e[1:].isdigit()))
    if missing:
        print(f"  ! {no}: 지문의 점 {', '.join(missing)}이(가) 그림에 없다. 이름을 넣거나 지문을 보라")
        NAME_WARNINGS += 1
    if extra:
        print(f"  {no}: 그림에만 있는 이름 {', '.join(extra)} — 지문이 부르지 않는 점이면 빼라")


def conditions_html(no: str, p: dict, fig_dir: Path) -> str:
    """조건 상자(평가원 꼴). "다음 조건을 만족시킨다." 뒤에 (가) (나) 항목만 든 상자, 그 아래
    after 문단("f(4)의 값을 구하시오."). 머리글은 없다. 지문 바로 뒤, 그림 앞에 온다."""
    conds = p.get("conditions")
    out = ""
    if conds:
        if not isinstance(conds, list):
            raise SystemExit(f"{no}: conditions는 목록('- …')이어야 한다")
        items = "".join(f'          <li>{rich(str(c).strip(), f"k{no}_{k}", fig_dir, 12.0, g.INK)}</li>\n'
                        for k, c in enumerate(conds, 1))
        out += f'      <div class="notes cond">\n        <ol class="cond">\n{items}        </ol>\n      </div>\n'
    if p.get("after"):
        out += f'      <p>{rich(str(p["after"]).strip(), f"e{no}", fig_dir, 12.0, g.INK)}</p>\n'
    return out


def notes_html(no: str, p: dict, fig_dir: Path) -> str:
    """보기 상자. 첫 줄 "보기", 그 아래 ㄱ. ㄴ. ㄷ. 항목. 테두리는 ::before가 그려 글줄 위상을
    건드리지 않는다(exam.css). 그림 뒤, 선지 앞에 온다."""
    notes = p.get("notes")
    if not notes:
        return ""
    if not isinstance(notes, list):
        raise SystemExit(f"{no}: notes는 목록('- …')이어야 한다")
    figs = [isinstance(c, dict) and c.get("figure") for c in notes]
    if any(figs):
        # 그림 보기(ㄱ. ㄴ. ㄷ. ㄹ.가 저마다 그래프). 두 열로 놓고 마커는 칸 왼쪽 위. 그림 너비는
        # 상자 안(229 - 16pt)의 절반에서 마커 칸 22pt를 뺀 84pt 안. 칸 수는 가장 높은 그림이 정한다
        if not all(figs):
            raise SystemExit(f"{no}: 보기를 그림으로 쓰려면 항목 모두를 '- figure: 이름.svg'로 적어라")
        units = [svg_units(no, fig_dir / str(f), NOTE_FIG_W, "그림 보기 칸 너비") for f in figs]
        items = "".join(f'          <li><div class="figure" style="--u:{max(units)}">'
                        f'<img src="figures/{f}" alt=""></div></li>\n' for f in figs)
        return ('      <div class="notes">\n        <p class="head">보기</p>\n'
                f'        <ol class="bogi figs">\n{items}        </ol>\n      </div>\n')
    items = "".join(f'          <li>{rich(str(c).strip(), f"b{no}_{k}", fig_dir, 12.0, g.INK)}</li>\n'
                    for k, c in enumerate(notes, 1))
    return ('      <div class="notes">\n        <p class="head">보기</p>\n'
            f'        <ol class="bogi">\n{items}        </ol>\n      </div>\n')


def table_html(no: str, p: dict, fig_dir: Path) -> str:
    """삼각비의 표. yaml의 table(head 머리 행 · rows 몸 행 목록)을 수행평가 통계 표와 같은
    격자(table.stat)로 조판한다 — 교과서의 삼각비의 표가 격자다. typo-0, 행 22pt, 선 0.4pt.
    칸 안 $…$는 10pt 수식. 그림 뒤, 보기 상자 앞에 온다. 높이 = (머리 행 + 몸 행) 칸, 아래 한 칸."""
    t = p.get("table")
    if not t:
        return ""
    if not isinstance(t, dict) or not isinstance(t.get("rows"), list) or not t["rows"]:
        raise SystemExit(f"{no}: table은 head·rows(행 목록)를 가진 표여야 한다")
    head, rows = t.get("head"), t["rows"]
    ncol = len(head) if head else len(rows[0])
    for r in ([head] if head else []) + rows:
        if not isinstance(r, list) or len(r) != ncol:
            raise SystemExit(f"{no}: 표의 행마다 칸 수가 {ncol}로 같아야 한다: {r}")
    k = 0

    def cell(c, tag):
        nonlocal k
        k += 1
        s = "" if c is None else str(c).strip()
        return f"<{tag}>{rich(s, f't{no}_{k}', fig_dir, 10.0, g.INK) if s else ''}</{tag}>"

    out = ['      <table class="stat">']
    first = ' class="first"'
    if head:
        out.append(f"        <thead><tr{first}>" + "".join(cell(c, "th") for c in head) + "</tr></thead>")
        first = ""
    out.append("        <tbody>")
    for r in rows:
        out.append(f"          <tr{first}>" + "".join(cell(c, "td") for c in r) + "</tr>")
        first = ""
    out.append("        </tbody>\n      </table>\n")
    return "\n".join(out)


def choices_html(no: str, p: dict, fig_dir: Path) -> str:
    choices = p.get("choices")
    if not choices:
        return ""
    cols, tall = choice_layout(choices)
    items = "".join(f'        <li>{rich(str(c).strip(), f"c{no}_{k}", fig_dir, 12.0, g.INK)}</li>\n'
                    for k, c in enumerate(choices, 1))
    return f'      <ol class="n7 c{cols}{" tall" if tall else ""}">\n{items}      </ol>\n'


def work_html(no: str, p: dict, fig_dir: Path) -> str:
    """선생님 쪽 풀 자리. 첫 줄 정답(10pt 회색). solution이 있으면 그 아래 풀이 한 줄 = 한 칸,
    빈 줄은 p.gap. 없으면 정답 줄만 — 답만 적는 정답표다."""
    out = [f'        <p class="answer">정답: '
           f'{rich(str(p["answer"]).strip(), f"a{no}", fig_dir, 10.0, CAPTION)}</p>']
    for i, line in enumerate(str(p.get("solution") or "").strip("\n").split("\n"), 1):
        if not line and i == 1:
            break
        if not line.strip():
            out.append('        <p class="gap"></p>')
        else:
            out.append(f'        <p>{rich(line.strip(), f"s{no}_{i}", fig_dir, 12.0, g.INK)}</p>')
    return "\n".join(out) + "\n"


VERBATIM = False       # yaml의 verbatim: true. 시험기출은 원문 그대로라 평가원 표기 검사를 하지 않는다


def problem_html(no: str, p: dict, fig_dir: Path, teacher: bool) -> str:
    if not teacher and not VERBATIM:
        check_notation(no, p)
    work = work_html(no, p, fig_dir) if teacher else ""
    # 번호 자리의 글. 보통은 번호(001)이고 시험기출의 논술형은 label(논술형 1)이다. 파일 이름과
    # 검사는 늘 번호로 한다
    label = html.escape(str(p.get("label") or no))
    return ('    <div class="col">\n'
            f'      <h2>{label}</h2>\n'
            f'{text_html(no, p, fig_dir)}'
            f'{conditions_html(no, p, fig_dir)}'
            f'{figure_html(no, p, fig_dir)}'
            f'{table_html(no, p, fig_dir)}'
            f'{notes_html(no, p, fig_dir)}'
            f'{choices_html(no, p, fig_dir)}'
            f'      <div class="work box {"t" if teacher else "n"}{no}">\n{work}      </div>\n'
            '    </div>\n')


def page_html(pair: list, head: str, name: bool, fig_dir: Path, teacher: bool) -> str:
    cols = "".join(problem_html(no, p, fig_dir, teacher) for no, p in pair)
    if len(pair) == 1:                          # 마지막 쪽에 문제가 하나면 오른 단은 비운다
        cols += '    <div class="col"></div>\n'
    name_html = '  <p class="name">이름<span class="blank"></span></p>\n' if name else ""
    return ('<section class="exam">\n'
            f'  <p class="series">{html.escape(head)}</p>\n'
            f'{name_html}'
            '  <div class="cols">\n'
            f'{cols}'
            '  </div>\n'
            '</section>\n')


numbers = gb.numbers    # 001, 002, … 또는 yaml이 준 no


def pages(problems: list) -> list[list]:
    items = list(zip(numbers(problems), problems))
    return [items[i:i + 2] for i in range(0, len(items), 2)]


def html_doc(body: list[str], m: dict, out_dir: Path, part: str = "") -> str:
    """쪽 조각들을 HTML 문서 하나로 감싼다. part(문제, 정답)가 있으면 제목 끝에 붙여 두 PDF를 가른다."""
    title = m["head"] + (f" · {part}" if part else "")
    return ('<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
            f'<title>{html.escape(title)}</title>\n'
            f'<link rel="stylesheet" href="{rel(BASE_CSS, out_dir)}">\n'
            f'<link rel="stylesheet" href="{rel(EXAM_CSS, out_dir)}">\n'
            '</head>\n<body>\n\n' + "\n".join(body) + '\n</body>\n</html>\n')


def build_pages(data: dict, m: dict, out_dir: Path) -> tuple[list[str], list[str], list[str]]:
    """학생 쪽 조각들, 선생님 쪽 조각들, 쪽마다 붙일 이름표(학생 쪽 다음 선생님 쪽 차례, 경고에 쓴다)."""
    global VERBATIM
    VERBATIM = bool(data.get("verbatim"))
    problems = data.get("problems") or []
    fig_dir = out_dir / "figures"
    student, teacher, labels = [], [], []
    for i, pair in enumerate(pages(problems)):
        student.append(page_html(pair, m["head"], i == 0, fig_dir, teacher=False))
        labels.append("·".join(no for no, _ in pair))
    if problems:                       # 선생님 쪽은 늘 붙는다. answer가 필수라 정답 줄은 늘 있다
        for pair in pages(problems):
            teacher.append(page_html(pair, m["head"], False, fig_dir, teacher=True))
            labels.append("선생님 " + "·".join(no for no, _ in pair))
    return student, teacher, labels


def build_html(data: dict, m: dict, out_dir: Path) -> tuple[str, list[str], int]:
    """옛 꼴의 HTML 하나(학생 쪽 뒤에 선생님 쪽), 쪽마다 붙일 이름표, 학생 쪽 수."""
    student, teacher, labels = build_pages(data, m, out_dir)
    return html_doc(student + teacher, m, out_dir), labels, len(student)


# ── 검사 ────────────────────────────────────────────────────────────────

def check(problems: list) -> int:
    """yaml에서 흔히 나는 잘못을 문제 번호와 함께 알려 준다. 정답 줄이나 1열 선지가
    단보다 넓으면 경고."""
    if not problems:
        raise SystemExit("problems가 비어 있다")
    bad = 0
    for i, p in enumerate(problems, 1):
        if not isinstance(p, dict):
            raise SystemExit(f"{i}번째 문제가 표가 아니다. '- text: …' 꼴로 적어라")
        # YAML 1.1은 따옴표 없는 no를 거짓으로 읽는다. 조용히 번호가 밀리므로 여기서 잡는다
        if False in p:
            raise SystemExit(f'{i}번째 문제: no는 키와 값을 모두 따옴표로 — "no": "004"처럼 적어라. '
                             "따옴표가 없으면 YAML이 거짓으로 읽어 번호가 무시된다")
        no = str(p.get("no") or f"{i:03d}")
        for key in ("text", "answer"):
            if key not in p:
                raise SystemExit(f"{no}번째 문제에 {key}가 없다")
        # 평가원 문항에는 소문항이 없다. 책의 소문항은 한 물음으로 합친다(2026-09-28 선생님, 삼각비 011)
        if "subs" in p:
            raise SystemExit(f"{no}번째 문제: 소문항(subs)은 쓰지 않는다. 한 물음으로 합쳐라(삼각비 011)")
        if "choices" in p and not isinstance(p["choices"], list):
            raise SystemExit(f"{no}번째 문제: choices는 목록('- …' 다섯 줄)이어야 한다")
        if "choices" in p and len(p["choices"] or []) != 5:
            raise SystemExit(f"{no}번째 문제: 선지는 다섯 개여야 한다")
        if p.get("choices") and choice_layout(p["choices"])[0] == 1:
            for k, c in enumerate(p["choices"], 1):
                if MARK_W + width_of(str(c).strip()) > COL_W:
                    print(f"  ! {no}번째 문제: 선지 {k}번이 단 글 너비를 넘어 두 줄이 된다. 짧게 써라")
                    bad += 1
        w = width_of("정답: " + str(p["answer"]).strip(), 10.0)
        if w > COL_W:
            print(f"  ! {no}번째 문제: 정답 줄 {w:.0f}pt가 단 글 너비 {COL_W:.0f}pt를 넘는다. 짧게 써라")
            bad += 1
        # 풀이의 줄 나눔은 선생님이 정한다. 단 너비를 넘는 줄은 렌더러가 말없이 두 줄로 감으니 여기서 잡는다
        for k, line in enumerate(str(p.get("solution") or "").strip("\n").split("\n"), 1):
            if line.strip() and (w := width_of(line.strip())) > COL_W:
                print(f"  ! {no}번째 문제: 풀이 {k}째 줄 {w:.0f}pt가 단 글 너비 {COL_W:.0f}pt를 넘어 저절로 두 줄이 된다. "
                      "어절에서 갈라라")
                bad += 1
    return bad


def overlap_by_column(boxes: list, labels: list[str]) -> int:
    """잇단 줄 수식 겹침을 단마다 따로 본다. 한 쪽에 문제가 둘이라 쪽 단위면 어느 문제인지 모른다."""
    bad = 0
    for label, page in zip(labels, boxes):
        head = "선생님 " if label.startswith("선생님") else ""
        for no, (x0, x1) in zip(label.split(" ", 1)[-1].split("·"), ((0, 297), (297, 595))):
            bad += check_overlap([[b for b in page if x0 <= b["x"] < x1]], [head + no])
    return bad


def report(boxes: list, labels: list[str], n_student: int, mins: dict | None = None) -> int:
    """풀 자리 상자(학생 쪽 div.work.box.n<번호>, 선생님 쪽 .t<번호>)로 잰다. 넘친 내용을
    WeasyPrint는 바닥 아래로 흘리지 않고 다음 쪽으로 쪼개므로, 상자가 있어야 할 쪽보다 뒤
    쪽에 있으면 그 문제의 블록이 단을 넘친 것이고, 같은 상자가 두 쪽에 걸쳐 있으면 그 안의
    풀이 글이 단 바닥을 넘은 것이다. 학생 쪽은 가장 좁은 단의 칸 수를 알려 주고 8칸 아래인
    단은 단마다 경고한다. 내용이 있는 요소는 글줄 상자까지 같은 class로 나오므로 쪽·이름표마다 맨 위
    상자(블록 상자) 하나만 본다.

    이름표에 n·t를 두는 까닭은 같은 문제 번호가 학생 쪽과 선생님 쪽에 둘 다 있어서다.
    번호만으로 키를 삼으면 학생 쪽 001 다음 쪽에 놓인 선생님 쪽 001을 '쪽을 넘어 이어진
    상자'로 잘못 읽어 shift가 어긋난다."""
    bad = 0
    found: dict[tuple[int, str], dict] = {}          # (쪽, 이름표) → 상자
    for i, page in enumerate(boxes):
        for b in sorted(page, key=lambda b: b["y"]):
            cls = b["class"].split()
            if "work" not in cls:
                continue
            tag = next((c for c in cls if c[:1] in "nt" and len(c) > 1), None)
            if tag is not None and (i, tag) not in found:
                found[(i, tag)] = b
    if len(boxes) != len(labels):
        print(f"  ! 쪽 수 {len(boxes)} ≠ {len(labels)}. 어느 문제가 한 쪽을 넘쳤다 — 아래 줄이 짚는다")
        bad += 1
    shift = 0                                        # 앞에서 밀린 쪽 수
    rows: list[tuple[str, float]] = []
    for i, label in enumerate(labels):
        teacher = i >= n_student
        for no in label.split(" ", 1)[-1].split("·"):
            who = ("선생님 " if teacher else "") + no
            tag = ("t" if teacher else "n") + no
            j = next((k for k in range(i + shift, len(boxes)) if (k, tag) in found), None)
            if j is None:
                print(f"  ! {who}: 풀 자리 상자를 못 찾았다. HTML 구조를 보라")
                bad += 1
                continue
            if j > i + shift:
                print(f"  ! {who}: 문제 블록이 단을 넘쳐 다음 쪽으로 밀렸다. 그림을 줄이거나 선지를 보라")
                bad += 1
                shift = j - i
                continue                             # 이어진 쪽에서 잰 y는 뜻이 없다. 칸 수에 넣지 않는다
            if (j + 1, tag) in found:                # 같은 상자가 다음 쪽에 이어진다
                print(f"  ! {who}: 풀이 글이 단 바닥을 넘어 다음 쪽으로 이어진다. 줄을 줄여라")
                bad += 1
                shift += 1
            if not teacher:
                rows.append((no, (BOTTOM - found[(j, tag)]["y"]) / GRID))
    if rows:
        no, r = min(rows, key=lambda t: t[1])
        print(f"  풀 자리: 가장 좁은 단 {no} {r:.1f}칸")
        for no, r in rows:
            floor = (mins or {}).get(no, MIN_ROWS)
            if r < floor:
                print(f"  ! {no}: 풀 자리 {r:.1f}칸. {floor:g}칸은 두라")
                bad += 1
            elif floor < MIN_ROWS:
                print(f"  {no}: 풀 자리 {r:.1f}칸(원문 분량이라 하한 {floor:g}칸, yaml의 min_rows)")
    return bad


# ── 눈으로 보기 ─────────────────────────────────────────────────────────

def pngs(pdf: Path, problems: list, out: Path, answer_pdf: Path | None = None) -> None:
    """쪽 PNG(p01.png …, 110dpi)와 그림이 있는 문제의 단 크롭(f001.png …, 200dpi). 어느 쪽 어느
    단에 어느 문제가 있는지는 번호에서 정해지므로 크롭은 기계가 자른다 — 사람은 보기만 한다.
    새 꼴은 pdf가 _문제.pdf이고 _정답.pdf의 쪽은 a01.png …로 뽑는다."""
    import fitz
    out.mkdir(parents=True, exist_ok=True)
    d = fitz.open(str(pdf))
    for p in d:
        p.get_pixmap(dpi=110).save(str(out / f"p{p.number + 1:02d}.png"))
    if answer_pdf is not None:
        for p in fitz.open(str(answer_pdf)):
            p.get_pixmap(dpi=110).save(str(out / f"a{p.number + 1:02d}.png"))
    def drawn(p: dict) -> bool:                      # 그림, 별행 수식, 그림 보기 가운데 하나라도 있으면
        return bool(p.get("figure") or DISPLAY.search(str(p.get("text", "")))
                    or any(isinstance(c, dict) for c in (p.get("notes") or [])))

    for i, (no, p) in enumerate(zip(numbers(problems), problems)):
        if not drawn(p):
            continue
        page = d[i // 2]
        x0, x1 = (60, 297) if i % 2 == 0 else (297, 535)
        page.get_pixmap(dpi=200, clip=fitz.Rect(x0, 120, x1, 700)).save(str(out / f"f{no}.png"))
    print(f"  PNG: {out}  (쪽 {len(d)}장, 그림 크롭 {sum(1 for p in problems if drawn(p))}장)")


# ── 빌드 ────────────────────────────────────────────────────────────────

def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")     # Windows 콘솔에서 한글이 깨지지 않게
    ap = argparse.ArgumentParser(description="시험대비 학습지 빌드")
    ap.add_argument("source", type=Path, help="단원 폴더(옛 꼴은 problems.yaml도 된다)")
    ap.add_argument("--no-figures", action="store_true", help="그림 스크립트(figures.py, 문제마다 figure.py)를 실행하지 않는다")
    ap.add_argument("--no-check", action="store_true", help="그리드 검사를 건너뛴다")
    ap.add_argument("--png", type=Path, metavar="DIR",
                    help="쪽마다 PNG(110dpi)와 그림 있는 문제의 단 크롭(200dpi)을 DIR에 뽑는다. 눈으로 볼 때")
    args = ap.parse_args()

    U = seal.U                                            # 단원 읽기(munhang/templates/unit.py)
    if not args.source.exists():
        print(f"입력이 없다: {args.source.resolve()}", file=sys.stderr)
        return 1
    out_dir, data = U.load(args.source)                   # 옛 꼴, 새 꼴 모두. 읽을 수 없으면 까닭을 말하고 멈춘다
    folders = U.is_folders(out_dir)
    src = out_dir / (U.OLD if not folders else U.UNIT)    # 날짜를 못 정할 때 수정 시각을 읽는 파일
    if not src.is_file():                                 # 새 꼴에 unit.yaml이 없으면 가장 늦게 고친 problem.yaml
        src = max((d / U.PROBLEM for d in U.problem_dirs(out_dir)), key=lambda f: f.stat().st_mtime, default=out_dir)
    problems = data.get("problems") or []
    warnings = 0
    if folders:                                           # 사진만 있고 아직 안 옮긴 문제는 빼고 빌드한다
        pending = [d.name for d in U.pending_dirs(out_dir)]
        if pending:
            print(f"  ! {', '.join(pending)}: problem.yaml이 아직 없어 빼고 빌드했다")
            warnings += 1
        if not problems:
            raise SystemExit("문제 폴더에 problem.yaml이 아직 하나도 없다. 사진을 옮겨 적은 뒤 빌드하라")
    warnings += check(problems)
    if folders:
        for no, p in U.numbered(data):
            for msg in U.md_mismatch(out_dir, no, p):     # problem.md와 problem.yaml이 같은 글인가(둘 다 TeX 꼴)
                print(f"  ! {no}: {msg}" + (" 한쪽을 고쳐 맞춰라" if "다르다" in msg else ""))
                warnings += 1
            figs = [p.get("figure")] + DISPLAY.findall(str(p.get("text", ""))) + \
                   [c.get("figure") for c in (p.get("notes") or []) if isinstance(c, dict)]
            for f in [str(f) for f in figs if f]:         # 문제는 제 번호의 그림만 부른다(p007.svg, p007a.svg)
                if not f.startswith(f"p{no}"):
                    print(f"  ! {no}: 그림 {f}는 이 문제 번호로 시작하지 않는다. p{no}.svg처럼 지어라")
                    warnings += 1
    for msg in seal.check(out_dir, data):               # 선생님이 확정한 문항의 글이 바뀌었으면 경고한다
        print(f"  ! {msg}")
        warnings += 1
    for msg in seal.records(out_dir, data):             # 확정 표시와 canon.md 쌍이 봉인과 어긋났으면
        print(f"  ! {msg}")
        warnings += 1
    m = meta(data, out_dir)
    if data.get("verbatim"):
        print("  표기 검사: 원문 그대로(verbatim)라 평가원 표기 검사를 건너뛴다")
    if width_of(m["head"], 10.0) > 475 - 120:       # 첫 쪽 오른쪽 끝의 "이름" 글과 90pt 빈 자리
        print(f"  ! 머리줄 '{m['head']}'이 길어 이름 칸과 겹친다. yaml의 exam·unit을 줄여라")
        warnings += 1

    env = dict(os.environ, PYTHONIOENCODING="utf-8",
               PYTHONPATH=os.pathsep.join(p for p in (str(GRIND), os.environ.get("PYTHONPATH")) if p))
    # PDF 안의 만든 날짜를 고정한다(WeasyPrint는 SOURCE_DATE_EPOCH를 따른다). 학기 첫날이거나
    # yaml의 date. 둘 다 없으면 yaml의 수정 시각
    env["SOURCE_DATE_EPOCH"] = str(m["epoch"] if m["epoch"] is not None else int(src.stat().st_mtime))
    if folders:                                          # 문제마다 figure.py. 한 프로세스에서 차례로 그린다
        scripts = [str(d / U.FIGURE) for d in U.problem_dirs(out_dir) if (d / U.FIGURE).is_file()]
        cmd = [sys.executable, str(HERE / "figrun.py"), *scripts] if scripts else None
    else:
        figures_py = out_dir / "figures.py"
        cmd = [sys.executable, str(figures_py)] if figures_py.is_file() else None
    if cmd and not args.no_figures:
        r = subprocess.run(cmd, cwd=str(out_dir), env=env,
                           stdout=subprocess.PIPE, stderr=None, text=True, encoding="utf-8")
        print(r.stdout, end="", flush=True)
        if r.returncode:
            return r.returncode
        warnings += sum(1 for line in r.stdout.splitlines() if line.lstrip().startswith("!"))
    fig_dir = out_dir / "figures"
    fig_dir.mkdir(exist_ok=True)

    student, teacher, labels = build_pages(data, m, out_dir)
    n_student = len(student)
    if folders:                        # 새 꼴은 PDF 둘. 학생 쪽은 _문제, 선생님 쪽은 _정답(쪽번호 1부터)
        docs = [(out_dir / f"{m['file']}_문제.html", html_doc(student, m, out_dir, "문제")),
                (out_dir / f"{m['file']}_정답.html", html_doc(teacher, m, out_dir, "정답"))]
    else:                              # 옛 꼴은 PDF 하나. 학생 쪽 뒤에 선생님 쪽
        docs = [(out_dir / f"{m['file']}.html", html_doc(student + teacher, m, out_dir))]
    warnings += NAME_WARNINGS
    # 수식 SVG(m 지문 · k 조건 · e 뒷문장 · b 보기 · c 선지 · a 정답 · s 풀이 + 번호)는 빌드마다 다시
    # 그린다. 이번에 안 쓴 것을 지운다. 그림 스크립트가 그린 그림(p*.svg 등)은 건드리지 않는다
    kept = {name for _, doc in docs for name in re.findall(r'src="figures/([^"]+)"', doc)}
    mine = tuple(f"{c}{no}_" for no in numbers(problems) for c in "mkebacstq")
    for old in fig_dir.glob("*.svg"):
        if ((old.name.startswith(mine) or re.fullmatch(r"[mkebacstq]\d{3}(_\d+)+\.svg", old.name))
                and old.name not in kept):
            old.unlink()

    boxes: list = []
    for out_html, doc in docs:
        out_html.write_text(doc, encoding="utf-8", newline="\n")
        print(out_html, flush=True)
        fd, tmp = tempfile.mkstemp(suffix=".json", prefix="exam_boxes_")
        os.close(fd)                   # 열어 둔 채면 Windows에서 지울 수 없다
        boxes_json = Path(tmp)
        cmd = [sys.executable, str(RENDER), str(out_html), "--boxes", str(boxes_json)]
        if not args.no_check:
            cmd.append("--check")
        try:
            r = subprocess.run(cmd, cwd=str(out_dir), env=env)
            if r.returncode:
                warnings += 1          # 그리드·서체 검사가 어긋났다. 아래 검사가 까닭을 짚도록 마저 돌린다
            if not boxes_json.exists() or boxes_json.stat().st_size == 0:
                return r.returncode or 1   # 렌더 자체가 터졌다
            boxes += json.loads(boxes_json.read_text(encoding="utf-8"))   # 학생 쪽 다음 선생님 쪽 차례
        finally:
            boxes_json.unlink(missing_ok=True)
    warnings += overlap_by_column(boxes, labels)
    # 시험기출은 지문과 보기와 선지를 원문 그대로 두어 풀 자리 8칸을 못 지키는 문제가 있다. 그 문제만
    # yaml의 min_rows로 하한을 낮춘다(그림을 줄여도 안 될 때만. 시험대비에는 쓰지 않는다)
    mins = {no: float(p["min_rows"]) for no, p in zip(numbers(problems), problems)
            if p.get("min_rows") is not None}
    warnings += report(boxes, labels, n_student, mins)
    if args.png:
        if folders:
            pngs(out_dir / f"{m['file']}_문제.pdf", problems, args.png, out_dir / f"{m['file']}_정답.pdf")
        else:
            pngs(out_dir / f"{m['file']}.pdf", problems, args.png)
    if warnings:
        print(f"  경고 {warnings}개. 위의 ! 줄을 보라")
    return 1 if warnings else 0


if __name__ == "__main__":
    sys.exit(main())
