import ast
from typing import Any

def _is_safe_node(node: ast.AST) -> bool:
    """
    Recursively verify that the AST node only contains safe operations.
    Allowed nodes: literals, binary/unary ops, comparisons,
    function calls to a whitelist of safe functions.
    """
    SAFE_NODES = (
        ast.Expression, ast.Module,
        ast.Expr, ast.Load,
        ast.Constant, ast.Num, ast.Str, ast.Bytes,  # literals
        ast.BinOp, ast.UnaryOp, ast.BoolOp,
        ast.Compare,
        ast.Call,
        ast.Name,
    )
    SAFE_NAMES = {
        'abs', 'round', 'min', 'max', 'len',
        # Add more safe builtins if needed
    }
    SAFE_OPS = (
        ast.Add, ast.Sub, ast.Mult, ast.Div,
        ast.FloorDiv, ast.Mod, ast.Pow,
        ast.UAdd, ast.USub,
        ast.And, ast.Or,
        ast.Eq, ast.NotEq, ast.Lt, ast.LtE,
        ast.Gt, ast.GtE
    )

    if not isinstance(node, SAFE_NODES):
        return False

    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name) or node.func.id not in SAFE_NAMES:
            return False

    if isinstance(node, ast.BinOp) and not isinstance(node.op, SAFE_OPS):
        return False
    if isinstance(node, ast.UnaryOp) and not isinstance(node.op, SAFE_OPS):
        return False
    if isinstance(node, ast.BoolOp) and not isinstance(node.op, SAFE_OPS):
        return False
    if isinstance(node, ast.Compare) and not all(isinstance(op, SAFE_OPS) for op in node.ops):
        return False

    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def process_user_expression(query_expr: str) -> str:
    """
    Safely evaluate a user supplied Python expression and return its
    string representation. If the expression is unsafe or evaluation
    fails, 'Error!' is returned.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(query_expr, mode='eval')

        # Verify that the expression is safe
        if not _is_safe_node(parsed):
            return 'Error!'

        # Restrict the globals and locals available to eval
        safe_globals = {
            '__builtins__': None,
            'abs': abs,
            'round': round,
            'min': min,
            'max': max,
            'len': len,
        }

        # Evaluate the expression
        result: Any = eval(compile(parsed, filename="<ast>", mode="eval"),
                          safe_globals, {})
        return str(result)
    except Exception:
        # Any error (parsing or runtime) results in a generic error message
        return 'Error!'