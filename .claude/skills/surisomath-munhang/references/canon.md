# 정본 대조본


## 쓰임


### 자료


#### 책과 정본
책의 문장과 정본의 문장을 나란히 둔 자료입니다. 책은 사진 속 문항의 글을 그대로 옮긴 것이고, 정본은 선생님이 확정해 봉인한 문장입니다. 봉인 목록은 단원 폴더의 sealed.json에 있고 문항의 글이 바뀌면 빌드가 멈춥니다. 퇴고 전에 이 문서를 처음부터 끝까지 다 읽고 같은 꼴의 문장은 정본을 본뜹니다. 규칙과 정본이 어긋나면 정본이 이기고 규칙을 고칩니다. 봉인하면 여기에 쌍을 더해 같은 커밋에 넣습니다. 세 단원 원과직선, 이차함수, 삼각비의 문항입니다.


### 표기


#### 코드 수준
책과 정본은 problems.yaml과 같은 코드 수준으로 적습니다. 정본은 yaml의 text를 한 글자도 바꾸지 않고 옮긴 것이라 그대로 복사해 쓸 수 있고, 기계로 대조해 어긋남이 없음을 확인합니다. 책은 책의 표기를 같은 코드 수준으로 옮긴 것입니다. 딱지는 책 문장 앞에 대괄호로 적고 정본에는 없습니다. 지문만 적으며 선지와 답은 책과 같습니다. 조건 상자는 (가) (나)를 한 줄씩 따로 폅니다. 이차함수 001만 선생님이 선지를 빼 서술형으로 바꿨습니다.


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
한 문장이던 것을 진술과 조건으로 갈랐습니다. "…에 내접할 때, …은?"이 "…에 내접한다."와 "…일 때"가 되었고, 주어는 화제인 "두 원 O, O'은"으로 세웠습니다. 책이 그림에만 적어 두던 네 길이 AD = 8, DF = 5, BC = 6, CE = 12를 지문에 채워 그림 없이도 조건이 서게 했습니다. "다음 그림과 같이"는 "그림과 같이"로 열었고 물음과 선지와 답은 그대로입니다. 두 원이 사각형에 내접한다는 진술로 여는 이 꼴은 원과직선 정본의 본보기입니다.


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
"오른쪽 그림과 같은 원에서"를 "그림과 같이 원의"로 열었습니다. 책의 정의문 "만나는 점을 E라 하자"를 화제 주어의 진술 "두 현 AB, CD는 점 E에서 서로 수직으로 만난다"로 바꿨습니다. 선생님이 정한 문장입니다. 세 길이와 물음은 책 그대로이고, 원에 이름을 주지 않은 것도 책을 따랐습니다. 수직은 서술이라 낱말로 쓰고 기호 ⊥는 식 안에서만 씁니다. 이름이 없는 원은 "이 원"으로 받습니다. 정의보다 진술로 여는 것이 평가원의 결이라 다른 문항도 본뜹니다.


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
"같은 간격으로 서로 평행하게 있다"를 "서로 평행하고, 이웃한 두 현 사이의 거리가 같다"로 바꿨습니다. 선생님이 정한 문장입니다. "서로"는 셋이 다 평행한 쪽에만 쓰고, 거리는 이웃한 두 현 사이만 같으니 "서로 같다"라 하지 않습니다. 되풀이를 피하려고 뺀 것이 아니라 뜻으로 가른 것입니다. 주어는 "세 현 …는"으로 세웠고 뒤따르는 새 사실은 "거리가"로 받았습니다. 이 쉼표는 잘못 읽히지 않게 둔 것입니다. 단위는 6cm처럼 붙여 썼고 물음은 그대로입니다.


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
"중심이 점 O로 일치하고"를 "점 O를 중심으로 하는"으로 바꿨습니다. 큰 원과 작은 원은 설명이지 이름이 아니라 C₁, C₂로 부르고 그림에도 이름을 넣었습니다. 그림에 없는 반지름 8, 6은 "…인" 절에서 "…일 때" 절로 내렸습니다. 거기 두면 그림이 거짓이 되기 때문입니다. 둘 다 선생님이 잡은 규칙입니다. 물음의 "큰 원의 현 AB의 길이"는 "선분 AB의 길이"로 하여 도형을 낱말로 불렀고, 기호 ⊥가 든 식은 그대로 두었습니다. 물음의 꼴은 그대로입니다.


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
원에 이름 C를 주어 중심 O와 갈랐습니다. "점 O"가 원 위의 점으로 읽힌다는 선생님 지적 때문입니다. "중심 O로부터의 거리가 6인 점 P가 있다"는 "중심 O와 점 P는 OP = 6을 만족시킨다"로, 정의 대신 진술로 세웠습니다. "…는 …을 만족시킨다"도 진술을 여는 평가원의 꼴입니다. "이때,"는 걷어냈고, 길이는 양수이니 "정수"를 "자연수"로 고쳤습니다. C는 그림에도 둡니다. 딱지 "앗! 실수"도 뺐고 현의 개수를 묻는 물음과 선지는 그대로입니다.


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
원에 이름 O를 주어 불렀습니다. 그림에 없는 반지름 √13은 "…인" 절에서 조건 절 "반지름의 길이가 √13이고"로 내렸습니다. "…이고 …, …일 때"로 이어지던 조건은 쉼표로 나란히 두었습니다. 물음의 기호 `$\overline{\mathrm{BH}}$`는 길이가 아니라 도형 자체를 가리키므로 낱말 "선분 BH"로 바꿨습니다. 수선의 발 H를 "라 하자"로 정의하고 조건을 "일 때"에 두는 흐름은 책과 같습니다. 딱지 "도전 문제"를 뺐습니다.


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
"원 O의 중심에서"를 "원 C의 중심 O에서"로 바꿔 원과 중심의 이름을 갈랐습니다. 꼭짓점 C가 원 C와 겹치므로 A, B, C를 P, Q, R로 바꿨습니다. 선생님이 "C 말고 다른 기호가 없으면 A, B, C를 바꿔"라 하셨습니다. 그림의 점 이름도 함께 바꿨습니다. 반지름 4는 조건 절 "길이는 4이고"로 내렸고, "삼각형 ACB"는 "삼각형 PQR"이 되었습니다. 호의 비는 기호 표기 그대로입니다. 딱지 "대표문제"를 뺐고 다섯 선지와 답은 책 그대로입니다.


