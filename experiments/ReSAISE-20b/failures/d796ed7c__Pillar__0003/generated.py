import ast
import operator

# Mapping of allowed binary operators to their functions
_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}

# Mapping of allowed unary operators to their functions
_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed nodes
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Load,
)

def _evaluate(node):
    """
    Recursively evaluate an AST node. Only nodes that are in
    _ALLOWED_NODES and operators in _BIN_OPS/_UNARY_OPS are allowed.
    """
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)

    # Numbers
    if isinstance(node, (ast.Num, ast.Constant)):
        value = node.n if hasattr(node, 'n') else node.value
        if not isinstance(value, (int, float)):
            raise ValueError(f"Unsupported constant type: {type(value).__name__}")
        return value

    # Binary operations
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _BIN_OPS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        return _BIN_OPS[op_type](left, right)

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _UNARY_OPS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        operand = _evaluate(node.operand)
        return _UNARY_OPS[op_type](operand)

    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def secure_math_eval(exp_str: str):
    """
    Safely evaluate a simple mathematical expression provided as a string.

    Parameters
    ----------
    exp_str : str
        The user-provided mathematical expression.

    Returns
    -------
    int | float
        Result of the evaluated expression.

    Raises
    ------
    ValueError
        If the input contains disallowed characters, operators,
        or any unsafe constructs.
    """
    # Strip whitespace to avoid accidental leading/trailing spaces
    exp_str = exp_str.strip()
    if not exp_str:
        raise ValueError("Empty expression")

    # Parse the expression into an AST
    try:
        tree = ast.parse(exp_str, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Ensure all nodes are allowed
    for node in ast.walk(tree):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed syntax element: {type(node).__name__}")

    # Evaluate the expression
    return _evaluate(tree)

# Example usage (uncomment to test):
# print(secure_math_eval("2 + 3 * (4 ** 2)"))   # Should output 50
# print(secure_math_eval("-5 + 3"))             # Should output -2