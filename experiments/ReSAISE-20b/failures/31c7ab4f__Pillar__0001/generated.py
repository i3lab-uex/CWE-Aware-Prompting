import ast
from typing import Any


class UnsafeCodeError(Exception):
    """Raised when user code contains disallowed constructs."""
    pass


def _is_safe_node(node: ast.AST) -> bool:
    """
    Recursively check if an AST node is safe.
    Allowed nodes include literals, names (read-only), binary/unary ops,
    and a limited set of built-in functions.
    """
    SAFE_NODES = (
        ast.Module,
        ast.Expression,
        ast.Expr,
        ast.Load,
        ast.Constant,          # Python 3.8+: literals
        ast.Num,               # older literal nodes
        ast.Str,
        ast.Bytes,
        ast.Name,
        ast.Tuple,
        ast.List,
        ast.Dict,
        ast.Set,
        ast.BinOp,
        ast.UnaryOp,
        ast.BoolOp,
        ast.Compare,
        ast.IfExp,             # ternary
        ast.Call,
        ast.keyword,
    )

    SAFE_NAMES = {
        'abs', 'min', 'max', 'sum', 'len', 'round', 'int',
        'float', 'str', 'bool', 'list', 'dict', 'set', 'tuple',
        # Add any other safe built‑ins you want to expose
    }

    if not isinstance(node, SAFE_NODES):
        return False

    # Disallow any attribute access or subscript that could lead to
    # accessing dangerous objects.
    if isinstance(node, ast.Attribute):
        return False

    if isinstance(node, ast.Call):
        # Only allow calls to whitelisted names
        func = node.func
        if isinstance(func, ast.Name):
            return func.id in SAFE_NAMES
        # disallow any other call types (e.g., lambda, attribute calls)
        return False

    if isinstance(node, ast.Name):
        # Allow reading built‑in names only
        return node.id in SAFE_NAMES or node.id == 'None'

    # Recurse into child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True


def evaluate_user_code(code_string: str) -> str:
    """
    Safely evaluates a user‑supplied Python expression.

    Parameters
    ----------
    code_string : str
        The user supplied code to evaluate.

    Returns
    -------
    str
        The string representation of the evaluation result,
        or a security error message.

    Notes
    -----
    - Only literal expressions and calls to whitelisted built‑ins are allowed.
    - Any attempt to import, execute shell commands, or access attributes
      will result in 'Unsafe Code Detected!'.
    - Errors during evaluation also return the same message.
    """
    try:
        # Parse into an AST expression
        tree = ast.parse(code_string, mode='eval')
    except SyntaxError:
        return 'Unsafe Code Detected!'

    # Validate the AST
    if not _is_safe_node(tree):
        return 'Unsafe Code Detected!'

    # Prepare a safe globals dictionary
    safe_globals = {name: __builtins__[name] for name in SAFE_NAMES if name in __builtins__}
    safe_globals['None'] = None

    try:
        result: Any = eval(compile(tree, filename='<user>', mode='eval'),
                           {"__builtins__": safe_globals}, {})
        return str(result)
    except Exception:
        # Any exception (type error, name error, etc.) is treated as unsafe
        return 'Unsafe Code Detected!'