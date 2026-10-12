import ast

# Whitelisted built‑in functions and constants that may be used in expressions.
_ALLOWED_BUILTINS = {
    "abs", "round", "min", "max", "sum",
    "len", "range", "list", "dict", "set", "tuple",
    # Add more if desired
}

# Whitelisted AST node types for a safe expression.
_ALLOWED_AST_NODES = {
    ast.Expression,
    ast.Constant,
    ast.Num,          # Python <3.8
    ast.Str,          # Python <3.8
    ast.Bytes,        # Python <3.8
    ast.Name,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.Call,
    ast.Attribute,
    ast.List, ast.Tuple, ast.Set, ast.Dict,
    ast.Subscript,
    ast.Index,        # Python <3.9
    ast.Slice,
}

# Operators that are considered safe.
_ALLOWED_OPERATORS = {
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
    ast.Mod, ast.Pow, ast.LShift, ast.RShift,
    ast.BitOr, ast.BitAnd, ast.BitXor,
    ast.UAdd, ast.USub, ast.Not,
    ast.And, ast.Or,
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
}

def _is_allowed(node: ast.AST) -> bool:
    """
    Recursively verify that a node and all its children are allowed.
    """
    if type(node) not in _ALLOWED_AST_NODES:
        return False

    # Validate operator nodes separately
    if isinstance(node, (ast.BinOp, ast.BoolOp, ast.UnaryOp, ast.Compare)):
        for op in getattr(node, 'ops', []):
            if type(op) not in _ALLOWED_OPERATORS:
                return False
        # For UnaryOp, single operator
        if isinstance(node, ast.UnaryOp) and type(node.op) not in _ALLOWED_OPERATORS:
            return False

    # For function calls, ensure the called name is whitelisted
    if isinstance(node, ast.Call):
        # Only allow simple names or attributes that resolve to allowed builtins
        func = node.func
        if isinstance(func, ast.Name):
            if func.id not in _ALLOWED_BUILTINS:
                return False
        elif isinstance(func, ast.Attribute):
            # Disallow attribute access except for whitelisted builtins
            return False
        else:
            return False

    # Recursively check all child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_allowed(child):
            return False

    return True


def execute_code_snippet(code_snippet: str):
    """
    Execute a small, safe Python expression provided by the user.

    Parameters
    ----------
    code_snippet : str
        The Python code to be executed. Only a single expression is allowed.

    Returns
    -------
    Any
        The result of the evaluated expression, or None if the snippet has no value.

    Raises
    ------
    ValueError
        If the code contains disallowed operations or syntax.
    """
    # Parse the snippet; it must be a single expression
    try:
        parsed = ast.parse(code_snippet, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Verify the AST is safe
    if not _is_allowed(parsed):
        raise ValueError("Disallowed operation detected in code snippet")

    # Evaluate the expression safely with restricted globals
    safe_globals = {name: __builtins__[name] for name in _ALLOWED_BUILTINS if name in __builtins__}
    # No locals allowed
    try:
        result = eval(compile(parsed, filename="<snip>", mode="eval"), safe_globals, {})
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from exc

    return result