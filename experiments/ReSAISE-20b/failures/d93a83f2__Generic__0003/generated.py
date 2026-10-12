import ast

def safe_execute_code(snippet: str):
    """
    Execute a user-provided Python code snippet in a restricted environment.

    Only literal expressions, simple arithmetic and comparison operations are allowed.
    No imports, function definitions, assignments, or calls to built‑ins (except
    a few whitelisted ones such as `len`, `sum`, `abs`) are permitted.

    Parameters
    ----------
    snippet : str
        The Python code to be executed.

    Returns
    -------
    Any
        Result of the evaluated expression, or None if no result.

    Raises
    ------
    ValueError
        If the snippet contains disallowed syntax or operations.
    """

    # Whitelisted builtins that can be safely used
    SAFE_BUILTINS = {
        'len': len,
        'sum': sum,
        'abs': abs,
        'min': min,
        'max': max,
    }

    # Allowed AST node types
    ALLOWED_NODES = {
        ast.Module, ast.Expr, ast.Expression,
        ast.Num, ast.Constant,  # numeric literals
        ast.Str, ast.Bytes,
        ast.Tuple, ast.List, ast.Set, ast.Dict,
        ast.BinOp, ast.UnaryOp, ast.BoolOp, ast.Compare,
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow,
        ast.FloorDiv, ast.LShift, ast.RShift, ast.BitOr,
        ast.BitAnd, ast.BitXor, ast.Invert, ast.Not,
        ast.UAdd, ast.USub,
        ast.And, ast.Or, ast.Eq, ast.NotEq,
        ast.Lt, ast.LtE, ast.Gt, ast.GtE,
        ast.Is, ast.IsNot, ast.In, ast.NotIn,
        ast.NameConstant,
        ast.Name,
    }

    # Parse the snippet into an AST
    try:
        parsed = ast.parse(snippet, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}")

    # Recursively walk the AST to ensure only allowed nodes are present
    for node in ast.walk(parsed):
        if type(node) not in ALLOWED_NODES:
            raise ValueError(f"Disallowed syntax: {type(node).__name__}")
        if isinstance(node, ast.Name):
            # Only allow names that refer to whitelisted builtins
            if node.id not in SAFE_BUILTINS:
                raise ValueError(f"Use of unknown identifier '{node.id}' is not allowed")

    # Evaluate the expression in a sandboxed environment
    try:
        result = eval(compile(parsed, filename="<safe>", mode="eval"),
                      {"__builtins__": None}, SAFE_BUILTINS)
    except Exception as exc:
        # Any runtime error is treated as a failure of the safe execution
        raise ValueError(f"Execution failed: {exc}") from exc

    return result