# 수행평가 학습지 규격


## 환경
포맷: PDF
패키지: pyyaml, weasyprint, pdfplumber, matplotlib, pymupdf. fontTools는 matplotlib이 깐다
설치: pip install pyyaml weasyprint pdfplumber matplotlib pymupdf
Windows: GTK 런타임이 따로 필요하다. winget install tschoonj.GTKForWindows
빌드: templates/build.py가 그림 → 수식 → 표 → HTML → PDF → 검사를 한 번에 한다. a4의 render.py는 직접 부르지 않는다
빌려 쓰는 것: surisomath-a4의 render.py와 base.css, surisomath-grind의 grind_figure.py와 build.py의 rich, surisomath-exam build.py의 width_of와 svg_width
함께 읽히는 것: 시험대비 build.py를 모듈로 읽으면 surisomath-munhang의 seal.py와 unit.py도 읽힌다. 수행평가는 둘을 쓰지 않지만 둘이 깨지면 빌드가 멈춘다
종료 코드: 경고가 하나라도 있으면 1. PDF는 그래도 나온다


## 쪽
단위: 문제 한 개 = 한 쪽(`<section class="assess">`)
본문 영역: 475×682pt(31칸). 세로 플렉스. 위에서부터 채우고 남은 높이가 빈 자리
단: 하나. 세로선, 가로선, 소제목, 심볼 없음
학생 쪽: 문제 수만큼. 첫 쪽 머리줄 오른쪽 끝에 이름 칸
선생님 쪽: 학생 쪽 뒤에 같은 차례(문제 셋이면 4~6쪽). 이름 칸 없음. 머리줄 오른쪽 끝에 정답, 빈 자리 위부터 풀이. answer가 필수라 늘 붙는다
표지, 제목 줄: 없음
쪽번호: a4 그대로(- n -). 선생님 쪽까지 이어 센다


## 쪽의 세로 짜임
기준: 본문 영역 위 끝 = 0
0~11pt: 빈 반 칸
11~33pt: 머리줄. typo-0, neutral-1000. 본문 위상(11 + 22k). 첫 쪽만 오른쪽 끝에 "이름"과 90pt 빈 자리(글에서 4pt 띄움, 아래 선 0.4pt)
33~44pt: 빈 반 칸
44~66pt: 문제 번호. typo-4. 제목 위상(22k)
66~77pt: 번호 아래 반 칸
77pt~: 지문 → 그림 → 표. 블록 사이와 아래 한 칸씩. 본문 위상
그 아래~682pt: 빈 자리. 선생님 쪽은 여기 위부터 풀이
반 칸을 두 번 비우는 까닭: 연마, 시험대비와 같다. 머리줄은 본문 위상에, 번호는 제목 위상에 있어야 한다. 11 + 22 + 11 + 22 + 11 = 77
빈 자리 최소: 12칸. build.py가 가장 좁은 쪽을 재서 알려 주고 모자란 쪽은 쪽마다 경고한다. 위의 반 칸 때문에 늘 .5로 끝난다
빈 자리가 주는 것: 지문이 한 줄 늘면 한 칸, 그림이 한 칸 늘면 한 칸, 표가 한 행 늘면 한 칸


## 머리줄과 정답 줄
머리줄: "수행평가", 학년도 학기, 학교, 학년, 날짜의 다섯 토막을 가운뎃점으로 이은 한 줄. build.py가 폴더 이름에서 만든다. 정본은 아래와 같다
```
수행평가 · 2026학년도 2학기 · 수지중학교 · 중1 · 2026. 9. 17.
```
이름 칸 몫: 120pt("이름" 글과 4pt와 90pt 빈 자리)
머리줄 최대: 355pt(475 − 120). 넘으면 이름 칸과 겹친다. build.py가 width_of로 재서 경고한다. 줄이려면 yaml에 term을 짧게 적는다
정답 줄: "정답: 8점". typo-0, neutral-500. 머리줄 오른쪽 끝, 오른끝맞추기. 선생님 쪽에만
정답 줄 산식: 머리줄 너비 + 16pt + 정답 너비 ≤ 475pt. 넘으면 build.py가 경고한다


## 문제 블록
번호: 001부터 problems.yaml 차례대로. typo-4(20pt/700/-0.05em), 왼끝맞추기
지문: typo-1, 한 문단. 어절 줄 바꿈은 render.py가 한다
그림: 지문 아래 가운데. a4의 `.figure` 블록. 높이 = SVG 높이(22의 배수, units = 높이 ÷ 22). 너비 475pt 안
그림 검사: 높이가 22의 배수가 아니면 멈춘다. 너비가 475pt를 넘으면 y 범위를 몇 배 넓히라고 알려 주고 멈춘다
표: 그림 아래. 그림과 표가 같이 있으면 그림이 먼저
넣지 않는 것: 답 칸, 배점, 풀이 과정 상자


