import ast
from typing import Any

def execute_user_input(user_code: str) -> str:
    """
    Safely evaluate a user supplied Python expression containing only
    simple arithmetic and string operations.

    Parameters
    ----------
    user_code : str
        The Python expression to evaluate.

    Returns
    -------
    str
        Result of the evaluation converted to a string, or 'Execution Blocked!'
        if the code contains unsafe constructs.

    Notes
    -----
    Only a restricted subset of AST nodes are allowed:
        - Expressions (BinOp, UnaryOp, BoolOp, Compare)
        - Literals (Num, Str, Constant)
        - Name nodes that refer to allowed builtins ('abs', 'min', 'max',
          'len', 'sum', etc.) – currently none are allowed.
        - Operators: Add, Sub, Mult, Div, Mod, Pow, FloorDiv,
          And, Or, Not, Eq, NotEq, Lt, LtE, Gt, GtE
    All other nodes result in blocking the execution.
    """
    # Define allowed node types
    ALLOWED_NODES = (
        ast.Expression,
        ast.Module,
        ast.Expr,
        ast.BinOp,
        ast.UnaryOp,
        ast.BoolOp,
        ast.Compare,
        ast.Call,  # but we will restrict calls further
        ast.Name,
        ast.Constant,
        ast.Num,   # for Python <3.8
        ast.Str,   # for Python <3.8
        ast.List,
        ast.Tuple,
    )

    ALLOWED_OPERATORS = (
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod,
        ast.Pow, ast.FloorDiv,
        ast.And, ast.Or, ast.Not,
        ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    )

    # Only allow a very small set of builtins (none for now)
    SAFE_BUILTINS = {}

    # Helper to walk the AST and validate nodes
    def _validate(node: ast.AST) -> bool:
        if not isinstance(node, ALLOWED_NODES):
            return False
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.operator) or isinstance(child, ast.unaryop) or isinstance(child, ast.boolop):
                if not isinstance(child, ALLOWED_OPERATORS):
                    return False
            if isinstance(child, ast.Call):
                # disallow any function calls
                return False
            if isinstance(child, ast.Name):
                # disallow variable names
                return False
            if not _validate(child):
                return False
        return True

    try:
        # Parse the code into an AST
        parsed = ast.parse(user_code, mode='eval')
    except SyntaxError:
        return 'Execution Blocked!'

    if not _validate(parsed):
        return 'Execution Blocked!'

    try:
        # Evaluate safely
        result = eval(compile(parsed, filename='<user_code>', mode='eval'),
                      {'__builtins__': SAFE_BUILTINS}, {})
    except Exception:
        return 'Execution Blocked!'

    return str(result)