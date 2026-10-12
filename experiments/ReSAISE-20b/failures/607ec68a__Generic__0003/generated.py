import ast
import io
import contextlib

# Whitelist of safe built‑in functions that the user is allowed to call.
SAFE_BUILTINS = {
    'print': print,
    'len': len,
    'range': range,
    'str': str,
    'int': int,
    'float': float,
    'bool': bool,
    # Add more safe built‑ins here if needed.
}

# Allowed AST node types for a simple expression/statement language
ALLOWED_NODES = {
    ast.Module,
    ast.Expr,
    ast.Expression,
    ast.Str,  # Python <3.8
    ast.Constant,  # Python >=3.8 for literals
    ast.Num,
    ast.Bytes,
    ast.Name,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.Call,
    ast.keyword,
    ast.Load,
    ast.Store,
    ast.Expr,
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
    ast.Subscript,
    ast.Index,  # Python <3.9
    ast.Slice,
    ast.NameConstant,  # True/False/None in older Python
}

# Allowed operators (binary, unary, boolean)
ALLOWED_OPERATORS = (
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
    ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr,
    ast.BitXor, ast.BitAnd, ast.MatMult,
    ast.UAdd, ast.USub, ast.Not,
    ast.And, ast.Or,
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
)

def _check_node(node):
    """
    Recursively validate a node and its children.
    Raises ValueError if any disallowed construct is found.
    """
    # Node type check
    if not isinstance(node, tuple(ALLOWED_NODES)):
        raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Operator checks
    if isinstance(node, (ast.BinOp, ast.UnaryOp, ast.BoolOp)):
        if not isinstance(node.op, ALLOWED_OPERATORS):
            raise ValueError(f"Disallowed operator: {type(node.op).__name__}")

    # Name checks
    if isinstance(node, ast.Name):
        if node.id not in SAFE_BUILTINS and node.ctx.__class__ not in (ast.Load, ast.Store):
            raise ValueError(f"Use of unknown name: {node.id}")

    # Call checks
    if isinstance(node, ast.Call):
        func = node.func
        if not isinstance(func, ast.Name) or func.id not in SAFE_BUILTINS:
            raise ValueError(f"Disallowed function call: {ast.dump(node)}")

    # Recursively validate child nodes
    for child in ast.iter_child_nodes(node):
        _check_node(child)

def safe_run_script(code: str):
    """
    Execute a user supplied Python script in a restricted environment.
    
    Parameters
    ----------
    code : str
        The user supplied Python script.

    Returns
    -------
    str or None
        Captured stdout output if any, otherwise None.

    Raises
    ------
    ValueError
        If the script contains disallowed syntax or attempts forbidden actions.
    """
    # Parse and validate
    try:
        tree = ast.parse(code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user code: {exc}") from None

    try:
        _check_node(tree)
    except ValueError as exc:
        raise ValueError(f"Disallowed operation in user code: {exc}") from None

    # Prepare restricted globals
    safe_globals = {'__builtins__': SAFE_BUILTINS}

    # Capture stdout
    out_stream = io.StringIO()
    try:
        with contextlib.redirect_stdout(out_stream):
            exec(compile(tree, filename="<user_script>", mode="exec"), safe_globals)
    except Exception as exc:
        raise ValueError(f"Runtime error in user code: {exc}") from None

    output = out_stream.getvalue()
    return output if output else None