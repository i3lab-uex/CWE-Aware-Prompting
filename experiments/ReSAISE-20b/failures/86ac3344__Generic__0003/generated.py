import ast
import operator as op

# Allowed operators and their corresponding functions
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}

# Allowed nodes in the AST
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # For Python < 3.8
    ast.Constant,     # For Python >= 3.8
    ast.Call,
    ast.Name,
    ast.Load,
)

# Allowed functions from the math module
_ALLOWED_FUNCS = {
    "abs": abs,
    "round": round,
}

def _eval(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Num):  # Python < 3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python >= 3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        oper_func = _ALLOWED_OPERATORS.get(type(node.op))
        if oper_func is None:
            raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
        return oper_func(left, right)
    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        oper_func = _ALLOWED_OPERATORS.get(type(node.op))
        if oper_func is None:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        return oper_func(operand)
    if isinstance(node, ast.Call):
        func_name = getattr(node.func, "id", None)
        if func_name not in _ALLOWED_FUNCS:
            raise ValueError(f"Function '{func_name}' is not allowed")
        args = [_eval(arg) for arg in node.args]
        return _ALLOWED_FUNCS[func_name](*args)
    if isinstance(node, ast.Name):
        raise ValueError(f"Usage of variable '{node.id}' is not allowed")
    raise ValueError(f"Unsupported expression node: {type(node).__name__}")

def secure_eval_expression(exp: str):
    """
    Evaluate a mathematical expression safely.

    Parameters
    ----------
    exp : str
        User-provided string containing the mathematical expression.

    Returns
    -------
    int | float
        The result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters, functions,
        or AST nodes.
    """
    # Basic syntax check: only allowed characters (digits, operators, whitespace, parentheses)
    allowed_chars = set("0123456789+-*/%(). ")
    if not all(c in allowed_chars for c in exp):
        raise ValueError("Expression contains disallowed characters")

    try:
        parsed = ast.parse(exp, mode="eval")
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Ensure all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed expression element: {type(node).__name__}")

    # Evaluate the parsed AST
    return _eval(parsed.body)