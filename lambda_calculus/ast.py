
ERROR_EVALUACION = 'Ilegal: se intenta aplicarle {1} a {0}.'
ERROR_EVALUACION_TIPOS = 'Ilegal: se intenta realizar {1}({0}), que tiene tipo {2} en vez de {3}.'

def is_var(x):
    return x.__class__.__name__ == 'LVar'

###############################################################################
################################### TIPOS #####################################
###############################################################################

class TBool:
    def __init__(self):
        pass
    def is_nat(self):
        return False
    def is_bool(self):
        return True
    def is_arrow(self):
        return False
    def __eq__(self, other):
        return other.is_bool()
    def __repr__(self):
        return 'Type<Bool>'
    def __str__(self):
        return 'Bool'

class TNat:
    def __init__(self):
        pass
    def is_nat(self):
        return True
    def is_bool(self):
        return False
    def is_arrow(self):
        return False
    def __eq__(self, other):
        return other.is_nat()
    def __repr__(self):
        return 'Type<Nat>'
    def __str__(self):
        return 'Nat'

class TArrow:
    def __init__(self, d, c, parens=False):
        self.domain_ = d
        self.codomain_ = c
    def is_nat(self):
        return False
    def is_bool(self):
        return False
    def is_arrow(self):
        return True
    def domain(self):
        return self.domain_
    def codomain(self):
        return self.codomain_
    def __eq__(self, other):
        return other.is_arrow() and other.codomain() == self.codomain_ and other.domain() == self.domain_
    def __repr__(self):
        return 'Type<'+str(self.domain_)+'->'+str(self.codomain_)+'>'
    def __str__(self):
        if self.domain_.is_arrow():
            return '('+str(self.domain_)+') -> '+str(self.codomain_)
        return str(self.domain_)+' -> '+str(self.codomain_)

###############################################################################
################################# TERMINOS ####################################
###############################################################################

class LBool:
    def __init__(self, t):
        self.value_ = t
        self.type_ = TBool()
        self.env_ = {}
    def add_judgement(self, var, t):
        self.env_[var] = t
    def get(self):
        return self.value_
    def value(self):
        return self
    def type(self):
        return self.type_
    def replace(self, var, e):
        return self
    def eval_in(self, other_expr):
        exit(ERROR_EVALUACION.format(str(other_expr), str(self)))
    def is_value(self):
        return True
    def __repr__(self):
        return 'Expr<'+str(self.value_).lower()+'>'
    def __str__(self):
        return str(self.value_).lower()

class LZero:
    def __init__(self):
        self.value_ = 0
        self.type_ = TNat()
        self.env_ = {}
    def add_judgement(self, var, t):
        self.env_[var] = t
    def get(self):
        return 0
    def value(self):
        return self
    def type(self):
        return self.type_
    def replace(self, var, e):
        return self
    def eval_in(self, other_expr):
        exit(ERROR_EVALUACION.format(str(other_expr), str(self.value_)))
    def is_value(self):
        return True
    def __repr__(self):
        return 'Expr<'+str(self.value_)+'>'
    def __str__(self):
        return str(self.value_).lower()

class LVar:
    def __init__(self, v):
        self.value_ = v
        self.env_ = {}
    def add_judgement(self, var, t):
        self.env_[var] = t
    def get(self):
        return self.value_
    def value(self):
        if self.value_ in self.env_:
            return self
        exit('Ilegal: variable libre '+self.value_+'.')
    def type(self):
        if self.value_ in self.env_:
            return self.env_[self.value_]
        exit('Ilegal: variable libre '+self.value_+'.')
    def replace(self, var, e):
        if var == self.value_:
            return e
        return self
    def eval_in(self, other_expr):
        return LApp(self, other_expr)
    def is_value(self):
        return False
    def __repr__(self):
        return 'Expr<'+str(self.value_)+'>'
    def __str__(self):
        return self.value_

