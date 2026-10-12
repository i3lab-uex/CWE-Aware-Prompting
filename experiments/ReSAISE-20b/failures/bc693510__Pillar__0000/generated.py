import ast

# A minimal set of safe built‑in functions that may be used in the snippet.
SAFE_BUILTINS = {
    'len': len,
    'sum': sum,
    'abs': abs,
    'min': min,
    'max': max,
}

# Node types that are considered safe for evaluation.
SAFE_NODES = (
    ast.Expression,  # top level
    ast.Expr,
    ast.Constant,
    ast.Num,         # for Python <3.8
    ast.Str,         # for Python <3.8
    ast.Bytes,
    ast.Name,
    ast.Load,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.Call,
    ast.keyword,
    ast.operator,
    ast.unaryop,
    ast.boolop,
    ast.cmpop,
)

def _is_safe_node(node):
    """
    Recursively check that every node in the AST is of a safe type
    and that all names used are from SAFE_BUILTINS.
    """
    if not isinstance(node, SAFE_NODES):
        return False

    # Names must be from the whitelist
    if isinstance(node, ast.Name):
        if node.id not in SAFE_BUILTINS:
            return False

    # Calls may only target safe builtins
    if isinstance(node, ast.Call):
        func = node.func
        if not (isinstance(func, ast.Name) and func.id in SAFE_BUILTINS):
            return False

    # Recurse into child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def run_python_snippet(python_snippet: str):
    """
    Execute a user‑provided Python snippet safely.

    Parameters
    ----------
    python_snippet : str
        The code to execute.  Only a single expression is allowed.
        No imports, assignments, or other statements are permitted.

    Returns
    -------
    Any
        The result of the expression, or None if there is no value.

    Raises
    ------
    ValueError
        If the snippet contains disallowed syntax or unsafe names.
    """
    # Parse the snippet into an AST
    try:
        tree = ast.parse(python_snippet, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python expression: {exc}") from exc

    # Validate the AST
    if not _is_safe_node(tree):
        raise ValueError("Snippet contains prohibited or unsafe operations")

    # Evaluate the expression in a restricted environment
    try:
        result = eval(compile(tree, filename="<snippet>", mode="eval"),
                      {"__builtins__": SAFE_BUILTINS}, {})
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from exc

    return result