import ast

def evaluate_user_code(code_string: str) -> str:
    """
    Safely evaluate a user supplied Python expression that contains only
    simple arithmetic or string operations.  Any disallowed syntax results
    in the special message 'Execution Blocked!'.

    Parameters
    ----------
    code_string : str
        The user supplied Python expression.

    Returns
    -------
    str
        Result of the evaluation converted to string, or 'Execution Blocked!'
        if the code contains unsafe constructs.
    """
    # Allowed AST node types
    allowed_nodes = {
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Num,          # Python <3.8
        ast.Str,          # Python <3.8
        ast.Constant,     # Python 3.8+
        ast.Name,
    }

    # Allowed operators
    allowed_ops = {
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
        ast.Mod, ast.Pow,
        ast.UAdd, ast.USub,
    }

    # Allowed names
    allowed_names = {"True", "False", "None"}

    try:
        parsed = ast.parse(code_string, mode='eval')
    except SyntaxError:
        return "Execution Blocked!"

    # Recursively check node safety
    def _check(node: ast.AST) -> bool:
        if type(node) not in allowed_nodes:
            return False
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.BinOp) or isinstance(child, ast.UnaryOp):
                # check operator
                if type(child.op) not in allowed_ops:
                    return False
            elif isinstance(child, ast.Name):
                if child.id not in allowed_names:
                    return False
            elif isinstance(child, (ast.Num, ast.Str)):
                pass  # literals are fine
            elif isinstance(child, ast.Constant):
                if not isinstance(child.value, (int, float, str, bool)) and child.value is not None:
                    return False
            # For all other nodes we already checked the type at top level
            if not _check(child):
                return False
        return True

    if not _check(parsed):
        return "Execution Blocked!"

    # Evaluate safely
    try:
        result = eval(compile(parsed, filename="<ast>", mode="eval"), {"__builtins__": {}}, {})
    except Exception:
        return "Execution Blocked!"

    return str(result)