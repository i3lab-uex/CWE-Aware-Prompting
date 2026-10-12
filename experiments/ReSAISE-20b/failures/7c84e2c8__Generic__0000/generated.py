import ast
import operator as op

# Mapping of allowed AST nodes to corresponding Python operators/functions
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

# Allowed names (functions/constants) from the math module
_ALLOWED_NAMES = {
    "abs": abs,
    "round": round,
    "min": min,
    "max": max,
}

# Add math functions and constants
import math
_ALLOWED_NAMES.update({
    name: getattr(math, name)
    for name in dir(math)
    if not name.startswith("_")
})


def _eval(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Num):  # <Python 3.8
        return node.n
    elif isinstance(node, ast.Constant):  # <Python 3.8
        if isinstance(node.value, (int, float)):
            return node.value
        else:
            raise ValueError(f"Unsupported constant type: {type(node.value)}")
    elif isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        operator_func = _ALLOWED_OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError(f"Unsupported binary operator: {ast.dump(node.op)}")
        return operator_func(left, right)
    elif isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        operator_func = _ALLOWED_OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError(f"Unsupported unary operator: {ast.dump(node.op)}")
        return operator_func(operand)
    elif isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name) or node.func.id not in _ALLOWED_NAMES:
            raise ValueError(f"Function '{getattr(node.func, 'id', None)}' is not allowed")
        func = _ALLOWED_NAMES[node.func.id]
        args = [_eval(arg) for arg in node.args]
        # No keyword arguments allowed
        if node.keywords:
            raise ValueError("Keyword arguments are not supported")
        return func(*args)
    elif isinstance(node, ast.Name):
        if node.id in _ALLOWED_NAMES:
            return _ALLOWED_NAMES[node.id]
        raise ValueError(f"Name '{node.id}' is not allowed")
    else:
        raise ValueError(f"Unsupported expression: {ast.dump(node)}")


def calculate_user_input(user_input: str):
    """
    Safely evaluate a mathematical expression provided by the user.

    Parameters
    ----------
    user_input : str
        The string containing the user’s mathematical expression.

    Returns
    -------
    result : int | float
        The result of evaluating the mathematical expression.

    Raises
    ------
    ValueError
        If the input contains invalid characters or if the expression is incorrect.
    """
    # Strip whitespace and ensure it's not empty
    expr = user_input.strip()
    if not expr:
        raise ValueError("Input expression is empty")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(expr, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Ensure the parsed tree contains only allowed nodes
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.Exec, ast.Global,
                            ast.Nonlocal, ast.Lambda)):
            raise ValueError(f"Disallowed construct: {ast.dump(node)}")

    # Evaluate the expression
    return _eval(parsed.body)