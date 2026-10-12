import ast
from typing import Any, Optional


# Define a whitelist of allowed AST node types for simple expressions.
_ALLOWED_NODES = {
    ast.Module,
    ast.Expr,
    ast.Expression,
    ast.Load,
    ast.Name,
    ast.Constant,
    ast.BinOp,
    ast.UnaryOp,
    ast.Call,
    ast.keyword,
    # Operators
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow,
    ast.USub, ast.UAdd,
    # Comparisons
    ast.Compare, ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    # Boolean ops
    ast.BoolOp, ast.And, ast.Or,
    # Subscript (e.g., a[0])
    ast.Subscript, ast.Index, ast.Slice,
}

# Allow only built-in functions that are safe
_SAFE_BUILTINS = {
    'abs': abs,
    'min': min,
    'max': max,
    'sum': sum,
    'len': len,
    'range': range,
    'int': int,
    'float': float,
    'str': str,
    'bool': bool,
    'list': list,
    'dict': dict,
    'tuple': tuple,
    'set': set,
}


def _is_safe_node(node: ast.AST) -> bool:
    """Recursively check that every node in the AST is allowed."""
    if type(node) not in _ALLOWED_NODES:
        return False
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True


def run_code_snippet(user_code: str) -> Optional[Any]:
    """
    Execute a user-provided Python code snippet in a sandboxed environment.

    The function only allows safe, read‑only operations:
      * simple expressions (arithmetic, comparisons)
      * calls to a whitelist of built‑in functions
      * no imports, file I/O, or execution of arbitrary code

    Parameters
    ----------
    user_code : str
        The Python code to execute.

    Returns
    -------
    Any or None
        The result of the last expression, or None if nothing is returned.

    Raises
    ------
    ValueError
        If the code contains disallowed syntax or attempts unsafe operations.
    """
    # Parse the code into an AST
    try:
        tree = ast.parse(user_code, mode='eval')
    except SyntaxError as exc:
        # If the code is not a single expression, try statement mode
        try:
            tree = ast.parse(user_code, mode='exec')
        except SyntaxError as exc2:
            raise ValueError(f"Syntax error in user code: {exc}") from None

    # Validate the AST
    if not _is_safe_node(tree):
        raise ValueError("User code contains prohibited or unsafe operations.")

    # Prepare the execution environment
    exec_globals = {"__builtins__": _SAFE_BUILTINS}
    exec_locals: dict[str, Any] = {}

    # Execute the code
    try:
        if isinstance(tree.body, ast.Module):
            # Multiple statements: exec
            compiled = compile(tree, filename="<user_code>", mode="exec")
            exec(compiled, exec_globals, exec_locals)
            # Return the value of the last expression if any
            if exec_locals:
                return exec_locals.get("_result")
        else:
            # Single expression: eval
            compiled = compile(tree, filename="<user_code>", mode="eval")
            return eval(compiled, exec_globals, exec_locals)
    except Exception as exc:
        # Wrap any exception in ValueError to avoid leaking internals
        raise ValueError(f"Error executing user code: {exc}") from None

    return None