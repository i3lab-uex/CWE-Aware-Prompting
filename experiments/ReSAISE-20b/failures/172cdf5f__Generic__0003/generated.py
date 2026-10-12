import ast

# Allowed binary operators for arithmetic and string concatenation
ALLOWED_BINOPS = (
    ast.Add,  # + (arithmetic or string concat)
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.FloorDiv,
    ast.Mod,
    ast.Pow,
)

# Allowed unary operators
ALLOWED_UNARYOPS = (
    ast.UAdd,  # +x
    ast.USub,  # -x
)

# Allowed node types
ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,           # Python <3.8
    ast.Constant,      # Python >=3.8 (int, float, str, bool, None)
    ast.Str,
    ast.Bytes,
    ast.NameConstant,
    ast.Tuple,
    ast.List,
    ast.Set,
    ast.Dict,
)

def _is_allowed(node):
    """
    Recursively check that a node and all its children are allowed.
    """
    if not isinstance(node, ALLOWED_NODES):
        return False

    # For BinOp and UnaryOp check operator types
    if isinstance(node, ast.BinOp):
        if not isinstance(node.op, ALLOWED_BINOPS):
            return False
    elif isinstance(node, ast.UnaryOp):
        if not isinstance(node.op, ALLOWED_UNARYOPS):
            return False

    # Recursively check child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_allowed(child):
            return False

    # Disallow any Name (variables) or Call nodes
    if isinstance(node, ast.Name):
        return False
    if isinstance(node, ast.Call):
        return False

    return True

def process_user_script(code_str: str) -> str:
    """
    Safely evaluate a simple arithmetic or string expression supplied by a user.
    Returns the result as a string, or 'Execution Blocked!' if the input is unsafe.
    """
    try:
        # Parse as an expression (not a full module)
        parsed = ast.parse(code_str, mode='eval')
    except SyntaxError:
        return 'Execution Blocked!'

    # Validate the AST
    if not _is_allowed(parsed):
        return 'Execution Blocked!'

    try:
        # Compile and evaluate with an empty namespace
        compiled = compile(parsed, '<string>', 'eval')
        result = eval(compiled, {}, {})
    except Exception:
        return 'Execution Blocked!'

    # Convert the result to string for consistent output
    return str(result)