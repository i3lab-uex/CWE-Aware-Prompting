import ast

def safe_execute_code(snippet: str):
    """
    Execute a small Python snippet safely.

    Only expressions that do not contain function calls, imports or
    other potentially unsafe constructs are allowed. The snippet is
    evaluated in a sandboxed environment with no built‑ins.

    Parameters:
        snippet (str): The Python code to execute.

    Returns:
        Any: The result of the expression if present, otherwise None.

    Raises:
        ValueError: If the snippet contains disallowed nodes.
    """
    # Parse the code into an AST
    try:
        parsed = ast.parse(snippet, mode='eval')
    except SyntaxError as exc:
        # Try to parse as a module (multiple statements)
        try:
            parsed = ast.parse(snippet, mode='exec')
        except SyntaxError as exc2:
            raise ValueError(f"Syntax error in snippet: {exc2}") from None

    # Define a set of allowed node types
    ALLOWED_NODES = {
        ast.Expression,
        ast.Module,
        ast.Expr,
        ast.Num,          # Python <3.8
        ast.Constant,     # Python 3.8+
        ast.BinOp,
        ast.UnaryOp,
        ast.operator,     # binary operators
        ast.unaryop,      # unary operators
        ast.NameConstant,
        ast.Tuple,
        ast.List,
        ast.Dict,
        ast.Set,
        ast.Name,
        ast.Load,
    }

    # Walk the tree and ensure only allowed nodes are present
    for node in ast.walk(parsed):
        if type(node) not in ALLOWED_NODES:
            raise ValueError(f"Disallowed syntax: {type(node).__name__}")

        # Disallow any function calls
        if isinstance(node, ast.Call):
            raise ValueError("Function calls are not allowed")

    # Prepare a sandboxed environment
    safe_globals = {"__builtins__": None}
    safe_locals = {}

    # Execute or evaluate based on the parsed mode
    if isinstance(parsed, ast.Expression):
        return eval(compile(parsed, filename="<safe>", mode="eval"),
                    safe_globals, safe_locals)
    else:
        exec(compile(parsed, filename="<safe>", mode="exec"),
             safe_globals, safe_locals)
        return None