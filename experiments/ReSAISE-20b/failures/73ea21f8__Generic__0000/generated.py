import ast
from typing import Any, Optional

# --------------------------------------------------------------------------- #
# Allowed AST node types (safe subset)
ALLOWED_NODES = {
    ast.Module,
    ast.Expr,
    ast.Expression,
    ast.Constant,          # literals: numbers, strings, bools, None
    ast.Num,               # Python <3.8 compatibility
    ast.Str,
    ast.Bytes,
    ast.NameConstant,      # Python <3.8
    ast.Tuple,
    ast.List,
    ast.Set,
    ast.Dict,
    ast.Name,              # variable names
    ast.Load,
    ast.Store,
    ast.UnaryOp,
    ast.BinOp,
    ast.BoolOp,
    ast.Compare,
    ast.Call,              # allow limited calls (e.g., len, range)
    ast.Attribute,
    ast.Subscript,
    # Operators
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
    ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr,
    ast.BitXor, ast.BitAnd, ast.UAdd, ast.USub,
    # Comparisons
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    # Boolean ops
    ast.And, ast.Or, ast.Not,
}

# Whitelist of safe built-in functions that may be called
SAFE_BUILTINS = {
    'len': len,
    'range': range,
    'abs': abs,
    'min': min,
    'max': max,
    'sum': sum,
    # Add more if desired
}

# --------------------------------------------------------------------------- #
def _is_safe(node: ast.AST) -> bool:
    """
    Recursively check that all nodes in the AST are part of the allowed set
    and that calls are only to whitelisted builtins.
    """
    if type(node) not in ALLOWED_NODES:
        return False

    # Special handling for function calls
    if isinstance(node, ast.Call):
        # Only allow calls to names that are in SAFE_BUILTINS
        if isinstance(node.func, ast.Name):
            if node.func.id not in SAFE_BUILTINS:
                return False
        else:
            # disallow attribute calls or complex expressions
            return False

    for child in ast.iter_child_nodes(node):
        if not _is_safe(child):
            return False
    return True

# --------------------------------------------------------------------------- #
def run_code_snippet(user_code: str) -> Optional[Any]:
    """
    Execute a user-provided Python code snippet in a sandboxed environment.

    Parameters
    ----------
    user_code : str
        The Python code to execute.  Only a single expression or a very small
        set of safe statements are allowed.

    Returns
    -------
    Optional[Any]
        The result of evaluating the expression if one exists; otherwise None.

    Raises
    ------
    ValueError
        If the snippet contains disallowed syntax or operations.
    """
    # Parse the code into an AST
    try:
        parsed = ast.parse(user_code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user code: {exc}") from exc

    # Verify that the entire tree is safe
    if not _is_safe(parsed):
        raise ValueError("User code contains disallowed operations or syntax")

    # Prepare a restricted execution environment
    safe_globals = {"__builtins__": SAFE_BUILTINS}
    safe_locals: dict[str, Any] = {}

    # If the code is a single expression, evaluate and return its value
    if len(parsed.body) == 1 and isinstance(parsed.body[0], ast.Expr):
        expr_code = compile(ast.Expression(parsed.body[0].value), "<user>", "eval")
        return eval(expr_code, safe_globals, safe_locals)

    # Otherwise, execute the code; capture any final expression result
    exec(compile(parsed, "<user>", "exec"), safe_globals, safe_locals)

    # Attempt to return the value of the last expression if present
    for node in reversed(parsed.body):
        if isinstance(node, ast.Expr):
            expr_code = compile(ast.Expression(node.value), "<user>", "eval")
            return eval(expr_code, safe_globals, safe_locals)

    # No expression to return
    return None