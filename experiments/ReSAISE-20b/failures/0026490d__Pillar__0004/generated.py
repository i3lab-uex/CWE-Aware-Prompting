import ast
import operator

# Mapping of allowed AST operators to the corresponding Python functions.
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed node types.
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.UnaryOp,
    ast.UAdd,
    ast.USub,
)

def _eval_node(node: ast.AST) -> float:
    """
    Recursively evaluate an AST node that represents a mathematical expression.
    Only the nodes and operators listed in `_ALLOWED_NODES` and `_ALLOWED_OPERATORS`
    are permitted. Any other node or operator raises a ValueError.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Numbers (constant literals)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.Num):  # Backward compatibility for older Python versions
        return node.n

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return _ALLOWED_OPERATORS[op_type](operand)

    # If we reach here, the node type is not allowed.
    raise ValueError(f"Unsupported expression component: {type(node).__name__}")

def evaluate_expression(expr: str) -> float:
    """
    Safely parse and evaluate a basic arithmetic expression.

    Parameters
    ----------
    expr : str
        The mathematical expression to evaluate. Only numbers and the following operators are allowed:
        +  -  *  /  //  %  **

    Returns
    -------
    float
        The result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters, operators, or any other security risk.
    """
    if not isinstance(expr, str):
        raise ValueError("Expression must be a string.")

    # Remove whitespace for easier handling and to avoid issues with accidental newlines.
    expr = expr.strip()
    if not expr:
        raise ValueError("Empty expression.")

    try:
        # Parse the expression into an AST. `mode='eval'` ensures only expressions are parsed.
        node = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax in expression: {exc}") from exc

    # Walk the AST to ensure only allowed nodes are present.
    for subnode in ast.walk(node):
        if not isinstance(subnode, _ALLOWED_NODES):
            raise ValueError(f"Disallowed expression component: {type(subnode).__name__}")

    # Evaluate the AST recursively.
    try:
        result = _eval_node(node)
    except ZeroDivisionError as exc:
        raise ValueError("Division by zero.") from exc
    except Exception as exc:  # Catch any unexpected errors in evaluation.
        raise ValueError(f"Failed to evaluate expression: {exc}") from exc

    return result