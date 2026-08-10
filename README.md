# surisomath

수리소 수학학원(SURISO MATH ACADEMY)의 Claude Code 플러그인.

## 스킬

### surisomath-a4

수리소 표준 문서 양식. A4 세로 595×842pt, 22pt 베이스라인 그리드, KoPubWorld 바탕체.
HTML로 쓰고 WeasyPrint로 PDF를 뽑는다.

```
skills/surisomath-a4/
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

python skills/surisomath-a4/templates/render.py 문서.html --check
```

`--check`는 렌더한 PDF의 모든 글줄이 22pt 그리드 위에 있는지 실제로 재서 알려 준다.

## 서체

KoPubWorld 바탕체를 저장소에 담아 두었다. 스킬은 `templates/fonts/`를 직접 읽으므로
새 PC에 플러그인만 깔아도 서체가 바로 박힌다. 따로 설치할 일이 없다.

한글·워드·파워포인트처럼 OS에 깔린 서체만 쓰는 프로그램에서 같은 서체를 쓰려면
그때만 설치한다. 관리자 권한이 필요 없다.

```
python lib/install_fonts.py           # 설치
python lib/install_fonts.py --check   # 설치 여부 확인
```

설치하면 서체 이름은 `KoPubWorldBatang_Pro`로 뜬다.

서체 저작권은 문화체육관광부와 한국출판인회의에 있다. 무료로 재배포할 수 있고,
배포할 때 약관을 함께 담아야 한다(`templates/fonts/LICENSE.md`).

## 브랜드 자산

```
assets/          로고 PNG 4종 — 심볼, 한글·영문·전체 워드마크
lib/suriso.py    자산 경로·색·인쇄 규격 상수
자료/             확정 인쇄물 PDF (문제집 표지, 배너, 숙제 라벨)
```

빌드 스크립트는 절대 경로를 박지 말고 `lib/suriso.py`에서 가져다 쓴다.
어느 PC에 설치되든 자기 위치를 기준으로 자산을 찾는다.

```
python lib/suriso.py       # 자산이 다 있는지 점검
```

브랜드 톤은 **순흑백 모노라인**이다. 검정 단색만 쓰고 회색 틴트를 쓰지 않는다.

## 설치

```
claude plugin marketplace add https://github.com/tom-heo-biik/surisomath.git
claude plugin install biik@surisomath
```
