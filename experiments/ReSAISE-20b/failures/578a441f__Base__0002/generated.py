import ast
from typing import Any, Optional

# Allowed AST node types – only simple expressions and statements
ALLOWED_NODES = {
    ast.Module,
    ast.Expr,
    ast.Load,
    ast.Store,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,
    ast.Constant,          # Python 3.8+
    ast.Name,
    ast.Call,
    ast.keyword,
    ast.Str,
    ast.Bytes,
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.FloorDiv,
    ast.Mod,
    ast.Pow,
    ast.LShift,
    ast.RShift,
    ast.BitOr,
    ast.BitXor,
    ast.BitAnd,
    ast.UAdd,
    ast.USub,
    ast.Not,
    ast.And,
    ast.Or,
    ast.Eq,
    ast.NotEq,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,
    ast.Is,
    ast.IsNot,
    ast.In,
    ast.NotIn,
}

# Allowed built‑in functions
SAFE_BUILTINS = {
    "abs": abs,
    "min": min,
    "max": max,
    "sum": sum,
    "len": len,
    "range": range,
    "print": print,
}

def _is_allowed(node: ast.AST) -> bool:
    """Recursively check that all nodes are in the allowed set."""
    if type(node) not in ALLOWED_NODES:
        return False
    for child in ast.iter_child_nodes(node):
        if not _is_allowed(child):
            return False
    return True

def run_user_script(user_script: str) -> Optional[Any]:
    """
    Execute a user supplied Python script in a restricted environment.

    Parameters
    ----------
    user_script : str
        The script to execute.

    Returns
    -------
    Optional[Any]
        Result of the last expression in the script, or None if no
        evaluatable expression is present.

    Raises
    ------
    ValueError
        If the script contains disallowed syntax or nodes.
    """
    try:
        # Parse the script to an AST
        parsed = ast.parse(user_script, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user script: {exc}") from None

    # Validate the AST
    if not _is_allowed(parsed):
        raise ValueError("User script contains disallowed operations.")

    # Prepare a safe global namespace
    safe_globals = {"__builtins__": SAFE_BUILTINS}
    # Empty locals to prevent leakage
    safe_locals = {}

    # Execute the script
    exec(compile(parsed, filename="<user_script>", mode="exec"),
         safe_globals, safe_locals)

    # Attempt to evaluate the last expression if present
    for node in reversed(parsed.body):
        if isinstance(node, ast.Expr):
            try:
                # Compile the expression node alone
                expr_code = compile(ast.Expression(body=node.value),
                                    filename="<user_script>", mode="eval")
                return eval(expr_code, safe_globals, safe_locals)
            except Exception:
                # If evaluation fails, ignore and continue
                pass

    return None