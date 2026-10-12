import ast
import operator as op
import math

# Supported binary operators mapping
_BIN_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}

# Supported unary operators mapping
_UNARY_OPS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed functions from the math module
_ALLOWED_FUNCS = {
    name for name in dir(math) if not name.startswith("_")
}

def secure_math_eval(expr_str: str):
    """
    Safely evaluate a mathematical expression supplied as a string.

    Parameters
    ----------
    expr_str : str
        The expression to evaluate. Only numeric literals, binary/unary operators,
        and functions from the math module are allowed.

    Returns
    -------
    float or int
        The result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed nodes, names, or syntax errors.
    """
    try:
        # Parse the expression into an AST
        expr_ast = ast.parse(expr_str, mode="eval")
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)

        # Numeric literal (Python 3.8+ uses Constant)
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            else:
                raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

        # Binary operation
        if isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_type = type(node.op)
            if op_type in _BIN_OPS:
                return _BIN_OPS[op_type](left, right)
            else:
                raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

        # Unary operation
        if isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            op_type = type(node.op)
            if op_type in _UNARY_OPS:
                return _UNARY_OPS[op_type](operand)
            else:
                raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

        # Function call
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Only direct function names are allowed")
            func_name = node.func.id
            if func_name not in _ALLOWED_FUNCS:
                raise ValueError(f"Function '{func_name}' is not allowed")
            func = getattr(math, func_name)
            args = [_eval(arg) for arg in node.args]
            if node.keywords:
                raise ValueError("Keyword arguments are not allowed")
            return func(*args)

        # Parentheses (handled by grouping in the AST)
        if isinstance(node, ast.Paren):
            return _eval(node.value)

        raise ValueError(f"Unsupported expression component: {type(node).__name__}")

    result = _eval(expr_ast)
    if not isinstance(result, (int, float)):
        raise ValueError("Result is not a numeric type")
    return result