import ast
from types import SimpleNamespace

# Whitelist of allowed AST node types
_ALLOWED_NODES = {
    ast.Module,
    ast.Expr,
    ast.Expression,
    ast.Load,
    ast.Store,
    ast.Name,
    ast.Constant,
    ast.BinOp,
    ast.UnaryOp,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Mod,
    ast.Pow,
    ast.FloorDiv,
    ast.LShift,
    ast.RShift,
    ast.BitOr,
    ast.BitXor,
    ast.BitAnd,
    ast.UAdd,
    ast.USub,
    ast.Not,
    ast.And,
    ast.Or,
    ast.Eq,
    ast.NotEq,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,
    ast.Is,
    ast.IsNot,
    ast.In,
    ast.NotIn,
    ast.Compare,
    ast.Call,
    ast.Attribute,
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
    ast.Subscript,
    ast.Index,
    ast.Slice,
    # Allow simple control flow
    ast.IfExp,
}

# Allowed built-in functions
_ALLOWED_BUILTINS = {
    'abs': abs,
    'min': min,
    'max': max,
    'sum': sum,
    'len': len,
    'range': range,
    'print': print,  # Note: print writes to stdout; can be redirected if needed
}

def _validate_ast(node):
    """
    Recursively ensure that every node in the AST is from the allowed set.
    Raises ValueError if a forbidden node is found.
    """
    if type(node) not in _ALLOWED_NODES:
        raise ValueError(f"Forbidden construct: {type(node).__name__}")
    for child in ast.iter_child_nodes(node):
        _validate_ast(child)

def execute_python_code(snippet_code: str):
    """
    Safely executes a small Python snippet and returns its result.

    Parameters
    ----------
    snippet_code : str
        The user-provided Python code to be executed.

    Returns
    -------
    Any
        The value of the last expression in the snippet, or None if there is none.

    Raises
    ------
    ValueError
        If the snippet contains forbidden operations or invalid code.
    """
    # Parse the code into an AST
    try:
        parsed = ast.parse(snippet_code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in snippet: {exc}") from None

    # Validate the AST
    _validate_ast(parsed)

    # Prepare a minimal execution environment
    safe_globals = {"__builtins__": _ALLOWED_BUILTINS}
    # Local namespace for variables defined in the snippet
    local_vars = {}

    # Execute the code
    try:
        exec(compile(parsed, filename="<safe_exec>", mode="exec"), safe_globals, local_vars)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from None

    # Return the value of the last expression if present
    if parsed.body and isinstance(parsed.body[-1], ast.Expr):
        # Evaluate the expression in the context of local_vars
        expr_code = compile(ast.Expression(parsed.body[-1].value), filename="<safe_exec>", mode="eval")
        return eval(expr_code, safe_globals, local_vars)

    return None