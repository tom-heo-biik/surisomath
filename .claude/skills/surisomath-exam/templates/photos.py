# -*- coding: utf-8 -*-
"""원문 사진 정리 — 이름 바꾸기와 읽기용 축소본.

    python photos.py 단원폴더                # 사진을 수리소_시험대비_…_001.jpg 꼴로 바꾸고 축소본을 뽑는다
    python photos.py 단원폴더 --small DIR    # 축소본을 DIR에 (기본은 임시 폴더)

선생님이 카카오톡으로 보낸 사진(KakaoTalk_….jpg)은 한 장이 문제 하나다. 파일 이름 차례가
문제 번호다(KakaoTalk_…969.jpg, _01.jpg, _02.jpg …). 이 스크립트가
  1. 단원 폴더에 있는 아직 정리 안 된 *.jpg를 이름순으로 번호에 붙인다(git mv).
     옛 꼴(problems.yaml이 있는 단원)은 <학습지 이름>_001.jpg, _002.jpg …로 바꾼다.
     새 꼴(문제마다 폴더, problems.yaml이 없는 단원)은 문제 폴더 001/, 002/ …를 만들고 그 안의
     photo.jpg로 옮긴다. 번호는 이미 있는 문제 폴더 다음부터다.
     이미 정리된 사진은 건드리지 않는다.
  2. 사진마다 긴 변 1400px, 품질 80의 축소본(001.jpg …)을 만든다. 원본은 600KB~1MB라 그대로 읽으면 무겁다.
이름 짓기·번호 매기기·축소는 결정론적인 일이라 사람이 하지 않는다. 사진을 읽어 지문을 옮기는
일만 사람(모델)이 한다.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from build import meta  # noqa: E402  폴더 이름에서 학습지 이름을 만든다

LONG = 1400
QUALITY = 80


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="원문 사진 이름 바꾸기와 축소본")
    ap.add_argument("folder", type=Path, help="build/시험대비/<시험>/<학년>/<단원>/")
    ap.add_argument("--small", type=Path, metavar="DIR", help="축소본 폴더. 기본은 임시 폴더")
    args = ap.parse_args()

    folder = args.folder.resolve()
    if not folder.is_dir():
        raise SystemExit(f"폴더가 없다: {folder}")
    # 시험기출처럼 폴더 이름으로 학습지 이름을 못 만드는 곳은 problems.yaml의 머리(series·exam·school·
    # grade·file)를 먼저 적어 두면 그것으로 짓는다
    src = folder / "problems.yaml"
    head = {}
    if src.is_file():
        import yaml
        head = {k: v for k, v in (yaml.safe_load(src.read_text(encoding="utf-8")) or {}).items()
                if k != "problems"}
    folders = not src.is_file()               # problems.yaml이 없으면 새 꼴(문제마다 폴더)
    if folders and (folder / "unit.yaml").is_file():
        import yaml
        head = yaml.safe_load((folder / "unit.yaml").read_text(encoding="utf-8")) or {}
    stem = meta(head, folder)["file"]
    from PIL import Image

    def move(p: Path, new: Path) -> None:
        if new.exists():
            raise SystemExit(f"이미 있다: {new.relative_to(folder)}")
        new.parent.mkdir(exist_ok=True)
        r = subprocess.run(["git", "mv", str(p), str(new)], cwd=str(folder), capture_output=True)
        if r.returncode:                      # git이 모르는 파일이면 그냥 옮긴다
            p.rename(new)
        print(f"  {p.name} → {new.relative_to(folder).as_posix()}")

    photos = sorted(p for p in folder.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png"))
    if folders:
        nums = [int(d.name) for d in folder.iterdir() if d.is_dir() and d.name.isdigit() and len(d.name) == 3]
        n = max(nums, default=0)
        for p in photos:                      # 단원 폴더 바로 아래 사진은 모두 아직 정리 안 된 것이다
            n += 1
            move(p, folder / f"{n:03d}" / f"photo{p.suffix.lower()}")
        photos = sorted(f for d in folder.iterdir() if d.is_dir() and d.name.isdigit() and len(d.name) == 3
                        for f in d.glob("photo.*"))
        label = lambda p: p.parent.name       # noqa: E731  축소본 이름은 문제 번호
    else:
        done = [p for p in photos if p.stem.startswith(stem + "_")]
        n = len(done)
        for p in photos:
            if p in done:
                continue
            n += 1
            move(p, folder / f"{stem}_{n:03d}{p.suffix.lower()}")
        photos = sorted(p for p in folder.iterdir() if p.stem.startswith(stem + "_"))
        label = lambda p: p.stem[len(stem) + 1:]   # noqa: E731

    small = args.small or Path(tempfile.gettempdir()) / "surisomath_photos" / stem
    small.mkdir(parents=True, exist_ok=True)
    for p in photos:
        im = Image.open(p)
        w, h = im.size
        s = LONG / max(w, h)
        if s < 1:
            im = im.resize((round(w * s), round(h * s)), Image.LANCZOS)
        im.convert("RGB").save(small / (label(p) + ".jpg"), quality=QUALITY)
    print(f"  사진 {len(photos)}장. 축소본: {small}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
