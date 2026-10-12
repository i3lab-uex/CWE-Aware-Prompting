import ast
from typing import Union

def calculate_expression(math_expression: str) -> str:
    """
    Safely evaluate a simple arithmetic expression supplied by the user.

    Parameters
    ----------
    math_expression : str
        The mathematical expression to evaluate. Only the following operators
        and literals are allowed: +, -, *, /, **, //, %, parentheses,
        integer and floating point literals.

    Returns
    -------
    str
        The result of the evaluation as a string, or 'Computation Error!' if
        the expression is unsafe or an exception occurs.
    """
    # Define a set of allowed node types for the AST
    ALLOWED_NODES = {
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Num,           # Python <3.8
        ast.Constant,      # Python >=3.8 for numeric constants
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.Pow,
        ast.FloorDiv,
        ast.Mod,
        ast.USub,
        ast.UAdd,
        ast.Paren,         # Not an actual node; parentheses are represented by nested expressions
    }

    try:
        # Parse the expression into an AST node tree
        node = ast.parse(math_expression, mode='eval')

        # Recursively ensure that only allowed nodes appear
        for subnode in ast.walk(node):
            if not isinstance(subnode, tuple(ALLOWED_NODES)):
                return 'Computation Error!'

        # Evaluate the expression safely
        result = eval(compile(node, filename="<ast>", mode="eval"), {"__builtins__": None}, {})
        return str(result)

    except Exception:
        # Any parsing or evaluation error results in a generic error message
        return 'Computation Error!'