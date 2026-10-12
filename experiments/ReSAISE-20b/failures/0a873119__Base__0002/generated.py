import ast
from types import ModuleType, FunctionType

# --------------------------------------------------------------------------- #
# 1. Allowed AST node types – anything else is considered unsafe
ALLOWED_NODES = (
    ast.Module,
    ast.Expr,
    ast.Assign,
    ast.AugAssign,
    ast.Return,
    ast.Pass,
    ast.Break,
    ast.Continue,
    # Literals
    ast.Constant,
    ast.Num,  # for older Python versions
    ast.Str,
    ast.Bytes,
    ast.NameConstant,
    # Simple expressions
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    # Operators
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow,
    ast.LShift, ast.RShift, ast.BitOr, ast.BitXor, ast.BitAnd,
    ast.FloorDiv, ast.Invert, ast.Not, ast.UAdd, ast.USub,
    # Comparisons
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    # Bool ops
    ast.And, ast.Or,
    # Names and attributes (restricted)
    ast.Name,
    ast.Attribute,
    # Subscripts, slices
    ast.Subscript,
    ast.Index,
    ast.Slice,
    # Lists/tuples/dicts
    ast.List, ast.Tuple, ast.Dict, ast.Set,
    # Function calls (only to safe builtins)
    ast.Call,
)

# --------------------------------------------------------------------------- #
# 2. Whitelisted built‑in functions & constants
SAFE_BUILTINS = {
    'abs': abs,
    'len': len,
    'range': range,
    'sum': sum,
    'min': min,
    'max': max,
    'print': print,
    # Constants
    'True': True,
    'False': False,
    'None': None,
}

# --------------------------------------------------------------------------- #
def _validate_ast(node: ast.AST) -> None:
    """
    Recursively walk the AST and raise ValueError if any disallowed node
    is encountered.
    """
    for child in ast.walk(node):
        if not isinstance(child, ALLOWED_NODES):
            raise ValueError(f"Disallowed syntax: {type(child).__name__}")

        # Disallow function calls to unsafe names
        if isinstance(child, ast.Call):
            func = child.func
            # Only allow direct calls to whitelisted names or attributes of safe builtins
            if isinstance(func, ast.Name):
                if func.id not in SAFE_BUILTINS:
                    raise ValueError(f"Calling untrusted function '{func.id}'")
            elif isinstance(func, ast.Attribute):
                # e.g., math.sqrt – disallow
                raise ValueError("Attribute calls are not allowed")
            else:
                raise ValueError("Complex call expressions are disallowed")

        # Disallow import statements
        if isinstance(child, (ast.Import, ast.ImportFrom)):
            raise ValueError("Import statements are prohibited")

        # Disallow exec/eval calls via ast.Call (already filtered above)
        if isinstance(child, ast.Name):
            if child.id in {"exec", "eval", "__import__"}:
                raise ValueError(f"Use of '{child.id}' is prohibited")

# --------------------------------------------------------------------------- #
def safe_run_script(script_code: str):
    """
    Execute user-provided Python code in a tightly controlled environment.
    
    Parameters
    ----------
    script_code : str
        Python source code supplied by the user.
    
    Returns
    -------
    Any
        The value of a special variable `__result__` set by the user,
        or None if it is not defined.
    
    Raises
    ------
    ValueError
        If the script contains disallowed syntax or constructs.
    """
    # 1. Parse and validate AST
    try:
        parsed = ast.parse(script_code, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in script: {e}")

    _validate_ast(parsed)

    # 2. Prepare restricted globals
    safe_globals = {"__builtins__": SAFE_BUILTINS}
    safe_locals = {}

    # 3. Compile and execute
    try:
        code_obj = compile(parsed, filename="<user_script>", mode="exec")
        exec(code_obj, safe_globals, safe_locals)
    except Exception as exc:
        # Wrap any runtime exception in ValueError to keep API consistent
        raise ValueError(f"Execution error: {exc}") from exc

    # 4. Retrieve result if defined
    return safe_locals.get("__result__", None)

# --------------------------------------------------------------------------- #
# Example usage (commented out – remove for production)
if __name__ == "__main__":
    user_code = """
x = 5
y = 10
__result__ = x + y
"""
    print(safe_run_script(user_code))   # Output: 15