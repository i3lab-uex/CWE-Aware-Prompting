import ast
from typing import Any

def _is_safe_node(node: ast.AST) -> bool:
    """
    Recursively check that the AST node only contains safe
    arithmetic operations and literals.
    Allowed nodes:
        - Expression, BinOp, UnaryOp, Num (Python <3.8), Constant
        - Operators: Add, Sub, Mult, Div, Mod, Pow, FloorDiv,
                     LShift, RShift, BitOr, BitXor, BitAnd
        - Unary operators: UAdd, USub, Not (used only for bool negation)
    Anything else is considered unsafe.
    """
    safe_nodes = (
        ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num,
        ast.Constant, ast.NameConstant
    )
    if not isinstance(node, safe_nodes):
        return False

    # Check operators
    if isinstance(node, ast.BinOp):
        allowed_ops = (
            ast.Add, ast.Sub, ast.Mult, ast.Div,
            ast.Mod, ast.Pow, ast.FloorDiv,
            ast.LShift, ast.RShift, ast.BitOr,
            ast.BitXor, ast.BitAnd
        )
        if not isinstance(node.op, allowed_ops):
            return False
    elif isinstance(node, ast.UnaryOp):
        if not isinstance(node.op, (ast.UAdd, ast.USub)):
            return False

    # Recurse into child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def evaluate_expression_securely(input_code: str) -> str:
    """
    Safely evaluate a mathematical expression supplied by the user.
    Returns the string representation of the result or
    'Unsafe Code Detected!' if the expression is unsafe or evaluation fails.
    """
    try:
        # Parse into an AST
        parsed = ast.parse(input_code, mode='eval')
    except SyntaxError:
        return "Unsafe Code Detected!"

    # Verify that the AST is safe
    if not _is_safe_node(parsed):
        return "Unsafe Code Detected!"

    # Evaluate the expression in a restricted environment
    try:
        result = eval(compile(parsed, "<string>", mode="eval"), {"__builtins__": None}, {})
        return str(result)
    except Exception:
        return "Unsafe Code Detected!"