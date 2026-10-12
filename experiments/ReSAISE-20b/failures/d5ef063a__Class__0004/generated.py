import ast
import sys
from io import StringIO

# Allowed AST node types (whitelist)
ALLOWED_NODES = {
    ast.Module,
    ast.Expr,
    ast.Call,
    ast.Name,
    ast.Load,
    ast.Constant,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # for older Python <3.8
    ast.Str,          # for older Python <3.8
    ast.Tuple,
    ast.List,
    ast.Dict,
    ast.Set,
    ast.Compare,
    ast.BoolOp,
    ast.IfExp,
    ast.Attribute,     # only if the attribute is on a whitelisted object
    ast.Subscript,
    ast.Index,         # for older Python <3.9
    ast.Slice,
}

# Allowed functions that can be called from the user code
ALLOWED_BUILTINS = {
    'print': print,
    'len': len,
    'range': range,
    'int': int,
    'float': float,
    'str': str,
    'bool': bool,
    'list': list,
    'dict': dict,
    'set': set,
    'tuple': tuple,
}

# Objects whose attributes may be accessed
ALLOWED_ATTRIBUTES = {
    # Example: allow math module's sqrt if imported (not allowed here)
}

def _validate_node(node):
    """Recursively validate that a node and its children are allowed."""
    if type(node) not in ALLOWED_NODES:
        raise ValueError(f"Disallowed syntax: {type(node).__name__}")

    # Disallow any Import or ImportFrom nodes
    if isinstance(node, (ast.Import, ast.ImportFrom)):
        raise ValueError("Import statements are not allowed")

    # Disallow attribute access except for whitelisted objects
    if isinstance(node, ast.Attribute):
        if not isinstance(node.value, (ast.Name, ast.Constant)):
            raise ValueError("Complex attribute access is not allowed")
        if node.attr.startswith('_'):
            raise ValueError(f"Access to private attribute '{node.attr}' is disallowed")

    # Disallow any function calls other than whitelisted builtins
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only direct function calls are allowed")
        if node.func.id not in ALLOWED_BUILTINS:
            raise ValueError(f"Call to unapproved function '{node.func.id}'")

    for child in ast.iter_child_nodes(node):
        _validate_node(child)

def restricted_run_code(run_code: str):
    """
    Execute `run_code` in a sandboxed environment that permits only safe operations.
    
    Parameters
    ----------
    run_code : str
        Python script to execute.

    Returns
    -------
    str or None
        Captured stdout output if any; otherwise None.

    Raises
    ------
    ValueError
        If the script contains disallowed syntax or runtime errors.
    """
    # Parse code and validate AST
    try:
        tree = ast.parse(run_code, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in user code: {e}") from None

    try:
        _validate_node(tree)
    except ValueError as e:
        raise ValueError(f"Security violation: {e}") from None

    # Prepare restricted execution environment
    sandbox_globals = {'__builtins__': ALLOWED_BUILTINS}
    sandbox_locals = {}

    # Capture stdout
    old_stdout = sys.stdout
    fake_out = StringIO()
    sys.stdout = fake_out

    try:
        exec(compile(tree, filename="<restricted>", mode="exec"),
             sandbox_globals,
             sandbox_locals)
    except Exception as e:
        raise ValueError(f"Runtime error: {e}") from None
    finally:
        sys.stdout = old_stdout

    output = fake_out.getvalue()
    return output if output else None