from __future__ import annotations
from typing import Callable, Mapping
from numbers import Number

class Term:
    def __init__(self):
        pass

    def __call__(self) -> Number:
        """
        Bind given Term with values
        """
        pass

    def __str__(self) -> str:
        """
        Returns formula of Term
        """
        pass

    def tree(self) -> dict:
        """
        Term represented with dictionary form
        """
        pass
    
    def diff(self, base: Symbol) -> Term:
        """
        Differential of given Term with Symbol
        """
        pass

class TermFunctionBase:

    @staticmethod
    def Termify(func: Callable[[Number], Number]):
        return lambda *args: func(*(arg() for arg in args))

    def __init__(self, name: str, func: Callable[[Term], Number], diff: Callable[[Term, Symbol], Term] | None = None):
        self.func = func
        self.name = name
        self.diff = diff
    
    def set_diff(self, diff: Callable[[Term, Symbol], Term]):
        self.diff = diff

    def __call__(self, *args: Term | Number) -> Term:
        return TermFunction(self, *map(ConstantNumber.Constify, args))
    
    def __str__(self):
        return self.name

class ConstantNumber(Term):

    def __init__(self, value: Number):
        self.value = float(value)
    
    def __call__(self):
        return self.value
    
    def __str__(self):
        return str(self.value)
    
    def __eq__(self, __value: ConstantNumber):
        return isinstance(__value, ConstantNumber) and self.value == __value.value
    
    def tree(self):
        return str(self)
    
    def Constify(arg: Term | Number):
        return ConstantNumber(arg) if isinstance(arg, Number) else arg
    
    def diff(self, base):
        return ConstantNumber(0.)

class Symbol(Term):
    
    symbols: Mapping[str, Symbol] = {}

    def __init__(self, name: str, __default=0.):
        if name not in self.symbols:
            self.value = __default
            self.name = name
            self.symbols[name] = self
        else:
            raise NameError(f"{name} already exists")

    def set_value(self, value):
        self.value = value

    def __call__(self):
        return self.value
    
    def __str__(self):
        return self.name
    
    def tree(self):
        return str(self)
    
    def diff(self, base):
        # TODO: multi-variable diff implementation
        return ConstantNumber(1.) if self == base else PseudoSymbol(f"d{str(self)}/d{str(base)}")

class PseudoSymbol(Term):

    def __init__(self, name: str, __default=0.):
        self.value = __default
        self.name = name

    # def set_value(self, value):
    #     self.value = value

    def __call__(self):
        return self.value
    
    def __str__(self):
        return self.name
    
    def tree(self):
        return str(self)
    
    def diff(self, base):
        # TODO: multi-variable diff implementation
        return PseudoSymbol(f"d{str(self)}/d{str(base)}")

class TermFunction(Term):
    def __init__(self, funcbase: TermFunctionBase, *args: Term):
        self.funcbase = funcbase
        self.args = list(args)
    
    def __call__(self):
        return self.funcbase.func(*self.args)
    
    def __str__(self):
        return f"{self.funcbase.name}({",".join(map(str, self.args))})"
    
    def tree(self):
        return {str(self.funcbase) : [arg.tree() for arg in self.args]}
    
    def diff(self, base: Symbol) -> Term:
        return self.funcbase.diff(*self.args, base=base)

__ADD = TermFunctionBase.Termify(float.__add__)
__SUB = TermFunctionBase.Termify(float.__sub__)
__MUL = TermFunctionBase.Termify(float.__mul__)
__DIV = TermFunctionBase.Termify(float.__truediv__)
def __POW(arg1: Term, arg2: ConstantNumber):
    if not isinstance(arg2, ConstantNumber): raise TypeError
    return float.__pow__(arg1(), arg2())

ADD = TermFunctionBase("add", __ADD)
SUB = TermFunctionBase("sub", __SUB)
MUL = TermFunctionBase("mul", __MUL)
DIV = TermFunctionBase("div", __DIV)
POW = TermFunctionBase("pow", __POW)

def __DIFFADD(arg1: Term, arg2: Term, base: Symbol):
    return ADD(arg1.diff(base=base), arg2.diff(base=base))

def __DIFFSUB(arg1: Term, arg2: Term, base: Symbol):
    return SUB(arg1.diff(base=base), arg2.diff(base=base))

def __DIFFMUL(arg1: Term, arg2: Term, base: Symbol):
    return ADD(MUL(arg1.diff(base=base), arg2), MUL(arg2.diff(base=base), arg1))

def __DIFFDIV(arg1: Term, arg2: Term, base: Symbol):
    return DIV(SUB(MUL(arg1.diff(base=base), arg2), MUL(arg1, arg2.diff(base=base))), POW(arg2, ConstantNumber(2.)))

def __DIFFPOW(arg1: Term, arg2: ConstantNumber, base: Symbol):
    if not isinstance(arg2, ConstantNumber): raise TypeError
    return MUL(arg2, MUL(arg1.diff(base=base), POW(arg1, ConstantNumber(arg2()-1))))

ADD.set_diff(__DIFFADD)
SUB.set_diff(__DIFFSUB)
MUL.set_diff(__DIFFMUL)
DIV.set_diff(__DIFFDIV)
POW.set_diff(__DIFFPOW)

__compressed = lambda term: isinstance(term, (ConstantNumber, Symbol, PseudoSymbol))

def compress(term: Term | TermFunction):
    if __compressed(term): return term

    isConstant = all((isinstance(arg, ConstantNumber) for arg in term.args))
    for i in range(len(term.args)):
        term.args[i] = compress(term.args[i])

    if isConstant: 
        term = ConstantNumber(term.funcbase.func(*term.args))

    elif term.funcbase == ADD:
        term = (term.args[0] if term.args[1] == ConstantNumber(0.) else
                term.args[1] if term.args[0] == ConstantNumber(0.) else
                term)

    elif term.funcbase == SUB:
        term = (term.args[0] if term.args[1] == ConstantNumber(0.) else
                term)
        
    elif term.funcbase == MUL:
        if ConstantNumber(0.) in term.args:
            term = ConstantNumber(0.)
        else:
            term = (term.args[0] if term.args[1] == ConstantNumber(1.) else
                    term.args[1] if term.args[0] == ConstantNumber(1.) else
                    term)
    
    elif term.funcbase == DIV:
        term = (ConstantNumber(0.) if term.args[0] == ConstantNumber(0.) else
                term.args[0] if term.args[1] == ConstantNumber(1.) else
                term)
            
    elif term.funcbase == POW:
        term = (term.args[0] if term.args[1] == ConstantNumber(1.) else
                ConstantNumber(1.) if term.args[1] == ConstantNumber(0.) else
                term)
        
    if __compressed(term): return term

    return term