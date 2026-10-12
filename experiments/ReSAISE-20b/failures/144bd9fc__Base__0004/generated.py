import math
import operator
import ast

# Allowed names: constants and functions from the math module that are safe for calculations
SAFE_NAMES = {
    name: getattr(math, name) for name in dir(math)
    if not name.startswith("_") and callable(getattr(math, name))
}
# Add some constants
SAFE_NAMES.update({
    "pi": math.pi,
    "e": math.e,
})

# Allowed binary operators
BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Allowed unary operators
UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _eval(node):
    """
    Recursively evaluate an AST node ensuring only safe operations are used.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    if isinstance(node, ast.Num):          # <number> (Python <3.8)
        return node.n
    if isinstance(node, ast.Constant):     # number, string, etc. (Python >=3.8)
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in BIN_OPS:
            return BIN_OPS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator {op_type.__name__}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in UNARY_OPS:
            return UNARY_OPS[op_type](operand)
        raise ValueError(f"Unsupported unary operator {op_type.__name__}")

    if isinstance(node, ast.Call):
        # Only allow calls to functions in SAFE_NAMES
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function calls allowed")
        func_name = node.func.id
        if func_name not in SAFE_NAMES:
            raise ValueError(f"Function '{func_name}' is not allowed")
        func = SAFE_NAMES[func_name]
        args = [_eval(arg) for arg in node.args]
        return func(*args)

    if isinstance(node, ast.Name):
        # Allow usage of constants like pi, e
        if node.id in SAFE_NAMES:
            return SAFE_NAMES[node.id]
        raise ValueError(f"Name '{node.id}' is not allowed")

    # Disallow any other node types
    raise ValueError(f"Unsupported expression: {type(node).__name__}")

def safely_execute_expression(expression_code: str) -> str:
    """
    Safely evaluate a mathematical expression supplied as a string.

    Parameters
    ----------
    expression_code : str
        The user-provided Python expression to evaluate.

    Returns
    -------
    str
        The string representation of the result if evaluation succeeds,
        otherwise "Unsafe Code Detected!".
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(expression_code, mode='eval')

        # Walk the tree to ensure only safe nodes are present
        for node in ast.walk(parsed):
            if isinstance(node, (ast.Import, ast.ImportFrom, ast.Exec,
                                 ast.Module, ast.FunctionDef, ast.ClassDef,
                                 ast.Lambda, ast.Assign, ast.AugAssign)):
                raise ValueError("Disallowed syntax detected")

        result = _eval(parsed)
        return str(result)

    except Exception:
        # Any error (parsing, disallowed node, runtime) is treated as unsafe
        return "Unsafe Code Detected!"