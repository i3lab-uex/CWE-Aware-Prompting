import ast
import operator as op
import math

# Mapping of allowed operators to their corresponding functions
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed names from the math module
_ALLOWED_NAMES = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}

def _eval(node: ast.AST):
    """
    Recursively evaluate an AST node, ensuring that only safe operations are performed.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    elif isinstance(node, ast.Num):  # For Python <3.8
        return node.n

    elif isinstance(node, ast.Constant):  # For Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    elif isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        operator_func = _ALLOWED_OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
        return operator_func(left, right)

    elif isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        operator_func = _ALLOWED_OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        return operator_func(operand)

    elif isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name) or node.func.id not in _ALLOWED_NAMES:
            raise ValueError(f"Function '{getattr(node.func, 'id', None)}' is not allowed")
        func = _ALLOWED_NAMES[node.func.id]
        args = [_eval(arg) for arg in node.args]
        return func(*args)

    elif isinstance(node, ast.Name):
        if node.id in _ALLOWED_NAMES:
            return _ALLOWED_NAMES[node.id]
        raise ValueError(f"Name '{node.id}' is not allowed")

    else:
        raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def calculate_user_input(user_input: str):
    """
    Safely evaluate a mathematical expression provided by the user.

    Parameters:
        user_input (str): The string containing the user's mathematical expression.

    Returns:
        The numerical result of evaluating the expression.

    Raises:
        ValueError: If the input contains invalid characters or if the expression is incorrect.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(user_input, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Ensure the AST contains only allowed nodes
    for node in ast.walk(parsed):
        if not isinstance(node, (
            ast.Expression, ast.BinOp, ast.UnaryOp,
            ast.Num, ast.Constant, ast.Call, ast.Name
        )):
            raise ValueError(f"Disallowed expression element: {type(node).__name__}")

    # Evaluate the parsed AST
    return _eval(parsed)