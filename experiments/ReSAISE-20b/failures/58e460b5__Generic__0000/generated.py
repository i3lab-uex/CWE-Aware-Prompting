import ast
import operator as op

# Supported binary operators mapping from AST to actual functions
_BIN_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}

# Supported unary operators mapping
_UNARY_OPS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

def _eval_node(node, var_dict):
    """Recursively evaluate an AST node safely."""
    if isinstance(node, ast.Expression):
        return _eval_node(node.body, var_dict)

    # Numbers (Python 3.8+ use Constant)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

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

    # Variables
    if isinstance(node, ast.Name):
        if node.id in var_dict:
            val = var_dict[node.id]
            if isinstance(val, (int, float)):
                return val
            raise ValueError(f"Variable '{node.id}' has non-numeric value")
        raise ValueError(f"Undefined variable: {node.id}")

    # Parentheses are handled by grouping in the AST
    if isinstance(node, ast.Paren):
        return _eval_node(node.value, var_dict)

    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def execute_calculation_string(calc_expr: str, var_dict: dict) -> str:
    """
    Evaluate a mathematical expression string with optional variables.

    Parameters
    ----------
    calc_expr : str
        The expression to evaluate, e.g. "2 * (x + 3)".
    var_dict : dict
        Mapping of variable names to numeric values.

    Returns
    -------
    str
        The computed result as a string.

    Raises
    ------
    ValueError
        If the expression is syntactically invalid or contains unsupported elements.
    """
    if not isinstance(calc_expr, str):
        raise ValueError("calc_expr must be a string")
    if not isinstance(var_dict, dict):
        raise ValueError("var_dict must be a dictionary")

    try:
        # Parse expression in eval mode; this returns an ast.Expression node
        tree = ast.parse(calc_expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from exc

    # Evaluate the parsed AST
    try:
        result = _eval_node(tree, var_dict)
    except Exception as exc:
        raise ValueError(f"Failed to evaluate expression: {exc}") from exc

    # Convert result to string, stripping trailing .0 for ints
    if isinstance(result, float) and result.is_integer():
        return str(int(result))
    return str(result)