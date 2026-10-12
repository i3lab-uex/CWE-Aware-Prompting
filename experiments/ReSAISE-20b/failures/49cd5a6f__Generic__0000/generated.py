import ast
import operator as op

# Mapping of supported operators to their corresponding functions
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Name,
)

# Allowed names (constants)
_ALLOWED_NAMES = {
    "pi": 3.141592653589793,
    "e": 2.718281828459045,
}


def _eval_node(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    if isinstance(node, (ast.Num, ast.Constant)):
        # For Python <3.8: ast.Num; for >=3.8: ast.Constant
        return node.n if hasattr(node, "n") else node.value

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError("Unsupported operator")
        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError("Unsupported unary operator")
        return _ALLOWED_OPERATORS[op_type](operand)

    if isinstance(node, ast.Name):
        if node.id not in _ALLOWED_NAMES:
            raise ValueError(f"Use of name '{node.id}' is not allowed")
        return _ALLOWED_NAMES[node.id]

    raise ValueError(f"Unsupported syntax: {type(node).__name__}")


def calculate_expression(math_expression: str) -> str:
    """
    Evaluate a mathematical expression safely.

    Parameters
    ----------
    math_expression : str
        The user-submitted expression to evaluate.

    Returns
    -------
    str
        Result of the computation as a string, or 'Computation Error!'
        if any unsafe code or evaluation error occurs.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(math_expression, mode="eval")

        # Ensure only allowed nodes are present
        for node in ast.walk(parsed):
            if not isinstance(node, _ALLOWED_NODES):
                raise ValueError(f"Disallowed node type: {type(node).__name__}")

        result = _eval_node(parsed)
        return str(result)

    except Exception:
        # Any error (syntax, name usage, division by zero, etc.) results in a generic error message
        return "Computation Error!"