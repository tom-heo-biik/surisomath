# -*- coding: utf-8 -*-
"""KoPubWorld 바탕체를 이 PC에 설치한다.

플러그인 안의 스킬은 templates/fonts/ 를 직접 읽으므로 설치 없이도 돌아간다.
이 스크립트는 그 바깥, 곧 한글·워드·파워포인트처럼 OS에 깔린 서체만 쓰는
프로그램에서도 같은 서체를 쓰려고 할 때만 필요하다.

    python lib/install_fonts.py            → 설치
    python lib/install_fonts.py --check    → 설치 여부만 본다

관리자 권한이 필요 없다. 사용자 계정 안에만 깐다.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

FONTS = Path(__file__).resolve().parent.parent / "skills" / "surisomath-a4" / "templates" / "fonts"

# 파일 이름 → (서체 안에 박힌 이름, 무게 키워드).
# 이름은 윈도우 레지스트리 등록에, 무게 키워드는 이미 깔렸는지 볼 때 쓴다.
FACES = {
    "KoPubWorld-Batang-Light.otf": ("KoPubWorldBatang_Pro Light", "light"),
    "KoPubWorld-Batang-Medium.otf": ("KoPubWorldBatang_Pro Medium", "medium"),
    "KoPubWorld-Batang-Bold.otf": ("KoPubWorldBatang_Pro Bold", "bold"),
}

FAMILY = "kopubworldbatang"


def _norm(s: str) -> str:
    """공백·하이픈·밑줄을 지우고 소문자로. 배포처마다 파일 이름이 달라서 필요하다."""
    return re.sub(r"[\s_\-]+", "", s).lower()


def target_dir() -> Path:
    """이 운영체제의 사용자 서체 폴더."""
    if sys.platform == "win32":
        import os

        return Path(os.environ["LOCALAPPDATA"]) / "Microsoft" / "Windows" / "Fonts"
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Fonts"
    return Path.home() / ".local" / "share" / "fonts"


def _registered_files() -> list[str]:
    """윈도우 레지스트리에 올라 있는 서체 파일 이름."""
    import winreg

    key = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"
    out = []
    for hive in (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE):
        try:
            with winreg.OpenKey(hive, key) as k:
                for i in range(winreg.QueryInfoKey(k)[1]):
                    _, data, _ = winreg.EnumValue(k, i)
                    if isinstance(data, str):
                        out.append(Path(data).name)
        except OSError:
            continue
    return out


def installed() -> set[str]:
    """이미 깔려 있는 서체의 파일 이름 집합(우리 이름 기준).

    같은 서체라도 배포처마다 파일 이름이 다르다. 실제로 이 PC에는 벤더 설치본이
    'KoPubWorld Batang_Pro Medium.otf' 라는 이름에 'KoPubWorld바탕체_Pro' 라는
    한글 이름으로 올라가 있다. 우리 파일 이름만 찾으면 못 보고 한 벌 더 깔게 된다.
    그래서 이름을 눌러 편 뒤 계열과 무게로 맞춘다.
    """
    names = [p.name for p in target_dir().glob("*") if p.is_file()]
    if sys.platform == "win32":
        names += _registered_files()

    flat = [_norm(n) for n in names]
    return {
        name
        for name, (_, weight) in FACES.items()
        if any(FAMILY in f and weight in f for f in flat)
    }


def _register_windows(path: Path, face: str) -> None:
    """레지스트리에 올리고 지금 켜져 있는 프로그램에도 알린다.

    복사만 해서는 다시 로그인하기 전까지 목록에 안 뜬다. 레지스트리 등록이
    다음 부팅까지 살리고, AddFontResource + WM_FONTCHANGE 가 지금 세션에 알린다.
    """
    import ctypes
    import winreg

    key = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_SET_VALUE) as k:
        winreg.SetValueEx(k, f"{face} (OpenType)", 0, winreg.REG_SZ, str(path))

    ctypes.windll.gdi32.AddFontResourceW(str(path))
    ctypes.windll.user32.SendMessageTimeoutW(
        0xFFFF,  # HWND_BROADCAST
        0x001D,  # WM_FONTCHANGE
        0, 0,
        0x0002,  # SMTO_ABORTIFHUNG
        1000,
        None,
    )


def main() -> int:
    check_only = "--check" in sys.argv
    dst = target_dir()

    missing = [n for n in FACES if not (FONTS / n).exists()]
    if missing:
        print(f"플러그인 안에 서체가 없다: {', '.join(missing)}", file=sys.stderr)
        print(f"  찾은 곳: {FONTS}", file=sys.stderr)
        return 1

    done = installed()

    if check_only:
        for name, (face, _) in FACES.items():
            print(f"  {'설치됨' if name in done else '미설치'}  {face}")
        return 0 if len(done) == len(FACES) else 1

    for name, (face, _) in FACES.items():
        if name in done:
            print(f"  건너뜀  {face} (이미 있음)")
            continue
        dst.mkdir(parents=True, exist_ok=True)
        out = dst / name
        shutil.copy2(FONTS / name, out)
        if sys.platform == "win32":
            _register_windows(out, face)
        print(f"  설치됨  {face}")

    if sys.platform not in ("win32", "darwin") and len(done) < len(FACES):
        if shutil.which("fc-cache"):
            subprocess.run(["fc-cache", "-f", str(dst)], check=False)
        else:
            print("  fc-cache 가 없다. 서체 목록 갱신은 직접 해야 한다.")

    print(f"\n{dst}")
    print("워드·한글·파워포인트에서 서체 이름은 'KoPubWorld바탕체_Pro' 로 뜬다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
