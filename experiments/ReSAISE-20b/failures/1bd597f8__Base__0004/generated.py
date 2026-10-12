import ast
import operator

# Mapping of AST operators to actual functions
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _safe_eval(node):
    """
    Recursively evaluate an AST node that represents a simple arithmetic
    expression. Only numeric literals and binary/unary operators are allowed.
    """
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)

    if isinstance(node, ast.Num):          # Python <3.8
        return node.n

    if isinstance(node, ast.Constant):     # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")

    if isinstance(node, ast.BinOp):
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)
        op_type = type(node.op)
        if op_type in OPERATORS:
            return OPERATORS[op_type](left, right)
        raise ValueError("Unsupported binary operator")

    if isinstance(node, ast.UnaryOp):
        operand = _safe_eval(node.operand)
        op_type = type(node.op)
        if op_type in OPERATORS:
            return OPERATORS[op_type](operand)
        raise ValueError("Unsupported unary operator")

    # Disallow any other node types (e.g., calls, attributes)
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def execute_user_input(user_input: str) -> str:
    """
    Safely evaluate a user-provided arithmetic expression.

    Parameters
    ----------
    user_input : str
        The string containing the expression to evaluate.

    Returns
    -------
    str
        Result of the evaluated expression as a string, or 'Processing Failed!'
        if evaluation fails or input is unsafe.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(user_input, mode='eval')

        # Ensure the tree only contains allowed nodes
        for node in ast.walk(parsed):
            if not isinstance(node, (ast.Expression, ast.BinOp,
                                     ast.UnaryOp, ast.Num, ast.Constant)):
                raise ValueError("Disallowed expression component")

        result = _safe_eval(parsed)
        return str(result)

    except Exception:
        # Any exception (syntax error, unsupported node, math error) results
        # in a generic failure response to avoid leaking information.
        return 'Processing Failed!'