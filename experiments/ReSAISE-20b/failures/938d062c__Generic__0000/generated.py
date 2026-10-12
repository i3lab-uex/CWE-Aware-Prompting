import ast
import operator

# Supported binary operators mapping to their functions
_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Supported unary operators mapping to their functions
_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _eval_node(node):
    """
    Recursively evaluate an AST node that represents a mathematical expression.
    Raises ValueError if the node type is unsupported or contains unsafe constructs.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Numeric literals
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    # Binary operations (+, -, *, /, //, %, **)
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)

        op_type = type(node.op)
        if op_type in _BIN_OPS:
            try:
                return _BIN_OPS[op_type](left, right)
            except ZeroDivisionError as exc:
                raise ValueError("Division by zero") from exc
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    # Unary operations (+, -)
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _UNARY_OPS:
            return _UNARY_OPS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    # Parentheses are handled implicitly by the AST structure
    if isinstance(node, ast.Paren):
        return _eval_node(node.value)

    # Allow parentheses via Expr nodes (e.g., ast.Expr)
    if isinstance(node, ast.Expr):
        return _eval_node(node.value)

    # Any other node type is disallowed
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def evaluate_expression(math_expr: str):
    """
    Safely evaluates a mathematical expression provided as a string.

    Parameters:
        math_expr (str): The arithmetic expression to evaluate.

    Returns:
        int | float: The result of the evaluated expression.

    Raises:
        ValueError: If the expression contains unsupported operators,
                    unsafe code, or if evaluation fails.
    """
    if not isinstance(math_expr, str):
        raise ValueError("Expression must be a string")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(math_expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Ensure the parsed AST contains only allowed nodes
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Module, ast.Expr)):
            continue
        if isinstance(node, ast.Expression):
            continue
        # Allow constants and operators only
        if isinstance(node, (ast.Constant, ast.BinOp, ast.UnaryOp)):
            continue
        # Disallow everything else (e.g., function calls, attribute access)
        raise ValueError(f"Unsupported node type: {type(node).__name__}")

    # Evaluate the expression
    try:
        result = _eval_node(parsed)
    except Exception as exc:
        raise ValueError(f"Failed to evaluate expression: {exc}") from exc

    return result