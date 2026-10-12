import ast
import operator

# Mapping of allowed AST operators to their corresponding Python functions
_ALLOWED_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_ALLOWED_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed literal node types
_ALLOWED_LITERAL_NODES = (ast.Constant, ast.Num, ast.Str, ast.Bytes)

# Names that are safe to use in expressions (e.g., True, False, None)
_ALLOWED_NAMES = {"True", "False", "None"}


def _evaluate(node):
    """
    Recursively evaluate an AST node that has already been validated
    to contain only safe constructs.
    """
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)

    # Literals
    if isinstance(node, (ast.Constant, ast.Num, ast.Str, ast.Bytes)):
        return node.value

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_BIN_OPS:
            raise ValueError("Unsupported binary operator")
        return _ALLOWED_BIN_OPS[op_type](left, right)

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_UNARY_OPS:
            raise ValueError("Unsupported unary operator")
        return _ALLOWED_UNARY_OPS[op_type](operand)

    # Name constants (True, False, None)
    if isinstance(node, ast.Name):
        if node.id in _ALLOWED_NAMES:
            return eval(node.id)  # safe because names are pre-defined
        raise ValueError(f"Disallowed name: {node.id}")

    # Fall back to blocked
    raise ValueError("Unsupported expression component")


def _is_safe_ast(node):
    """
    Walk the AST and ensure only allowed node types are present.
    Return True if safe, False otherwise.
    """
    for child in ast.walk(node):
        # Allow Expression as root
        if isinstance(child, (ast.Expression,)):
            continue

        # Literals
        if isinstance(child, _ALLOWED_LITERAL_NODES):
            continue

        # Names must be in allowed set
        if isinstance(child, ast.Name):
            if child.id not in _ALLOWED_NAMES:
                return False
            continue

        # Binary and Unary ops must be allowed types
        if isinstance(child, (ast.BinOp, ast.UnaryOp)):
            continue

        # All other node types are disallowed
        return False

    return True


def process_user_script(code_str: str) -> str:
    """
    Safely evaluate a user-supplied Python script that should contain only
    simple arithmetic or string operations.

    Parameters:
        code_str (str): The user-provided script content.

    Returns:
        str: The string representation of the evaluation result,
             or 'Execution Blocked!' if unsafe input is detected.
    """
    try:
        # Parse the code into an AST
        parsed = ast.parse(code_str, mode="eval")
    except SyntaxError:
        return "Execution Blocked!"

    # Validate the AST
    if not _is_safe_ast(parsed):
        return "Execution Blocked!"

    try:
        result = _evaluate(parsed)
    except Exception:
        return "Execution Blocked!"

    return str(result)