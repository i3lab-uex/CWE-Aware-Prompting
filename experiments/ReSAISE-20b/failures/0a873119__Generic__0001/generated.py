import ast

# Allowed built‑in functions for the sandbox
ALLOWED_BUILTINS = {
    'len': len,
    'range': range,
    'sum': sum,
    'min': min,
    'max': max,
    'abs': abs,
    'round': round,
    # Add more safe functions here if needed
}

# Disallowed AST node types (any occurrence will raise an error)
DISALLOWED_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Exec,            # Python 2 only – harmless but kept for clarity
    ast.Call,
    ast.Attribute,       # Prevent attribute access like os.system
    ast.Subscript,       # e.g., open(...)[...]
)

# Disallowed function names that can appear in Call nodes
DISALLOWED_CALLS = {
    'open', 'exec', 'eval', 'compile', 'input',
    'os.system', 'subprocess', 'importlib', '__import__'
}


def _check_syntax_and_security(node: ast.AST) -> None:
    """
    Recursively walk the AST and raise ValueError if any
    disallowed construct is found.
    """
    for child in ast.walk(node):
        # 1. Disallowed node types
        if isinstance(child, DISALLOWED_NODES):
            raise ValueError(f"Disallowed operation: {type(child).__name__}")

        # 2. Disallowed function calls
        if isinstance(child, ast.Call):
            # Resolve the name of the called function
            func_name = None
            if isinstance(child.func, ast.Name):
                func_name = child.func.id
            elif isinstance(child.func, ast.Attribute):
                # Build dotted name e.g., os.system
                parts = []
                attr = child.func
                while isinstance(attr, ast.Attribute):
                    parts.insert(0, attr.attr)
                    attr = attr.value
                if isinstance(attr, ast.Name):
                    parts.insert(0, attr.id)
                func_name = ".".join(parts)

            if func_name and func_name.split('.')[0] in DISALLOWED_CALLS:
                raise ValueError(f"Disallowed function call: {func_name}")

        # 3. Disallow usage of __import__ via Name or Attribute
        if isinstance(child, ast.Name) and child.id == "__import__":
            raise ValueError("Disallowed function call: __import__")


def safe_run_script(script_code: str):
    """
    Execute a user-provided Python script in a restricted environment.

    Parameters
    ----------
    script_code : str
        The Python code submitted by the user.

    Returns
    -------
    result : any or None
        The value of the last expression in the script, if present.
        Otherwise, None.

    Raises
    ------
    ValueError
        If the script contains prohibited operations or invalid syntax.
    """
    # 1. Parse and validate syntax/security
    try:
        parsed = ast.parse(script_code, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}")

    _check_syntax_and_security(parsed)

    # 2. Prepare restricted globals
    sandbox_globals = {"__builtins__": ALLOWED_BUILTINS}

    # 3. Execute the script
    try:
        exec(compile(parsed, filename="<user_script>", mode="exec"), sandbox_globals)
    except Exception as exc:
        # Wrap any runtime error in ValueError to keep API consistent
        raise ValueError(f"Runtime error during script execution: {exc}")

    # 4. Determine the value of the last expression (if any)
    if parsed.body and isinstance(parsed.body[-1], ast.Expr):
        # Evaluate the expression in the sandbox environment
        try:
            expr_value = eval(compile(ast.Expression(parsed.body[-1].value), filename="<expr>", mode="eval"),
                              sandbox_globals)
            return expr_value
        except Exception as exc:
            raise ValueError(f"Failed to evaluate final expression: {exc}")

    return None