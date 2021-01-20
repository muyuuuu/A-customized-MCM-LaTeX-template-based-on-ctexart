import sympy as sy


def equation(t, i, u1, u2):
    return -sy.diff(i(t), t, 1) + u1*i(t) + i(t)*(1 - i(t))*u2


u1 = sy.symbols('u1')
u2 = sy.symbols('u2')
t = sy.symbols('t')
i = sy.Function('i')

res = sy.dsolve(equation(t, i, u1, u2), i(t))
print(res)
print()
print('-'*50)
print()
sy.pprint(res)
