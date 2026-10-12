import ast
import operator as op
import math

# Mapping of allowed operators to their corresponding functions
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

# Mapping of allowed math functions
_ALLOWED_FUNCTIONS = {
    name: getattr(math, name)
    for name in [
        'acos', 'acosh', 'asin', 'asinh', 'atan',
        'atan2', 'atanh', 'ceil', 'copysign', 'cos',
        'cosh', 'degrees', 'e', 'exp', 'fabs', 'floor',
        'fmod', 'frexp', 'hypot', 'ldexp', 'lgamma',
        'log', 'log10', 'modf', 'pow', 'radians', 'sin',
        'sinh', 'sqrt', 'tan', 'tanh', 'pi'
    ]
}

def _eval(node: ast.AST) -> float:
    """
    Recursively evaluate an AST node.
    Only nodes listed in _ALLOWED_OPERATORS and _ALLOWED_FUNCTIONS are permitted.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    if isinstance(node, ast.Num):  # For Python <3.8
        return node.n

    if isinstance(node, ast.Constant):  # For Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        operator_func = _ALLOWED_OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
        return operator_func(left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        operator_func = _ALLOWED_OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        return operator_func(operand)

    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function calls are allowed")
        func_name = node.func.id
        if func_name not in _ALLOWED_FUNCTIONS:
            raise ValueError(f"Function '{func_name}' is not allowed")
        args = [_eval(arg) for arg in node.args]
        return _ALLOWED_FUNCTIONS[func_name](*args)

    if isinstance(node, ast.Name):
        # Allow access to constants like pi and e
        if node.id in _ALLOWED_FUNCTIONS:
            return _ALLOWED_FUNCTIONS[node.id]
        raise ValueError(f"Unknown identifier: {node.id}")

    # Reject any other node types
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def calculate_from_input(user_input: str) -> float:
    """
    Safely evaluate a mathematical expression provided by the user.

    Parameters
    ----------
    user_input : str
        The mathematical expression entered by the user.

    Returns
    -------
    float
        Numerical result of evaluating the safe mathematical expression.

    Raises
    ------
    ValueError
        If the input contains unsafe elements or is malformed.
    """
    if not isinstance(user_input, str):
        raise ValueError("Input must be a string")

    # Strip whitespace and ensure it's not empty
    expr = user_input.strip()
    if not expr:
        raise ValueError("Empty expression")

    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Malformed expression: {exc}") from exc

    # Ensure the parsed tree only contains allowed nodes
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.Exec, ast.Global, ast.Nonlocal)):
            raise ValueError("Import or execution statements are not allowed")
        if isinstance(node, ast.Attribute):
            raise ValueError("Attribute access is not allowed")

    result = _eval(parsed)
    if isinstance(result, complex):
        raise ValueError("Complex numbers are not supported")
    return result