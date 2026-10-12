import ast
from typing import Any, Optional

# Allowed AST node types for a safe expression
ALLOWED_NODES = {
    ast.Expression,
    ast.Module,
    ast.Expr,
    ast.Constant,        # literals: int, float, str, bool, None
    ast.Num,             # for Python <3.8 compatibility
    ast.Str,
    ast.Bytes,
    ast.NameConstant,    # for Python <3.8
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
    # Operators
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod,
    ast.Pow, ast.LShift, ast.RShift, ast.BitOr, ast.BitXor, ast.BitAnd,
    ast.UAdd, ast.USub, ast.Not,
    ast.And, ast.Or,
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    # Name (only allowed if it's a constant from the safe namespace)
    ast.Name,
}

# Names that are considered safe (only built‑in constants)
SAFE_NAMES = {
    "True": True,
    "False": False,
    "None": None,
}

def _is_safe_node(node: ast.AST) -> bool:
    """Recursively check that a node and its children are allowed."""
    if type(node) not in ALLOWED_NODES:
        return False
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def run_code_snippet(user_code: str) -> Optional[Any]:
    """
    Execute a user-provided Python code snippet in a restricted environment.
    
    Parameters
    ----------
    user_code : str
        The code snippet to execute.  It must be a single expression containing only
        literals and safe operators.  No statements, imports, function definitions,
        or attribute access are allowed.
    
    Returns
    -------
    Optional[Any]
        The result of evaluating the expression, or None if there is no result.
    
    Raises
    ------
    ValueError
        If the code contains prohibited actions or is not a single expression.
    """
    # Strip surrounding whitespace and ensure we have exactly one line
    stripped = user_code.strip()
    if not stripped:
        return None
    
    # Parse the code; disallow any statements other than an expression
    try:
        parsed = ast.parse(stripped, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python expression: {exc}") from exc
    
    # Verify that the AST contains only allowed nodes
    if not _is_safe_node(parsed):
        raise ValueError("Code contains prohibited operations.")
    
    # Compile the expression in eval mode
    compiled = compile(parsed, "<string>", mode="eval")
    
    # Prepare a minimal globals dict with only safe names
    safe_globals = {"__builtins__": None}
    safe_globals.update(SAFE_NAMES)
    
    # Evaluate the expression safely
    try:
        result = eval(compiled, safe_globals)
    except Exception as exc:
        # Any runtime error is surfaced as a ValueError for consistency
        raise ValueError(f"Execution error: {exc}") from exc
    
    return result