## 풀이
입력: yaml의 `solution: |` 블록
자리: 빈 자리 위부터. 줄마다 p 하나, 문단 간격 없음. 한 줄 = 한 칸. 빈 줄은 한 칸(p.gap)
서체: typo-1. 수식은 `$…$`(12pt)
줄 너비: 본문 너비 475pt, 한글 38자쯤. 넘는 줄은 어절에서 둘로 끊는다
바닥: 682pt. 넘으면 WeasyPrint가 쪽을 쪼개고 build.py가 "풀이 글이 바닥을 넘어 다음 쪽으로 이어진다"로 짚는다
식 번호: 수식 뒤에 줄임표와 원 숫자를 글로. `$a=-\dfrac{1}{4}$ …… ①이고`, "①에 의하여"
좌표의 음수: 둘째 성분이 음수면 `$(8,\,{-2})$`. 안 감싸면 쉼표 뒤 마이너스가 이항 연산자로 벌어진다(좌우 2pt씩). 첫 성분 `$(-4,\,1)$`은 괜찮다


## 표
텍스트: typo-0
행 높이: 22pt
선: 가로와 세로 모두(격자). a4 규격(가로만)의 수행평가 예외
선 두께: 0.4pt
선 색: neutral-500
위선: 첫 행에만. build.py가 첫 행에 class first를 단다(caption이 첫 자식이라 base.css의 thead:first-child가 안 잡힌다)
배경: 없음
열 너비: 같은 너비(table-layout: fixed, 너비를 주지 않는다)
글 정렬: 가운데
셀 패딩: 좌우 8pt
제목: caption. 표 위 가운데. 10pt/500, neutral-1000. 높이 22pt(한 칸)
간격: 위아래 한 칸(22pt). 지문이나 그림 아래 한 칸, 표 아래 한 칸
위첨자: 계급의 이상, 미만. `0^이상~20^미만`처럼 ^ 뒤 한글. 6pt, 줄 높이 0에 relative로 올려 글줄 상자를 안 키운다
물결표: 앞뒤 붙임(a4)
단위: 머리 칸에 괄호로. 점수(점), 횟수(회), 학생 수(명). 원문 표기 그대로
수식: 칸 안 `$…$`는 10pt Computer Modern. 분수도 된다
답 칸: `{답: 9}`. 학생 쪽은 빈 셀, 선생님 쪽은 neutral-500 값(class ans)
빈 칸: `""` 또는 null. 양쪽 다 빈 셀
값: 원문 숫자 그대로(0.2를 0.20으로 고치지 않는다)
yaml: `table:` 아래 title(선택), head(머리 행, 선택), rows(몸 행 목록). 행은 목록, 칸 수는 모두 같아야 한다. 칸은 값이거나 {답: 값}
HTML: `<table class="stat">` 안에 caption, thead(head가 있으면), tbody


## 그림
규격: 연마와 같다. 도형 선 0.7pt(g.EDGE), 그래프 선 1pt(g.STRING), 보조선과 점선 0.4pt(g.AUX), 글자 10pt 정체(g.LABEL), 잉크 여백 4pt
배율: y 범위가 정한다. 좌표평면은 가로세로 배율이 같아야 하므로 y 범위로 배율만 정하고 x 범위는 save()가 잡는다
너비: 475pt 안(단이 없다)
높이: 22의 배수(g.canvas의 units)
축: 0.4pt에 채운 화살촉 6pt(figures.py의 arrow, HEAD = 6.0)
눈금: figures.py의 tick_x(통계 그래프)
좌표 글: 점의 반대쪽 축 옆. 제2사분면의 점이면 x좌표는 x축 아래, y좌표는 y축 오른쪽. O는 곡선과 숫자가 없는 사분면 쪽
도우미: surisomath-grind/templates/grind_figure.py. build.py가 PYTHONPATH에 넣는다
저장 이름: g.save(f, "p1.svg")처럼 늘 준다. 빼면 멈춘다. 이름을 빼서 p001.svg가 되는 곳은 시험대비 새 꼴의 문제 폴더(001/figure.py)뿐이다
견본: build/연마/2026.09.12/figures.py, 정본의 figures.py
보기: PDF를 pymupdf로 PNG를 뽑아 본다. SVG를 바로 열면 점선이 실선으로 보인다


