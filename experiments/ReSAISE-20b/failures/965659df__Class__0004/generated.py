import ast
import operator

# Mapping of allowed AST operator nodes to actual functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
}

# Mapping of allowed AST unary operators
_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _eval_node(node):
    """Recursively evaluate an AST node, allowing only safe operations."""
    if isinstance(node, ast.Num):          # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):     # Python 3.8+
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

    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    if isinstance(node, (ast.Paren)):
        # Parentheses are handled implicitly by AST
        return _eval_node(node.value)

    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def evaluate_math_expression(expression: str):
    """
    Safely evaluates a simple mathematical expression provided as a string.

    Parameters
    ----------
    expression : str
        The user‑supplied mathematical expression (e.g., "3 + 4 * (2 - 1)").

    Returns
    -------
    int | float
        The result of the evaluated expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters, unsupported operations,
        or any other unsafe construct.
    """
    if not isinstance(expression, str):
        raise ValueError("Expression must be a string")

    # Strip whitespace to avoid accidental leading/trailing spaces
    expr = expression.strip()

    if not expr:
        raise ValueError("Empty expression")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}")

    # Ensure the parsed tree contains only allowed nodes
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Call, ast.Attribute, ast.Import,
                            ast.ImportFrom, ast.Module, ast.Lambda)):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Evaluate the parsed expression
    return _eval_node(parsed)

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(evaluate_math_expression("3 + 4 * (2 - 1)"))  # Should output 7