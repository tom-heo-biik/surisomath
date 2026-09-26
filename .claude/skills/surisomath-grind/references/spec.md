# 연마 규격


## 환경
포맷: PDF
선행 스킬: surisomath-a4(판형, 여백, 그리드, 서체, 렌더, 그리드 검사), surisomath-munhang(문제 글의 문형과 표기)
패키지: pyyaml, weasyprint, pdfplumber, matplotlib, pymupdf
렌더: matplotlib(그림과 수식), WeasyPrint(PDF). a4의 render.py를 build.py가 부른다


## 쪽
단위: 문제 한 개 = 한 쪽(`<section class="problem">`)
본문 영역: 475×682pt(31칸). 세로 플렉스. 위에서부터 채우고 남은 높이를 풀이 자리가 가진다
표지, 이름 칸, 단원명: 없음. 단원명은 문서 제목(`<title>`)과 파일 이름에만
쪽번호: a4 그대로(- n -). 선생님 쪽까지 이어 센다
선생님 쪽: 학생 쪽 뒤에 같은 차례로. 문제 셋이면 4~6쪽. solution이 있는 문제만


## 쪽의 세로 짜임
기준: 본문 영역 위 끝 = 0
0~11pt: 빈 반 칸
11~33pt: 시리즈 이름(왼쪽)과 정답(오른쪽 끝, 선생님 쪽에만). typo-0. 본문 위상(11 + 22k)
33~44pt: 빈 반 칸
44~66pt: 문제 번호. typo-4. 제목 위상(22k)
66~77pt: 번호 아래 반 칸
77pt~: 문제 글. typo-1. 문단 아래 22pt
그 아래: 그림(있으면). units × 22pt. 아래 22pt
그 아래: 소제목 줄 한 칸(22pt). 선 없음
그 아래~682pt: 두 단 풀이 자리. 세로선
위상 산식: 11 + 22 + 11 + 22 + 11 = 77
풀이 자리 최소: 12칸. build.py가 가장 좁은 쪽을 재서 알려 준다
풀이 자리 칸 수: 위의 반 칸 때문에 늘 .5로 끝난다
풀이 자리가 주는 것: 문제 글 한 줄에 한 칸, 그림 units 한 칸에 한 칸


