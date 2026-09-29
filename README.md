# surisomath

수리소 수학학원(SURISO MATH ACADEMY)의 Claude Code 플러그인.

## 스킬

### surisomath-a4

수리소 표준 문서 양식. A4 세로 595×842pt, 22pt 베이스라인 그리드, KoPubWorld 바탕체.
HTML로 쓰고 WeasyPrint로 PDF를 뽑는다.

```
.claude/skills/surisomath-a4/
├─ SKILL.md
└─ templates/
   ├─ base.html      복사해서 쓰는 빈 뼈대
   ├─ base.css       규격 구현 스타일시트
   ├─ sample.html    모든 요소가 들어간 견본
   ├─ render.py      HTML → PDF (어절 줄 바꿈 자동 처리)
   ├─ figure.py      수식·그래프 → Computer Modern SVG
   └─ fonts/         KoPubWorld 바탕체 Light·Medium·Bold + 라이선스
```

```
pip install weasyprint pdfplumber matplotlib
winget install tschoonj.GTKForWindows        # Windows에서만

python .claude/skills/surisomath-a4/templates/render.py 문서.html --check
```

`--check`는 렌더한 PDF의 모든 글줄이 22pt 그리드 위에 있는지 실제로 재서 알려 준다.

### surisomath-grind

서술형 학습지 '연마(硏磨)' 양식. surisomath-a4 위에 얹는다. 문제 한 개가 한 쪽이고,
아래 두 단(원석 풀이·보석 풀이)은 학생이 손으로 채운다. 문제는 `problems.yaml`에
데이터로 적고, 그림·HTML·PDF·그리드 검사를 명령 하나로 뽑는다.

```
.claude/skills/surisomath-grind/
├─ SKILL.md
└─ templates/
   ├─ grind.css        base.css 위에 얹는 연마 스타일
   ├─ grind_figure.py  문제 그림 도우미(캔버스·점선 곡선 치수·음영·직각 표시)
   ├─ build.py         problems.yaml → 그림 → HTML → PDF → --check
   ├─ symbol.svg       소제목 앞 심볼(22pt)
   └─ sample/          견본 단원. 새 단원은 이 폴더를 복사해 출발한다
```

```
python .claude/skills/surisomath-grind/templates/build.py build/연마/2026.09.12/problems.yaml
```

학습지 폴더는 `build/연마/{YYYY.MM.DD}/`. 정본은 위 명령의 `2026.09.12/`이고, 그보다 앞서 양식을
시험한 `build/연마_원의둘레와넓이/`는 견본으로 삼지 않는다.

### surisomath-exam

실전 모의 학습지 '시험대비' 양식. surisomath-a4 위에 얹고 연마의 그림 도우미와 수식 조판,
surisomath-munhang의 단원 읽기와 표기 검사와 봉인을 빌려 쓴다. 한 쪽에 문제 둘(두 단), 문제 아래는
학생이 손으로 푸는 빈 자리. 선생님 쪽에는 정답 줄과 풀이가 같은 자리에 붙는다. 길이와 크기는
식 안의 기호로, 도형은 낱말(선분 AB, 각 A, 삼각형 ABC)로 쓰고 빌드가 그 경계를 검사한다.

```
.claude/skills/surisomath-exam/
├─ SKILL.md
└─ templates/
   ├─ exam.css      base.css 위에 얹는 시험대비 스타일(두 단·세로선·머리줄·이름 칸·선지 열)
   ├─ build.py      단원 폴더 → 그림 → HTML → PDF → 검사. 옛 꼴과 새 꼴을 다 빌드한다.
   │                연마 build.py의 rich()를 모듈로 쓴다. --png DIR이면 쪽과 그림 크롭 PNG
   ├─ figrun.py     새 꼴에서 문제마다 둔 figure.py를 한 프로세스에서 차례로 돌린다(build.py가 부른다)
   ├─ photos.py     선생님이 보낸 문제 사진을 번호에 붙이고 읽기용 축소본을 뽑는다.
   │                새 꼴은 001/photo.jpg, 옛 꼴은 수리소_시험대비_…_001.jpg
   ├─ sample/          옛 꼴 견본 세 문제(problems.yaml 하나)
   └─ sample_folders/  새 꼴 견본 세 문제(unit.yaml, 001~003/, 002/figure.py). 새 단원은 이 짜임으로 출발한다
```

