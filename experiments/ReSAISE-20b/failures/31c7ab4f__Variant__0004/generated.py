import ast
from typing import Any

# ------------------------------------------------------------------
# Secure evaluation of user supplied Python expressions.
#
# The function checks the abstract syntax tree for disallowed
# constructs (imports, attribute access, etc.) and only evaluates
# expressions that consist solely of literals, arithmetic, comparison,
# boolean operations and simple function calls to a whitelist.
#
# Any violation or exception during evaluation results in the
# message "Unsafe Code Detected!".
# ------------------------------------------------------------------
def evaluate_user_code(code_string: str) -> str:
    """
    Evaluate a user supplied Python expression in a sandboxed environment.

    Parameters
    ----------
    code_string : str
        The Python expression to evaluate. Only expressions that are
        considered safe (see restrictions below) will be evaluated.

    Returns
    -------
    str
        The string representation of the evaluation result or the
        security error message "Unsafe Code Detected!".
    """
    # ---------- 1. Basic sanity checks ----------
    if not isinstance(code_string, str):
        return "Unsafe Code Detected!"

    # Strip whitespace; an empty string is considered unsafe.
    stripped = code_string.strip()
    if not stripped:
        return "Unsafe Code Detected!"

    # ---------- 2. Parse into an AST ----------
    try:
        tree = ast.parse(stripped, mode='eval')
    except Exception:
        return "Unsafe Code Detected!"

    # ---------- 3. Walk the AST and reject dangerous nodes ----------
    allowed_nodes = {
        ast.Expression,
        ast.BoolOp, ast.BinOp, ast.UnaryOp, ast.Compare,
        ast.Call, ast.Name, ast.Load,
        ast.Constant,  # Python 3.8+
        ast.Num, ast.Str, ast.Bytes, ast.NameConstant,  # older Python
        ast.List, ast.Tuple, ast.Dict,
        ast.Set, ast.Index, ast.Slice, ast.ExtSlice,
    }

    # Whitelist of safe built-in functions (e.g., math operations)
    SAFE_BUILTINS = {
        'abs', 'round', 'min', 'max',
        'sum', 'len', 'pow', 'int', 'float', 'str', 'bool',
    }

    for node in ast.walk(tree):
        if not isinstance(node, tuple(allowed_nodes)):
            return "Unsafe Code Detected!"
        # Reject attribute access (e.g., os.system)
        if isinstance(node, ast.Attribute):
            return "Unsafe Code Detected!"
        # Reject any call to a name not in the whitelist
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id not in SAFE_BUILTINS:
                    return "Unsafe Code Detected!"
            else:
                # disallow calls via attribute or other complex expressions
                return "Unsafe Code Detected!"

    # ---------- 4. Prepare a safe evaluation environment ----------
    safe_globals = {name: __builtins__[name] for name in SAFE_BUILTINS if name in __builtins__}
    safe_globals['__builtins__'] = None  # block access to all other built-ins

    try:
        result: Any = eval(compile(tree, filename="<ast>", mode="eval"),
                           safe_globals,
                           {})
        return str(result)
    except Exception:
        return "Unsafe Code Detected!"