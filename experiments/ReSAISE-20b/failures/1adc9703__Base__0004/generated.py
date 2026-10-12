import ast

# Allowed operators and node types for a safe expression evaluator.
ALLOWED_OPERATORS = {
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.FloorDiv,
    ast.Mod,
    ast.Pow,
    ast.UAdd,
    ast.USub,
}

# Allowed node types: literals, expressions, binary/unary operations.
ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
}

def _is_safe_node(node: ast.AST) -> bool:
    """
    Recursively verify that the AST node only contains allowed constructs.
    """
    if type(node) not in ALLOWED_NODES:
        return False
    if isinstance(node, ast.BinOp):
        if type(node.op) not in ALLOWED_OPERATORS:
            return False
    if isinstance(node, ast.UnaryOp):
        if type(node.op) not in ALLOWED_OPERATORS:
            return False
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def process_user_expression(expr: str) -> str:
    """
    Safely evaluate a simple mathematical expression provided by the user.
    
    Parameters
    ----------
    expr : str
        The user supplied expression to evaluate.

    Returns
    -------
    str
        Result of the evaluated expression or 'Processing Failed!' on error.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode='eval')
        
        # Ensure the entire tree is safe
        if not _is_safe_node(parsed):
            return 'Processing Failed!'
        
        # Evaluate the expression in a restricted namespace
        result = eval(compile(parsed, filename="<user_expr>", mode="eval"), {"__builtins__": None}, {})
        return str(result)
    except Exception:
        # Any exception (syntax, type error, division by zero, etc.) results in failure
        return 'Processing Failed!'