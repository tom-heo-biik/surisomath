# -*- coding: utf-8 -*-
"""원문 사진 정리 — 이름 바꾸기와 읽기용 축소본.

    python photos.py 단원폴더                # 사진을 수리소_시험대비_…_001.jpg 꼴로 바꾸고 축소본을 뽑는다
    python photos.py 단원폴더 --small DIR    # 축소본을 DIR에 (기본은 임시 폴더)

선생님이 카카오톡으로 보낸 사진(KakaoTalk_….jpg)은 한 장이 문제 하나다. 파일 이름 차례가
문제 번호다(KakaoTalk_…969.jpg, _01.jpg, _02.jpg …). 이 스크립트가
  1. 아직 양식 이름이 아닌 *.jpg를 이름순으로 <학습지 이름>_001.jpg, _002.jpg …로 바꾼다(git mv).
     이미 양식 이름인 사진은 건드리지 않는다.
  2. 사진마다 긴 변 1400px, 품질 80의 축소본을 만든다. 원본은 600KB~1MB라 그대로 읽으면 무겁다.
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
    stem = meta({}, folder)["file"]
    from PIL import Image

    photos = sorted(p for p in folder.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png"))
    done = [p for p in photos if p.stem.startswith(stem + "_")]
    todo = [p for p in photos if p not in done]
    n = len(done)
    for p in todo:
        n += 1
        new = folder / f"{stem}_{n:03d}{p.suffix.lower()}"
        if new.exists():
            raise SystemExit(f"이미 있다: {new.name}")
        r = subprocess.run(["git", "mv", str(p), str(new)], cwd=str(folder), capture_output=True)
        if r.returncode:                      # git이 모르는 파일이면 그냥 옮긴다
            p.rename(new)
        print(f"  {p.name} → {new.name}")
    photos = sorted(p for p in folder.iterdir() if p.stem.startswith(stem + "_"))

    small = args.small or Path(tempfile.gettempdir()) / "surisomath_photos" / stem
    small.mkdir(parents=True, exist_ok=True)
    for p in photos:
        im = Image.open(p)
        w, h = im.size
        s = LONG / max(w, h)
        if s < 1:
            im = im.resize((round(w * s), round(h * s)), Image.LANCZOS)
        im.convert("RGB").save(small / (p.stem[len(stem) + 1:] + ".jpg"), quality=QUALITY)
    print(f"  사진 {len(photos)}장. 축소본: {small}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
