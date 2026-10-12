import ast
import operator

# Supported operators mapping
_OPERATOR_MAP = {
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

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,  # top-level container
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Name,
    ast.Load,
)

# Only allow numeric constants and the variable 'pi' or 'e'
_ALLOWED_NAMES = {'pi': 3.141592653589793, 'e': 2.718281828459045}

def _evaluate(node):
    """Recursively evaluate a parsed AST node safely."""
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)

    if isinstance(node, ast.Constant):  # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")

    if isinstance(node, ast.Num):  # Python <3.8
        return node.n

    if isinstance(node, ast.Name):
        if node.id in _ALLOWED_NAMES:
            return _ALLOWED_NAMES[node.id]
        raise ValueError(f"Unknown identifier: {node.id}")

    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        op_type = type(node.op)
        if op_type in _OPERATOR_MAP:
            return _OPERATOR_MAP[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type}")

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        op_type = type(node.op)
        if op_type in _OPERATOR_MAP:
            return _OPERATOR_MAP[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type}")

    raise ValueError(f"Unsupported AST node type: {type(node)}")

def calculate_expression(ex_string: str) -> str:
    """
    Safely evaluate a basic arithmetic expression.

    Parameters
    ----------
    ex_string : str
        String representation of the mathematical expression to evaluate.

    Returns
    -------
    str
        The result as a string, or 'Computation Error!' if evaluation fails.
    """
    try:
        # Parse expression into AST
        parsed = ast.parse(ex_string, mode='eval')

        # Verify all nodes are allowed
        for node in ast.walk(parsed):
            if not isinstance(node, _ALLOWED_NODES):
                raise ValueError(f"Disallowed node: {type(node)}")

        # Evaluate safely
        result = _evaluate(parsed)
        return str(result)

    except Exception:
        # Any error results in a generic computation failure message
        return 'Computation Error!'