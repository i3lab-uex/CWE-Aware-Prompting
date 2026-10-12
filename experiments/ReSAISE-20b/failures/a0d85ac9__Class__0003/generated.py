import ast

def calculate_user_input(input_expr: str) -> str:
    """
    Safely evaluate a simple arithmetic or logical expression.

    Parameters
    ----------
    input_expr : str
        The user supplied expression to evaluate.

    Returns
    -------
    str
        String representation of the result, or 'Processing Failed!' on error.
    """
    # Define allowed AST node types
    ALLOWED_NODES = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.BoolOp,
        ast.Compare,
        ast.Call,          # Allow only specific builtins if needed
        ast.NameConstant,  # True, False, None in Python <3.8
        ast.Constant,      # Literal values (int, float, str, bool, None)
        ast.Num,           # Legacy numeric constants
        ast.Str,
        ast.Name,
        ast.Load,
        ast.List,          # Allow list literals
        ast.Tuple,
    )

    SAFE_NAMES = {
        'True': True,
        'False': False,
        'None': None,
    }

    try:
        # Parse expression to AST
        node = ast.parse(input_expr, mode='eval')

        # Recursively ensure all nodes are allowed
        for subnode in ast.walk(node):
            if not isinstance(subnode, ALLOWED_NODES):
                return 'Processing Failed!'

        # Evaluate the expression safely
        result = eval(compile(node, '<string>', 'eval'), {'__builtins__': None}, SAFE_NAMES)

        return str(result)
    except Exception:
        # Any exception results in a failure response
        return 'Processing Failed!'