```
python .claude/skills/surisomath-exam/templates/photos.py "build/시험대비/20262학기기말/중1/기본 도형"
python .claude/skills/surisomath-exam/templates/build.py "build/시험대비/20262학기기말/중1/기본 도형" --png out
python .claude/skills/surisomath-exam/templates/build.py build/시험대비/20262학기중간/중3/이차함수
```

단원 폴더는 `build/시험대비/{시험}/{학년}/{단원}/`. 시험 폴더 이름(`20262학기중간`)에서 머리줄과
파일 이름을 만든다. 폴더 이름에 빈칸이 있으면(`원과 직선`, `기본 도형`) 명령에서 따옴표로 감싼다.

단원은 두 꼴이다. 단원에 `problems.yaml`이 있으면 옛 꼴, 없으면 새 꼴이고 둘이 섞이면 빌드가 멈춘다.
명령은 어느 꼴이든 단원 폴더를 받는다(옛 꼴은 `problems.yaml` 경로도 된다).

옛 꼴(단원 하나에 problems.yaml)은 단원에 `problems.yaml`, `problems.md`, `figures.py`를 하나씩 둔다.
PDF는 하나이고 학생 쪽 뒤에 선생님 쪽이 붙는다. 20262학기중간 중3의 세 단원, 시험기출 수지중학교,
견본 `sample/`이 이 꼴이다.

새 꼴(문제마다 폴더, 2026-09-30부터)은 문제마다 `001/`, `002/` … 폴더를 두고 그 안에 `problem.yaml`,
`problem.md`(원문과 되돌리기 기록), `figure.py`(그림이 있을 때), `photo.jpg`(원문 사진)를 둔다.
번호는 폴더 이름이다. PDF와 HTML은 둘이다. `{학습지 이름}_문제.pdf`는 학생 쪽이고 첫 쪽에 이름 칸이 있다.
`{학습지 이름}_정답.pdf`는 선생님 쪽이고 쪽번호가 1부터다.

새 꼴의 그림은 모두 단원의 `figures/`에 모이므로 이름이 문제 번호로 시작한다. `g.save(f)`에 이름을
안 주면 `p001.svg`이고, 그림이 둘이면 `p001a.svg`처럼 짓는다. 여러 문제가 같이 쓰는 그림 도우미는
단원의 `figlib.py`에 둔다. 머리 설정이 폴더 이름과 다를 때만 단원의 `unit.yaml`에 적는다.

정본은 20262학기중간 중3의 이차함수(좌표평면 그림, 보기와 조건 상자, 평가원 문형), 원과 직선(원과
현과 접선 그림, 문장 안 도형의 낱말), 삼각비(도형 그림, 삼각비의 표, 삽화 문제) 세 단원이다. 셋 다
옛 꼴이고 새 꼴의 짜임은 `sample_folders/`가 보여 준다.

### surisomath-assess

학교 수행평가 대비 학습지 '수행평가' 양식. surisomath-a4 위에 얹고 연마의 그림 도우미와 수식 조판,
시험대비의 너비 재기를 빌려 쓴다. 문제 한 개가 한 쪽, 단은 하나, 문제 아래는 학생이 손으로 쓰는
빈 종이다. 선생님 쪽이 같은 차례로 뒤에 붙고 정답은 머리줄 오른쪽 끝, 풀이는 빈 자리에 들어간다.
중1 통계의 도수분포표는 격자 표로 조판하고, 답 칸은 학생 쪽에서 비고 선생님 쪽에서 회색으로 찍힌다.

