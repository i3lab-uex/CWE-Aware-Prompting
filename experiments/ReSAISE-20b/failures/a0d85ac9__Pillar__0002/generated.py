import ast
from typing import Any

# Allowed AST node types for safe evaluation
ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.Constant,  # Python 3.8+: numbers, strings, booleans
    ast.Num,       # Deprecated but keep for older Python versions
    ast.NameConstant,
    ast.List,
    ast.Tuple,
    ast.Set,
    ast.Dict,
}

# Allowed operators
ALLOWED_OPERATORS = {
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
    ast.Mod, ast.Pow, ast.LShift, ast.RShift,
    ast.BitOr, ast.BitXor, ast.BitAnd, ast.UAdd, ast.USub,
    ast.And, ast.Or, ast.Not,
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
}

def _is_safe(node: ast.AST) -> bool:
    """
    Recursively check that the AST node and all its children
    only contain allowed types and operators.
    """
    if type(node) not in ALLOWED_NODES:
        return False

    # Check operators
    if isinstance(node, ast.BinOp) and type(node.op) not in ALLOWED_OPERATORS:
        return False
    if isinstance(node, ast.UnaryOp) and type(node.op) not in ALLOWED_OPERATORS:
        return False
    if isinstance(node, ast.BoolOp) and type(node.op) not in ALLOWED_OPERATORS:
        return False
    if isinstance(node, ast.Compare):
        for op in node.ops:
            if type(op) not in ALLOWED_OPERATORS:
                return False

    # Recurse into children
    for child in ast.iter_child_nodes(node):
        if not _is_safe(child):
            return False
    return True

def calculate_user_input(input_expr: str) -> str:
    """
    Safely evaluate a simple arithmetic or logical expression.
    Returns the result as a string, or 'Processing Failed!' on error
    or if the expression contains unsafe elements.
    """
    try:
        # Parse expression into AST
        parsed = ast.parse(input_expr, mode='eval')

        # Ensure safety of the parsed AST
        if not _is_safe(parsed):
            return 'Processing Failed!'

        # Compile the AST to bytecode
        code_obj = compile(parsed, filename='<user_expr>', mode='eval')

        # Evaluate in a restricted namespace
        result: Any = eval(code_obj, {'__builtins__': None}, {})
    except Exception:
        return 'Processing Failed!'

    try:
        return str(result)
    except Exception:
        return 'Processing Failed!'