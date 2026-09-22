# -*- coding: utf-8 -*-
"""수행평가 학습지 빌드 — problems.yaml 하나로 그림·수식·표·HTML·PDF·검사까지.

    python build.py 학습지폴더/problems.yaml              → 같은 폴더에 HTML과 PDF
    python build.py 학습지폴더/problems.yaml --no-figures   그림은 다시 그리지 않는다
    python build.py 학습지폴더/problems.yaml --no-check     그리드 검사를 건너뛴다

하는 일
  1. 학습지 폴더에 figures.py가 있으면 실행해 figures/ 에 SVG를 뽑는다. grind_figure를
     찾도록 연마 templates 폴더를 PYTHONPATH에 넣어 준다.
  2. problems.yaml을 읽어 문제 한 개 = 한 쪽인 HTML을 쓴다. 그림은 SVG 높이가 22의 배수인지,
     너비가 본문 너비(475pt) 안인지 본다.
  3. 지문·표·정답·풀이의 $…$는 연마 build.py의 rich()가 Computer Modern SVG로 그린다.
  4. 표(table)는 중1 교과서의 도수분포표 꼴로 조판한다. 제목은 표 위 가운데, 빈 칸은 빈 셀,
     계급의 이상·미만은 `0^이상~20^미만`처럼 ^ 뒤에 적으면 위첨자가 된다. `{답: 9}`로 적은 칸은
     학생 쪽에서 빈 칸이고 선생님 쪽에서 회색 값이다.
  5. 학생 쪽 뒤에 선생님 쪽을 같은 차례로 붙인다(문제 셋이면 4~6쪽). 양식은 같고 머리줄 오른쪽
     끝에 정답(연마와 같다), solution이 있으면 빈 자리 위부터 풀이 한 줄 = 한 칸.
  6. surisomath-a4/templates/render.py 로 PDF를 뽑고 --check 로 그리드를 검사한다.
  7. 빈 자리의 위 끝(학생 쪽 div.work.box.n<번호>, 선생님 쪽 .t<번호>)을 받아 가장 좁은 쪽의 남은
     칸을 알려 주고, 문제 블록이 한 쪽을 넘쳐 밀린 문제와 풀이가 바닥을 넘은 문제를 짚는다.
     빈 자리가 12칸 아래면, 머리줄이 이름 칸·정답과 겹치면, 잇단 줄의 수식이 겹치면 경고.

경고가 하나라도 있으면 종료 코드가 1이다. PDF는 그래도 나온다.

problems.yaml
  term: 2026학년도 2학기        # 생략하면 학기 폴더 이름(20262학기)에서 만든다
  school: 수지중학교            # 생략하면 학교 폴더 이름
  grade: 중1                   # 생략하면 학년 폴더 이름
  date: 2026.09.17             # 수행평가 날짜. 생략하면 학습지 폴더 이름(2026.09.17). 머리줄과 PDF 날짜에 쓴다
  file: 수리소_수행평가_…        # 생략하면 수리소_수행평가_수지중학교_중1_2026.09.17
  problems:
    - text: 다음 그림과 같이 …   # 지문. 원문 문장 그대로, 표기만 조판. ": "가 들어가면 따옴표로 감싼다
      figure: p1.svg           # figures/ 안의 그림. units는 없다 — SVG 높이가 칸 수를 정한다
      alt: …                   # 그림 설명. PDF에는 안 찍힌다
      table:                   # 표. 그림과 함께 있어도 된다(그림이 먼저)
        title: 시영이의 사격 점수   # 표 제목. 표 위 가운데. 생략 가능
        head: [점수(점), 5, 6]     # 머리 행. 생략 가능
        rows:                     # 몸 행. 빈 칸은 "" — 학생이 채운다. {답: 9}는 학생 쪽 빈 칸·선생님 쪽 회색 9
          - [횟수(회), 2, 1]
      answer: 8점              # 정답. 필수 — 선생님 쪽 머리줄 오른쪽 끝에 찍힌다
      solution: |              # 선생님 풀이(선택). 줄마다 한 칸. 빈 줄은 한 칸을 비운다
        주어진 그림에서 …
    - "no": "004"              # 번호를 직접 줄 때. 키까지 따옴표로(YAML은 no를 거짓으로 읽는다)
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
EXAM = SKILLS / "surisomath-exam" / "templates"
RENDER = A4 / "render.py"
BASE_CSS = A4 / "base.css"
ASSESS_CSS = HERE / "assess.css"

sys.path.insert(0, str(GRIND))
import grind_figure as g  # noqa: E402  본문 안 수식을 그린다


def _load(name: str, path: Path):
    """다른 스킬의 build.py를 모듈로 읽는다(__main__ 가드가 있다). 같은 코드를 복사하지 않는다."""
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


eb = _load("exam_build", EXAM / "build.py")    # 시험대비 build.py. 연마 build.py(gb)를 안에서 읽는다
gb = eb.gb
rich, rel, svg_height, check_overlap, numbers = gb.rich, gb.rel, gb.svg_height, gb.check_overlap, gb.numbers
svg_width, width_of = eb.svg_width, eb.width_of

SERIES = "수행평가"
GRID = 22.0
BOTTOM = 754.0         # 본문 영역 아래 끝(842 - 88). 빈 자리가 여기서 끝난다
WIDTH = 475.0          # 본문 너비(pt). 그림은 이보다 넓을 수 없다
MIN_ROWS = 12          # 빈 자리 최소 칸 수. 서술형 답안을 손으로 쓰는 자리다
CAPTION = gb.CAPTION   # neutral-500. 정답 줄과 표의 답 칸
ANS_KEY = "답"         # 표의 답 칸 {답: 9}
TERM = re.compile(r"(\d{4})(\d)학기")
DATE = re.compile(r"(\d{4})\.(\d{1,2})\.(\d{1,2})")
SUP = re.compile(r"\^([가-힣]+)")       # 계급의 이상·미만 위첨자


# ── 머리줄 · 파일 이름 · 날짜 ─────────────────────────────────────────────

def meta(data: dict, out_dir: Path) -> dict:
    """머리줄·파일 이름·PDF 날짜. 폴더 build/수행평가/<학기>/<학교>/<학년>/<날짜>/ 에서 만들고
    yaml의 term·school·grade·date·file이 있으면 그것이 이긴다."""
    parents = [p.name for p in out_dir.parents[:3]]
    t = TERM.fullmatch(parents[2]) if len(parents) > 2 else None
    term = data.get("term") or (t and f"{t[1]}학년도 {t[2]}학기")
    school = data.get("school") or (parents[1] if len(parents) > 1 else None)
    grade = data.get("grade") or (parents[0] if parents else None)
    d = DATE.fullmatch(str(data.get("date") or out_dir.name).strip())
    if not (term and school and grade and d):
        raise SystemExit("폴더가 build/수행평가/<YYYY><N>학기/<학교>/<학년>/<YYYY.MM.DD>/ 꼴이 아니다. "
                         "problems.yaml에 term·school·grade·date를 적어라")
    y, mo, da = int(d[1]), int(d[2]), int(d[3])
    date = f"{y}. {mo}. {da}."                               # a4 날짜 표기
    stem = f"수리소_수행평가_{school}_{grade}_{y}.{mo:02d}.{da:02d}"
    return {"term": str(term), "school": str(school), "grade": str(grade), "date": date,
            "file": str(data.get("file") or stem).replace(" ", ""),
            "epoch": calendar.timegm((y, mo, da, 0, 0, 0)),
            "head": f"{SERIES} · {term} · {school} · {grade} · {date}"}


# ── HTML ────────────────────────────────────────────────────────────────

def figure_html(no: str, p: dict, fig_dir: Path) -> str:
    if not p.get("figure"):
        return ""
    svg = fig_dir / str(p["figure"])
    if not svg.is_file():
        raise SystemExit(f"{no}: 그림 파일이 없다: {svg}")
    h, w = svg_height(svg), svg_width(svg)
    if h is None or w is None:
        raise SystemExit(f"{no}: {svg.name}의 크기를 읽을 수 없다. grind_figure.save()로 만든 SVG여야 한다")
    units = round(h / GRID)
    if abs(h - units * GRID) > 0.05:
        raise SystemExit(f"{no}: {svg.name} 높이 {h:g}pt가 22의 배수가 아니다. g.canvas의 units를 보라")
    if w > WIDTH + 0.05:
        raise SystemExit(f"{no}: {svg.name} 너비 {w:.0f}pt가 본문 너비 {WIDTH:.0f}pt를 넘는다. "
                         f"y 범위를 {w / WIDTH:.2f}배 넓혀 배율을 줄여라")
    alt = html.escape(str(p.get("alt", "")))
    return (f'  <div class="figure" style="--u:{units}">'
            f'<img src="figures/{svg.name}" alt="{alt}"></div>\n')


def cell_value(no: str, c) -> tuple[str, bool]:
    """(칸의 글, 답 칸인지). {답: 9}는 답 칸 — 학생 쪽에서 빈 칸, 선생님 쪽에서 회색 값."""
    if isinstance(c, dict):
        if set(c) != {ANS_KEY}:
            raise SystemExit(f"{no}: 표의 칸은 값이거나 {{{ANS_KEY}: 값}}이어야 한다: {c}")
        v = c[ANS_KEY]
        return ("" if v is None else str(v).strip()), True
    return ("" if c is None else str(c).strip()), False


def cell_html(no: str, c, tag: str, k: int, fig_dir: Path, teacher: bool) -> str:
    """표 한 칸. 빈 값("", null)은 빈 셀 — 학생이 채운다. $…$는 10pt 수식, ^이상·^미만은 위첨자.
    답 칸은 학생 쪽에서 빈 셀, 선생님 쪽에서 회색(캡션 색) 값이다."""
    s, ans = cell_value(no, c)
    if not s or (ans and not teacher):
        return f"<{tag}></{tag}>"
    color = CAPTION if ans else g.INK
    inner = SUP.sub(r"<sup>\1</sup>", rich(s, f"t{no}_{k}", fig_dir, 10.0, color))
    cls = ' class="ans"' if ans else ""
    return f"<{tag}{cls}>{inner}</{tag}>"


def table_html(no: str, p: dict, fig_dir: Path, teacher: bool) -> str:
    t = p.get("table")
    if not t:
        return ""
    if not isinstance(t, dict) or not isinstance(t.get("rows"), list) or not t["rows"]:
        raise SystemExit(f"{no}: table은 title·head·rows(행 목록)를 가진 표여야 한다")
    head = t.get("head")
    rows = t["rows"]
    ncol = len(head) if head else len(rows[0])
    for r in ([head] if head else []) + rows:
        if not isinstance(r, list) or len(r) != ncol:
            raise SystemExit(f"{no}: 표의 행마다 칸 수가 {ncol}로 같아야 한다: {r}")
    # 표의 첫 행에 class first — 위선(--top)은 이 행에만 건다. caption이 첫 자식이라 base.css의
    # thead:first-child 선택자가 안 잡히고, 첫 행이 아닌 행에 위선을 걸면 그 행부터 0.4pt씩 밀린다
    k = 0
    first = ' class="first"'
    out = ['  <table class="stat">']
    if t.get("title"):
        out.append(f'    <caption>{html.escape(str(t["title"]).strip())}</caption>')
    if head:
        cells = []
        for c in head:
            k += 1
            cells.append(cell_html(no, c, "th", k, fig_dir, teacher))
        out.append(f"    <thead>\n      <tr{first}>" + "".join(cells) + "</tr>\n    </thead>")
        first = ""
    out.append("    <tbody>")
    for r in rows:
        cells = []
        for c in r:
            k += 1
            cells.append(cell_html(no, c, "td", k, fig_dir, teacher))
        out.append(f"      <tr{first}>" + "".join(cells) + "</tr>")
        first = ""
    out.append("    </tbody>\n  </table>\n")
    return "\n".join(out)


def solution_html(no: str, p: dict, fig_dir: Path) -> str:
    """선생님 풀이. 빈 자리 위부터 줄마다 p 하나(문단 간격 없음), 빈 줄은 p.gap으로 한 칸을 비운다.
    정답은 여기가 아니라 머리줄 오른쪽 끝에 있다(연마와 같다)."""
    out = []
    for i, line in enumerate(str(p.get("solution") or "").strip("\n").split("\n"), 1):
        if not line and i == 1:
            break
        if not line.strip():
            out.append('    <p class="gap"></p>')
        else:
            out.append(f'    <p>{rich(line.strip(), f"s{no}_{i}", fig_dir, 12.0, g.INK)}</p>')
    return "".join(s + "\n" for s in out)


def problem_html(no: str, p: dict, head: str, name: bool, fig_dir: Path, teacher: bool) -> str:
    """문제 한 쪽. teacher면 선생님 쪽 — 같은 양식에 머리줄 오른쪽 끝에 정답, 빈 자리에 풀이."""
    text = rich(str(p["text"]).strip(), f"m{no}", fig_dir, 12.0, g.INK)
    name_html = '  <p class="name">이름<span class="blank"></span></p>\n' if name and not teacher else ""
    answer = (f'  <p class="answer">정답: {rich(str(p["answer"]).strip(), f"a{no}", fig_dir, 10.0, CAPTION)}</p>\n'
              if teacher else "")
    work = solution_html(no, p, fig_dir) if teacher else ""
    tag = ("t" if teacher else "n") + no
    return ('<section class="assess">\n'
            f'  <p class="series">{html.escape(head)}</p>\n'
            f'{name_html}{answer}'
            f'  <h2>{no}</h2>\n'
            f'  <p>{text}</p>\n'
            f'{figure_html(no, p, fig_dir)}'
            f'{table_html(no, p, fig_dir, teacher)}'
            f'  <div class="work box {tag}">\n{work}  </div>\n'
            '</section>\n')


def build_html(data: dict, m: dict, out_dir: Path) -> tuple[str, list[str], int]:
    """HTML 전체, 쪽마다 붙일 이름표(경고에 쓴다), 학생 쪽 수. 선생님 쪽은 학생 쪽 뒤에 같은 차례로."""
    problems = data.get("problems") or []
    fig_dir = out_dir / "figures"
    nos = numbers(problems)
    body = [problem_html(no, p, m["head"], i == 0, fig_dir, teacher=False)
            for i, (no, p) in enumerate(zip(nos, problems))]
    labels = list(nos)
    body += [problem_html(no, p, m["head"], False, fig_dir, teacher=True) for no, p in zip(nos, problems)]
    labels += ["선생님 " + no for no in nos]
    doc = ('<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
           f'<title>{html.escape(m["head"])}</title>\n'
           f'<link rel="stylesheet" href="{rel(BASE_CSS, out_dir)}">\n'
           f'<link rel="stylesheet" href="{rel(ASSESS_CSS, out_dir)}">\n'
           '</head>\n<body>\n\n' + "\n".join(body) + '\n</body>\n</html>\n')
    return doc, labels, len(nos)


# ── 검사 ────────────────────────────────────────────────────────────────

def check(problems: list) -> None:
    """yaml에서 흔히 나는 잘못을 문제 번호와 함께 알려 준다."""
    if not problems:
        raise SystemExit("problems가 비어 있다")
    for i, p in enumerate(problems, 1):
        if not isinstance(p, dict):
            raise SystemExit(f"{i}번째 문제가 표가 아니다. '- text: …' 꼴로 적어라")
        # YAML 1.1은 따옴표 없는 no를 거짓으로 읽는다. 조용히 번호가 밀리므로 여기서 잡는다
        if False in p:
            raise SystemExit(f'{i}번째 문제: no는 키와 값을 모두 따옴표로 — "no": "004"처럼 적어라. '
                             "따옴표가 없으면 YAML이 거짓으로 읽어 번호가 무시된다")
        for key in ("text", "answer"):
            if key not in p:
                raise SystemExit(f"{i}번째 문제에 {key}가 없다")


def report(boxes: list, labels: list[str], n_student: int) -> int:
    """빈 자리 상자(학생 쪽 div.work.box.n<번호>, 선생님 쪽 .t<번호>)로 잰다. 넘친 내용을 WeasyPrint는
    바닥 아래로 흘리지 않고 다음 쪽으로 쪼개므로, 상자가 있어야 할 쪽보다 뒤에 있으면 그 문제의
    블록이 한 쪽을 넘친 것이고, 같은 상자가 두 쪽에 걸쳐 있으면 그 안의 풀이 글이 바닥을 넘은
    것이다. 학생 쪽은 가장 좁은 쪽의 칸 수를 알려 주고 MIN_ROWS 아래인 쪽은 쪽마다 경고한다.
    내용이 있는 요소는 글줄 상자까지 같은 class로 나오므로 쪽·이름표마다 맨 위 상자 하나만 본다."""
    bad = 0
    found: dict[tuple[int, str], dict] = {}
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
    shift = 0
    rows: list[tuple[str, float]] = []
    for i, label in enumerate(labels):
        teacher = i >= n_student
        no = label.split(" ", 1)[-1]
        tag = ("t" if teacher else "n") + no
        j = next((k for k in range(i + shift, len(boxes)) if (k, tag) in found), None)
        if j is None:
            print(f"  ! {label}: 빈 자리 상자를 못 찾았다. HTML 구조를 보라")
            bad += 1
            continue
        if j > i + shift:
            print(f"  ! {label}: 문제 블록이 한 쪽을 넘쳐 다음 쪽으로 밀렸다. 그림이나 표를 줄여라")
            bad += 1
            shift = j - i
            continue
        if (j + 1, tag) in found:                # 같은 상자가 다음 쪽에 이어진다
            print(f"  ! {label}: 풀이 글이 바닥을 넘어 다음 쪽으로 이어진다. 줄을 줄여라")
            bad += 1
            shift += 1
        if not teacher:
            rows.append((no, (BOTTOM - found[(j, tag)]["y"]) / GRID))
    if rows:
        no, r = min(rows, key=lambda t: t[1])
        print(f"  빈 자리: 가장 좁은 쪽 {no} {r:.1f}칸")
        for no, r in rows:
            if r < MIN_ROWS:
                print(f"  ! {no}: 빈 자리 {r:.1f}칸. {MIN_ROWS}칸은 두라(그림 units를 줄이거나 표를 줄인다)")
                bad += 1
    return bad


# ── 빌드 ────────────────────────────────────────────────────────────────

def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")     # Windows 콘솔에서 한글이 깨지지 않게
    ap = argparse.ArgumentParser(description="수행평가 학습지 빌드")
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
        print(f"{src.name}을 읽을 수 없다{where}. ': '가 든 글은 따옴표로 감싸라.", file=sys.stderr)
        print(e, file=sys.stderr)
        return 1
    problems = data.get("problems") or []
    check(problems)
    m = meta(data, out_dir)
    warnings = 0
    head_w = width_of(m["head"], 10.0)
    if head_w > WIDTH - 120:                        # 첫 쪽 오른쪽 끝의 "이름" 글과 90pt 빈 자리
        print(f"  ! 머리줄 '{m['head']}'이 길어 이름 칸과 겹친다. yaml의 term·school을 줄여라")
        warnings += 1
    for no, p in zip(numbers(problems), problems):   # 선생님 쪽 머리줄 오른쪽 끝의 정답
        w = width_of("정답: " + str(p["answer"]).strip(), 10.0)
        if head_w + 16 + w > WIDTH:
            print(f"  ! {no}: 정답 줄 {w:.0f}pt가 머리줄과 겹친다. 짧게 써라")
            warnings += 1

    env = dict(os.environ, PYTHONIOENCODING="utf-8",
               PYTHONPATH=os.pathsep.join(p for p in (str(GRIND), os.environ.get("PYTHONPATH")) if p))
    # PDF 안의 만든 날짜를 수행평가 날짜로 고정한다(WeasyPrint는 SOURCE_DATE_EPOCH를 따른다).
    # 같은 입력이면 PDF도 바이트 단위로 같아 git이 바뀐 것으로 보지 않는다
    env["SOURCE_DATE_EPOCH"] = str(m["epoch"])
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

    doc, labels, n_student = build_html(data, m, out_dir)
    # 수식 SVG(m 지문 · t 표 · a 정답 · s 풀이 + 번호)는 빌드마다 다시 그린다. 이번에 안 쓴 것을
    # 지운다. figures.py가 그린 그림(p*.svg 등)은 건드리지 않는다
    kept = set(re.findall(r'src="figures/([^"]+)"', doc))
    for old in fig_dir.glob("*.svg"):
        if re.fullmatch(r"[mtas]\d{3}(_\d+)+\.svg", old.name) and old.name not in kept:
            old.unlink()
    out_html = out_dir / f"{m['file']}.html"
    out_html.write_text(doc, encoding="utf-8")
    print(out_html, flush=True)

    fd, tmp = tempfile.mkstemp(suffix=".json", prefix="assess_boxes_")
    os.close(fd)                       # 열어 둔 채면 Windows에서 지울 수 없다
    boxes_json = Path(tmp)
    cmd = [sys.executable, str(RENDER), str(out_html), "--boxes", str(boxes_json)]
    if not args.no_check:
        cmd.append("--check")
    try:
        r = subprocess.run(cmd, cwd=str(out_dir), env=env)
        if r.returncode:
            warnings += 1              # 그리드·서체 검사가 어긋났다. 아래 검사가 까닭을 짚도록 마저 돌린다
        if not boxes_json.exists() or boxes_json.stat().st_size == 0:
            return r.returncode or 1   # 렌더 자체가 터졌다
        boxes = json.loads(boxes_json.read_text(encoding="utf-8"))
    finally:
        boxes_json.unlink(missing_ok=True)
    warnings += check_overlap(boxes, labels)
    warnings += report(boxes, labels, n_student)
    if warnings:
        print(f"  경고 {warnings}개. 위의 ! 줄을 보라")
    return 1 if warnings else 0


if __name__ == "__main__":
    sys.exit(main())
