# -*- coding: utf-8 -*-
"""표기 규칙 검사 — 평가원 문형(surisomath-munhang SKILL.md '표기 규칙').

길이·크기라는 수는 식 안에서 기호(\\overline{\\mathrm{AD}}=6, \\angle\\mathrm{B}=90^{\\circ}), 도형 그 자체는
낱말(선분 AC, 각 C, 변 BC). 한 문제에 두 꼴이 같이 보이는 것은 뜻이 달라서다(2026-09-23 선생님 결정,
2026-09-26 삼각비 012를 보고 "어떤 규칙이냐"고 물은 뒤 유지로 확정). 이 검사는 그 경계를 지킨다 —
  (가) 기호가 식 밖에 홀로 있으면("$\\overline{\\mathrm{AC}}$는 …", "$\\angle\\mathrm{C}$의 이등분선") 도형을 기호로 쓴 것
  (나) 낱말 뒤에 = : < > ⊥가 오면("선분 $\\mathrm{AB}$ = 6") 길이를 낱말로 쓴 것
  (다) 한 문장에 한 글자 각(∠A)과 세 글자 각(∠BAC)이 같이 있으면 각의 이름을 섞어 쓴 것. 줄일 수 있으면
       한 글자로(삼각비 019 ∠CAB → ∠A), 없으면 세 글자로(021 ∠A → ∠BAC) 맞춘다. "∠C = 90°인 직각삼각형"은
       003, 005 정본의 정형구라 넘긴다(016)

문형에서는 하나를 더 본다(2026-09-30 선생님 "'다음 그림'은 표기 검사기가 잡게 하자").
  (라) 그림을 놓인 자리로 부르면("다음 그림과 같이", "오른쪽 그림의", "아래 그림에서") 그림 문제는 "그림과 같이 …"로
       연다는 규칙(munhang SKILL '그림과 같이')을 어긴 것. 자리 말 뒤에 "의", "과 같은", "에 주어진", "두", "각"이나
       괄호가 끼어도 잡는다("다음과 같은 그림", "다음 두 그림", "다음 [그림 1]"). 그림자와 그림책, 그림판, 표("아래 표")는
       넘긴다. 자리 말은 낱말 머리에 있을 때만 센다("단위 그림", "1위 그림"의 위는 아니다)

    python .claude/skills/surisomath-munhang/templates/notation.py "{단원 폴더}"
        문제마다 ! 줄을 찍고, 경고가 있으면 종료 코드 1. 옛 꼴은 problems.yaml 경로도 된다.
        verbatim: true인 단원(시험기출)은 빌드처럼 건너뛴다

시험대비 build.py는 check()를 불러 문제 번호를 붙여 찍고 경고 수에 더한다. 연마와 수행평가 빌드에 넣으려면
같은 방식으로 부른다(연마 지문이 문장 안 기호를 쓰는 곳이 있으면 먼저 그것부터 낱말로). 다만 두 양식의 지문은
선생님이 퇴고를 시키기 전에는 도입도 원문 그대로라 (라)가 경고한다(연마 2026.09.12의 002, 003, 수행평가 2026.09.17의 001).
"""
from __future__ import annotations

import re
import sys

MATH_RX = re.compile(r"\$(.+?)\$")
SHAPE_TEX = ("\\overline", "\\angle", "\\overset{\\frown}", "\\triangle", "□")
EXPR_TEX = ("=", ":", "<", ">", "+", "-", "^", "/", "\\perp", "\\parallel", "\\dfrac", "\\frac",
            "\\times", "\\leq", "\\geq", "\\neq", "\\cdot")
