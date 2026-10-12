import ast
import operator

# Mapping of allowed binary operators to their implementations
_ALLOWED_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Mapping of allowed unary operators
_ALLOWED_UNARYOPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def evaluate_expression(expr: str):
    """
    Safely evaluates a simple arithmetic expression provided as a string.

    Supported operators: +, -, *, /, //, %, **.
    Numbers may be integers or floats. No variables or function calls are allowed.

    Args:
        expr: The expression string to evaluate.

    Returns:
        The numerical result of the evaluation (int or float).

    Raises:
        ValueError: If the expression contains unsupported syntax, unsafe
                    constructs, or invalid operations.
    """
    try:
        # Parse the expression into an AST node
        tree = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Recursively evaluate the AST node
    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)

        # Numbers (int or float)
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

        # Binary operations
        if isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)

            op_type = type(node.op)
            if op_type not in _ALLOWED_BINOPS:
                raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

            # Protect against division by zero
            if op_type in (ast.Div, ast.FloorDiv, ast.Mod) and right == 0:
                raise ValueError("Division or modulo by zero")

            return _ALLOWED_BINOPS[op_type](left, right)

        # Unary operations (+/-)
        if isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            op_type = type(node.op)
            if op_type not in _ALLOWED_UNARYOPS:
                raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
            return _ALLOWED_UNARYOPS[op_type](operand)

        # Parenthesized expressions are just the inner expression
        if isinstance(node, ast.Paren):
            return _eval(node.value)

        # Disallow any other node types (e.g., function calls, names)
        raise ValueError(f"Unsupported expression element: {type(node).__name__}")

    result = _eval(tree)
    return result