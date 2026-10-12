import ast
import operator
from typing import Any, Dict

# Mapping of AST operator nodes to actual Python functions.
_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.MatMult: operator.matmul,   # optional
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

class EvalError(ValueError):
    """Custom exception for evaluation errors."""


def _eval_node(node: ast.AST, mapping: Dict[str, Any]) -> Any:
    """
    Recursively evaluate an AST node safely.
    Only a small subset of nodes is allowed.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body, mapping)

    # Numbers (Python 3.8+ uses Constant)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise EvalError(f"Unsupported constant type: {type(node.value).__name__}")

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left, mapping)
        right = _eval_node(node.right, mapping)
        op_type = type(node.op)
        if op_type not in _BIN_OPS:
            raise EvalError(f"Unsupported binary operator: {op_type.__name__}")
        try:
            return _BIN_OPS[op_type](left, right)
        except Exception as exc:
            raise EvalError(f"Error evaluating binary operation: {exc}") from exc

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand, mapping)
        op_type = type(node.op)
        if op_type not in _UNARY_OPS:
            raise EvalError(f"Unsupported unary operator: {op_type.__name__}")
        try:
            return _UNARY_OPS[op_type](operand)
        except Exception as exc:
            raise EvalError(f"Error evaluating unary operation: {exc}") from exc

    # Variable names
    if isinstance(node, ast.Name):
        if node.id in mapping:
            val = mapping[node.id]
            if isinstance(val, (int, float)):
                return val
            raise EvalError(f"Variable '{node.id}' is not numeric")
        else:
            raise EvalError(f"Undefined variable: {node.id}")

    # Parenthesized expressions are just the inner expression
    if isinstance(node, ast.Paren):
        return _eval_node(node.value, mapping)

    # Unsupported nodes
    raise EvalError(f"Unsupported expression element: {type(node).__name__}")


def evaluate_math_expr(math_expression: str, variable_mapping: Dict[str, Any]) -> str:
    """
    Safely evaluate a mathematical expression with optional variables.

    Parameters
    ----------
    math_expression : str
        The mathematical expression to evaluate.
    variable_mapping : dict
        Mapping of variable names (str) to numeric values.

    Returns
    -------
    str
        The evaluated result converted to string. Integer results are returned
        without a decimal point.

    Raises
    ------
    ValueError
        If the expression is invalid or evaluation fails.
    """
    if not isinstance(math_expression, str):
        raise ValueError("math_expression must be a string")

    if not isinstance(variable_mapping, dict):
        raise ValueError("variable_mapping must be a dictionary")

    try:
        # Parse the expression in eval mode to get an AST
        parsed = ast.parse(math_expression, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from exc

    try:
        result = _eval_node(parsed, variable_mapping)
    except EvalError as exc:
        raise ValueError(f"Evaluation error: {exc}") from exc

    # Convert to string; strip trailing .0 for ints
    if isinstance(result, float) and result.is_integer():
        return str(int(result))
    return str(result)