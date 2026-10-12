import ast
import builtins
import sys
from contextlib import redirect_stdout
from io import StringIO

# A set of disallowed AST node types that could lead to unsafe operations
DISALLOWED_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Exec,          # Python 2
    ast.Call,         # restrict calls to safe builtins only
}

# A set of disallowed builtin names that should not be accessible in the sandbox
DISALLOWED_BUILTINS = {
    "open", "eval", "exec", "compile", "input",
    "__import__", "globals", "locals", "vars",
}

def _sanitize_ast(node: ast.AST):
    """
    Recursively walk the AST and raise ValueError if disallowed nodes or
    unsafe function calls are detected.
    """
    for child in ast.walk(node):
        # Disallow import statements
        if isinstance(child, (ast.Import, ast.ImportFrom)):
            raise ValueError("Import statements are not allowed.")
        # Disallow calls to disallowed builtins
        if isinstance(child, ast.Call):
            func = child.func
            # Function name could be a Name or Attribute
            if isinstance(func, ast.Name):
                func_name = func.id
            elif isinstance(func, ast.Attribute):
                # e.g., os.system -> disallow any attribute call
                raise ValueError(f"Attribute calls like {ast.unparse(func)} are disallowed.")
            else:
                raise ValueError("Complex function calls are not allowed.")

            if func_name in DISALLOWED_BUILTINS:
                raise ValueError(f"Use of builtin '{func_name}' is disallowed.")
            # Allow only a whitelist of safe builtins
            if func_name not in SAFE_BUILTINS:
                raise ValueError(f"Call to '{func_name}' is not allowed.")
    # No disallowed nodes found
    return

# Whitelist of safe builtins that can be used in the sandbox
SAFE_BUILTINS = {
    "abs", "all", "any", "bool", "chr", "complex",
    "dict", "divmod", "float", "int", "len",
    "list", "max", "min", "pow", "range",
    "round", "set", "str", "sum", "tuple",
}

def process_code_input(code_input: str):
    """
    Execute a Python code snippet safely.

    Parameters
    ----------
    code_input : str
        The Python code to run.

    Returns
    -------
    None or object
        If the snippet prints nothing and does not evaluate to a value,
        returns None.  Otherwise, returns the last expression's result
        if available.

    Raises
    ------
    ValueError
        If the code contains disallowed operations or unsafe constructs.
    """
    # Parse into an AST and validate
    try:
        parsed = ast.parse(code_input, mode="exec")
    except SyntaxError as e:
        raise ValueError(f"Syntax error in code: {e}")

    _sanitize_ast(parsed)

    # Prepare restricted globals
    sandbox_globals = {"__builtins__": {name: getattr(builtins, name) for name in SAFE_BUILTINS}}
    sandbox_locals = {}

    # Capture stdout
    output_buffer = StringIO()
    with redirect_stdout(output_buffer):
        try:
            exec(compile(parsed, filename="<sandbox>", mode="exec"),
                 sandbox_globals,
                 sandbox_locals)
        except Exception as exc:
            raise ValueError(f"Runtime error: {exc}") from exc

    # Determine if there is a result to return
    # If the code contains a last expression (e.g., `x = 5; x`), it will be
    # stored in the last line of `sandbox_locals`.  Since we executed in
    # exec mode, no explicit value is returned.  We simply check for any
    # output on stdout.
    captured_output = output_buffer.getvalue()
    if captured_output.strip():
        return captured_output.rstrip("\n")
    # No printed output; return None
    return None