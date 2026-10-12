import ast

def evaluate_student_response(student_query: str) -> str:
    """
    Safely evaluates a simple Python expression provided by the student.
    
    Parameters
    ----------
    student_query : str
        A string containing a Python expression to evaluate.

    Returns
    -------
    str
        The string representation of the evaluation result, or 'Error!'
        if the expression is invalid or potentially malicious.
    """
    # Basic whitelist of allowed AST node types
    ALLOWED_NODES = {
        ast.Expression,
        ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant,
        ast.Name, ast.Load, ast.Call,
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod,
        ast.Pow, ast.LShift, ast.RShift, ast.BitOr,
        ast.BitAnd, ast.BitXor, ast.FloorDiv,
        ast.UAdd, ast.USub,
    }

    # Disallow any import or attribute access
    if any(tok.type == tok.OP and tok.string in ('import', 'from') for tok in ast.walk(ast.parse(student_query))):
        return "Error!"

    try:
        # Parse the expression to ensure it's safe
        tree = ast.parse(student_query, mode='eval')
        for node in ast.walk(tree):
            if type(node) not in ALLOWED_NODES:
                return "Error!"
    except Exception:
        return "Error!"

    # Evaluate with no builtins and empty globals/locals
    try:
        result = eval(compile(tree, filename="<student>", mode="eval"),
                      {"__builtins__": None}, {})
        return str(result)
    except Exception:
        return "Error!"