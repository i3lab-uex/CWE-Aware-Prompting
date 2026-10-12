import ast

# Allowed AST node types for a safe expression
ALLOWED_NODES = {
    ast.Expression,  # top-level container
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.Call,  # allow limited builtins like len, abs
    ast.NameConstant,
    ast.Num,
    ast.Constant,
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
    ast.Name,
    ast.Subscript,
    ast.Index,
    ast.Slice,
}

# Allowed functions that can be used safely
SAFE_BUILTINS = {
    'abs': abs,
    'len': len,
    'min': min,
    'max': max,
    'sum': sum,
}

def _is_safe(node: ast.AST) -> bool:
    """Recursively ensure all nodes are in the allowed set."""
    if type(node) not in ALLOWED_NODES:
        return False
    for child in ast.iter_child_nodes(node):
        if not _is_safe(child):
            return False
    return True

def process_user_query(user_input: str) -> str:
    """
    Safely evaluate a simple Python expression from user input.
    
    Parameters
    ----------
    user_input : str
        The expression to evaluate.

    Returns
    -------
    str
        String representation of the result or 'Error!' on failure.
    """
    try:
        # Parse the expression
        parsed = ast.parse(user_input, mode='eval')
        
        # Verify safety of the AST
        if not _is_safe(parsed):
            return 'Error!'
        
        # Evaluate with restricted globals
        result = eval(
            compile(parsed, filename="<user_query>", mode="eval"),
            {"__builtins__": None},
            SAFE_BUILTINS
        )
        return str(result)
    except Exception:
        # Any parsing or evaluation error is treated as untrustworthy
        return 'Error!'