### 008


#### 책
```
오른쪽 그림은 가로, 세로의 길이가 각각 10, 6인 직사각형 $\mathrm{ABCD}$의 내부에 점 $\mathrm{C}$를 중심으로 하고 $\overline{\mathrm{CD}}$를 반지름으로 하는 사분원을 그린 것이다. 점 $\mathrm{B}$에서 사분원에 그은 접선이 변 $\mathrm{AD}$와 만나는 점을 $\mathrm{E}$라 할 때, $\overline{\mathrm{AE}}$의 길이는?
```


#### 정본
```
그림과 같이 $\overline{\mathrm{OA}}=6$, $\overline{\mathrm{OC}}=10$인 직사각형 $\mathrm{OABC}$와 부채꼴 $\mathrm{OAD}$가 있다. 변 $\mathrm{AB}$ 위의 점 $\mathrm{E}$에 대하여 선분 $\mathrm{CE}$가 호 $\mathrm{AD}$에 접할 때, 선분 $\mathrm{BE}$의 길이는?
```


#### 바뀐 것
선생님이 짜임을 정했습니다. 그림을 180° 돌려 부채꼴 중심을 O로 두고 직사각형을 OABC, 호의 다른 끝을 변 OC 위의 D라 하여 "직사각형 OABC와 부채꼴 OAD가 있다"로 열었습니다(삼각비 006 꼴). "점 B에서 사분원에 그은 접선이 변 AD와 만나는 점을 E"는 "변 AB 위의 점 E에 대하여 선분 CE가 호 AD에 접할 때"로 했습니다. 옛 A, B, C, D, E는 새 B, C, O, A, E이고 책의 AE는 새 BE라 물음은 "선분 BE의 길이는?"입니다.


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
선생님이 선지를 빼고 조건 상자 (가) (나)의 서술형으로 바꿨습니다. 답은 21이고 값으로만 적습니다. yaml에서는 첫 줄이 text이고, (가) (나)가 conditions, 마지막 줄이 after입니다. "x의 값에 관계없이"는 "모든 실수 x에 대하여"로 썼고, 여는 말 "…가 다음 조건을 만족시킨다."는 평가원의 정형구라 그대로 둡니다. 어느 문항을 상자로 할지는 선생님이 정합니다. 풀이도 함께 봉인되어 있어 풀이 문체의 정본이기도 합니다.


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
"및 … 각각 …"으로 묶은 것을 "…와 두 점 A, B에서 만나고 y축과 점 C에서 만난다"로 풀었습니다. 주어는 화제 "직선 l은"이고, 직선이 만나는 것은 함수가 아니라 그래프입니다. 직선을 주어로 세운 진술이 점 C까지 세워 줍니다. "직선 y = 1 위에 있고"는 "y좌표가 1이고"로 바꿨습니다. 그림에 원점 O가 있어 단서 "(단, O는 원점이다.)"를 붙였습니다. 단서는 마침표를 찍어 문장 끝에 둡니다. 비 1 : 4와 기울기를 묻는 물음과 선지는 그대로입니다.


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
"x²의 계수가 1인"을 평가원 말 "최고차항의 계수가 1인"으로 바꿨습니다. "점 (1, 0)에서 만난다"는 "모두 점 (1, 0)을 지나고"로 하고, 그림에만 있던 x절편 2, 3, 4를 지문에 채웠습니다. 이 셋이 없으면 세 함수가 하나로 정해지지 않습니다. 물음의 "이차함수 y = …"는 "함수 y = …"로 하여 이차함수라는 힌트를 지운 것입니다. 그림에 원점 O가 있어 단서를 붙였습니다. "다음 그림과 같이"는 첫머리의 "그림과 같이"로 옮겨 두었습니다.


