import re
import operator
from numbers import Number


#test_expr = "(define x 5) ( + (* 2 x) 7)"
#test_expr = "(define x 5) (if (and (= 5 5) (= 6 6)) (define x 7))"
test_expr = "(not (= 5 5))"
operations = []
variables = {}


def attribution(var, value):
    variables[var] = value
    return "%s = %d" % (var, value)


def conditional(condition, expression):
    if do_op(condition):
        return do_op(expression)
    else:
        return False


operators = {
    '+':  operator.add,
    '-':  operator.sub,
    '*':  operator.mul,
    '**': operator.pow,
    '/':  operator.truediv,
    '=':  operator.eq,
    '!=': operator.ne,
    '<':  operator.lt,
    '<=': operator.le,
    '>':  operator.gt,
    '>=': operator.ge,
    'abs': operator.abs,
    'mod': operator.mod,
    'or': operator.__or__,
    'and': operator.__and__,
    'not': operator.__not__,
    'define': attribution,
    'if':     conditional,

}


def validate(expr):
    q = []
    for c in expr:
        if c == '(':
            q.append('(')
        if c == ')':
            if not q:
                return False
            q.pop()
    if q:
        return False
    return True


def strip(expr):
    while '' in expr:
        expr.remove('')
    while ' ' in expr:
        expr.remove(' ')


def tokenize(expr):
    expr = re.split('(\W)', expr)
    strip(expr)
    return expr


def make_tuple(expr, i):
    if expr[i] == '(' or expr[i] == ')':
        i = i + 1

    if expr[i].isdigit():
        return int(expr[i]), i

    if expr[i].isalpha() and len(expr[i]) == 1:
        return expr[i], i

    a = expr[i]
    b, i = make_tuple(expr, i+1)
    c, i = make_tuple(expr, i+1)

    return (a, b, c), i+1


def parse(expr):
    while expr:
        t, i = make_tuple(expr, 1)
        expr = expr[i+1:]
        operations.append(t)


def do_op(op):
    if isinstance(op, Number) or isinstance(op, bool):
        return op

    if isinstance(op, str):
        if op in variables:
            return variables[op]
        else:
            return op

    if op[0] == 'define':
        return operators[op[0]](op[1], do_op(op[2]))
    if operators[op[0]]
    return operators[op[0]](do_op(op[1]), do_op(op[2]))


def main():
    expr = tokenize(test_expr)
    parse(expr)
    print(operations)
    for op in operations:
        print(do_op(op))


main()
