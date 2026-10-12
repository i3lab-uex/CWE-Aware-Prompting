import ast
import builtins

# Define a whitelist of allowed names and modules
SAFE_BUILTINS = {
    'abs', 'all', 'any', 'bool', 'dict', 'float', 'int',
    'len', 'list', 'max', 'min', 'pow', 'range', 'round',
    'str', 'sum', 'tuple', 'zip'
}

# Allowed AST node types
ALLOWED_NODES = {
    ast.Module,
    ast.Expr, ast.Load,
    ast.Assign, ast.AugAssign,
    ast.Name, ast.Constant,
    ast.BinOp, ast.UnaryOp, ast.BoolOp,
    ast.Compare, ast.IfExp,
    ast.Call, ast.Attribute,
    ast.List, ast.Tuple, ast.Dict,
    ast.Set, ast.Subscript, ast.Index,
    ast.Slice, ast.ExtSlice,
    ast.For, ast.While, ast.If,
    ast.Return, ast.FunctionDef, ast.arguments,
    ast.arg, ast.keyword,
    # Operators
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
    ast.Mod, ast.Pow, ast.LShift, ast.RShift,
    ast.BitOr, ast.BitAnd, ast.BitXor, ast.Invert,
    ast.Not, ast.And, ast.Or,
    # Comparisons
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE,
    ast.Gt, ast.GtE, ast.Is, ast.IsNot,
    ast.In, ast.NotIn
}

def _check_ast(node: ast.AST):
    """
    Recursively verify that the AST only contains allowed nodes.
    Raise ValueError if an illegal node is encountered.
    """
    if type(node) not in ALLOWED_NODES:
        raise ValueError(f"Disallowed construct: {type(node).__name__}")
    for child in ast.iter_child_nodes(node):
        _check_ast(child)

def safe_run_script(script_code: str):
    """
    Execute user supplied Python code in a restricted environment.
    
    Parameters
    ----------
    script_code : str
        The Python code to execute.

    Returns
    -------
    result : Any
        The value of the last expression in the script, or None if none.

    Raises
    ------
    ValueError
        If the code contains disallowed constructs or invalid syntax.
    """
    # Parse the code into an AST
    try:
        tree = ast.parse(script_code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Ensure the AST only contains safe nodes
    _check_ast(tree)

    # Prepare a restricted globals dict
    safe_globals = {name: getattr(builtins, name) for name in SAFE_BUILTINS}
    # Provide a minimal __builtins__ to avoid accidental access
    safe_globals['__builtins__'] = None

    # Execute the code
    exec(compile(tree, filename="<safe_script>", mode="exec"), safe_globals)

    # Retrieve the result of the last expression if any
    # We look for a 'return' value or the value of the last Expr node
    result = None
    for node in reversed(tree.body):
        if isinstance(node, ast.Return):
            result = eval(compile(ast.Expression(body=node.value), "", "eval"), safe_globals)
            break
        if isinstance(node, ast.Expr):
            result = eval(compile(ast.Expression(body=node.value), "", "eval"), safe_globals)
            break

    return result