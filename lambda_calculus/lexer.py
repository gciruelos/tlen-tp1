#! coding: utf-8
"""Calculator lexer example."""
import ply.lex as lex

"""
Lista de tokens

El analizador léxico de PLY (al llamar al método lex.lex()) va a buscar
para cada uno de estos tokens una variable "t_TOKEN" en el módulo actual.

Sí, es súper nigromántico pero es lo que hay.

t_TOKEN puede ser:

- Una expresión regular
- Una función cuyo docstring sea una expresión regular (bizarro).

En el segundo caso, podemos hacer algunas cosas "extras", como se
muestra aquí abajo.

"""

class LambdaType:
    def __init__(self, t):
        self.type_ = t
    def is_nat(self):
        return self.type_ == 'Nat'
    def is_bool(self):
        return self.type_ == 'Bool'
    def is_function(self):
        return not (self.is_bool() or self.is_nat())
    def type(self):
        return self.type_
    def __repr__(self):
        return 'Type<'+str(self.type_)+'>'

class LBool:
    def __init__(self, t):
        self.value_ = t
        self.type_ = LambdaType('Bool')
    def get(self):
        return self.value_
    def value(self):
        return self
    def type(self):
        return self.type_
    def replace(self, var, e):
        return self
    def is_value(self):
        return True
    def __repr__(self):
        return 'Expr<'+str(self.value_)+' : '+str(self.type_.type())+'>'

class LNat:
    def __init__(self, n):
        self.value_ = n
        self.type_ = LambdaType('Nat')
    def get(self):
        return self.value_
    def value(self):
        return self
    def type(self):
        return self.type_
    def replace(self, var, e):
        return self
    def is_value(self):
        return True
    def __repr__(self):
        return 'Expr<'+str(self.value_)+' : '+str(self.type_)+'>'

class LVar:
    def __init__(self, v):
        self.value_ = v
    def get(self):
        return self.value_
    def value(self):
        return None
    def type(self):
        return None
    def replace(self, var, e):
        if var == self.value_:
            return e
        return self
    def is_value(self):
        return False
    def __repr__(self):
        return 'Expr<'+str(self.value_)+'>'

class LIsZero:
    def __init__(self, e):
        self.value_ = e
    def get(self):
        return self.value_
    def value(self):
        reduced = self.value_.value()
        if reduced.type().is_nat():
            return LBool(reduced.get() == 0)
        else:
            print('ERROR!')
            pass  # ERROR!
        self.value_ = reduced
    def type(self):
        reduced = self.value_.value()
        if reduced.type().is_nat():
            return LambdaType('Bool')
        else:
            print('ERROR!')
            pass  # ERROR!
    def replace(self, var, e):
        self.value_ = self.value_.replace(var, e)
        return self
    def is_value(self):
        return False
    def __repr__(self):
        return 'Expr<iszero('+str(self.value_)+')>'

class LSucc:
    def __init__(self, e):
        self.value_ = e
    def get(self):
        return self.value_
    def value(self):
        reduced = self.value_.value()
        if reduced.type().is_nat():
            return LNat(reduced.get() + 1)
        else:
            pass  # ERROR!
        self.value_ = reduced
    def type(self):
        reduced = self.value_.value()
        if reduced.type().is_nat():
            return LambdaType('Nat')
        else:
            pass  # ERROR!
    def replace(self, var, e):
        self.value_ = self.value_.replace(var, e)
        return self
    def is_value(self):
        v = self.value_
        return v.is_value() and v.__class__.__name__ != 'LLambda'
    def __repr__(self):
        return 'Expr<succ('+str(self.value_)+')>'

class LPred:
    def __init__(self, e):
        self.value_ = e
    def get(self):
        return self.value_
    def reduce(self):
        self.value_ = self.value_.value()
    def value(self):
        self.reduce()
        reduced = self.value_
        if reduced.type().is_nat() and reduced.get() > 0:
            return LNat(reduced.get() - 1)
        else:
            pass  # ERROR!
    def type(self):
        self.reduce()
        reduced = self.value_
        if reduced.type().is_nat():
            return LambdaType('Nat')
        else:
            pass  # ERROR!
    def replace(self, var, e):
        self.value_ = self.value_.replace(var, e)
        return self
    def is_value(self):
        return False
    def __repr__(self):
        return 'Expr<pred('+str(self.value_)+')>'