### 019


#### 책
```
[앗! 실수] 오른쪽 그림과 같이 $\angle\mathrm{B}=90^{\circ}$, $\angle\mathrm{CAB}=30^{\circ}$, $\overline{\mathrm{BC}}=4$인 직각삼각형 $\mathrm{ABC}$의 빗변 $\mathrm{AC}$ 위를 움직이는 점 $\mathrm{P}$에 대하여 $\overline{\mathrm{AP}}^2+\overline{\mathrm{BP}}^2$의 최솟값을 구하시오.
```


#### 정본
```
그림과 같이 $\angle\mathrm{B}=90^{\circ}$, $\angle\mathrm{A}=30^{\circ}$, $\overline{\mathrm{BC}}=4$인 직각삼각형 $\mathrm{ABC}$에서 변 $\mathrm{AC}$ 위의 점 $\mathrm{P}$에 대하여 $\overline{\mathrm{AP}}^2+\overline{\mathrm{BP}}^2$의 최솟값을 구하시오.
```


#### 바뀐 것
"직각삼각형 ABC의 빗변 AC 위를 움직이는 점 P에 대하여"를 "직각삼각형 ABC에서 변 AC 위의 점 P에 대하여"로 바꿨습니다. 005와 024 정본의 "…에서 변 … 위의 점 …에 대하여" 꼴이고 선생님이 정한 문장입니다. "움직이는"은 최솟값이 품는 뜻이라 뺐고 빗변은 변으로 불렀습니다. ∠CAB는 ∠A로 하여 한 글자 각과 세 글자 각을 섞지 않았습니다. "오른쪽 그림과 같이"는 "그림과 같이"로 열고 딱지도 뺐습니다. 그림과 답 30은 책 그대로입니다.


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
"폭이 서로 같은"은 답에서 저절로 나오므로 뺐습니다. "두 점 O(0, 0), A"는 "원점 O와 점 A"로 썼습니다. 네 점을 각각 P, Q, R, S라 하던 것을 "직선 y = k가 … x좌표를 작은 것부터 차례로 x₁, x₂, …, xₙ이라 하자"로 열어 두어 조건의 x₄가 네 점을 끌어내게 했습니다. 정의는 "라 하자"에, 조건은 "일 때"에 두는 흐름입니다. 선생님이 정한 꼴이고 단서에 상수 k를 더했습니다. 그림에는 직선 y = k가 없고 딱지 "도전 문제"를 뺐습니다.


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
그림에 있는 두 길이를 "…인 직사각형"에 얹었고 "색종이 ABCD"는 "직사각형 ABCD 모양의 종이"로 썼습니다. 접는 선 RQ를 먼저 잡던 것을 접는 조건 뒤에 "접는 선이 두 변 AD, BC와 만나는 점을 각각 R, Q"로 정의했습니다. 접는 조건 하나가 접는 선을 정하고 R, Q, P는 그 결과이기 때문입니다. 원인 뒤에 결과를 두는 쪽을 선생님이 골랐습니다. 그림에만 있던 점 P를 지문에 넣고 ∠x는 θ°로 바꿨습니다. 여기 "각각"은 변과 점의 대응이라 맞습니다.


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
선생님이 문항의 짜임을 새로 정했습니다. 큰 직각삼각형을 ABC로 두고 책의 B와 D를 맞바꿔 D를 변 BC의 중점으로 삼았습니다. 푸는 도구인 점 E와 답에 안 쓰이는 수치 6을 뺐습니다. 삼각비는 직각삼각형에서 읽는다는 것이 이 문항의 알맹이라서 수선은 푸는 사람의 몫입니다. 존재문 "…가 있다"로 열고 "…라 하고, …라 하자"로 정의한 뒤 "…일 때"에 조건을 두었습니다. 그림에서도 E와 수선과 직각 표시와 6을 뺐고 ∠x, ∠y는 θ₁°, θ₂°가 되었습니다.


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
"오른쪽 그림과 같이"를 "그림과 같이"로 바꿨습니다. ∠x는 θ°로, sin x + cos x는 sin θ° + cos θ°로 썼습니다. 육십분법이라 문자에도 °를 붙이는 것이 선생님이 정한 규칙입니다. 좌표평면 위의 세 점은 "…에 대하여"로 받는 것이 평가원의 꼴이라서 그대로 두었습니다. 그림에 원점 O가 있어 단서 "(단, O는 원점이다.)"를 붙였습니다. 세 좌표와 선지와 답은 책 그대로이고 둘째 성분이 음수인 좌표 C는 yaml에서 중괄호로 감쌌습니다.


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
그림에만 있던 직각 ∠C = 90°를 지문에 넣었습니다. "= 1" 대신 BC = 4를 삼각형 정의에 얹고 네 등식은 같은 길이란 관계만 남겼습니다. 선생님 결정이라 그림도 FC의 1 대신 BC에 4를 답니다. "…이 되도록 … 정하였다"는 "변 BC 위의 세 점 D, E, F에 대하여 …이다"로 썼고, "직각삼각형 ABC에서"도 선생님이 고른 말입니다. ∠x, ∠y는 θ₁°, θ₂°, tan(x + y)는 tan(θ₁ + θ₂)°입니다. 딱지 "도전 문제"를 뺐습니다.


