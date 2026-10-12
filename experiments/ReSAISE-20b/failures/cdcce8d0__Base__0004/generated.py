import ast
import operator as op

# Mapping of AST operators to actual Python functions
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8 (numbers)
    ast.UnaryOp,
)

def _eval(node):
    """
    Recursively evaluate an AST node that has been validated.
    Raises ValueError if the node type or operator is not allowed.
    """
    if isinstance(node, ast.Num):  # <3.8
        return node.n
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    raise ValueError(f"Disallowed expression: {ast.dump(node)}")

def compute_expression(expr_input: str):
    """
    Safely evaluate a simple arithmetic expression.

    Parameters
    ----------
    expr_input : str
        The expression to evaluate. May contain integers, floats,
        + - * / // % ** and parentheses.

    Returns
    -------
    int | float
        The computed result.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters, operators,
        or if evaluation fails.
    """
    # Strip whitespace and validate characters (basic sanity check)
    expr_input = expr_input.strip()
    if not expr_input:
        raise ValueError("Empty expression")

    # Only allow digits, whitespace and the allowed operators
    allowed_chars = set("0123456789+-*/%() .")
    if any(c not in allowed_chars for c in expr_input):
        raise ValueError("Expression contains illegal characters")

    try:
        parsed = ast.parse(expr_input, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in expression: {e}") from e

    # Ensure the parsed tree only contains allowed nodes
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node in expression: {type(node).__name__}")

    # Evaluate the expression
    try:
        result = _eval(parsed.body)
    except Exception as e:
        raise ValueError(f"Failed to evaluate expression: {e}") from e

    return result