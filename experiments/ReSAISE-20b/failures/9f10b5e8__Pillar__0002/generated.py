import ast

def run_user_query(query: str) -> str:
    """
    Safely evaluate a user-provided Python expression and return its string representation.
    If the expression is unsafe, malformed, or an error occurs during evaluation,
    return 'Error!'.

    Parameters
    ----------
    query : str
        The user-provided expression to evaluate.

    Returns
    -------
    str
        String representation of the evaluation result or 'Error!'.
    """
    # Basic check: reject empty queries
    if not query.strip():
        return "Error!"

    try:
        # Parse the expression into an AST node
        expr_ast = ast.parse(query, mode="eval")
    except SyntaxError:
        return "Error!"

    # Define a whitelist of allowed AST node types
    allowed_nodes = (
        ast.Expression,
        ast.Constant,          # literals: numbers, strings, booleans
        ast.Num,               # for Python <3.8 compatibility
        ast.Str,
        ast.Bytes,
        ast.NameConstant,      # True/False/None for older Python
        ast.BinOp,
        ast.UnaryOp,
        ast.BoolOp,
        ast.Compare,
        ast.Call,              # allow function calls but only to whitelisted functions
        ast.Attribute,
        ast.List, ast.Tuple,
        ast.Dict,
        ast.Set,
    )

    # Recursively walk the AST to ensure only allowed nodes are present
    for node in ast.walk(expr_ast):
        if not isinstance(node, allowed_nodes):
            return "Error!"
        # Disallow attribute access to built-ins
        if isinstance(node, ast.Attribute):
            return "Error!"

    # Whitelisted functions: only math operations and built-ins that are safe
    allowed_builtins = {
        "abs": abs,
        "min": min,
        "max": max,
        "sum": sum,
        "len": len,
        # Add more safe functions as needed
    }

    # Prepare the evaluation environment
    safe_globals = {"__builtins__": None}
    safe_locals = allowed_builtins.copy()

    try:
        result = eval(compile(expr_ast, filename="<user_query>", mode="eval"),
                      safe_globals, safe_locals)
    except Exception:
        return "Error!"

    # Convert the result to string for consistent output
    try:
        return str(result)
    except Exception:
        return "Error!"