import ast
from typing import Any

def execute_user_input(user_input: str) -> str:
    """
    Safely evaluate a user supplied arithmetic expression.

    Parameters
    ----------
    user_input : str
        Expression to evaluate. Only basic arithmetic (+, -, *, /, **, //, %, parentheses)
        and numeric literals are allowed.

    Returns
    -------
    str
        The result of the expression converted to string, or 'Processing Failed!' if
        evaluation fails or the input contains disallowed content.
    """
    # Strip whitespace and check for empty string
    expr = user_input.strip()
    if not expr:
        return "Processing Failed!"

    # Allowed node types for a safe expression
    allowed_nodes = {
        ast.Expression, ast.BinOp, ast.UnaryOp,
        ast.Num, ast.Constant,  # constant numeric values
        ast.Add, ast.Sub, ast.Mult,
        ast.Div, ast.FloorDiv, ast.Mod, ast.Pow,
        ast.UAdd, ast.USub,
        ast.Paren := None  # placeholder; parentheses are implicit in the AST
    }

    try:
        # Parse expression into an AST
        parsed = ast.parse(expr, mode='eval')

        # Recursively ensure all nodes are allowed
        for node in ast.walk(parsed):
            if type(node) not in allowed_nodes:
                # Disallow anything else (e.g., function calls, attribute access)
                return "Processing Failed!"

        # Evaluate safely: no builtins or globals
        result = eval(compile(parsed, filename="<ast>", mode="eval"),
                      {"__builtins__": None}, {})
        return str(result)

    except Exception:
        # Any error (syntax, division by zero, etc.) results in failure
        return "Processing Failed!"