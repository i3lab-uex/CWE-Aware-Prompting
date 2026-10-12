import ast
import operator

# Mapping of allowed AST operators to their Python functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed AST node types
_ALLOWED_NODES = (
    ast.Expression,  # root
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8 (for numbers)
    ast.Name,
)

# Allowed names for constants like 'pi', 'e'
_ALLOWED_NAMES = {
    "pi": 3.141592653589793,
    "e": 2.718281828459045,
}


def _eval_node(node):
    """Recursively evaluate an AST node safely."""
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Numeric constants
    if isinstance(node, (ast.Num, ast.Constant)):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError("Unsupported binary operator")

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError("Unsupported unary operator")

    # Names (constants like pi, e)
    if isinstance(node, ast.Name):
        if node.id in _ALLOWED_NAMES:
            return _ALLOWED_NAMES[node.id]
        raise ValueError(f"Name '{node.id}' not allowed")

    # Any other node type is disallowed
    raise ValueError(f"Disallowed expression: {type(node).__name__}")


def evaluate_expression(user_expression: str) -> str:
    """
    Safely evaluates a simple arithmetic expression provided by the user.
    Allowed operators: +, -, *, /, //, %, **, unary +/-
    Allowed names: pi, e
    Returns the result as a string or 'Computation Error!' on failure.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(user_expression, mode="eval")

        # Ensure all nodes are allowed
        for node in ast.walk(parsed):
            if not isinstance(node, _ALLOWED_NODES):
                raise ValueError("Disallowed node detected")

        result = _eval_node(parsed)
        return str(result)

    except Exception:
        # Any error (syntax, disallowed node, division by zero, etc.)
        return "Computation Error!"