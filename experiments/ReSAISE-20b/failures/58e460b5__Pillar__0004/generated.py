import ast
import operator as op
from typing import Any, Dict

# Allowed binary operators mapping to functions
_ALLOWED_BINOPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}

# Allowed unary operators mapping to functions
_ALLOWED_UNOPS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed constants and names
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Name,
)

def _eval_node(node: ast.AST, var_dict: Dict[str, Any]) -> Any:
    """Recursively evaluate an AST node safely."""
    if isinstance(node, ast.Expression):
        return _eval_node(node.body, var_dict)

    if isinstance(node, ast.Num):  # Python <3.8
        return node.n

    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.Name):
        if node.id in var_dict:
            return var_dict[node.id]
        raise ValueError(f"Undefined variable: {node.id}")

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left, var_dict)
        right = _eval_node(node.right, var_dict)
        op_type = type(node.op)
        if op_type in _ALLOWED_BINOPS:
            return _ALLOWED_BINOPS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand, var_dict)
        op_type = type(node.op)
        if op_type in _ALLOWED_UNOPS:
            return _ALLOWED_UNOPS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    raise ValueError(f"Unsupported expression node: {type(node).__name__}")


def execute_calculation_string(calc_expr: str, var_dict: Dict[str, Any]) -> str:
    """
    Safely evaluate a mathematical expression string with optional variable substitution.

    Parameters
    ----------
    calc_expr : str
        The mathematical expression to evaluate.
    var_dict : dict
        Mapping of variable names to numeric values.

    Returns
    -------
    str
        The evaluated result converted to a string.

    Raises
    ------
    ValueError
        If the expression is invalid or contains unsupported constructs.
    """
    try:
        # Parse expression into an AST
        parsed = ast.parse(calc_expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Ensure all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed expression element: {type(node).__name__}")

    # Evaluate the parsed AST
    result = _eval_node(parsed, var_dict)

    return str(result)