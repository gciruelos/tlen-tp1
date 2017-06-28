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
    def type(self):
        return self.type_
    def value(self):
        return self.value_
    def __repr__(self):
        return 'Expr<'+str(self.value_)+' : '+str(self.type_.type())+'>'

class LNat:
    def __init__(self, n):
        self.value_ = n
        self.type_ = LambdaType('Nat')
    def type(self):
        return self.type_
    def value(self):
        return self.value_
    def __repr__(self):
        return 'Expr<'+str(self.value_)+' : '+str(self.type_)+'>'

class LVar:
    def __init__(self, v):
        self.value_ = v
    def type(self):
        return None
    def value(self):
        return self.value_
    def __repr__(self):
        return 'Expr<'+str(self.value_)+'>'

class LLambda:
    def __init__(self, x, t, m):
        self.value_ = (x,t,m)
    def type(self):
        return None
    def value(self):
        return self.value_
    def eval_in(self, other_expr):
        m = self.value_[2]
        class_type = m.__class__.__name__
        if class_type == 'LLambda':
            return m.eval_in(other_expr)
        elif class_type == 'LVar':
            if m.value() == self.value_[0].value():
                return other_expr

    def __repr__(self):
        return 'Expr<\\'+str(self.value_)+'>'

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

    'NAT',

    'LPARENS',
    'RPARENS',


)


t_IF = r'if'
t_THEN = r'then'
t_ELSE = r'else'

t_LAM = r'\\'
t_COLON = r':'
t_DOT = r'.'
t_NAT = r'Nat'

t_LPARENS = r'\('
t_RPARENS = r'\)'


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
    r'[a-z]'
    t.value = LVar(t.value)
    return t

# Build the lexer
lexer = lex.lex()

def apply_lexer(string):
    """Aplica el lexer al string dado."""
    lexer.input(string)

    return list(lexer)
