import ast
import operator

# Mapping of allowed AST nodes to their corresponding Python operators/functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed AST node types
_ALLOWED_NODES = (
    ast.Expression,  # top-level container
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Call,
    ast.Name,
    ast.Load,
    ast.Tuple,
    ast.List,
)

def _eval_node(node):
    """
    Recursively evaluate an AST node, only if it is composed of allowed constructs.
    Raises ValueError for any disallowed nodes or unsafe usage.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Numbers
    if isinstance(node, (ast.Num, ast.Constant)):
        if isinstance(node.value, (int, float)):
            return node.value
        else:
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        else:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        else:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    # Parentheses are represented by nested expressions; no special handling needed

    raise ValueError(f"Disallowed expression: {ast.dump(node)}")

def process_math_expression(math_expr: str):
    """
    Safely evaluate a simple mathematical expression provided as a string.

    Parameters
    ----------
    math_expr : str
        The user supplied mathematical expression.

    Returns
    -------
    int | float
        The computed result of the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters, unsafe usage,
        or cannot be safely evaluated.
    """
    # Basic validation: only allow characters that are part of the allowed
    # syntax (digits, operators, parentheses, whitespace).
    if not all(ch.isdigit() or ch in "+-*/%(). " for ch in math_expr):
        raise ValueError("Expression contains illegal characters.")

    try:
        # Parse expression into an AST
        parsed = ast.parse(math_expr, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Ensure all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Evaluate the parsed expression safely
    return _eval_node(parsed)