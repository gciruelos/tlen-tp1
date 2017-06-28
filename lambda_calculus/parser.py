"""Parser LR(1) de calculadora."""
import ply.yacc as yacc
from .lexer import tokens

class LambdaType:
    def __init__(self, t):
        self.type = t
    def is_nat(self):
        return self.type == 'Nat'
    def is_bool(self):
        return self.type == 'Bool'
    def is_function(self):
        return not (self.is_bool() or self.is_nat())
    def type(self):
        return self.type



class LambdaTerm:
    def __init__(self, term, type_):
        self.type = type_
        self.term = term
    def is_nat(self):
        return selt.type.is_nat()
    def is_bool(self):
        return selt.type.is_bool()
    def is_function(self):
        return selt.type.is_function()
    def value(self):
        return self.term


'''
  T  -> T -> T2
      | T2.
  T2 -> Bool | Nat.
'''

def p_type_bool(p):
    'type2 : BOOL'
    print(list(p))
    p[0] = LambdaType(p[1])

def p_type_nat(p):
    'type2 : NAT'
    print(list(p))
    p[0] = LambdaType(p[1])

def p_type_arrow(p):
    'type : type ARROW type2'
    print(list(p))
    p[0] = LambdaType((p[1], p[3]))

def p_type_arrow(p):
    'type : type2'
    print(list(p))
    p[0] = p[1]



def p_term_true(p):
    'term : TRUE'
    print(list(p))
    p[0] = LambdaTerm(True, LambdaType('Bool'))

def p_term_false(p):
    'term : FALSE'
    print(list(p))
    p[0] = LambdaTerm(False, LambdaType('Bool'))

def p_term_ifthenelse(p):
    'term : IF term THEN term ELSE term'
    print(list(p))
    if p[2].is_bool():
        if p[2].value():
            p[0] = p[4]
        else:
            p[0] = p[6]
    print(p[0])

def p_term_var(p):
    'term : VAR'
    print(list(p))
    p[0] = p[1]



def p_term_abstraction(p):
    'term : LAMBDA VAR COLON type DOT term'
    print(list(p))
    p[0] = p[1]

def p_error(p):
    print("Hubo un error en el parseo.")

    parser.restart()


# Build the parser
parser = yacc.yacc(debug=True)

def apply_parser(string):
    return str(parser.parse(string).value())
