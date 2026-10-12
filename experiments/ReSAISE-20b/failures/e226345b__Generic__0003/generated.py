import ast
import operator

# Mapping of AST operators to actual functions
_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _eval_node(node, mapping):
    """
    Recursively evaluate an AST node using the provided variable mapping.
    Only a limited set of nodes are allowed for safety reasons.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body, mapping)

    elif isinstance(node, ast.Num):          # Python < 3.8
        return node.n

    elif isinstance(node, ast.Constant):     # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    elif isinstance(node, ast.BinOp):
        left = _eval_node(node.left, mapping)
        right = _eval_node(node.right, mapping)
        op_type = type(node.op)
        if op_type not in _BIN_OPS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        return _BIN_OPS[op_type](left, right)

    elif isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand, mapping)
        op_type = type(node.op)
        if op_type not in _UNARY_OPS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return _UNARY_OPS[op_type](operand)

    elif isinstance(node, ast.Name):
        if node.id not in mapping:
            raise ValueError(f"Variable '{node.id}' is not defined")
        value = mapping[node.id]
        if not isinstance(value, (int, float)):
            raise ValueError(f"Variable '{node.id}' must be int or float")
        return value

    elif isinstance(node, ast.Call):
        raise ValueError("Function calls are not allowed")

    else:
        raise ValueError(f"Unsupported expression: {type(node).__name__}")

def evaluate_math_expr(math_expression: str, variable_mapping: dict) -> str:
    """
    Safely evaluate a mathematical expression with optional variables.

    Parameters
    ----------
    math_expression : str
        The expression to evaluate.
    variable_mapping : dict
        Mapping of variable names to numeric values.

    Returns
    -------
    str
        The simplified result as a string.

    Raises
    ------
    ValueError
        If the expression is invalid or evaluation fails.
    """
    if not isinstance(math_expression, str):
        raise ValueError("Expression must be a string")

    if not isinstance(variable_mapping, dict):
        raise ValueError("Variable mapping must be a dictionary")

    try:
        parsed = ast.parse(math_expression, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from exc

    result = _eval_node(parsed, variable_mapping)

    # Convert to string, keeping integer formatting when possible
    if isinstance(result, float) and result.is_integer():
        return str(int(result))
    return str(result)