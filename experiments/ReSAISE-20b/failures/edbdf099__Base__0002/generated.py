import ast

# Allowed built‑in functions that may appear in user code
ALLOWED_BUILTINS = {
    "len": len,
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
}

# Allowed AST node types
ALLOWED_NODES = (
    ast.Expression,  # top level
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.Call,
    ast.Name,
    ast.Constant,   # Python 3.8+: literal values
    ast.Num,        # older literals
    ast.Str,
    ast.Bytes,
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
)

# Operators that are considered safe
SAFE_OPERATORS = (
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
    ast.Mod, ast.Pow, ast.UAdd, ast.USub,
    ast.And, ast.Or, ast.Not,
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
)

def _is_safe_node(node):
    """
    Recursively ensure that every node in the AST is of an allowed type
    and uses only safe operators.
    """
    if not isinstance(node, ALLOWED_NODES):
        return False

    # Check operators for BinOp and BoolOp
    if isinstance(node, (ast.BinOp, ast.BoolOp)):
        if not isinstance(node.op, SAFE_OPERATORS):
            return False

    # Check comparison operators
    if isinstance(node, ast.Compare):
        for op in node.ops:
            if not isinstance(op, SAFE_OPERATORS):
                return False

    # Calls must be to allowed built‑ins only
    if isinstance(node, ast.Call):
        func = node.func
        # allow simple name calls (e.g., len(x))
        if isinstance(func, ast.Name):
            if func.id not in ALLOWED_BUILTINS:
                return False
        else:
            # disallow attribute calls or complex expressions
            return False

    # Names are only allowed if they refer to built‑ins or constants
    if isinstance(node, ast.Name):
        if node.id not in ALLOWED_BUILTINS and node.id not in ("True", "False", "None"):
            return False

    # Recurse into child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def process_user_code(code_script: str) -> str:
    """
    Safely evaluate a user supplied Python expression or simple script.
    Returns the string representation of the result, or 'Execution Blocked!'
    if any unsafe constructs are detected.
    """
    try:
        # Parse the code into an AST
        parsed = ast.parse(code_script, mode="eval")  # only expressions allowed

    except SyntaxError:
        return "Execution Blocked!"

    # Validate the AST
    if not _is_safe_node(parsed):
        return "Execution Blocked!"

    # Prepare safe evaluation environment
    safe_globals = {"__builtins__": None}
    safe_locals = ALLOWED_BUILTINS.copy()

    try:
        result = eval(compile(parsed, "<user_code>", mode="eval"),
                      safe_globals,
                      safe_locals)
    except Exception:
        return "Execution Blocked!"

    return str(result)