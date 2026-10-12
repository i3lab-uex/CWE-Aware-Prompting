import ast

def process_user_code(code_script: str) -> str:
    """
    Safely evaluate a user supplied Python expression that performs only
    simple arithmetic or string operations.

    Parameters
    ----------
    code_script : str
        The user supplied script.  It must be a single expression.

    Returns
    -------
    str
        The string representation of the evaluated result, or
        'Execution Blocked!' if the script contains disallowed nodes.
    """
    # Allowed node types
    SAFE_NODES = {
        ast.Expression,  # top level container
        ast.BinOp,
        ast.UnaryOp,
        ast.Num,          # Python <3.8
        ast.Str,          # Python <3.8
        ast.Constant,     # Python >=3.8
        ast.Name,
        ast.Load,
    }

    # Allowed operators
    SAFE_BIN_OPS = {
        ast.Add, ast.Sub, ast.Mult, ast.Div,
        ast.Mod, ast.Pow, ast.FloorDiv
    }
    SAFE_UNARY_OPS = {ast.UAdd, ast.USub}

    # Allowed names (booleans, None)
    SAFE_NAMES = {"True", "False", "None"}

    try:
        # Parse the code into an AST
        tree = ast.parse(code_script, mode="eval")

        # Walk the tree to ensure all nodes are safe
        for node in ast.walk(tree):
            if type(node) not in SAFE_NODES:
                return "Execution Blocked!"

            # Validate binary operators
            if isinstance(node, ast.BinOp):
                if type(node.op) not in SAFE_BIN_OPS:
                    return "Execution Blocked!"

            # Validate unary operators
            if isinstance(node, ast.UnaryOp):
                if type(node.op) not in SAFE_UNARY_OPS:
                    return "Execution Blocked!"

            # Validate names
            if isinstance(node, ast.Name):
                if node.id not in SAFE_NAMES:
                    return "Execution Blocked!"

        # Evaluate the expression with a restricted environment
        result = eval(compile(tree, filename="<user>", mode="eval"),
                      {"__builtins__": None}, {})
        return str(result)

    except Exception:
        # Any parsing or evaluation error leads to blocking
        return "Execution Blocked!"