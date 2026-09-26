# 정본 대조본

책의 문장과 정본의 문장을 나란히 둔 자료다. 책은 사진 속 문항(문제집)의 글을 그대로 옮긴 것이고, 정본은 선생님이 확정해 봉인한 문장이다(단원 폴더의 sealed.json). 퇴고할 때 같은 꼴의 문장은 여기 정본을 본뜬다. SKILL.md의 규칙과 정본이 어긋나면 정본이 이긴다.

- 책과 정본은 problems.yaml과 같은 코드 수준으로 적는다. 정본은 yaml의 text를 한 글자도 바꾸지 않고 옮긴 것이라 그대로 복사해 쓸 수 있다. 책은 책의 표기(`$\angle x$`, `$\sin x$`, 띄어 쓴 단위 "6 cm", "오른쪽 그림")를 같은 코드 수준으로 옮긴 것이다.
- 지문만 적는다. 선지와 답은 책과 같다. 이차함수 001만 선생님이 선지를 빼 서술형으로 바꿨다.
- 책의 딱지("도전 문제", "대표문제", "앗! 실수")는 책 문장 앞에 [ ]로 적는다. 정본에는 없다.
- 문항을 봉인하면 여기 쌍을 더한다. 책은 사진에서, 정본은 problems.yaml에서 옮긴다.


## 원과직선

### 001

#### 책

```
다음 그림과 같이 두 원 $\mathrm{O}$, $\mathrm{O}'$이 각각 두 사각형 $\mathrm{ABCD}$, $\mathrm{CEFD}$에 내접할 때, $\overline{\mathrm{EF}}-\overline{\mathrm{AB}}$의 값은?
```

#### 정본

```
그림과 같이 두 원 $\mathrm{O}$, $\mathrm{O}'$은 각각 두 사각형 $\mathrm{ABCD}$, $\mathrm{CEFD}$에 내접한다. $\overline{\mathrm{AD}}=8$, $\overline{\mathrm{DF}}=5$, $\overline{\mathrm{BC}}=6$, $\overline{\mathrm{CE}}=12$일 때, $\overline{\mathrm{EF}}-\overline{\mathrm{AB}}$의 값은?
```

#### 바뀐 것

"…에 내접할 때, …은?" 한 문장을 진술("…에 내접한다.")과 조건("…일 때")으로 가른다. 주어는 화제 "두 원 O, O'은". 그림에만 있던 네 길이를 지문에 채웠다.

### 002

#### 책

```
오른쪽 그림과 같은 원에서 서로 수직인 두 현 $\mathrm{AB}$, $\mathrm{CD}$가 만나는 점을 $\mathrm{E}$라 하자. $\overline{\mathrm{AE}}=5$, $\overline{\mathrm{EB}}=9$, $\overline{\mathrm{CD}}=16$일 때, 이 원의 넓이는?
```

#### 정본

```
그림과 같이 원의 두 현 $\mathrm{AB}$, $\mathrm{CD}$는 점 $\mathrm{E}$에서 서로 수직으로 만난다. $\overline{\mathrm{AE}}=5$, $\overline{\mathrm{EB}}=9$, $\overline{\mathrm{CD}}=16$일 때, 이 원의 넓이는?
```

#### 바뀐 것

"오른쪽 그림과 같은 원에서" → "그림과 같이 원의". 정의문 "만나는 점을 E라 하자"를 화제 주어의 진술 "두 현 AB, CD는 점 E에서 서로 수직으로 만난다"로(선생님).

### 003

#### 책

```
오른쪽 그림과 같이 원 $\mathrm{O}$의 세 현 $\mathrm{AB}$, $\mathrm{CD}$, $\mathrm{EF}$가 같은 간격으로 서로 평행하게 있다. $\overline{\mathrm{AB}}=6$ cm, $\overline{\mathrm{CD}}=8$ cm, $\overline{\mathrm{EF}}=2\sqrt{21}$ cm일 때, 원 $\mathrm{O}$의 둘레의 길이를 구하시오.
```

#### 정본

```
그림과 같이 원 $\mathrm{O}$의 세 현 $\mathrm{AB}$, $\mathrm{CD}$, $\mathrm{EF}$는 서로 평행하고, 이웃한 두 현 사이의 거리가 같다. $\overline{\mathrm{AB}}=6$cm, $\overline{\mathrm{CD}}=8$cm, $\overline{\mathrm{EF}}=2\sqrt{21}$cm일 때, 원 $\mathrm{O}$의 둘레의 길이를 구하시오.
```

