import ast

# A set of AST node types that are considered safe.
SAFE_NODES = {
    ast.Module,
    ast.Expr,
    ast.Assign,
    ast.Name,
    ast.Load,
    ast.Store,
    ast.Constant,
    ast.Num,          # for Python <3.8
    ast.Str,          # for Python <3.8
    ast.Tuple,
    ast.List,
    ast.Dict,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.IfExp,
    ast.Subscript,
    ast.Index,        # for Python <3.9
    ast.Slice,
    ast.Attribute,
    ast.JoinedStr,    # f-strings
    ast.FormattedValue,
}

# Operators that are allowed.
SAFE_OPERATORS = (
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
    ast.Mod, ast.Pow, ast.LShift, ast.RShift,
    ast.BitOr, ast.BitAnd, ast.BitXor,
    ast.Invert, ast.Not, ast.UAdd, ast.USub,
    ast.And, ast.Or, ast.Eq, ast.NotEq, ast.Lt,
    ast.LtE, ast.Gt, ast.GtE, ast.Is, ast.IsNot,
    ast.In, ast.NotIn
)

def _check_node(node):
    """
    Recursively check that the node and its children are all safe.
    Raise ValueError if an unsafe node is found.
    """
    if type(node) not in SAFE_NODES:
        raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Disallow any function calls.
    if isinstance(node, ast.Call):
        raise ValueError("Function calls are not allowed")

    # Disallow imports.
    if isinstance(node, (ast.Import, ast.ImportFrom)):
        raise ValueError("Import statements are not allowed")

    # Disallow attribute access that could reach dangerous objects.
    if isinstance(node, ast.Attribute):
        # Only allow simple attributes of literals or names that we whitelist.
        if isinstance(node.value, (ast.Name, ast.Constant)):
            # Further checks can be added here.
            pass
        else:
            raise ValueError("Complex attribute access is not allowed")

    # Check operators.
    if isinstance(node, ast.BinOp) or isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in SAFE_OPERATORS:
            raise ValueError(f"Disallowed operator: {op_type.__name__}")

    # Recursively check all child nodes.
    for child in ast.iter_child_nodes(node):
        _check_node(child)

def execute_python_script(python_code: str):
    """
    Execute a user-provided Python script in a sandboxed environment.
    Only very simple, non-harmful operations are permitted.

    Parameters
    ----------
    python_code : str
        The code to execute.

    Returns
    -------
    Any
        The result of the executed script if it is a single expression,
        otherwise None.

    Raises
    ------
    ValueError
        If the script contains disallowed operations or invalid syntax.
    """
    try:
        # Parse the code into an AST.
        tree = ast.parse(python_code, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Validate all nodes in the AST.
    for node in ast.walk(tree):
        _check_node(node)

    # Prepare a very restricted global environment.
    safe_globals = {"__builtins__": {}}
    local_vars = {}

    # If the script is a single expression, evaluate it.
    if len(tree.body) == 1 and isinstance(tree.body[0], ast.Expr):
        try:
            expr = compile(ast.Expression(body=tree.body[0].value), '<string>', 'eval')
            return eval(expr, safe_globals, local_vars)
        except Exception as e:
            raise ValueError(f"Execution error: {e}") from None

    # Otherwise execute the script normally.
    try:
        exec(compile(tree, '<string>', 'exec'), safe_globals, local_vars)
    except Exception as e:
        raise ValueError(f"Execution error: {e}") from None

    return None