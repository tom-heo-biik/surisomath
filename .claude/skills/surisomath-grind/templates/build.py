# -*- coding: utf-8 -*-
"""연마(硏磨) 학습지 빌드 — problems.yaml 하나로 그림·HTML·PDF·그리드 검사까지.

    python build.py 단원폴더/problems.yaml              → 같은 폴더에 HTML과 PDF
    python build.py 단원폴더/problems.yaml --no-figures   그림은 다시 그리지 않는다

하는 일
  1. 단원 폴더에 figures.py가 있으면 실행해 figures/ 에 SVG를 뽑는다.
     grind_figure를 찾도록 이 폴더를 PYTHONPATH에 넣어 준다.
  2. 심볼(symbol.svg)을 figures/ 에 복사한다.
  3. problems.yaml을 읽어 문제 한 개 = 한 쪽인 HTML을 쓴다. 그림마다 SVG 높이가
     units×22pt인지 확인한다. base.css와 grind.css는 저장소 안 상대 경로로 링크한다.
  4. 문제 글과 정답의 $…$는 Computer Modern 수식 SVG로 바꿔 figures/ 에 둔다
     (본문 12pt 검정, 정답 10pt 회색). 수식이 든 어절은 통째로 nowrap이다.
  5. surisomath-a4/templates/render.py 로 PDF를 뽑고 --check 로 그리드를 검사한다.
  6. 쪽마다 두 단 상자를 재서 풀이 자리가 몇 칸인지 알려 준다. 12칸 아래면 경고.

경고가 하나라도 있으면 종료 코드가 1이다. PDF는 그래도 나온다.

problems.yaml
  series: 연마(硏磨)          # 생략하면 연마(硏磨)
  unit: 2026. 9. 12.          # 문서 제목(<title>)에 쓴다. 생략하면 폴더 이름 2026.09.12를 2026. 9. 12.로
  file: 수리소_연마_2026.09.12   # 출력 파일 이름. 생략하면 수리소_연마_<폴더 이름>
                              # 정본 폴더(build/연마/<날짜>/)에서는 세 줄 다 생략한다
  problems:
    - text: 지름이 17cm인 …    # 문제 글. 한 문단. ": "가 들어가면 따옴표로 감싼다
      answer: 5바퀴           # 정답. "정답: " 뒤에 그대로 붙는다
    - text: 점 $(-4,\\,3)$을 지나는 반비례 그래프 $y=\\dfrac{a}{x}\\ (a\\neq 0)$가 …
      answer: $a=-12$        # $…$는 수식(matplotlib mathtext). 조사는 붙여 쓴다
    - "no": "004"             # 번호. 키까지 따옴표로. YAML은 no를 거짓으로 읽는다
      text: …
      figure: p2.svg          # figures/ 안의 그림 파일
      units: 5                # 그림 블록 높이(22pt의 칸 수). figure가 있으면 필수
      alt: …                  # 그림을 글로 적어 둔다. PDF에는 안 찍힌다
      answer: 114.24cm
"""
from __future__ import annotations

import argparse
import html
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import grind_figure as g  # noqa: E402  본문 안 수식을 그린다
A4 = HERE.parents[1] / "surisomath-a4" / "templates"
RENDER = A4 / "render.py"
BASE_CSS = A4 / "base.css"
GRIND_CSS = HERE / "grind.css"
SYMBOL = HERE / "symbol.svg"

DEFAULT_SERIES = "연마(硏磨)"
LEFT, RIGHT = "원석 풀이", "보석 풀이"
GRID = 22.0
BOTTOM = 754.0         # 본문 영역 아래 끝(842 - 88). 두 단 상자가 여기서 끝난다
MIN_ROWS = 12          # 풀이 자리 최소 칸 수
CAPTION = "#636363"    # neutral-500. 정답 줄의 수식 색
MATH = re.compile(r"\$([^$]+)\$")


def rel(target: Path, start: Path) -> str:
    """HTML이 있는 폴더에서 target까지의 상대 경로. 저장소 안이면 어느 PC에서든 같다."""
    return os.path.relpath(target, start).replace(os.sep, "/")


def svg_height(path: Path) -> float | None:
    m = re.search(r'<svg[^>]*\sheight="([\d.]+)pt"', path.read_text(encoding="utf-8")[:4000])
    return float(m.group(1)) if m else None


