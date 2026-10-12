import ast

# Allowed node types and operators for a safe evaluation environment
_ALLOWED_NODES = {
    ast.Expression,
    ast.Constant,          # literals (int, float, str, bool, None)
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.Name,              # only for True/False/None
}

_ALLOWED_BINOPS = {
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.FloorDiv,
    ast.Mod,
    ast.Pow,
    ast.LShift,
    ast.RShift,
    ast.BitOr,
    ast.BitAnd,
    ast.BitXor,
}

_ALLOWED_UNARYOPS = {
    ast.UAdd,
    ast.USub,
    ast.Not,
}

_ALLOWED_BOOLOPS = {ast.And, ast.Or}
_ALLOWED_COMPARISONS = {
    ast.Eq,
    ast.NotEq,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,
}

_ALLOWED_NAMES = {"True", "False", "None"}

def _is_safe_node(node: ast.AST) -> bool:
    """Recursively check if a node and its children are safe."""
    if type(node) not in _ALLOWED_NODES:
        return False

    if isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_BINOPS:
            return False
    elif isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_UNARYOPS:
            return False
    elif isinstance(node, ast.BoolOp):
        if type(node.op) not in _ALLOWED_BOOLOPS:
            return False
    elif isinstance(node, ast.Compare):
        if any(type(op) not in _ALLOWED_COMPARISONS for op in node.ops):
            return False
    elif isinstance(node, ast.Name):
        if node.id not in _ALLOWED_NAMES:
            return False

    # Recursively check child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False

    return True

def run_user_script(script_input: str) -> str:
    """
    Safely evaluate a user-provided Python expression that may contain
    basic arithmetic or string operations.

    Parameters:
        script_input (str): The user-provided Python code.

    Returns:
        str: The string representation of the evaluated result, or
             'Execution Blocked!' if unsafe code is detected.
    """
    try:
        # Parse the input into an AST
        tree = ast.parse(script_input, mode="eval")
    except SyntaxError:
        return "Execution Blocked!"

    # Validate the AST for safety
    if not _is_safe_node(tree):
        return "Execution Blocked!"

    try:
        # Compile and evaluate the expression in a restricted environment
        compiled = compile(tree, filename="<user_script>", mode="eval")
        result = eval(compiled, {"__builtins__": {}}, {})
    except Exception:
        # Any runtime error is treated as unsafe
        return "Execution Blocked!"

    return str(result)