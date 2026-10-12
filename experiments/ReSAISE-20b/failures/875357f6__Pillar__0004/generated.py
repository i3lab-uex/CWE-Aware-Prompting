import ast
import sys
import io
from types import ModuleType

# Define a set of allowed AST node types.  Anything outside this set will
# raise a ValueError during validation.
ALLOWED_NODES = {
    ast.Module, ast.Expr, ast.Load, ast.Store,
    ast.Name, ast.Constant,
    # Control flow
    ast.If, ast.For, ast.While, ast.Break, ast.Continue,
    # Expressions
    ast.BinOp, ast.UnaryOp, ast.BoolOp, ast.Compare,
    # Operators
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow,
    ast.LShift, ast.RShift, ast.BitOr, ast.BitAnd, ast.BitXor,
    ast.FloorDiv, ast.Invert, ast.Not, ast.UAdd, ast.USub,
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    # Function calls (restricted to a safe whitelist)
    ast.Call,
}

# Safe functions that the user is allowed to call.
SAFE_FUNCTIONS = {
    'print': print,
    # Add other safe built-ins as needed
}

def _validate_node(node):
    """Recursively ensure all nodes are in ALLOWED_NODES."""
    if type(node) not in ALLOWED_NODES:
        raise ValueError(f"Forbidden node type: {type(node).__name__}")
    for child in ast.iter_child_nodes(node):
        _validate_node(child)

def execute_user_script(submitted_script: str):
    """
    Safely executes a user supplied Python script.

    Parameters
    ----------
    submitted_script : str
        The user provided script.

    Returns
    -------
    Any
        The value returned by the script if it contains a return statement,
        otherwise None.

    Raises
    ------
    ValueError
        If the script contains syntax errors or disallowed constructs.
    """
    # Parse the script to an AST
    try:
        tree = ast.parse(submitted_script, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in user script: {e}") from None

    # Validate the tree
    _validate_node(tree)

    # Build a minimal execution environment
    safe_globals = {
        '__builtins__': {},  # no built-ins by default
        **SAFE_FUNCTIONS,   # only whitelisted safe functions
    }
    safe_locals = {}

    # Capture stdout if print is used
    old_stdout = sys.stdout
    captured_output = io.StringIO()
    sys.stdout = captured_output

    try:
        exec(compile(tree, filename="<user_script>", mode="exec"), safe_globals, safe_locals)
    except Exception as exc:
        raise ValueError(f"Error during execution: {exc}") from None
    finally:
        sys.stdout = old_stdout

    # Return captured output if anything was printed
    out = captured_output.getvalue()
    return out or None