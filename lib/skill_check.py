"""선생님이 정한 문서 여덟 규칙으로 마크다운(SKILL.md, references/*.md)을 잰다.
- 본문은 최하위 헤더 아래에만
- H1을 뺀 모든 헤더 위에 빈 줄 둘
- 최하위 헤더와 본문 사이 빈 줄 없음
- 최하위 헤더의 첫 문단(항목이나 코드 블록 앞의 글)은 공백 제외 정확히 200자
- 플레이스홀더는 {중괄호}, 경로는 슬래시
- em dash와 가운뎃점 없음(CLAUDE.md)
사용: python lib/skill_check.py <md> [<md> ...]
      --loose 이면 200자를 알리기만 한다(a4처럼 명세 줄 꼴인 파일)
종료 코드는 어긋난 파일이 있으면 1."""
import io, re, sys


def check(path, strict=True):
    s = io.open(path, encoding="utf-8").read()
    body = s.split("---", 2)[2] if s.startswith("---") else s
    lines = body.split("\n")
    errs, notes = [], []
    hdr = [(i, len(ln.split(" ")[0])) for i, ln in enumerate(lines) if re.match(r"#{1,6} ", ln)]
    in_code = False
    for i, ln in enumerate(lines):
        if ln.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if "—" in ln:
            errs.append(f"{i+1}: em dash")
        if "·" in ln:
            errs.append(f"{i+1}: 가운뎃점")
        plain = re.sub(r"`[^`]*`", "", ln)
        if re.search(r"<[^<>]+>", plain) and not re.match(r"#{1,6} ", ln):
            notes.append(f"{i+1}: 꺾쇠 플레이스홀더? {ln.strip()[:60]}")
        if re.search(r"[A-Za-z가-힣]\\[A-Za-z가-힣]", plain):
            notes.append(f"{i+1}: 역슬래시 경로? {ln.strip()[:60]}")
    for n, (i, lvl) in enumerate(hdr):
        if n > 0 or lvl > 1:
            ok = i >= 2 and lines[i-1] == "" and lines[i-2] == "" and (i < 3 or lines[i-3] != "")
            if not ok:
                errs.append(f"{i+1}: 헤더 위 빈 줄이 둘이 아님 {lines[i]!r}")
        j = hdr[n+1][0] if n + 1 < len(hdr) else len(lines)
        nxt = hdr[n+1][1] if n + 1 < len(hdr) else 0
        content = lines[i+1:j]
        has = any(c.strip() for c in content)
        leaf = not (nxt > lvl)
        if leaf:
            if not has:
                errs.append(f"{i+1}: 최하위 헤더에 본문 없음 {lines[i]!r}")
            elif lines[i+1] == "":
                errs.append(f"{i+1}: 최하위 헤더 아래 빈 줄 {lines[i]!r}")
            else:
                para = []
                for c in content:
                    if c == "" or c.startswith("- ") or c.startswith("```") or re.match(r"\d+\. ", c):
                        break
                    para.append(c)
                n_chars = len("".join(para).replace(" ", ""))
                if para and n_chars != 200:
                    (errs if strict else notes).append(f"{i+1}: 첫 문단 {n_chars}자 ({n_chars-200:+d}) {lines[i]!r}")
                if not para:
                    notes.append(f"{i+1}: 첫 문단 없음(항목이나 코드로 시작) {lines[i]!r}")
        elif has:
            errs.append(f"{i+1}: 최하위가 아닌 헤더 아래 본문 {lines[i]!r}")
    return errs, notes, len(s), len(lines)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    strict = "--loose" not in sys.argv
    rc = 0
    for p in [a for a in sys.argv[1:] if not a.startswith("--")]:
        errs, notes, n, m = check(p, strict)
        print(f"== {p}  {n}자 {m}줄")
        for e in errs:
            print("  !", e)
        for e in notes:
            print("  -", e)
        if not errs:
            print("  이상 없음")
        rc |= bool(errs)
    sys.exit(rc)