def rich(s: str, prefix: str, fig_dir: Path, size: float, color: str) -> str:
    """글을 HTML로. $…$는 수식 SVG(img)로 바꾼다.

    수식을 먼저 떼어 내고 나서 어절(공백으로 나뉜 토막)을 나눈다. 수식 안의
    띄어쓰기("$y=ax\\ (a\\neq 0)$")가 어절을 가르면 안 되기 때문이다. 수식이 든
    어절은 span.w로 감싸 안의 글·수식이 한 덩어리로 줄 바꿈되게 한다 —
    "$y=ax$와"에서 조사 '와'가 다음 줄로 떨어지지 않는다. render.py는 class w인
    요소를 건드리지 않는다. 수식이 없는 어절은 그대로 두고 render.py가 nowrap을
    건다."""
    maths: list[str] = []
    NUL = chr(0)                        # 수식 자리표. 글에 나올 리 없는 글자

    def stash(m: re.Match) -> str:
        maths.append(m.group(1))
        return f"{NUL}{len(maths) - 1}{NUL}"

    out = []
    for tok in MATH.sub(stash, s).split():
        if NUL not in tok:
            out.append(html.escape(tok))
            continue
        parts = []
        for j, piece in enumerate(tok.split(NUL)):
            if j % 2 == 0:              # 홀수째 조각이 수식 번호다
                parts.append(html.escape(piece))
                continue
            i = int(piece)
            name = f"{prefix}_{i + 1}.svg"
            w, h, d = g.inline(maths[i], fig_dir / name, size=size, color=color)
            parts.append(f'<img class="mi" src="figures/{name}" alt="{html.escape(maths[i])}" '
                         f'style="height:{h:.2f}pt;vertical-align:{-d:.2f}pt">')
        out.append('<span class="w">' + "".join(parts) + "</span>")
    return " ".join(out)


def problem_html(no: str, p: dict, series: str, fig_dir: Path) -> str:
    text = rich(str(p["text"]).strip(), f"m{no}", fig_dir, 12.0, g.INK)
    answer = rich(str(p["answer"]).strip(), f"a{no}", fig_dir, 10.0, CAPTION)
    fig = ""
    if p.get("figure"):
        if "units" not in p:
            raise SystemExit(f"{no}: figure가 있으면 units(칸 수)가 필요하다")
        units = int(p["units"])
        svg = fig_dir / str(p["figure"])
        if not svg.is_file():
            raise SystemExit(f"{no}: 그림 파일이 없다: {svg}")
        h = svg_height(svg)
        if h is not None and abs(h - units * GRID) > 0.05:
            raise SystemExit(f"{no}: {svg.name} 높이 {h:g}pt ≠ units {units} × 22 = {units * GRID:g}pt. "
                             "yaml의 units와 g.canvas의 units를 맞춰라")
        alt = html.escape(str(p.get("alt", "")))
        fig = (f'  <div class="figure" style="--u:{units}">'
               f'<img src="figures/{svg.name}" alt="{alt}"></div>\n')
    return (
        '<section class="problem">\n'
        f'  <p class="series">{html.escape(series)}</p>\n'
        f'  <h2>{no}</h2>\n'
        f'  <p class="answer">정답: {answer}</p>\n'
        f'  <p>{text}</p>\n'
        f'{fig}'
        '  <div class="cols head">\n'
        f'    <div><h3><img src="figures/symbol.svg" alt=""><span>{LEFT}</span></h3></div>\n'
        f'    <div><h3><img src="figures/symbol.svg" alt=""><span>{RIGHT}</span></h3></div>\n'
        '  </div>\n'
        '  <div class="cols">\n'
        '    <div></div>\n'
        '    <div></div>\n'
        '  </div>\n'
        '</section>\n'
    )


def numbers(problems: list[dict]) -> list[str]:
    return [str(p.get("no") or f"{i:03d}") for i, p in enumerate(problems, 1)]


def check(problems: list[dict]) -> None:
    """yaml에서 흔히 나는 잘못을 문제 번호와 함께 알려 준다."""
    for i, p in enumerate(problems, 1):
        if not isinstance(p, dict):
            raise SystemExit(f"{i}번째 문제가 표가 아니다. '- text: …' 꼴로 적어라")
        # YAML 1.1은 따옴표 없는 no를 거짓으로 읽는다. 조용히 번호가 밀리므로 여기서 잡는다
        if False in p:
            raise SystemExit(f'{i}번째 문제: no를 "no": "{p[False]}" 로 적어라. '
                             "따옴표가 없으면 YAML이 거짓으로 읽어 번호가 무시된다")
        for key in ("text", "answer"):
            if key not in p:
                raise SystemExit(f"{i}번째 문제에 {key}가 없다")


def build_html(data: dict, out_dir: Path) -> str:
    series = data.get("series") or DEFAULT_SERIES
    unit = data.get("unit") or ""
    title = f"{series} {unit}".strip()
    problems = data.get("problems") or []
    if not problems:
        raise SystemExit("problems가 비어 있다")

    body = [problem_html(no, p, series, out_dir / "figures")
            for no, p in zip(numbers(problems), problems)]
    return (
        '<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
        f'<title>{html.escape(title)}</title>\n'
        f'<link rel="stylesheet" href="{rel(BASE_CSS, out_dir)}">\n'
        f'<link rel="stylesheet" href="{rel(GRIND_CSS, out_dir)}">\n'
        '</head>\n<body>\n\n' + "\n".join(body) + '\n</body>\n</html>\n'
    )