```
.claude/skills/surisomath-assess/
├─ SKILL.md
└─ templates/
   ├─ assess.css    base.css 위에 얹는 수행평가 스타일(머리줄·이름 칸·격자 표·이상/미만 위첨자)
   └─ build.py      problems.yaml → 그림 → 수식 → 표 → HTML → PDF → 검사. 시험대비·연마 build.py를 모듈로 쓴다
```

```
python .claude/skills/surisomath-assess/templates/build.py build/수행평가/20262학기/수지중학교/중1/2026.09.17/problems.yaml
```

학습지 폴더는 `build/수행평가/{학기}/{학교}/{학년}/{날짜}/`. 폴더 이름에서 머리줄
"수행평가 · 2026학년도 2학기 · 수지중학교 · 중1 · 2026. 9. 17."과 파일 이름을 만든다. 정본은 그 폴더다.
수행평가는 옛 꼴 그대로다(학습지 하나에 problems.yaml, PDF 하나).

### surisomath-munhang

학습지의 문제 글(문항)을 평가원 문형으로 쓰고 퇴고하는 스킬. 양식이 아니라 글의 규칙이라 연마,
시험대비, 수행평가가 함께 따른다. 문장의 짜임, 낱말과 기호의 경계, 확정 문항의 봉인, 독립 검토
절차가 있다. 시험대비 빌드가 여기 있는 도구로 단원을 읽고 표기와 봉인을 검사한다.

```
.claude/skills/surisomath-munhang/
├─ SKILL.md
├─ references/
│  ├─ notation.md      낱말과 기호의 표기 규칙
│  └─ canon.md         확정 문항의 책 문장과 정본 문장 쌍(정본 대조본)
└─ templates/
   ├─ unit.py          단원 읽기. 옛 꼴과 새 꼴을 같은 모양으로 돌려준다(빌드, 봉인, 표기 검사가 함께 쓴다)
   ├─ seal.py          확정 문항 봉인. 단원의 sealed.json에 글의 해시를 적고 빌드마다 대조한다
   ├─ notation.py      표기 검사(길이와 크기는 식 안의 기호, 도형은 낱말)
   └─ review_brief.md  독립 검토자에게 주는 브리핑 틀
```

```
python .claude/skills/surisomath-munhang/templates/seal.py "build/시험대비/20262학기기말/중1/기본 도형" 003 004
python .claude/skills/surisomath-munhang/templates/seal.py "build/시험대비/20262학기기말/중1/기본 도형" --check
python .claude/skills/surisomath-munhang/templates/notation.py "build/시험대비/20262학기기말/중1/기본 도형"
```

봉인은 선생님이 번호를 짚어 확정할 때만 건다. `--list`는 봉인 목록, `--unseal 003`은 풀기다. 확정
표시는 옛 꼴이 `problems.md` 머리의 확정 줄, 새 꼴이 그 문제 `problem.md` 둘째 줄의
`확정(2026. 10. 1.)`이다. `--check`와 빌드가 봉인과 이 표시와 `canon.md` 쌍을 맞춰 본다.

## 학습지 인쇄

연마, 시험대비, 수행평가 PDF를 학원 프린터(EPSON EM-C800)로 뽑는다. 100% 크기, 양면 긴 쪽 넘김,
품질 "표준"과 해상도 "일반"이다. "최고품질"이 필요하면 `--quality high`로 "높게"와 "섬세하게"다.
학생 쪽과 선생님 쪽의 부수는 `=학생 쪽 부수/선생님 쪽 부수`로 따로 정한다. PDF 꼴은 둘이다.

PDF가 하나인 것은 연마, 수행평가, 시험대비 옛 꼴이다. 앞 절반이 학생 쪽, 뒤 절반이 선생님 쪽이라
반으로 가르고 쪽 수가 홀수면 멈춘다. 연마는 풀이가 있는 문제만 선생님 쪽이 붙으니 풀이가 빠진 문제가
있으면 절반이 맞지 않는다. 그때는 `--pages`로 쪽을 정한다.

