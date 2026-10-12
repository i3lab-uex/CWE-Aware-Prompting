import ast
import operator

# Mapping of allowed operators to their corresponding functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Allowed unary operators
_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # For Python <3.8
    ast.Constant,     # For Python >=3.8 (int, float)
    ast.Expr,
)

def _evaluate(node):
    """
    Recursively evaluate an AST node that has been validated.
    """
    if isinstance(node, ast.Constant):
        if not isinstance(node.value, (int, float)):
            raise ValueError(f"Unsupported constant type: {type(node.value)}")
        return node.value

    if isinstance(node, ast.Num):  # Python <3.8
        return node.n

    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)

        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_UNARY_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return _ALLOWED_UNARY_OPERATORS[op_type](operand)

    raise ValueError(f"Unsupported AST node: {type(node).__name__}")

def compute_math_expression(expression_input: str):
    """
    Safely evaluate a mathematical expression provided by the user.

    Parameters
    ----------
    expression_input : str
        The mathematical expression to evaluate.

    Returns
    -------
    int | float
        Result of evaluating the expression.

    Raises
    ------
    ValueError
        If the input contains disallowed syntax or unsafe components.
    """
    # Strip whitespace to avoid accidental leading/trailing characters
    expr = expression_input.strip()

    if not expr:
        raise ValueError("Empty expression")

    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Validate node types recursively
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed expression element: {type(node).__name__}")

        # Ensure only allowed operators are used
        if isinstance(node, ast.BinOp) and type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError(f"Disallowed binary operator: {type(node.op).__name__}")
        if isinstance(node, ast.UnaryOp) and type(node.op) not in _ALLOWED_UNARY_OPERATORS:
            raise ValueError(f"Disallowed unary operator: {type(node.op).__name__}")

    # Evaluate the parsed AST
    return _evaluate(parsed.body)