### 006


#### 책
```
오른쪽 그림과 같이 한 변의 길이가 2인 정사각형 $\mathrm{OABC}$의 한 꼭짓점 $\mathrm{O}$를 중심으로 하고 $\overline{\mathrm{OA}}$를 반지름으로 하는 사분원 $\mathrm{AOC}$가 있다. 정사각형의 두 변 $\mathrm{AB}$, $\mathrm{BC}$ 및 사분원의 호 $\mathrm{AC}$에 접하는 원 $\mathrm{O}'$의 반지름의 길이를 구하시오.
```


#### 정본
```
그림과 같이 $\overline{\mathrm{OA}}=2$인 정사각형 $\mathrm{OABC}$와 부채꼴 $\mathrm{OAC}$에 대하여 두 변 $\mathrm{AB}$, $\mathrm{BC}$와 호 $\mathrm{AC}$에 접하는 원 $\mathrm{O}'$이 있다. 이때 원 $\mathrm{O}'$의 반지름의 길이를 구하시오.
```


#### 바뀐 것
사분원의 정의 문장과 원 O'의 정의를 선생님이 정한 한 문장으로 줄였습니다. 길이 2는 정사각형의 정의에 얹고 사분원은 017처럼 부채꼴 OAC라고만 불렀습니다. 중심과 반지름과 중심각은 정사각형이 정합니다. 존재문과 물음을 갈랐고 "이때"는 선생님이 넣으라 한 말이라 평가원처럼 쉼표 없이 썼습니다(2022학년도 수능 15번). "오른쪽 그림과 같이"는 "그림과 같이"로 열었고 "및"은 "와"로 바꿨습니다. 답 6 − 4√2와 그림은 책 그대로입니다.


