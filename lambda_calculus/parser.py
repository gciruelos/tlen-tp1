"""Parser LR(1) de calculadora."""
import ply.yacc as yacc
from .lexer import tokens, LambdaType, LBool, LNat, LLambda



def p_expr_true(p):
    'expr : TRUE'
    p[0] = p[1]

def p_expr_false(p):
    'expr : FALSE'
    p[0] = p[1]

def p_expr_zero(p):
    'expr : ZERO'
    p[0] = p[1]

def p_expr_ifthenelse(p):
    'expr : IF expr THEN expr ELSE expr'
    print(list(p))
    if p[2].type().is_bool():
        if p[2].value():
            p[0] = p[4]
        else:
            p[0] = p[6]

def p_expr_var(p):
    'expr : VAR'
    p[0] = p[1]

def p_expr_lambda(p):
    'expr : lambda'
    p[0] = p[1]

def p_lambda(p):
    'lambda : LAM VAR COLON type DOT expr'
    p[0] = LLambda(p[2], p[4], p[6])

def p_type_nat(p):
    'type : NAT'
    p[0] = LambdaType('Nat')


def p_expr_app(p):
    'expr : func arg'
    p[0] = p[1].eval_in(p[2])

def p_func_lambda(p):
    'func : LPARENS lambda RPARENS'
    p[0] = p[2]

def p_arg_expr(p):
    'arg : expr'
    p[0] = p[1]


def p_error(p):
    print("Hubo un error en el parseo.")

    parser.restart()


# Build the parser
parser = yacc.yacc(debug=True)

def apply_parser(str):
    p = parser.parse(str)
    return p