#### 바뀐 것

"같은 간격으로 서로 평행하게 있다" → "서로 평행하고, 이웃한 두 현 사이의 거리가 같다"(선생님이 정한 문장. "서로"는 셋이 다 평행한 쪽에만 쓴다). 주어는 "세 현 …는". 단위는 붙여 쓴다.

### 004

#### 책

```
다음 그림과 같이 중심이 점 $\mathrm{O}$로 일치하고 반지름의 길이가 각각 8, 6인 두 원이 있다. 큰 원의 현 $\mathrm{AC}$가 작은 원에 접하고 $\overline{\mathrm{OC}}\perp\overline{\mathrm{AB}}$일 때, 큰 원의 현 $\mathrm{AB}$의 길이를 구하시오.
```

#### 정본

```
그림과 같이 점 $\mathrm{O}$를 중심으로 하는 두 원 $\mathrm{C}_1$, $\mathrm{C}_2$가 있다. 원 $\mathrm{C}_1$의 두 현 $\mathrm{AB}$, $\mathrm{AC}$에 대하여 현 $\mathrm{AC}$는 원 $\mathrm{C}_2$에 접하고 $\overline{\mathrm{OC}}\perp\overline{\mathrm{AB}}$이다. 두 원 $\mathrm{C}_1$, $\mathrm{C}_2$의 반지름의 길이가 각각 8, 6일 때, 선분 $\mathrm{AB}$의 길이를 구하시오.
```

#### 바뀐 것

"중심이 점 O로 일치하고" → "점 O를 중심으로 하는". "큰 원", "작은 원"은 설명이지 이름이 아니라 C₁, C₂로 부른다(선생님). 그림에 없는 반지름 8, 6은 "…인" 절에서 "…일 때" 절로(선생님). "큰 원의 현 AB의 길이" → "선분 AB의 길이".

### 005

#### 책

```
[앗! 실수] 다음 그림과 같이 반지름의 길이가 10인 원의 중심 $\mathrm{O}$로부터의 거리가 6인 점 $\mathrm{P}$가 있다. 이때, 점 $\mathrm{P}$를 지나고 길이가 정수인 현의 개수는?
```

#### 정본

```
그림과 같이 반지름의 길이가 10인 원 $\mathrm{C}$의 중심 $\mathrm{O}$와 점 $\mathrm{P}$는 $\overline{\mathrm{OP}}=6$을 만족시킨다. 점 $\mathrm{P}$를 지나고 길이가 자연수인 원 $\mathrm{C}$의 현의 개수는?
```

#### 바뀐 것

원에 이름 C를 주어 중심 O와 가른다("점 O"가 원 위의 점으로 읽히지 않게, 선생님 지적). "중심 O로부터의 거리가 6인 점 P가 있다" → "중심 O와 점 P는 OP = 6을 만족시킨다". "이때," 걷어냄. 길이는 양수라 "정수" → "자연수".

### 006

#### 책

```
[도전 문제] 다음 그림과 같이 반지름의 길이가 $\sqrt{13}$인 원의 두 현 $\mathrm{AB}$, $\mathrm{CD}$에 대하여 점 $\mathrm{A}$에서 현 $\mathrm{CD}$에 내린 수선의 발을 $\mathrm{H}$라 하자. $\overline{\mathrm{AB}}:\overline{\mathrm{CD}}=1:\sqrt{3}$이고 $\angle\mathrm{BAH}=90^{\circ}$, $\overline{\mathrm{AH}}=4$일 때, $\overline{\mathrm{BH}}$의 길이는?
```

#### 정본

```
그림과 같이 원 $\mathrm{O}$의 두 현 $\mathrm{AB}$, $\mathrm{CD}$에 대하여 점 $\mathrm{A}$에서 현 $\mathrm{CD}$에 내린 수선의 발을 $\mathrm{H}$라 하자. 원 $\mathrm{O}$의 반지름의 길이가 $\sqrt{13}$이고 $\overline{\mathrm{AB}}:\overline{\mathrm{CD}}=1:\sqrt{3}$, $\angle\mathrm{BAH}=90^{\circ}$, $\overline{\mathrm{AH}}=4$일 때, 선분 $\mathrm{BH}$의 길이는?
```

