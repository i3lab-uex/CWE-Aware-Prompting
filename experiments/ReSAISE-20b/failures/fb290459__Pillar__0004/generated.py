import ast
import operator as op

# Allowed binary operators mapping to Python functions
_ALLOWED_BIN_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}

# Allowed unary operators mapping to Python functions
_ALLOWED_UNARY_OPS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed nodes that may appear in a safe expression
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,            # Python < 3.8
    ast.Constant,       # Python >= 3.8
    ast.Call,
    ast.Name,
    ast.Load,
)

# Only a handful of safe functions are permitted
_ALLOWED_FUNCS = {
    "abs": abs,
    "round": round,
    "min": min,
    "max": max,
}

def _eval_node(node):
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    if isinstance(node, ast.Num):  # Python <3.8
        return node.n

    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value)}")

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_BIN_OPS:
            return _ALLOWED_BIN_OPS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_UNARY_OPS:
            return _ALLOWED_UNARY_OPS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    if isinstance(node, ast.Call):
        # Only allow calls to whitelisted functions
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only direct function calls are allowed")
        func_name = node.func.id
        if func_name not in _ALLOWED_FUNCS:
            raise ValueError(f"Function '{func_name}' is not allowed")
        args = [_eval_node(arg) for arg in node.args]
        return _ALLOWED_FUNCS[func_name](*args)

    if isinstance(node, ast.Name):
        # No variables allowed
        raise ValueError(f"Variables are not permitted: {node.id}")

    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def process_math_expression(math_expr: str):
    """
    Safely evaluate a simple mathematical expression.

    Parameters
    ----------
    math_expr : str
        The user supplied mathematical expression.

    Returns
    -------
    result : int or float
        The evaluated numeric result.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters, unsafe constructs,
        or cannot be evaluated.
    """
    if not isinstance(math_expr, str):
        raise ValueError("Expression must be a string")

    # Basic syntax check: only allowed characters (digits, operators, whitespace,
    # parentheses, decimal point, commas for function arguments)
    allowed_chars = set("0123456789+-*/%()^., ")
    if any(c not in allowed_chars for c in math_expr):
        raise ValueError("Expression contains illegal characters")

    # Replace caret '^' with '**' for exponentiation
    math_expr = math_expr.replace('^', '**')

    try:
        parsed = ast.parse(math_expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}")

    # Ensure all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed expression element: {type(node).__name__}")

    # Evaluate safely
    return _eval_node(parsed)

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(process_math_expression("2 + 3 * (4 - 1)"))   # Output: 11
#     print(process_math_expression("abs(-5) + round(2.7)"))  # Output: 8