### 007


#### 책
```
다음 그림과 같이 $\angle\mathrm{A}=30^{\circ}$, $\angle\mathrm{B}=90^{\circ}$인 직각삼각형 $\mathrm{ABC}$의 빗변 $\mathrm{AC}$ 위에 두 반원 $\mathrm{O}$, $\mathrm{O}'$의 지름이 놓여 있다. 두 반원은 모두 변 $\mathrm{AB}$에 접하면서 서로 외접하고, 반원 $\mathrm{O}'$은 변 $\mathrm{BC}$에 접한다. 두 반원 $\mathrm{O}$, $\mathrm{O}'$의 반지름의 길이를 각각 $r$, $r'$이라 할 때, $\dfrac{r'}{r}$의 값을 구하시오. (단, 두 반원 $\mathrm{O}$, $\mathrm{O}'$과 변 $\mathrm{AB}$의 접점은 각각 $\mathrm{D}$, $\mathrm{E}$이다.)
```


#### 정본
```
그림과 같이 $\angle\mathrm{Q}=90^{\circ}$, $\angle\mathrm{P}=30^{\circ}$인 직각삼각형 $\mathrm{PQR}$이 있다. 두 반원 $\mathrm{C}$, $\mathrm{C}'$은 지름이 빗변 $\mathrm{PR}$ 위에 있고 변 $\mathrm{PQ}$에 접하며 서로 외접한다. 두 반원 $\mathrm{C}$, $\mathrm{C}'$의 반지름의 길이를 각각 $r$, $r'$이라 하자. 반원 $\mathrm{C}$가 변 $\mathrm{QR}$에 접할 때, $\dfrac{r}{r'}$의 값을 구하시오.
```


#### 바뀐 것
선생님이 정본 문장을 직접 썼습니다. 큰 반원이 C, 작은 반원이 C'이고 꼭짓점 C가 겹쳐 삼각형 ABC를 PQR로 바꿨습니다. 두 반원의 공통 조건을 한 문장에 모아 말하고, 반원 C가 변 QR에 접하는 것을 "…일 때" 조건으로 물음에 붙였습니다. 이름이 서로 바뀌어 물음은 r'/r이 r/r'이 되고 답 3은 책 그대로입니다. 접점 D, E와 중심 O, O'은 지문이 부르지 않아 그림에서 뺐고, 반지름 선분은 풀이의 보조선이 되어 r, r'을 빗변 위의 지름에 달았습니다.


### 008


#### 책
```
$0^{\circ}<A<B<90^{\circ}$일 때, 이차방정식 $2x^2-x-1=0$의 한 근이 $\tan B$의 값과 같다. 다음 중 $\sqrt{(\cos A-\sin A)^2}-\sqrt{(\cos A+\sin A)^2}$과 같은 것은?
```


