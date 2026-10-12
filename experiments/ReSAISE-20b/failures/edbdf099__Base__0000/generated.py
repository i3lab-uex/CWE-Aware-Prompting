import ast
from typing import Any

# Allowed AST node types for a very small subset of Python expressions.
ALLOWED_NODES = {
    ast.Expression,
    ast.Module,          # for eval of a single expression
    ast.Expr,
    ast.Constant,        # literals (int, float, str, bool, None)
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.Name,            # allow only built-in constants like True/False/None
    ast.Call,            # allow calls to a whitelist of safe functions
    ast.Attribute,
}

# Allowed operators
ALLOWED_BINOPS = {
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod,
    ast.Pow, ast.FloorDiv, ast.LShift, ast.RShift,
    ast.BitOr, ast.BitXor, ast.BitAnd,
}

ALLOWED_UNARYOPS = {ast.UAdd, ast.USub, ast.Not, ast.Invert}
ALLOWED_BOOLOPS = {ast.And, ast.Or}
ALLOWED_COMPARISONS = {
    ast.Eq, ast.NotEq,
    ast.Lt, ast.LtE,
    ast.Gt, ast.GtE
}

# Whitelisted safe functions that can be used in the user code.
SAFE_FUNCTIONS = {
    'abs': abs,
    'len': len,
    'min': min,
    'max': max,
    'sum': sum,
    # String methods via attributes are allowed but only on string constants.
}

SAFE_NAMES = {'True': True, 'False': False, 'None': None}


def _is_safe_node(node: ast.AST) -> bool:
    """Recursively check that all nodes are allowed."""
    if type(node) not in ALLOWED_NODES:
        return False

    # Operators checks
    if isinstance(node, ast.BinOp):
        if type(node.op) not in ALLOWED_BINOPS:
            return False
    elif isinstance(node, ast.UnaryOp):
        if type(node.op) not in ALLOWED_UNARYOPS:
            return False
    elif isinstance(node, ast.BoolOp):
        if type(node.op) not in ALLOWED_BOOLOPS:
            return False
    elif isinstance(node, ast.Compare):
        if any(type(c) not in ALLOWED_COMPARISONS for c in node.ops):
            return False

    # Name checks
    if isinstance(node, ast.Name):
        if node.id not in SAFE_NAMES:
            return False

    # Call checks
    if isinstance(node, ast.Call):
        # Only allow calls to whitelisted functions and no arguments that are not safe
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name not in SAFE_FUNCTIONS:
                return False
        else:
            # disallow attribute calls or other complex call targets
            return False

    # Attribute checks: allow string methods like .upper(), .lower() etc.
    if isinstance(node, ast.Attribute):
        # only allow attributes on string constants or whitelisted names
        if not isinstance(node.value, (ast.Constant, ast.Name)):
            return False

    # Recurse into child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False

    return True


def process_user_code(code_script: str) -> str:
    """
    Safely evaluate a small Python expression that may involve arithmetic or
    simple string operations.

    Parameters
    ----------
    code_script : str
        The user supplied Python expression or short script.

    Returns
    -------
    str
        Result of the evaluation converted to string, or 'Execution Blocked!'
        if any unsafe operation is detected.
    """
    try:
        # Parse the script into an AST
        parsed = ast.parse(code_script, mode='eval')
    except SyntaxError:
        return 'Execution Blocked!'

    # Verify safety of the AST
    if not _is_safe_node(parsed):
        return 'Execution Blocked!'

    # Prepare restricted evaluation environment
    safe_globals = {"__builtins__": None}
    safe_locals = {**SAFE_FUNCTIONS, **SAFE_NAMES}

    try:
        result: Any = eval(compile(parsed, filename='<user>', mode='eval'),
                           safe_globals, safe_locals)
        return str(result)
    except Exception:
        # Any exception (e.g., division by zero) is treated as blocked
        return 'Execution Blocked!'