# -*- coding: utf-8 -*-
"""단원 읽기 — 옛 꼴과 새 꼴을 같은 모양으로 돌려준다. 빌드, 봉인, 표기 검사가 함께 쓴다.

옛 꼴(단원 하나에 파일 하나): 단원/problems.yaml(머리 설정 + problems 목록), problems.md, figures.py.
    번호는 목록의 차례(또는 "no"). 20262학기중간의 세 단원과 시험기출, 견본이 이 꼴이다.
새 꼴(문제마다 폴더, 2026-09-30 선생님): 단원/001/problem.yaml(문제 하나), problem.md, figure.py,
    photo.jpg. 번호는 폴더 이름이다. 머리 설정이 필요하면 단원/unit.yaml(series, exam, school, grade,
    unit, file, date, verbatim). 단원에 problems.yaml이 있으면 옛 꼴, 없으면 새 꼴이다.

    load(경로)는 (단원 폴더, data)를 돌려준다. 경로는 단원 폴더, problems.yaml, unit.yaml, 문제 폴더,
    problem.yaml 가운데 무엇이든 된다. data는 머리 설정에 "problems"(문제 목록)를 더한 것이고 새 꼴이면
    문제마다 "no"가 폴더 이름으로 들어 있다.
"""
from __future__ import annotations

import io
import re
from pathlib import Path

OLD = "problems.yaml"          # 옛 꼴의 단원 파일
UNIT = "unit.yaml"             # 새 꼴의 머리 설정(선택)
PROBLEM = "problem.yaml"       # 새 꼴의 문제 하나
PROBLEM_MD = "problem.md"      # 새 꼴의 원문과 되돌리기 기록
FIGURE = "figure.py"           # 새 꼴의 그 문제 그림
NO_RX = re.compile(r"\d{3}")


class UnitError(SystemExit):
    """단원을 읽을 수 없을 때. 빌드와 도구는 이 글을 그대로 보여 주고 멈춘다."""


def unit_dir(path: Path | str) -> Path:
    """어느 경로를 받아도 단원 폴더를 돌려준다."""
    p = Path(path).resolve()
    if p.is_file():
        p = p.parent
    if (p / PROBLEM).is_file() and NO_RX.fullmatch(p.name):
        p = p.parent                   # 문제 폴더를 받았다
    return p


def is_folders(unit: Path) -> bool:
    """새 꼴(문제마다 폴더)인가. problems.yaml이 있으면 옛 꼴이다."""
    return not (unit / OLD).is_file()


def problem_dirs(unit: Path) -> list[Path]:
    """새 꼴의 문제 폴더(001, 002, …) 가운데 problem.yaml이 있는 것을 번호 차례로."""
    return sorted(d for d in unit.iterdir()
                  if d.is_dir() and NO_RX.fullmatch(d.name) and (d / PROBLEM).is_file())


def pending_dirs(unit: Path) -> list[Path]:
    """사진만 있고 problem.yaml이 아직 없는 문제 폴더. 빌드는 이 문제들을 빼고 경고한다(옮기는 중)."""
    return sorted(d for d in unit.iterdir()
                  if d.is_dir() and NO_RX.fullmatch(d.name) and not (d / PROBLEM).is_file())


