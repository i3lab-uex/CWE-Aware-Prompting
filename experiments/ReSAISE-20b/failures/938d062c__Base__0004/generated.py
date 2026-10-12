import ast
import operator as op

# Mapping of supported operators to their corresponding functions
_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}

# Mapping of supported unary operators
_UNARY_OPERATORS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Call,
)

def _eval_node(node):
    """
    Recursively evaluate an AST node that represents a mathematical expression.
    Raises ValueError for unsupported nodes or operations.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    if isinstance(node, (ast.Num, ast.Constant)):
        # For constants: ensure they are numeric
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)

        op_type = type(node.op)
        if op_type not in _OPERATORS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        return _OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type not in _UNARY_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return _UNARY_OPERATORS[op_type](operand)

    if isinstance(node, ast.Call):
        # Disallow function calls entirely for safety
        raise ValueError("Function calls are not allowed in expressions")

    # Any other node types are disallowed
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def evaluate_expression(math_expr: str):
    """
    Safely evaluates a mathematical expression provided as a string.

    Parameters
    ----------
    math_expr : str
        The arithmetic expression to evaluate. Only the following operators are supported:
        +, -, *, /, //, %, **. Parentheses and whitespace are also allowed.

    Returns
    -------
    int | float
        The result of the evaluated expression.

    Raises
    ------
    ValueError
        If the expression contains unsupported operators, characters,
        or if evaluation fails for any reason.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(math_expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax in expression: {exc}") from None

    # Ensure the parsed tree contains only allowed node types
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Unsupported element in expression: {type(node).__name__}")

    # Evaluate the parsed AST safely
    return _eval_node(parsed)