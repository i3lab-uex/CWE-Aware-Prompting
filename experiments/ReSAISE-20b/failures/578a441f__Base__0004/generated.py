import ast
from types import SimpleNamespace

# Whitelist of safe built‑in functions and constants
SAFE_BUILTINS = {
    'abs': abs,
    'len': len,
    'range': range,
    'min': min,
    'max': max,
    'sum': sum,
    'sorted': sorted,
    'int': int,
    'float': float,
    'str': str,
    'bool': bool,
    'dict': dict,
    'list': list,
    'tuple': tuple,
    'set': set,
}

# Allowed AST node types
ALLOWED_NODES = {
    ast.Module, ast.Expr, ast.Assign,
    ast.Name, ast.Constant,
    ast.BinOp, ast.UnaryOp, ast.BoolOp,
    ast.Compare, ast.IfExp,
    ast.List, ast.Tuple, ast.Set, ast.Dict,
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod,
    ast.Pow, ast.LShift, ast.RShift, ast.BitOr, ast.BitXor,
    ast.FloorDiv, ast.And, ast.Or, ast.Not,
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    # Allow simple attribute access to built‑ins only
    ast.Attribute, 
}

# Disallowed constructs that could lead to code injection or side effects
DISALLOWED_NODES = {
    ast.Import, ast.ImportFrom,
    ast.Call,  # disallow function calls
    ast.Lambda, ast.FunctionDef, ast.AsyncFunctionDef,
    ast.For, ast.While, ast.With, ast.Try,
    ast.Delete, ast.Global, ast.Nonlocal,
    ast.AugAssign, ast.Raise, ast.Assert, ast.Yield,
}

def _is_safe(node: ast.AST) -> bool:
    """
    Recursively check that a node and its children are all allowed.
    """
    if type(node) in DISALLOWED_NODES:
        return False
    if not isinstance(node, tuple(ALLOWED_NODES)):
        # For attribute access we only allow built‑in names
        if isinstance(node, ast.Attribute):
            # e.g., __import__ or os.system are disallowed
            if isinstance(node.value, ast.Name) and node.value.id in SAFE_BUILTINS:
                return True
            else:
                return False
        return False

    for child in ast.iter_child_nodes(node):
        if not _is_safe(child):
            return False
    return True

def run_user_script(user_script: str):
    """
    Execute a user supplied Python script in a highly restricted environment.

    Parameters
    ----------
    user_script : str
        The Python code to run.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If the script contains disallowed operations or invalid syntax.
    """
    try:
        parsed = ast.parse(user_script, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user script: {exc}") from exc

    if not _is_safe(parsed):
        raise ValueError("User script contains disallowed operations")

    # Prepare a restricted global namespace
    safe_globals = {"__builtins__": SAFE_BUILTINS}
    # No local namespace needed
    try:
        exec(compile(parsed, filename="<user_script>", mode="exec"), safe_globals)
    except Exception as exc:
        # Any runtime exception is propagated as ValueError
        raise ValueError(f"Runtime error in user script: {exc}") from exc

    return None