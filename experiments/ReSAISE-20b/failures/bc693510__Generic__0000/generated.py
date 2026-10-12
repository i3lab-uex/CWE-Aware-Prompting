import ast

def run_python_snippet(python_snippet: str):
    """
    Execute a user-provided Python snippet in a safe sandbox.

    Parameters
    ----------
    python_snippet : str
        The Python code to execute. Only simple expressions are allowed.

    Returns
    -------
    Any
        The result of the evaluated expression, or None if nothing is returned.

    Raises
    ------
    ValueError
        If the snippet contains disallowed syntax or constructs.
    """
    # Define a set of AST node types that are considered safe
    SAFE_NODES = {
        ast.Expression,
        ast.Module,
        ast.Expr,
        ast.Constant,          # Numbers, strings, booleans, None
        ast.Num,               # For Python <3.8 compatibility
        ast.Str,
        ast.Bytes,
        ast.NameConstant,      # For Python <3.8 compatibility
        ast.BinOp,
        ast.UnaryOp,
        ast.BoolOp,
        ast.Compare,
        ast.Name,              # Variable names (only loads)
        ast.Load,
        ast.operator,
        ast.unaryop,
        ast.boolop,
        ast.cmpop,
    }

    # Helper function to recursively walk the AST and ensure all nodes are safe
    def _check_safe(node: ast.AST):
        if type(node) not in SAFE_NODES:
            raise ValueError(f"Disallowed construct: {type(node).__name__}")
        for child in ast.iter_child_nodes(node):
            _check_safe(child)

    try:
        # Parse the snippet. We accept either a single expression or a module.
        parsed = ast.parse(python_snippet, mode='eval')
    except SyntaxError:
        # If eval fails, try as a module (e.g., multiple statements)
        parsed = ast.parse(python_snippet, mode='exec')
        # For exec mode we don't return a value
        _check_safe(parsed)
        # Execute with empty globals/locals for safety
        exec(compile(parsed, '<string>', 'exec'), {}, {})
        return None

    # Ensure the parsed AST is safe
    _check_safe(parsed)

    # Evaluate the expression safely
    return eval(compile(parsed, '<string>', 'eval'), {}, {})