## 첫 줄
시리즈 이름: 연마(硏磨). typo-0(10pt/300/-0.02em). neutral-1000
정답: `정답: 5바퀴`. typo-0. neutral-500. 오른쪽 끝맞추기. 선생님 쪽에만
정답 표기: 단위까지 붙임(114.24cm, 둘레 37.68cm, 넓이 56.52cm²)
정답 길이: 한 줄. 400pt 안쪽. 넘으면 두 줄이 되어 번호와 겹치고 경고도 없다
정답 수식: `$…$`. 10pt 회색(#636363)


## 문제 번호
형식: 001, 002, … 세 자리. 단원마다 001부터
서체: typo-4(20pt/700/-0.05em). 왼끝맞추기


## 문제 글과 그림 블록
문제 글: typo-1. 한 문단. 어절 줄 바꿈은 render.py
그림 자리: 문제 글 아래 가운데. a4의 `.figure` 블록(`div.figure[style="--u:n"]`)
그림 블록 높이: units × 22pt. 캔버스 높이가 곧 블록 높이. yaml의 units와 SVG 높이가 다르면 build.py가 멈춘다
units: 5~7칸. 도형 하나면 5, 치수가 바깥에 붙거나 도형이 두 줄이면 6~7
그림 너비: 475pt 안. 넘으면 save가 경고


## 두 단 풀이 자리
소제목: 왼쪽 "원석 풀이", 오른쪽 "보석 풀이". typo-2(h3)
선생님 쪽 소제목: 왼쪽 "선생님 풀이", 오른쪽 "메모"
심볼: templates/symbol.svg. 높이 22pt(한 칸), 너비 25.42pt. 소제목 앞
심볼 간격: 선에서 4pt, 글은 심볼에서 4pt
소제목 줄: 선 없음. 선은 그 아래 칸부터 바닥(682pt)까지
세로선: 세 개. 본문 영역 기준 x = 0, 237, 475pt(쪽 기준 60, 297, 535). neutral-1000. 0.4pt
단 너비: 237pt + 238pt. 반반(237.5)이면 가운데 선이 픽셀 경계에 걸쳐 화면에서 회색으로 보인다
글 자리: 선에서 8pt 안쪽. 왼 단 글 너비 221pt(한글 18자쯤)
가로선: 없음. a4 규격(선은 가로만)의 연마 예외가 세로선
풀이 글: typo-1. 줄마다 한 칸(문단 간격 없음). 빈 줄은 한 칸(p.gap)


## 그림 선과 표시
도형 선: 0.7pt(g.EDGE). 도형 안을 가르는 선(지름, 길의 가장자리, 안쪽 호)도 같다
끈과 경로: 1pt(g.STRING). 원 둘레에서 반지름의 6~8% 띄운다
보조선: 0.4pt 실선(g.AUX). 높이, 반지름, 지시선, 직각 표시, 각의 호
점선: 0.4pt. 대시 2pt를 주지만 matplotlib이 선 두께를 곱해 0.8pt 등간격으로 찍힌다. 길이 표시(dim)와 수선(g.dashed)
점선 도형: 0.7pt. 대시 2pt 간격 2pt(g.poly와 g.seg의 dashed=True)
일점쇄선: 0.4pt. 긴 획 6pt, 빈 2pt, 점 1pt, 빈 2pt. 회전축(g.axis)
점: 지름 2.4pt 채운 원(g.dot)
직각 표시: 0.4pt. 한 변 5.5pt(g.MARK)
색칠: 잉크 10% 틴트(alpha 0.10). 테두리 없음
글자: 10pt(g.LABEL). 잉크. 보통 글자는 정체(cmr10), `$x$`는 이탤릭. 한글은 KoPub 폴백. 패스로 변환
잉크 여백: 잉크에서 캔버스 가장자리까지 4pt(g.MARGIN). 위아래가 4pt 아래면 잘리고 22pt(g.SLACK) 넘게 남으면 그림이 블록에 비해 작다
길이 글 양옆: 점선을 2pt 비운다(g.PAD)
길이 글 한도: 현의 8할. 넘으면 dim이 경고
길이 표시 부풀기: gap. 좌표 단위. 생략하면 가로 곡선 10pt쯤, 세로 곡선 글 너비 절반 + 6pt
길이 표시 물림: trim. pt. trim=3이면 양끝 3pt
지시선: 0.4pt. 길이 22pt(g.LEADER). 기본 방향 (3, 2) 오른쪽 위. 글은 선 끝에서 3pt
각 표시: 호 0.4pt. 반지름 r 기본 12pt. 글은 호에서 3pt(pad). p→q 반시계가 우각이면 경고
같은 각 표시: 이등분선 위 r pt에 점(지름 2.2pt) 또는 ×(3pt 획 둘)
같은 길이 표시: 선분 한가운데 직각 획 5pt(g.TICK) n개. 획 사이 2pt
겹침 검사(_check_labels): 글자 상자를 안쪽으로 1.5pt(LABEL_TOL) 줄인 뒤 선(Line2D), 테두리 있는 패치(원, 호), 다른 글자와 겹치면 경고. 선은 0.5pt마다 표본점
색칠 경계 검사(_check_shades): 색칠 변마다 안쪽 다섯 점에서 0.8pt(SHADE_TOL) 안에 선이 없으면 경고. 3pt(SHADE_MIN)보다 짧은 변은 보지 않는다. gid="noedge"는 뺀다
점 이름 주석: SVG 끝 `<!-- names: … -->`. 대문자와 프라임과 숫자 첨자. 글자 첨자(Aₙ)는 수열 이름이라 뺀다
SVG 재현성: svg.hashsalt "surisomath", 생성 시각 없음. 같은 그림은 다시 빌드해도 바이트 단위로 같다


## 통계 그래프와 좌표평면
캔버스(통계): `g.canvas(units, 0, units*22)`로 1단위 = 1pt
모눈: 정사각 18pt(15pt면 계급 경계 숫자가 붙는다). neutral-500 실선 0.4pt
축: 0.4pt에 채운 화살촉(길이 6pt)
그래프 선: 1pt(a4 그래프 규격)
좌표평면 배율: 가로세로 같아야 한다. y 범위로 배율만 정한다
반비례 가지: 축 반길이 R을 b/R² ≈ 0.15가 되게(b=8이면 R=7)
견본: build/연마/2026.09.12/figures.py(arrow, tick_x 도우미 포함)


## 수식
렌더: matplotlib mathtext. Computer Modern. 글자는 패스
본문: 12pt 검정. 정답: 10pt 회색(#636363). 풀이: 12pt 검정
SVG 상자: 잉크에 0.5pt 여백(pad). (너비, 높이, 깊이)를 pt로 재서 img의 height와 vertical-align에 적는다
글줄 상자: KoPub 12pt, 행간 22pt. 베이스라인 위 14.4pt, 아래 7.6pt(ascent 1.05em, descent 0.49em에 반행간을 더한 값)
분수(\dfrac): 분자 기준선 0.46em 위, 분모 기준선 0.40em 아래(FRAC_NUM, FRAC_DEN). 가로줄 0.04em(FRAC_RULE, TeX 규격). 가로줄과 최소 3θ 띄움. 가로줄은 = 의 한가운데(축 높이)
분수 높이(12pt): b/x 위 13.8pt 아래 4.8pt, 20/100 위 13.3pt 아래 6.9pt, 가장 큰 b/y 22pt. 분자와 가로줄 2.3pt, 가로줄과 분모 2.4pt
쓰지 않는 규격: TeX 디스플레이(num1 0.677em, denom1 0.686em)는 25.8pt라 22pt 행간에서 잇단 줄이 3.8pt 겹친다. matplotlib 기본(가로줄에서 1pt씩)은 납작하다
\frac: 텍스트 스타일. 분자와 분모가 7할로 줄고 기준선은 0.394em과 0.345em(cmsy num2, denom2). 최소 띄움 θ
분수 뒤 여백: 0.12em(TeX nulldelimiterspace)
시험용 환경 변수: GRIND_FRAC="0.68,0.69"처럼 주면 다른 값을 시험한다
근호: 왼쪽 상자만 밑줄 두께 하나. 오른쪽 상자 없음(The TeXbook 부록 G 규칙 11). matplotlib 기본은 양옆 밑줄 두께의 두 배(12pt에서 2pt)
근호 넘침: 0.5pt
상자를 넘는 수식: build.py가 img에 음수 여백을 줘 글줄만 22pt로 지킨다. 잉크는 옆 줄과 겹칠 수 있다
수식 겹침 검사: render.py --boxes의 레이아웃 상자로 img.mi끼리 0.2pt 넘게 겹치면 경고
어절 묶기: 수식이 든 어절은 span.w로 한 덩어리. BIND_NOUNS(원, 점, 현, 선분, 변, 삼각형, 사각형, 각, 호, 중심, 직선, 지름, 반지름, 꼭짓점, 그래프 등)와 "(단,"은 뒤의 수식과 묶는다
수식 SVG 이름: m{번호}_{k}.svg(문제 글), a{번호}_{k}.svg(정답), s{번호}_{k}.svg(풀이). 빌드마다 다시 그리고 안 쓴 것은 지운다


## 파일 이름과 날짜
단원 폴더: build/연마/{YYYY.MM.DD}/
제목: `<title>`은 "{series} {unit}". 정본 폴더면 "연마(硏磨) 2026. 9. 12."(a4 날짜 표기)
파일 이름: 수리소_연마_{YYYY.MM.DD}. 날짜 폴더가 아니면 수리소_연마_{unit에서 공백 뺀 것}
PDF 날짜: SOURCE_DATE_EPOCH를 폴더 날짜 0시(UTC)로 고정. 날짜 폴더가 아니면 problems.yaml의 수정 시각
그림 SVG: figures/p*.svg(이름은 figures.py의 save가 정한다)
심볼: templates/symbol.svg를 figures/symbol.svg로 복사
빌드 결과: 수리소_연마_{YYYY.MM.DD}.html, .pdf. base.css와 grind.css는 저장소 안 상대 경로로 링크


## HTML 뼈대
쪽: `section.problem` 안에 `p.series`, `h2`(번호), `p.answer`, `p`(문제 글), `div.figure[style="--u:n"]`, `div.cols.head`, `div.cols`
소제목: `div.cols.head > div > h3`에 `img`(심볼)와 `span`(글)
풀이: `div.solution > p`. 빈 줄은 `p.gap`
수식: `img.mi`. style에 height, vertical-align, margin
어절: `span.w`(수식이 든 어절). 나머지 어절의 nowrap은 render.py가 건다


## 빌드
명령: `python .claude/skills/surisomath-grind/templates/build.py build/연마/{날짜}/problems.yaml`
--no-figures: figures.py를 실행하지 않는다
--no-check: 그리드 검사를 건너뛴다
하는 일: figures.py 실행 → symbol.svg 복사 → 수식 SVG → HTML → render.py(PDF, --check, --boxes) → 수식 겹침 검사 → 풀이 자리 검사
종료 코드: 경고(`!` 줄)가 하나라도 있으면 1. PDF는 그래도 나온다
멈추는 것: yaml 문법 오류, 문제에 text나 answer 없음, "no" 따옴표 없음, mathtext 문법 오류, units와 SVG 높이 불일치
경고하는 것: 그림 너비와 여백, 글자 겹침, 색칠 경계, 쪽 수 ≠ 문제 수, 두 단 상자 없음(문제가 한 쪽을 넘침), 풀이 글 바닥 넘침, 풀이 자리 12칸 아래, 잇단 줄 수식 겹침, 그리드와 서체(render.py --check)


## 보기와 인쇄
PDF 보기: `python -c "import fitz; d=fitz.open('…pdf'); [p.get_pixmap(dpi=110).save(f'{p.number}.png') for p in d]"`
인쇄: `python lib/print_pdf.py {PDF}=학생쪽부수/선생님쪽부수 --plan`으로 보고 `--go`. 몇 쪽만이면 `--pages 1-2`
인쇄 설정: 100%, 양면 긴 쪽, 품질 높게, 색 없는 장은 흑백. README의 학습지 인쇄


## 참고
설치: pip install pyyaml weasyprint pdfplumber matplotlib pymupdf
Windows: GTK 런타임이 따로 필요하다. winget install tschoonj.GTKForWindows
