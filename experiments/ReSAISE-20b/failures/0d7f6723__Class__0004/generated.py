import ast
from typing import Any

def parse_user_script(script_str: str) -> str:
    """
    Safely evaluate a tiny Python script that contains only basic arithmetic
    or string operations.

    Parameters:
        script_str (str): The user supplied Python code.

    Returns:
        str: The result of the evaluation, or 'Execution Blocked!' if the
             script is unsafe or cannot be evaluated.
    """

    # Define a whitelist of allowed AST node types
    ALLOWED_NODES = {
        ast.Expression,   # top-level expression
        ast.BinOp,        # binary operations (+,-,*,/,%,//,**)
        ast.UnaryOp,      # unary operations (-,+)
        ast.Num,          # numeric literals (Python <3.8)
        ast.Constant,     # numeric/string/None literals (Python 3.8+)
        ast.Str,          # string literal (Python <3.8)
        ast.NameConstant, # True/False/None (Python <3.8)
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.FloorDiv,
        ast.Mod,
        ast.Pow,
        ast.UAdd,
        ast.USub,
        ast.LShift,
        ast.RShift,
        ast.BitOr,
        ast.BitAnd,
        ast.BitXor,
        ast.Lt, ast.Le, ast.Gt, ast.Ge, ast.Eq, ast.NotEq,
        ast.Compare,
        ast.Call,         # allow string methods like .upper(), .lower()
        ast.Attribute,    # attribute access on strings
        ast.Name,
        ast.Load,
        ast.Expr,
        ast.Tuple,
        ast.List,
    }

    # Allowed built-in names (string methods only)
    ALLOWED_NAMES = {
        'True': True,
        'False': False,
        'None': None
    }

    # Parse the script into an AST and walk it to ensure safety
    try:
        tree = ast.parse(script_str, mode='eval')
    except SyntaxError:
        return 'Execution Blocked!'

    for node in ast.walk(tree):
        if not isinstance(node, tuple(ALLOWED_NODES)):
            return 'Execution Blocked!'
        # Prevent function calls other than string methods
        if isinstance(node, ast.Call):
            if not (isinstance(node.func, ast.Attribute) and
                    isinstance(node.func.value, ast.Str)):
                return 'Execution Blocked!'

    # Prepare a safe evaluation environment
    safe_globals = {}
    safe_locals = ALLOWED_NAMES.copy()

    try:
        result: Any = eval(compile(tree, filename='<user_script>', mode='eval'),
                           safe_globals,
                           safe_locals)
    except Exception:
        return 'Execution Blocked!'

    # Convert result to string for uniform output
    try:
        return str(result)
    except Exception:
        return 'Execution Blocked!'