WORD_EQ_RX = re.compile(r"(선분|변|현|호|각|지름|반지름) \$\\mathrm\{[A-Z]+\}[^$]*\$ ?(=|:|<|>|⊥)")
ANGLE_RX = re.compile(r"\\angle\s*((?:\\mathrm\{[A-Z]+\}(?:'|_\{[^{}]*\}|_[0-9a-z])?)+)")   # 각 이름, 첨자·프라임 포함
RIGHT_TRI_RX = re.compile(r"\$\\angle\\mathrm\{[A-Z]\}=90\^\{\\circ\}\$인 직각삼각형")        # 정형구
SENTENCE_RX = re.compile(r"(?<=[.?])\s+")
FIGURE_AT_RX = re.compile(                                      # 자리로 부른 그림
    r"(?<![가-힣0-9$])"                                           # 낱말 머리만(단위, 순위, 1위는 아니다)
    r"(?:다음|오른\s?쪽|왼\s?쪽|위\s?쪽|아래\s?쪽|윗\s?쪽|아랫\s?쪽|오른편|왼편|우측|좌측|상단|하단"
    r"|아래|아랫|위|윗|옆|앞|밑의)"                                   # 밑그림(낱말)은 넘기게 밑은 '밑의'만
    r"(?:의|에\s*(?:주어진|있는|제시된|보인)|[과와]\s*같은)?\s*"         # 다음에 주어진 그림, 다음과 같은 그림
    r"(?:(?:두|세|네|다섯|여섯|각|여러|모든)\s+)?"                       # 다음 두 그림, 다음 각 그림
    r"(?:[\[<〈《(（「]\s*)?"                                       # 다음 [그림 1], 오른쪽 〈그림〉
    r"그림(?![자책판])")                                           # 그림자, 그림책, 그림판은 넘긴다


def angle_mix(s: str) -> list[str]:
    """한 문장에 한 글자 각과 세 글자 각이 같이 있으면 그 문장의 각 이름들(∠C, ∠AED)을 돌려준다."""
    out = []
    for sent in SENTENCE_RX.split(RIGHT_TRI_RX.sub("", s)):
        toks = [m.group(1) for m in ANGLE_RX.finditer(sent)]
        sizes = {sum(len(x) for x in re.findall(r"\\mathrm\{([A-Z]+)\}", t)) for t in toks}
        if 1 in sizes and 3 in sizes:
            out.append(", ".join("∠" + re.sub(r"\\mathrm\{([A-Z]+)\}", r"\1", t) for t in toks))
    return out


def check(fields: list[str]) -> list[str]:
    """지문·조건·뒷문장·보기(문자열 목록)에서 규칙을 벗어난 곳을 경고 글 목록으로 돌려준다."""
    out: list[str] = []
    for s in fields:
        for m in FIGURE_AT_RX.finditer(s):
            out.append(f"그림을 놓인 자리로 불렀다('{' '.join(m.group(0).split())}'). 자리 말을 빼고 "
                       f"지문은 '그림과 같이 …'로 연다(munhang SKILL '그림과 같이')")
        for names in angle_mix(s):
            out.append(f"한 문장에 한 글자 각과 세 글자 각이 섞였다({names}). 줄일 수 있으면 한 글자로, "
                       f"없으면 세 글자로 맞춰라")
        for m in MATH_RX.finditer(s):
            tex = m.group(1)
            if any(t in tex for t in SHAPE_TEX) and not any(op in tex for op in EXPR_TEX):
                out.append(f"도형을 기호로 썼다 — ${tex}$. 문장 안의 도형은 낱말(선분 AB, 각 C)로 쓰고, "
                           f"길이·크기라면 식(= : < ⊥)에 넣어라")
        for m in WORD_EQ_RX.finditer(s):
            out.append(f"길이를 낱말로 썼다 — '{m.group(0)}'. 식 안의 길이·크기는 기호"
                       f"(\\overline{{\\mathrm{{AB}}}}=6, \\angle\\mathrm{{B}}=90^{{\\circ}})로")
    return out


def problem_fields(p: dict) -> list[str]:
    """problems.yaml의 문제 하나에서 검사할 글 — text, after, conditions, notes."""
    fields = [str(p.get("text", "")), str(p.get("after", ""))]
    for key in ("conditions", "notes"):
        fields += [str(x) for x in (p.get(key) or [])]
    return fields


def main(argv: list[str]) -> int:
    import importlib.util
    from pathlib import Path

    if len(argv) != 2:
        print("쓰는 법: python notation.py <단원 폴더 또는 problems.yaml>")
        return 2
    name = "munhang_unit"                         # 단원 읽기(옛 꼴, 새 꼴 모두). seal.py와 같은 모듈
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, Path(__file__).resolve().parent / "unit.py")
        sys.modules[name] = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(sys.modules[name])
    U = sys.modules[name]
    _, data = U.load(argv[1])
    if data.get("verbatim"):                      # 시험기출처럼 원문 그대로인 단원은 빌드처럼 건너뛴다
        print("표기 검사: 원문 그대로(verbatim)라 평가원 표기 검사를 건너뛴다")
        return 0
    n = 0
    for no, p in U.numbered(data):
        for msg in check(problem_fields(p)):
            print(f"  ! {no}: {msg}")
            n += 1
    print(f"표기 검사: 경고 {n}개")
    return 1 if n else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
