import ast
import operator as op

# Mapping of allowed operators to their corresponding functions
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

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Call,
    ast.Name,
    ast.Load,
)

# Whitelist of allowed names (functions, constants)
_ALLOWED_NAMES = {
    "abs": abs,
    "round": round,
    "min": min,
    "max": max,
}

def _eval(node):
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    elif isinstance(node, ast.Num):          # Python <3.8
        return node.n
    elif isinstance(node, ast.Constant):     # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
    elif isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
        left = _eval(node.left)
        right = _eval(node.right)
        return _ALLOWED_OPERATORS[type(node.op)](left, right)
    elif isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        operand = _eval(node.operand)
        return _ALLOWED_OPERATORS[type(node.op)](operand)
    elif isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only direct function calls are allowed")
        func_name = node.func.id
        if func_name not in _ALLOWED_NAMES:
            raise ValueError(f"Function '{func_name}' is not allowed")
        args = [_eval(arg) for arg in node.args]
        return _ALLOWED_NAMES[func_name](*args)
    elif isinstance(node, ast.Name):
        # Allow only constants like 'pi' or 'e' if added to whitelist
        raise ValueError(f"Usage of names is not allowed: {node.id}")
    else:
        raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def evaluate_and_compute(calc_expr: str):
    """
    Safely evaluates a mathematical expression provided as a string.

    Parameters:
        calc_expr (str): The expression to evaluate.

    Returns:
        int | float: The evaluated result.

    Raises:
        ValueError: If the expression contains unsupported operators, characters,
                    or if evaluation fails.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(calc_expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}")

    # Verify all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Evaluate the parsed expression
    try:
        result = _eval(parsed)
    except Exception as exc:
        raise ValueError(f"Evaluation error: {exc}") from exc

    return result