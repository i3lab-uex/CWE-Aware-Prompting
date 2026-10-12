import ast
import io
import sys

# --------------------------------------------------------------------------- #
# Safe execution environment
# --------------------------------------------------------------------------- #

# Whitelisted built‑in functions that the user code is allowed to call.
ALLOWED_BUILTINS = {
    "print": print,
    "len": len,
    "range": range,
    "sum": sum,
    "min": min,
    "max": max,
    "abs": abs,
    # Add more safe functions here if needed
}

# Whitelisted AST node types. Anything outside this list will raise an error.
ALLOWED_AST_NODES = (
    ast.Module,
    ast.Expr,
    ast.Load,
    ast.Call,
    ast.Name,
    ast.Constant,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.IfExp,
    ast.Attribute,
    # Operators
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
    ast.Mod, ast.Pow,
    ast.UAdd, ast.USub,
    ast.And, ast.Or,
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    # Other simple constructs
    ast.List, ast.Tuple, ast.Dict, ast.Set,
)

def _check_ast(node: ast.AST) -> None:
    """
    Recursively walk the AST and ensure that every node is allowed.
    Raises ValueError if a forbidden node or name is found.
    """
    if not isinstance(node, ALLOWED_AST_NODES):
        raise ValueError(f"Forbidden AST node: {type(node).__name__}")

    # Special check for function calls – only allow whitelisted names
    if isinstance(node, ast.Call):
        # The callee must be a Name and in ALLOWED_BUILTINS
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name not in ALLOWED_BUILTINS:
                raise ValueError(f"Call to unallowed function: {func_name}")
        else:
            # Disallow attribute calls (e.g., os.system)
            raise ValueError("Only simple function names are allowed in calls")

    for child in ast.iter_child_nodes(node):
        _check_ast(child)

def evaluate_user_input(user_code: str) -> str | None:
    """
    Safely execute a user supplied Python script.

    Parameters
    ----------
    user_code : str
        The code snippet submitted by the user.

    Returns
    -------
    str | None
        Captured stdout from the execution, or None if nothing was printed.

    Raises
    ------
    ValueError
        If the script contains syntax errors or disallowed operations.
    """
    # Parse code to an AST and validate it
    try:
        parsed = ast.parse(user_code, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user code: {exc}") from None

    _check_ast(parsed)

    # Prepare a restricted global namespace
    safe_globals = {"__builtins__": ALLOWED_BUILTINS}

    # Capture printed output
    old_stdout = sys.stdout
    captured = io.StringIO()
    try:
        sys.stdout = captured
        exec(compile(parsed, filename="<user_code>", mode="exec"), safe_globals)
    finally:
        sys.stdout = old_stdout

    output = captured.getvalue()
    return output if output else None