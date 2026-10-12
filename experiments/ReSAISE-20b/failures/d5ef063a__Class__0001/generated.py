import ast
import sys
import io
from types import FunctionType, ModuleType

# List of safe built-in functions and constants
SAFE_BUILTINS = {
    'abs', 'all', 'any', 'bool', 'chr', 'dict',
    'float', 'int', 'len', 'list', 'max', 'min',
    'pow', 'range', 'str', 'sum', 'tuple',
    # Add any other safe functions you wish to expose
}

# Disallowed node types that could lead to unsafe behavior
DISALLOWED_NODES = (
    ast.Import,            # import statements
    ast.ImportFrom,        # from ... import ...
    ast.Module,            # top-level module node (handled separately)
    ast.Exec,              # exec statement in Python 2
    ast.Call,             # we will filter calls to builtins only
)

# Disallowed names (functions/modules)
DISALLOWED_NAMES = {
    'open', 'eval', 'exec', 'compile',
    '__import__', 'globals', 'locals',
    'vars', 'dir', 'getattr', 'setattr',
    'delattr', 'type', 'repr',
}

def _is_safe_call(node: ast.Call) -> bool:
    """
    Return True if the call is to a safe builtin function.
    """
    # Only allow simple Name calls, not attribute accesses
    if isinstance(node.func, ast.Name):
        return node.func.id in SAFE_BUILTINS
    # Allow calls to builtins via __builtins__? (disallowed)
    return False

def _check_node(node: ast.AST, allowed_names: set):
    """
    Recursively walk the AST and ensure no disallowed nodes or names.
    """
    if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
        raise ValueError("Import statements are not allowed.")
    if isinstance(node, ast.Call) and not _is_safe_call(node):
        raise ValueError(f"Call to disallowed function or attribute: {ast.dump(node)}")
    if isinstance(node, ast.Attribute):
        # Disallow attribute access like os.system
        raise ValueError(f"Attribute access is not allowed: {ast.dump(node)}")
    if isinstance(node, ast.Name):
        # Disallow usage of disallowed names
        if node.id in DISALLOWED_NAMES:
            raise ValueError(f"Use of disallowed name '{node.id}'")
    for child in ast.iter_child_nodes(node):
        _check_node(child, allowed_names)

def restricted_run_code(run_code: str):
    """
    Execute a user supplied Python script in a restricted environment.

    Parameters
    ----------
    run_code : str
        The user supplied Python script to execute.

    Returns
    -------
    output : str or None
        The captured stdout output of the script, if any.

    Raises
    ------
    ValueError
        If the script contains disallowed operations or syntax errors.
    """
    # Parse the code to an AST and perform static checks
    try:
        tree = ast.parse(run_code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user code: {exc}") from exc

    # Perform static analysis
    _check_node(tree, SAFE_BUILTINS)

    # Prepare a restricted global namespace
    safe_globals = {name: __builtins__[name] for name in SAFE_BUILTINS}
    safe_globals['__builtins__'] = safe_globals  # Ensure __builtins__ is restricted

    # Capture stdout
    old_stdout = sys.stdout
    fake_out = io.StringIO()
    try:
        sys.stdout = fake_out
        # Execute the code in a new module namespace to avoid leakage
        exec(compile(tree, filename="<restricted>", mode="exec"), safe_globals)
    except Exception as exc:
        raise ValueError(f"Runtime error in user code: {exc}") from exc
    finally:
        sys.stdout = old_stdout

    output = fake_out.getvalue()
    return output if output else None