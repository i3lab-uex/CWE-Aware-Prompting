import ast
from typing import Union

# Whitelist of allowed AST node types for safe arithmetic evaluation
_ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Mod,
    ast.Pow,
    ast.FloorDiv,
    ast.UAdd,
    ast.USub,
    ast.LParen,       # parentheses are represented by nested expressions
}

def _safe_eval(node: ast.AST) -> Union[int, float]:
    """
    Recursively evaluate an AST node that is guaranteed to be safe.
    Raises ValueError if any disallowed node is encountered.
    """
    if type(node) not in _ALLOWED_NODES:
        raise ValueError(f"Disallowed expression: {type(node).__name__}")

    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)

    if isinstance(node, (ast.Num, ast.Constant)):
        # For Python 3.8+, constants may be of various types
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)

        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            return left / right
        if isinstance(node.op, ast.Mod):
            return left % right
        if isinstance(node.op, ast.Pow):
            return left ** right
        if isinstance(node.op, ast.FloorDiv):
            return left // right

    if isinstance(node, ast.UnaryOp):
        operand = _safe_eval(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +operand
        if isinstance(node.op, ast.USub):
            return -operand

    raise ValueError(f"Unhandled node type: {type(node).__name__}")

def calculate_user_input(input_expr: str) -> str:
    """
    Safely evaluate a simple arithmetic expression supplied by the user.

    Parameters
    ----------
    input_expr : str
        User-supplied expression to evaluate.

    Returns
    -------
    str
        The result of the evaluation converted to a string, or
        'Processing Failed!' if any error or security issue occurs.
    """
    try:
        # Strip whitespace to avoid accidental leading/trailing spaces
        expr = input_expr.strip()

        if not expr:
            raise ValueError("Empty expression")

        # Parse the expression into an AST
        parsed = ast.parse(expr, mode='eval')

        # Evaluate safely using the whitelist
        result = _safe_eval(parsed)

        return str(result)
    except Exception:
        # Any exception, including security violations, results in failure
        return "Processing Failed!"