import ast
import operator

# Mapping of allowed operators to their functions
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

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,  # root
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,         # Python <3.8
    ast.Constant,    # Python 3.8+
    ast.Name,
)

# Whitelist of safe names (e.g., math constants)
_ALLOWED_NAMES = {
    'pi': 3.141592653589793,
    'e' : 2.718281828459045,
}

def _evaluate(node):
    """Recursively evaluate an AST node safely."""
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)

    if isinstance(node, (ast.Num, ast.Constant)):
        # Numbers only
        return node.n if hasattr(node, 'n') else node.value

    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError("Unsupported binary operator")
        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError("Unsupported unary operator")
        return _ALLOWED_OPERATORS[op_type](operand)

    if isinstance(node, ast.Name):
        id = node.id
        if id in _ALLOWED_NAMES:
            return _ALLOWED_NAMES[id]
        raise ValueError(f"Use of untrusted name: {id}")

    # Any other node type is disallowed
    raise ValueError(f"Disallowed expression: {ast.dump(node)}")

def securely_compute_expression(formula: str) -> str:
    """
    Safely evaluate a mathematical expression provided as a string.
    
    Parameters
    ----------
    formula : str
        The user supplied expression.

    Returns
    -------
    str
        The string representation of the computed result or 
        'Processing Failed!' if the expression is unsafe or errors occur.
    """
    try:
        # Parse into an AST
        parsed = ast.parse(formula, mode='eval')

        # Ensure all nodes are allowed
        for node in ast.walk(parsed):
            if not isinstance(node, _ALLOWED_NODES):
                return 'Processing Failed!'

        result = _evaluate(parsed)
        # Convert to string (could be int, float, etc.)
        return str(result)

    except Exception:
        # Any exception is treated as failure
        return 'Processing Failed!'