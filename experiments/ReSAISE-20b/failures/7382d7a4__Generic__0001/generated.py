import ast

# Allowed AST node types and operators for a very small sandbox.
ALLOWED_NODES = {
    ast.Expression,
    ast.Module,
    ast.Expr,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # for Python < 3.8
    ast.Constant,     # for Python >= 3.8
    ast.Str,          # legacy string constants
    ast.NameConstant, # True/False/None
}

ALLOWED_BINOPS = {
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.FloorDiv,
    ast.Mod,
    ast.Pow,
}

ALLOWED_UNARYOPS = {
    ast.UAdd,
    ast.USub,
}


def _is_safe(node: ast.AST) -> bool:
    """Recursively check that all nodes are allowed."""
    if type(node) not in ALLOWED_NODES:
        return False

    # Check binary operations
    if isinstance(node, ast.BinOp):
        if type(node.op) not in ALLOWED_BINOPS:
            return False
    # Check unary operations
    if isinstance(node, ast.UnaryOp):
        if type(node.op) not in ALLOWED_UNARYOPS:
            return False

    # Recursively check children
    for child in ast.iter_child_nodes(node):
        if not _is_safe(child):
            return False
    return True


def execute_user_code(script_code: str) -> str:
    """
    Evaluate a user supplied script containing only simple arithmetic or
    string operations.  If the code contains disallowed constructs, return
    'Execution Blocked!'.

    Parameters
    ----------
    script_code : str
        User supplied Python code.

    Returns
    -------
    str
        Result of the evaluation or 'Execution Blocked!'.
    """
    try:
        # Parse the code into an AST
        parsed = ast.parse(script_code, mode="eval")
    except SyntaxError:
        return "Execution Blocked!"

    # Verify that the AST contains only allowed nodes
    if not _is_safe(parsed):
        return "Execution Blocked!"

    # Safely evaluate the expression
    try:
        result = eval(compile(parsed, "<string>", mode="eval"), {}, {})
        return str(result)
    except Exception:
        # Any runtime error is treated as unsafe
        return "Execution Blocked!"