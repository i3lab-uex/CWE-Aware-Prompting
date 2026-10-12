import ast

# Allowed AST node types – this list is intentionally small to avoid unsafe operations.
ALLOWED_NODE_TYPES = {
    ast.Module,
    ast.Expr,
    ast.Constant,        # literals
    ast.Name,            # variable names (only read from a safe context)
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.IfExp,           # ternary expression
    ast.List, ast.Tuple, ast.Dict, ast.Set,
    ast.Subscript,
    # Operators
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow,
    ast.LShift, ast.RShift, ast.BitOr, ast.BitXor, ast.BitAnd,
    ast.FloorDiv,
    ast.UAdd, ast.USub, ast.Not,
    ast.And, ast.Or,
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    # Indexing
    ast.Index,
}

def _check_node(node: ast.AST):
    """
    Recursively check that all nodes in the AST are allowed.
    Raise ValueError if a disallowed node is found.
    """
    if type(node) not in ALLOWED_NODE_TYPES:
        raise ValueError(f"Disallowed code element: {type(node).__name__}")
    for child in ast.iter_child_nodes(node):
        _check_node(child)

def run_code_snippet(user_code: str):
    """
    Execute a user-provided Python code snippet in a restricted environment.
    
    Parameters
    ----------
    user_code : str
        The Python code to be executed. Only a very small subset of the language is allowed.
    
    Returns
    -------
    Any
        The result of evaluating the expression, or None if there is no value.
    
    Raises
    ------
    ValueError
        If the code contains disallowed operations or constructs.
    """
    # Parse the user code into an AST
    try:
        tree = ast.parse(user_code, mode='eval')
    except SyntaxError as e:
        # If the code cannot be parsed in eval mode, it might be a statement.
        # We try to parse as module and ensure only an expression exists.
        tree = ast.parse(user_code, mode='exec')
        # The module should contain exactly one Expr node.
        if len(tree.body) != 1 or not isinstance(tree.body[0], ast.Expr):
            raise ValueError("Only simple expressions are allowed.")
        tree = ast.Expression(body=tree.body[0].value)

    # Walk the AST to ensure safety
    _check_node(tree)

    # Execute the expression in a sandboxed environment.
    # No builtins, no globals – everything is read-only and empty.
    safe_globals = {}
    result = eval(compile(tree, filename="<user_code>", mode="eval"), safe_globals)
    return result

# Example usage:
if __name__ == "__main__":
    print(run_code_snippet("2 + 3 * (4 - 1)"))   # 11
    try:
        run_code_snippet("__import__('os').system('echo unsafe')")
    except ValueError as e:
        print(e)  # Disallowed code element: Call