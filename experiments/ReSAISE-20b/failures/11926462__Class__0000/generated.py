import ast
import operator as op
import math

# Supported operators mapping
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.FloorDiv: op.floordiv,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Supported math functions (you can extend this list as needed)
_ALLOWED_FUNCTIONS = {
    name: getattr(math, name) for name in dir(math) if not name.startswith("_")
}

def _eval(node):
    """
    Recursively evaluate an AST node.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    if isinstance(node, ast.Num):  # <Python 3.8
        return node.n

    if isinstance(node, ast.Constant):  # <Python 3.8
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

    if isinstance(node, ast.Call):
        # Only allow function calls to whitelisted math functions
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only direct function calls are allowed")
        func_name = node.func.id
        if func_name not in _ALLOWED_FUNCTIONS:
            raise ValueError(f"Function '{func_name}' is not allowed")
        func = _ALLOWED_FUNCTIONS[func_name]
        args = [_eval(arg) for arg in node.args]
        return func(*args)

    if isinstance(node, ast.Name):
        # Allow usage of constants like 'pi', 'e'
        if node.id in _ALLOWED_FUNCTIONS:
            return _ALLOWED_FUNCTIONS[node.id]
        raise ValueError(f"Name '{node.id}' is not allowed")

    # Disallow any other node types
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def evaluate_user_math(math_expression: str):
    """
    Safely evaluates a mathematical expression supplied by the user.

    Parameters
    ----------
    math_expression : str
        The mathematical expression to evaluate.

    Returns
    -------
    float | int
        Result of the evaluation.

    Raises
    ------
    ValueError
        If the expression contains disallowed constructs or is malformed.
    """
    if not isinstance(math_expression, str):
        raise ValueError("Input must be a string")

    try:
        # Parse expression into an AST
        parsed = ast.parse(math_expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Malformed expression: {exc}") from None

    # Ensure the parsed AST contains only allowed nodes
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.Exec,
                             ast.Lambda, ast.FunctionDef, ast.ClassDef)):
            raise ValueError("Disallowed syntax in expression")

    # Evaluate the parsed AST
    return _eval(parsed)

# Example usage (uncomment to test)
# print(evaluate_user_math("2 + 3 * sin(pi / 4)"))