import ast
import operator as op
import re

# Allowed operators mapping from AST nodes to actual functions
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
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

def _eval_node(node: ast.AST, var_map: dict) -> float:
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Expression):
        return _eval_node(node.body, var_map)

    if isinstance(node, (ast.Num, ast.Constant)):
        # For Python 3.8+, constants can be of many types
        return node.n if hasattr(node, "n") else node.value

    if isinstance(node, ast.Name):
        if node.id in var_map:
            return var_map[node.id]
        raise ValueError(f"Undefined variable: {node.id}")

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left, var_map)
        right = _eval_node(node.right, var_map)
        op_func = _ALLOWED_OPERATORS.get(type(node.op))
        if not op_func:
            raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
        return op_func(left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand, var_map)
        op_func = _ALLOWED_OPERATORS.get(type(node.op))
        if not op_func:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        return op_func(operand)

    raise ValueError(f"Unsupported expression component: {type(node).__name__}")

def evaluate_expression(expr: str, var_map: dict) -> str:
    """
    Safely evaluate a mathematical expression with optional variables.

    Parameters
    ----------
    expr : str
        The expression to evaluate. May contain numeric literals and variable names.
    var_map : dict
        Mapping of variable names to numeric values.

    Returns
    -------
    str
        The string representation of the evaluated result.

    Raises
    ------
    ValueError
        If the expression contains unsupported syntax or if evaluation fails.
    """
    # Basic sanity check: allow only digits, operators, parentheses, dots and variable names
    if not re.fullmatch(r"[0-9a-zA-Z_+\-*/%^().\s]+", expr):
        raise ValueError("Expression contains invalid characters")

    try:
        parsed = ast.parse(expr, mode="eval")
    except SyntaxError as e:
        raise ValueError(f"Invalid expression syntax: {e}") from None

    # Ensure only allowed node types are present
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed expression component: {type(node).__name__}")

    result = _eval_node(parsed, var_map)

    # Convert to string with minimal formatting
    return str(result)