#### 바뀐 것

원에 이름 O. 그림에 없는 반지름 √13을 "…인" 절에서 조건 절로("반지름의 길이가 √13이고 …"). 물음의 기호 `$\overline{\mathrm{BH}}$` → 낱말 "선분 BH"(도형은 낱말).

### 007

#### 책

```
[대표문제] 오른쪽 그림과 같이 반지름의 길이가 4인 원 $\mathrm{O}$의 중심에서 두 현 $\mathrm{AB}$, $\mathrm{AC}$에 내린 수선의 발을 각각 $\mathrm{H}$, $\mathrm{I}$라 하자. $\overline{\mathrm{OH}}=\overline{\mathrm{OI}}$, $\overset{\frown}{\mathrm{AB}}:\overset{\frown}{\mathrm{BC}}=5:2$일 때, 삼각형 $\mathrm{ACB}$의 넓이는?
```

#### 정본

```
그림과 같이 원 $\mathrm{C}$의 중심 $\mathrm{O}$에서 두 현 $\mathrm{PQ}$, $\mathrm{PR}$에 내린 수선의 발을 각각 $\mathrm{H}$, $\mathrm{I}$라 하자. 원 $\mathrm{C}$의 반지름의 길이는 4이고 $\overline{\mathrm{OH}}=\overline{\mathrm{OI}}$, $\overset{\frown}{\mathrm{PQ}}:\overset{\frown}{\mathrm{QR}}=5:2$일 때, 삼각형 $\mathrm{PQR}$의 넓이는?
```

#### 바뀐 것

"원 O의 중심에서" → "원 C의 중심 O에서"(원과 중심을 가른다). 꼭짓점 C가 원 C와 겹쳐 A, B, C → P, Q, R(선생님 "C 말고 다른 기호가 없으면 A, B, C를 바꿔"). 반지름 4는 조건 절로("길이는 4이고"). "삼각형 ACB" → "삼각형 PQR".


## 이차함수

### 001

#### 책

```
이차함수 $f(x)$에 대하여 $x$의 값에 관계없이 $f(x+1)-f(x-1)=4x+2$가 성립하고, $f(0)=1$일 때, $f(4)$의 값은?
① $13$ ② $15$ ③ $17$ ④ $19$ ⑤ $21$
```

#### 정본

```
이차함수 $f(x)$가 다음 조건을 만족시킨다.
(가) $f(0)=1$
(나) 모든 실수 $x$에 대하여 $f(x+1)-f(x-1)=4x+2$이다.
$f(4)$의 값을 구하시오.
```

#### 바뀐 것

선생님이 선지를 빼고 조건 상자 (가) (나)의 서술형으로 바꿨다(답 21). yaml에서는 첫 줄이 text, (가) (나)가 conditions, 마지막 줄이 after다. "x의 값에 관계없이" → "모든 실수 x에 대하여". 상자의 여는 말 "…가 다음 조건을 만족시킨다."는 평가원 정형구다. 풀이도 봉인되어 있다(problems.yaml의 solution, 풀이 문체의 정본).

### 002

#### 책

```
오른쪽 그림과 같이 직선 $l$이 이차함수 $y=\dfrac{1}{4}x^2$의 그래프 및 $y$축과 각각 두 점 $\mathrm{A}$, $\mathrm{B}$와 점 $\mathrm{C}$에서 만난다. 점 $\mathrm{C}$가 직선 $y=1$ 위에 있고 $\overline{\mathrm{AC}}:\overline{\mathrm{CB}}=1:4$일 때, 직선 $l$의 기울기는?
```

#### 정본

```
그림과 같이 직선 $l$은 이차함수 $y=\dfrac{1}{4}x^2$의 그래프와 두 점 $\mathrm{A}$, $\mathrm{B}$에서 만나고 $y$축과 점 $\mathrm{C}$에서 만난다. 점 $\mathrm{C}$의 $y$좌표가 1이고 $\overline{\mathrm{AC}}:\overline{\mathrm{CB}}=1:4$일 때, 직선 $l$의 기울기는? (단, $\mathrm{O}$는 원점이다.)
```

#### 바뀐 것

