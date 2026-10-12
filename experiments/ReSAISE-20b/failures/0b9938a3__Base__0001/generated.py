import ast

# Whitelist of safe names that may appear in expressions (e.g., math functions)
SAFE_NAMES = {
    'abs', 'round', 'min', 'max',
}

def _is_safe_node(node: ast.AST) -> bool:
    """
    Recursively check that the AST node contains only safe constructs.
    Allowed nodes: Expression, BoolOp, BinOp, UnaryOp, Compare,
    Call (only to SAFE_NAMES), Num, Str, NameConstant, Constant,
    List, Tuple, Dict, Set.
    """
    allowed_types = (
        ast.Expression, ast.BoolOp, ast.BinOp, ast.UnaryOp,
        ast.Compare, ast.Call, ast.Num, ast.Str, ast.NameConstant,
        ast.Constant, ast.List, ast.Tuple, ast.Dict, ast.Set,
    )
    if not isinstance(node, allowed_types):
        return False

    # Check calls
    if isinstance(node, ast.Call):
        # Only allow function names from SAFE_NAMES
        if not isinstance(node.func, ast.Name):
            return False
        if node.func.id not in SAFE_NAMES:
            return False

    # Recursively check child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def process_user_input(user_query: str) -> str:
    """
    Safely evaluate a user-provided Python expression.

    Parameters
    ----------
    user_query : str
        The expression to evaluate.

    Returns
    -------
    str
        Result of the evaluation as a string, or 'Error!' on failure.
    """
    try:
        # Parse the expression
        parsed = ast.parse(user_query, mode='eval')

        # Validate AST safety
        if not _is_safe_node(parsed):
            return 'Error!'

        # Compile and evaluate with no globals or builtins
        code = compile(parsed, '<string>', 'eval')
        result = eval(code, {'__builtins__': {}}, {})
        return str(result)
    except Exception:
        return 'Error!'