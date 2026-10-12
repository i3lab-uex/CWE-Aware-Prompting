import ast
import operator

# Supported binary operators mapping
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

def _eval_node(node):
    """
    Recursively evaluate an AST node that represents a numeric expression.
    Only allows literals and the operators defined in _ALLOWED_OPERATORS.
    """
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported operator: {op_type}")
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +operand
        if isinstance(node.op, ast.USub):
            return -operand
        raise ValueError(f"Unsupported unary operator: {type(node.op)}")
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
    raise ValueError(f"Unsupported expression type: {type(node)}")

def evaluate_expression(user_expr: str) -> str:
    """
    Safely evaluates a simple numeric expression supplied by the user.
    
    Parameters
    ----------
    user_expr : str
        The user-supplied expression to evaluate.

    Returns
    -------
    str
        String representation of the evaluated result, or 'Processing Failed!'
        if evaluation fails or input is unsafe.
    """
    try:
        # Parse expression into AST
        parsed = ast.parse(user_expr, mode='eval')
        # Ensure the tree only contains allowed nodes
        for node in ast.walk(parsed):
            if not isinstance(node, (ast.Expression, ast.BinOp,
                                     ast.UnaryOp, ast.Num, ast.Constant)):
                return 'Processing Failed!'
        result = _eval_node(parsed)
        return str(result)
    except Exception:
        # Any exception, including syntax errors or disallowed nodes,
        # results in a failure response.
        return 'Processing Failed!'