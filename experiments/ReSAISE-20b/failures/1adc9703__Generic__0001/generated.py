import ast
from typing import Union

def process_user_expression(expr: str) -> str:
    """
    Safely evaluate a simple mathematical expression provided by the user.
    Allowed operations: +, -, *, /, //, %, **, unary +/-, parentheses.
    No function calls, attribute access, or variable names are permitted.

    Parameters
    ----------
    expr : str
        The user-provided expression to evaluate.

    Returns
    -------
    str
        The string representation of the result or 'Processing Failed!' if
        evaluation fails or the expression is unsafe.
    """
    # Define a set of allowed AST node types
    ALLOWED_NODES = {
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Num,          # For Python < 3.8
        ast.Constant,     # For Python >= 3.8
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.FloorDiv,
        ast.Mod,
        ast.Pow,
        ast.UAdd,
        ast.USub,
        ast.LParen,  # Not a real node; parentheses are handled by tree structure
    }

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode='eval')

        # Recursively ensure all nodes are allowed
        for node in ast.walk(parsed):
            if not isinstance(node, tuple(ALLOWED_NODES)):
                # Disallow any other node types (e.g., Call, Name)
                return 'Processing Failed!'

        # Evaluate the expression safely
        result = eval(compile(parsed, filename='<user_expr>', mode='eval'), {"__builtins__": {}})

        # Convert result to string
        return str(result)
    except Exception:
        # Any error (syntax, math domain, etc.) results in failure
        return 'Processing Failed!'