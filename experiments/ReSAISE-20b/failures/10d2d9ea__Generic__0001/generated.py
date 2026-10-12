import ast
import operator

# Supported operators mapping
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Supported unary operators
UNARY_OPERATORS = {
    ast.UAdd: lambda x: +x,
    ast.USub: lambda x: -x,
}


def parse_and_calculate(expression: str):
    """
    Parse a simple arithmetic expression and compute its value.

    Supports +, -, *, /, //, %, ** and parentheses.
    Raises ValueError for unsupported syntax or characters.
    """
    if not isinstance(expression, str):
        raise ValueError("Expression must be a string")

    # Strip whitespace
    expr = expression.strip()

    try:
        tree = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid expression: {e}")

    # Recursively evaluate the AST
    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_type = type(node.op)
            if op_type in OPERATORS:
                return OPERATORS[op_type](left, right)
            else:
                raise ValueError(f"Unsupported binary operator: {op_type}")
        elif isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            op_type = type(node.op)
            if op_type in UNARY_OPERATORS:
                return UNARY_OPERATORS[op_type](operand)
            else:
                raise ValueError(f"Unsupported unary operator: {op_type}")
        elif isinstance(node, ast.Num):  # Python <3.8
            return node.n
        elif isinstance(node, ast.Constant):  # Python >=3.8
            if isinstance(node.value, (int, float)):
                return node.value
            else:
                raise ValueError(f"Unsupported constant type: {type(node.value)}")
        elif isinstance(node, ast.Paren):  # Not needed in eval mode
            return _eval(node.value)
        else:
            raise ValueError(f"Unsupported expression component: {type(node)}")

    result = _eval(tree)

    # Ensure the result is a number
    if not isinstance(result, (int, float)):
        raise ValueError("Result is not a number")

    return result