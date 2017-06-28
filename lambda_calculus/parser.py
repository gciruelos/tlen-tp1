"""Parser LR(1) de calculadora."""
import ply.yacc as yacc
from .lexer import tokens, LambdaType, LBool, LNat



def p_term_true(p):
    'term : TRUE'
    p[0] = p[1]

def p_term_false(p):
    'term : FALSE'
    p[0] = p[1]

def p_term_zero(p):
    'term : ZERO'
    p[0] = p[1]

def p_term_ifthenelse(p):
    'term : IF term THEN term ELSE term'
    print(list(p))
    print(p[2])
    print(p[2].type())
    if p[2].type().is_bool():
        if p[2].value():
            p[0] = p[4]
        else:
            p[0] = p[6]


def p_error(p):
    print("Hubo un error en el parseo.")

    parser.restart()


# Build the parser
parser = yacc.yacc(debug=True)

def apply_parser(str):
    p = parser.parse(str)
    return p
