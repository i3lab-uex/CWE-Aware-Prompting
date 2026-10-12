import ast

# A minimal set of safe built‑in functions that can be used in the snippet
SAFE_BUILTINS = {
    'abs': abs,
    'len': len,
    'sum': sum,
    'min': min,
    'max': max,
    'sorted': sorted,
    'range': range,
}

# Whitelisted AST node types that are considered safe
SAFE_NODES = {
    ast.Expression,
    ast.Module,
    ast.Expr,

    # Literals
    ast.Constant,   # Python 3.8+: handles numbers, strings, bytes, bools, None
    ast.Num,
    ast.Str,

    # Operations
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,

    # Operators
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod,
    ast.Pow, ast.LShift, ast.RShift, ast.BitOr, ast.BitXor, ast.BitAnd,
    ast.FloorDiv,
    ast.And, ast.Or, ast.Not,

    # Comparisons
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,

    # Function calls (only to whitelisted builtins)
    ast.Call,
    ast.Name,   # for function names and constants
}

def _is_safe_node(node: ast.AST) -> bool:
    """
    Recursively ensure that every node in the AST is within the whitelist.
    Raise ValueError if an unsafe node is encountered.
    """
    if type(node) not in SAFE_NODES:
        raise ValueError(f"Disallowed construct: {type(node).__name__}")

    # Special handling for function calls – only allow whitelisted builtins
    if isinstance(node, ast.Call):
        # The function being called must be a simple Name (no attribute access)
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function calls are allowed")
        if node.func.id not in SAFE_BUILTINS:
            raise ValueError(f"Calling '{node.func.id}' is not allowed")
        # Recursively check arguments
        for arg in node.args:
            _is_safe_node(arg)
        # No keyword args or starargs allowed
        if node.keywords:
            raise ValueError("Keyword arguments are not allowed")
        return

    # Recursively walk through child nodes
    for child in ast.iter_child_nodes(node):
        _is_safe_node(child)

def safe_execute_code(snippet: str):
    """
    Execute a user-provided Python code snippet safely.

    Parameters
    ----------
    snippet : str
        The Python source to execute. Only expressions using safe builtins,
        literals, and basic operators are permitted.

    Returns
    -------
    Any
        The value of the evaluated expression, or None if nothing is returned.

    Raises
    ------
    ValueError
        If the snippet contains disallowed constructs.
    """
    # Parse the code into an AST
    try:
        parsed = ast.parse(snippet, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in snippet: {e}")

    # Validate the AST
    _is_safe_node(parsed)

    # Prepare a minimal execution environment
    safe_globals = {"__builtins__": SAFE_BUILTINS}
    # No locals needed for eval
    try:
        result = eval(compile(parsed, filename="<safe>", mode="eval"), safe_globals)
    except Exception as e:
        # Wrap any runtime error in ValueError for consistency
        raise ValueError(f"Execution failed: {e}") from e

    return result

# Example usage (uncomment to test)
# print(safe_execute_code("2 + 3 * 4"))          # 14
# print(safe_execute_code("len('hello')"))       # 5
# safe_execute_code("__import__('os').system('ls')")  # Raises ValueError