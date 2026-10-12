import ast
import operator

# Supported operators mapping from AST node to actual function
_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Supported unary operators
_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _eval_node(node):
    """
    Recursively evaluate an AST node that represents a mathematical expression.
    Only numeric literals and the supported operators are allowed.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Numeric literal (int or float)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    # Binary operations (e.g., 1 + 2)
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)

        op_type = type(node.op)
        if op_type in _OPERATORS:
            return _OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    # Unary operations (e.g., -5)
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _UNARY_OPERATORS:
            return _UNARY_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    # Parentheses are handled by the AST structure itself
    if isinstance(node, ast.Paren):
        return _eval_node(node.value)

    # If we reach here, the node type is unsupported
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def parse_and_calculate(expression: str):
    """
    Parse a simple arithmetic expression and compute its result.

    Parameters
    ----------
    expression : str
        The arithmetic expression to evaluate. Only integers, floats,
        parentheses, and the operators + - * / // % ** are allowed.

    Returns
    -------
    result : int | float
        The numerical result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains unsupported characters, syntax errors,
        or any disallowed operation.
    """
    if not isinstance(expression, str):
        raise ValueError("Expression must be a string")

    # Strip whitespace to avoid accidental parsing of spaces as tokens
    expr = expression.strip()

    if not expr:
        raise ValueError("Empty expression")

    # Parse the expression into an AST
    try:
        tree = ast.parse(expr, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Walk the AST and evaluate it safely
    return _eval_node(tree)

# Example usage:
if __name__ == "__main__":
    tests = [
        "2 + 3 * (4 - 1)",
        "-5 ** 2",
        "10 / 3",
        "7 % 4 + 2",
    ]
    for t in tests:
        print(f"{t} = {parse_and_calculate(t)}")