import ast
from typing import Any

# List of AST node types that are considered unsafe
UNSAFE_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Exec,           # exec() in Python 2 (kept for completeness)
    ast.Call,
}

# List of function names that are disallowed
DISALLOWED_FUNCS = {
    'eval',
    'exec',
    'compile',
    '__import__',
    'open',
    'input',
    'os',   # os module attributes accessed via attribute lookup
}

# Simple whitelist of allowed builtins for eval
ALLOWED_BUILTINS = {
    'abs', 'all', 'any', 'bool', 'dict', 'float', 'int',
    'len', 'list', 'max', 'min', 'pow', 'range', 'round',
    'sum', 'tuple', 'str', 'chr', 'ord', 'reversed',
    # math functions
    'math': __import__('math'),
}

def _is_safe(node: ast.AST) -> bool:
    """
    Recursively check that the AST contains only safe nodes.
    """
    if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
        return False

    # Disallow function calls to unsafe functions
    if isinstance(node, ast.Call):
        func = node.func
        # Handle attribute access like math.sqrt
        if isinstance(func, ast.Attribute):
            # Allow attributes of whitelisted modules only
            if isinstance(func.value, ast.Name) and func.value.id in ALLOWED_BUILTINS:
                return True
            else:
                return False
        if isinstance(func, ast.Name):
            if func.id in DISALLOWED_FUNCS:
                return False
        # Otherwise allow the call (e.g., len, sum)
    if isinstance(node, ast.Name):
        # Disallow names that are not in allowed builtins
        if node.id not in ALLOWED_BUILTINS:
            return False

    for child in ast.iter_child_nodes(node):
        if not _is_safe(child):
            return False
    return True

def evaluate_user_code(code_string: str) -> str:
    """
    Safely evaluates a Python expression provided as a string.

    Parameters
    ----------
    code_string : str
        The user supplied Python expression to evaluate.

    Returns
    -------
    str
        String representation of the evaluation result, or an error message.
    """
    try:
        # Parse code into AST
        tree = ast.parse(code_string, mode='eval')
    except SyntaxError:
        return 'Unsafe Code Detected!'

    # Check safety of the parsed AST
    if not _is_safe(tree):
        return 'Unsafe Code Detected!'

    # Prepare safe evaluation environment
    safe_globals = {name: obj for name, obj in ALLOWED_BUILTINS.items() if not isinstance(obj, type)}
    safe_globals.update({'__builtins__': {name: __builtins__[name] for name in ALLOWED_BUILTINS if isinstance(name, str)}})

    try:
        result = eval(compile(tree, filename='<user_code>', mode='eval'), safe_globals, {})
        return str(result)
    except Exception:
        return 'Unsafe Code Detected!'