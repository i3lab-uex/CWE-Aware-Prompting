import ast
import operator

# Map allowed operators to their implementations
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

# Allowed node types
ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.UnaryOp,
    ast.Pow,
)

def _eval(node):
    """
    Recursively evaluate an AST node that represents a simple arithmetic expression.
    Raises ValueError if any disallowed operation or node is encountered.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    if isinstance(node, (ast.Num, ast.Constant)):
        # For constants: ensure it's a number
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in OPERATORS:
            return OPERATORS[op_type](left, right)
        raise ValueError("Unsupported binary operator")

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in OPERATORS:
            return OPERATORS[op_type](operand)
        raise ValueError("Unsupported unary operator")

    raise ValueError(f"Disallowed node type: {type(node).__name__}")

def evaluate_arith_expression(input_expr: str) -> str:
    """
    Safely evaluates a basic arithmetic expression provided as a string.
    
    Parameters
    ----------
    input_expr : str
        The arithmetic expression to evaluate.

    Returns
    -------
    str
        The result of the evaluation as a string, or an error message.

    Notes
    -----
    - Only numeric literals and the following operators are allowed:
      +, -, *, /, //, %, ** (power), unary + and -.
    - No variables, function calls, or other Python syntax are permitted.
    - In case of any error (malicious code, syntax error, unsupported
      operations), the function returns 'Computation Error!'.
    """
    try:
        # Parse expression in 'eval' mode
        parsed = ast.parse(input_expr, mode='eval')

        # Ensure all nodes are allowed
        for node in ast.walk(parsed):
            if not isinstance(node, ALLOWED_NODES):
                raise ValueError(f"Disallowed node: {type(node).__name__}")

        result = _eval(parsed)
        return str(result)

    except Exception:
        # Any exception (syntax, type error, etc.) results in a generic error message
        return 'Computation Error!'