"및 … 각각 …"으로 묶은 것을 "…와 두 점 A, B에서 만나고 y축과 점 C에서 만난다"로 푼다. 주어는 화제 "직선 l은". "직선 y = 1 위에 있고" → "y좌표가 1이고". 그림에 원점 O가 있어 단서를 붙였다.

### 019

#### 책

```
$x^2$의 계수가 1인 세 이차함수 $y=f(x)$, $y=g(x)$, $y=h(x)$의 그래프가 다음 그림과 같이 점 $(1,\,0)$에서 만난다. 이차함수 $y=f(x)+g(x)+h(x)$의 그래프의 꼭짓점의 좌표를 구하시오.
```

#### 정본

```
그림과 같이 최고차항의 계수가 1인 세 이차함수 $y=f(x)$, $y=g(x)$, $y=h(x)$의 그래프는 모두 점 $(1,\,0)$을 지나고, $x$축과 만나는 다른 한 점의 $x$좌표가 각각 2, 3, 4이다. 함수 $y=f(x)+g(x)+h(x)$의 그래프의 꼭짓점의 좌표를 구하시오. (단, $\mathrm{O}$는 원점이다.)
```

#### 바뀐 것

"x²의 계수가 1인" → "최고차항의 계수가 1인"(평가원 말). "점 (1, 0)에서 만난다" → "모두 점 (1, 0)을 지나고". 그림에만 있던 x절편 2, 3, 4를 지문에. 물음의 "이차함수 y = …" → "함수 y = …"(이차함수라는 것이 힌트가 된다). 단서 "(단, O는 원점이다.)".

### 020

#### 책

```
[도전 문제] 다음 그림과 같이 폭이 서로 같은 두 이차함수 $f(x)=x^2$, $g(x)=ax^2+bx+c$의 그래프가 두 점 $\mathrm{O}(0,\,0)$, $\mathrm{A}$에서 만나고, 점 $\mathrm{A}$는 이차함수 $y=g(x)$의 그래프의 꼭짓점이다. $x$축에 평행한 직선이 두 이차함수의 그래프와 만나는 네 점을 각각 $\mathrm{P}$, $\mathrm{Q}$, $\mathrm{R}$, $\mathrm{S}$라 하면 $\overline{\mathrm{PR}}=2$, $\overline{\mathrm{QS}}=2\sqrt{3}$일 때, $a+b+c$의 값을 구하시오. (단, 점 $\mathrm{A}$는 제1사분면 위에 있고, $a$, $b$, $c$는 상수이다.)
```

#### 정본

```
그림과 같이 두 이차함수 $f(x)=x^2$, $g(x)=ax^2+bx+c$의 그래프는 원점 $\mathrm{O}$와 점 $\mathrm{A}$에서 만나고, 점 $\mathrm{A}$는 이차함수 $y=g(x)$의 그래프의 꼭짓점이다. 직선 $y=k$가 두 이차함수의 그래프와 만나는 점의 $x$좌표를 작은 것부터 차례로 $x_1$, $x_2$, …, $x_n$이라 하자. $x_3-x_1=2$, $x_4-x_2=2\sqrt{3}$일 때, $a+b+c$의 값을 구하시오. (단, 점 $\mathrm{A}$는 제1사분면 위에 있고, $a$, $b$, $c$, $k$는 상수이다.)
```

#### 바뀐 것

"폭이 서로 같은"은 답에서 저절로 나오는 것이라 뺐다. "두 점 O(0, 0), A" → "원점 O와 점 A". "x축에 평행한 직선이 … 네 점을 각각 P, Q, R, S라 하면 PR = 2, QS = 2√3일 때" → "직선 y = k가 … 점의 x좌표를 작은 것부터 차례로 x₁, x₂, …, xₙ이라 하자. x₃ − x₁ = 2, x₄ − x₂ = 2√3일 때"(정의는 "라 하자", 조건은 "일 때". 개수를 말하지 않고 열어 두어 x₄가 네 점을 끌어낸다. 선생님이 정한 꼴). 단서에 k를 더했다. 그림에는 직선 y = k가 없다.


## 삼각비

### 002

#### 책

