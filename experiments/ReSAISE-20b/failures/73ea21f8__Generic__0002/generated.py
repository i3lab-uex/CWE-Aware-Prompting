import ast

# A list of AST node types that are considered safe.
SAFE_NODES = {
    ast.Module,
    ast.Expr,
    ast.Assign,
    ast.Name,
    ast.Load,
    ast.Store,
    ast.Constant,          # literals (int, float, str, bool, None)
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.IfExp,             # ternary
    ast.operator,
    ast.unaryop,
    ast.boolop,
    ast.cmpop,
    # allow simple subscript for indexing lists/dicts
    ast.Subscript,
    ast.Index,
    ast.Slice,
    # allow attribute access only on allowed names
    ast.Attribute,
}

# Names that are explicitly disallowed (builtins we don't want)
DISALLOWED_NAMES = {
    'open', 'exec', 'eval', 'compile', '__import__',
    'input', 'print', 'exit', 'quit', 'help',
}

def _is_safe_node(node):
    """Recursively check if the node and all its children are safe."""
    # Reject disallowed node types
    if type(node) not in SAFE_NODES:
        return False

    # Reject disallowed names
    if isinstance(node, ast.Name):
        if node.id in DISALLOWED_NAMES:
            return False

    # For attribute access, ensure the base object is safe
    if isinstance(node, ast.Attribute):
        return _is_safe_node(node.value)

    # For subscript, check the value and slice
    if isinstance(node, ast.Subscript):
        return _is_safe_node(node.value) and _is_safe_node(node.slice)

    # Recursively check all child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def run_code_snippet(user_code: str):
    """
    Execute a user-provided Python code snippet in a restricted environment.

    Parameters
    ----------
    user_code : str
        The Python code to execute.

    Returns
    -------
    Any
        Result of the last expression if present, otherwise None.

    Raises
    ------
    ValueError
        If the code contains disallowed operations.
    """
    # Parse the user code into an AST
    try:
        parsed = ast.parse(user_code, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in user code: {e}") from None

    # Ensure the entire AST is safe
    if not all(_is_safe_node(node) for node in parsed.body):
        raise ValueError("User code contains disallowed operations.")

    # Prepare a restricted globals dict
    safe_globals = {"__builtins__": None}
    # Allow access to a few built-in types for constants
    safe_globals.update({
        'True': True,
        'False': False,
        'None': None
    })

    # Execute the code
    exec(compile(parsed, filename="<user_snippet>", mode="exec"), safe_globals)

    # If the last statement is an expression, return its value
    if parsed.body and isinstance(parsed.body[-1], ast.Expr):
        # Evaluate the expression in the same safe environment
        expr = parsed.body[-1].value
        return eval(compile(ast.Expression(expr), filename="<user_snippet>", mode="eval"), safe_globals)

    return None