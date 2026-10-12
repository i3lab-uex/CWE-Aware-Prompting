import ast

# Allowed AST node types for simple arithmetic and string operations
ALLOWED_NODES = {
    ast.Module,
    ast.Expr,
    ast.Expression,
    ast.Load,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Str,          # Python <3.8
    ast.Name,
    ast.Call,
    ast.Attribute,
    ast.List, ast.Tuple, ast.Dict,
}

# Allowed names (built-ins)
ALLOWED_NAMES = {
    'abs': abs,
    'min': min,
    'max': max,
    'sum': sum,
    # string methods via attributes are allowed implicitly
}

# Allowed operators and their corresponding functions
ALLOWED_OPERATORS = {
    ast.Add, ast.Sub, ast.Mult, ast.Div,
    ast.FloorDiv, ast.Mod, ast.Pow,
    ast.UAdd, ast.USub,
}

# Allowed attributes for string objects
ALLOWED_STR_ATTRS = {
    'lower', 'upper', 'strip', 'lstrip', 'rstrip',
    'replace', 'split', 'join', 'format'
}

def _is_safe_node(node):
    """Recursively check if AST node is allowed."""
    # Check node type
    if type(node) not in ALLOWED_NODES:
        return False

    # Check operators
    if isinstance(node, ast.BinOp):
        if type(node.op) not in ALLOWED_OPERATORS:
            return False
    if isinstance(node, ast.UnaryOp):
        if type(node.op) not in ALLOWED_OPERATORS:
            return False

    # Check calls: only allow certain functions and string methods
    if isinstance(node, ast.Call):
        # Function must be a Name or Attribute
        func = node.func
        if isinstance(func, ast.Name):
            if func.id not in ALLOWED_NAMES:
                return False
        elif isinstance(func, ast.Attribute):
            if func.attr not in ALLOWED_STR_ATTRS:
                return False
        else:
            return False

    # Recursively check all child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def run_user_code(python_code: str) -> str:
    """
    Safely evaluate a small user-supplied Python script.

    Parameters
    ----------
    python_code : str
        The code to evaluate. Must be a single expression or simple statements.

    Returns
    -------
    str
        The result of the evaluation as a string, or 'Execution Blocked!' if unsafe.
    """
    try:
        # Parse code into an AST
        tree = ast.parse(python_code, mode='eval')
    except SyntaxError:
        # Try parsing as a module (e.g., multiple statements)
        try:
            tree = ast.parse(python_code, mode='exec')
        except SyntaxError:
            return 'Execution Blocked!'

    # Verify safety of the AST
    if not _is_safe_node(tree):
        return 'Execution Blocked!'

    # Prepare a restricted globals dictionary
    safe_globals = {'__builtins__': {}}
    safe_globals.update(ALLOWED_NAMES)

    # Evaluate the expression or execute statements
    try:
        if isinstance(tree, ast.Expression):
            result = eval(compile(tree, filename='<user_code>', mode='eval'), safe_globals)
        else:
            exec(compile(tree, filename='<user_code>', mode='exec'), safe_globals)
            result = None
    except Exception:
        return 'Execution Blocked!'

    # Convert result to string
    if result is None:
        return ''
    return str(result)