import ast
import operator as op
import math

# Mapping of AST operators to actual functions
OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}

# Allowed unary operators
UNARY_OPERATORS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed names (constants and math functions)
ALLOWED_NAMES = {
    k: getattr(math, k) for k in dir(math) if not k.startswith("_")
}
# Add built-in constants
ALLOWED_NAMES.update({"pi": math.pi, "e": math.e})

def _eval(node: ast.AST):
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    elif isinstance(node, ast.Num):  # <Python 3.8
        return node.n

    elif isinstance(node, ast.Constant):  # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    elif isinstance(node, ast.BinOp):
        if type(node.op) not in OPERATORS:
            raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
        left = _eval(node.left)
        right = _eval(node.right)
        return OPERATORS[type(node.op)](left, right)

    elif isinstance(node, ast.UnaryOp):
        if type(node.op) not in UNARY_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        operand = _eval(node.operand)
        return UNARY_OPERATORS[type(node.op)](operand)

    elif isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name) or node.func.id not in ALLOWED_NAMES:
            raise ValueError(f"Function '{getattr(node.func, 'id', None)}' is not allowed")
        func = ALLOWED_NAMES[node.func.id]
        args = [_eval(arg) for arg in node.args]
        if node.keywords:
            raise ValueError("Keyword arguments are not allowed")
        return func(*args)

    elif isinstance(node, ast.Name):
        if node.id not in ALLOWED_NAMES:
            raise ValueError(f"Name '{node.id}' is not allowed")
        return ALLOWED_NAMES[node.id]

    else:
        raise ValueError(f"Unsupported expression: {type(node).__name__}")

def safe_execute_operation(operation: str):
    """
    Safely evaluate a mathematical operation string.

    Parameters
    ----------
    operation : str
        A mathematical expression (e.g., "2 + 3 * sin(pi/4)").

    Returns
    -------
    float or int
        The result of the evaluated expression.

    Raises
    ------
    ValueError
        If the expression contains unsafe or unsupported elements.
    """
    try:
        parsed = ast.parse(operation, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Ensure only allowed node types are present
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Module,)):
            continue
        if not isinstance(
            node,
            (
                ast.Expression,
                ast.Num,
                ast.Constant,
                ast.BinOp,
                ast.UnaryOp,
                ast.Call,
                ast.Name,
                ast.Load,
            ),
        ):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    return _eval(parsed)