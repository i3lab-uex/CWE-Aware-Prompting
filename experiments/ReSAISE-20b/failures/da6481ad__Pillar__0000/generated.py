import ast
import operator as op

# Supported operators mapping
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

# Allowed constants
_ALLOWED_CONSTANTS = {
    "pi": 3.141592653589793,
    "e": 2.718281828459045,
}

def _eval(node: ast.AST) -> float:
    if isinstance(node, ast.Num):  # <Python<3.8
        return node.n
    if isinstance(node, ast.Constant):  # <Python>=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value)}")
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Operator {op_type.__name__} not allowed")
    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unary operator {op_type.__name__} not allowed")
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    if isinstance(node, ast.Call):
        # Disallow function calls for safety
        raise ValueError("Function calls are not allowed")
    if isinstance(node, ast.Name):
        if node.id in _ALLOWED_CONSTANTS:
            return _ALLOWED_CONSTANTS[node.id]
        raise ValueError(f"Unknown identifier: {node.id}")
    if isinstance(node, ast.Module):
        # Allow a single expression in the module body
        if len(node.body) != 1:
            raise ValueError("Only a single expression is allowed")
        return _eval(node.body[0])
    raise ValueError(f"Unsupported syntax: {ast.dump(node)}")

def secure_math_eval(expr_str: str) -> float:
    """
    Evaluate a mathematical expression safely.

    Parameters
    ----------
    expr_str : str
        The expression to evaluate.

    Returns
    -------
    float
        Result of the evaluation.

    Raises
    ------
    ValueError
        If the expression contains unsafe or unsupported syntax.
    """
    if not isinstance(expr_str, str):
        raise ValueError("Input must be a string")

    # Strip whitespace to avoid accidental leading/trailing characters
    expr_str = expr_str.strip()
    if not expr_str:
        raise ValueError("Empty expression")

    try:
        parsed = ast.parse(expr_str, mode="eval")
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Walk the AST to ensure no disallowed nodes are present
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.Exec, ast.Call)):
            raise ValueError("Disallowed operation detected")
        if isinstance(node, ast.Attribute):
            raise ValueError("Attribute access is not allowed")

    result = _eval(parsed)
    if isinstance(result, complex):
        raise ValueError("Complex numbers are not supported")
    return result