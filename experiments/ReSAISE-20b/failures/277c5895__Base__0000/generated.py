import ast

# Whitelisted AST node types that are considered safe
SAFE_NODES = {
    # Expressions
    ast.Module,
    ast.Expr,
    ast.Expression,

    # Literals and containers
    ast.Constant,  # int, float, str, bool, None
    ast.Num,
    ast.Str,
    ast.Bytes,
    ast.NameConstant,

    # Collections
    ast.List, ast.Tuple, ast.Set, ast.Dict,
    ast.ListComp, ast.GeneratorExp, ast.DictComp, ast.SetComp,

    # Operators
    ast.BinOp, ast.UnaryOp, ast.BoolOp,
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow,
    ast.LShift, ast.RShift, ast.BitOr, ast.BitXor, ast.BitAnd,
    ast.FloorDiv,
    ast.Invert, ast.Not, ast.UAdd, ast.USub,

    # Comparisons
    ast.Compare,
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    ast.Is, ast.IsNot, ast.In, ast.NotIn,

    # Control flow
    ast.IfExp,
    ast.Name,  # variable names (read only)
}

# Names that are allowed to be used in the code (none for strict sandbox)
ALLOWED_NAMES = set()

def _is_safe_node(node: ast.AST) -> bool:
    """Recursively ensure that every node is in the whitelist."""
    if type(node) not in SAFE_NODES:
        return False
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def execute_user_code(submitted_code: str):
    """
    Execute a user‑supplied Python script in a tightly controlled sandbox.
    
    Parameters
    ----------
    submitted_code : str
        The Python code to execute.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If the code contains syntax errors or disallowed operations.
    """
    # 1. Parse the code to an AST, catching syntax errors
    try:
        parsed = ast.parse(submitted_code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # 2. Validate that the AST contains only safe nodes
    if not _is_safe_node(parsed):
        raise ValueError("The script contains prohibited operations.")

    # 3. Prepare a restricted execution environment
    safe_globals = {"__builtins__": {}}
    # Optionally expose a minimal set of builtins
    for name in ALLOWED_NAMES:
        safe_globals[name] = __builtins__[name]

    # 4. Compile and execute the code
    try:
        compiled = compile(parsed, filename="<user_code>", mode="exec")
        exec(compiled, safe_globals)
    except Exception as exc:
        # Re‑raise as ValueError to keep API consistent
        raise ValueError(f"Execution error: {exc}") from None

    return None