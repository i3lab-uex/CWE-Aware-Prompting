import ast
from typing import Any, Optional

# List of AST node types that are considered dangerous
_PROHIBITED_NODES = (
    ast.Import,          # import statements
    ast.ImportFrom,
    ast.Exec,            # exec() in Python 2 (kept for completeness)
    ast.Call,            # function calls – we will filter the names
)

# Names that are explicitly disallowed even if they appear in a Call node
_PROHIBITED_CALL_NAMES = {
    "open",   # file operations
    "eval",
    "exec",
    "__import__",
    "compile",
}

def _is_call_allowed(node: ast.Call) -> bool:
    """
    Allow only calls to built-in functions that are safe.
    We disallow any call that uses a Name node whose id is in
    _PROHIBITED_CALL_NAMES or any attribute access.
    """
    if isinstance(node.func, ast.Name):
        return node.func.id not in _PROHIBITED_CALL_NAMES
    # Disallow attribute calls (e.g., os.system)
    return False

def _validate_ast(tree: ast.AST) -> None:
    """
    Walk the AST and raise ValueError if any prohibited node is found.
    """
    for node in ast.walk(tree):
        if isinstance(node, _PROHIBITED_NODES):
            raise ValueError(f"Prohibited statement: {ast.dump(node)}")
        if isinstance(node, ast.Call) and not _is_call_allowed(node):
            raise ValueError(f"Disallowed function call: {ast.dump(node)}")

def run_python_snippet(python_snippet: str) -> Optional[Any]:
    """
    Execute a small Python snippet in a restricted environment.

    Parameters
    ----------
    python_snippet : str
        The code to execute. It may contain expressions and statements but
        must not use imports, eval/exec, or any disallowed function calls.

    Returns
    -------
    Any | None
        The value of the last expression in the snippet if present,
        otherwise ``None``.

    Raises
    ------
    ValueError
        If the snippet contains prohibited actions.
    """
    # Parse the code into an AST and validate it
    try:
        tree = ast.parse(python_snippet, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in snippet: {exc}") from exc

    _validate_ast(tree)

    # Prepare a restricted execution environment
    safe_globals = {"__builtins__": {}}
    # Expose a few harmless built-ins
    safe_builtins = {
        "abs": abs,
        "min": min,
        "max": max,
        "sum": sum,
        "len": len,
        "range": range,
        "float": float,
        "int": int,
        "str": str,
        "bool": bool,
    }
    safe_globals["__builtins__"].update(safe_builtins)

    # Execute the code
    exec(compile(tree, filename="<snippet>", mode="exec"), safe_globals)

    # If the last node is an expression, evaluate and return its value
    if tree.body and isinstance(tree.body[-1], ast.Expr):
        expr = compile(ast.Expression(body=tree.body[-1].value), filename="<expr>", mode="eval")
        return eval(expr, safe_globals)
    return None