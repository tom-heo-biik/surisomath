# -*- coding: utf-8 -*-
"""확정 문항 봉인 — 선생님이 "됐다"고 한 문항의 글이 다음 세션의 퇴고에서 바뀌지 않게 한다.

단원 폴더의 sealed.json에 문항 번호마다 글의 지문(digest)과 날짜를 적는다. 글은 problems.yaml의
text·conditions·after·table·notes·subs·choices·answer(그림 파일 이름은 뺀다 — 그림 손질은 문항을 바꾸지
않는다). 빌드가 매번 대조해 봉인된 문항의 글이 바뀌었으면 `!`로 멈춘다.

선생님 풀이(solution)가 있는 문항을 봉인하면 풀이의 지문(solution)도 함께 적는다. 풀이도 선생님이 확정한
것이라서다(2026-09-26 "풀이도 봉인", 이차함수 001). 줄 나눔까지 선생님이 정하므로 줄째로 잰다. 풀이 없이
봉인한 문항에 뒤에 풀이를 넣는 것은 막지 않는다(초안은 대화에 쓰고 확정되면 넣는다). 풀이가 확정되면 같은
번호를 다시 봉인해 풀이까지 잠근다.

    python seal.py <problems.yaml> 003 004      봉인(선생님이 확정한 번호만. 풀이가 있으면 풀이까지)
    python seal.py <problems.yaml> --unseal 003  풀기(선생님이 번호를 짚어 풀라고 했을 때)
    python seal.py <problems.yaml> --check       대조. 바뀐 것이 있으면 종료 코드 1
    python seal.py <problems.yaml> --list        봉인 목록(풀이가 봉인된 문항은 풀이 지문도 보인다)

봉인은 사람이 건다. 모델이 알아서 걸거나 풀지 않는다(2026-09-26 선생님 요청 — 원과직선 003·004가 첫 봉인).
"""
from __future__ import annotations

import hashlib
import io
import json
import sys
from pathlib import Path

FIELDS = ("text", "after", "answer")
LISTS = ("conditions", "notes", "subs", "choices")


def digest(p: dict) -> str:
    """문항의 글을 한 줄로 이어 sha1 앞 열두 자리."""
    parts = [str(p.get(k, "")).strip() for k in FIELDS]
    for k in LISTS:
        parts += [str(x).strip() for x in (p.get(k) or [])]
    t = p.get("table") or {}
    if t:
        parts += [str(x) for x in (t.get("head") or [])]
        for row in t.get("rows") or []:
            parts += [str(x) for x in row]
    return hashlib.sha1("\n".join(parts).encode("utf-8")).hexdigest()[:12]


def solution_digest(p: dict) -> str | None:
    """선생님 풀이의 지문. 줄마다 양끝 공백만 지우고 줄 나눔은 그대로 잰다(빈 줄도 한 칸이다). 풀이가 없으면 None."""
    lines = [ln.strip() for ln in str(p.get("solution") or "").strip("\n").split("\n")]
    if not any(lines):
        return None
    return hashlib.sha1("\n".join(lines).encode("utf-8")).hexdigest()[:12]


def numbered(data: dict) -> list[tuple[str, dict]]:
    out = []
    for i, p in enumerate(data.get("problems") or [], 1):
        out.append((str(p.get("no") or f"{i:03d}"), p))
    return out


def seal_path(yaml_path: Path) -> Path:
    return yaml_path.parent / "sealed.json"


def load(yaml_path: Path) -> dict:
    sp = seal_path(yaml_path)
    if not sp.is_file():
        return {}
    with io.open(sp, encoding="utf-8") as fh:
        return json.load(fh)


def save(yaml_path: Path, seals: dict) -> None:
    with io.open(seal_path(yaml_path), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(dict(sorted(seals.items())), fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def check(yaml_path: Path, data: dict) -> list[str]:
    """봉인과 지금 글(과 봉인된 풀이)을 대조해 어긋난 문항마다 경고 글을 돌려준다. 봉인이 없으면 빈 목록."""
    seals = load(yaml_path)
    if not seals:
        return []
    now = dict(numbered(data))
    out = []
    for no, s in seals.items():
        p = now.get(no)
        if p is None:
            out.append(f"{no}: 봉인된 문항이 yaml에 없다(번호가 밀렸나). sealed.json을 보라")
            continue
        if digest(p) != s["digest"]:
            out.append(f"{no}: 확정 문항({s['date']} 봉인)의 글이 바뀌었다. 되돌리거나, 선생님이 풀라고 한 것이면 "
                       f"`python seal.py problems.yaml --unseal {no}` 뒤에 다시 봉인하라")
        if s.get("solution") and solution_digest(p) != s["solution"]:
            out.append(f"{no}: 확정 문항({s['date']} 봉인)의 풀이가 바뀌었다(줄 나눔도 봉인이다). 되돌리거나, "
                       f"선생님이 풀라고 한 것이면 `python seal.py problems.yaml --unseal {no}` 뒤에 다시 봉인하라")
    return out


def main(argv: list[str]) -> int:
    import datetime

    import yaml

    if len(argv) < 3:
        print(__doc__)
        return 2
    yaml_path = Path(argv[1])
    with io.open(yaml_path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    seals = load(yaml_path)
    now = dict(numbered(data))
    cmd, rest = argv[2], argv[3:]
    if cmd == "--check":
        msgs = check(yaml_path, data)
        for m in msgs:
            print("  ! " + m)
        print(f"봉인 대조: {len(seals)}개 중 어긋남 {len(msgs)}개")
        return 1 if msgs else 0
    if cmd == "--list":
        for no, s in sorted(seals.items()):
            sol = f"  풀이 {s['solution']}" if s.get("solution") else ""
            print(f"  {no}  {s['date']}  {s['digest']}{sol}")
        print(f"봉인 {len(seals)}개")
        return 0
    if cmd == "--unseal":
        for no in rest:
            if seals.pop(no, None) is None:
                print(f"  {no}: 봉인이 없다")
            else:
                print(f"  {no}: 풀었다")
        save(yaml_path, seals)
        return 0
    nos = [cmd] + rest
    today = datetime.date.today().isoformat()
    for no in nos:
        if no not in now:
            print(f"  ! {no}: yaml에 없는 번호")
            return 1
        entry = {"date": today, "digest": digest(now[no])}
        sol = solution_digest(now[no])
        if sol:
            entry["solution"] = sol
        seals[no] = entry
        print(f"  {no}: 봉인 {today} {entry['digest']}" + (f"  풀이 {sol}" if sol else "  (풀이 없음)"))
    save(yaml_path, seals)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
