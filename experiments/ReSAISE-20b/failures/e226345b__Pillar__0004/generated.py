import ast
import operator as op
import re

# Allowed operators mapping
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.FloorDiv: op.floordiv,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Name,
)

def _eval_node(node: ast.AST, variables: dict):
    if isinstance(node, ast.Num):  # <3.8
        return node.n
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
    if isinstance(node, ast.Name):
        if node.id in variables:
            return variables[node.id]
        raise ValueError(f"Undefined variable: {node.id}")
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left, variables)
        right = _eval_node(node.right, variables)
        oper_type = type(node.op)
        if oper_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[oper_type](left, right)
        raise ValueError(f"Unsupported binary operator: {oper_type.__name__}")
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand, variables)
        oper_type = type(node.op)
        if oper_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[oper_type](operand)
        raise ValueError(f"Unsupported unary operator: {oper_type.__name__}")
    raise ValueError(f"Unsupported AST node: {type(node).__name__}")

def _safe_parse(expr: str) -> ast.Expression:
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in expression: {e}") from None
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed expression element: {type(node).__name__}")
    return parsed

def evaluate_math_expr(math_expression: str, variable_mapping: dict) -> str:
    """
    Evaluate a mathematical expression with optional variables.

    Parameters
    ----------
    math_expression : str
        The arithmetic expression to evaluate.
    variable_mapping : dict
        Mapping from variable names (strings) to numeric values.

    Returns
    -------
    str
        The simplified result of the expression as a string.

    Raises
    ------
    ValueError
        If the expression is invalid or evaluation fails.
    """
    if not isinstance(math_expression, str):
        raise ValueError("math_expression must be a string")
    if not isinstance(variable_mapping, dict):
        raise ValueError("variable_mapping must be a dictionary")

    # Ensure all keys in variable_mapping are valid identifiers
    for key in variable_mapping:
        if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', key):
            raise ValueError(f"Invalid variable name: {key}")

    # Replace variables with placeholders to prevent accidental code execution
    expr = math_expression

    parsed_expr = _safe_parse(expr)

    try:
        result = _eval_node(parsed_expr.body, variable_mapping)
    except Exception as e:
        raise ValueError(f"Failed to evaluate expression: {e}") from None

    # Return result as string, preserving float/int formatting
    return str(result)