import ast
import io
import sys

# Allowed AST node types for a safe subset of Python
SAFE_NODES = {
    ast.Module,
    ast.Expr,
    ast.Constant,
    ast.Str,           # for older Python versions
    ast.Num,
    ast.Name,
    ast.Load,
    ast.Call,
    ast.BinOp,
    ast.UnaryOp,
    ast.operator,
    ast.unaryop,
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow,
    ast.UAdd, ast.USub,
    ast.keyword,
}

# Names that are considered safe to use
SAFE_NAMES = {
    'print',
    # add other allowed builtins if needed
}

def _is_safe_node(node):
    """Recursively check that all nodes are in the allowed set."""
    if type(node) not in SAFE_NODES:
        return False
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    # For Call nodes, ensure the function name is safe
    if isinstance(node, ast.Call):
        # Function must be a Name and in SAFE_NAMES
        func = node.func
        if isinstance(func, ast.Name):
            if func.id not in SAFE_NAMES:
                return False
        else:
            # disallow attribute access, lambda, etc.
            return False
    return True

def execute_user_code(script_to_execute: str):
    """
    Execute a user-provided Python script in a restricted environment.

    Parameters
    ----------
    script_to_execute : str
        The Python code to execute.

    Returns
    -------
    str or None
        Captured output from `print` statements, or None if nothing was printed.

    Raises
    ------
    ValueError
        If the script contains prohibited actions or has syntax errors.
    """
    # Parse and validate syntax
    try:
        parsed = ast.parse(script_to_execute, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user script: {exc}") from None

    # Ensure the AST only contains safe nodes
    if not _is_safe_node(parsed):
        raise ValueError("User script contains disallowed operations.")

    # Prepare a restricted globals dict
    safe_globals = {
        '__builtins__': {'print': print},
    }

    # Capture stdout
    old_stdout = sys.stdout
    fake_out = io.StringIO()
    try:
        sys.stdout = fake_out
        exec(compile(parsed, filename='<user_script>', mode='exec'), safe_globals)
    except Exception as exc:
        raise ValueError(f"Error during script execution: {exc}") from None
    finally:
        sys.stdout = old_stdout

    output = fake_out.getvalue()
    return output if output else None