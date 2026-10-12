import ast
import operator as op

# Supported operators mapping
_SUPPORTED_OPERATORS = {
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

def _eval(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    elif isinstance(node, ast.Num):  # For Python <3.8
        return node.n
    elif isinstance(node, ast.Constant):  # For Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
    elif isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in _SUPPORTED_OPERATORS:
            try:
                return _SUPPORTED_OPERATORS[op_type](left, right)
            except ZeroDivisionError as exc:
                raise ValueError("Division by zero") from exc
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
    elif isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in _SUPPORTED_OPERATORS:
            return _SUPPORTED_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
    elif isinstance(node, ast.Paren):  # Not present in AST; parentheses handled by grouping
        return _eval(node.value)
    else:
        raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def calculate_expression(math_expr: str):
    """
    Safely evaluate a simple arithmetic expression provided as a string.

    Parameters:
        math_expr (str): The user-provided mathematical expression.

    Returns:
        float | int: The computed result of the expression.

    Raises:
        ValueError: If the input contains unsupported characters, unsafe commands,
                    or invalid operations.
    """
    if not isinstance(math_expr, str):
        raise ValueError("Input must be a string")

    # Strip whitespace to avoid accidental comments or trailing characters
    expr = math_expr.strip()
    if not expr:
        raise ValueError("Empty expression")

    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc.msg}") from exc

    # Ensure the parsed AST contains only allowed nodes
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Call, ast.Attribute, ast.Import,
                            ast.ImportFrom, ast.FunctionDef,
                            ast.ClassDef, ast.Lambda)):
            raise ValueError(f"Disallowed construct: {type(node).__name__}")

    return _eval(parsed)