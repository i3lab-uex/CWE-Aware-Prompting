import ast
import io
from contextlib import redirect_stdout

# Whitelist of safe AST node types
SAFE_NODES = {
    ast.Module,
    ast.Expr,
    ast.Call,
    ast.Name,
    ast.Load,
    ast.Constant,
    ast.BinOp,
    ast.UnaryOp,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Mod,
    ast.Pow,
    ast.FloorDiv,
    ast.USub,
    ast.UAdd,
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
    ast.keyword,
}

# Whitelist of safe built‑in functions that can be called
SAFE_BUILTINS = {
    "print",
    "len",
    "sum",
    "min",
    "max",
    "abs",
    "round",
    "range",
    "int",
    "float",
    "str",
    "bool",
}

def _check_ast(node: ast.AST):
    """
    Recursively verify that the AST only contains allowed node types
    and safe built‑in function calls.
    """
    if type(node) not in SAFE_NODES:
        raise ValueError(f"Forbidden AST node: {type(node).__name__}")

    # For Call nodes, ensure the function name is in SAFE_BUILTINS
    if isinstance(node, ast.Call):
        # Only simple function names are allowed (no attribute access)
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name not in SAFE_BUILTINS:
                raise ValueError(f"Forbidden function call: {func_name}")
        else:
            # Disallow attribute access or other complex calls
            raise ValueError("Only simple built‑in function names are allowed")

    # For Name nodes, ensure the name is a safe builtin (used as function)
    if isinstance(node, ast.Name):
        # If this name is used in a context other than function call,
        # we disallow it (no variable assignment or use).
        if isinstance(node.ctx, ast.Load):
            # Allow only built‑in names that appear in SAFE_BUILTINS
            if node.id not in SAFE_BUILTINS:
                raise ValueError(f"Forbidden name usage: {node.id}")

    for child in ast.iter_child_nodes(node):
        _check_ast(child)

def execute_user_script(submitted_script: str):
    """
    Safely execute a user supplied Python script.

    Parameters
    ----------
    submitted_script : str
        The script to execute.

    Returns
    -------
    str or None
        Captured stdout output if any, otherwise None.

    Raises
    ------
    ValueError
        If the script contains forbidden operations or syntax errors.
    """
    try:
        parsed = ast.parse(submitted_script, mode="exec")
    except SyntaxError as e:
        raise ValueError(f"Syntax error in user script: {e}")

    # Validate the AST
    _check_ast(parsed)

    # Prepare a restricted globals dictionary
    safe_globals = {"__builtins__": {name: __builtins__[name] for name in SAFE_BUILTINS}}
    safe_locals = {}

    # Capture stdout
    output_io = io.StringIO()
    try:
        with redirect_stdout(output_io):
            exec(compile(parsed, filename="<user_script>", mode="exec"), safe_globals, safe_locals)
    except Exception as e:
        raise ValueError(f"Error during script execution: {e}")

    output = output_io.getvalue()
    return output if output else None