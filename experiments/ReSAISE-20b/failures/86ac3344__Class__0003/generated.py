import ast
import operator as op

# Allowed operators mapping
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
    ast.Expression,  # root
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Pow,
)

def _eval(node):
    """
    Recursively evaluate an AST node after validating it.
    """
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)

        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Operator {op_type.__name__} is not allowed")
        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unary operator {op_type.__name__} is not allowed")
        return _ALLOWED_OPERATORS[op_type](operand)

    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def secure_eval_expression(exp: str):
    """
    Safely evaluate a mathematical expression containing only numbers and
    basic arithmetic operators.

    Parameters:
        exp (str): The user-provided expression string.

    Returns:
        int or float: The result of evaluating the expression.

    Raises:
        ValueError: If the expression contains disallowed characters,
                    unsupported operations, or is malformed.
    """
    if not isinstance(exp, str):
        raise ValueError("Expression must be a string")

    # Strip whitespace and check for disallowed characters early
    allowed_chars = set("0123456789+-*/%()^ .\t\n")
    if any(c not in allowed_chars for c in exp):
        raise ValueError("Expression contains invalid characters")

    # Replace caret with Python's exponent operator
    exp = exp.replace("^", "**")

    try:
        # Parse expression into an AST
        parsed = ast.parse(exp, mode="eval")
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}")

    # Validate the parsed tree
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Evaluate safely
    return _eval(parsed.body)