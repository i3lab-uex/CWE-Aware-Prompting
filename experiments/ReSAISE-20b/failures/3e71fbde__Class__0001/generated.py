import ast
import builtins
import io
import sys

# A minimal whitelist of safe builtin functions/objects that may be used.
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
    'str': str,
    'sum': sum,
}

# Allowed AST node types
ALLOWED_NODES = {
    ast.Module, ast.Expr, ast.Assign, ast.AugAssign,
    ast.Name, ast.Load, ast.Store, ast.Del,
    ast.Constant, ast.Num, ast.Str,  # for Python <3.8
    ast.BinOp, ast.UnaryOp, ast.BoolOp,
    ast.Compare, ast.IfExp,
    ast.operator, ast.unaryop, ast.boolop, ast.cmpop,
    ast.Call,
    ast.Attribute,
}

# Disallowed node types
DISALLOWED_NODES = {
    ast.Import, ast.ImportFrom,
    ast.Exec,  # not present in modern AST but kept for clarity
    ast.Lambda,
    ast.FunctionDef, ast.AsyncFunctionDef,
    ast.ClassDef,
    ast.Global, ast.Nonlocal,
    ast.With, ast.AsyncWith,
    ast.For, ast.While, ast.Return,
    ast.Try, ast.ExceptHandler,
}

def _validate_ast(node):
    """
    Recursively walk the AST and ensure only allowed nodes are present.
    Raise ValueError if a disallowed node is found or an attribute
    access that could reach unsafe objects.
    """
    if type(node) in DISALLOWED_NODES:
        raise ValueError(f"Disallowed construct: {type(node).__name__}")

    if not isinstance(node, tuple(ALLOWED_NODES)):
        raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # For attribute accesses, ensure the base is a safe builtin
    if isinstance(node, ast.Attribute):
        # e.g., math.sqrt -> disallowed because math not in SAFE_BUILTINS
        if isinstance(node.value, ast.Name):
            if node.value.id not in SAFE_BUILTINS:
                raise ValueError(f"Disallowed attribute access: {node.value.id}")
        else:
            # nested attributes are disallowed
            raise ValueError(f"Complex attribute access not allowed: {ast.dump(node)}")

    for child in ast.iter_child_nodes(node):
        _validate_ast(child)

def run_code_snippet(snippet: str) -> None | str:
    """
    Execute a small Python code snippet safely.

    Parameters
    ----------
    snippet : str
        The Python code to run. Must not contain disallowed constructs.

    Returns
    -------
    None or str
        If the snippet produces output via print, that output is returned as a string.
        If no output is produced, None is returned.

    Raises
    ------
    ValueError
        If the snippet contains disallowed operations or unsafe constructs.
    """
    # Parse the code into an AST
    try:
        parsed = ast.parse(snippet, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in snippet: {e}") from None

    # Validate the AST
    _validate_ast(parsed)

    # Prepare a restricted globals dict containing only SAFE_BUILTINS
    safe_globals = {"__builtins__": SAFE_BUILTINS}
    # Allow locals to be empty; no variables can be created that escape this scope
    safe_locals = {}

    # Capture stdout
    old_stdout = sys.stdout
    buffer = io.StringIO()
    try:
        sys.stdout = buffer
        exec(compile(parsed, filename="<snippet>", mode="exec"), safe_globals, safe_locals)
    finally:
        sys.stdout = old_stdout

    output = buffer.getvalue()
    return output if output else None