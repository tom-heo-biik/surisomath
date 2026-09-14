---
name: surisomath-exam
description: "수리소 수학학원의 실전 모의 학습지 '시험대비' 양식이 작성되어 있는 SKILL입니다. 시험대비 학습지를 새로 만들거나 고치는 상황에 사용합니다. surisomath-a4 위에 얹고 surisomath-grind의 그림 도우미와 수식 조판을 빌려 쓰므로 두 SKILL도 함께 읽어야 합니다. 한 쪽에 문제 둘, 두 단에 한 문제씩이고 문제 아래가 학생이 손으로 푸는 빈 자리입니다."
---

# 수리소 수학학원 시험대비 학습지 양식


## 환경
포맷: PDF
선행 스킬: surisomath-a4 — 판형·여백·그리드·서체·렌더·그리드 검사. surisomath-grind — 그림 도우미(grind_figure.py)와 본문 수식 조판(build.py의 rich), 분수 규격
작업 순서: build.py가 그림 → 수식 → HTML → PDF → 검사를 한 번에 한다. a4의 render.py를 직접 부르지 않는다
패키지: pyyaml, weasyprint, pdfplumber, matplotlib, pymupdf. fontTools는 matplotlib이 깐다


## 쪽
단위: 한 쪽에 문제 둘(`<section class="exam">`). 두 단, 단마다 문제 하나
본문 영역: 475×682pt(31칸). 위에 머리줄, 44pt부터 바닥까지 두 단
학생 쪽: 문제 열 개면 다섯 쪽. 선생님 쪽이 그 뒤에 같은 짝으로 다섯 쪽(6~10쪽). 문제 수가 홀수면 마지막 쪽의 오른 단이 빈다
표지·제목 줄·이름 칸 행: 없음. 머리줄에 시험·학년·단원이 있고 첫 쪽 머리줄 오른쪽 끝에 이름 칸이 있다
쪽번호: a4 그대로(- n -). 선생님 쪽까지 이어 센다


## 쪽의 세로 짜임
기준: 본문 영역 위 끝 = 0
0~11pt: 빈 반 칸
11~33pt: 머리줄 "시험대비 · 2026학년도 2학기 중간고사 · 중3 · 삼각비". typo-0, neutral-1000. 본문 위상(11 + 22k). 첫 쪽만 오른쪽 끝에 "이름"과 90pt 빈 자리(아래 선 0.4pt)
33~44pt: 빈 반 칸
44~66pt: 문제 번호. typo-4. 제목 위상(22k)
66~77pt: 번호 아래 반 칸
77pt~: 지문 → 그림 → 선지. 블록 사이·선지 아래 한 칸씩. 본문 위상
그 아래~682pt: 풀 자리. 빈 종이. 소제목·심볼·가로선 없음
반 칸을 두 번 비우는 까닭: 연마와 같다. 11 + 22 + 11 + 22 + 11 = 77
풀 자리: 문제 글부터 바닥까지 27.5칸에서 문제 블록을 뺀 것. 늘 .5로 끝난다. build.py가 가장 좁은 단의 칸 수를 알려 주고, 8칸 아래인 단은 단마다 경고한다


## 단
왼 단 x = 0~237pt, 오른 단 237~475pt. 가운데 세로선 하나(neutral-1000, 0.4pt)가 x = 237pt(쪽 기준 297pt)에 번호 줄 위(44pt)부터 바닥(682pt)까지. 정수 좌표라야 화면에서 검게 보인다
글은 선에서 8pt. 왼 단 글 너비 229pt, 오른 단 230pt
바깥 세로선·가로선: 없음. 학교 시험지 꼴이다. 연마의 세 줄 상자는 두 번 푸는 자리라 여기 안 쓴다
단을 넘치면: WeasyPrint는 넘친 내용을 바닥 아래로 흘리지 않고 쪽을 쪼갠다. build.py가 풀 자리 상자의 쪽을 보고 어느 문제가 밀렸는지 짚는다("문제 블록이 단을 넘쳐 다음 쪽으로 밀렸다" / "풀이 글이 단 바닥을 넘어 다음 쪽으로 이어진다")


## 문제
번호: 001부터 problems.yaml 차례대로. typo-4, 단 왼끝. 순서는 바꾸지 않는다
지문: typo-1, 한 문단. problems.md 문장을 한 글자도 바꾸지 않는다. 바꾸는 것은 표기뿐이다
그림: 지문 아래 단 가운데. a4의 `.figure` 블록. units는 yaml에 적지 않는다 — SVG 높이가 칸 수다(22의 배수가 아니면 멈춘다). 너비 229pt 안. 넘으면 build.py가 y 범위를 몇 배 넓히라고 알려 준다
선지: `<ol class="n7">`(① ② ③ ④ ⑤, 마커 칸 22pt). build.py가 선지마다 너비(마커 22pt + 글)를 재서 다섯 모두 45.8pt(단 글 너비 ÷ 5) 안이면 5열 한 줄, 76.3pt(÷ 3) 안이면 3열(①②③ / ④⑤, ④는 ① 아래), 아니면 1열 다섯 줄. 수능·모의고사 관례다. 1열에서 항목 하나가 단을 넘으면 경고한다
넣지 않는 것: 답 칸, 배점, [서술형] 표시. 문제 글에 없는 것은 넣지 않는다


