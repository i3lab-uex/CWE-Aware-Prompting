import ast

# List of AST node types that are considered safe.
SAFE_NODES = {
    # Root nodes
    ast.Module,
    ast.Expression,
    # Statements
    ast.Expr,
    ast.Assign,
    # Expressions
    ast.Constant,
    ast.Name,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    # Operators
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
    ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr,
    ast.BitAnd, ast.BitXor, ast.Invert, ast.Not,
    ast.UAdd, ast.USub,
    # Comparisons
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    # Boolean ops
    ast.And, ast.Or,
}

# Disallowed nodes (any node not in SAFE_NODES is prohibited)
def _is_safe(node):
    if type(node) not in SAFE_NODES:
        return False
    for child in ast.iter_child_nodes(node):
        if not _is_safe(child):
            return False
    return True

def run_code_snippet(user_code: str):
    """
    Execute a user supplied code snippet in a highly restricted environment.

    The function allows only a very small subset of Python syntax:
        - arithmetic, boolean and comparison expressions
        - variable assignment to simple names
    Any other construct (imports, function definitions, attribute access,
    calls, etc.) will raise a ValueError.

    Parameters
    ----------
    user_code : str
        The Python code snippet to execute.

    Returns
    -------
    Any
        The value of the last expression in the snippet, or None if no
        expression produces a result.

    Raises
    ------
    ValueError
        If the snippet contains disallowed syntax or semantics.
    """
    try:
        # Parse into an AST
        parsed = ast.parse(user_code, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python syntax: {exc}") from None

    # Ensure the AST contains only safe nodes
    if not _is_safe(parsed):
        raise ValueError("Disallowed code detected in snippet")

    # Prepare a restricted execution environment
    safe_globals = {"__builtins__": {}}
    safe_locals = {}

    # Compile the AST
    code_obj = compile(parsed, filename="<user_code>", mode="exec")

    # Execute and capture the result of the last expression if any
    exec_result = None
    try:
        # We execute line by line to capture the value of the last expression.
        for node in parsed.body:
            if isinstance(node, ast.Expr):
                # Evaluate the expression and store its value
                exec_result = eval(compile(ast.Expression(node.value), filename="<expr>", mode="eval"),
                                   safe_globals, safe_locals)
            else:
                # For assignments and other statements, just execute
                exec(compile(ast.Module([node], type_ignores=[]), filename="<stmt>", mode="exec"),
                     safe_globals, safe_locals)
    except Exception as exc:
        # Re‑raise any runtime errors as ValueError to keep the API simple
        raise ValueError(f"Runtime error in snippet: {exc}") from None

    return exec_result