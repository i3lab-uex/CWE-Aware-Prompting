import ast
import sys
import io

# A list of AST node types that are considered safe.
SAFE_NODES = (
    ast.Module,
    ast.Expr,
    ast.Load,
    ast.Store,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.Call,
    ast.Name,
    ast.Constant,
    ast.Num,          # for Python <3.8
    ast.Str,          # for Python <3.8
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
    ast.NameConstant, # for True/False/None in <3.8
    ast.Subscript,
    ast.Index,
    ast.Slice,
    ast.Attribute,    # only allowed attributes of whitelisted objects
)

# Whitelist of safe builtins that may be used by user code.
SAFE_BUILTINS = {
    'abs': abs,
    'min': min,
    'max': max,
    'sum': sum,
    'len': len,
    'range': range,
    'print': print,  # we capture prints
}

# Whitelisted modules that can be accessed via attribute access.
WHITELISTED_MODULES = {
    'math': __import__('math'),
}

def _is_safe_name(name: str) -> bool:
    """Return True if name is in the allowed builtin or whitelisted modules."""
    return name in SAFE_BUILTINS or name in WHITELISTED_MODULES

def _check_node(node: ast.AST) -> None:
    """Recursively walk the AST and raise ValueError on disallowed nodes."""
    if not isinstance(node, SAFE_NODES):
        raise ValueError(f"Forbidden construct: {type(node).__name__}")

    # Special handling for Call nodes: disallow calling arbitrary functions.
    if isinstance(node, ast.Call):
        # Function being called must be a Name or Attribute of whitelisted object
        func = node.func
        if isinstance(func, ast.Name):
            if not _is_safe_name(func.id):
                raise ValueError(f"Calling disallowed function '{func.id}'")
        elif isinstance(func, ast.Attribute):
            if not (isinstance(func.value, ast.Name) and _is_safe_name(func.value.id)):
                raise ValueError(f"Accessing disallowed attribute on '{func.value.id}'")
        else:
            raise ValueError("Only simple function calls are allowed")

    # Disallow imports entirely
    if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
        raise ValueError("Import statements are not allowed")

    # Disallow attribute access on arbitrary objects except whitelisted modules
    if isinstance(node, ast.Attribute):
        if not (isinstance(node.value, ast.Name) and _is_safe_name(node.value.id)):
            raise ValueError(f"Access to attribute '{node.attr}' of disallowed object")

    # Recurse into child nodes
    for child in ast.iter_child_nodes(node):
        _check_node(child)

def evaluate_user_input(user_code: str):
    """
    Execute a user supplied Python script in a restricted environment.
    
    Parameters
    ----------
    user_code : str
        The code to execute.

    Returns
    -------
    output : str or None
        Captured stdout if any; otherwise None.

    Raises
    ------
    ValueError
        If the code contains disallowed operations or is syntactically invalid.
    """
    # Parse the user code into an AST
    try:
        parsed = ast.parse(user_code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user code: {exc}") from None

    # Validate the AST
    _check_node(parsed)

    # Prepare a restricted globals dictionary
    safe_globals = {
        '__builtins__': SAFE_BUILTINS,
        **WHITELISTED_MODULES
    }

    # Capture stdout
    old_stdout = sys.stdout
    buffer = io.StringIO()
    sys.stdout = buffer

    try:
        exec(compile(parsed, filename="<user_code>", mode="exec"), safe_globals, {})
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from None
    finally:
        sys.stdout = old_stdout

    output = buffer.getvalue()
    return output if output else None