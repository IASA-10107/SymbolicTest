
# 미분기? 사용설명서

## 사용법

**예시** 
```
Current Symbol: [X, Y]

ADD(POW(X, 4.5) , MUL(X, Y))
=> add(pow(X,4.5),mul(X,Y))

(For X)
=> add(mul(4.5,pow(X,3.5)),add(Y,mul(dY/dX,X)))

(For Y)
=> add(mul(4.5,mul(dX/dY,pow(X,3.5))),add(mul(dX/dY,Y),X))
```

**주의사항**
- 입력창에 입력한 수식은 Enter를 쳐야 반영됩니다!  
- 예외 발생시 Reload 버튼을 눌러 재로드 할 수 있습니다  

## Symbol
X, Y, FOO 등 변수를 정의합니다  

## Term
변수와 함수로 이루어진 임의의 식입니다  

### 미분
입력된 Term을 선택된 Differential Base로 미분한 결과를 출력합니다  
합성함수의 미분, 다변수 함수의 미분을 지원합니다  

### 지원 함수

**ADD :: Term, Term -> Term**  
> 더하기 연산입니다, 합의 미분법을 지원합니다  

**SUB :: Term, Term -> Term**  
> 빼기 연산입니다  

**MUL :: Term, Term -> Term**  
> 곱하기 연산입니다, 곱의 미분법을 지원합니다  

**DIV :: Term, Term -> Term**  
> 나누기 연산입니다, 몫의 미분법을 지원합니다  

**POW :: Term, ConstantNumber -> Term**  
> 거듭제곱 연산입니다, 다항함수의 미분법을 지원합니다  
> (! Term을 지수로 가지는 지수함수는 지원되지 않습니다)