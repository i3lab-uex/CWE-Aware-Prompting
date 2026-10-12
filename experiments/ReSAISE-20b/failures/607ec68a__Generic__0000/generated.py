import ast
import io
import sys

# ---------- Allowed nodes and names ----------
SAFE_NODES = (
    ast.Module,
    ast.Expr,
    ast.Assign,
    ast.Name,
    ast.Load,
    ast.Store,
    ast.Constant,
    ast.BinOp,
    ast.UnaryOp,
    ast.Compare,
    ast.BoolOp,
    ast.IfExp,
    ast.ListComp,
    ast.DictComp,
    ast.SetComp,
    ast.GeneratorExp,
    ast.Tuple,
    ast.List,
    ast.Dict,
    ast.Set,
    ast.Call,
    ast.Subscript,
    ast.Index,
    ast.Slice,
    ast.Attribute,   # for builtins like math.sqrt
)

# Allowed built-in functions and attributes
SAFE_BUILTINS = {
    'print': print,
    'len': len,
    'range': range,
    'abs': abs,
    'min': min,
    'max': max,
    'sum': sum,
    # You can add more safe builtins here
}

# Allowed modules that can be imported (empty by default)
SAFE_IMPORTS = {
    # 'math': __import__('math'),
}

def _is_safe_node(node):
    """Recursively check if all nodes in the AST are safe."""
    if not isinstance(node, SAFE_NODES):
        return False
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def safe_run_script(code: str):
    """
    Execute a Python script provided as a string in a restricted environment.
    
    Parameters:
        code (str): The user-provided Python script.
    
    Returns:
        str or None: Captured stdout output, or None if nothing was printed.
    
    Raises:
        ValueError: If the script contains prohibited syntax or attempts
                    disallowed operations.
    """
    # Parse and validate AST
    try:
        parsed = ast.parse(code, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in script: {e}") from None

    if not _is_safe_node(parsed):
        raise ValueError("Script contains prohibited or unsafe constructs.")

    # Prepare restricted globals
    restricted_globals = {
        '__builtins__': SAFE_BUILTINS,
        **SAFE_IMPORTS
    }
    
    # Capture stdout
    old_stdout = sys.stdout
    out_buffer = io.StringIO()
    try:
        sys.stdout = out_buffer
        exec(compile(parsed, filename="<user_script>", mode='exec'), restricted_globals)
    except Exception as e:
        raise ValueError(f"Error during script execution: {e}") from None
    finally:
        sys.stdout = old_stdout

    output = out_buffer.getvalue()
    return output if output else None