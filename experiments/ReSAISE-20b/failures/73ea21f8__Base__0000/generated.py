import ast
from types import ModuleType, FunctionType

# Define a set of disallowed AST node types and keywords
DISALLOWED_NODES = {
    ast.Import, ast.ImportFrom,  # import statements
    ast.Call,                     # disallow function calls in general (except builtins we allow)
}

DISALLOWED_KEYWORDS = {
    'exec', 'eval', '__import__',
    'open', 'input', 'print'  # disallow user printing
}

# Allowed builtins (very small subset)
ALLOWED_BUILTINS = {
    'abs': abs,
    'min': min,
    'max': max,
    'sum': sum,
    'len': len,
    'range': range,
    # add more safe builtins as needed
}

def _validate_code(user_code: str):
    """
    Validate the AST of the user code. Raise ValueError if any disallowed
    construct is found.
    """
    try:
        tree = ast.parse(user_code, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in code snippet: {e}")

    for node in ast.walk(tree):
        # Disallow import statements
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            raise ValueError("Import statements are not allowed.")
        # Disallow calls to disallowed functions
        if isinstance(node, ast.Call):
            # Allow only builtins we explicitly allow
            if isinstance(node.func, ast.Name):
                func_name = node.func.id
                if func_name not in ALLOWED_BUILTINS:
                    raise ValueError(f"Calling function '{func_name}' is not allowed.")
            else:
                # Any other call (e.g., attribute access) is disallowed
                raise ValueError("Only simple function calls to allowed builtins are permitted.")
        # Disallow usage of prohibited keywords via Name nodes
        if isinstance(node, ast.Name):
            if node.id in DISALLOWED_KEYWORDS:
                raise ValueError(f"Usage of '{node.id}' is prohibited.")

def run_code_snippet(user_code: str):
    """
    Execute a user-provided Python code snippet in a restricted environment.

    Parameters
    ----------
    user_code : str
        The Python code to execute.

    Returns
    -------
    Any
        Result of the executed code if it contains a single expression,
        otherwise None.

    Raises
    ------
    ValueError
        If the code snippet contains prohibited actions.
    """
    # Validate the code before execution
    _validate_code(user_code)

    # Prepare a restricted globals dictionary
    safe_globals = {"__builtins__": ALLOWED_BUILTINS}
    # No local variables should be leaked
    safe_locals = {}

    # Compile the code
    compiled = compile(user_code, '<user_snippet>', 'exec')

    # Execute the code in the restricted environment
    exec(compiled, safe_globals, safe_locals)

    # If the snippet defines a variable named '__result__', return it
    if "__result__" in safe_locals:
        return safe_locals["__result__"]

    # If the snippet is a single expression, eval it
    try:
        expr_tree = ast.parse(user_code, mode='eval')
        return eval(compile(expr_tree, '<user_snippet>', 'eval'), safe_globals, safe_locals)
    except SyntaxError:
        # Not a single expression; nothing to return
        return None

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     code = "x = 5\ny = 10\n__result__ = x + y"
#     print(run_code_snippet(code))   # Output: 15