def report_space(pdf: Path, nos: list[str]) -> int:
    """쪽마다 두 단 풀이 자리가 몇 칸인지 잰다.

    두 단 상자(테두리)를 PDF에서 직접 재므로 글자에 기대지 않는다. 소제목 글을
    찾아 세던 때는 문제 글에 '원석'이 들어 있으면 그 낱말을 소제목으로 알고
    엉뚱한 값을 냈다. 상자가 아예 없는 쪽은 문제가 한 쪽을 넘쳐 두 단이 잘린
    것이다."""
    try:
        import pdfplumber
    except ImportError:
        print("  (pdfplumber가 없어 풀이 자리 검사를 건너뜀: pip install pdfplumber)")
        return 0
    bad = 0
    rows: list[tuple[str, float]] = []
    with pdfplumber.open(pdf) as doc:
        if len(doc.pages) != len(nos):
            print(f"  ! 쪽 수 {len(doc.pages)} ≠ 문제 수 {len(nos)}. 어느 문제가 한 쪽을 넘쳤다")
            return 1
        for no, page in zip(nos, doc.pages):
            box = [r for r in page.rects
                   if abs(r["bottom"] - BOTTOM) < 1 and r["width"] > 100 and r["height"] > GRID]
            if not box:
                print(f"  ! {no}: 두 단 풀이 자리가 없다. 문제 글이나 그림이 한 쪽을 넘쳤다")
                bad += 1
                continue
            rows.append((no, max(r["height"] for r in box) / GRID))
    if not rows:
        return bad or 1
    no, r = min(rows, key=lambda t: t[1])
    print(f"  풀이 자리: 가장 좁은 쪽 {no} {r:.1f}칸")
    if r < MIN_ROWS:
        print(f"  ! {no}: 풀이 자리 {r:.1f}칸. {MIN_ROWS}칸은 두라(그림 units를 줄이거나 문제 글을 줄인다)")
        bad += 1
    return bad


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")     # Windows 콘솔에서 한글이 깨지지 않게
    ap = argparse.ArgumentParser(description="연마(硏磨) 학습지 빌드")
    ap.add_argument("source", type=Path, help="problems.yaml")
    ap.add_argument("--no-figures", action="store_true", help="figures.py를 실행하지 않는다")
    ap.add_argument("--no-check", action="store_true", help="그리드 검사를 건너뛴다")
    args = ap.parse_args()

    src = args.source.resolve()
    if not src.is_file():
        print(f"입력 파일이 없다: {src}", file=sys.stderr)
        return 1
    out_dir = src.parent
    try:
        data = yaml.safe_load(src.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as e:
        mark = getattr(e, "problem_mark", None)
        where = f" ({mark.line + 1}째 줄)" if mark else ""
        print(f"{src.name}을 읽을 수 없다{where}. ': '가 든 글은 따옴표로 감싸라.",
              file=sys.stderr)
        print(e, file=sys.stderr)
        return 1
    check(data.get("problems") or [])

    env = dict(os.environ, PYTHONIOENCODING="utf-8",
               PYTHONPATH=os.pathsep.join(p for p in (str(HERE), os.environ.get("PYTHONPATH")) if p))
    warnings = 0
    figures_py = out_dir / "figures.py"
    if figures_py.is_file() and not args.no_figures:
        r = subprocess.run([sys.executable, str(figures_py)], cwd=str(out_dir), env=env,
                           stdout=subprocess.PIPE, stderr=None, text=True, encoding="utf-8")
        print(r.stdout, end="", flush=True)
        if r.returncode:
            return r.returncode
        warnings += sum(1 for line in r.stdout.splitlines() if line.lstrip().startswith("!"))
    fig_dir = out_dir / "figures"
    fig_dir.mkdir(exist_ok=True)
    shutil.copyfile(SYMBOL, fig_dir / "symbol.svg")

    # 제목과 파일 이름. 정본 폴더(build/연마/YYYY.MM.DD/)면 날짜에서 만든다 —
    # 제목 '2026. 9. 12.'(a4 날짜 표기), 파일 수리소_연마_2026.09.12
    date = re.fullmatch(r"(\d{4})\.(\d{2})\.(\d{2})", out_dir.name)
    if not data.get("unit") and date:
        data["unit"] = f"{int(date[1])}. {int(date[2])}. {int(date[3])}."
    stem = out_dir.name if date else str(data.get("unit") or "").replace(" ", "")
    name = data.get("file") or f"수리소_연마_{stem}"
    out_html = out_dir / f"{name}.html"
    out_html.write_text(build_html(data, out_dir), encoding="utf-8")
    print(out_html, flush=True)

    cmd = [sys.executable, str(RENDER), str(out_html)]
    if not args.no_check:
        cmd.append("--check")
    r = subprocess.run(cmd, cwd=str(out_dir), env=env)
    if r.returncode:
        return r.returncode
    warnings += report_space(out_html.with_suffix(".pdf"), numbers(data.get("problems") or []))
    if warnings:
        print(f"  경고 {warnings}개. 위의 ! 줄을 보라")
    return 1 if warnings else 0


if __name__ == "__main__":
    sys.exit(main())
