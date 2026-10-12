import ast
import operator as op

# Mapping of supported operators to their functions
_ALLOWED_BINOPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}

_ALLOWED_UNARYOPS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed numeric literal types (Python 3.8+ uses ast.Constant)
_ALLOWED_NUMERIC_TYPES = (int, float)

def _eval_node(node):
    """
    Recursively evaluate an AST node.
    Raises ValueError if the node contains unsupported elements.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Numeric literal
    if isinstance(node, ast.Constant):
        if not isinstance(node.value, _ALLOWED_NUMERIC_TYPES):
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
        return node.value

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_BINOPS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        return _ALLOWED_BINOPS[op_type](left, right)

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_UNARYOPS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return _ALLOWED_UNARYOPS[op_type](operand)

    # Parentheses are represented by nested expressions; no separate node type needed

    raise ValueError(f"Unsupported expression component: {ast.dump(node)}")

def compute_expression(expr: str):
    """
    Evaluate a mathematical expression given as a string.

    Parameters
    ----------
    expr : str
        The expression to evaluate. Only basic arithmetic operators (+, -, *, /,
        //, %, **) and numeric literals are allowed.

    Returns
    -------
    int | float
        The result of the evaluated expression.

    Raises
    ------
    ValueError
        If the expression contains unsupported operators, unsafe code, or if evaluation fails.
    """
    # Strip whitespace to simplify parsing
    expr = expr.strip()
    if not expr:
        raise ValueError("Empty expression")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Ensure the parsed tree only contains allowed nodes
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Module,)):
            continue  # top-level container
        if not isinstance(node, (
                ast.Expression,
                ast.BinOp,
                ast.UnaryOp,
                ast.Constant,
                ast.Expr,
                ast.Load,
                ast.Expression
            )):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Evaluate the parsed AST safely
    return _eval_node(parsed)

# Example usage (uncomment to test):
# if __name__ == "__main__":
#     print(compute_expression("2 + 3 * (4 - 1) / 5**2"))