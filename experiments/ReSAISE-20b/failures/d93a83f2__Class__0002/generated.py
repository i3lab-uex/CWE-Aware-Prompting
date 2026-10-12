import ast
from types import SimpleNamespace

# Whitelisted built‑in functions that are considered safe.
SAFE_BUILTINS = {
    'abs', 'all', 'any', 'bool', 'chr', 'divmod',
    'float', 'hash', 'hex', 'int', 'isinstance',
    'len', 'max', 'min', 'pow', 'range', 'repr',
    'round', 'str', 'sum', 'tuple'
}

# Whitelisted names that may appear in the snippet (e.g., literals).
SAFE_NAMES = set(SAFE_BUILTINS)

# Allowed AST node types.
ALLOWED_NODES = (
    ast.Module,
    ast.Expr,
    ast.Assign,
    ast.AugAssign,
    ast.Name,
    ast.Constant,
    ast.Num,        # For Python <3.8
    ast.Str,        # For Python <3.8
    ast.Tuple,
    ast.List,
    ast.Dict,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.IfExp,
    ast.operator,   # generic operator node
    ast.unaryop,
    ast.boolop,
    ast.cmpop,
)

# Operators that are considered safe.
SAFE_OPERATORS = (
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
    ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr,
    ast.BitXor, ast.BitAnd, ast.UAdd, ast.USub, ast.Not,
    ast.Invert, ast.Eq, ast.NotEq, ast.Lt, ast.LtE,
    ast.Gt, ast.GtE, ast.Is, ast.IsNot, ast.In, ast.NotIn,
    ast.And, ast.Or
)

def _check_node(node: ast.AST):
    """Recursively ensure the node and its children are safe."""
    if not isinstance(node, ALLOWED_NODES):
        raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Check operators
    if isinstance(node, ast.operator) or isinstance(node, ast.unaryop) \
       or isinstance(node, ast.boolop) or isinstance(node, ast.cmpop):
        if type(node) not in SAFE_OPERATORS:
            raise ValueError(f"Disallowed operator: {type(node).__name__}")

    # Names must be whitelisted or built‑in
    if isinstance(node, ast.Name):
        if node.id not in SAFE_NAMES:
            raise ValueError(f"Use of untrusted name: {node.id}")

    # Disallow attribute access, calls, imports, etc.
    if isinstance(node, (ast.Call, ast.Attribute, ast.Subscript,
                         ast.Import, ast.ImportFrom, ast.Global,
                         ast.Nonlocal, ast.Lambda)):
        raise ValueError(f"Disallowed construct: {type(node).__name__}")

    for child in ast.iter_child_nodes(node):
        _check_node(child)

def safe_execute_code(snippet: str):
    """
    Execute a user‑provided Python snippet in a restricted environment.

    Parameters
    ----------
    snippet : str
        The code to execute. It may contain expressions, assignments,
        or simple statements.

    Returns
    -------
    Any
        The value of the last expression if present, otherwise None.

    Raises
    ------
    ValueError
        If the snippet contains disallowed syntax or constructs.
    """
    # Parse the code into an AST
    try:
        tree = ast.parse(snippet, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in snippet: {exc}")

    # Perform safety checks
    _check_node(tree)

    # Prepare a restricted globals dictionary.
    safe_globals = {name: __builtins__[name] for name in SAFE_BUILTINS}
    safe_globals['__builtins__'] = None  # prevent access to other builtins

    # Execute the code
    local_vars = {}
    try:
        exec(compile(tree, filename='<string>', mode='exec'), safe_globals, local_vars)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from exc

    # If the snippet ends with an expression, return its value.
    if tree.body and isinstance(tree.body[-1], ast.Expr):
        expr_node = tree.body[-1].value
        try:
            return eval(compile(ast.Expression(expr_node), filename='<string>', mode='eval'),
                        safe_globals, local_vars)
        except Exception as exc:
            raise ValueError(f"Evaluation error: {exc}") from exc

    return None