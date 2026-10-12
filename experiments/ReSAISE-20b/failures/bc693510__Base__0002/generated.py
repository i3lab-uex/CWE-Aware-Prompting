import ast
from typing import Any

# Define a whitelist of allowed AST node types
_ALLOWED_NODES = {
    # Expressions
    ast.Expression, ast.Str, ast.Bytes, ast.Num, ast.Constant,
    ast.Name, ast.Load, ast.Attribute,
    # Literals and containers
    ast.Tuple, ast.List, ast.Dict, ast.Set,
    # Operations
    ast.BinOp, ast.UnaryOp, ast.BoolOp, ast.Compare,
    # Operators
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
    ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr,
    ast.BitXor, ast.BitAnd, ast.Invert, ast.Not, ast.UAdd,
    ast.USub, ast.And, ast.Or, ast.Eq, ast.NotEq, ast.Lt,
    ast.LtE, ast.Gt, ast.GtE, ast.Is, ast.IsNot, ast.In,
    ast.NotIn,
    # Function calls (restricted to built-in safe functions)
    ast.Call, ast.NameConstant,
}

# Whitelisted built‑in names that can be used in the snippet
_ALLOWED_BUILTINS = {
    'abs': abs,
    'len': len,
    'sum': sum,
    'min': min,
    'max': max,
    'sorted': sorted,
    'round': round,
    # Add more safe functions if needed
}

def _is_safe_node(node: ast.AST) -> bool:
    """
    Recursively ensure that every node in the AST is from the whitelist.
    """
    if type(node) not in _ALLOWED_NODES:
        return False
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def run_python_snippet(python_snippet: str) -> Any:
    """
    Execute a small, user‑provided Python snippet in a restricted environment.

    Parameters
    ----------
    python_snippet : str
        The code snippet to execute. It may contain one or more expressions,
        but only safe operations are permitted.

    Returns
    -------
    Any
        The value of the last expression in the snippet, or None if no
        expression produces a value.

    Raises
    ------
    ValueError
        If the snippet contains disallowed syntax, imports, or other unsafe
        constructs.
    """
    # Parse the snippet into an AST; disallow multi‑statement modules
    try:
        tree = ast.parse(python_snippet, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python code: {exc}") from None

    # Verify that the AST contains only safe nodes
    if not _is_safe_node(tree):
        raise ValueError("The snippet contains prohibited or unsafe operations.")

    # Prepare the execution environment
    safe_globals = {"__builtins__": _ALLOWED_BUILTINS}
    # No local variables are allowed to be created
    safe_locals = {}

    # Evaluate the expression safely
    try:
        result = eval(compile(tree, filename="<snippet>", mode="eval"),
                      safe_globals, safe_locals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from None

    return result