```
오른쪽 그림과 같이 직사각형 모양의 색종이 $\mathrm{ABCD}$를 $\overline{\mathrm{RQ}}$를 접는 선으로 하여 점 $\mathrm{D}$가 점 $\mathrm{B}$에 오도록 접었다. $\overline{\mathrm{AB}}=4$ cm, $\overline{\mathrm{AD}}=8$ cm이고 $\angle\mathrm{BRQ}=\angle x$라 할 때, $\sin x$의 값은?
```

#### 정본

```
그림과 같이 $\overline{\mathrm{AB}}=4$cm, $\overline{\mathrm{AD}}=8$cm인 직사각형 $\mathrm{ABCD}$ 모양의 종이를 점 $\mathrm{D}$가 점 $\mathrm{B}$에 오도록 접었다. 접는 선이 두 변 $\mathrm{AD}$, $\mathrm{BC}$와 만나는 점을 각각 $\mathrm{R}$, $\mathrm{Q}$라 하고, 점 $\mathrm{C}$가 옮겨진 점을 $\mathrm{P}$라 하자. $\angle\mathrm{BRQ}=\theta^{\circ}$라 할 때, $\sin\theta^{\circ}$의 값은?
```

#### 바뀐 것

그림에 있는 두 길이를 "…인 직사각형"에 얹는다. "색종이 ABCD" → "직사각형 ABCD 모양의 종이". 접는 선 RQ를 먼저 잡던 것을 접는 조건 뒤에 "접는 선이 두 변 AD, BC와 만나는 점을 각각 R, Q"로 정의한다(원인 → 결과, 선생님이 고른 쪽). 그림에만 있던 P를 지문에. `$\angle x$` → `$\theta^{\circ}$`.

### 003

#### 책

```
[Step 2 A등급을 위한 문제] 오른쪽 그림의 두 직각삼각형 $\mathrm{ABC}$, $\mathrm{ADE}$에서 점 $\mathrm{B}$는 $\overline{\mathrm{CD}}$ 위의 점이고 $\angle\mathrm{ACB}=\angle\mathrm{AED}=90^{\circ}$, $\overline{\mathrm{BC}}=\overline{\mathrm{BD}}=6$이다. $\angle\mathrm{BAC}=\angle x$, $\angle\mathrm{DAE}=\angle y$, $\sin x=\dfrac{1}{3}$일 때, $\cos y$의 값을 구하시오.
```

#### 정본

```
그림과 같이 $\angle\mathrm{C}=90^{\circ}$인 직각삼각형 $\mathrm{ABC}$가 있다. 변 $\mathrm{BC}$의 중점을 $\mathrm{D}$라 하고, $\angle\mathrm{DAC}=\theta_1^{\circ}$, $\angle\mathrm{BAD}=\theta_2^{\circ}$라 하자. $\sin\theta_1^{\circ}=\dfrac{1}{3}$일 때, $\cos\theta_2^{\circ}$의 값을 구하시오.
```

#### 바뀐 것

선생님이 짜임을 새로 정했다. 큰 직각삼각형을 ABC로 두고(책의 B와 D를 맞바꿈) D를 변 BC의 중점으로. 푸는 도구인 점 E(B에서 AD에 내린 수선의 발)와 답에 안 쓰이는 6을 뺐다. 존재문 "…가 있다" → "…라 하고, …라 하자" → "…일 때" → 물음. 그림에서도 E, 수선, 6을 뺐다.

### 004

#### 책

```
오른쪽 그림과 같이 좌표평면 위의 세 점 $\mathrm{A}(6,\,6)$, $\mathrm{B}(-2,\,2)$, $\mathrm{C}(2,\,{-1})$에 대하여 $\angle\mathrm{ABC}=\angle x$라 할 때, $\sin x+\cos x$의 값은?
```

#### 정본

```
그림과 같이 좌표평면 위의 세 점 $\mathrm{A}(6,\,6)$, $\mathrm{B}(-2,\,2)$, $\mathrm{C}(2,\,{-1})$에 대하여 $\angle\mathrm{ABC}=\theta^{\circ}$라 할 때, $\sin\theta^{\circ}+\cos\theta^{\circ}$의 값은? (단, $\mathrm{O}$는 원점이다.)
```

#### 바뀐 것

"오른쪽 그림과 같이" → "그림과 같이". `$\angle x$` → `$\theta^{\circ}$`. 그림에 원점 O가 있어 단서를 붙였다. 좌표 세 점은 "…에 대하여"로 받는다.

