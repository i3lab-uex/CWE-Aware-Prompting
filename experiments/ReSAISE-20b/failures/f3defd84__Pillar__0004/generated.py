import ast

def evaluate_input_expression(expression: str) -> str:
    """
    Safely evaluates a simple arithmetic or logical expression supplied by the user.
    Returns the result as a string, or 'Processing Failed!' if any error occurs
    or the expression contains disallowed constructs.
    """
    # Allowed node types
    allowed_nodes = {
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.BoolOp,
        ast.Compare,
        ast.NameConstant,   # True, False, None (Python <3.8)
        ast.Constant,       # numeric literals (Python >=3.8)
        ast.Num,            # numeric literals for older Python
    }

    # Allowed operators
    allowed_ops = {
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
        ast.Mod, ast.Pow,
        ast.UAdd, ast.USub, ast.Not,
        ast.And, ast.Or,
        ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    }

    # Allowed names
    allowed_names = {"True", "False", "None"}

    try:
        # Parse the expression into an AST
        tree = ast.parse(expression, mode="eval")

        # Recursively verify nodes are allowed
        for node in ast.walk(tree):
            if type(node) not in allowed_nodes:
                return "Processing Failed!"
            if isinstance(node, ast.BinOp) and type(node.op) not in allowed_ops:
                return "Processing Failed!"
            if isinstance(node, ast.UnaryOp) and type(node.op) not in allowed_ops:
                return "Processing Failed!"
            if isinstance(node, ast.BoolOp) and type(node.op) not in allowed_ops:
                return "Processing Failed!"
            if isinstance(node, ast.Compare):
                for op in node.ops:
                    if type(op) not in allowed_ops:
                        return "Processing Failed!"
            if isinstance(node, ast.Name):
                if node.id not in allowed_names:
                    return "Processing Failed!"

        # Evaluate the expression safely
        result = eval(compile(tree, filename="<ast>", mode="eval"), {}, {})
        return str(result)

    except Exception:
        # Any exception leads to a failure message
        return "Processing Failed!"