import ast
import operator

# Allowed binary operators mapped to their functions
ALLOWED_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Allowed unary operators mapped to their functions
ALLOWED_UNARYOPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def compute_math_expression(expression_input: str):
    """
    Safely evaluate a mathematical expression supplied by the user.

    Parameters
    ----------
    expression_input : str
        The raw mathematical expression entered by the user.

    Returns
    -------
    float or int
        Result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed syntax or cannot be parsed.
    """
    try:
        # Parse into an AST
        node = ast.parse(expression_input, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from None

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Constant):  # Python >=3.8
            if isinstance(node.value, (int, float)):
                return node.value
            else:
                raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
        elif isinstance(node, ast.Num):  # Python <3.8
            return node.n
        elif isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in ALLOWED_BINOPS:
                raise ValueError(f"Disallowed binary operator: {op_type.__name__}")
            left = _eval(node.left)
            right = _eval(node.right)
            return ALLOWED_BINOPS[op_type](left, right)
        elif isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in ALLOWED_UNARYOPS:
                raise ValueError(f"Disallowed unary operator: {op_type.__name__}")
            operand = _eval(node.operand)
            return ALLOWED_UNARYOPS[op_type](operand)
        elif isinstance(node, ast.Paren):  # Not a real AST node; handled by grouping
            return _eval(node.value)
        else:
            # Any other node type is disallowed
            raise ValueError(f"Disallowed expression element: {type(node).__name__}")

    return _eval(node)

# Example usage (commented out for production):
# if __name__ == "__main__":
#     expr = input("Enter math expression: ")
#     try:
#         result = compute_math_expression(expr)
#         print("Result:", result)
#     except ValueError as e:
#         print("Error:", e)