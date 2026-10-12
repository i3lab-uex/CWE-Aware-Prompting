import ast
import operator
from typing import Any, Dict

# Supported binary operators mapping
_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Supported unary operators mapping
_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _eval_node(node: ast.AST, var_map: Dict[str, Any]) -> Any:
    """
    Recursively evaluate an AST node using the provided variable mapping.
    Raises ValueError on unsupported nodes or missing variables.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body, var_map)

    # Numbers
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    # Variables (Names)
    if isinstance(node, ast.Name):
        if node.id in var_map:
            val = var_map[node.id]
            if isinstance(val, (int, float)):
                return val
            raise ValueError(f"Variable '{node.id}' must be int or float")
        raise ValueError(f"Undefined variable: {node.id}")

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left, var_map)
        right = _eval_node(node.right, var_map)
        op_type = type(node.op)
        if op_type in _BIN_OPS:
            return _BIN_OPS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand, var_map)
        op_type = type(node.op)
        if op_type in _UNARY_OPS:
            return _UNARY_OPS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    # Parentheses are just grouping, handled by the AST structure
    if isinstance(node, ast.Paren):
        return _eval_node(node.value, var_map)

    raise ValueError(f"Unsupported expression component: {type(node).__name__}")

def evaluate_math_expr(math_expression: str, variable_mapping: Dict[str, Any]) -> str:
    """
    Safely evaluate a mathematical expression with optional variables.

    Parameters
    ----------
    math_expression : str
        The mathematical expression to evaluate.
    variable_mapping : dict
        Mapping from variable names (str) to numeric values (int or float).

    Returns
    -------
    str
        The evaluated result as a string.

    Raises
    ------
    ValueError
        If the expression contains unsupported syntax, undefined variables,
        or evaluation fails.
    """
    if not isinstance(math_expression, str):
        raise ValueError("math_expression must be a string")

    try:
        # Parse the expression in 'eval' mode to get an AST
        expr_ast = ast.parse(math_expression, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from exc

    # Ensure the AST contains only allowed nodes
    for node in ast.walk(expr_ast):
        if isinstance(node, (ast.Call, ast.Attribute, ast.Subscript,
                            ast.Lambda, ast.FunctionDef, ast.ClassDef)):
            raise ValueError(f"Unsupported node type: {type(node).__name__}")

    # Evaluate the parsed AST
    try:
        result = _eval_node(expr_ast, variable_mapping)
    except Exception as exc:  # Catch all evaluation errors
        raise ValueError(f"Evaluation error: {exc}") from exc

    # Convert result to string; keep integer representation if possible
    if isinstance(result, float) and result.is_integer():
        return str(int(result))
    return str(result)