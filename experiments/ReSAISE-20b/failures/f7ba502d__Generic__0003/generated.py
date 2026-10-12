import ast
import operator as op

# Supported operators mapping to their corresponding functions
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.FloorDiv: op.floordiv,
}

# Supported unary operators
_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed numeric constants (int, float)
_ALLOWED_NUMERIC_TYPES = (int, float)


def _eval_node(node: ast.AST):
    """
    Recursively evaluate an AST node.
    Only allows safe arithmetic operations and numeric literals.
    Raises ValueError for any unsupported nodes or types.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Numeric literal (Python 3.8+ uses Constant)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, _ALLOWED_NUMERIC_TYPES):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    # Binary operation
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)

        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    # Unary operation
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_UNARY_OPERATORS:
            return _ALLOWED_UNARY_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    # Parenthesized expressions are just the inner expression
    if isinstance(node, ast.Paren):
        return _eval_node(node.value)

    raise ValueError(f"Unsupported expression component: {type(node).__name__}")


def safe_eval_expression(expr: str):
    """
    Safely evaluate a mathematical expression provided as a string.

    Parameters
    ----------
    expr : str
        The user-supplied mathematical expression to evaluate.

    Returns
    -------
    result : int or float
        The numeric result of evaluating the expression.

    Raises
    ------
    ValueError
        If the input contains invalid characters, unsupported operations,
        or if the expression is syntactically incorrect.
    """
    # Strip whitespace to avoid accidental leading/trailing spaces
    expr = expr.strip()
    if not expr:
        raise ValueError("Empty expression")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode="eval")
    except SyntaxError as e:
        raise ValueError(f"Syntax error in expression: {e}") from None

    # Evaluate the parsed AST safely
    return _eval_node(parsed)