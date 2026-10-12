import ast
import sys
import io
from types import ModuleType

# Whitelist of allowed AST node types
ALLOWED_NODES = {
    ast.Module,
    ast.Expr,
    ast.ImportFrom,
    ast.Import,
    ast.Name,
    ast.Load,
    ast.Store,
    ast.Call,
    ast.Constant,
    ast.Num,          # for Python <3.8
    ast.Str,          # for Python <3.8
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.IfExp,
    ast.Attribute,
    ast.Subscript,
    ast.Index,        # for Python <3.9
    ast.Slice,
    ast.keyword,
}

# Whitelist of safe builtins
SAFE_BUILTINS = {
    'abs', 'all', 'any', 'bool', 'bytes',
    'chr', 'dict', 'float', 'int', 'len',
    'list', 'max', 'min', 'pow', 'range',
    'round', 'str', 'tuple', 'sum'
}

# Additional safe functions or modules that may be required
SAFE_MODULES = {
    'math': __import__('math')
}

def _is_safe_node(node: ast.AST) -> bool:
    """Recursively verify that a node and its children are allowed."""
    if type(node) not in ALLOWED_NODES:
        return False
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def process_user_code(code_submission: str):
    """
    Safely execute a user-provided Python script.

    Parameters
    ----------
    code_submission : str
        The script to execute.

    Returns
    -------
    Any
        Output captured from the script, or None if no output.

    Raises
    ------
    ValueError
        If the script contains forbidden actions or syntax errors.
    """
    # Parse and validate syntax
    try:
        parsed = ast.parse(code_submission, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user script: {exc}") from None

    # Validate all nodes
    if not _is_safe_node(parsed):
        raise ValueError("User script contains disallowed operations.")

    # Prepare restricted globals
    safe_globals = {
        '__builtins__': {k: __builtins__[k] for k in SAFE_BUILTINS if k in __builtins__}
    }
    safe_globals.update(SAFE_MODULES)

    # Capture stdout
    old_stdout = sys.stdout
    buffer = io.StringIO()
    try:
        sys.stdout = buffer
        exec(compile(parsed, filename="<user>", mode="exec"), safe_globals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from None
    finally:
        sys.stdout = old_stdout

    output = buffer.getvalue()
    return output if output else None