def _yaml(path: Path) -> dict:
    import yaml
    try:
        with io.open(path, encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
    except yaml.YAMLError as e:
        mark = getattr(e, "problem_mark", None)
        where = f" ({mark.line + 1}째 줄)" if mark else ""
        raise UnitError(f"{path}을 읽을 수 없다{where}. ': '가 든 글은 따옴표로 감싸라.\n{e}") from None
    return data or {}


def load(path: Path | str) -> tuple[Path, dict]:
    """(단원 폴더, data). data["problems"]는 문제 목록이고 새 꼴이면 문제마다 "no"가 폴더 이름이다."""
    unit = unit_dir(path)
    if not unit.is_dir():
        raise UnitError(f"단원 폴더가 없다: {unit}")
    if not is_folders(unit):
        if problem_dirs(unit):
            raise UnitError(f"{unit.name}에 {OLD}와 문제 폴더(001/{PROBLEM})가 함께 있다. 한 꼴로만 둔다")
        data = _yaml(unit / OLD)
        if not isinstance(data, dict):
            raise UnitError(f"{unit / OLD}는 머리 설정과 problems 목록을 가진 표여야 한다")
        return unit, data
    head = _yaml(unit / UNIT) if (unit / UNIT).is_file() else {}
    if "problems" in head:
        raise UnitError(f"{UNIT}에는 머리 설정만 둔다. 문제는 001/{PROBLEM}처럼 폴더마다 둔다")
    problems = []
    for d in problem_dirs(unit):
        p = _yaml(d / PROBLEM)
        if not isinstance(p, dict):
            raise UnitError(f"{d.name}/{PROBLEM}은 '키: 값' 표여야 한다(text, answer …)")
        if False in p or ("no" in p and str(p["no"]) != d.name):
            raise UnitError(f"{d.name}/{PROBLEM}: 번호는 폴더 이름이 정한다. no를 지워라")
        problems.append({**p, "no": d.name})
    if not problems and not pending_dirs(unit):
        raise UnitError(f"{unit}에 {OLD}도 문제 폴더(001/{PROBLEM})도 없다. 단원 폴더가 맞는지 보라")
    return unit, {**head, "problems": problems}


def numbered(data: dict) -> list[tuple[str, dict]]:
    """[(번호, 문제)]. 옛 꼴은 목록 차례나 "no", 새 꼴은 폴더 이름."""
    return [(str(p.get("no") or f"{i:03d}"), p) for i, p in enumerate(data.get("problems") or [], 1)]


def md_sections(unit: Path, no: str) -> dict[str, str] | None:
    """새 꼴 problem.md의 절('## 지문' …)을 {절 이름: 글}로. 파일이 없으면 None."""
    md = unit / no / PROBLEM_MD
    if not md.is_file():
        return None
    secs, cur, buf = {}, None, []
    for line in md.read_text(encoding="utf-8").splitlines() + ["## "]:
        if line.startswith("## "):
            if cur:
                secs[cur] = "\n".join(buf).strip()
            cur, buf = line[3:].strip(), []
        elif cur:
            buf.append(line)
    return secs


def _flat(s) -> str:
    return re.sub(r"\s+", " ", str(s)).strip()


def _where(a: str, b: str) -> str:
    """두 글이 처음 어긋나는 자리의 앞뒤 스무 자쯤을 나란히. 긴 지문에서 사람이 눈으로 찾지 않게 한다."""
    i = next((k for k, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))
    lo = max(0, i - 20)
    return f" 처음 어긋나는 곳: md「…{a[lo:i + 20]}…」, yaml「…{b[lo:i + 20]}…」"


def md_mismatch(unit: Path, no: str, p: dict) -> list[str]:
    """새 꼴에서 problem.md(선생님이 읽고 고치는 원문)와 problem.yaml(빌드 입력)이 같은 글인지 본다.
    둘 다 TeX 꼴이다(2026-09-30 선생님). 지문, 조건((가) …), 뒷문장, 보기(ㄱ. …), 선지(1. …)를 대 본다.
    지문과 뒷문장은 줄바꿈과 겹친 빈칸을 하나로 보고, 조건, 보기, 선지는 한 줄이 한 항목이다. 보기가 그림이면
    (notes 항목이 figure) 보기는 대조하지 않는다. 표와 그림 설명과 책과 달라진 것도 대조하지 않는다."""
    s = md_sections(unit, no)
    if s is None:
        return [f"{PROBLEM_MD}가 없다. 원문(지문, 그림 설명, 선지)을 적어 두어라"]
    out = []

    def items(name: str, rx: str) -> list[str]:
        return [_flat(re.sub(rx, "", line)) for line in s.get(name, "").splitlines() if line.strip()]

    md_text, y_text = _flat(s.get("지문", "")), _flat(p.get("text", ""))
    if md_text != y_text:
        out.append("problem.md의 지문이 problem.yaml의 text와 다르다." + _where(md_text, y_text))
    figure_notes = any(isinstance(x, dict) for x in (p.get("notes") or []))
    for name, key, rx in (("조건", "conditions", r"^\s*\([가-힣]\)\s*"), ("보기", "notes", r"^\s*[ㄱ-ㅎ]\.\s*"),
                          ("선지", "choices", r"^\s*\d+\.\s*")):
        if key == "notes" and figure_notes:
            continue
        want, got = [_flat(x) for x in (p.get(key) or [])], items(name, rx)
        if (name in s or want) and got != want:
            k = next((k for k, (x, y) in enumerate(zip(got, want)) if x != y), None)
            hint = (f" {k + 1}째 항목이 다르다." + _where(got[k], want[k]) if k is not None
                    else f" 항목 수가 md {len(got)}개, yaml {len(want)}개다.")
            out.append(f"problem.md의 {name}이(가) problem.yaml의 {key}와 다르다." + hint)
    md_after, y_after = _flat(s.get("뒷문장", "")), _flat(p.get("after", ""))
    if ("뒷문장" in s or p.get("after")) and md_after != y_after:
        out.append("problem.md의 뒷문장이 problem.yaml의 after와 다르다." + _where(md_after, y_after))
    return out


def confirmed_mark(unit: Path, no: str) -> bool:
    """새 꼴에서 그 문제의 problem.md 첫머리(다섯 줄 안)에 "확정(2026. 9. 30.)" 줄이 있는가."""
    md = unit / no / PROBLEM_MD
    if not md.is_file():
        return False
    head = md.read_text(encoding="utf-8").splitlines()[:5]
    return any(line.startswith("확정(") for line in head)
