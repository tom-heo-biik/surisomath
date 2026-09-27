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

    python notation.py <problems.yaml>      문제마다 ! 줄을 찍고, 경고가 있으면 종료 코드 1

시험대비 build.py는 check()를 불러 문제 번호를 붙여 찍고 경고 수에 더한다. 연마·수행평가 빌드에 넣으려면
같은 방식으로 부른다(연마 지문이 문장 안 기호를 쓰는 곳이 있으면 먼저 그것부터 낱말로).
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
    """지문·조건·뒷문장·보기·소문항(문자열 목록)에서 규칙을 벗어난 곳을 경고 글 목록으로 돌려준다."""
    out: list[str] = []
    for s in fields:
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
    """problems.yaml의 문제 하나에서 검사할 글 — text, after, conditions, notes, subs."""
    fields = [str(p.get("text", "")), str(p.get("after", ""))]
    for key in ("conditions", "notes", "subs"):
        fields += [str(x) for x in (p.get(key) or [])]
    return fields


def main(argv: list[str]) -> int:
    import io

    import yaml

    if len(argv) != 2:
        print("쓰는 법: python notation.py <problems.yaml>")
        return 2
    with io.open(argv[1], encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    n = 0
    for i, p in enumerate(data.get("problems") or [], 1):
        no = str(p.get("no") or f"{i:03d}")
        for msg in check(problem_fields(p)):
            print(f"  ! {no}: {msg}")
            n += 1
    print(f"표기 검사: 경고 {n}개")
    return 1 if n else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
