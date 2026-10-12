import ast
import operator

# Allowed binary operators and their implementations
ALLOWED_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Allowed unary operators
ALLOWED_UNOPS = {
    ast.UAdd: lambda x: +x,
    ast.USub: lambda x: -x,
}

# Allowed node types
ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Name,
    ast.Call,
    ast.Attribute,
    ast.Subscript,
    ast.Index,
)

# Safe functions and constants from math module
import math
SAFE_NAMES = {
    name: getattr(math, name)
    for name in dir(math) if not name.startswith('_')
}
SAFE_NAMES.update({
    'abs': abs,
    'round': round,
    'pow': pow,
})

def _eval(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    if isinstance(node, (ast.Num, ast.Constant)):
        # Numbers only
        return node.n

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in ALLOWED_BINOPS:
            return ALLOWED_BINOPS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in ALLOWED_UNOPS:
            return ALLOWED_UNOPS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    if isinstance(node, ast.Name):
        id_ = node.id
        if id_ in SAFE_NAMES:
            return SAFE_NAMES[id_]
        raise ValueError(f"Use of unknown name: {id_}")

    if isinstance(node, ast.Call):
        func = _eval(node.func)
        args = [_eval(arg) for arg in node.args]
        if callable(func):
            return func(*args)
        raise ValueError(f"Attempted to call non-callable: {func}")

    if isinstance(node, ast.Attribute):
        value = _eval(node.value)
        attr = node.attr
        if hasattr(value, attr):
            return getattr(value, attr)
        raise ValueError(f"Attribute {attr} not found on {value}")

    if isinstance(node, ast.Subscript):
        value = _eval(node.value)
        slice_ = node.slice
        if isinstance(slice_, ast.Index):
            index = _eval(slice_.value)
            return value[index]
        raise ValueError("Only simple indexing is allowed")

    raise ValueError(f"Unsupported expression component: {type(node).__name__}")

def perform_safe_math(expression: str):
    """
    Safely evaluate a mathematical expression supplied as a string.

    Parameters
    ----------
    expression : str
        The expression to evaluate. Only numbers, basic arithmetic operators,
        parentheses, and safe math functions/constants are permitted.

    Returns
    -------
    int | float
        The numeric result of the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed syntax, unsafe names,
        or otherwise cannot be safely evaluated.
    """
    if not isinstance(expression, str):
        raise ValueError("Expression must be a string")

    try:
        # Parse expression into an AST
        parsed = ast.parse(expression, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}")

    # Validate all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, ALLOWED_NODES):
            raise ValueError(f"Disallowed syntax: {type(node).__name__}")

    # Evaluate safely
    return _eval(parsed)

# Example usage (remove or comment out in production)
if __name__ == "__main__":
    tests = [
        "2 + 3 * 4",
        "(1 + 2) ** 3",
        "math.sqrt(16)",
        "abs(-5)",
        "pow(2, 8)",
    ]
    for expr in tests:
        print(f"{expr} = {perform_safe_math(expr)}")