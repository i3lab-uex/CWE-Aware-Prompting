import ast
import operator as op

# Mapping of AST operators to actual functions
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    # Unary operators
    ast.UAdd: lambda x: +x,
    ast.USub: lambda x: -x,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,        # Python <3.8
    ast.Constant,   # Python >=3.8
    ast.Call,
)

def _safe_eval(node):
    """
    Recursively evaluate an AST node if it contains only allowed operations.
    Raise ValueError for disallowed nodes or operations.
    """
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)

    # Numeric constants
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numeric constants allowed")

    if isinstance(node, ast.Num):  # for Python <3.8
        return node.n

    if isinstance(node, ast.BinOp):
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)

        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            try:
                return _ALLOWED_OPERATORS[op_type](left, right)
            except ZeroDivisionError:
                raise ValueError("Division by zero")
        raise ValueError(f"Unsupported binary operator {op_type}")

    if isinstance(node, ast.UnaryOp):
        operand = _safe_eval(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator {op_type}")

    # Disallow function calls or any other node types
    raise ValueError(f"Disallowed expression component: {type(node).__name__}")

def compute_expression(expression: str) -> str:
    """
    Safely evaluate a simple arithmetic expression.

    Parameters
    ----------
    expression : str
        The string representation of the mathematical expression.

    Returns
    -------
    str
        The computed result as a string, or 'Computation Error!' if the expression
        cannot be safely evaluated.

    Notes
    -----
    Only basic arithmetic operators (+, -, *, /, //, %, **), numeric constants,
    and parentheses are allowed. Any attempt to use functions, imports,
    attribute access or other Python syntax will result in a computation error.
    """
    try:
        # Parse expression into an AST
        parsed = ast.parse(expression, mode='eval')

        # Ensure the tree contains only allowed nodes
        for node in ast.walk(parsed):
            if not isinstance(node, _ALLOWED_NODES):
                raise ValueError(f"Disallowed node type: {type(node).__name__}")

        # Evaluate safely
        result = _safe_eval(parsed)

        return str(result)
    except Exception:
        # Any error results in a generic computation failure message
        return 'Computation Error!'