import re
import operator
from numbers import Number

operations = []
variables = {}

tests = {
    'test1': "(define x 5)",
    'test2': "(define x (+ 2 2))",
    'test3': "(define x 1) ( + (* 2 x) 7)",
    'test4': "(define x (- 0 5)) (if (< x 0) (define x (* x (- 0 1))))",
    'test5': "(if (= (+ 1 1) 2) (define x 11))",
    'test6': "(/ 5 (* 2 (+ 1 (- 2 1))))",
    'test7': "(()",
    'test8': "())",
    'test9': "(notvalid 2 3)",
    'test9': "(+ x 2)"
}


# Assign a value to a variable
def attribution(var, value):
    variables[var] = value
    return '{var} = {value}'.format(var=var, value=value)


# Conditional statements
def conditional(condition, expression):
    if do_op(condition):
        return do_op(expression)
    else:
        return False


operators = {
    '+':  operator.add,
    '-':  operator.sub,
    '*':  operator.mul,
    '/':  operator.truediv,
    '=':  operator.eq,
    '<':  operator.lt,
    '>':  operator.gt,
    'or':  operator.__or__,
    'and': operator.__and__,
    'define': attribution,
    'if':     conditional,
}

# Validate an expression: Makes sure all brackets are paired
def validate(expr):
    q = []
    index = 0
    for c in expr:
        if c == '(':
            q.append(('(', index))
        if c == ')':
            if not q:
                print("Unexpected ')")
                return False
            q.pop()
        index += 1
    if len(q) != 0:
        print("Missing ')' for '(' at position {position}".format(position=q.pop()[1]))
        return False
    return True


# Remove whitespaces from a tokenized expression
def strip(expr):
    while '' in expr:
        expr.remove('')
    while ' ' in expr:
        expr.remove(' ')


# Split the expression in tokens for parsin
def tokenize(expr):
    expr = re.split('(\W)', expr)
    strip(expr)
    return expr


# Transform the tokenized string into tuples the program can operate on
def make_tuple(expr, i):
    if expr[i] == '(' or expr[i] == ')':
        i = i + 1
    if expr[i].isdigit():
        return int(expr[i]), i
    if expr[i].isalpha() and len(expr[i]) == 1 and expr[i-1] != '(':
        return expr[i], i
    a = expr[i]
    b, i = make_tuple(expr, i+1)
    c, i = make_tuple(expr, i+1)
    return (a, b, c), i+1


# Read all operations from an expression
def parse(expr):
    while expr:
        t, i = make_tuple(expr, 1)
        expr = expr[i+1:]
        operations.append(t)


# Perform an operation
def do_op(op):
    #value
    if isinstance(op, Number) or isinstance(op, bool):
        return op
    # variable
    if isinstance(op, str) and len(op) == 1:
        if op in variables:
            return variables[op]
        else:
            print("{var} is not defined".format(var=op))
    if op[0] == 'define':
        try:
            return operators[op[0]](op[1], do_op(op[2]))
        except Exception:
            pass
    if op[0] == 'if':
        try:
            return operators[op[0]](do_op(op[1]), op[2])
        except Exception:
            pass
    if op[0] in operators:
        try:
            return operators[op[0]](do_op(op[1]), do_op(op[2]))
        except Exception:
            pass
    else:
        return "{op} is not a valid operation".format(op=op[0])


# Evaluate an expression
# Check if it's valid, tokenizes it and does all operations
def eval(expr):
    if validate(expr):
        expr = tokenize(expr)
        parse(expr)
        for op in operations:
            yield do_op(op)


# Run all tests
def alltests():
    for test in tests:
        print(test, tests[test])
        result = eval(tests[test])
        if result != None:
            print(result)
        operations.clear()
        print()


def shell(prompt = 'Enter an expression: '):
    expr = input(prompt)
    while expr != 'quit':
        operations.clear()

        if expr == 'alltests':
            alltests()
            expr = ''

        if expr == 'clear':
            variables.clear()
            expr = ''

        if expr in tests:
            print(tests[expr])
            expr = tests[expr]

        for result in eval(expr):
            if result != None:
                print(result)

        expr = input(prompt)


def main():
    shell()


main()