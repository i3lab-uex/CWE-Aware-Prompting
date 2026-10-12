import ast
import io
import sys

# List of AST node types that are considered safe for user scripts.
SAFE_NODE_TYPES = {
    ast.Module,
    ast.Expr,
    ast.Assign,
    ast.Name,
    ast.Constant,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.IfExp,
    ast.Call,
    ast.Load,
    ast.Store,
    ast.operator,
    ast.unaryop,
    ast.boolop,
    ast.cmpop,
}

# Only the following built-in functions are allowed.
SAFE_BUILTINS = {
    'print': print,
}

# Disallowed function names (for example, open, exec).
DISALLOWED_CALLS = {'open', 'exec', 'eval', '__import__'}

def _is_safe_ast(node: ast.AST) -> bool:
    """
    Recursively check that the node and all its children are of safe types.
    Also checks that function calls are to allowed functions only.
    """
    if type(node) not in SAFE_NODE_TYPES:
        return False

    # Special handling for Call nodes
    if isinstance(node, ast.Call):
        # The function being called must be a Name and in SAFE_BUILTINS
        if not isinstance(node.func, ast.Name):
            return False
        if node.func.id not in SAFE_BUILTINS:
            return False

    for child in ast.iter_child_nodes(node):
        if not _is_safe_ast(child):
            return False

    return True


def execute_user_code(script_to_execute: str) -> str | None:
    """
    Execute a user supplied Python script in a restricted environment.

    Parameters
    ----------
    script_to_execute : str
        The Python source code to execute.

    Returns
    -------
    str | None
        Captured output from the script if any, otherwise None.

    Raises
    ------
    ValueError
        If the script contains syntax errors or attempts to perform disallowed actions.
    """
    # Parse the source into an AST and check for syntax errors
    try:
        parsed = ast.parse(script_to_execute, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user script: {exc}") from exc

    # Validate the AST for safety
    if not _is_safe_ast(parsed):
        raise ValueError("User script contains disallowed operations")

    # Prepare a restricted globals dictionary
    safe_globals = {"__builtins__": SAFE_BUILTINS}

    # Capture stdout
    old_stdout = sys.stdout
    output_capture = io.StringIO()
    try:
        sys.stdout = output_capture
        exec(compile(parsed, filename="<user_script>", mode="exec"), safe_globals)
    except Exception as exc:
        raise ValueError(f"Error during script execution: {exc}") from exc
    finally:
        sys.stdout = old_stdout

    output = output_capture.getvalue()
    return output if output else None