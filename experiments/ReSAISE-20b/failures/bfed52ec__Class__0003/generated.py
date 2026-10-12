import ast
import operator as op

# Mapping of allowed operators to their functions
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

# Allowed names (constants)
_ALLOWED_NAMES = {
    "pi": 3.141592653589793,
    "e": 2.718281828459045,
}

def _eval(node):
    """
    Recursively evaluate an AST node ensuring only safe operations are performed.
    """
    if isinstance(node, ast.Num):  # <Python 3.8
        return node.n
    if isinstance(node, ast.Constant):  # <Python 3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        oper_type = type(node.op)
        if oper_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[oper_type](left, right)
        raise ValueError("Unsupported binary operator")
    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        oper_type = type(node.op)
        if oper_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[oper_type](operand)
        raise ValueError("Unsupported unary operator")
    if isinstance(node, ast.Name):
        if node.id in _ALLOWED_NAMES:
            return _ALLOWED_NAMES[node.id]
        raise ValueError(f"Use of name '{node.id}' is not allowed")
    if isinstance(node, ast.Expr):
        return _eval(node.value)
    raise ValueError("Unsupported expression")

def securely_compute_expression(formula: str) -> str:
    """
    Safely evaluate a simple mathematical expression provided as a string.

    Parameters
    ----------
    formula : str
        The user supplied mathematical expression to evaluate.

    Returns
    -------
    str
        String representation of the result if evaluation succeeds, otherwise
        'Processing Failed!'.

    Notes
    -----
    The function only permits numeric literals, the operators +, -, *, /,
    //, %, **, unary minus, and a limited set of constants (`pi`, `e`).
    Any other constructs (function calls, attribute access, imports,
    etc.) are rejected to mitigate injection risks.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(formula, mode="eval")

        # Ensure the parsed tree only contains allowed nodes
        for node in ast.walk(parsed):
            if not isinstance(node, (
                ast.Expression,
                ast.BinOp,
                ast.UnaryOp,
                ast.Num,
                ast.Constant,
                ast.Name,
                ast.Expr,
            )):
                raise ValueError("Disallowed node in expression")

        # Evaluate the parsed AST
        result = _eval(parsed.body)

        return str(result)
    except Exception:
        # Any exception (parsing, evaluation, or security check) leads to failure
        return "Processing Failed!"