class LIsZero:
    def __init__(self, e):
        self.value_ = e
        self.env_ = {}
    def add_judgement(self, var, t):
        self.env_[var] = t
        self.value_.add_judgement(var, t)
    def get(self):
        return self.value_
    def reduce(self):
        while not self.value_.is_value() and not is_var(self.value_):
            self.value_ = self.value_.value()
    def value(self):
        self.reduce()
        reduced = self.value_
        if reduced.type().is_nat():
            return LBool(reduced.get() == 0)
        else:
            exit(ERROR_EVALUACION_TIPOS
                    .format(str(reduced), 'iszero', reduced.type(), 'Nat'))
    def type(self):
        self.reduce()
        reduced = self.value_
        if reduced.type().is_nat():
            return TBool()
        else:
            exit(ERROR_EVALUACION_TIPOS
                    .format(str(reduced), 'iszero', reduced.type(), 'Nat'))
    def replace(self, var, e):
        self.value_ = self.value_.replace(var, e)
        return self
    def eval_in(self, other_expr):
        exit(ERROR_EVALUACION.format(str(other_expr), 'iszero'))
    def is_value(self):
        return False
    def __repr__(self):
        return 'Expr<iszero('+str(self.value_)+')>'
    def __str__(self):
        return 'iszero('+str(self.value_)+')'

class LSucc:
    def __init__(self, e):
        self.value_ = e
        self.env_ = {}
    def add_judgement(self, var, t):
        self.env_[var] = t
        self.value_.add_judgement(var, t)
    def get(self):
        return self.value_.get() + 1
    def minus_one(self):
        return self.value_
    def reduce(self):
        while not self.value_.is_value() and not is_var(self.value_):
            self.value_ = self.value_.value()
    def value(self):
        self.reduce()
        reduced = self.value_
        if reduced.type().is_nat():
            return LSucc(reduced)
        else:
            exit(ERROR_EVALUACION_TIPOS
                    .format('succ', str(reduced), reduced.type(), 'Nat'))
    def type(self):
        self.reduce()
        reduced = self.value_
        if reduced.type().is_nat():
            return TNat()
        else:
            exit(ERROR_EVALUACION_TIPOS
                    .format('succ', str(reduced), reduced.type(), 'Nat'))
    def replace(self, var, e):
        self.value_ = self.value_.replace(var, e)
        return self
    def eval_in(self, other_expr):
        exit(ERROR_EVALUACION.format(str(other_expr), str(self)))
    def is_value(self):
        v = self.value_
        return v.is_value() and v.__class__.__name__ != 'LLambda'
    def __repr__(self):
        return 'Expr<succ('+str(self.value_)+')>'
    def __str__(self):
        return str(self.get())

class LPred:
    def __init__(self, e):
        self.value_ = e
        self.env_ = {}
    def add_judgement(self, var, t):
        self.env_[var] = t
        self.value_.add_judgement(var, t)
    def get(self):
        return self.value_
    def reduce(self):
        while not self.value_.is_value() and not is_var(self.value_):
            self.value_ = self.value_.value()
    def value(self):
        self.reduce()
        reduced = self.value_
        if reduced.type().is_nat():  # No hay que chequear reduced.get() > 0.
            if reduced.get() <= 1:
                return LZero()
            else:
                return reduced.minus_one()
        else:
            exit(ERROR_EVALUACION_TIPOS
                    .format(str(reduced), 'pred', reduced.type(), 'Nat'))
    def type(self):
        self.reduce()
        reduced = self.value_
        if reduced.type().is_nat():
            return TNat()
        else:
            exit(ERROR_EVALUACION_TIPOS
                    .format(str(reduced), 'pred', reduced.type(), 'Nat'))
    def replace(self, var, e):
        self.value_ = self.value_.replace(var, e)
        return self
    def eval_in(self, other_expr):
        exit(ERROR_EVALUACION.format(str(other_expr), str(self)))
    def is_value(self):
        return False
    def __repr__(self):
        return 'Expr<pred('+repr(self.value_)+')>'
    def __str__(self):
        return 'pred('+str(self.value_)+')'

