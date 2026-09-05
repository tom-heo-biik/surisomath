---
name: surisomath-a4
description: "수리소 수학학원의 표준 문서 양식이 작성되어 있는 SKILL입니다. 사용자가 문서 작업을 요청하는 상황에 사용합니다. 인쇄해서 보는 종이 문서입니다. 여백이 많이 남아도 좋으니, 섹션 중간에 페이지가 끊기지 않도록 작업해 주세요."
---

# 수리소 수학학원 문서 양식


## 환경
포맷: PDF


## 판형
paper: A4 세로(210×297mm)
unit: pt(A4 = 595×842)


## 여백
margin-top: 72pt
margin-side: 60pt
margin-bottom: 88pt


## 베이스라인 그리드
여백 방향: 아래
단위: 22pt
반 칸: 11pt
문단 간격: 22pt
섹션 위 간격: 33pt
섹션 아래 간격: 11pt


## 타이포그래피
font: KoPubWorld 바탕체
body-leading: 22pt
typo-4(제목): 20pt/700/-0.05em
typo-3(섹션): 16pt/500/-0.04em
typo-2(소제목): 12pt/500/-0.03em
typo-1(본문): 12pt/300/-0.03em
typo-0(캡션): 10pt/300/-0.02em + 10pt/500/-0.02em


## 미시 타이포그래피
문서 제목 정렬: 왼쪽정렬 or 가운데정렬
그 외 정렬 방식: 왼끝맞추기
줄 바꿈 규칙: 어절 단위 줄 바꿈(keep-all)
줄 바꿈 규칙 주의할 점: WeasyPrint는 keep-all 속성을 지원하지 않음. 어절 전부에 nowrap을 걸어야 함
외톨이줄 제어: 최소 한 섹션 유지(오펀·위도우 금지)
숫자 세트: 고정폭 숫자, 미지원 시 오른쪽 정렬
라틴 혼용: 안 함
따옴표 모양: 둥근 따옴표
순서 표기: 1. → 가. → 1) → 가) → (1) → (가) → ① → ㉮
날짜 표기: YYYY. M. D.
시각 표기: HH:mm
통화 표기: 000,000원
단위 붙여쓰기: 숫자에 전부 붙임(10건, 3개월, 50%)
물결표(~): 앞뒤 모두 붙임


## 명도
neutral-500: 
#636363(L 0.500 · C 0.000)
neutral-1000: 
#000000(L 0.000 · C 0.000)


## 표
텍스트: typo-0
행 높이: 22pt
행 높이 주의할 점: 선 두께(0.4pt) 보정 필요
선: 가로만
선 두께: 0.4pt
배경: 없음
셀 패딩: 가로 16pt(첫 열 왼쪽·끝 열 오른쪽은 0)
간격: 표 위아래 22pt


## 리스트
항목 사이 간격: 0pt
블록 높이: 22pt
마커: • / ◦
마커 간격: 10pt(글머리표 왼끝에서 텍스트 왼끝까지)
레벨: 최대 2레벨
레벨 들여쓰기: 12pt(레벨이 내려갈 때 마커와 텍스트가 함께 이동)
구현: `li > ul { margin-left: -10pt; padding-left: 12pt; }`


## 쪽번호
형식: - n -
크기: typo-0
위치: 하단 중앙에서 44pt 위


## 수식
렌더링: LaTeX
폰트: Computer Modern
크기: 본문 배율 1.0
구현: `figsize = (475/72, units*22/72)`
줄 바꿈: 수식 안에서 안 함
블록 높이: 22의 배수 pt(별행)


## 그래프
렌더링: LaTeX(TikZ/pgfplots)
폰트: Computer Modern
배율: 1.0
구현: `.math > * { width: auto; height: auto; max-width: 100%; max-height: 100%; }`
축 선 두께: 0.4pt
그래프 선 두께: 1pt
점선 두께: 0.4pt
점선 등간격: 2pt
블록 높이: 22의 배수 pt


## 파일
templates/base.html: 복사해서 쓰는 빈 뼈대
templates/base.css: 위 규격을 그대로 구현한 스타일시트
templates/sample.html: 모든 요소가 한 번씩 들어간 견본
templates/render.py: HTML을 PDF로 렌더
templates/figure.py: 수식·그래프를 Computer Modern SVG로 출력
templates/fonts/: KoPubWorld 바탕체 Light·Medium·Bold


## 작업 순서
1. templates/base.html을 복사해 내용을 채운다
2. 섹션은 반드시 `<section>`으로 감싼다. 쪽이 중간에서 끊기지 않는 단위가 이것이다
3. `python templates/render.py 문서.html --check`
4. --check가 "이상 없음"이면 모든 글줄이 22pt 그리드 위에 있다
5. 양식 서체가 안 박히면 --check 없이도 경고가 뜬다. 뜨면 그리드도 같이 깨져 있다


## 쓰는 법
어절 줄 바꿈: render.py가 어절마다 nowrap을 건다. HTML에 따로 쓰지 않는다
수식·그래프: `<div class="math" style="--u:3">` — 높이를 22pt의 몇 칸으로 줄지 정한다
순서 표기: `<ol class="n1">`~`<ol class="n8">`이 1. 가. 1) 가) (1) (가) ① ㉮ 순서다
숫자 열 오른쪽 정렬: `<td class="num">`


## 참고
pip install weasyprint --break-system-packages
Windows는 GTK 런타임이 따로 필요하다: winget install tschoonj.GTKForWindows
https://cdn.jsdelivr.net/npm/font-kopubworld@1.0.3/fonts/KoPubWorld-Batang-Light.otf
https://cdn.jsdelivr.net/npm/font-kopubworld@1.0.3/fonts/KoPubWorld-Batang-Medium.otf
https://cdn.jsdelivr.net/npm/font-kopubworld@1.0.3/fonts/KoPubWorld-Batang-Bold.otf
