import ast

def evaluate_user_code(code_string: str) -> str:
    """
    Safely evaluates a Python expression supplied by the user.

    Parameters
    ----------
    code_string : str
        A string containing a Python expression to evaluate.

    Returns
    -------
    str
        The string representation of the evaluated result, or
        'Unsafe Code Detected!' if the input contains disallowed constructs
        or evaluation fails for any reason.
    """
    # Define a set of AST node types that are considered unsafe
    disallowed_nodes = {
        ast.Import, ast.ImportFrom,          # importing modules
        ast.Exec,                              # exec statement (Python 2)
        ast.Call,                               # function calls in general
        ast.Attribute,                          # attribute access (e.g., __import__)
        ast.Lambda,                            # lambda expressions
        ast.Yield, ast.YieldFrom,              # generators
    }

    # Further restrict the allowed nodes to a minimal set that represents
    # arithmetic, comparisons, boolean logic and literals.
    allowed_nodes = {
        ast.Expression,
        ast.Module,
        ast.Expr,
        ast.Constant,   # literals in Python 3.8+
        ast.Num,        # numeric literal (Python <3.8)
        ast.Str,        # string literal (Python <3.8)
        ast.Bytes,
        ast.NameConstant,
        ast.BinOp, ast.UnaryOp, ast.BoolOp,
        ast.Compare,
        ast.Subscript,  # e.g., a[0]
        ast.Index,
        ast.Slice,
        ast.List, ast.Tuple, ast.Dict, ast.Set,
        ast.Name,
        # Operators
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
        ast.Mod, ast.Pow, ast.LShift, ast.RShift,
        ast.BitOr, ast.BitXor, ast.BitAnd, ast.MatMult,
        ast.UAdd, ast.USub, ast.Not,
        ast.And, ast.Or, ast.Eq, ast.NotEq,
        ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    }

    # Parse the code to an AST
    try:
        tree = ast.parse(code_string, mode='eval')
    except SyntaxError:
        return 'Unsafe Code Detected!'

    # Walk the tree and reject disallowed nodes
    for node in ast.walk(tree):
        if isinstance(node, tuple(disallowed_nodes)):
            return 'Unsafe Code Detected!'
        # Allow only the nodes in allowed set
        if not isinstance(node, tuple(allowed_nodes)):
            return 'Unsafe Code Detected!'

    # Prepare a safe evaluation environment
    safe_globals = {"__builtins__": {}}
    try:
        result = eval(compile(tree, filename="<user_code>", mode="eval"), safe_globals, {})
        return str(result)
    except Exception:
        # Any runtime error is treated as unsafe
        return 'Unsafe Code Detected!'