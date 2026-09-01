"""수리소 수학학원 문서 양식 — HTML을 PDF로 렌더한다.

    python render.py 문서.html                 → 문서.pdf
    python render.py 문서.html -o 결과.pdf
    python render.py 문서.html --check         → 렌더 후 베이스라인 그리드 검사

하는 일
  1. Windows에서 GTK 런타임 경로를 자동으로 잡는다(WeasyPrint의 네이티브 의존성).
  2. 본문 텍스트를 어절 단위로 <span class="w">로 감싼다.
     WeasyPrint는 word-break:keep-all을 지원하지 않아 한글이 어절 중간에서
     끊긴다. white-space:nowrap을 어절마다 걸어야 어절 단위 줄 바꿈이 된다.
  3. 스타일시트 링크가 없으면 base.css를 자동으로 붙인다.
  4. 렌더한 PDF에 양식 서체가 실제로 박혔는지 확인한다.
"""

import argparse
import os
import re
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE_CSS = HERE / "base.css"
GRID = 22.0
FONT = "KoPubWorld"     # base.css 가 쓰는 서체. 이게 안 박히면 그리드가 통째로 밀린다

# WeasyPrint가 쓰는 GTK 런타임 (Windows)
GTK_DIRS = [
    r"C:\Program Files\GTK3-Runtime Win64\bin",
    r"C:\msys64\mingw64\bin",
]


def setup_gtk() -> None:
    if os.name != "nt":
        return
    for d in GTK_DIRS:
        if os.path.isdir(d):
            os.add_dll_directory(d)
            os.environ["PATH"] = d + os.pathsep + os.environ["PATH"]
            return


def import_weasyprint():
    """GLib이 stderr로 쏟는 UWP 경고를 삼키고 import한다."""
    setup_gtk()
    if os.name != "nt":
        import weasyprint
        return weasyprint

    saved = os.dup(2)
    buf = tempfile.TemporaryFile()
    os.dup2(buf.fileno(), 2)
    try:
        import weasyprint
    except Exception:
        os.dup2(saved, 2)
        buf.seek(0)
        sys.stderr.write(buf.read().decode("utf-8", "replace"))
        raise
    else:
        os.dup2(saved, 2)
        buf.seek(0)
        noise = re.compile(r"GLib-GIO-WARNING|^\(process:|^\s*$")
        for line in buf.read().decode("utf-8", "replace").splitlines():
            if not noise.search(line):
                sys.stderr.write(line + "\n")
        return weasyprint
    finally:
        os.close(saved)
        buf.close()


# --- 어절 단위 줄 바꿈 ------------------------------------------------------

XHTML = "{http://www.w3.org/1999/xhtml}"
SKIP_TAGS = {"script", "style", "pre", "code", "textarea", "head", "title"}
SKIP_CLASSES = {"w", "math", "raw"}
SPACE = re.compile(r"(\s+)")


def _local(tag) -> str:
    return tag.rsplit("}", 1)[-1] if isinstance(tag, str) else ""


def _span(word: str):
    el = ET.Element("span")
    el.set("class", "w")
    el.text = word
    return el


def _split(text: str):
    """텍스트를 (어절 span | 공백 텍스트) 시퀀스로 쪼갠다."""
    out = []
    for part in SPACE.split(text):
        if not part:
            continue
        out.append(("t", part) if part.isspace() else ("e", _span(part)))
    return out


def _sequence(el):
    """el의 자식/텍스트를 순서대로 납작하게 편다."""
    seq = []
    if el.text:
        seq.append(("t", el.text))
    for child in el:
        seq.append(("e", child))
        if child.tail:
            seq.append(("t", child.tail))
            child.tail = None
    el.text = None
    return seq


def _rebuild(el, seq):
    el.text = None
    for child in list(el):
        el.remove(child)
    last = None
    for kind, val in seq:
        if kind == "e":
            el.append(val)
            last = val
        elif last is None:
            el.text = (el.text or "") + val
        else:
            last.tail = (last.tail or "") + val


def wrap_eojeol(el) -> None:
    """직계 텍스트를 어절 span으로 감싸고 자식으로 내려간다."""
    if _local(el.tag) in SKIP_TAGS:
        return
    if SKIP_CLASSES & set((el.get("class") or "").split()):
        return
    for child in list(el):
        wrap_eojeol(child)
    seq = []
    for kind, val in _sequence(el):
        seq.extend(_split(val) if kind == "t" else [(kind, val)])
    _rebuild(el, seq)


def prepare(src: Path) -> tuple[str, bool]:
    """HTML을 읽어 어절 처리하고, 스타일시트 링크 유무를 함께 돌려준다."""
    import tinyhtml5

    tree = tinyhtml5.parse(src.read_text(encoding="utf-8"))
    root = tree.getroot() if hasattr(tree, "getroot") else tree

    for el in root.iter():
        if isinstance(el.tag, str) and el.tag.startswith(XHTML):
            el.tag = el.tag[len(XHTML):]

    has_css = any(
        _local(el.tag) == "link" and "stylesheet" in (el.get("rel") or "")
        for el in root.iter()
    )

    body = root.find("body")
    wrap_eojeol(body if body is not None else root)

    html = ET.tostring(root, encoding="unicode", method="html")
    return "<!doctype html>\n" + html, has_css


# --- 그리드 검사 ------------------------------------------------------------

