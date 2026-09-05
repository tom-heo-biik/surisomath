"""수리소 수학학원 문서 양식 — 수식·그래프를 SVG로 뽑는다.

스펙대로 Computer Modern, 배율 1.0, 축 0.4pt / 곡선 1pt / 점선 0.4pt·2pt 등간격,
블록 높이는 22pt의 배수로 맞춘다. 글과 선은 neutral-1000, 격자만 neutral-500이다.
글자는 패스로 변환하므로 결과 SVG는 폰트 설치 없이 그대로 렌더된다.

    from figure import equation, graph

    equation(r"\\int_0^1 x^2\\,dx = \\frac{1}{3}", "figures/eq.svg", units=2)
    graph({"측정": (xs, ys)}, "figures/g.svg", units=8, xlabel="월", ylabel="건")

명령줄로 견본을 만들려면:

    python figure.py --samples

TikZ/pgfplots를 쓸 수 있는 환경이라면 같은 규격(높이 22의 배수, 축 0.4pt,
곡선 1pt)으로 SVG나 PDF를 뽑아 그대로 바꿔 끼우면 된다.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

GRID = 22.0          # 베이스라인 한 칸(pt)
CONTENT_W = 475.0    # 본문 영역 너비 595 - 60 - 60 (pt)
PT = 1 / 72          # pt → inch

RULE = 0.4           # 축 선 두께
CURVE = 1.0          # 그래프 선 두께
DASH = (0, (2, 2))   # 점선 2pt 등간격
INK = "#000000"      # neutral-1000 — 글·선
INK_AUX = "#636363"  # neutral-500 — 격자. 알파 틴트 대신 스펙의 회색을 그대로 쓴다

# Computer Modern에는 한글이 없다. 숫자·수식은 CM으로 두고 한글만 본문 활자로
# 떨어지도록 폴백을 건다(matplotlib 3.6+ 의 글리프 단위 폴백).
# 폴백은 font.family 를 리스트로 줘야 글리프 단위로 동작한다.
# font.serif 리스트로는 안 넘어간다.
_KO_FILE = Path(__file__).resolve().parent / "fonts" / "KoPubWorld-Batang-Light.otf"
_FAMILY = ["cmr10"]
if _KO_FILE.is_file():
    fm.fontManager.addfont(str(_KO_FILE))
    _FAMILY.append(fm.FontProperties(fname=str(_KO_FILE)).get_name())
_FAMILY.append("DejaVu Serif")

matplotlib.rcParams.update({
    "mathtext.fontset": "cm",             # Computer Modern
    "font.family": _FAMILY,
    "axes.formatter.use_mathtext": True,  # cmr10의 마이너스 기호 경고 회피
    "svg.fonttype": "path",               # 글자를 패스로 — 폰트 의존 없음
    "axes.unicode_minus": False,
})


def _figure(units: int, width_pt: float):
    """높이가 정확히 units × 22pt인 빈 figure를 만든다."""
    if units < 1:
        raise ValueError("units는 1 이상이어야 한다")
    fig = plt.figure(figsize=(width_pt * PT, units * GRID * PT))
    fig.patch.set_alpha(0)
    return fig


def equation(tex: str, out: str, units: int = 2, size: float = 12.0,
             width_pt: float = CONTENT_W) -> str:
    """LaTeX 수식을 별행 블록으로 렌더한다. 수식 안에서 줄은 바꾸지 않는다."""
    fig = _figure(units, width_pt)
    fig.text(0.5, 0.5, f"${tex}$", ha="center", va="center",
             fontsize=size, color=INK)
    fig.savefig(out, format="svg", transparent=True)
    plt.close(fig)
    return out


def graph(series: dict, out: str, units: int = 8, size: float = 12.0,
          width_pt: float = CONTENT_W, xlabel: str = "", ylabel: str = "",
          grid: bool = True) -> str:
    """series = {이름: (x들, y들)}. 첫 계열은 실선, 이후는 점선."""
    fig = _figure(units, width_pt)
    ax = fig.add_axes((0.10, 0.18, 0.86, 0.76))

    for i, (name, (xs, ys)) in enumerate(series.items()):
        ax.plot(xs, ys, label=name, color=INK,
                linewidth=CURVE if i == 0 else RULE,
                linestyle="-" if i == 0 else DASH)

    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_linewidth(RULE)
        ax.spines[side].set_color(INK)

    ax.tick_params(width=RULE, length=2, labelsize=size, colors=INK)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=size, color=INK)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=size, color=INK)
    if grid:
        ax.grid(True, axis="y", linewidth=RULE, linestyle=DASH, color=INK_AUX)
        ax.set_axisbelow(True)
    if len(series) > 1:
        ax.legend(fontsize=size, frameon=False, labelcolor=INK)

    fig.savefig(out, format="svg", transparent=True)
    plt.close(fig)
    return out


if __name__ == "__main__":
    import sys
    from pathlib import Path

    if "--samples" not in sys.argv:
        print(__doc__)
        sys.exit(0)

    here = Path(__file__).resolve().parent / "figures"
    here.mkdir(exist_ok=True)

    equation(r"\sum_{k=1}^{n} k^2 = \frac{n(n+1)(2n+1)}{6}",
             str(here / "equation-sample.svg"), units=3)

    xs = list(range(1, 13))
    graph({"올해": (xs, [12, 18, 15, 24, 31, 28, 35, 41, 38, 44, 47, 52]),
           "지난해": (xs, [9, 11, 14, 16, 21, 19, 24, 27, 26, 30, 33, 35])},
          str(here / "graph-sample.svg"), units=8, xlabel="월", ylabel="건")

    for f in sorted(here.glob("*.svg")):
        print(f"{f.name}  {f.stat().st_size:,} bytes")
