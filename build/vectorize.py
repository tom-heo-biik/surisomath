# -*- coding: utf-8 -*-
"""저해상도 2도(二度) 로고 비트맵을 SVG 패스로 바꾼다.

고려대 엠블럼은 595px GIF, 수리소 워드마크는 691px PNG뿐이다. 60×180cm 배너에서
엠블럼은 210mm로 앉으므로 그대로 키우면 72DPI밖에 안 나온다. 계단이 보인다.

비트맵을 4배로 늘려 안티에일리어싱의 0.5 등고선을 따면, 원본이 이미 가지고 있던
가장자리 정보가 그대로 살아나 부분 픽셀 정밀도의 윤곽이 나온다. 없는 해상도를
지어내는 것이 아니라 이미 있는 것을 꺼내 쓰는 것이라, 확대해도 깨지지 않는다.

짝홀 채우기(even-odd)를 쓰므로 구멍을 따로 가려낼 필요가 없다. 흰 방패 안의 붉은
호랑이도, 그 호랑이 안의 흰 줄무늬도 겹침 횟수의 홀짝으로 저절로 풀린다.
"""
from __future__ import annotations

import cv2
import numpy as np


def _mask(path: str, source: str = "auto") -> np.ndarray:
    """로고에서 '찍히는 부분'을 0~255 회색 마스크로 꺼낸다.

    어느 채널을 읽느냐가 결과를 가른다. 고려대 GIF의 알파는 0 아니면 255뿐이라
    그것을 따면 계단이 그대로 남는다. 같은 파일의 RGB에는 크림슨과 흰색을 섞은
    중간색이 남아 있어서, 그쪽을 읽어야 부분 픽셀 정밀도가 나온다.

    source='alpha'  알파 채널 (수리소 워드마크: 안티에일리어싱된 검정 글자)
    source='light'  밝기 (고려대 역상: 크림슨 바탕 위의 흰 표시)
    """
    from PIL import Image

    im = Image.open(path)
    a = np.array(im.convert("RGBA"))
    if source == "auto":
        # 알파가 이진값이면 가장자리 정보가 없다는 뜻이다. 밝기 쪽으로 넘긴다
        edge = ((a[:, :, 3] > 5) & (a[:, :, 3] < 250)).mean()
        source = "alpha" if edge > 0.001 else "light"
    if source == "alpha":
        return a[:, :, 3]
    # #7C001A와 #FFFFFF는 초록 채널만으로 0 대 255까지 완전히 벌어진다
    return a[:, :, 1]


def trace(
    path: str,
    upscale: int = 6,
    epsilon: float = 1.2,
    smooth: float = 0.8,
    source: str = "auto",
    trim: int = 0,
) -> tuple[str, tuple[int, int, int, int]]:
    """SVG 패스 데이터와 내용물의 경계 상자(x, y, w, h)를 원본 픽셀 단위로 돌려준다.

    trim은 가장자리에서 지울 픽셀 수다. 고려대 GIF는 화면 네 변이 1~2픽셀 밝게
    번져 있어서 그대로 두면 사각 테두리가 딸려 나온다. 로고가 아니라 저장 흔적이다.
    """
    m = _mask(path, source)
    if trim:
        m = m.copy()
        m[:trim, :] = m[-trim:, :] = 0
        m[:, :trim] = m[:, -trim:] = 0
    h, w = m.shape

    big = cv2.resize(m, (w * upscale, h * upscale), interpolation=cv2.INTER_CUBIC)
    if smooth:
        # 원본 1픽셀보다 좁게 흐린다. 계단의 떨림만 눌리고 획은 안 먹힌다
        big = cv2.GaussianBlur(big, (0, 0), smooth * upscale)
    _, binary = cv2.threshold(big, 127, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    parts, xs, ys = [], [], []
    for c in contours:
        c = cv2.approxPolyDP(c, epsilon, True)
        if len(c) < 3 or abs(cv2.contourArea(c)) < upscale * upscale:
            continue  # 원본 1픽셀보다 작은 티끌은 버린다
        pts = c.reshape(-1, 2) / upscale
        xs.append(pts[:, 0])
        ys.append(pts[:, 1])
        d = "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in pts) + " Z"
        parts.append(d)

    if not parts:
        raise ValueError(f"윤곽을 하나도 못 찾았습니다: {path}")

    xs, ys = np.concatenate(xs), np.concatenate(ys)
    x0, y0 = int(np.floor(xs.min())), int(np.floor(ys.min()))
    x1, y1 = int(np.ceil(xs.max())), int(np.ceil(ys.max()))
    return " ".join(parts), (x0, y0, x1 - x0, y1 - y0)


def svg(path: str, fill: str = "#FFFFFF", **kw) -> str:
    """내용물에 딱 맞게 잘라 낸 독립 SVG 문자열. viewBox 원점이 내용물 왼쪽 위다."""
    d, (x, y, w, h) = trace(path, **kw)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {w} {h}">'
        f'<path fill="{fill}" fill-rule="evenodd" d="{d}"/></svg>'
    )


if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
    import suriso  # noqa: E402

    targets = {
        "ku_emblem": (suriso.ASSETS / "고려대학교" / "crimson1negative.gif", {"trim": 2}),
        "wordmark_kr": (suriso.WORDMARK_KR, {}),
        "wordmark_full": (suriso.WORDMARK_FULL, {}),
    }
    out = Path(__file__).resolve().parent / "_trace"
    out.mkdir(exist_ok=True)
    for name, (src, kw) in targets.items():
        d, box = trace(str(src), **kw)
        print(f"{name:14s} 경계 {box}  패스 {len(d):,}자  조각 {d.count('M'):,}개")
        (out / f"{name}.svg").write_text(svg(str(src), fill="#000000", **kw), encoding="utf-8")