## 학습지 폴더
자리: build/수행평가/{학기}/{학교}/{학년}/{YYYY.MM.DD}/
학기 폴더: YYYY + N학기(20262학기). build.py가 정규식으로 읽어 "2026학년도 2학기"를 만든다
학교, 학년 폴더: 이름 그대로 머리줄에
날짜 폴더: YYYY.MM.DD(2026.09.17). 머리줄에는 a4 날짜 표기(2026. 9. 17.)
파일 이름: 수리소_수행평가_{학교}_{학년}_{YYYY.MM.DD}(수리소_수행평가_수지중학교_중1_2026.09.17)
원문 md: 학습지 폴더 옆 {YYYY.MM.DD}.md(2026.09.17.md) 또는 폴더 안 problems.md. 선생님이 쓴다. 빌드는 읽지 않고 손대지 않는다
problems.yaml: 빌드 입력
figures.py: 그 학습지 그림만. 그림이 없으면 두지 않는다
figures/: 빌드가 만든 SVG. 그림 p*.svg, 수식은 m(지문), t(표 칸), a(정답), s(풀이) 뒤에 번호. 수식 SVG는 빌드마다 다시 그리고 안 쓴 것은 지운다
결과: 수리소_수행평가_{…}.html, .pdf
PDF 날짜: 수행평가 날짜로 고정(SOURCE_DATE_EPOCH). 같은 입력이면 PDF도 바이트 단위로 같다


## 원문 md
머리: `# {YYYY.MM.DD} {학교} {학년} 수행평가`
문제: `## 001`, `## 002`, …
지문: `### 지문` 아래 한 문단
그림: `### 그림` 아래 설명 글(점의 좌표, 지나는 점)
표: `### 표` 아래 `#### 제목`과 `#### 내용`. 내용은 행마다 한 줄, 칸은 `|`로 가른다


## problems.yaml
머리 정보: term, school, grade, date, file은 적지 않는다. 폴더 이름에서 만든다. 적으면 그것이 이긴다(머리줄이 길 때 term을 줄이는 데 쓴다)
problems: 문제 목록. 차례가 번호다
필드 차례: "no"(선택) → text → figure → alt → table(title → head → rows) → answer → solution
text: 지문. 원문 문장 그대로, 표기만 조판. `": "`가 들어가면 따옴표로 감싼다. 역슬래시는 따옴표 없는 글에서 그대로 살아 있다
figure: figures/ 안의 그림 파일 이름(p1.svg). units는 적지 않는다
alt: 그림 설명. PDF에는 안 찍힌다
table: title(선택), head(선택), rows
answer: 필수. 서술형은 단위까지(8점), 수식은 `$…$`, 표 완성은 답 칸 값을 읽는 차례로(9, 0.36, 0.2, 7, 1)
solution: 선택. `|` 블록. 줄마다 한 칸, 빈 줄은 한 칸
"no": 번호를 직접 줄 때. `"no": "004"`처럼 키와 값 모두 따옴표로. 따옴표가 없으면 YAML이 거짓으로 읽고 build.py가 멈춘다


## 파일
templates/assess.css: base.css 위에 얹는 수행평가 스타일. 위 규격의 구현
templates/build.py: 빌드. 시험대비 build.py를 모듈로 읽고 그 안의 연마 build.py(rich)를 함께 쓴다
references/spec.md: 이 파일
실행: `python .claude/skills/surisomath-assess/templates/build.py build/수행평가/{학기}/{학교}/{학년}/{날짜}/problems.yaml`
--no-figures: figures.py를 실행하지 않는다(글만 고칠 때)
--no-check: 그리드 검사를 건너뛴다
PDF 보기: `python -c "import fitz; d=fitz.open('…pdf'); [p.get_pixmap(dpi=110).save(f'{p.number}.png') for p in d]"`
인쇄: `python lib/print_pdf.py {PDF}=학생쪽부수/선생님쪽부수 --plan`으로 보고 `--go`. 몇 쪽만이면 `--pages 1-2`. 100%, 양면 긴 쪽, 품질 표준. 색 없는 장은 흑백. README의 학습지 인쇄
인쇄 가르기: 수행평가는 PDF 하나라 print_pdf가 앞 절반을 학생 쪽, 뒤 절반을 선생님 쪽으로 가른다. 시험대비 새 꼴의 _문제.pdf, _정답.pdf 짝과 다르다


## 검사
figures.py: grind_figure.save()의 `!` 줄(잉크 여백, y 범위 제안, 글자 겹침, 색칠 경계)
그림: 높이가 22의 배수인지, 너비가 475pt 안인지. 아니면 멈춘다
머리줄: 글 너비 355pt 초과
정답 줄: 머리줄 너비 + 16pt + 정답 너비가 475pt 초과
그리드와 서체: a4 render.py --check
잇단 줄 수식 겹침: 연마 build.py의 check_overlap
쪽 수: 학생 쪽 + 선생님 쪽과 다르면 어느 문제가 한 쪽을 넘친 것
블록 넘침: "문제 블록이 한 쪽을 넘쳐 다음 쪽으로 밀렸다". 그림이나 표를 줄인다
풀이 넘침: "풀이 글이 바닥을 넘어 다음 쪽으로 이어진다". 줄을 줄인다
빈 자리: 가장 좁은 쪽의 칸 수를 알려 주고 12칸 아래인 쪽은 쪽마다 경고
