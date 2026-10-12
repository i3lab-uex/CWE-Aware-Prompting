import ast
import operator as op
import math

# Allowed operators mapped to their corresponding functions
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}

# Allowed unary operators
_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed names from the math module
_ALLOWED_NAMES = {
    name: getattr(math, name)
    for name in [
        'acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2', 'atanh',
        'ceil', 'comb', 'copysign', 'cos', 'cosh', 'degrees',
        'dist', 'e', 'erf', 'erfc', 'exp', 'expm1', 'fabs',
        'factorial', 'floor', 'fmod', 'frexp', 'fsum', 'gamma',
        'gcd', 'hypot', 'isclose', 'isfinite', 'isinf',
        'isnan', 'ldexp', 'lgamma', 'log', 'log10', 'log1p',
        'log2', 'modf', 'nan', 'pi', 'pow', 'prod',
        'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh',
        'trunc',
    ]
}

# Optional constants from the math module
_ALLOWED_NAMES.update({
    'inf': math.inf,
    'nan': math.nan,
})

def _eval(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    if isinstance(node, ast.Constant):  # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.Num):  # Deprecated in newer Python
        return node.n

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
        if op_type in _ALLOWED_UNARY_OPERATORS:
            return _ALLOWED_UNARY_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    if isinstance(node, ast.Call):
        # Only allow calls to allowed functions with no arguments or single numeric argument
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function calls are allowed")
        func_name = node.func.id
        if func_name not in _ALLOWED_NAMES:
            raise ValueError(f"Function '{func_name}' is not allowed")
        func = _ALLOWED_NAMES[func_name]
        if len(node.args) != 1:
            raise ValueError("Only single-argument functions are supported")
        arg = _eval(node.args[0])
        return func(arg)

    if isinstance(node, ast.Name):
        if node.id in _ALLOWED_NAMES:
            return _ALLOWED_NAMES[node.id]
        raise ValueError(f"Name '{node.id}' is not allowed")

    if isinstance(node, ast.Tuple):
        # Support tuples for functions like hypot
        return tuple(_eval(elt) for elt in node.elts)

    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def compute_expression(expression_input: str):
    """
    Safely evaluate a simple mathematical expression.

    Parameters
    ----------
    expression_input : str
        The user supplied expression.

    Returns
    -------
    float | int
        Result of the evaluated expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed syntax or cannot be evaluated.
    """
    if not isinstance(expression_input, str):
        raise ValueError("Input must be a string")

    # Strip whitespace to avoid accidental leading/trailing spaces
    expr = expression_input.strip()
    if not expr:
        raise ValueError("Empty expression")

    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in expression: {e}")

    # Ensure the parsed AST contains only allowed nodes
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Module,)):
            continue
        if not isinstance(
                node,
                (
                    ast.Expression, ast.Constant, ast.Num,
                    ast.BinOp, ast.UnaryOp, ast.Call, ast.Name,
                    ast.Tuple
                )):
            raise ValueError(f"Disallowed expression element: {type(node).__name__}")

    result = _eval(parsed)
    if isinstance(result, (int, float)):
        return result
    raise ValueError("Result is not a numeric value")