## 표기 규칙
낱말로 쓴 도형 표기를 교과서 기호로 조판한다. 연마 규칙(`!=` → `\neq`, `b/x` → `\dfrac{b}{x}`, 점 이름 정체, 변수 이탤릭, 수식 뒤 조사 붙여 쓰기) 위에 얹는다
선분 AB → `$\overline{\mathrm{AB}}$`
각 A, 각 BAC → `$\angle\mathrm{A}$`, `$\angle\mathrm{BAC}$`
삼각형 ABC → `$\triangle\!\mathrm{ABC}$`. `\!`가 없으면 "△ ABC"처럼 벌어진다
사각형 ABCD → `$□\mathrm{ABCD}$`. 유니코드 □를 그대로 쓴다. `\square`는 mathtext에 없다
루트 (…)^2, 2루트3 → `$\sqrt{(\cdots)^2}$`, `$2\sqrt{3}$`
sinx, tan 52°, 35° → `$\sin x$`, `$\tan 52^{\circ}$`, `$35^{\circ}$`. 각도는 낱말 사이에 홀로 있어도 수식 서체다. `^{\circ}`처럼 중괄호로 감싼다 — `^\circ`는 "60 °"처럼 벌어지고, 수식 안의 °는 γ로 찍힌다
각 BAC = 60°, tan63°=1.96 → `$\angle\mathrm{BAC}=60^{\circ}$`, `$\tan 63^{\circ}=1.96$`
80 / (tan 52° + tan 35°) → `$\dfrac{80}{\tan 52^{\circ}+\tan 35^{\circ}}$`
A'BC' → `$\triangle\!\mathrm{A}'\mathrm{BC}'$`. 프라임은 mathrm 밖에
낱말로 남기는 것: 직각삼각형 ABC, 정사각형 ABCD, 직사각형 ABCD(이름만 `$\mathrm{ABCD}$`), 점 A, 지점 A, 직선 $l$(이탤릭), 중점 M. 교과서에서도 낱말이다
치수: 80m, 4cm, 124m, 30%는 글자 그대로(a4의 단위 붙여쓰기). 수식 안 값에 단위가 붙으면 `$\overline{\mathrm{AB}}=8$cm`처럼 수식 뒤에 글자로
분수 분자에 근호가 들면(`$\dfrac{40\sqrt{3}}{9}$`) 수식이 글줄 상자 위로 3pt쯤 넘는다. 교과서 표기라 그대로 쓰되 잇단 두 줄에서 세로로 겹치게 두지 않는다 — build.py가 겹치면 단마다 경고한다


## 선생님 쪽
자리: 학생 쪽 뒤에 같은 짝으로. 양식은 학생 쪽과 똑같고 이름 칸만 없다
정답 줄: 풀 자리 첫 줄 "정답: ④". typo-0, neutral-500, 왼끝. 객관식은 번호만, 서술형은 단위까지(182.35m, 2% 감소). 한 줄, 단 글 너비 안 — 넘으면 경고. answer는 solution이 없어도 필수다
풀이: yaml의 `solution: |` 블록. 정답 줄 다음 줄부터. 줄마다 한 칸, 빈 줄은 한 칸을 비운다. typo-1, 수식은 `$…$`. 한 줄이 단 너비(한글 19자쯤)를 안 넘게 짧게 끊어 쓴다. 단 바닥을 넘으면 경고
풀이 문체: 연마 규칙 그대로. 서술형 모범 답안. 전개만 쓰고 대입한 식·계산은 일부러 생략. "~이므로 ~이다." 마지막 줄 "따라서 …이다." 그림은 "주어진 그림에서". 객관식은 마지막 줄에 식을 적고 정답 줄이 번호를 맡는다
solution이 없는 문제: 그 단의 풀 자리가 비고 정답도 안 찍힌다. 문제 전부에 없으면 선생님 쪽을 안 붙인다


## 그림
규격: 연마 것 그대로(도형 선 0.7pt, 보조선 0.4pt, 글자 10pt 정체, 잉크 여백 4pt, y 범위가 배율)
너비: 단이 좁다. 넓은 그림(두 지점에서 올려다본 산)은 y 범위를 넉넉히 잡아 배율을 낮춘다
칸 수: 5~7. 도형 하나면 5, 회전축처럼 세로로 긴 그림은 7
삽화: 없다. 산·기구·성산일출봉은 지면 선 위의 삼각형이다
각: `g.angle(ax, v, p, q, "$35^{\circ}$", r=12)`. 호 0.4pt, 글은 각 안쪽 이등분선 위. 같은 각 표시는 `ticks=1`. p→q 반시계가 우각이면 경고한다
같은 길이: `g.tick(ax, p, q, n)`. 중점 표시. 다른 쌍은 n=2
길이 글: 교과서처럼 변 옆에 바로 적는다 — `g.name(ax, 변의 가운데, "80m", dy=-5, va="top")`. 점선 곡선(`g.dim`)은 그려지지 않은 길이에만
점선 도형: `g.poly(ax, pts, dashed=True)`. 회전축: `g.axis(ax, p, q, "$l$")` 일점쇄선
직각 표시: `g.right_angle`·`g.foot`. 정사각형·직사각형은 `g.rect`가 네 귀퉁이에 그린다
눈으로 볼 때: PDF를 pymupdf로 PNG를 뽑아 본다. SVG를 pymupdf로 바로 열면 점선이 실선으로 보인다


