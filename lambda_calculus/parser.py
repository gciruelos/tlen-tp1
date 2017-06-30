"""Parser LR(1) de lambda."""
import ply.yacc as yacc
from .lexer import tokens
from .ast import TNat,TBool,TArrow, LBool, LZero, LVar, LLambda, LSucc, LPred, LApp, LIfThenElse,LIsZero

precedence = (
    ('right', 'ARROW'),
)

########################## EXPRESION ###########################################
#
#  E -> S L
#     | S
#
################################################################################

def p_expr_s_lambda(p):
    'expr : S lambda'
    if p[1] is None:
        p[0] = p[2]
    else:
        p[0] = LApp(p[1], p[2])


def p_expr_s(p):
    'expr : S'
    p[0] = p[1]

########################## S ###################################################
#
#  S -> S cont
#     | λ
#
################################################################################

def p_s_factor(p):
    'S : S cont'
    if p[1] is None:
        p[0] = p[2]
    else:
        p[0] = LApp(p[1], p[2])

def p_s_empty(p):
    'S : '

########################## cont ################################################
#
#  C -> (E)
#     | var
#     | true
#     | false
#     | 0
#     | iszero(E)
#     | succ(E)
#     | pred(E)
#     | if E then E else C
#
################################################################################

def p_cont_expr(p):
    'cont : LPARENS expr RPARENS'
    p[0] = p[2]

def p_cont_var(p):
    'cont : VAR'
    p[0] = p[1]

def p_cont_true(p):
    'cont : TRUE'
    p[0] = p[1]

def p_cont_false(p):
    'cont : FALSE'
    p[0] = p[1]

def p_cont_zero(p):
    'cont : ZERO'
    p[0] = p[1]

def p_cont_iszero(p):
    'cont : ISZERO LPARENS expr RPARENS'
    p[0] = LIsZero(p[3])

def p_cont_succ(p):
    'cont : SUCC LPARENS expr RPARENS'
    p[0] = LSucc(p[3])

def p_cont_pred(p):
    'cont : PRED LPARENS expr RPARENS'
    p[0] = LPred(p[3])

def p_cont_ifthenelse(p):
    'cont : IF expr THEN expr ELSE cont'
    p[0] = LIfThenElse(p[2], p[4], p[6])


########################## LAMBDA ##############################################
#
#  L -> \ V : T . E
#
################################################################################

def p_lambda(p):
    'lambda : LAM VAR COLON type DOT expr'
    p[0] = LLambda(p[2], p[4], p[6])


########################## TIPOS ###############################################
#
#  T -> T' -> T
#     | T'
#
#  T' -> (T -> T')
#      | Bool
#      | Nat
#
################################################################################


def p_type_arrow(p):
    'type : typex ARROW type'
    p[0] = TArrow(p[1], p[3])

def p_type_typex(p):
    'type : typex'
    p[0] = p[1]

def p_typex_arrow(p):
    'typex : LPARENS type ARROW typex RPARENS'
    p[0] = TArrow(p[2], p[4])

def p_typex_nat(p):
    'typex : NAT'
    p[0] = TNat()

def p_typex_bool(p):
    'typex : BOOL'
    p[0] = TBool()


def p_error(p):
    if p is not None:
        exit('Error de sintaxis: "{}" no esperado en la posicion {}.'.format(p.value, p.lexpos))
    else:
        exit('Error de sintaxis: fin de linea no esperado.')



# Build the parser
parser = yacc.yacc(debug=True)

def apply_parser(str):
    p = parser.parse(str)
    p.add_judgement('h4x0r', 'turururu')  # Llamo a add judgement del padre asi
                                          # propaga todos los judgements hacia
                                          # abajo.
    # print(repr(p))
    while p is not None and not p.is_value():
        p = p.value()
        # print(repr(p))
    return p
