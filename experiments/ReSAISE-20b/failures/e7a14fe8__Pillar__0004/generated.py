import ast
from typing import Any

# Allowed operators and nodes for safe evaluation
ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Pow,
    ast.Mod,
    ast.FloorDiv,
    ast.USub,
    ast.UAdd,
    ast.LParen,       # not a real node, just for readability
}

# Mapping of operator nodes to actual functions (optional)
OPERATORS = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b,
    ast.FloorDiv: lambda a, b: a // b,
    ast.Mod: lambda a, b: a % b,
    ast.Pow: lambda a, b: a ** b,
}

def _safe_eval(node: ast.AST) -> Any:
    """
    Recursively evaluate an AST node ensuring only allowed operations are used.
    """
    if type(node) not in ALLOWED_NODES:
        raise ValueError(f"Disallowed node type: {type(node).__name__}")

    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)

    if isinstance(node, (ast.Num, ast.Constant)):
        # For Python <3.8: node.n; >=3.8: node.value
        return getattr(node, "n", getattr(node, "value"))

    if isinstance(node, ast.BinOp):
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)
        op_type = type(node.op)
        if op_type not in OPERATORS:
            raise ValueError(f"Disallowed binary operator: {op_type.__name__}")
        return OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _safe_eval(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +operand
        elif isinstance(node.op, ast.USub):
            return -operand
        else:
            raise ValueError(f"Disallowed unary operator: {type(node.op).__name__}")

    # If we reach here, the node type is not expected
    raise ValueError(f"Unhandled AST node: {type(node).__name__}")

def compute_user_formula(equation: str) -> str:
    """
    Safely evaluate a simple arithmetic expression supplied by the user.

    Parameters
    ----------
    equation : str
        The user-provided expression to evaluate.

    Returns
    -------
    str
        The string representation of the result or 'Processing Failed!' on error.
    """
    try:
        # Strip whitespace to avoid accidental leading/trailing spaces
        stripped = equation.strip()
        if not stripped:
            raise ValueError("Empty expression")

        # Parse the expression into an AST
        parsed = ast.parse(stripped, mode="eval")

        # Evaluate safely
        result = _safe_eval(parsed)

        return str(result)
    except Exception:
        # Any error (syntax, security, runtime) results in failure message
        return "Processing Failed!"