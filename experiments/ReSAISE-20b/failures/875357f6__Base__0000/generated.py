import ast
import io
import sys
from types import ModuleType

# Whitelisted AST node types that are considered safe.
ALLOWED_NODES = {
    ast.Module,
    ast.Expr,
    ast.Assign,
    ast.AugAssign,
    ast.Return,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.If,
    ast.For,
    ast.While,
    ast.FunctionDef,
    ast.Return,
    ast.Name,
    ast.Load,
    ast.Store,
    ast.Call,
    ast.Constant,
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
    ast.Index,
    ast.Subscript,
    ast.Attribute,
    # Operators
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow,
    ast.LShift, ast.RShift, ast.BitOr, ast.BitXor, ast.BitAnd,
    ast.FloorDiv, ast.Invert, ast.Not, ast.UAdd, ast.USub,
    # Comparisons
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    ast.Is, ast.IsNot, ast.In, ast.NotIn
}

# Whitelisted names for attributes and builtins.
ALLOWED_NAMES = {
    # Builtins
    'print', 'len', 'range', 'abs', 'min', 'max',
    # Math constants/functions
    'math': ['sqrt', 'sin', 'cos', 'tan', 'pi'],
}

def _is_allowed_name(name: str) -> bool:
    """Check if a name is allowed (builtins or module attributes)."""
    if name in ALLOWED_NAMES:
        return True
    for mod, attrs in ALLOWED_NAMES.items():
        if name.startswith(f"{mod}."):
            attr = name.split(".", 1)[1]
            return attr in attrs
    return False

def _check_node(node: ast.AST):
    """Recursively validate AST nodes."""
    if type(node) not in ALLOWED_NODES:
        raise ValueError(f"Forbidden node: {type(node).__name__}")

    # Check attributes for Call nodes
    if isinstance(node, ast.Call):
        func = node.func
        # Function name can be Name or Attribute
        if isinstance(func, ast.Name):
            if not _is_allowed_name(func.id):
                raise ValueError(f"Forbidden function call: {func.id}")
        elif isinstance(func, ast.Attribute):
            # e.g., math.sqrt
            full_name = f"{func.value.id}.{func.attr}" if isinstance(func.value, ast.Name) else func.attr
            if not _is_allowed_name(full_name):
                raise ValueError(f"Forbidden function call: {full_name}")
        else:
            raise ValueError("Unsupported call target")

    # Recursively check child nodes
    for child in ast.iter_child_nodes(node):
        _check_node(child)

def execute_user_script(submitted_script: str) -> str | None:
    """
    Execute a user-provided Python script in a restricted environment.
    
    Parameters
    ----------
    submitted_script : str
        The Python code to execute.

    Returns
    -------
    str | None
        Captured stdout output if any, otherwise None.

    Raises
    ------
    ValueError
        If the script contains syntax errors or disallowed operations.
    """
    # Parse and validate the AST
    try:
        tree = ast.parse(submitted_script, mode="exec")
    except SyntaxError as e:
        raise ValueError(f"Syntax error in script: {e}") from None

    _check_node(tree)

    # Prepare a restricted globals dictionary
    safe_builtins = {
        'print': print,
        'len': len,
        'range': range,
        'abs': abs,
        'min': min,
        'max': max,
    }
    import math
    safe_builtins['math'] = math

    # Capture stdout
    old_stdout = sys.stdout
    fake_out = io.StringIO()
    sys.stdout = fake_out

    try:
        exec(compile(tree, filename="<user_script>", mode="exec"),
             {"__builtins__": safe_builtins}, {})
    except Exception as e:
        raise ValueError(f"Execution error: {e}") from None
    finally:
        sys.stdout = old_stdout

    output = fake_out.getvalue()
    return output if output else None