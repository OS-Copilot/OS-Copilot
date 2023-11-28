from sympy import symbols, Eq, solve

x, y = symbols('x y')

# 设方程组为：
# 3x + 2y = 2
#  x + 2y = 0
eq1 = Eq(3*x + 2*y, 2)
eq2 = Eq(x + 2*y, 0)

# 使用 solve 解方程组
sol = solve((eq1,eq2), (x, y))
print(sol)