class LIfThenElse:
    def __init__(self, guarda, case_true, case_false):
        self.value_ = (guarda, case_true, case_false)
        self.env_ = {}
    def add_judgement(self, var, t):
        self.env_[var] = t
        self.value_[0].add_judgement(var, t)
        self.value_[1].add_judgement(var, t)
        self.value_[2].add_judgement(var, t)
    def get(self):
        return self.value_
    def reduce(self):
        reduced_guarda = self.value_[0].value()
        while not reduced_guarda.is_value() and not is_var(reduced_guarda):
            print(reduced_guarda.__class__.__name__)
            reduced_guarda = reduced_guarda.value()
        reduced_true = self.value_[1].value()
        while not reduced_true.is_value() and not is_var(reduced_guarda):
            reduced_true = reduced_true.value()
        reduced_false = self.value_[2].value()
        while not reduced_false.is_value() and not is_var(reduced_guarda):
            reduced_false = reduced_false.value()
        self.value_ = (reduced_guarda, reduced_true, reduced_false)
    def value(self):
        self.reduce()
        reduced_guarda = self.value_[0]
        reduced_true = self.value_[1]
        reduced_false = self.value_[2]
        if reduced_guarda.type().is_bool():
            if reduced_true.type() != reduced_false.type():
                exit('Ilegal: distintos tipos en el cuerpo del if: '
                     '{} y {} tienen distintos tipos ({} y {} respectivamente).'
                    .format(str(reduced_true), str(reduced_false),
                            reduced_true.type(), reduced_false.type()))
            elif reduced_guarda.get():
                return reduced_true
            else:
                return reduced_false
        else:
            exit('Ilegal: se esperaba un Bool en la guarda del if y se encontró {}, de tipo {}.'
                    .format(str(reduced_guarda), reduced_guarda.type()))
    def type(self):
        self.reduce()
        return self.value_[1].type()
    def replace(self, var, e):
        self.value_ = (self.value_[0].replace(var, e),
                self.value_[1].replace(var, e),
                self.value_[2].replace(var, e))
        return self
    def eval_in(self, other_expr):
        return LApp(self, other_expr)
    def is_value(self):
        return False
    def __repr__(self):
        return 'Expr<if'+repr(self.value_)+'>'
    def __str__(self):
        return 'if '+str(self.value_[0])+' then '+str(self.value_[1])+' else '+str(self.value_[2])

class LLambda:
    def __init__(self, x, t, m):
        self.value_ = (x,t,m)
        self.env_ = {}
    def add_judgement(self, var, t):
        self.env_[var] = t
        self.value_[2].add_judgement(var, t)
        self.value_[2].add_judgement(self.value_[0].get(), self.value_[1])
    def get(self):
        return self.value_
    def reduce(self):
        pass
    def value(self):
        self.reduce()
        return self
    def type(self):
        self.reduce()
        return TArrow(self.value_[1], self.value_[2].type())
    def replace(self, var, e):
        self.value_ = (self.value_[0],
                self.value_[1],
                self.value_[2].replace(var, e))
        return self
    def eval_in(self, other_expr):
        if self.value_[1] != other_expr.type():
            exit('Ilegal: el lambda tiene dominio {} y se le está pasando un '
                 'parámetro ({}) de tipo {}.'
                .format(str(self.value_[1]), str(other_expr),
                        other_expr.type()))
        return self.value_[2].replace(self.value_[0].get(), other_expr)
    def is_value(self):
        return True
    def __repr__(self):
        return 'Expr<\\'+str(self.value_)+'>'
    def __str__(self):
        return '\\ '+str(self.value_[0])+' : '+str(self.value_[1])+' . '+str(self.value_[2])

class LApp:
    def __init__(self, fun, arg):
        self.value_ = (fun, arg)
        self.env_ = {}
    def add_judgement(self, var, t):
        self.env_[var] = t
        self.value_[0].add_judgement(var, t)
        self.value_[1].add_judgement(var, t)
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
        t0 = self.value_[0].type()
        t1 = self.value_[1].type()
        if t0.is_arrow() and t0.domain() == t1:
            return t0.codomain()
        exit('Ilegal: la función {} tiene dominio {} y se le está pasando un'
             'parámetro ({}) de tipo {}.'
            .format(str(self.value_[0]), t0.domain(),
                    str(self.value_[1]), self.value_[1].type()))
    def replace(self, var, e):
        self.value_ = (self.value_[0].replace(var, e),
                       self.value_[1].replace(var, e))
        return self
    def eval_in(self, other_expr):
        return LApp(self, other_expr)
    def is_value(self):
        return False
    def __repr__(self):
        return 'Expr<@'+str(self.value_)+'>'
    def __str__(self):
        return str(self.value_[0])+' '+str(self.value_[1])

