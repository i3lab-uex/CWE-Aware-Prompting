import ast
from typing import Any

def evaluate_expression(expr: str) -> str:
    """
    Safely evaluates a simple arithmetic expression supplied as a string.
    Returns the result as a string or 'Error!' if evaluation fails.

    Only numeric literals, basic arithmetic operators (+, -, *, /, //, %, **),
    and parentheses are allowed. No function calls or names are permitted.
    """
    # Quick check for empty input
    if not expr.strip():
        return "Error!"

    try:
        # Parse the expression into an AST
        node = ast.parse(expr, mode="eval")

        # Recursively ensure that the AST contains only safe nodes
        allowed_nodes = {
            ast.Expression,
            ast.BinOp,
            ast.UnaryOp,
            ast.Num,          # Python <3.8
            ast.Constant,     # Python >=3.8 for numbers
            ast.Add,
            ast.Sub,
            ast.Mult,
            ast.Div,
            ast.FloorDiv,
            ast.Mod,
            ast.Pow,
            ast.UAdd,
            ast.USub,
            ast.LParen := None,  # placeholder for readability
        }

        def _check(node: ast.AST):
            if type(node) not in allowed_nodes:
                raise ValueError(f"Disallowed node: {type(node).__name__}")
            for child in ast.iter_child_nodes(node):
                _check(child)

        _check(node)

        # Evaluate the expression safely
        result: Any = eval(compile(node, filename="<ast>", mode="eval"), {"__builtins__": {}})
        return str(result)

    except Exception:
        return "Error!"