## 파일
templates/exam.css: base.css 위에 얹는 시험대비 스타일. 위 규격의 구현
templates/build.py: problems.yaml 하나로 그림 → 수식 → HTML → PDF → 검사. 연마 build.py를 모듈로 읽어 rich()를 쓴다
templates/sample/: 견본 세 문제(객관식 5열, 그림 있는 서술형, 객관식 3열 — 홀수 짝). 새 단원은 이 폴더의 problems.yaml과 figures.py를 복사해 출발한다. 실제 학습지의 정본은 build/시험대비/20262학기중간/중3/삼각비/
견본은 회귀 검사다: build.py·exam.css·render.py·grind_figure.py를 고친 뒤 견본을 다시 빌드해 `git status --short .claude/skills/surisomath-exam/templates/sample/`가 비어 있으면 양식이 그대로라는 뜻이다


## 단원 폴더
자리: build/시험대비/<시험>/<학년>/<단원>/. 시험 폴더 이름은 `YYYY` + `N학기` + `중간|기말`(20262학기중간). build.py가 정규식으로 읽어 머리줄 "2026학년도 2학기 중간고사"와 파일 이름 수리소_시험대비_2026_2학기중간_중3_삼각비를 만든다. 학년·단원 폴더 이름은 그대로 쓴다
problems.md: 선생님 원문. `## 001` 아래 `### 지문` `### 그림`(설명) `### 선지`(1.~5.). 빌드는 이 파일을 읽지 않고 손대지도 않는다
problems.yaml: 빌드 입력. 지문을 표기 규칙대로 옮기고 choices·answer·solution, 그림이 있으면 figure·alt. exam·grade·unit·file·date는 적지 않는다 — 폴더 이름에서 만든다
figures.py: 그 단원 그림만. 그림이 없으면 두지 않는다
figures/: 빌드가 만든 SVG(그림 p*.svg, 수식 m*·c*·a*·s*.svg). 수식 SVG는 빌드마다 다시 그리고 안 쓴 것은 지운다
수리소_시험대비_….html, .pdf: 빌드 결과. PDF 안의 만든 날짜는 학기 첫날(1학기 3. 1., 2학기 9. 1.)로 고정해 같은 입력이면 PDF도 바이트 단위로 같다. 폴더 꼴이 안 맞으면 yaml의 date를 적어라


## 작업 순서
1. build/시험대비/<시험>/<학년>/<단원>/problems.md를 읽는다. templates/sample/의 problems.yaml과 figures.py를 그 옆에 복사한다
2. problems.yaml에 지문을 표기 규칙대로 옮기고 choices·answer·solution·figure·alt를 적는다. exam·grade·unit·file·date 줄은 지운다
3. figures.py에 그 단원 그림만 남긴다
4. `python .claude/skills/surisomath-exam/templates/build.py build/시험대비/<시험>/<학년>/<단원>/problems.yaml`
5. 경고가 없으면(종료 코드 0) 규격은 끝이다. `!` 줄은 무엇을 어떻게 고치라고 말해 준다. 그대로 고치고 다시 돌린다. 그리드 검사가 어긋나도 뒤 검사가 끝까지 돌아 까닭을 짚는다
6. PDF를 눈으로 본다. 각도 글이 선에 걸리는지, 그림이 문제와 맞는지, 선지 열이 관례대로인지는 눈으로만 안다
그림은 그대로 두고 글만 고칠 때는 --no-figures를 붙인다. 그리드 검사를 건너뛰려면 --no-check


## 쓰는 법
problems.yaml: problems[]만 있으면 된다. text · answer, 객관식이면 choices(다섯, 목록), 그림이 있으면 figure · alt, 선생님 풀이가 있으면 solution(`|` 블록)
text에 ": "가 들어가면 따옴표로 감싼다. 수식의 역슬래시는 따옴표 없는 글에서 그대로 살아 있다
번호를 직접 주려면 `"no": "004"` — 키와 값 모두 따옴표로
figures.py 뼈대: `import grind_figure as g` → `g.setup(__file__)` → 그림 함수들 → `if __name__ == "__main__":`에서 부른다. 연마와 같다
PDF 보기: `python -c "import fitz; d=fitz.open('…pdf'); [p.get_pixmap(dpi=110).save(f'{p.number}.png') for p in d]"`


## 참고
pip install pyyaml weasyprint pdfplumber matplotlib pymupdf
Windows는 GTK 런타임이 따로 필요하다: winget install tschoonj.GTKForWindows
