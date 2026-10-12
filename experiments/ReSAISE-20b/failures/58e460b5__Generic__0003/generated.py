import ast
import operator as op

# Supported operators mapping
_BIN_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}
_UNARY_OPS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

def _eval(node, var_dict):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Expression):
        return _eval(node.body, var_dict)
    elif isinstance(node, ast.Num):  # For Python <3.8
        return node.n
    elif isinstance(node, ast.Constant):  # For Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
    elif isinstance(node, ast.BinOp):
        left = _eval(node.left, var_dict)
        right = _eval(node.right, var_dict)
        op_func = _BIN_OPs.get(type(node.op))
        if op_func is None:
            raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
        return op_func(left, right)
    elif isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand, var_dict)
        op_func = _UNARY_OPs.get(type(node.op))
        if op_func is None:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        return op_func(operand)
    elif isinstance(node, ast.Name):
        if node.id in var_dict:
            return var_dict[node.id]
        raise ValueError(f"Undefined variable: {node.id}")
    elif isinstance(node, ast.Call):
        raise ValueError("Function calls are not allowed")
    else:
        raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def execute_calculation_string(calc_expr: str, var_dict: dict) -> str:
    """
    Evaluate a mathematical expression with optional variables.

    Parameters
    ----------
    calc_expr : str
        The expression to evaluate.
    var_dict : dict
        Mapping of variable names to numeric values.

    Returns
    -------
    str
        The computed result as a string.

    Raises
    ------
    ValueError
        If the expression contains unsupported syntax or evaluation fails.
    """
    if not isinstance(calc_expr, str):
        raise ValueError("calc_expr must be a string")
    if not isinstance(var_dict, dict):
        raise ValueError("var_dict must be a dictionary")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(calc_expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax in expression: {exc}") from exc

    # Evaluate the parsed AST safely
    try:
        result = _eval(parsed, var_dict)
    except Exception as exc:  # Catch all evaluation errors
        raise ValueError(f"Failed to evaluate expression: {exc}") from exc

    return str(result)