### 005

#### 책

```
[도전 문제] 다음 그림과 같이 $\overline{\mathrm{AC}}=\sqrt{2}$인 직각삼각형 $\mathrm{ABC}$에서 $\overline{\mathrm{BD}}=\overline{\mathrm{DE}}=\overline{\mathrm{EF}}=\overline{\mathrm{FC}}=1$이 되도록 변 $\mathrm{BC}$ 위에 세 점 $\mathrm{D}$, $\mathrm{E}$, $\mathrm{F}$를 정하였다. $\angle\mathrm{ABD}=\angle x$, $\angle\mathrm{AEF}=\angle y$라 할 때, $\tan(x+y)$의 값을 구하시오.
```

#### 정본

```
그림과 같이 $\angle\mathrm{C}=90^{\circ}$, $\overline{\mathrm{AC}}=\sqrt{2}$, $\overline{\mathrm{BC}}=4$인 직각삼각형 $\mathrm{ABC}$에서 변 $\mathrm{BC}$ 위의 세 점 $\mathrm{D}$, $\mathrm{E}$, $\mathrm{F}$에 대하여 $\overline{\mathrm{BD}}=\overline{\mathrm{DE}}=\overline{\mathrm{EF}}=\overline{\mathrm{FC}}$이다. $\angle\mathrm{ABD}=\theta_1^{\circ}$, $\angle\mathrm{AEF}=\theta_2^{\circ}$라 할 때, $\tan(\theta_1+\theta_2)^{\circ}$의 값을 구하시오.
```

#### 바뀐 것

그림으로만 주던 직각 ∠C = 90°를 지문에. "= 1" 대신 BC = 4를 삼각형의 정의에 넣고 네 등식은 같은 길이라는 관계만 남겼다(선생님 결정. 그림도 FC의 1 대신 BC에 4). "…이 되도록 … 정하였다" → "변 BC 위의 세 점 D, E, F에 대하여 …이다". `$\angle x$`, `$\angle y$` → `$\theta_1^{\circ}$`, `$\theta_2^{\circ}$`. `$\tan(x+y)$` → `$\tan(\theta_1+\theta_2)^{\circ}$`.

### 012

#### 책

```
다음 그림과 같이 $\angle\mathrm{B}=\angle\mathrm{D}=90^{\circ}$, $\overline{\mathrm{AD}}=6$, $\overline{\mathrm{CD}}=12$인 사각형 $\mathrm{ABCD}$의 꼭짓점 $\mathrm{D}$에서 변 $\mathrm{BC}$에 내린 수선의 발을 $\mathrm{H}$라 하자. $\overline{\mathrm{AC}}$는 $\angle\mathrm{C}$의 이등분선이고 $\overline{\mathrm{AC}}$, $\overline{\mathrm{DH}}$의 교점을 $\mathrm{E}$라 하자. $\angle\mathrm{CDH}=\angle x$라 할 때, $\sin x$의 값을 구하시오.
```

#### 정본

```
그림과 같이 $\angle\mathrm{B}=\angle\mathrm{D}=90^{\circ}$, $\overline{\mathrm{AD}}=6$, $\overline{\mathrm{CD}}=12$인 사각형 $\mathrm{ABCD}$에서 선분 $\mathrm{AC}$는 각 $\mathrm{C}$의 이등분선이다. 꼭짓점 $\mathrm{D}$에서 변 $\mathrm{BC}$에 내린 수선의 발을 $\mathrm{H}$, 선분 $\mathrm{AC}$와 선분 $\mathrm{DH}$의 교점을 $\mathrm{E}$라 하자. $\angle\mathrm{CDH}=\theta^{\circ}$라 할 때, $\sin\theta^{\circ}$의 값을 구하시오.
```

#### 바뀐 것

사각형의 조건(선분 AC는 각 C의 이등분선)을 사각형에 먼저 두고, 점 H와 E의 정의를 한 문장에. 기호 `$\overline{\mathrm{AC}}$`, `$\angle\mathrm{C}$`는 길이와 크기라 도형을 가리킬 땐 낱말 "선분 AC", "각 C". "AC, DH의 교점" → "선분 AC와 선분 DH의 교점"(교점은 하나씩 부른다, 선생님). `$\angle x$` → `$\theta^{\circ}$`.
