import ast
import operator as op
import re
from typing import Dict, Any

# Mapping of supported operators to their corresponding functions
_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}

# Mapping of supported unary operators
_UNARY_OPERATORS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

def _eval(node: ast.AST, var_map: Dict[str, Any]) -> Any:
    """
    Recursively evaluate an AST node using the provided variable mapping.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body, var_map)
    elif isinstance(node, ast.Num):  # For Python <3.8
        return node.n
    elif isinstance(node, ast.Constant):  # For Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value)}")
    elif isinstance(node, ast.BinOp):
        left = _eval(node.left, var_map)
        right = _eval(node.right, var_map)
        operator_func = _OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError(f"Unsupported binary operator: {ast.dump(node.op)}")
        return operator_func(left, right)
    elif isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand, var_map)
        operator_func = _UNARY_OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError(f"Unsupported unary operator: {ast.dump(node.op)}")
        return operator_func(operand)
    elif isinstance(node, ast.Name):
        if node.id in var_map:
            return var_map[node.id]
        raise ValueError(f"Undefined variable: {node.id}")
    elif isinstance(node, ast.Call):
        raise ValueError("Function calls are not allowed.")
    else:
        raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def _sanitize_expr(expr: str) -> str:
    """
    Remove any potentially dangerous characters that could lead to command injection.
    Only allow digits, whitespace, operators, parentheses, decimal points, and variable names.
    """
    # Allow letters, digits, underscore for variables
    if not re.fullmatch(r"[A-Za-z0-9_\.\+\-\*/\^\(\) ]*", expr):
        raise ValueError("Expression contains invalid characters.")
    return expr

def evaluate_expression(expr: str, var_map: Dict[str, Any]) -> str:
    """
    Evaluate a mathematical expression with optional variable substitution.

    Parameters
    ----------
    expr : str
        The mathematical expression to evaluate.
    var_map : dict
        Mapping of variable names (str) to numeric values.

    Returns
    -------
    str
        The simplified result as a string.

    Raises
    ------
    ValueError
        If the expression is invalid or evaluation fails.
    """
    # 1. Sanitize input to avoid command injection or other unsafe patterns
    expr = _sanitize_expr(expr)

    # 2. Parse expression into an AST safely
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from exc

    # 3. Ensure that the AST only contains allowed nodes
    for node in ast.walk(parsed):
        if not isinstance(node, (ast.Expression, ast.BinOp, ast.UnaryOp,
                                 ast.Num, ast.Constant, ast.Name,
                                 ast.Add, ast.Sub, ast.Mult, ast.Div,
                                 ast.FloorDiv, ast.Mod, ast.Pow,
                                 ast.UAdd, ast.USub)):
            raise ValueError(f"Disallowed expression component: {ast.dump(node)}")

    # 4. Evaluate the AST
    try:
        result = _eval(parsed, var_map)
    except Exception as exc:
        raise ValueError(f"Evaluation error: {exc}") from exc

    # 5. Return the result as a string
    return str(result)