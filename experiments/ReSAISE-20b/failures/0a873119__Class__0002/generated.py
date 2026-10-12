import ast

# A whitelist of safe built‑in functions that we expose to the user script.
SAFE_BUILTINS = {
    'abs': abs,
    'all': all,
    'any': any,
    'bool': bool,
    'dict': dict,
    'float': float,
    'int': int,
    'len': len,
    'list': list,
    'max': max,
    'min': min,
    'pow': pow,
    'range': range,
    'round': round,
    'str': str,
    'sum': sum,
    # Add more if needed
}

# A set of AST node types that are disallowed in the user script.
DISALLOWED_NODES = {
    ast.Import, ast.ImportFrom,          # no imports
    ast.Exec,                             # exec is not an AST node in Py3, but keep for completeness
    ast.Call,                             # we will filter calls to unsafe functions later
    ast.Attribute,                        # attribute access is potentially dangerous (e.g. __import__)
}

# A set of function names that are considered unsafe if called.
UNSAFE_FUNCTIONS = {
    'open', 'eval', 'exec', '__import__',
    # Add more if needed
}

def _is_safe_call(node: ast.Call) -> bool:
    """
    Determine if a function call node is safe.
    Only allow calls to functions that are present in SAFE_BUILTINS and
    do not involve attribute access.
    """
    # The callee must be a simple name (no attributes, subscripts, etc.)
    if not isinstance(node.func, ast.Name):
        return False
    func_name = node.func.id
    if func_name not in SAFE_BUILTINS:
        return False
    # All arguments are allowed (they will be evaluated in the sandbox)
    return True

def _validate_ast(tree: ast.AST) -> None:
    """
    Walk the AST and ensure that no disallowed nodes or unsafe calls appear.
    Raise ValueError if a problem is found.
    """
    for node in ast.walk(tree):
        # Disallow any import statements or attribute access
        if type(node) in DISALLOWED_NODES:
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

        # Specifically check function calls
        if isinstance(node, ast.Call):
            if not _is_safe_call(node):
                raise ValueError(f"Disallowed function call: {ast.unparse(node).strip()}")

        # Disallow any usage of dunder names (e.g., __dict__, __class__)
        if isinstance(node, ast.Attribute):
            # Attribute access is already disallowed above
            pass

        # Disallow assignment to built-in names (e.g., len = 5)
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in SAFE_BUILTINS:
                    raise ValueError(f"Cannot assign to built‑in name: {target.id}")

def safe_run_script(script_code: str):
    """
    Execute a user‑provided Python script in a restricted environment.
    
    Parameters
    ----------
    script_code : str
        The Python source code to execute.

    Returns
    -------
    Any
        The value of the last expression in the script, or None if none.

    Raises
    ------
    ValueError
        If the script contains disallowed syntax or unsafe operations.
    """
    try:
        # Parse the code to an AST; this will raise SyntaxError for invalid syntax.
        tree = ast.parse(script_code, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in script: {e}") from None

    # Validate the AST for safety
    _validate_ast(tree)

    # Prepare a sandboxed globals dictionary.
    sandbox_globals = {'__builtins__': SAFE_BUILTINS}

    # Execute the script. Any exception from the script is propagated.
    exec(compile(tree, filename='<user_script>', mode='exec'), sandbox_globals)

    # If the script defines a variable named "__result__", return it.
    # This is a convention that allows scripts to explicitly expose a result.
    if "__result__" in sandbox_globals:
        return sandbox_globals["__result__"]

    # Otherwise, attempt to evaluate the last expression in the script.
    # We reparse the code in 'eval' mode to get the last expression.
    try:
        expr_tree = ast.parse(script_code, mode='eval')
        return eval(compile(expr_tree, filename='<user_script>', mode='eval'), sandbox_globals)
    except SyntaxError:
        # No expression to evaluate
        return None

# Example usage (for testing purposes; remove or comment out in production):
if __name__ == "__main__":
    test_code = """
x = 10
y = 20
__result__ = x + y
"""
    print(safe_run_script(test_code))  # Should output 30