#### 정본
```
이차함수 $f(x)=2x^2-x-1$에 대하여 $f(\tan\theta_0^{\circ})=0$일 때, $\sqrt{(\cos\theta^{\circ}-\sin\theta^{\circ})^2}-\sqrt{(\cos\theta^{\circ}+\sin\theta^{\circ})^2}$을 간단히 한 것은? (단, $0<\theta<\theta_0<90$)
```


#### 바뀐 것
책의 "이차방정식의 한 근이 tan B의 값과 같다"를 선생님 지시로 "이차함수 f(x)에 대하여 f(tan θ₀°) = 0일 때"로 바꿨습니다. 근이 되는 붙박이 각을 θ₀°로 부른 것은 θ₂가 먼저 나오면 어색하고 θ₁이 θ₂보다 큰 것도 이상하다는 선생님 판단이고, 자유로운 각은 θ°입니다. 범위 0 < θ < θ₀ < 90은 물음 뒤 단서로 뺐습니다. "다음 중 …과 같은 것은?"은 "…을 간단히 한 것은?"으로 고쳤고 선지의 A는 θ°로 바꿨습니다. 답은 ①입니다.


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
사각형의 조건인 "선분 AC는 각 C의 이등분선이다"를 사각형에 먼저 두고, 점 H와 E의 정의를 한 문장에 모았습니다. 기호 `$\overline{\mathrm{AC}}$`와 `$\angle\mathrm{C}$`는 길이와 크기라 도형을 가리킬 때는 낱말 "선분 AC", "각 C"로 썼습니다. "AC, DH의 교점"은 "선분 AC와 선분 DH의 교점"으로 하나씩 불렀습니다. 선생님의 지시입니다. ∠x는 θ°로 바꿨고 그림은 책 그대로입니다.


### 017


#### 책
```
[2018년 3월 교육청] 오른쪽 그림과 같이 반지름의 길이가 4이고 중심각의 크기가 $90^{\circ}$인 부채꼴 $\mathrm{OAB}$의 호 $\mathrm{AB}$를 삼등분하여, 점 $\mathrm{B}$에 가까운 점을 $\mathrm{P}$라 하자. 세 선분 $\mathrm{OA}$, $\mathrm{OB}$, $\mathrm{AP}$에 모두 접하는 원의 반지름의 길이는?
```


#### 정본
```
그림과 같이 $\angle\mathrm{AOB}=90^{\circ}$, $\overline{\mathrm{OA}}=\overline{\mathrm{OB}}=4$인 부채꼴 $\mathrm{OAB}$와 $\angle\mathrm{POA}=2\angle\mathrm{POB}$를 만족시키는 현 $\mathrm{AP}$가 있다. 원 $\mathrm{C}$가 세 선분 $\mathrm{OA}$, $\mathrm{OB}$, $\mathrm{AP}$에 모두 접할 때, 원 $\mathrm{C}$의 반지름의 길이는?
```


#### 바뀐 것
선생님이 정본 문장을 썼습니다. "반지름의 길이가 4이고 중심각의 크기가 90°인 부채꼴"은 "∠AOB = 90°, OA = OB = 4인 부채꼴"로, 삼등분점 P는 "∠POA = 2∠POB를 만족시키는 현 AP"로 했습니다. 원을 C라 하고 세 선분에 접하는 조건을 "…일 때"로 물음에 붙였습니다(007 정본의 꼴). 4가 "…인" 절에 들어와 그림에 4와 C를 넣었습니다. "오른쪽 그림과 같이"는 "그림과 같이"로, 출처는 뺐습니다. 답 ②는 그대로입니다.


### 018


#### 책
```
오른쪽 그림과 같이 $\overline{\mathrm{AB}}=\overline{\mathrm{BC}}=\overline{\mathrm{AD}}=6$, $\angle\mathrm{BAD}=90^{\circ}$인 사각형 $\mathrm{ABCD}$가 있다. $\angle\mathrm{CBD}+\angle\mathrm{CDB}=45^{\circ}$일 때, $\overline{\mathrm{CD}}$의 길이는?
```


