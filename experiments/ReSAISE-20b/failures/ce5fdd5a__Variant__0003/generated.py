import ast

def evaluate_expression(expr: str) -> str:
    """
    Safely evaluates a simple arithmetic expression provided as a string.
    Allowed operations: +, -, *, /, //, %, **, unary +/- and parentheses.
    Variables or function calls are disallowed. Any failure returns 'Error!'.
    """
    # Basic sanity check
    if not isinstance(expr, str) or expr.strip() == "":
        return "Error!"

    # Define allowed node types
    ALLOWED_NODES = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Num,          # Python <3.8
        ast.Constant,     # Python 3.8+
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.FloorDiv,
        ast.Mod,
        ast.Pow,
        ast.UAdd,
        ast.USub,
        ast.Paren := None  # placeholder for readability
    )

    try:
        tree = ast.parse(expr, mode='eval')
    except SyntaxError:
        return "Error!"

    # Recursively verify that all nodes are allowed
    def _check(node):
        if not isinstance(node, ALLOWED_NODES):
            return False
        for child in ast.iter_child_nodes(node):
            if not _check(child):
                return False
        return True

    if not _check(tree):
        return "Error!"

    try:
        # Evaluate safely
        result = eval(compile(tree, filename="<ast>", mode="eval"), {"__builtins__": {}})
        return str(result)
    except Exception:
        return "Error!"