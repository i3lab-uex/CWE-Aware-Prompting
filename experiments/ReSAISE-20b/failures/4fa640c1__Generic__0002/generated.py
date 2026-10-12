import ast
import operator

# Map of allowed AST node types to corresponding Python operators/functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

def _eval_node(node):
    """
    Recursively evaluate an AST node that represents a mathematical expression.
    Only allowed nodes are processed; any other node raises ValueError.
    """
    if isinstance(node, ast.Num):  # For Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # For Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
    if isinstance(node, ast.Paren):  # Not actually a node type; handled by grouping
        return _eval_node(node.value)
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def perform_safe_math(expression: str):
    """
    Safely evaluate a mathematical expression string containing only
    numbers and the following operators: +, -, *, /, //, %, **.
    Parentheses are allowed for grouping.

    Parameters:
        expression (str): The mathematical expression to evaluate.

    Returns:
        float or int: Result of the evaluated expression.

    Raises:
        ValueError: If the expression contains disallowed characters,
                    operators, or is malformed.
    """
    if not isinstance(expression, str):
        raise ValueError("Expression must be a string")

    # Strip whitespace and ensure no suspicious characters
    cleaned = expression.strip()
    if not cleaned:
        raise ValueError("Empty expression")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(cleaned, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid expression syntax: {e}") from None

    # Walk the AST to ensure only allowed nodes are present
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Module, ast.Expr)):
            continue  # top-level nodes are fine
        if isinstance(node, (ast.Num, ast.Constant, ast.BinOp,
                            ast.UnaryOp, ast.Expression)):
            continue
        # Disallow any other node types (e.g., Call, Name)
        raise ValueError(f"Disallowed expression element: {type(node).__name__}")

    # Evaluate the AST safely
    return _eval_node(parsed.body)