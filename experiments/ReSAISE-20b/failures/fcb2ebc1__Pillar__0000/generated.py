import ast
import operator as op
import re

# Allowed operators mapping
_ALLOWED_OPS = {
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
    ast.Expression, ast.BinOp, ast.UnaryOp,
    ast.Num, ast.Constant,  # Python <3.8 and >=3.8
    ast.Name,
)

def _eval_node(node, var_values):
    if isinstance(node, (ast.Num, ast.Constant)):
        return node.n if hasattr(node, 'n') else node.value

    if isinstance(node, ast.Name):
        try:
            return var_values[node.id]
        except KeyError as exc:
            raise ValueError(f"Undefined variable: {node.id}") from exc

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left, var_values)
        right = _eval_node(node.right, var_values)
        try:
            return _ALLOWED_OPS[type(node.op)](left, right)
        except KeyError as exc:
            raise ValueError(f"Unsupported binary operator: {node.op}") from exc

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand, var_values)
        try:
            return _ALLOWED_OPS[type(node.op)](operand)
        except KeyError as exc:
            raise ValueError(f"Unsupported unary operator: {node.op}") from exc

    raise ValueError(f"Disallowed expression element: {ast.dump(node)}")

def simplify_math_expr(math_expr: str, var_values: dict) -> str:
    """
    Safely evaluate a mathematical expression with optional variables.

    Parameters
    ----------
    math_expr : str
        The expression to evaluate, e.g. "2 * (x + 3)".
    var_values : dict
        Mapping of variable names to numeric values.

    Returns
    -------
    str
        The evaluated result as a string.

    Raises
    ------
    ValueError
        If the expression contains unsupported syntax or evaluation fails.
    """
    # Sanitize whitespace
    expr = math_expr.strip()

    # Basic sanity check: no disallowed characters (letters, digits, operators, parentheses)
    if not re.fullmatch(r"[0-9a-zA-Z_\.\+\-\*/\^%\(\)\s]+", expr):
        raise ValueError("Expression contains disallowed characters")

    # Replace caret '^' with Python exponent operator '**'
    expr = expr.replace("^", "**")

    try:
        parsed = ast.parse(expr, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Verify all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES) and not isinstance(node, (ast.operator, ast.unaryop)):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Evaluate
    try:
        result = _eval_node(parsed.body, var_values)
    except Exception as exc:
        raise ValueError(f"Evaluation error: {exc}") from exc

    return str(result)