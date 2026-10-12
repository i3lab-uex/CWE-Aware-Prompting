import ast
from typing import Any

# Allowed AST node types for safe evaluation
_ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Constant,          # literals: numbers, strings, bools, None
    ast.Num,               # Python <3.8 compatibility
    ast.Str,
    ast.Bytes,
    ast.NameConstant,      # True, False, None in Python <3.8
}

# Allowed binary operators (arithmetic & string ops)
_ALLOWED_BINOPS = {
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.FloorDiv,
    ast.Mod,
    ast.Pow,
    ast.LShift,
    ast.RShift,
    ast.BitOr,
    ast.BitAnd,
    ast.BitXor,
}

# Allowed unary operators
_ALLOWED_UNARYOPS = {
    ast.UAdd,
    ast.USub,
    ast.Not,
    ast.Invert,
}


def _safe_eval(node: ast.AST) -> Any:
    """
    Recursively evaluate an AST node that has already been validated.
    """
    if isinstance(node, ast.Constant):  # Python 3.8+
        return node.value
    if isinstance(node, ast.Num):       # Python <3.8
        return node.n
    if isinstance(node, ast.Str):
        return node.s
    if isinstance(node, ast.Bytes):
        return node.s
    if isinstance(node, ast.NameConstant):  # True/False/None in <3.8
        return node.value

    if isinstance(node, ast.BinOp):
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)

        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            return left / right
        if isinstance(node.op, ast.FloorDiv):
            return left // right
        if isinstance(node.op, ast.Mod):
            return left % right
        if isinstance(node.op, ast.Pow):
            return left ** right
        if isinstance(node.op, ast.LShift):
            return left << right
        if isinstance(node.op, ast.RShift):
            return left >> right
        if isinstance(node.op, ast.BitOr):
            return left | right
        if isinstance(node.op, ast.BitAnd):
            return left & right
        if isinstance(node.op, ast.BitXor):
            return left ^ right

    if isinstance(node, ast.UnaryOp):
        operand = _safe_eval(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +operand
        if isinstance(node.op, ast.USub):
            return -operand
        if isinstance(node.op, ast.Not):
            return not operand
        if isinstance(node.op, ast.Invert):
            return ~operand

    # If we reach here, the node type was not expected
    raise ValueError(f"Unsupported AST node: {type(node).__name__}")


def _validate_ast(tree: ast.AST) -> bool:
    """
    Walk the AST and ensure only allowed node types and operators are present.
    Returns True if validation passes, False otherwise.
    """
    for node in ast.walk(tree):
        # Only allow the specified node types
        if not isinstance(node, tuple(_ALLOWED_NODES)):
            return False

        # Check binary operators
        if isinstance(node, ast.BinOp) and not isinstance(node.op, tuple(_ALLOWED_BINOPS)):
            return False

        # Check unary operators
        if isinstance(node, ast.UnaryOp) and not isinstance(node.op, tuple(_ALLOWED_UNARYOPS)):
            return False

    return True


def evaluate_user_code(code_string: str) -> str:
    """
    Safely evaluates a simple arithmetic or string expression provided by the user.
    If the code contains unsafe operations, returns 'Execution Blocked!'.

    Parameters
    ----------
    code_string : str
        The user supplied Python expression.

    Returns
    -------
    str
        Result of evaluation as a string, or 'Execution Blocked!' if unsafe.
    """
    try:
        # Parse in eval mode to restrict to expressions only
        parsed = ast.parse(code_string, mode='eval')

        # Validate the AST for safety
        if not _validate_ast(parsed):
            return 'Execution Blocked!'

        # Evaluate the safe AST
        result = _safe_eval(parsed.body)

        return str(result)
    except Exception:
        # Any exception (syntax, type error, division by zero, etc.) leads to block
        return 'Execution Blocked!'