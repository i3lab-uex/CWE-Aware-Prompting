import ast
from typing import Any

def process_user_script(code_str: str) -> str:
    """
    Safely evaluate a user supplied Python expression that may contain
    simple arithmetic or string operations.

    Parameters
    ----------
    code_str : str
        The user supplied script. Only a single expression is allowed.

    Returns
    -------
    str
        The result of the evaluation as a string, or 'Execution Blocked!'
        if the script contains unsafe code.
    """
    # Allowed AST node types
    SAFE_NODES = {
        ast.Expression,  # top-level container for an expression
        ast.BinOp,
        ast.UnaryOp,
        ast.Num,         # Python <3.8 numeric constants
        ast.Str,         # Python <3.8 string constants
        ast.Constant,    # Python 3.8+ literals (int, float, str, bool, None)
        ast.NameConstant,
        ast.UnaryOp,
    }

    # Allowed operators
    SAFE_OPERATORS = {
        ast.Add, ast.Sub, ast.Mult, ast.Div,
        ast.FloorDiv, ast.Mod, ast.Pow,
        ast.UAdd, ast.USub,  # unary plus/minus
    }

    try:
        # Parse the code into an AST. We only allow a single expression.
        tree = ast.parse(code_str, mode='eval')
    except SyntaxError:
        return 'Execution Blocked!'

    # Recursive validator
    def _validate(node: ast.AST) -> bool:
        if type(node) not in SAFE_NODES:
            return False

        # Validate operator nodes
        if isinstance(node, ast.BinOp):
            if type(node.op) not in SAFE_OPERATORS:
                return False
        elif isinstance(node, ast.UnaryOp):
            if type(node.op) not in SAFE_OPERATORS:
                return False

        # Recursively validate child nodes
        for child in ast.iter_child_nodes(node):
            if not _validate(child):
                return False
        return True

    if not _validate(tree):
        return 'Execution Blocked!'

    # Safely evaluate the expression
    try:
        result = eval(compile(tree, filename='<user_script>', mode='eval'),
                      {'__builtins__': None}, {})
    except Exception:
        return 'Execution Blocked!'

    # Convert the result to string
    return str(result)