#### 정본
```
그림과 같이 $\angle\mathrm{BAD}=90^{\circ}$, $\overline{\mathrm{AB}}=\overline{\mathrm{BC}}=\overline{\mathrm{AD}}=6$인 사각형 $\mathrm{ABCD}$가 있다. $\angle\mathrm{CBD}+\angle\mathrm{CDB}=45^{\circ}$일 때, 선분 $\mathrm{CD}$의 길이는?
```


#### 바뀐 것
"오른쪽 그림과 같이"를 "그림과 같이"로 열었습니다. 책이 길이 뒤에 둔 ∠BAD = 90°를 선생님이 앞으로 옮겨 "∠BAD = 90°, AB = BC = AD = 6인 사각형 ABCD가 있다"로 했습니다. 028 정본 "∠B = 40°, AB = a, AC = b인 삼각형"과 같은 차례입니다. 존재문으로 열고 "…일 때"로 조건을 잇는 짜임은 책 그대로입니다. 물음의 기호 CD는 도형이라 낱말 "선분 CD"로 고쳐 썼습니다. 선지와 답 ③, 그림은 책 그대로 옮겼습니다.


### 022


#### 책
```
오른쪽 그림의 $\triangle\!\mathrm{ABC}$는 정삼각형이다. $\overline{\mathrm{AC}}$의 중점을 $\mathrm{D}$, $\overline{\mathrm{BD}}$의 중점을 $\mathrm{E}$, $\angle\mathrm{BCE}=\angle x$라 할 때, $\sin x$의 값을 구하시오.
```


#### 정본
```
그림과 같이 정삼각형 $\mathrm{ABC}$에서 변 $\mathrm{AC}$의 중점을 $\mathrm{D}$, 선분 $\mathrm{BD}$의 중점을 $\mathrm{E}$라 하자. $\angle\mathrm{BCE}=\theta^{\circ}$라 할 때, $\sin\theta^{\circ}$의 값을 구하시오.
```


#### 바뀐 것
"오른쪽 그림의 △ABC는 정삼각형이다"를 "그림과 같이 정삼각형 ABC에서"로 열었습니다. 책의 기호 AC, BD는 도형이라 낱말 "변 AC", "선분 BD"로 바꿨습니다. 두 중점의 정의와 각의 조건이 한 문장에 있던 것을 "…을 E라 하자. ∠BCE = θ°라 할 때"로 갈랐습니다(012 정본의 꼴). 각의 크기 문자는 교과서의 ∠x 대신 θ°입니다. 그림의 각 θ°는 19°로 좁아서 호의 반지름을 12에서 22로 키웠습니다. 물음과 답은 책 그대로입니다.


### 024


#### 책
```
[2017년 3월 교육청] 다음 그림과 같이 $\overline{\mathrm{AB}}=12$, $\overline{\mathrm{AC}}=8\sqrt{2}$, $\angle\mathrm{A}=75^{\circ}$인 삼각형 $\mathrm{ABC}$가 있다. $\angle\mathrm{BAD}=45^{\circ}$, $\angle\mathrm{DAC}=30^{\circ}$가 되도록 변 $\mathrm{BC}$ 위에 점 $\mathrm{D}$를 잡을 때, $\dfrac{\overline{\mathrm{BD}}}{\overline{\mathrm{DC}}}$의 값은?
```


#### 정본
```
그림과 같이 $\overline{\mathrm{AB}}=12$, $\overline{\mathrm{AC}}=8\sqrt{2}$인 삼각형 $\mathrm{ABC}$에서 변 $\mathrm{BC}$ 위의 점 $\mathrm{D}$에 대하여 $\angle\mathrm{BAD}=45^{\circ}$, $\angle\mathrm{DAC}=30^{\circ}$일 때, $\dfrac{\overline{\mathrm{BD}}}{\overline{\mathrm{DC}}}$의 값은?
```


