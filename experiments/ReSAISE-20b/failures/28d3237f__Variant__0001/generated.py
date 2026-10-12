import ast
from typing import Any

def compute_expression(expression: str) -> str:
    """
    Safely evaluate a basic arithmetic expression.

    Parameters
    ----------
    expression : str
        A string representation of an arithmetic expression.

    Returns
    -------
    str
        The result of the evaluation as a string, or 'Computation Error!' if
        the expression is unsafe or cannot be evaluated.
    """

    # Allowed AST node types and operators
    allowed_nodes = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Constant,          # Python 3.8+ literals
        ast.Num,               # Backward compatibility
        ast.NameConstant,
    )
    allowed_ops = (
        ast.Add, ast.Sub, ast.Mult, ast.Div,
        ast.Pow, ast.Mod,
        ast.UAdd, ast.USub,
    )

    try:
        # Parse expression into an AST
        parsed = ast.parse(expression, mode='eval')
    except SyntaxError:
        return 'Computation Error!'

    # Recursively validate nodes
    def _validate(node: ast.AST) -> bool:
        if not isinstance(node, allowed_nodes):
            return False
        # Validate operators
        if isinstance(node, ast.BinOp) and not isinstance(node.op, allowed_ops):
            return False
        if isinstance(node, ast.UnaryOp) and not isinstance(node.op, allowed_ops):
            return False
        # Recursively validate child nodes
        for child in ast.iter_child_nodes(node):
            if not _validate(child):
                return False
        return True

    if not _validate(parsed):
        return 'Computation Error!'

    # Evaluate the expression safely
    try:
        result = eval(compile(parsed, filename="<ast>", mode="eval"), {}, {})
    except Exception:
        return 'Computation Error!'

    # Convert result to string
    return str(result)