import ast
from typing import Any

def calculate_expression(expr_input: str) -> str:
    """
    Safely evaluate a simple arithmetic expression supplied by the user.

    Parameters
    ----------
    expr_input : str
        The mathematical expression to evaluate. Only supports +, -, *, /,
        //, %, ** and parentheses.

    Returns
    -------
    str
        The result as a string if evaluation succeeds, otherwise an error
        message. Any suspicious or unsafe input triggers the generic
        'Computation Error!' response.
    """
    # Strip whitespace to reduce accidental formatting issues
    expr = expr_input.strip()

    # Define allowed AST node types for a safe subset of Python expressions
    allowed_nodes = {
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Num,          # Python <3.8
        ast.Constant,     # Python >=3.8
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.FloorDiv,
        ast.Mod,
        ast.Pow,
        ast.UAdd,
        ast.USub,
        ast.Paren,        # Not a real node; parentheses are handled by grouping
    }

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError:
        return 'Computation Error!'

    # Recursively ensure that only allowed nodes are present
    def _check(node: ast.AST) -> bool:
        if type(node) not in allowed_nodes:
            return False
        for child in ast.iter_child_nodes(node):
            if not _check(child):
                return False
        return True

    if not _check(parsed):
        return 'Computation Error!'

    # Evaluate the expression safely
    try:
        result: Any = eval(compile(parsed, filename="<ast>", mode="eval"))
    except Exception:
        return 'Computation Error!'

    # Ensure the result is a number (int or float)
    if isinstance(result, (int, float)):
        return str(result)
    else:
        return 'Computation Error!'