import ast

def evaluate_quiz_expression(quiz_expr: str) -> str:
    """
    Safely evaluates a user-provided Python expression.

    The function only permits safe arithmetic and boolean expressions.
    Any attempt to access disallowed attributes, call functions, or
    use unsafe constructs results in an 'Error!' return value.

    Parameters:
        quiz_expr (str): The expression to evaluate.

    Returns:
        str: The string representation of the result, or 'Error!' on failure.
    """
    # Define allowed node types
    ALLOWED_NODES = {
        ast.Expression, ast.BinOp, ast.UnaryOp, ast.BoolOp,
        ast.Compare, ast.Call, ast.NameConstant, ast.Num,
        ast.Str, ast.Bytes, ast.List, ast.Tuple, ast.Set, ast.Dict,
        ast.Name, ast.Load, ast.Constant
    }

    # Whitelist of safe built-in names (operators and constants)
    SAFE_NAMES = {
        'True': True,
        'False': False,
        'None': None,
    }

    # Whitelist of allowed functions/operators
    SAFE_FUNCTIONS = {}

    try:
        # Parse the expression into an AST
        tree = ast.parse(quiz_expr, mode='eval')

        # Recursively check node safety
        for node in ast.walk(tree):
            if not isinstance(node, tuple(ALLOWED_NODES)):
                return 'Error!'
            # Disallow any calls to functions
            if isinstance(node, ast.Call):
                return 'Error!'

        # Evaluate safely with restricted globals/locals
        result = eval(
            compile(tree, '<string>', mode='eval'),
            {'__builtins__': None},
            {**SAFE_NAMES, **SAFE_FUNCTIONS}
        )
        return str(result)
    except Exception:
        return 'Error!'