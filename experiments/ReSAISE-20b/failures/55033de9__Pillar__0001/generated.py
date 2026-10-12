import ast
from typing import Union

# Allowed AST node types for safe evaluation
_ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Pow,
    ast.Mod,
    ast.FloorDiv,
    ast.USub,
    ast.UAdd,
    ast.LParen,       # not a real node, but parentheses are handled by grouping
}

# Mapping from AST operator nodes to actual Python operators
_OPERATOR_MAP = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b,
    ast.FloorDiv: lambda a, b: a // b,
    ast.Mod: lambda a, b: a % b,
    ast.Pow: lambda a, b: a ** b,
    ast.UAdd: lambda a: +a,
    ast.USub: lambda a: -a,
}

def _eval_node(node: ast.AST) -> Union[int, float]:
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    if isinstance(node, (ast.Num,)):
        # Python <3.8
        return node.n

    if isinstance(node, ast.Constant):
        # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _OPERATOR_MAP:
            return _OPERATOR_MAP[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _OPERATOR_MAP:
            return _OPERATOR_MAP[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    raise ValueError(f"Disallowed expression component: {type(node).__name__}")

def evaluate_expression(expression: str) -> Union[int, float]:
    """
    Safely evaluate a mathematical expression consisting only of numbers and
    the following operators: +, -, *, /, //, %, **, parentheses.
    
    Parameters
    ----------
    expression : str
        The mathematical expression to evaluate.

    Returns
    -------
    int | float
        Result of the evaluated expression.

    Raises
    ------
    ValueError
        If the expression contains unsupported characters, operators,
        or constructs that could lead to unsafe evaluation.
    """
    if not isinstance(expression, str):
        raise ValueError("Expression must be a string.")

    # Strip whitespace for easier parsing
    expression = expression.strip()
    if not expression:
        raise ValueError("Empty expression.")

    try:
        parsed = ast.parse(expression, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}")

    # Ensure all nodes are allowed
    for node in ast.walk(parsed):
        if type(node) not in _ALLOWED_NODES:
            raise ValueError(f"Disallowed syntax element: {type(node).__name__}")

    return _eval_node(parsed)