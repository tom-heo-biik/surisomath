# 서체

인쇄물 빌드 스크립트가 쓰는 서체. 배포가 전제라 저장소에 담아 둔다.
경로는 `lib/suriso.py`에서 가져다 쓴다. 절대 경로를 코드에 박지 않는다.

KoPubWorld 바탕체는 여기 없다. `skills/surisomath-a4/templates/fonts/`에 산다.
그 스킬 명세가 서체를 자기 파일 목록으로 잡고 있어서, 사본을 하나 더 두지 않고
그쪽을 정본으로 본다.

## 담은 것

| 서체 | 무게 | 쓰임 |
|---|---|---|
| Pretendard | 300·400·500·600·700 | 화면용 산세리프 |
| 학교안심 상장 R | 단일 | 상장 |

## 라이선스

둘 다 SIL Open Font License 1.1이다. 자유롭게 쓰고 함께 배포할 수 있다.
서체 파일 자체를 파는 것만 금지된다. 배포할 때 약관을 같이 담아야 해서
아래 두 파일을 함께 둔다.

- `Pretendard-LICENSE.txt` — © 2021 Kil Hyung-jin
- `HakgyoansimSangjang-LICENSE.txt` — © 2025 KERIS, 교육저작권지원센터 배포

## 없는 것

Jura·Geist Mono·IBM Plex Mono는 담지 않았다. 문제집 표지 **시안** 스크립트
(`build_covers.py`)만 쓰고, 채택된 최종본(`build_final.py`)은 KoPubWorld 바탕체
하나로 돈다. 원본 파일도 이미 사라졌다 — 클로드 세션 임시 폴더에 있었다.

Malgun Gothic은 담을 수 없다. 마이크로소프트 독점이라 재배포가 안 된다.
`build_final.py`가 상수로 잡아 두긴 했으나 실제로 부르지는 않는다.
