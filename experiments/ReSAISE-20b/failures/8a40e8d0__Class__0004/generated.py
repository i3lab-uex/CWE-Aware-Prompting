import ast
import operator

# Allowed binary operators mapping to their functions
_ALLOWED_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Allowed unary operators
_ALLOWED_UNOPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _eval_node(node):
    """
    Recursively evaluate an AST node. Only numeric literals and
    allowed arithmetic operations are permitted.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Literal numbers (int/float)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")

    # Binary operations (e.g., 1 + 2)
    if isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_BINOPS:
            raise ValueError("Unsupported binary operator")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return _ALLOWED_BINOPS[type(node.op)](left, right)

    # Unary operations (e.g., -5)
    if isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_UNOPS:
            raise ValueError("Unsupported unary operator")
        operand = _eval_node(node.operand)
        return _ALLOWED_UNOPS[type(node.op)](operand)

    # Parenthesized expressions are just the inner expression
    if isinstance(node, ast.Paren):
        return _eval_node(node.value)

    # Disallow any other node types
    raise ValueError("Unsupported expression element")

def evaluate_expression(expr_string: str) -> str:
    """
    Safely evaluates a simple arithmetic expression supplied by the user.

    Parameters
    ----------
    expr_string : str
        The user‑supplied expression to evaluate.

    Returns
    -------
    str
        The result of the evaluation as a string, or an error message.

    Raises
    ------
    None.  Any failure results in the string 'Computation Error!'.
    """
    try:
        # Parse expression into an AST; fail if syntax is invalid
        parsed = ast.parse(expr_string, mode='eval')

        # Ensure that the AST contains only allowed nodes
        for node in ast.walk(parsed):
            if not isinstance(node, (
                ast.Expression,
                ast.BinOp,
                ast.UnaryOp,
                ast.Constant,
                ast.Num,          # Python <3.8 compatibility
            )):
                raise ValueError("Disallowed expression component")

        result = _eval_node(parsed)
        return str(result)

    except Exception:
        # Any error (syntax, unsupported node, division by zero, etc.)
        return 'Computation Error!'