import ast

# Allowed node types for a safe subset of Python expressions.
SAFE_NODE_TYPES = {
    # Expressions
    ast.Expression,
    # Literals
    ast.Constant,  # for Python >=3.8 (covers int, float, str, bool, None)
    ast.Num,
    ast.Str,
    ast.Bytes,
    # Binary operations (+, -, *, /, //, %, **)
    ast.BinOp,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.FloorDiv,
    ast.Mod,
    ast.Pow,
    # Unary operations (+, -)
    ast.UnaryOp,
    ast.UAdd,
    ast.USub,
    # Comparisons
    ast.Compare,
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    # Boolean operations
    ast.BoolOp,
    ast.And,
    ast.Or,
    # Parentheses grouping
    ast.Paren,  # Not an actual node; parentheses are just grouping in the AST.
    # Name constants like True, False, None
    ast.NameConstant,
    # Tuple/list/tuple literals
    ast.Tuple,
    ast.List,
    # Indexing/slicing (allow only simple indexing)
    ast.Subscript,
    ast.Index,
    # Attribute access for built-in methods like str.upper()
    ast.Attribute,
}

# Whitelist of allowed names (functions, constants)
ALLOWED_NAMES = {
    'True': True,
    'False': False,
    'None': None,
    # math constants/functions
    'abs': abs,
    'round': round,
    'min': min,
    'max': max,
    # string methods (via attribute access)
}

def _is_safe_node(node: ast.AST) -> bool:
    """
    Recursively check that all nodes in the AST belong to SAFE_NODE_TYPES
    and that names/attributes are whitelisted.
    """
    if type(node) not in SAFE_NODE_TYPES:
        return False

    # Check for disallowed attribute names (e.g., __dict__, etc.)
    if isinstance(node, ast.Attribute):
        # Allow only simple attributes that are part of built-in string methods
        if not isinstance(node.value, (ast.Name, ast.Constant)):
            return False
        # Disallow any attribute that starts with underscore
        if node.attr.startswith('_'):
            return False

    # Check names: only allow whitelisted constants
    if isinstance(node, ast.Name):
        if node.id not in ALLOWED_NAMES:
            return False

    # Recursively check child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def execute_user_code(user_code: str) -> str:
    """
    Execute a small Python expression safely.

    Parameters
    ----------
    user_code : str
        A string containing a simple Python expression (arithmetic, string ops).

    Returns
    -------
    str
        The string representation of the evaluated result,
        or 'Execution Blocked!' if the code is unsafe.
    """
    try:
        # Parse expression only; disallow statements
        parsed = ast.parse(user_code, mode='eval')
    except SyntaxError:
        return 'Execution Blocked!'

    if not _is_safe_node(parsed):
        return 'Execution Blocked!'

    # Prepare a safe evaluation environment
    safe_globals = {'__builtins__': None}
    safe_locals = ALLOWED_NAMES.copy()

    try:
        result = eval(compile(parsed, '<string>', mode='eval'), safe_globals, safe_locals)
    except Exception:
        return 'Execution Blocked!'

    # Convert result to string for uniform output
    return str(result)

# Example usage:
if __name__ == "__main__":
    tests = [
        "2 + 3 * 4",
        "'hello'.upper() + ' world'",
        "__import__('os').system('echo unsafe')",
        "abs(-5)",
        "open('file.txt', 'w').write('test')",
    ]
    for code in tests:
        print(f"Input: {code!r} -> Output: {execute_user_code(code)!r}")