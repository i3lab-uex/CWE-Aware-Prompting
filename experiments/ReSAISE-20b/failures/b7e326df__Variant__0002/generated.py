import ast
from typing import Any

def execute_user_input(expr: str) -> str:
    """
    Safely evaluate a user supplied Python expression.

    Parameters
    ----------
    expr : str
        The user supplied expression to evaluate.

    Returns
    -------
    str
        The string representation of the evaluation result, or 'Error!'
        if the expression is unsafe or raises an exception.
    """
    # Quick sanity checks
    if not isinstance(expr, str) or not expr.strip():
        return "Error!"

    # Try to parse the expression first
    try:
        parsed = ast.parse(expr, mode="eval")
    except SyntaxError:
        return "Error!"

    # Ensure that only safe nodes are present
    SAFE_NODES = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.BoolOp,
        ast.Compare,
        ast.Call,          # allow function calls but will be restricted
        ast.Num,
        ast.Str,
        ast.Constant,      # Python 3.8+
        ast.Name,
        ast.List,
        ast.Tuple,
        ast.Dict,
        ast.Set,
        ast.Index,
        ast.Subscript,
        ast.Slice,
        ast.Load,
    )

    for node in ast.walk(parsed):
        if not isinstance(node, SAFE_NODES):
            return "Error!"
        # Disallow attribute access and any function calls
        if isinstance(node, ast.Call):
            return "Error!"
        if isinstance(node, ast.Attribute):
            return "Error!"

    # Prepare safe eval environment
    SAFE_GLOBALS = {
        "__builtins__": {},  # no builtins
    }

    try:
        result: Any = eval(compile(parsed, filename="<ast>", mode="eval"),
                           SAFE_GLOBALS,
                           {})
        return str(result)
    except Exception:
        return "Error!"