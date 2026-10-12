import ast
import io
import sys

# Allowed AST node types
ALLOWED_NODES = (
    ast.Module,
    ast.Expr,
    ast.Load,
    ast.Store,
    ast.Name,
    ast.Constant,
    ast.Num,  # for Python <3.8
    ast.Str,  # for Python <3.8
    ast.Tuple,
    ast.List,
    ast.Dict,
    ast.Set,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.IfExp,
    ast.For,
    ast.While,
    ast.Break,
    ast.Continue,
    ast.Pass,
    ast.Return,
    ast.Assign,
    ast.AugAssign,
    ast.While,
    ast.For,
    ast.If,
    ast.With,
    ast.Call,  # but we will restrict calls to a whitelist
)

# Allowed builtins
SAFE_BUILTINS = {
    "print": print,
    "len": len,
    "range": range,
    "int": int,
    "float": float,
    "str": str,
    "bool": bool,
    "list": list,
    "dict": dict,
    "set": set,
    "tuple": tuple,
    "abs": abs,
    "sum": sum,
    # Add more safe functions as needed
}

# Whitelist of allowed function names that can be called in the script
ALLOWED_FUNCTIONS = {"print", "len", "range", "int", "float", "str",
                     "bool", "list", "dict", "set", "tuple", "abs", "sum"}

def _is_allowed_call(node: ast.Call) -> bool:
    """
    Verify that the function being called is in ALLOWED_FUNCTIONS.
    """
    if isinstance(node.func, ast.Name):
        return node.func.id in ALLOWED_FUNCTIONS
    # Disallow attribute calls (e.g., os.system, __import__)
    return False

def _validate_ast(node: ast.AST) -> None:
    """
    Recursively walk the AST and ensure only allowed nodes are present.
    Raise ValueError if a disallowed node is found.
    """
    for child in ast.walk(node):
        if not isinstance(child, ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(child).__name__}")

        if isinstance(child, ast.Call):
            if not _is_allowed_call(child):
                raise ValueError(f"Disallowed function call: {ast.dump(child)}")

        # Disallow import statements
        if isinstance(child, (ast.Import, ast.ImportFrom)):
            raise ValueError("Import statements are not allowed.")

        # Disallow lambda expressions
        if isinstance(child, ast.Lambda):
            raise ValueError("Lambda expressions are not allowed.")

def execute_user_code(script_to_execute: str):
    """
    Execute a user-supplied Python script in a restricted environment.
    
    Parameters
    ----------
    script_to_execute : str
        The user's Python script as a string.

    Returns
    -------
    str or None
        Captured stdout output if the script prints something,
        otherwise None.

    Raises
    ------
    ValueError
        If the script contains prohibited actions or has syntax errors.
    """
    try:
        parsed = ast.parse(script_to_execute, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in script: {exc}") from exc

    # Validate the AST for safety
    _validate_ast(parsed)

    # Prepare restricted globals and locals
    safe_globals = {"__builtins__": SAFE_BUILTINS}
    safe_locals = {}

    # Capture stdout
    old_stdout = sys.stdout
    stdout_capture = io.StringIO()
    try:
        sys.stdout = stdout_capture
        exec(compile(parsed, filename="<user_script>", mode="exec"),
             safe_globals, safe_locals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from exc
    finally:
        sys.stdout = old_stdout

    output = stdout_capture.getvalue()
    return output if output else None