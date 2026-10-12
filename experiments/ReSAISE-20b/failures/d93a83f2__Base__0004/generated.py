import ast

# Allowed built-in functions (if any). Empty to avoid surprises.
ALLOWED_BUILTINS = {}

# Allowed AST node types for a simple expression
_ALLOWED_NODES = {
    ast.Expression,
    ast.Module,
    ast.Expr,
    ast.Constant,
    ast.Name,
    ast.Load,
    ast.Store,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.IfExp,
    ast.Call,          # If you want to allow function calls
    ast.keyword,
    ast.Attribute,
    # Operators
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow,
    ast.LShift, ast.RShift, ast.BitOr, ast.BitAnd, ast.BitXor,
    ast.FloorDiv,
    ast.And, ast.Or,
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    # Unary operators
    ast.UAdd, ast.USub, ast.Not,
}

# Disallowed node types (for quick rejection)
_FORBIDDEN_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Exec,           # Python 2 only; kept for completeness
    ast.Global,
    ast.Nonlocal,
    ast.With,
    ast.FunctionDef,
    ast.ClassDef,
    ast.Lambda,
    ast.Assign,
    ast.AugAssign,
    ast.For,
    ast.While,
    ast.If,
    ast.Try,
    ast.Raise,
    ast.Delete,
    ast.Yield,
    ast.YieldFrom,
}

def _check_ast(node: ast.AST):
    """
    Recursively walk the AST and ensure that only allowed nodes are present.
    Raises ValueError if a forbidden node is encountered.
    """
    if type(node) in _FORBIDDEN_NODES:
        raise ValueError(f"Forbidden node: {type(node).__name__}")

    if type(node) not in _ALLOWED_NODES:
        raise ValueError(f"Disallowed node: {type(node).__name__}")

    for child in ast.iter_child_nodes(node):
        _check_ast(child)

def safe_execute_code(snippet: str):
    """
    Execute a user-provided Python code snippet in a highly restricted environment.

    Parameters
    ----------
    snippet : str
        The Python code to execute. Must be a single expression.

    Returns
    -------
    Any
        The result of the evaluated expression, or None if there is no result.

    Raises
    ------
    ValueError
        If the snippet contains prohibited actions or disallowed syntax.
    """
    # Parse the code into an AST
    try:
        parsed = ast.parse(snippet, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in snippet: {e}")

    # Validate the AST
    _check_ast(parsed)

    # Prepare a restricted execution environment
    safe_globals = {"__builtins__": ALLOWED_BUILTINS}
    safe_locals = {}

    # Evaluate the expression
    try:
        result = eval(compile(parsed, filename="<safe>", mode="eval"),
                      safe_globals,
                      safe_locals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from exc

    return result