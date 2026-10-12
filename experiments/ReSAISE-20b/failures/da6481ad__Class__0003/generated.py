import ast
import operator as op

# Allowed operators mapping
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

# Allowed functions (optional, can be extended)
_ALLOWED_FUNCTIONS = {
    'abs': abs,
    'round': round,
}

def _eval(node):
    """
    Recursively evaluate an AST node.
    Raises ValueError for any disallowed construct.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    elif isinstance(node, ast.Num):  # For Python <3.8
        return node.n

    elif isinstance(node, ast.Constant):  # For Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value)}")

    elif isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError(f"Operator {type(node.op).__name__} is not allowed")
        left = _eval(node.left)
        right = _eval(node.right)
        return _ALLOWED_OPERATORS[type(node.op)](left, right)

    elif isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unary operator {type(node.op).__name__} is not allowed")
        operand = _eval(node.operand)
        return _ALLOWED_OPERATORS[type(node.op)](operand)

    elif isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function names are allowed")
        func_name = node.func.id
        if func_name not in _ALLOWED_FUNCTIONS:
            raise ValueError(f"Function '{func_name}' is not allowed")
        args = [_eval(arg) for arg in node.args]
        return _ALLOWED_FUNCTIONS[func_name](*args)

    elif isinstance(node, ast.Name):
        # No variables allowed
        raise ValueError(f"Use of variable '{node.id}' is not permitted")

    else:
        raise ValueError(f"Unsupported expression: {ast.dump(node)}")


def secure_math_eval(expr_str: str):
    """
    Safely evaluate a mathematical expression provided as a string.

    Parameters
    ----------
    expr_str : str
        The expression to evaluate. Only numeric literals, basic arithmetic operators,
        and a whitelist of safe functions are permitted.

    Returns
    -------
    result : int or float
        The numerical result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed syntax, unsafe characters,
        or unsupported operations.
    """
    if not isinstance(expr_str, str):
        raise ValueError("Expression must be a string")

    # Strip whitespace to avoid accidental injection via spaces
    expr_str = expr_str.strip()
    if not expr_str:
        raise ValueError("Empty expression")

    try:
        parsed = ast.parse(expr_str, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Ensure the parsed tree contains only allowed nodes
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.Global,
                            ast.Nonlocal, ast.Exec, ast.Lambda, ast.FunctionDef,
                            ast.ClassDef)):
            raise ValueError(f"Disallowed construct: {type(node).__name__}")

    return _eval(parsed)