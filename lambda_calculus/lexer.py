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

tokens = (
    'TRUE',
    'FALSE',
    'IF',
    'THEN',
    'ELSE',
    'LAMBDA',
    'COLON',
    'DOT',
    'ZERO',
    'SUCC',
    'PRED',
    'ISZERO',
    'LPARENS',
    'RPARENS',
    'VAR',  # ?? pensar mejor
    'BOOL',
    'NAT',
    'ARROW',
)

t_TRUE = r'true'
t_FALSE = r'false'
t_IF = r'if'
t_THEN = r'then'
t_ELSE = r'else'
t_LAMBDA = r'\\'
t_COLON = r':'
t_DOT = r'\.'
t_ZERO = r'0'
t_SUCC = r'succ'
t_PRED = r'pred'
t_ISZERO = r'iszero'
t_LPARENS = r'\('
t_RPARENS = r'\)'
t_VAR = r'x'

t_BOOL = r'Bool'
t_NAT = r'Nat'
t_ARROW = r'->'

t_ignore = ' \t'



# Build the lexer
lexer = lex.lex()

def apply_lexer(string):
    """Aplica el lexer al string dado."""
    lexer.input(string)

    return list(lexer)
