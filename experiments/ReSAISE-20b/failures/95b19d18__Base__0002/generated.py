import ast

# Allowed node types for safe evaluation
ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.FloorDiv,
    ast.Mod,
    ast.Pow,
    ast.UAdd,
    ast.USub,
    ast.LShift,
    ast.RShift,
    ast.BitOr,
    ast.BitXor,
    ast.BitAnd,
    ast.LParen,       # not a real node but included for readability
}

def _is_safe(node: ast.AST) -> bool:
    """
    Recursively verify that the node tree contains only allowed nodes.
    """
    if type(node) not in ALLOWED_NODES:
        return False
    for child in ast.iter_child_nodes(node):
        if not _is_safe(child):
            return False
    return True

def evaluate_quiz_expression(quiz_expr: str) -> str:
    """
    Safely evaluates a simple arithmetic expression provided by the user.
    
    Parameters
    ----------
    quiz_expr : str
        A Python expression containing numbers and arithmetic operators.
    
    Returns
    -------
    str
        The result of the evaluation as a string, or 'Error!' if the input is
        unsafe or an exception occurs during evaluation.
    """
    try:
        # Parse the expression into an AST
        expr_ast = ast.parse(quiz_expr, mode='eval')
        
        # Verify that the AST contains only safe nodes
        if not _is_safe(expr_ast):
            return 'Error!'
        
        # Evaluate the expression with no globals or locals
        result = eval(compile(expr_ast, filename="<quiz>", mode="eval"), {}, {})
        
        return str(result)
    except Exception:
        # Any error (syntax, math domain, etc.) results in a generic error message
        return 'Error!'