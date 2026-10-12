import ast
import operator as op

# Allowed operators mapping to corresponding functions
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

def _eval_node(node, var_map):
    """
    Recursively evaluate an AST node using only allowed operations and
    the provided variable mapping.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body, var_map)

    if isinstance(node, ast.Constant):  # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.Num):  # Python <3.8
        return node.n

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left, var_map)
        right = _eval_node(node.right, var_map)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand, var_map)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    if isinstance(node, ast.Name):
        if node.id in var_map:
            val = var_map[node.id]
            if isinstance(val, (int, float)):
                return val
            raise ValueError(f"Variable '{node.id}' must be numeric")
        raise ValueError(f"Undefined variable: {node.id}")

    if isinstance(node, ast.Call):
        raise ValueError("Function calls are not allowed")

    # Any other node type is disallowed
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def evaluate_expression(expr: str, var_map: dict) -> str:
    """
    Safely evaluate a mathematical expression containing numbers,
    basic arithmetic operators, and variables defined in var_map.

    Parameters
    ----------
    expr : str
        The expression to evaluate.
    var_map : dict
        Mapping from variable names (str) to numeric values.

    Returns
    -------
    str
        The evaluated result converted to a string.

    Raises
    ------
    ValueError
        If the expression is invalid, contains disallowed constructs,
        or evaluation fails.
    """
    if not isinstance(expr, str):
        raise ValueError("Expression must be a string")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}")

    # Ensure the AST contains only allowed nodes
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Module,)):
            continue  # Module node is only present when mode='exec'
        if isinstance(node, (ast.Expr,)):
            continue
        if not isinstance(node, (
                ast.Expression,
                ast.Constant,
                ast.Num,
                ast.BinOp,
                ast.UnaryOp,
                ast.Name,
        )):
            raise ValueError(f"Disallowed expression element: {type(node).__name__}")

    # Evaluate the parsed AST
    result = _eval_node(parsed, var_map)

    return str(result)