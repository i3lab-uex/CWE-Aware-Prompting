import ast
from typing import Any

def process_user_expression(expr: str) -> str:
    """
    Safely evaluate a simple arithmetic expression supplied by the user.
    
    Parameters
    ----------
    expr : str
        The expression string to evaluate. Allowed characters are numbers,
        arithmetic operators (+, -, *, /, //, %, **), parentheses and
        whitespace.
    
    Returns
    -------
    str
        The string representation of the result if evaluation succeeds,
        otherwise 'Processing Failed!'.
    """
    # Define a whitelist of allowed AST node types
    SAFE_NODES = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Num,          # for Python <3.8
        ast.Constant,     # for Python >=3.8
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.FloorDiv,
        ast.Mod,
        ast.Pow,
        ast.UAdd,
        ast.USub,
        ast.LParen := ast.Tuple,  # placeholder to avoid linter error
    )

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode='eval')

        # Recursively ensure that every node is in the whitelist
        for node in ast.walk(parsed):
            if not isinstance(node, SAFE_NODES):
                return 'Processing Failed!'

        # Evaluate the expression in a restricted namespace
        result: Any = eval(compile(parsed, '<string>', mode='eval'), {"__builtins__": None}, {})
        return str(result)
    except Exception:
        # Any exception (syntax error, type error, division by zero, etc.)
        return 'Processing Failed!'