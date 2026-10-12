import ast
import operator

# Mapping of allowed operators to their corresponding functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python < 3.8
    ast.Constant,     # Python >= 3.8
    ast.Name,
    ast.Load,
)

# Allowed names (constants only)
_ALLOWED_NAMES = {
    'pi': 3.141592653589793,
    'e' : 2.718281828459045,
}

def _safe_eval(node):
    """Recursively evaluate an AST node if it is safe."""
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)

    if isinstance(node, ast.Constant):  # Python >=3.8
        return node.value

    if isinstance(node, ast.Num):  # Python <3.8
        return node.n

    if isinstance(node, ast.BinOp):
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError("Unsupported binary operator")
        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _safe_eval(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError("Unsupported unary operator")
        return _ALLOWED_OPERATORS[op_type](operand)

    if isinstance(node, ast.Name):
        if node.id not in _ALLOWED_NAMES:
            raise ValueError(f"Name '{node.id}' is not allowed")
        return _ALLOWED_NAMES[node.id]

    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def compute_user_formula(equation: str) -> str:
    """
    Safely evaluate a mathematical expression provided by the user.
    
    Parameters
    ----------
    equation : str
        The user-supplied expression to evaluate.

    Returns
    -------
    str
        String representation of the result, or 'Processing Failed!' on error.
    """
    try:
        # Parse expression into an AST
        parsed = ast.parse(equation, mode='eval')

        # Verify that only allowed nodes are present
        for node in ast.walk(parsed):
            if not isinstance(node, _ALLOWED_NODES):
                raise ValueError(f"Disallowed node type: {type(node).__name__}")

        result = _safe_eval(parsed)
        return str(result)

    except Exception:
        # Any exception results in a failure response
        return 'Processing Failed!'