#### 바뀐 것
"∠BAD = 45°, ∠DAC = 30°가 되도록 변 BC 위에 점 D를 잡을 때"를 "삼각형 ABC에서 변 BC 위의 점 D에 대하여 …일 때"로 바꿨습니다. 005 정본의 꼴이고 선생님이 정한 문장입니다. 책의 ∠A = 75°는 그림에 없고 45°와 30°의 합이라 선생님의 지시로 뺐습니다. 두 길이와 두 각만으로 삼각형이 정해져 답 3/2는 그대로입니다. "다음 그림과 같이"는 "그림과 같이"로 열었고 출처를 뺐습니다. 그림은 책 그대로 45°와 30°를 답니다.


### 028


#### 책
```
[도전 문제] 오른쪽 그림과 같이 $\angle\mathrm{B}=40^{\circ}$인 $\triangle\!\mathrm{ABC}$에서 $\angle\mathrm{A}$의 이등분선과 $\overline{\mathrm{BC}}$의 교점을 $\mathrm{D}$라 하면 $\overline{\mathrm{AB}}=\overline{\mathrm{AC}}+\overline{\mathrm{CD}}$이다. $\overline{\mathrm{AB}}=a$, $\overline{\mathrm{AC}}=b$라 할 때, $\triangle\!\mathrm{ABC}$의 넓이를 $a$, $b$를 사용하여 나타내시오.
```


#### 정본
```
그림과 같이 $\angle\mathrm{B}=40^{\circ}$, $\overline{\mathrm{AB}}=a$, $\overline{\mathrm{AC}}=b$인 삼각형 $\mathrm{ABC}$에서 각 $\mathrm{A}$의 이등분선이 변 $\mathrm{BC}$와 만나는 점을 $\mathrm{D}$라 하자. $\overline{\mathrm{AB}}=\overline{\mathrm{AC}}+\overline{\mathrm{CD}}$일 때, 삼각형 $\mathrm{ABC}$의 넓이를 $a$, $b$로 나타내시오.
```


#### 바뀐 것
책이 뒤에 둔 AB = a, AC = b를 ∠B = 40°와 함께 삼각형의 정의에 얹었습니다. "∠A의 이등분선과 BC의 교점을 D라 하면 …이다"는 "각 A의 이등분선이 변 BC와 만나는 점을 D라 하자. …일 때"로 하여 정의와 조건을 갈랐습니다. 각과 변은 낱말로 불렀습니다. 물음 "a, b를 사용하여 나타내시오"는 선생님이 고른 "a, b로 나타내시오"입니다. △ABC는 삼각형 ABC로 썼고 딱지 "도전 문제"를 뺐습니다. 답 (√3/4)ab는 그대로입니다.


### 029


#### 책
```
[대표문제] 오른쪽 그림과 같이 $\overline{\mathrm{AB}}$를 지름으로 하고 반지름의 길이가 3인 원 $\mathrm{O}$에 내접하는 사각형 $\mathrm{ABCD}$가 있다. $\angle\mathrm{B}=30^{\circ}$, $\overline{\mathrm{AD}}=\overline{\mathrm{DC}}$일 때, 사각형 $\mathrm{ABCD}$의 넓이는?
```


#### 정본
```
그림과 같이 선분 $\mathrm{AB}$를 지름으로 하고 반지름의 길이가 3인 원 $\mathrm{O}$에 내접하는 사각형 $\mathrm{ABCD}$에서 $\angle\mathrm{B}=30^{\circ}$, $\overline{\mathrm{AD}}=\overline{\mathrm{DC}}$일 때, 사각형 $\mathrm{ABCD}$의 넓이는?
```


#### 바뀐 것
"오른쪽 그림과 같이"를 "그림과 같이"로 열었습니다. 책의 기호 AB는 지름이라는 도형을 가리키므로 낱말 "선분 AB"로 바꿨습니다. "사각형 ABCD가 있다. ∠B = 30°, AD = DC일 때"는 선생님이 고른 "사각형 ABCD에서 ∠B = 30°, AD = DC일 때"로 이어 한 문장이 되었습니다. 024와 028과 같은 "…에서" 꼴입니다. 반지름 3과 두 조건과 물음과 선지는 책 그대로이고 딱지 "대표문제"를 뺐습니다. 그림도 책 그대로 옮겼습니다.
