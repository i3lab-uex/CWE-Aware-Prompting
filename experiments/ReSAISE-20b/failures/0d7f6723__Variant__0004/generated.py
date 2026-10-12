import ast

def parse_user_script(script_str: str) -> str:
    """
    Safely evaluate a tiny Python script containing only basic arithmetic
    and string operations.  If the script contains any disallowed constructs,
    return 'Execution Blocked!'.

    Parameters
    ----------
    script_str : str
        The user supplied Python expression.

    Returns
    -------
    str
        String representation of the evaluated result or a security warning.
    """
    # Allowed AST node types
    allowed_nodes = {
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Constant,          # Python 3.8+ literal values
        ast.Num,               # Backward compatibility (Python <3.8)
        ast.Str,
        ast.Bytes,
        ast.NameConstant,      # True/False/None
        ast.Tuple,
        ast.List,
    }

    # Allowed operators
    allowed_ops = {
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod,
        ast.Pow, ast.FloorDiv,
        ast.UAdd, ast.USub
    }

    try:
        # Parse the expression into an AST node
        tree = ast.parse(script_str, mode='eval')
    except SyntaxError:
        return 'Execution Blocked!'

    # Recursively walk the tree and ensure all nodes are allowed
    for node in ast.walk(tree):
        if type(node) not in allowed_nodes:
            return 'Execution Blocked!'

        # For BinOp and UnaryOp, check operator types
        if isinstance(node, ast.BinOp):
            if type(node.op) not in allowed_ops:
                return 'Execution Blocked!'
        if isinstance(node, ast.UnaryOp):
            if type(node.op) not in allowed_ops:
                return 'Execution Blocked!'

        # Disallow any Name nodes (no variables)
        if isinstance(node, ast.Name):
            return 'Execution Blocked!'

    # Evaluate the expression in a restricted environment
    try:
        result = eval(compile(tree, filename='<user_script>', mode='eval'), {}, {})
    except Exception:
        return 'Execution Blocked!'

    # Return the string representation of the result
    return str(result)