PDF가 둘인 것은 시험대비 새 꼴이다. `{학습지 이름}_문제.pdf`가 학생 쪽, `{학습지 이름}_정답.pdf`가
선생님 쪽이다. 짝의 앞 이름(`{학습지 이름}.pdf`)이나 둘 가운데 하나를 적으면 짝을 찾아 `_문제.pdf`에
학생 쪽 부수, `_정답.pdf`에 선생님 쪽 부수를 건다. 가르지 않으니 홀수 쪽이어도 된다. 짝 없이 한쪽
파일만 있으면 그 파일을 통째로 그쪽 부수만큼 보낸다.

```
python lib/print_pdf.py 삼각비.pdf=4/2 "원과 직선.pdf=2/2" --plan   계획과 프린터 설정 확인
python lib/print_pdf.py 삼각비.pdf=4/2 "원과 직선.pdf=2/2" --go     보낸다 (학생 쪽 4부, 선생님 쪽 2부 …)
python lib/print_pdf.py "기본 도형.pdf=4/2" --go                 새 꼴 짝. 기본 도형_문제.pdf 4부, 기본 도형_정답.pdf 2부
python lib/print_pdf.py "기본 도형_정답.pdf=0/1" --go            새 꼴 짝에서 정답만 한 부
python lib/print_pdf.py 삼각비.pdf --pages 1-2 --go              1, 2쪽만 한 부
python lib/print_pdf.py "기본 도형_문제.pdf" --pages 1-2 --go    짝의 한쪽만 쪽을 고를 때는 그 파일 이름을 적는다
python lib/print_pdf.py 삼각비.pdf=4/1 --quality high --go       "최고품질"이면 높게+섬세하게로
```

예의 PDF 이름은 줄여 적었다. 실제 이름에는 `수리소_시험대비_2026_2학기기말_중1_기본 도형_문제.pdf`처럼
학습지 이름이 붙는다. 짝을 제대로 찾았는지는 `--plan`이 맨 먼저 찍는 작업 목록(`… 기본 도형 학생 쪽 1/4`,
`… 기본 도형 선생님 쪽 1/2`)으로 본다.

쪽을 프린터 해상도로 그려 1:1로 보내므로 뷰어의 용지 맞춤이 끼지 않는다. 색 없는 장은 흑백으로,
색 있는 장만 컬러로 보낸다. 프린터가 작업 순서를 바꾸지 못하게 뒤 작업을 멈춰 두었다가 차례로 푼다.
프린터 기본 설정은 건드리지 않는다. 자세한 까닭은 `lib/print_pdf.py` 머리에 적었다.

Windows 전용이고 `pip install pywin32 numpy pymupdf`가 필요하다. 품질 설정 이름이 Epson 드라이버
고유라 다른 프린터에서는 설정 확인 단계에서 멈춘다. 프린터 이름이 다르면 `--printer`로 준다.

## 서체

셋 다 저장소에 담아 두었다. 스킬과 빌드 스크립트가 담아 둔 파일을 직접 읽으므로
새 PC에 플러그인만 깔아도 서체가 바로 박힌다. 따로 설치할 일이 없다.

| 서체 | 무게 | 자리 | 쓰임 |
|---|---|---|---|
| KoPubWorld 바탕체 | 300·500·700 | `.claude/skills/surisomath-a4/templates/fonts/` | 문서·인쇄물 본문 |
| Pretendard | 300·400·500·600·700 | `assets/fonts/` | 화면용 산세리프 |
| 학교안심 상장 R | 단일 | `assets/fonts/` | 상장 |

KoPubWorld만 자리가 다른 까닭은 `surisomath-a4` 명세가 서체를 자기 파일 목록으로
잡고 있어서다. 사본을 하나 더 두지 않고 그쪽을 정본으로 본다.

한글·워드·파워포인트처럼 OS에 깔린 서체만 쓰는 프로그램에서 같은 서체를 쓰려면
그때만 설치한다. 관리자 권한이 필요 없다.

```
python lib/install_fonts.py           # 설치
python lib/install_fonts.py --check   # 설치 여부 확인
```

서체 이름은 `KoPubWorld바탕체_Pro` · `Pretendard` · `학교안심 상장`으로 뜬다.