class LIfThenElse:
    def __init__(self, guarda, case_true, case_false):
        self.value_ = (guarda, case_true, case_false)
    def get(self):
        return self.value_
    def reduce(self):
        reduced_guarda = self.value_[0].value()
        reduced_true = self.value_[1].value()
        reduced_false = self.value_[2].value()
        self.value_ = (reduced_guarda, reduced_true, reduced_false)
    def value(self):
        self.reduce()
        reduced_guarda = self.value_[0]
        reduced_true = self.value_[1]
        reduced_false = self.value_[2]
        if reduced_guarda.type().is_bool():  # chequear same type
            if reduced_guarda.get():
                return reduced_true
            else:
                return reduced_false
        else:
            print('ERROR!')
            pass  # ERROR!
    def type(self):
        self.reduce()
        return self.value_[1].type()
    def replace(self, var, e):
        self.value_ = (self.value_[0].replace(var, e),
                self.value_[1].replace(var, e),
                self.value_[2].replace(var, e))
        return self
    def is_value(self):
        return False
    def __repr__(self):
        return 'Expr<if'+str(self.value_)+'>'

class LLambda:
    def __init__(self, x, t, m):
        self.value_ = (x,t,m)
    def get(self):
        return self.value_
    def reduce(self):
        pass
    def value(self):
        self.reduce()
        return self
    def type(self):
        self.reduce()
        return None
    def replace(self, var, e):
        self.value_ = (self.value_[0],
                self.value_[1],
                self.value_[2].replace(var, e))
        return self
    def eval_in(self, other_expr):
        return self.value_[2].replace(self.value_[0].get(), other_expr)
    def is_value(self):
        return True
    def __repr__(self):
        return 'Expr<\\'+str(self.value_)+'>'

class LApp:
    def __init__(self, fun, arg):
        self.value_ = (fun, arg)
    def get(self):
        return self.value_
    def reduce(self):
        reduced_fun = self.value_[0].value()
        self.value_ = (reduced_fun, self.value_[1])
    def value(self):
        self.reduce()
        return self.value_[0].eval_in(self.value_[1])
    def type(self):
        self.reduce()
        return self.value_[0].eval_in(self.value_[1]).type()
    def replace(self, var, e):
        self.value_ = (self.value_[0].replace(var, e),
                       self.value_[1].replace(var, e))
        return self
    def is_value(self):
        return False
    def __repr__(self):
        return 'Expr<@'+str(self.value_)+'>'

tokens = (
    'TRUE',
    'FALSE',
    'ZERO',
    'IF',
    'THEN',
    'ELSE',

    'VAR',
    'LAM',
    'COLON',
    'DOT',

    'LPARENS',
    'RPARENS',

    'ISZERO',
    'SUCC',
    'PRED',

    'ARROW',
    'NAT',
    'BOOL',

)


t_IF = r'if'
t_THEN = r'then'
t_ELSE = r'else'

t_LAM = r'\\'
t_COLON = r':'
t_DOT = r'\.'

t_LPARENS = r'\('
t_RPARENS = r'\)'

t_ISZERO = r'iszero'
t_SUCC = r'succ'
t_PRED = r'pred'

t_ARROW = r'->'
t_NAT = r'Nat'
t_BOOL = r'Bool'

t_ignore = ' \t'


def t_TRUE(t):
    r'true'
    t.value = LBool(True)
    return t

def t_FALSE(t):
    r'false'
    t.value = LBool(False)
    return t

def t_ZERO(t):
    r'0'
    t.value = LNat(0)
    return t

def t_VAR(t):
    r'[x-z]'
    t.value = LVar(t.value)
    return t

# Build the lexer
lexer = lex.lex()
def apply_lexer(string):
    """Aplica el lexer al string dado."""
    lexer.input(string)

    return list(lexer)
