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
        return 'LambdaType<'+str(self.type_)+'>'

class LBool:
    def __init__(self, t):
        self.value_ = t
        self.type_ = LambdaType('Bool')
    def type(self):
        return self.type_
    def value(self):
        return self.value_
    def __repr__(self):
        return 'LambdaTerm<'+str(self.value_)+' : '+str(self.type_.type())+'>'

class LNat:
    def __init__(self, n):
        self.value_ = n
        self.type_ = LambdaType('Nat')
    def type(self):
        return self.type_
    def value(self):
        return self.value_
    def __repr__(self):
        return 'LambdaTerm<'+str(self.value_)+' : '+str(self.type_)+'>'


tokens = (
    'TRUE',
    'FALSE',
    'ZERO',
    'IF',
    'THEN',
    'ELSE',

)


t_IF = r'if'
t_THEN = r'then'
t_ELSE = r'else'


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

# Build the lexer
lexer = lex.lex()

def apply_lexer(string):
    """Aplica el lexer al string dado."""
    lexer.input(string)

    return list(lexer)