셋 다 무료로 재배포할 수 있고, 배포할 때 약관을 함께 담아야 한다. KoPubWorld는
문화체육관광부와 한국출판인회의가, Pretendard는 길형진이, 학교안심 상장은 KERIS가
저작권을 갖는다. 뒤 둘은 SIL Open Font License 1.1이다. 자세한 것은
[`assets/fonts/README.md`](assets/fonts/README.md).

Jura·Geist Mono·IBM Plex Mono·Malgun Gothic은 담지 않았다. 까닭은 같은 문서에 적었다.

## 브랜드 자산

```
assets/              로고 PNG 4종 — 심볼, 한글·영문·전체 워드마크
assets/고려대학교/     고려대 공식 엠블럼 GIF 4종 (정상·역상 × 흰색·베이지)
assets/fonts/        Pretendard·학교안심 상장 + 라이선스
lib/suriso.py        자산 경로·서체·색·인쇄 규격 상수
build/               인쇄물 빌드 스크립트
자료/                 확정 인쇄물 PDF (문제집 표지, 배너, 숙제 라벨)
```

빌드 스크립트는 절대 경로를 박지 말고 `lib/suriso.py`에서 가져다 쓴다.
어느 PC에 설치되든 자기 위치를 기준으로 자산을 찾는다.

```
python lib/suriso.py       # 자산이 다 있는지 점검
```

브랜드 톤은 **순흑백 모노라인**이다. 검정 단색만 쓰고 회색 틴트를 쓰지 않는다.
고려대 크림슨(`#7C001A`)은 고려대와 함께 쓰는 인쇄물에만 쓴다.

## 인쇄물 빌드

```
build/
├─ vectorize.py    저해상도 로고 비트맵 → SVG 패스
└─ banner_kut.py   고려대 KUT 우수단체상 배너 600×1800mm
```

```
python build/banner_kut.py            자료/ 에 인쇄용 CMYK PDF를 쓴다
python build/banner_kut.py --rgb      화면 확인용 RGB판도 같이 쓴다
python build/banner_kut.py --parts    프레임·월계관·장식만 크게 뽑아 본다
```

로고 원본이 래스터뿐이라 1.8m 배너에 그대로 키우면 계단이 보인다. `vectorize.py`가
비트맵을 6배로 늘려 안티에일리어싱의 0.5 등고선을 따서 패스를 만든다. 없는 해상도를
지어내는 것이 아니라 원본이 이미 가진 가장자리 정보를 꺼내 쓰는 것이라, 확대해도
깨지지 않는다.

### 인쇄 규약

비즈하우스 기준으로 맞춰 두었다. 다른 곳에 넘길 때도 이 세 가지는 대개 같다.

| | |
|---|---|
| 색상 모드 | DeviceCMYK. WeasyPrint가 RGB로만 쓰므로 `to_cmyk()`가 내용 스트림의 `rg`/`RG`를 `k`/`K`로 갈아 끼운다 |
| 서체 | 전부 아웃라인. 조판하지 않고 fontTools로 글리프 윤곽을 떠서 앉히므로 PDF에 서체가 없다 |
| 투명도 | 없음. `ca=1`짜리 ExtGState까지 걷어내 검판에 안 걸리게 한다 |
| 비트맵 | 없음. 전부 벡터라 60×180cm에서도 해상도 개념이 없다 |

CMYK 값은 시스템 ICC(sRGB → U.S. Web Coated SWOP, 상대색도)로 뽑아 `CMYK` 표에
박아 두었다. 자동 변환에 맡기지 않는 까닭은 인쇄소마다 결과가 달라지기 때문이다.
비즈하우스는 "한 색상값이 20 이상 차이나야 서로 다른 색으로 출력된다"고 하는데,
시안의 금색 두 톤은 CMYK로 Y가 7밖에 안 벌어져 같은 색으로 찍힌다. 그래서 하나로
합쳤다.

## 설치

```
claude plugin marketplace add https://github.com/tom-heo-biik/surisomath.git
claude plugin install biik@surisomath
```
