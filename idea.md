Term :: -> Number  
- Symbol : for handling variable? ~~(+ handling dy/dx things)~~  
- PseudoSymbol : for handling dy/dx things  
- ConstantNumber : for handling number in wrapped space  
  
NumberFunction :: Number, ... -> Number  
TermFunction :: Term, ... -> Term  

TermFunctionBase :: NumberFunction -> TermFunction  

diff :: Symbol -> (Term -> Term)  