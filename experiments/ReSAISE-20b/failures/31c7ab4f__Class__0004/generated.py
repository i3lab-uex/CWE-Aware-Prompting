import ast

# Whitelist of safe AST node types that are allowed in user expressions.
SAFE_NODES = {
    ast.Expression,
    ast.Module,
    ast.Expr,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.Call,
    ast.Name,
    ast.Load,
    ast.Constant,  # Python 3.8+ for literals
    ast.Num,       # For older Python versions
    ast.Str,
    ast.Bytes,
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
    ast.NameConstant,  # True/False/None
    ast.Subscript,
    ast.Index,
    ast.Slice,
    ast.Attribute,  # allow attribute access only for a limited set of safe names
}

# Set of safe built‑in functions that the user is allowed to call.
SAFE_BUILTINS = {
    'abs', 'round', 'min', 'max', 'sum',
    'len', 'sorted', 'list', 'tuple', 'dict', 'set',
}

# Names that are allowed to be accessed as attributes.
ALLOWED_ATTRIBUTES = {
    'math': {'sin', 'cos', 'tan', 'sqrt', 'log', 'pi', 'e'},
}

def _is_safe(node: ast.AST) -> bool:
    """
    Recursively verify that every node in the AST is part of the whitelist.
    """
    if type(node) not in SAFE_NODES:
        return False

    # For Call nodes, ensure that the function name is in SAFE_BUILTINS
    if isinstance(node, ast.Call):
        # Only allow direct name calls (no attribute calls)
        if not isinstance(node.func, ast.Name):
            return False
        if node.func.id not in SAFE_BUILTINS:
            return False

    # For Attribute nodes, ensure the attribute is allowed for that module
    if isinstance(node, ast.Attribute):
        # Only allow attributes on a Name (e.g., math.sin)
        if not isinstance(node.value, ast.Name):
            return False
        module_name = node.value.id
        if module_name not in ALLOWED_ATTRIBUTES:
            return False
        if node.attr not in ALLOWED_ATTRIBUTES[module_name]:
            return False

    # Recurse into children
    for child in ast.iter_child_nodes(node):
        if not _is_safe(child):
            return False
    return True

def evaluate_user_code(code_string: str) -> str:
    """
    Evaluate a user supplied Python expression in a highly restricted
    environment.  If the code contains unsafe constructs or an exception
    occurs, return 'Unsafe Code Detected!'.

    Parameters:
        code_string (str): The expression to evaluate.

    Returns:
        str: The string representation of the result, or an error message.
    """
    try:
        # Parse the expression
        parsed = ast.parse(code_string, mode='eval')
    except SyntaxError:
        return 'Unsafe Code Detected!'

    # Ensure the parsed AST only contains allowed nodes
    if not _is_safe(parsed):
        return 'Unsafe Code Detected!'

    # Prepare a safe globals dictionary
    safe_globals = {
        '__builtins__': {name: __builtins__[name] for name in SAFE_BUILTINS if name in __builtins__},
        'math': __import__('math'),
    }

    try:
        result = eval(compile(parsed, filename='<user_code>', mode='eval'), safe_globals, {})
        return str(result)
    except Exception:
        return 'Unsafe Code Detected!'