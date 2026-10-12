import ast

def _is_safe_node(node: ast.AST) -> bool:
    """
    Recursively check that the AST node only contains safe expressions.
    Allowed nodes: literals, arithmetic/boolean ops, unary ops,
    name lookups for a limited set of safe names (e.g., math constants),
    and function calls to whitelisted functions.
    """
    safe_nodes = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.BoolOp,
        ast.Compare,
        ast.Call,
        ast.Name,
        ast.Load,
        ast.Constant,
        ast.Num,      # for Python <3.8
        ast.Str,
        ast.Bytes,
        ast.List,
        ast.Tuple,
        ast.Dict,
        ast.Set,
    )
    if not isinstance(node, safe_nodes):
        return False

    # Disallow attribute access
    if isinstance(node, ast.Attribute):
        return False

    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False

    # If it's a Call, restrict function name
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            return False
        # Whitelist allowed function names
        allowed_funcs = {"abs", "round", "min", "max"}
        if node.func.id not in allowed_funcs:
            return False

    # If it's a Name, restrict to allowed names
    if isinstance(node, ast.Name):
        allowed_names = {"True", "False", "None"}
        if node.id not in allowed_names:
            return False

    return True


def process_user_expression(query_expr: str) -> str:
    """
    Safely evaluate a user supplied Python expression.

    Parameters
    ----------
    query_expr : str
        The expression to evaluate.

    Returns
    -------
    str
        Result of the evaluation as a string, or 'Error!' if unsafe or
        evaluation fails.
    """
    try:
        # Parse expression to AST and ensure it's a single expression
        parsed = ast.parse(query_expr, mode="eval")

        # Validate AST nodes
        if not _is_safe_node(parsed):
            return "Error!"

        # Evaluate with no builtins or globals
        result = eval(compile(parsed, "<string>", mode="eval"),
                      {"__builtins__": None}, {})
        return str(result)
    except Exception:
        return "Error!"