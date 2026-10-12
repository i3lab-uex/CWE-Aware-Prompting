import ast
import operator as op
from typing import Any, Dict

# Supported operators mapping
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

def _eval_node(node: ast.AST, vars_map: Dict[str, Any]) -> float:
    """
    Recursively evaluate an AST node safely.
    Only numeric literals, variables from vars_map, and allowed operators are permitted.
    """
    if isinstance(node, ast.Num):  # For Python <3.8
        return node.n

    if isinstance(node, ast.Constant):  # For Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.Name):
        if node.id in vars_map:
            val = vars_map[node.id]
            if isinstance(val, (int, float)):
                return val
            raise ValueError(f"Variable '{node.id}' has non-numeric value: {val!r}")
        raise ValueError(f"Undefined variable: '{node.id}'")

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left, vars_map)
        right = _eval_node(node.right, vars_map)
        operator_func = _ALLOWED_OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError(f"Unsupported binary operator: {ast.dump(node.op)}")
        return operator_func(left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand, vars_map)
        operator_func = _ALLOWED_OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError(f"Unsupported unary operator: {ast.dump(node.op)}")
        return operator_func(operand)

    # Disallow any other node types (e.g., calls, attribute access)
    raise ValueError(f"Unsupported expression component: {ast.dump(node)}")

def simplify_math_expression(formula_str: str, vars_mapping: Dict[str, Any]) -> str:
    """
    Evaluate a mathematical expression with optional variables.

    Parameters
    ----------
    formula_str : str
        The arithmetic expression to evaluate. May contain +, -, *, /, **, % and variables.
    vars_mapping : dict
        Mapping of variable names to numeric values.

    Returns
    -------
    str
        The evaluated result converted to a string.

    Raises
    ------
    ValueError
        If the expression is invalid, contains unsupported constructs,
        or if variable substitution fails.
    """
    try:
        # Parse the expression into an AST
        expr_ast = ast.parse(formula_str, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid expression syntax: {e}") from e

    # Ensure the top-level node is an Expression
    if not isinstance(expr_ast.body, ast.Expression):
        raise ValueError("Expression must be a single evaluable expression")

    try:
        result = _eval_node(expr_ast.body, vars_mapping)
    except Exception as exc:
        raise ValueError(f"Failed to evaluate expression: {exc}") from exc

    return str(result)