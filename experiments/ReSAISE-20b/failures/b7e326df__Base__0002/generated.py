import ast

# Allowed AST node types for safe evaluation
ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.NameConstant,  # True, False, None
    ast.Num,           # numeric literals (Python <3.8)
    ast.Constant,      # numeric/string/None literals (Python 3.8+)
    ast.Tuple,
    ast.List,
    ast.Dict,
    ast.Set,
    ast.Name,          # variable names (we will limit to safe ones)
    ast.Load,
    ast.Subscript,
    ast.Index,         # for subscript indexing
    ast.Slice,
}

# Names that are considered safe (e.g., math functions)
SAFE_NAMES = {
    "abs": abs,
    "round": round,
    "min": min,
    "max": max,
}

# Operators that are allowed
ALLOWED_OPERATORS = {
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
    ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr,
    ast.BitXor, ast.BitAnd, ast.Invert, ast.Not,
    ast.UAdd, ast.USub,
}

# Comparators that are allowed
ALLOWED_COMPARATORS = {
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    ast.Is, ast.IsNot, ast.In, ast.NotIn
}

def _is_safe_node(node):
    """
    Recursively verify that the AST node only contains allowed types.
    """
    if type(node) not in ALLOWED_NODES:
        return False
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    # Specific checks for operators and comparators
    if isinstance(node, ast.BinOp) and type(node.op) not in ALLOWED_OPERATORS:
        return False
    if isinstance(node, ast.UnaryOp) and type(node.op) not in ALLOWED_OPERATORS:
        return False
    if isinstance(node, ast.BoolOp):
        for op in node.ops:
            if type(op) not in ALLOWED_OPERATORS:
                return False
    if isinstance(node, ast.Compare):
        for op in node.ops:
            if type(op) not in ALLOWED_COMPARATORS:
                return False
    # Names: only allow SAFE_NAMES or built-in constants
    if isinstance(node, ast.Name):
        if node.id not in SAFE_NAMES and node.id not in {"True", "False", "None"}:
            return False
    return True

def execute_user_input(expr: str) -> str:
    """
    Safely evaluate a user-provided Python expression.

    Parameters
    ----------
    expr : str
        The expression to evaluate.

    Returns
    -------
    str
        String representation of the evaluation result or 'Error!' on failure.
    """
    try:
        # Parse expression into an AST
        parsed = ast.parse(expr, mode="eval")

        # Verify safety of the AST
        if not _is_safe_node(parsed):
            return "Error!"

        # Evaluate with restricted globals
        result = eval(
            parsed,
            {"__builtins__": None},  # no built-ins
            SAFE_NAMES              # only allowed functions
        )
        return str(result)
    except Exception:
        return "Error!"