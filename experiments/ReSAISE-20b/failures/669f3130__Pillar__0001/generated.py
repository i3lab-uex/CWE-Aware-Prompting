import ast
import operator

# Map AST operators to actual functions
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

# Allowed nodes
_ALLOWED_NODES = (
    ast.Expression,  # top-level node
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Name,
    ast.Load,
)

# Only allow the following names (e.g., math constants)
_ALLOWED_NAMES = {
    'pi': 3.141592653589793,
    'e' : 2.718281828459045,
}

def _evaluate(node):
    """
    Recursively evaluate an AST node. Only permitted arithmetic expressions are allowed.
    Raises ValueError if disallowed nodes or names are encountered.
    """
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)

    # Numbers
    if isinstance(node, (ast.Num, ast.Constant)):
        return node.n

    # Variables/constants
    if isinstance(node, ast.Name):
        if node.id in _ALLOWED_NAMES:
            return _ALLOWED_NAMES[node.id]
        raise ValueError(f"Disallowed name: {node.id}")

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Disallowed operator: {op_type.__name__}")

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Disallowed unary operator: {op_type.__name__}")

    # Any other node is disallowed
    raise ValueError(f"Disallowed AST node: {type(node).__name__}")

def exec_calculation(calc_string: str) -> str:
    """
    Safely evaluate a simple arithmetic expression provided by the user.
    Returns the result as a string, or 'Computation Error!' on failure.
    """
    try:
        # Parse expression without evaluating
        parsed = ast.parse(calc_string, mode='eval')

        # Verify all nodes are allowed
        for node in ast.walk(parsed):
            if not isinstance(node, _ALLOWED_NODES):
                raise ValueError(f"Disallowed node detected: {type(node).__name__}")

        result = _evaluate(parsed)
        return str(result)

    except Exception:
        # Any exception results in a generic error message
        return 'Computation Error!'