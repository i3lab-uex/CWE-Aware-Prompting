import ast

# Allowed AST node types for a safe, expression‑only evaluator
ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Str,
    ast.Bytes,
    ast.NameConstant, # True/False/None
    ast.Tuple,
    ast.List,
    ast.Dict,
    ast.Set,
}

# Allowed operators
ALLOWED_OPERATORS = {
    ast.Add,  # + (also string concat)
    ast.Sub,  # -
    ast.Mult, # *
    ast.Div,  # /
    ast.FloorDiv,  # //
    ast.Mod,  # %
    ast.Pow,  # **
    ast.UAdd, # unary +
    ast.USub, # unary -
}

# Optional: allow parentheses via ast.Expr only
def _is_safe(node):
    """
    Recursively ensure that the AST node tree contains only allowed nodes
    and operators.
    """
    if type(node) not in ALLOWED_NODES:
        return False

    # Check operator nodes
    if isinstance(node, ast.BinOp):
        if type(node.op) not in ALLOWED_OPERATORS:
            return False
    elif isinstance(node, ast.UnaryOp):
        if type(node.op) not in ALLOWED_OPERATORS:
            return False

    # Recurse into child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe(child):
            return False

    return True

def parse_user_script(script_str: str) -> str:
    """
    Safely evaluate a tiny Python script containing only basic arithmetic
    or string operations.

    Parameters:
        script_str (str): The user-provided script to evaluate.

    Returns:
        str: The string representation of the result, or a security warning.
    """
    # Reject empty input immediately
    if not script_str.strip():
        return "Execution Blocked!"

    try:
        # Parse as an expression only
        parsed = ast.parse(script_str, mode='eval')
    except SyntaxError:
        return "Execution Blocked!"

    # Validate the parsed AST
    if not _is_safe(parsed):
        return "Execution Blocked!"

    try:
        # Evaluate with no builtins or globals
        result = eval(compile(parsed, filename="<user_script>", mode="eval"),
                      {"__builtins__": None}, {})
    except Exception:
        return "Execution Blocked!"

    # Convert the result to string for consistent output
    try:
        return str(result)
    except Exception:
        return "Execution Blocked!"