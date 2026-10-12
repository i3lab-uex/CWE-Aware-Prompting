import ast
import operator as op
import math

# Supported operators mapping from AST node to Python function
OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed math functions
ALLOWED_FUNCS = {
    name: getattr(math, name) for name in [
        'acos', 'acosh', 'asin', 'asinh', 'atan',
        'atan2', 'atanh', 'ceil', 'comb', 'copysign',
        'cos', 'cosh', 'degrees', 'dist', 'e',
        'exp', 'expm1', 'fabs', 'factorial', 'floor',
        'fmod', 'frexp', 'fsum', 'gamma', 'gcd',
        'hypot', 'isclose', 'isfinite', 'isinf', 'isnan',
        'ldexp', 'lgamma', 'log', 'log10', 'log1p',
        'log2', 'modf', 'pow', 'prod', 'radians',
        'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'trunc',
        # Constants
        'pi', 'tau', 'e'
    ]
}

# Allowed names (constants) only
ALLOWED_NAMES = {
    name: getattr(math, name) for name in ['pi', 'e', 'tau']
}

def _eval(node):
    """
    Recursively evaluate an AST node ensuring only allowed operations are used.
    """
    if isinstance(node, ast.Num):          # <number> (Python <3.8)
        return node.n
    if isinstance(node, ast.Constant):     # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        oper_func = OPERATORS.get(type(node.op))
        if oper_func is None:
            raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
        return oper_func(left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        oper_func = OPERATORS.get(type(node.op))
        if oper_func is None:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        return oper_func(operand)

    if isinstance(node, ast.Call):
        # Only allow functions defined in ALLOWED_FUNCS
        func_name = getattr(node.func, 'id', None)
        if func_name not in ALLOWED_FUNCS:
            raise ValueError(f"Function '{func_name}' is not allowed.")
        args = [_eval(arg) for arg in node.args]
        # No kwargs allowed
        if node.keywords:
            raise ValueError("Keyword arguments are not supported.")
        return ALLOWED_FUNCS[func_name](*args)

    if isinstance(node, ast.Name):
        # Allow constants like pi, e
        if node.id in ALLOWED_NAMES:
            return ALLOWED_NAMES[node.id]
        raise ValueError(f"Name '{node.id}' is not allowed.")

    # Any other node type is disallowed
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def calculate_from_input(user_input: str) -> float:
    """
    Safely evaluate a mathematical expression provided by the user.

    Parameters
    ----------
    user_input : str
        The mathematical expression to evaluate.

    Returns
    -------
    float
        The numerical result of the evaluation.

    Raises
    ------
    ValueError
        If the expression is unsafe, malformed or contains disallowed elements.
    """
    if not isinstance(user_input, str):
        raise ValueError("Input must be a string.")

    # Strip whitespace to avoid accidental leading/trailing spaces causing parse issues
    user_input = user_input.strip()
    if not user_input:
        raise ValueError("Input cannot be empty.")

    try:
        # Parse expression into AST
        expr_ast = ast.parse(user_input, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Malformed expression: {exc}") from exc

    # Ensure the parsed tree contains only allowed nodes
    if not isinstance(expr_ast.body, (ast.Expression)):
        raise ValueError("Expression must be a single evaluatable expression.")

    try:
        result = _eval(expr_ast.body)
    except ZeroDivisionError as exc:
        raise ValueError("Division by zero.") from exc
    except Exception as exc:
        # Wrap any other exception as ValueError to avoid leaking details
        raise ValueError(f"Error evaluating expression: {exc}") from exc

    # Ensure result is a number
    if not isinstance(result, (int, float)):
        raise ValueError("Expression did not evaluate to a numeric result.")

    return float(result)