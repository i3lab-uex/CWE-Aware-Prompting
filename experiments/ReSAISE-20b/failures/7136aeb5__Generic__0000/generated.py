import ast
import operator

# Map allowed AST operators to actual Python functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    # Unary operators
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # For Python <3.8
    ast.Constant,     # For numbers in Python >=3.8
    ast.Pow,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Mod,
    ast.UAdd,
    ast.USub,
    ast.LParen := None,  # not a real node but placeholder
)

def _eval(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Num):  # <3.8
        return node.n
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value)}")
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        return _ALLOWED_OPERATORS[op_type](left, right)
    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return _ALLOWED_OPERATORS[op_type](operand)
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def evaluate_expression_safely(expr: str):
    """
    Safely evaluates a mathematical expression string containing numbers,
    +, -, *, /, **, %, and parentheses.

    Parameters
    ----------
    expr : str
        The expression to evaluate.

    Returns
    -------
    int | float
        Result of the evaluation.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters or is malformed.
    """
    if not isinstance(expr, str):
        raise ValueError("Expression must be a string")

    # Strip whitespace to simplify checks
    expr = expr.strip()
    if not expr:
        raise ValueError("Empty expression")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Walk the tree and ensure only allowed nodes are present
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            # Skip LParen placeholder
            if getattr(node, 'name', None) == 'LParen':
                continue
            raise ValueError(f"Disallowed expression element: {type(node).__name__}")

    # Evaluate the parsed expression
    return _eval(parsed.body)