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

# Allowed unary operators mapping to their functions
_ALLOWED_UNARYOPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _eval_node(node):
    """Recursively evaluate an AST node in a safe manner."""
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    if isinstance(node, ast.Num):  # For Python <3.8
        return node.n

    if isinstance(node, ast.Constant):  # For Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_BINOPS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return _ALLOWED_BINOPS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_UNARYOPS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        operand = _eval_node(node.operand)
        return _ALLOWED_UNARYOPS[op_type](operand)

    if isinstance(node, ast.Paren):
        return _eval_node(node.value)

    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def calculate_expression(math_expr: str):
    """
    Evaluate a simple arithmetic expression safely.

    Parameters
    ----------
    math_expr : str
        A string containing the mathematical expression to evaluate.

    Returns
    -------
    result : int | float
        The numerical result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains unsupported characters, unsafe operations,
        or is otherwise invalid.
    """
    # Strip whitespace to avoid accidental injection via spaces
    expr = math_expr.strip()

    try:
        # Parse expression into an AST; mode='eval' ensures it is a single expression
        parsed = ast.parse(expr, mode="eval")
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Walk the AST to ensure only allowed nodes are present
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Module,)):
            continue
        if not isinstance(
            node,
            (
                ast.Expression,
                ast.BinOp,
                ast.UnaryOp,
                ast.Num,  # for older Python
                ast.Constant,  # for newer Python
                ast.Add,
                ast.Sub,
                ast.Mult,
                ast.Div,
                ast.FloorDiv,
                ast.Mod,
                ast.Pow,
                ast.UAdd,
                ast.USub,
                ast.Paren,  # Not actually a node in AST; kept for clarity
            ),
        ):
            raise ValueError(f"Unsupported element detected: {type(node).__name__}")

    # Evaluate the parsed expression
    return _eval_node(parsed)

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(calculate_expression("2 + 3 * (4 - 1) / 5 ** 2"))