import ast
import operator

# Mapping of allowed AST operators to actual Python functions
_ALLOWED_OPERATORS = {
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

# Mapping of allowed AST unary operators
_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,  # root
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8 (numbers)
    ast.NameConstant, # True/False/None
)

def _eval_node(node):
    """
    Recursively evaluate an AST node, ensuring only allowed nodes and operators are used.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    if isinstance(node, (ast.Num, ast.Constant)):
        # Only numeric constants are allowed
        value = node.n if isinstance(node, ast.Num) else node.value
        if isinstance(value, (int, float)):
            return value
        raise ValueError("Unsupported constant type")

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Operator {op_type.__name__} not allowed")

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_UNARY_OPERATORS:
            return _ALLOWED_UNARY_OPERATORS[op_type](operand)
        raise ValueError(f"Unary operator {op_type.__name__} not allowed")

    # Reject any other node types
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def process_user_expression(expr: str) -> str:
    """
    Safely evaluate a simple arithmetic expression provided by the user.
    
    Parameters
    ----------
    expr : str
        The user-provided expression to evaluate.

    Returns
    -------
    str
        The result of the evaluated expression as a string, or
        'Processing Failed!' if the expression is invalid or unsafe.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode='eval')

        # Ensure all nodes in the tree are allowed
        for node in ast.walk(parsed):
            if not isinstance(node, _ALLOWED_NODES):
                return 'Processing Failed!'

        # Evaluate the expression
        result = _eval_node(parsed)
        return str(result)

    except Exception:
        # Any error (syntax, evaluation, or security) leads to failure
        return 'Processing Failed!'