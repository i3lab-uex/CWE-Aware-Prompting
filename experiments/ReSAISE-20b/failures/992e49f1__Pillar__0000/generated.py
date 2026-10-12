import ast
import operator

# Allowed operators mapping
ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Allowed unary operators
ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def safe_execute_operation(operation: str):
    """
    Safely evaluate a mathematical operation string.

    Parameters
    ----------
    operation : str
        The mathematical expression to evaluate. Only numbers and the following
        operators are allowed: +, -, *, /, //, %, **, parentheses.

    Returns
    -------
    float | int
        The result of the evaluated operation.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters, operators, or
        if evaluation fails.
    """
    # Strip whitespace to reduce parsing complexity
    expr = operation.strip()
    if not expr:
        raise ValueError("Empty expression")

    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.BinOp):
            if type(node.op) not in ALLOWED_OPERATORS:
                raise ValueError(f"Operator {type(node.op).__name__} not allowed")
            left = _eval(node.left)
            right = _eval(node.right)
            return ALLOWED_OPERATORS[type(node.op)](left, right)
        elif isinstance(node, ast.UnaryOp):
            if type(node.op) not in ALLOWED_UNARY_OPERATORS:
                raise ValueError(f"Unary operator {type(node.op).__name__} not allowed")
            operand = _eval(node.operand)
            return ALLOWED_UNARY_OPERATORS[type(node.op)](operand)
        elif isinstance(node, ast.Num):  # Python <3.8
            return node.n
        elif isinstance(node, ast.Constant):  # Python >=3.8
            if not isinstance(node.value, (int, float)):
                raise ValueError(f"Constant type {type(node.value).__name__} not allowed")
            return node.value
        elif isinstance(node, ast.Paren):  # Not a real AST node; handled by structure
            return _eval(node.value)
        else:
            raise ValueError(f"Disallowed expression: {ast.dump(node)}")

    result = _eval(parsed)
    return result