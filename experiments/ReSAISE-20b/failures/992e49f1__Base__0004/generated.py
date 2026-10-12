import ast
import operator as op

# Allowed operators mapping to actual Python functions
_ALLOWED_OPERATORS = {
    ast.Add:   op.add,
    ast.Sub:   op.sub,
    ast.Mult:  op.mul,
    ast.Div:   op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod:   op.mod,
    ast.Pow:   op.pow,
    ast.UAdd:  lambda x: +x,
    ast.USub:  lambda x: -x,
}

# Allowed nodes in the AST
_ALLOWED_NODES = (
    ast.Expression,  # top level
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8 (numbers)
    ast.Call,         # for math functions
    ast.Name,
    ast.Load,
)

# Allowed function names from the math module (extend as needed)
_ALLOWED_FUNCS = {
    'sqrt': 2.0,  # placeholder; actual function will be fetched
}

import math

def _eval(node):
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    elif isinstance(node, ast.Num):  # Python <3.8
        return node.n
    elif isinstance(node, ast.Constant):  # Python >=3.8
        if not isinstance(node.value, (int, float)):
            raise ValueError(f"Unsupported constant type: {type(node.value)}")
        return node.value
    elif isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError(f"Operator {node.op} is not allowed")
        left = _eval(node.left)
        right = _eval(node.right)
        return _ALLOWED_OPERATORS[type(node.op)](left, right)
    elif isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unary operator {node.op} is not allowed")
        operand = _eval(node.operand)
        return _ALLOWED_OPERATORS[type(node.op)](operand)
    elif isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function names are allowed")
        func_name = node.func.id
        if func_name not in _ALLOWED_FUNCS:
            raise ValueError(f"Function '{func_name}' is not allowed")
        func = getattr(math, func_name)
        args = [_eval(arg) for arg in node.args]
        return func(*args)
    elif isinstance(node, ast.Name):
        # disallow any variable usage
        raise ValueError(f"Usage of variables is not allowed: {node.id}")
    else:
        raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def safe_execute_operation(operation: str):
    """
    Safely evaluate a mathematical expression provided as a string.

    Parameters
    ----------
    operation : str
        The mathematical operation to evaluate. Only numeric literals,
        the operators + - * / // % **, parentheses, and a whitelist of
        math functions are permitted.

    Returns
    -------
    result : float or int
        The computed value of the expression.

    Raises
    ------
    ValueError
        If the input contains disallowed characters, operators,
        or if evaluation fails.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(operation, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Ensure all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed syntax element: {type(node).__name__}")

    # Evaluate the expression
    return _eval(parsed)

# Example usage (uncomment to test)
# print(safe_execute_operation("2 + 3 * (4 - 1)"))