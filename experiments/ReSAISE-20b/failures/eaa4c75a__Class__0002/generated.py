import ast
import operator
import re

# Supported binary operators mapping to their corresponding functions
_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Supported unary operators mapping to their corresponding functions
_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _eval_node(node, var_map):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Num):  # For Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # For Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left, var_map)
        right = _eval_node(node.right, var_map)
        op_type = type(node.op)
        if op_type in _BIN_OPS:
            return _BIN_OPS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand, var_map)
        op_type = type(node.op)
        if op_type in _UNARY_OPS:
            return _UNARY_OPS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
    if isinstance(node, ast.Name):
        id_ = node.id
        if id_ in var_map:
            val = var_map[id_]
            if isinstance(val, (int, float)):
                return val
            raise ValueError(f"Variable '{id_}' must be int or float")
        raise ValueError(f"Unknown variable: {id_}")
    if isinstance(node, ast.Expression):
        return _eval_node(node.body, var_map)
    # Allow parentheses via Expr nodes
    if isinstance(node, ast.Expr):
        return _eval_node(node.value, var_map)
    raise ValueError(f"Unsupported expression node: {type(node).__name__}")

def evaluate_expression(expr: str, var_map: dict) -> str:
    """
    Safely evaluate a mathematical expression with optional variable substitution.

    Parameters
    ----------
    expr : str
        The arithmetic expression to evaluate.
    var_map : dict
        Mapping of variable names (str) to numeric values (int or float).

    Returns
    -------
    str
        The simplified result as a string.

    Raises
    ------
    ValueError
        If the expression is invalid or contains unsupported elements.
    """
    if not isinstance(expr, str):
        raise ValueError("Expression must be a string")
    if not isinstance(var_map, dict):
        raise ValueError("Variable map must be a dictionary")

    # Basic syntax check: allow only digits, operators, parentheses and variable names
    if not re.fullmatch(r"[0-9\.\+\-\*\/\%\^\(\)\s]*|[a-zA-Z_][a-zA-Z0-9_\.\+\-\*\/\%\^\(\)\s]*", expr):
        raise ValueError("Expression contains invalid characters")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in expression: {e}")

    # Evaluate the parsed AST
    try:
        result = _eval_node(parsed, var_map)
    except Exception as e:
        raise ValueError(f"Failed to evaluate expression: {e}")

    return str(result)