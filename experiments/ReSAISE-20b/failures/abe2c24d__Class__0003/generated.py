import math
import operator as op
import ast

# Allowed operators mapping
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

# Allowed functions from math module
_ALLOWED_FUNCTIONS = {
    name: getattr(math, name) for name in dir(math)
    if callable(getattr(math, name))
}

# Allowed constants from math module
_ALLOWED_CONSTANTS = {
    'pi': math.pi,
    'e': math.e,
}

def _eval(node):
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    elif isinstance(node, ast.Num):  # For Python <3.8
        return node.n
    elif isinstance(node, ast.Constant):  # For Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        else:
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
    elif isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_func = _ALLOWED_OPERATORS.get(type(node.op))
        if op_func is None:
            raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
        return op_func(left, right)
    elif isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_func = _ALLOWED_OPERATORS.get(type(node.op))
        if op_func is None:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        return op_func(operand)
    elif isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only direct function calls are allowed")
        func_name = node.func.id
        if func_name not in _ALLOWED_FUNCTIONS:
            raise ValueError(f"Function '{func_name}' is not allowed")
        args = [_eval(arg) for arg in node.args]
        # No kwargs support
        if node.keywords:
            raise ValueError("Keyword arguments are not allowed")
        return _ALLOWED_FUNCTIONS[func_name](*args)
    elif isinstance(node, ast.Name):
        if node.id in _ALLOWED_CONSTANTS:
            return _ALLOWED_CONSTANTS[node.id]
        else:
            raise ValueError(f"Unknown identifier: {node.id}")
    elif isinstance(node, ast.Expr):
        return _eval(node.value)
    else:
        raise ValueError(f"Unsupported expression: {ast.dump(node)}")

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
        If the input contains unsafe constructs, unsupported operations,
        or is not a well-formed mathematical expression.
    """
    try:
        # Parse the input into an AST
        parsed = ast.parse(user_input, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Walk the tree to ensure only allowed nodes are present
    for node in ast.walk(parsed):
        if not isinstance(node, (
            ast.Expression,
            ast.BinOp,
            ast.UnaryOp,
            ast.Num,
            ast.Constant,
            ast.Call,
            ast.Name,
            ast.Expr,
            ast.Load,
        )):
            raise ValueError(f"Disallowed expression component: {type(node).__name__}")

    # Evaluate the parsed AST
    result = _eval(parsed)
    if not isinstance(result, (int, float)):
        raise ValueError(f"Expression did not evaluate to a number: {result}")
    return result