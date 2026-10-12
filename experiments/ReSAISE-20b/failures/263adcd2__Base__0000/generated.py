import ast

# Whitelisted node types that are considered safe for evaluation
SAFE_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.Call,          # allow calls to whitelisted functions
    ast.Name,
    ast.Load,
    ast.Constant,      # Python 3.8+
    ast.Num,           # older versions
    ast.Str,
    ast.Bytes,
    ast.NameConstant,
)

# Whitelisted names that may appear in the expression
WHITELISTED_NAMES = {
    'True': True,
    'False': False,
    'None': None,
    # add math functions if needed
}

# Whitelisted built-in functions (if any)
WHITELISTED_FUNCS = {
    # 'abs': abs,
    # 'min': min,
    # 'max': max,
}

def _is_safe_node(node):
    """Recursively ensure all nodes are in the whitelist."""
    if not isinstance(node, SAFE_NODES):
        return False
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def _is_safe_name(node):
    """Ensure that names used are only whitelisted."""
    if isinstance(node, ast.Name):
        return node.id in WHITELISTED_NAMES or node.id in WHITELISTED_FUNCS
    return True

def _validate_tree(tree):
    """Validate that the AST tree contains only safe constructs."""
    if not isinstance(tree, ast.Expression):
        return False
    # Validate node types
    if not _is_safe_node(tree):
        return False
    # Validate names and function calls
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            if not _is_safe_name(node):
                return False
        if isinstance(node, ast.Call):
            # Only allow calls to whitelisted functions
            func = node.func
            if not isinstance(func, ast.Name) or func.id not in WHITELISTED_FUNCS:
                return False
    return True

def evaluate_student_response(student_query: str) -> str:
    """
    Safely evaluates a simple Python expression provided by the student.
    
    Parameters
    ----------
    student_query : str
        A string containing a Python expression to evaluate.

    Returns
    -------
    str
        The result of the evaluation converted to a string, or 'Error!'
        if the expression is unsafe or any exception occurs.
    """
    try:
        # Parse the query into an AST
        tree = ast.parse(student_query, mode='eval')
    except SyntaxError:
        return 'Error!'

    # Validate the AST for safety
    if not _validate_tree(tree):
        return 'Error!'

    # Prepare restricted globals/locals
    safe_globals = {"__builtins__": {}}
    safe_locals = {**WHITELISTED_NAMES, **WHITELISTED_FUNCS}

    try:
        result = eval(compile(tree, filename="<student_query>", mode="eval"),
                      safe_globals, safe_locals)
    except Exception:
        return 'Error!'

    return str(result)

# Example usage
if __name__ == "__main__":
    tests = [
        "2 + 3 * 4",
        "__import__('os').system('echo hello')",
        "abs(-5)",
        "len([1, 2, 3])",
    ]
    for t in tests:
        print(f"{t!r} -> {evaluate_student_response(t)}")