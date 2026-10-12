import ast

# Allowed node types for a safe mathematical expression
_ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.FloorDiv,
    ast.Mod,
    ast.Pow,
    ast.UAdd,
    ast.USub,
    ast.LParen,       # Not a real node; parentheses are handled by the parser
}

# Allowed operators as strings for quick lookup
_ALLOWED_OPERATORS = {
    '+', '-', '*', '/', '//', '%', '**',
}

def _validate_node(node: ast.AST) -> None:
    """
    Recursively validate AST nodes to ensure only safe operations are present.
    Raises ValueError if an unsafe node is found.
    """
    # For Python <3.8, numbers are represented by ast.Num
    if isinstance(node, (ast.Num, ast.Constant)):
        # Constants must be numeric types
        if not isinstance(node.value, (int, float)):
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
        return

    if isinstance(node, ast.Expression):
        _validate_node(node.body)
        return

    if isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_NODES:
            raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
        _validate_node(node.left)
        _validate_node(node.right)
        return

    if isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_NODES:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        _validate_node(node.operand)
        return

    # Anything else is disallowed
    raise ValueError(f"Disallowed expression: {ast.dump(node)}")

def secure_eval_expression(exp: str):
    """
    Evaluate a simple mathematical expression safely.

    Parameters
    ----------
    exp : str
        The user-provided mathematical expression.

    Returns
    -------
    result : int | float
        The evaluated numeric result of the expression.

    Raises
    ------
    ValueError
        If the expression contains invalid or unsafe characters/operations.
    """
    # Strip whitespace and validate allowed characters
    if not exp.strip():
        raise ValueError("Empty expression")

    # Allow only digits, operators, parentheses, decimal points, and whitespace
    allowed_chars = set("0123456789+-*/%() .")
    if any(ch not in allowed_chars for ch in exp):
        raise ValueError("Expression contains invalid characters")

    try:
        # Parse expression into AST
        parsed = ast.parse(exp, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in expression: {e}")

    # Validate AST for safety
    _validate_node(parsed)

    # Evaluate safely with no globals or locals
    try:
        result = eval(compile(parsed, filename="<ast>", mode="eval"), {}, {})
    except Exception as e:
        raise ValueError(f"Error during evaluation: {e}")

    return result