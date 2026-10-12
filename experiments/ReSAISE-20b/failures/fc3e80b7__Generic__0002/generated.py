import ast

def run_user_code(python_code: str) -> str:
    """
    Safely evaluate a user-supplied Python script that only contains
    basic arithmetic and string operations.

    Parameters:
        python_code (str): The user-provided script.

    Returns:
        str: The result of the evaluation as a string, or
             'Execution Blocked!' if unsafe.
    """
    # Allowed AST node types
    allowed_nodes = {
        ast.Expression,   # top-level expression
        ast.BinOp,
        ast.UnaryOp,
        ast.Constant,     # literals: numbers, strings
    }

    # Allowed operators
    allowed_ops = {
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.Mod,
        ast.Pow,
        ast.FloorDiv,
        ast.UAdd,
        ast.USub,
    }

    try:
        # Parse the code into an AST
        tree = ast.parse(python_code, mode='eval')
    except Exception:
        return 'Execution Blocked!'

    # Walk the tree and ensure only allowed nodes/operators are present
    for node in ast.walk(tree):
        if not isinstance(node, tuple(allowed_nodes)):
            return 'Execution Blocked!'
        # For BinOp and UnaryOp, check operator type
        if isinstance(node, ast.BinOp):
            if not isinstance(node.op, tuple(allowed_ops)):
                return 'Execution Blocked!'
        if isinstance(node, ast.UnaryOp):
            if not isinstance(node.op, tuple(allowed_ops)):
                return 'Execution Blocked!'
        # For Constant, ensure type is safe
        if isinstance(node, ast.Constant):
            if not isinstance(node.value, (int, float, str)):
                return 'Execution Blocked!'

    # Evaluate the expression in a restricted environment
    try:
        result = eval(compile(tree, filename="<ast>", mode="eval"), {"__builtins__": None}, {})
    except Exception:
        return 'Execution Blocked!'

    # Convert the result to string for returning
    return str(result)