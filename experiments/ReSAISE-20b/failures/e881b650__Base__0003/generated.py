import ast
import operator

# Mapping of supported operators to their corresponding functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Mapping of supported unary operators
_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _eval_node(node):
    """
    Recursively evaluate an AST node, allowing only safe arithmetic operations.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    if isinstance(node, ast.Num):  # For Python <3.8
        return node.n

    if isinstance(node, ast.Constant):  # For Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_UNARY_OPERATORS:
            return _ALLOWED_UNARY_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    if isinstance(node, ast.Paren):
        return _eval_node(node.value)

    # Disallow any other node types
    raise ValueError(f"Unsupported expression component: {type(node).__name__}")

def compute_expression(expr: str):
    """
    Safely evaluate a mathematical expression given as a string.

    Parameters
    ----------
    expr : str
        The arithmetic expression to evaluate. Only basic arithmetic operators are allowed.

    Returns
    -------
    int | float
        The numerical result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains unsupported operators, characters, or if evaluation fails.
    """
    # Strip whitespace to avoid issues with parsing
    expr = expr.strip()
    if not expr:
        raise ValueError("Empty expression")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax in expression: {e}") from None

    # Ensure the top-level node is an Expression
    if not isinstance(parsed, ast.Expression):
        raise ValueError("Expression must be a single evaluatable expression")

    # Evaluate the parsed AST safely
    return _eval_node(parsed)

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(compute_expression("2 + 3 * (4 - 1) / 5 ** 2"))