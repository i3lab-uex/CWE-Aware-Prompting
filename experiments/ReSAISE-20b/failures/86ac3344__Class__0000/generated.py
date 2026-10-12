import ast
import operator

# Allowed binary operators mapping to the actual Python functions
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

# Allowed numeric constants
_ALLOWED_NUMERIC_TYPES = (int, float)

def secure_eval_expression(exp: str):
    """
    Evaluate a mathematical expression safely.

    Parameters
    ----------
    exp : str
        User supplied mathematical expression.

    Returns
    -------
    result : int or float
        Result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed syntax or unsafe operations.
    """
    # Parse the string into an AST
    try:
        expr_ast = ast.parse(exp, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Recursive evaluator
    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)

        # Numbers
        if isinstance(node, ast.Constant):
            if isinstance(node.value, _ALLOWED_NUMERIC_TYPES):
                return node.value
            raise ValueError(f"Disallowed constant type: {type(node.value).__name__}")

        if isinstance(node, ast.Num):  # For Python <3.8 compatibility
            return node.n

        # Binary operations (+, -, *, /, //, %, **)
        if isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in _ALLOWED_BINOPS:
                raise ValueError(f"Disallowed binary operator: {op_type.__name__}")
            left = _eval(node.left)
            right = _eval(node.right)
            # Protect against division by zero
            if op_type in (ast.Div, ast.FloorDiv) and right == 0:
                raise ValueError("Division by zero")
            return _ALLOWED_BINOPS[op_type](left, right)

        # Unary operations (+/-)
        if isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in _ALLOWED_UNOPS:
                raise ValueError(f"Disallowed unary operator: {op_type.__name__}")
            operand = _eval(node.operand)
            return _ALLOWED_UNOPS[op_type](operand)

        # Parentheses are just grouping; handled by the AST structure
        if isinstance(node, ast.Paren):  # Not a real node; keep for completeness
            return _eval(node.value)

        raise ValueError(f"Disallowed expression: {ast.dump(node)}")

    return _eval(expr_ast)

# Example usage (uncomment to test)
# print(secure_eval_expression("2 + 3 * (4 - 1) / 5"))