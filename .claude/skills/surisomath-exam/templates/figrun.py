# -*- coding: utf-8 -*-
"""새 꼴(문제마다 폴더) 단원의 그림을 한 프로세스에서 차례로 그린다. build.py가 부른다.

    python figrun.py 단원폴더/001/figure.py 단원폴더/002/figure.py …

문제마다 파이썬을 새로 띄우면 matplotlib을 부르는 데만 한 번에 1~2초라 100문제면 몇 분이다. 그래서 한
프로세스에서 figure.py를 __main__으로 차례로 돌린다. figure.py는 옛 figures.py와 같은 뼈대다
(import grind_figure as g → g.setup(__file__) → 그림 함수 → if __name__ == "__main__":). 작업 폴더는
그 문제 폴더다. 단원 폴더를 import 경로에 넣으므로 여러 문제가 같이 쓰는 도우미는 단원/figlib.py에 두고
figure.py에서 import figlib로 부른다. 한 문제의 figure.py가 터지면 그 번호를 알리고 종료 코드 1로 멈춘다.
"""
from __future__ import annotations

import runpy
import sys
import traceback
from pathlib import Path


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    import os

    import grind_figure as g
    import matplotlib.pyplot as plt
    print("figures/")
    for arg in argv[1:]:
        fp = Path(arg).resolve()
        unit = str(fp.parent.parent)
        if unit not in sys.path:
            sys.path.insert(0, unit)
        # 한 프로세스라 앞 문제의 출력 폴더와 기본 이름이 남는다. setup을 빠뜨린 figure.py가 남의 그림을
        # 덮지 않게 되돌리고, 상대 경로가 그 문제 폴더를 가리키게 작업 폴더를 옮긴다
        g.OUT = g.DEFAULT_NAME = None
        os.chdir(fp.parent)
        try:
            runpy.run_path(str(fp), run_name="__main__")
        except SystemExit as e:
            if e.code not in (None, 0):
                print(f"  ! {fp.parent.name}/figure.py가 멈췄다({e.code})")
                return 1
        except Exception:
            traceback.print_exc()
            print(f"  ! {fp.parent.name}/figure.py에서 오류가 났다. 위의 역추적을 보라")
            return 1
        finally:
            plt.close("all")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
