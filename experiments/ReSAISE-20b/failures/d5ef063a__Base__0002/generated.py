import ast

# Allowed AST node types for safe execution
SAFE_NODES = {
    ast.Module,
    ast.Expr,
    ast.Load,
    ast.Store,
    ast.Name,
    ast.Constant,
    ast.BinOp,
    ast.UnaryOp,
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow,
    ast.USub, ast.UAdd,
    ast.Call,
    ast.Attribute,
    ast.List, ast.Tuple,
    ast.Dict,
    ast.Compare,
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    ast.IfExp,
}

# Functions that are considered safe (e.g., print, len)
SAFE_FUNCTIONS = {
    'print': print,
    'len': len,
    'range': range,
    'int': int,
    'float': float,
    'str': str,
}

def _check_ast(node):
    """
    Recursively ensure that all nodes in the AST are within SAFE_NODES.
    Raise ValueError if an unsafe node is found.
    """
    if type(node) not in SAFE_NODES:
        raise ValueError(f"Disallowed node: {type(node).__name__}")
    for child in ast.iter_child_nodes(node):
        _check_ast(child)

def restricted_run_code(run_code: str):
    """
    Execute a user-provided Python script in a highly restricted environment.
    
    Parameters
    ----------
    run_code : str
        The Python code to execute.

    Returns
    -------
    None or any value returned by the script.
    
    Raises
    ------
    ValueError
        If the code contains syntax errors or attempts prohibited actions.
    """
    # Parse the code to an AST and validate node types
    try:
        parsed = ast.parse(run_code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error: {exc}") from exc

    _check_ast(parsed)

    # Build a restricted global namespace
    safe_globals = {"__builtins__": {}}
    safe_globals.update(SAFE_FUNCTIONS)

    # Capture printed output
    import io, sys
    old_stdout = sys.stdout
    fake_out = io.StringIO()
    sys.stdout = fake_out

    try:
        exec(compile(parsed, filename="<restricted>", mode="exec"), safe_globals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from exc
    finally:
        sys.stdout = old_stdout

    # Return captured output if any, else None
    out_text = fake_out.getvalue()
    return out_text if out_text else None

# Example usage:
if __name__ == "__main__":
    code = """
x = 5
y = len([1,2,3])
print(x + y)
"""
    print("Output:", restricted_run_code(code))