def check_grid(pdf_path: Path) -> int:
    """모든 글줄의 베이스라인이 22pt 그리드 위에 있는지 본다.

    베이스라인이 줄상자 안에서 놓이는 높이는 글자 크기마다 다르다. 그래서
    크기별로 묶어 잔여값(mod 22)이 문서 전체에서 같은지를 본다. 표 테두리가
    행 높이를 늘리거나, 쪽 맨 위에 여백이 남는 식으로 그리드가 밀리면 잡힌다.

    허용오차 0.25pt — 표 셀은 행간이 21.6pt라 같은 10pt 글자여도 베이스라인이
    본문보다 0.2pt 아래에 놓인다. 줄상자는 그리드 위에 있으므로 이 정도는 통과
    시키고, 행마다 쌓이는 0.4pt 밀림이나 쪽 맨 위 11pt 밀림은 잡는다.
    """
    try:
        import pdfplumber
    except ImportError:
        print("  (pdfplumber가 없어 검사를 건너뜀: pip install pdfplumber)")
        return 0

    lines = []          # (쪽, 베이스라인, 크기)
    with pdfplumber.open(pdf_path) as pdf:
        for pno, page in enumerate(pdf.pages, 1):
            folio_top = page.height - 88          # 쪽번호 영역은 뺀다
            seen = set()
            for c in page.chars:
                base = round(page.height - c["matrix"][5], 2)
                size = round(c["size"], 1)
                if base < folio_top and (base, size) not in seen:
                    seen.add((base, size))
                    lines.append((pno, base, size))

    ref: dict[float, float] = {}
    bad = 0
    for pno, base, size in sorted(lines, key=lambda r: (r[2], r[0], r[1])):
        residue = base % GRID
        if size not in ref:
            ref[size] = residue
            continue
        off = abs(residue - ref[size])
        off = min(off, GRID - off)
        if off > 0.25:
            print(f"  ! p{pno} {size}pt 줄 base={base:.2f} — 그리드에서 {off:.2f}pt 벗어남")
            bad += 1

    print(f"  그리드 검사: {len(lines)}행 중 " + ("이상 없음" if bad == 0 else f"{bad}행 어긋남"))
    return bad


# --- 서체 검사 --------------------------------------------------------------

def check_fonts(pdf_path: Path) -> int:
    """양식 서체가 PDF에 실제로 박혔는지 본다.

    @font-face 가 등록되지 않으면 WeasyPrint 는 아무 말 없이 다른 서체로 떨어진다.
    글자 크기도 줄 높이도 그대로라 눈으로는 잘 안 보인다. 그런데 서체마다 줄상자
    안에서 베이스라인이 놓이는 높이가 달라 그리드가 통째로 밀리고, 인라인 블록이
    섞인 리스트에서는 줄 높이까지 늘어난다. 조용히 틀리는 종류의 고장이라
    --check 를 안 걸어도 매번 확인한다.
    """
    try:
        import pdfplumber
    except ImportError:
        return 0

    used = set()
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages[:5]:          # 본문 서체는 앞쪽에서 다 드러난다
            used.update(c["fontname"].split("+")[-1] for c in page.chars)
            if any(FONT in f for f in used):
                return 0

    if not used:
        return 0                            # 글자가 없는 문서는 볼 것이 없다

    print(f"  ! 양식 서체({FONT})가 안 박혔다. 대신 쓰인 서체: {', '.join(sorted(used))}")
    print(f"    {HERE / 'fonts'} 안에 otf 세 개가 있는지 보라.")
    return 1


# --- 진입점 -----------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description="수리소 수학학원 문서 양식 렌더러")
    ap.add_argument("source", type=Path, help="입력 HTML")
    ap.add_argument("-o", "--output", type=Path, help="출력 PDF (기본: 같은 이름 .pdf)")
    ap.add_argument("--check", action="store_true", help="렌더 후 베이스라인 그리드 검사")
    ap.add_argument("--no-wrap", action="store_true", help="어절 nowrap 처리를 끈다")
    args = ap.parse_args()

    src = args.source.resolve()
    if not src.is_file():
        print(f"입력 파일이 없다: {src}", file=sys.stderr)
        return 1
    out = (args.output or src.with_suffix(".pdf")).resolve()

    weasyprint = import_weasyprint()

    if args.no_wrap:
        html_str, has_css = src.read_text(encoding="utf-8"), True
    else:
        html_str, has_css = prepare(src)

    # @font-face 는 스타일시트와 문서가 같은 FontConfiguration 을 봐야 등록된다.
    # CSS(...) 만 넘기고 이걸 빠뜨리면 base.css 의 서체 선언이 통째로 무시되어
    # 시스템 서체로 조용히 떨어진다. <link> 로 붙인 경우에는 WeasyPrint 가 스스로
    # 만들어 쓰므로 문제가 안 드러난다. 그래서 여기서 하나를 만들어 양쪽에 준다.
    from weasyprint.text.fonts import FontConfiguration
    font_config = FontConfiguration()

    sheets = [] if has_css else [weasyprint.CSS(filename=str(BASE_CSS), font_config=font_config)]
    doc = weasyprint.HTML(string=html_str, base_url=str(src)).render(
        stylesheets=sheets, font_config=font_config)
    doc.write_pdf(str(out))

    print(f"{out}  ({len(doc.pages)}쪽)")
    bad = check_fonts(out)
    if args.check:
        bad += check_grid(out)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
