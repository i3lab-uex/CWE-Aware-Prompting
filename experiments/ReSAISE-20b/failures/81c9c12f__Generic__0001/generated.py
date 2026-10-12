import ast
import operator as op
import math

# Allowed binary operators mapping to actual functions
_ALLOWED_BIN_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}

# Allowed unary operators
_ALLOWED_UNARY_OPS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed names from the math module
_ALLOWED_NAMES = {name for name in dir(math) if not name.startswith("_")}

def _eval(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    # Numbers (Python 3.8+ use Constant)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")

    # BinOp
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        oper_type = type(node.op)
        if oper_type in _ALLOWED_BIN_OPS:
            return _ALLOWED_BIN_OPS[oper_type](left, right)
        raise ValueError("Unsupported binary operator")

    # UnaryOp
    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        oper_type = type(node.op)
        if oper_type in _ALLOWED_UNARY_OPS:
            return _ALLOWED_UNARY_OPS[oper_type](operand)
        raise ValueError("Unsupported unary operator")

    # Call to math functions
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name) or node.func.id not in _ALLOWED_NAMES:
            raise ValueError("Unauthorized function call")
        func = getattr(math, node.func.id)
        args = [_eval(arg) for arg in node.args]
        # No kwargs allowed
        if node.keywords:
            raise ValueError("Keyword arguments not allowed")
        return func(*args)

    # Name (constants like pi, e)
    if isinstance(node, ast.Name):
        if node.id in _ALLOWED_NAMES:
            return getattr(math, node.id)
        raise ValueError("Unauthorized name")

    # Unsupported nodes
    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def math_expression_safety_check(math_input: str) -> str:
    """
    Safely evaluate a mathematical expression supplied as a string.
    
    Parameters
    ----------
    math_input : str
        The user-provided mathematical expression.

    Returns
    -------
    str
        String representation of the evaluated result, or a warning message.

    Raises
    ------
    str
        'Unsafe Code Detected!' if the expression contains disallowed content or evaluation fails.
    """
    try:
        # Parse input into an AST
        parsed = ast.parse(math_input, mode='eval')
    except SyntaxError:
        return 'Unsafe Code Detected!'

    # Walk the AST to ensure no disallowed nodes are present
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.Module,
                             ast.Exec, ast.Lambda, ast.FunctionDef,
                             ast.ClassDef, ast.AsyncFunctionDef)):
            return 'Unsafe Code Detected!'

    try:
        result = _eval(parsed)
    except Exception:
        return 'Unsafe Code Detected!'

    return str(result)