"""Parser LR(1) de calculadora."""
import ply.yacc as yacc
from .lexer import tokens, LambdaType, LBool, LNat, LLambda


########################## EXPRESSIO############################################
#
#  E -> S L
#     | S
#
################################################################################

def p_expr_s_lambda(p):
    'expr : S lambda'

def p_expr_s(p):
    'expr : S'

########################## S ###################################################
#
#  S -> S cont
#     | λ
#
################################################################################

def p_s_factor(p):
    'S : S cont'

def p_s_empty(p):
    'S : '

########################## cont ################################################
#
#  cont -> (E)
#     | Var
#     | Val
#     | if expr then expr else S
#
################################################################################

def p_cont_expr(p):
    'cont : LPARENS expr RPARENS'
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

def p_cont_ifthenelse(p):
    'cont : IF expr THEN expr ELSE S'
    print(list(p))
    if p[2].type().is_bool():
        if p[2].value():
            p[0] = p[4]
        else:
            p[0] = p[6]


def p_cont_var(p):
    'cont : VAR'
    p[0] = p[1]


########################### FUNCTION ############################################
##
##  F -> V
##     | (L)
##     | F A
##
#################################################################################
#
#def p_func_expr(p):
#    'func : VAR'
#    p[0] = p[1]
#
#def p_func_lambda(p):
#    'func : LPARENS lambda RPARENS'
#    p[0] = p[2]
#
#def p_func_app(p):
#    'func : func arg'
#    p[0] = p[1].eval_in(p[2])
#
########################### ARGUMENT ############################################
##
##  A -> C
##     | (L)
##     | (F A)
##
#################################################################################
#
#def p_arg_expr(p):
#    'arg : cont'
#    p[0] = p[1]
#
#def p_arg_lambda(p):
#    'arg : LPARENS lambda RPARENS'
#    p[0] = p[2]
#
#def p_arg_app(p):
#    'arg : LPARENS func arg RPARENS'
#    p[0] = p[2].eval_in(p[3])

########################## LAMBDA ##############################################
#
#  L -> \ V : T . E
#
################################################################################

def p_lambda(p):
    'lambda : LAM VAR COLON type DOT expr'
    p[0] = LLambda(p[2], p[4], p[6])


def p_type_nat(p):
    'type : NAT'
    p[0] = LambdaType('Nat')


def p_error(p):
    print("Hubo un error en el parseo.")

    parser.restart()


# Build the parser
parser = yacc.yacc(debug=True)

def apply_parser(str):
    p = parser.parse(str)
    return p
