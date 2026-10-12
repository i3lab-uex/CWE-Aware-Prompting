import ast
import operator
from typing import Any, Dict

# Mapping of AST operator nodes to actual functions
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


def evaluate_expression(expr: str, var_map: Dict[str, Any]) -> str:
    """
    Safely evaluate a mathematical expression that may contain variables.

    Parameters
    ----------
    expr : str
        The expression to evaluate.
    var_map : dict
        Mapping of variable names to numeric values.

    Returns
    -------
    str
        The evaluated result as a string.

    Raises
    ------
    ValueError
        If the expression contains unsupported syntax or if evaluation fails.
    """
    try:
        # Parse expression into an AST node
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from exc

    def _eval(node: ast.AST) -> Any:
        if isinstance(node, ast.Expression):
            return _eval(node.body)

        # Numbers (Python 3.8+ uses Constant)
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

        # Binary operations
        if isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_type = type(node.op)
            if op_type in _BIN_OPS:
                return _BIN_OPS[op_type](left, right)
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

        # Unary operations
        if isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            op_type = type(node.op)
            if op_type in _UNARY_OPS:
                return _UNARY_OPS[op_type](operand)
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

        # Variable names
        if isinstance(node, ast.Name):
            if node.id in var_map:
                val = var_map[node.id]
                if isinstance(val, (int, float)):
                    return val
                raise ValueError(f"Variable '{node.id}' has non-numeric value")
            raise ValueError(f"Undefined variable: {node.id}")

        # Disallow everything else
        raise ValueError(f"Unsupported expression element: {type(node).__name__}")

    try:
        result = _eval(parsed)
    except Exception as exc:  # Catch any unexpected error during evaluation
        raise ValueError(f"Evaluation failed: {exc}") from exc

    # Convert result to string, preserving integer formatting when possible
    if isinstance(result, float) and result.is_integer():
        return str(int(result))
    return str(result)