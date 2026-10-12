import ast
import operator as op

# Supported operators and functions
_allowed_ops = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}

_allowed_funcs = {
    'abs': abs,
    'round': round,
    'sqrt': __import__('math').sqrt,
    'sin': __import__('math').sin,
    'cos': __import__('math').cos,
    'tan': __import__('math').tan,
    'log': __import__('math').log,
    'exp': __import__('math').exp,
}

def _eval(node):
    if isinstance(node, ast.Num):  # < Python3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value)}")
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        oper = _allowed_ops.get(type(node.op))
        if oper is None:
            raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
        return oper(left, right)
    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        oper = _allowed_ops.get(type(node.op))
        if oper is None:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        return oper(operand)
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function names are allowed")
        func_name = node.func.id
        if func_name not in _allowed_funcs:
            raise ValueError(f"Function '{func_name}' is not allowed")
        args = [_eval(arg) for arg in node.args]
        return _allowed_funcs[func_name](*args)
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def evaluate_user_expression(expression: str):
    """
    Safely evaluate a mathematical expression supplied by the user.

    Parameters
    ----------
    expression : str
        The user-provided mathematical expression.

    Returns
    -------
    result : int or float
        The evaluated numeric result.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters, operators,
        functions, or is syntactically incorrect.
    """
    if not isinstance(expression, str):
        raise ValueError("Expression must be a string")

    try:
        parsed = ast.parse(expression, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Ensure the parsed tree contains only allowed nodes
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Module,)):
            continue
        if not isinstance(node, (
                ast.Expression,
                ast.BinOp,
                ast.UnaryOp,
                ast.Num,
                ast.Constant,
                ast.Call,
                ast.Name,
                ast.Load
            )):
            raise ValueError(f"Disallowed expression component: {type(node).__name__}")

    return _eval(parsed)

# Example usage (uncomment to test)
# print(evaluate_user_expression("2 + 3 * sqrt(16) - log(1)"))