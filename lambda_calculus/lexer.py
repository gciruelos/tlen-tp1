#! coding: utf-8
"""Calculator lexer example."""
import ply.lex as lex
from .ast import TNat,TBool,TArrow, LBool, LZero, LVar, LLambda, LSucc, LPred, LApp, LIfThenElse,LIsZero
from difflib import get_close_matches

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

tokenizables = [
'if',
'then',
'else',
'\\',
':',
'.',
'(',
')',
'iszero',
'succ',
'pred',
'->',
'Nat',
'Bool']

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
    t.value = LZero()
    return t

# Sin i,s,p
def t_VAR(t):
    r'[abcjxyz]'
    t.value = LVar(t.value)
    return t

def t_error(t):
    errStr = t.value.split(' ', 1)[0]
    print('Error de sintaxis: la cadena "{}" no puede ser tokenizada.'
          .format(errStr))
    if get_close_matches(errStr, tokenizables, n = 1):
        print('Habrás querido usar "{}"?'
              .format(*get_close_matches(errStr, tokenizables, n = 1)))
    exit(0)

# Build the lexer
lexer = lex.lex()
def apply_lexer(string):
    """Aplica el lexer al string dado."""
    lexer.input(string)

    return list(lexer)
