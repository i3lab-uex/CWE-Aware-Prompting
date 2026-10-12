import ast
import operator

# Mapping of AST operator nodes to actual Python operators
_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
}
_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _eval_node(node, var_dict):
    """
    Recursively evaluate an AST node in a safe manner.
    Only a restricted subset of nodes is allowed.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body, var_dict)

    # Numbers (Python 3.8+ uses Constant)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    # For older Python versions, handle Num
    if isinstance(node, ast.Num):
        return node.n

    # Variable names
    if isinstance(node, ast.Name):
        if node.id in var_dict:
            val = var_dict[node.id]
            if isinstance(val, (int, float)):
                return val
            raise ValueError(f"Variable '{node.id}' must be a number")
        raise ValueError(f"Undefined variable: {node.id}")

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left, var_dict)
        right = _eval_node(node.right, var_dict)
        op_type = type(node.op)
        if op_type in _BIN_OPS:
            return _BIN_OPS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand, var_dict)
        op_type = type(node.op)
        if op_type in _UNARY_OPS:
            return _UNARY_OPS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    # Parentheses are handled by grouping in the AST
    if isinstance(node, ast.Paren):
        return _eval_node(node.value, var_dict)

    raise ValueError(f"Unsupported expression element: {type(node).__name__}")


def execute_calculation_string(calc_expr: str, var_dict: dict) -> str:
    """
    Evaluate a mathematical expression safely with variable substitution.

    Parameters
    ----------
    calc_expr : str
        The arithmetic expression to evaluate.
    var_dict : dict
        Mapping of variable names (str) to numeric values.

    Returns
    -------
    str
        The string representation of the computed result.

    Raises
    ------
    ValueError
        If the expression is syntactically invalid or contains unsupported nodes.
    """
    if not isinstance(calc_expr, str):
        raise ValueError("calc_expr must be a string")

    if not isinstance(var_dict, dict):
        raise ValueError("var_dict must be a dictionary")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(calc_expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from None

    # Evaluate the parsed AST
    try:
        result = _eval_node(parsed, var_dict)
    except ZeroDivisionError as exc:
        raise ValueError(f"Math error: {exc}") from None
    except Exception as exc:
        raise ValueError(f"Evaluation error: {exc}") from None

    # Convert result to string; keep float formatting concise
    if isinstance(result, float):
        return str(round(result, 10)).rstrip('0').rstrip('.') if '.' in str(result) else str(result)
    return str(result)