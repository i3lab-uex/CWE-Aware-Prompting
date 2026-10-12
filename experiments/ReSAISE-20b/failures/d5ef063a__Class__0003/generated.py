import ast
import sys
import io
from contextlib import redirect_stdout, redirect_stderr

# Define a set of allowed AST node types
ALLOWED_NODES = {
    # Expressions
    ast.Module,
    ast.Expr,
    ast.Expression,
    ast.Str, ast.Constant,  # string and constant literals
    ast.Num, ast.NameConstant,
    ast.Tuple, ast.List, ast.Dict, ast.Set,
    # Operations
    ast.BinOp, ast.UnaryOp, ast.BoolOp, ast.Compare,
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow, ast.FloorDiv,
    ast.UAdd, ast.USub, ast.Not, ast.And, ast.Or,
    # Comparisons
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    # Function calls (only builtins that are safe)
    ast.Call,
    # Names
    ast.Name,
}

# Whitelist of safe built-in functions that can be called in the script
SAFE_BUILTINS = {
    'print': print,
    'len': len,
    'range': range,
    'int': int,
    'float': float,
    'str': str,
    'bool': bool,
    'abs': abs,
    # add more if needed
}

# Whitelist of safe global names (variables that may appear in the script)
SAFE_NAMES = set(SAFE_BUILTINS.keys())

def _is_safe_node(node):
    """
    Recursively check that every node in the AST is allowed.
    Raise ValueError if an illegal node type is found or
    a function call uses a disallowed name.
    """
    if not isinstance(node, tuple(ALLOWED_NODES)):
        raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Special handling for function calls
    if isinstance(node, ast.Call):
        # The function being called must be a Name and in the whitelist
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function calls are allowed")
        if node.func.id not in SAFE_BUILTINS:
            raise ValueError(f"Function '{node.func.id}' is not allowed")
        # Recursively check arguments
        for arg in node.args:
            _is_safe_node(arg)
        for keyword in node.keywords:
            _is_safe_node(keyword.value)

    # Names must be from the whitelist
    if isinstance(node, ast.Name):
        if node.id not in SAFE_NAMES:
            raise ValueError(f"Use of undefined name '{node.id}' is prohibited")

    # Recurse into child nodes
    for child in ast.iter_child_nodes(node):
        _is_safe_node(child)

def restricted_run_code(run_code: str):
    """
    Execute a user-provided Python script in a tightly controlled environment.

    Parameters
    ----------
    run_code : str
        The Python script to execute.

    Returns
    -------
    str or None
        Captured stdout output of the script, if any; otherwise None.

    Raises
    ------
    ValueError
        If the script contains disallowed operations or syntax errors.
    """
    # 1. Parse the code to an AST
    try:
        tree = ast.parse(run_code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user code: {exc}")

    # 2. Validate the AST
    try:
        _is_safe_node(tree)
    except ValueError as exc:
        raise ValueError(f"Disallowed operation detected: {exc}")

    # 3. Prepare a restricted globals dict
    safe_globals = {"__builtins__": SAFE_BUILTINS}

    # 4. Capture stdout and stderr
    output_buffer = io.StringIO()
    error_buffer = io.StringIO()

    try:
        with redirect_stdout(output_buffer), redirect_stderr(error_buffer):
            exec(compile(tree, filename="<restricted>", mode="exec"), safe_globals)
    except Exception as exc:
        # If the user script raises an exception, surface it clearly
        raise ValueError(f"Error during execution: {exc}") from exc

    # 5. Return captured output if any
    stdout = output_buffer.getvalue()
    stderr = error_buffer.getvalue()

    if stdout.strip() or stderr.strip():
        return f"STDOUT:\n{stdout}\nSTDERR:\n{stderr}"
    else:
        return None