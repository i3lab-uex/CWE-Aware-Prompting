import ast
import operator as op

# Mapping of supported operators to their corresponding functions
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}

# Mapping of supported unary operators
_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

def compute_expression(input_expr: str):
    """
    Safely evaluate a simple arithmetic expression provided as a string.

    Parameters
    ----------
    input_expr : str
        The user-provided arithmetic expression to evaluate.

    Returns
    -------
    result : float or int
        The numeric result of the evaluated expression.

    Raises
    ------
    ValueError
        If the expression contains unsupported characters, unsafe nodes,
        or invalid operations.
    """
    try:
        # Parse the expression into an AST node
        expr_ast = ast.parse(input_expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid expression syntax: {e}") from None

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Num):  # For Python <3.8
            return node.n
        elif isinstance(node, ast.Constant):  # For Python >=3.8
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
        elif isinstance(node, ast.BinOp):
            if type(node.op) not in _ALLOWED_OPERATORS:
                raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
            left = _eval(node.left)
            right = _eval(node.right)
            try:
                return _ALLOWED_OPERATORS[type(node.op)](left, right)
            except ZeroDivisionError:
                raise ValueError("Division by zero") from None
        elif isinstance(node, ast.UnaryOp):
            if type(node.op) not in _ALLOWED_UNARY_OPERATORS:
                raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
            operand = _eval(node.operand)
            return _ALLOWED_UNARY_OPERATORS[type(node.op)](operand)
        elif isinstance(node, ast.Paren):
            return _eval(node.value)
        else:
            # Reject any other node types (e.g., function calls, attributes)
            raise ValueError(f"Unsupported expression element: {type(node).__name__}")

    return _eval(expr_ast)

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     expr = "3 + 4 * (2 - 1) / 5 ** 2"
#     print(compute_expression(expr))