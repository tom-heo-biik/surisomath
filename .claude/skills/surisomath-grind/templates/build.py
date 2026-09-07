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
  4. surisomath-a4/templates/render.py 로 PDF를 뽑고 --check 로 그리드를 검사한다.
  5. 쪽마다 풀이 자리가 몇 칸 남았는지 재서 가장 좁은 쪽을 알려 준다. 12칸 아래면 경고.

경고가 하나라도 있으면 종료 코드가 1이다. PDF는 그래도 나온다.

problems.yaml
  series: 연마(硏磨)          # 생략하면 연마(硏磨)
  unit: 원의 둘레와 넓이       # 문서 제목(<title>)에 쓴다
  file: 수리소_연마_원의둘레와넓이   # 출력 파일 이름. 생략하면 수리소_연마_<unit에서 공백 뺀 것>
  problems:
    - text: 지름이 17cm인 …    # 문제 글. 한 문단. ": "가 들어가면 따옴표로 감싼다
      answer: 5바퀴           # 정답. "정답: " 뒤에 그대로 붙는다
    - no: "004"               # 번호. 생략하면 순서대로 001, 002, …
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
A4 = HERE.parents[1] / "surisomath-a4" / "templates"
RENDER = A4 / "render.py"
BASE_CSS = A4 / "base.css"
GRIND_CSS = HERE / "grind.css"
SYMBOL = HERE / "symbol.svg"

DEFAULT_SERIES = "연마(硏磨)"
LEFT, RIGHT = "원석 풀이", "보석 풀이"
GRID = 22.0
MIN_ROWS = 12          # 풀이 자리 최소 칸 수


def rel(target: Path, start: Path) -> str:
    """HTML이 있는 폴더에서 target까지의 상대 경로. 저장소 안이면 어느 PC에서든 같다."""
    return os.path.relpath(target, start).replace(os.sep, "/")


def svg_height(path: Path) -> float | None:
    m = re.search(r'<svg[^>]*\sheight="([\d.]+)pt"', path.read_text(encoding="utf-8")[:4000])
    return float(m.group(1)) if m else None


def problem_html(no: str, p: dict, series: str, fig_dir: Path) -> str:
    text = html.escape(str(p["text"]).strip())
    answer = html.escape(str(p["answer"]).strip())
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
    """쪽마다 두 단 풀이 자리가 몇 칸인지 잰다. 소제목 줄('원석 풀이')의 자리로 안다.
    소제목 줄상자 위는 72 + 11 + 22m, 풀이 자리는 그 아래 칸부터 754까지다."""
    try:
        import pdfplumber
    except ImportError:
        return 0
    rows: list[tuple[str, float]] = []
    with pdfplumber.open(pdf) as doc:
        if len(doc.pages) != len(nos):
            print(f"  ! 쪽 수 {len(doc.pages)} ≠ 문제 수 {len(nos)}. 어느 문제가 한 쪽을 넘쳤다")
            return 1
        for no, page in zip(nos, doc.pages):
            head = [w for w in page.extract_words() if w["text"].startswith(LEFT[:2])]
            if not head:
                continue
            line_top = (head[0]["top"] + head[0]["bottom"]) / 2 - GRID / 2
            m = round((line_top - 83) / GRID)
            rows.append((no, (754 - 105 - GRID * m) / GRID))
    if not rows:
        return 0
    no, r = min(rows, key=lambda t: t[1])
    print(f"  풀이 자리: 가장 좁은 쪽 {no} {r:.1f}칸")
    if r < MIN_ROWS:
        print(f"  ! {no}: 풀이 자리 {r:.1f}칸. {MIN_ROWS}칸은 두라(그림 units를 줄이거나 문제 글을 줄인다)")
        return 1
    return 0


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
    data = yaml.safe_load(src.read_text(encoding="utf-8")) or {}

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

    unit = str(data.get("unit") or "").replace(" ", "")
    name = data.get("file") or f"수리소_연마_{unit}"
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
