import ast

# Whitelist of allowed built‑in functions and constants
SAFE_BUILTINS = {
    "abs": abs,
    "all": all,
    "any": any,
    "bool": bool,
    "dict": dict,
    "float": float,
    "int": int,
    "len": len,
    "list": list,
    "max": max,
    "min": min,
    "pow": pow,
    "range": range,
    "round": round,
    "sum": sum,
    # add more as needed
}

# Set of AST node types that are disallowed
PROHIBITED_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Exec,           # py2
    ast.Call,          # restrict function calls explicitly
    ast.Import,
    ast.ImportFrom,
    ast.Attribute,
    ast.Name,          # for names not in SAFE_BUILTINS
    ast.Global,
    ast.Nonlocal,
    ast.With,          # could be used to open files
    ast.Try,
    ast.ExceptHandler,
    ast.Raise,
    ast.Assert,
}

def _check_ast(node: ast.AST):
    """
    Recursively walk the AST and raise ValueError if a prohibited
    construct is found or an unsafe function call is made.
    """
    for child in ast.iter_child_nodes(node):
        # Disallow any forbidden node type
        if type(child) in PROHIBITED_NODES:
            raise ValueError(f"Prohibited operation: {type(child).__name__}")

        # Disallow function calls that are not in SAFE_BUILTINS
        if isinstance(child, ast.Call):
            # Handle both direct calls and attribute calls
            func = child.func
            if isinstance(func, ast.Name):
                if func.id not in SAFE_BUILTINS:
                    raise ValueError(f"Unauthorized function call: {func.id}")
            else:
                # Attribute calls (e.g., os.system) are disallowed
                raise ValueError("Attribute function calls are not allowed")

        # Disallow any use of the 'open' builtin via attribute or call
        if isinstance(child, ast.Name) and child.id == "open":
            raise ValueError("Usage of 'open' is prohibited")

        _check_ast(child)

def safe_run_script(script_code: str):
    """
    Execute a user supplied Python script in a restricted environment.

    Parameters
    ----------
    script_code : str
        The user supplied Python code to execute.

    Returns
    -------
    Any
        The value of the last expression in the script, or None if no
        expression produces a result.

    Raises
    ------
    ValueError
        If the script contains disallowed syntax or constructs.
    """
    try:
        # Parse the code to an AST for static analysis
        parsed = ast.parse(script_code, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Perform a static safety check
    _check_ast(parsed)

    # Prepare restricted execution environment
    safe_globals = {"__builtins__": SAFE_BUILTINS}
    local_vars = {}

    # Execute the script
    exec(compile(parsed, filename="<user_script>", mode="exec"),
         safe_globals,
         local_vars)

    # Attempt to retrieve the value of the last expression if any
    # (Python's exec doesn't return a result, so we look for
    #   the last expression in the AST and evaluate it)
    if parsed.body:
        last_stmt = parsed.body[-1]
        if isinstance(last_stmt, ast.Expr):
            # Evaluate the expression in the same restricted environment
            expr_code = compile(ast.Expression(last_stmt.value), filename="<user_script>", mode="eval")
            return eval(expr_code, safe_globals, local_vars)

    return None