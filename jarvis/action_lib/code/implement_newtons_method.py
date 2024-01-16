from jarvis.action.base_action import BaseAction
from sympy import symbols, diff, Rational

class implement_newtons_method(BaseAction):
    def __init__(self):
        self._description = "Implement Newton's Method to find a root of the function f(x)."

    def __call__(self, f_expression, x0, denominator_digits, max_iter=100, *args, **kwargs):
        """
        Approximate the roots of the function using Newton's Method starting from x_0.
        Iterate until the denominator of the fraction, when fully reduced, has a specified number of digits.

        Args:
            f_expression (string): The function expression for which the root is to be found.
            x0 (float or sympy expression): The initial guess for the root.
            denominator_digits (int): The number of digits in the denominator to check for.
            max_iter (int, optional): Maximum number of iterations. Defaults to 100.

        Returns:
        tuple: A tuple containing the smallest n where the denominator of the approximation has 25 digits and the corresponding approximation.
               Returns (None, None) if no such n is found within max_iter.
            """
        # Create a symbol x dynamically
        x = symbols('x')

        # Convert the string expression to a sympy expression
        f = eval(f_expression)

        # First derivative of the function
        f_prime = diff(f, x)

        for n in range(max_iter):
            # Calculate the next approximation
            x1 = x0 - f.subs(x, x0)/f_prime.subs(x, x0)

            # Check if the denominator has the specified number of digits when the fraction is fully reduced
            if len(str(Rational(x1).q)) >= denominator_digits:
                return n + 1, x1  # n + 1 because we start counting from 1

            x0 = x1

        return None, None

# Example of how to use the class (this should be in the comments):
# newtons_method = implement_newtons_method()
# n, approximation = newtons_method(f_expression="x**3 - 5*x**2 + 2*x", x0=1, denominator_digits=25, max_iter=100)