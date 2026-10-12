import ast

# List of disallowed AST node types
DISALLOWED_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Exec,  # exec is removed in Python3 but keep for completeness
    ast.Global,
    ast.Nonlocal,
    ast.With,  # can be used to open files
    ast.Call,  # restrict calls to builtins only
)

# Allowed builtins – a very small subset
SAFE_BUILTINS = {
    "abs": abs,
    "all": all,
    "any": any,
    "bool": bool,
    "chr": chr,
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
    "str": str,
    "sum": sum,
    "tuple": tuple,
}

def _validate_ast(node: ast.AST):
    """
    Recursively validate the AST to ensure no disallowed nodes are present.
    Raises ValueError if a prohibited construct is found.
    """
    for child in ast.iter_child_nodes(node):
        # Reject any disallowed node
        if isinstance(child, DISALLOWED_NODES):
            raise ValueError(f"Disallowed operation: {type(child).__name__}")

        # Reject function or lambda definitions
        if isinstance(child, (ast.FunctionDef, ast.Lambda)):
            raise ValueError("Function or lambda definitions are not allowed.")

        # Reject attribute access (e.g., os.system)
        if isinstance(child, ast.Attribute):
            raise ValueError("Attribute access is not allowed.")

        # Reject calls to functions other than those in SAFE_BUILTINS
        if isinstance(child, ast.Call):
            # Only allow calls to names that are in SAFE_BUILTINS
            if isinstance(child.func, ast.Name):
                if child.func.id not in SAFE_BUILTINS:
                    raise ValueError(f"Call to untrusted function '{child.func.id}' is not allowed.")
            else:
                raise ValueError("Only simple function calls are allowed.")

        # Recurse into children
        _validate_ast(child)

def safe_run_script(script_code: str):
    """
    Execute a user-provided Python script in a restricted environment.

    Parameters
    ----------
    script_code : str
        The Python code submitted by the user.

    Returns
    -------
    result : Any or None
        The value of the last expression in the script, if any.
        Otherwise returns None.

    Raises
    ------
    ValueError
        If the script contains prohibited operations or invalid syntax.
    """
    # Parse the code to an AST and validate it
    try:
        parsed = ast.parse(script_code, mode="exec")
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    _validate_ast(parsed)

    # Prepare a restricted execution environment
    exec_globals = {"__builtins__": SAFE_BUILTINS}
    exec_locals = {}

    # Compile the code
    compiled = compile(parsed, filename="<user_script>", mode="exec")

    # Execute the script
    try:
        exec(compiled, exec_globals, exec_locals)
    except Exception as e:
        # Re-raise as ValueError to match the contract
        raise ValueError(f"Execution error: {e}") from None

    # If the last statement is an expression, return its value
    if parsed.body and isinstance(parsed.body[-1], ast.Expr):
        # Evaluate the expression in the same restricted environment
        expr_code = compile(ast.Expression(parsed.body[-1].value), filename="<user_script>", mode="eval")
        try:
            return eval(expr_code, exec_globals, exec_locals)
        except Exception as e:
            raise ValueError(f"Evaluation error: {e}") from None

    return None