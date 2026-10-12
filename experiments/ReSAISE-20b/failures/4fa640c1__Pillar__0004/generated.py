import ast
import operator

# Map AST operators to actual functions
_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Allowed unary operators
_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def perform_safe_math(expression: str):
    """
    Safely evaluate a mathematical expression consisting of numbers and
    the operators +, -, *, /, //, %, **. Parentheses are allowed.

    Parameters
    ----------
    expression : str
        The mathematical expression to evaluate.

    Returns
    -------
    result : float or int
        The computed value of the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed nodes or is otherwise invalid.
    """
    if not isinstance(expression, str):
        raise ValueError("Expression must be a string")

    try:
        parsed = ast.parse(expression, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)

        elif isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_type = type(node.op)
            if op_type not in _OPERATORS:
                raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
            return _OPERATORS[op_type](left, right)

        elif isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            op_type = type(node.op)
            if op_type not in _UNARY_OPERATORS:
                raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
            return _UNARY_OPERATORS[op_type](operand)

        elif isinstance(node, ast.Num):   # Python <3.8
            return node.n

        elif isinstance(node, ast.Constant):  # Python >=3.8
            if isinstance(node.value, (int, float)):
                return node.value
            else:
                raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

        elif isinstance(node, ast.Paren):  # Not a real AST node; parentheses are handled by structure
            return _eval(node.value)

        else:
            raise ValueError(f"Disallowed expression: {ast.dump(node)}")

    return _eval(parsed)