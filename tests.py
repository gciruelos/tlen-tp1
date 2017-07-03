#!/usr/bin/python3
from lambda_calculus import parse, lex

tests = [
    ('0', '0', 'Nat'),
    ('true', 'true', 'Bool'),
    ('if true then 0 else false', None, None),
    ('\\x:Bool.if x then false else true', '\ x : Bool . if x then false else true', 'Bool -> Bool'),
    ('\\x:Nat.succ(0)', '\ x : Nat . 1', 'Nat -> Nat'),
    ('\\z:Nat.z', '\ z : Nat . z', 'Nat -> Nat'),
    ('(\\x:Bool.succ(x)) true', None, None),
    ('succ(succ(succ(0)))', '3', 'Nat'),
    ('x', None, None),
    ('succ(succ(pred(0)))', '2', 'Nat'),
    ('0 0', None, None),
    ('\\x:Nat->Nat.\\y:Nat.(\\z:Bool.if z then x y else 0)', '\ x : Nat -> Nat . \ y : Nat . \ z : Bool . if z then x y else 0', '(Nat -> Nat) -> Nat -> Bool -> Nat'),
    ('(\\x:Nat->Nat.\\y:Nat.(\\z:Bool.if z then x y else 0)) (\\j:Nat.succ(j)) succ(succ(succ(succ(succ(succ(succ(succ(0)))))))) true', '9', 'Nat'),
    # Nuestros tests.
    ('(\\z:Nat. pred(z)) ((\\x:Nat->Nat. x succ(succ(0))) \\y:Nat. y)', '1', 'Nat'),
    ('(\\x:Nat.succ(x)) 0 0', None, None),
    ('(\\x:Nat->Nat. x succ(succ(0))) \y:Nat. y', '2', 'Nat'),
    ('(\\x:Nat. if iszero(x) then succ(x) else pred(x)) pred(0)', '1', 'Nat'),
    ('(\\x:Nat. if iszero(x) then succ(x) else pred(x)) succ(0)', '0', 'Nat'),
    ('(\\x:Nat. if iszero(x) then succ(x) then pred(x)) succ(0)', None, None),
]



for test in tests:
    try:
        p = parse(test[0])
        if str(p.value()) == test[1] and str(p.type()) == test[2]:
            print('PASSED', test[0])
        else:
            print('FAILED', test[0])
            if str(p.value()) != test[1]:
                print('Got', str(p.value()), 'but expected', test[1])
            if str(p.type()) != test[2]:
                print('Got', str(p.type()), 'but expected', test[2])
    except:
        if test[1] is None:
            print('PASSED', test[0])
        else:
            print('FAILED', test[0])

