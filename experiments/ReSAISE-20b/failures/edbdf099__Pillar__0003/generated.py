import ast

def process_user_code(code_script: str) -> str:
    """
    Safely evaluate a small Python script that performs basic arithmetic or
    string operations.  Any attempt to use disallowed syntax (imports,
    attribute access, function calls, etc.) results in 'Execution Blocked!'.

    Parameters
    ----------
    code_script : str
        A Python script containing a single expression or statement.

    Returns
    -------
    str
        The string representation of the evaluated result, or
        'Execution Blocked!' if unsafe code is detected.
    """

    # Define a set of AST node types that are considered safe
    SAFE_NODES = {
        ast.Module,
        ast.Expr,
        ast.Expression,
        ast.Num,          # numeric literals (Python <3.8)
        ast.Constant,     # Python 3.8+: numeric/string/None literals
        ast.BinOp,
        ast.UnaryOp,
        ast.BoolOp,
        ast.Compare,
        ast.NameConstant, # True/False/None for older Python
        ast.List,
        ast.Tuple,
        ast.Dict,
        ast.Set,
        ast.Str,          # string literals (Python <3.8)
        ast.Name,         # variable names (only allowed builtins)
        ast.Load,
    }

    # Allowed names in the expression
    ALLOWED_NAMES = {
        'True', 'False', 'None',
        # add any builtins you want to expose, e.g., len
    }

    try:
        # Parse the script into an AST
        tree = ast.parse(code_script, mode='eval')
    except SyntaxError:
        # If parsing fails we block the execution
        return 'Execution Blocked!'

    # Recursive check for disallowed nodes and names
    def _check_node(node):
        if type(node) not in SAFE_NODES:
            return False
        # Names must be whitelisted
        if isinstance(node, ast.Name):
            if node.id not in ALLOWED_NAMES:
                return False
        # Recurse into children
        for child in ast.iter_child_nodes(node):
            if not _check_node(child):
                return False
        return True

    if not _check_node(tree):
        return 'Execution Blocked!'

    # Prepare a safe evaluation environment
    safe_globals = {}
    safe_locals = {}

    try:
        result = eval(compile(tree, filename='<user_code>', mode='eval'),
                      safe_globals, safe_locals)
    except Exception:
        # Any runtime error is treated as a block
        return 'Execution Blocked!'

    return str(result)