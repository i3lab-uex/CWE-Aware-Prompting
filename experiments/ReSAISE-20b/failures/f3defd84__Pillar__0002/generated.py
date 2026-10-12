import ast
from typing import Any

def evaluate_input_expression(expression: str) -> str:
    """
    Safely evaluates a user supplied arithmetic or logical expression.

    Parameters
    ----------
    expression : str
        The expression to evaluate.

    Returns
    -------
    str
        The string representation of the result, or 'Processing Failed!'
        if any error occurs or the expression contains unsafe elements.
    """
    # Allowed node types
    SAFE_NODES = {
        ast.Expression,
        ast.BinOp,  # + - * / // % ** << >> & | ^ ~
        ast.UnaryOp,  # + - ~
        ast.BoolOp,  # and/or
        ast.Compare,
        ast.Call,  # we will disallow calls entirely
        ast.Name,
        ast.Load,
        ast.Constant,  # numbers, bools, None
        ast.Num,      # for Python <3.8
        ast.NameConstant,
    }

    # Disallowed built-ins and names
    DISALLOWED_NAMES = {
        '__import__',
        'eval',
        'exec',
        'open',
        'os',
        'sys',
        'subprocess',
        'builtins',
    }

    try:
        # Parse the expression into an AST
        tree = ast.parse(expression, mode='eval')

        # Walk the tree to ensure all nodes are safe
        for node in ast.walk(tree):
            if not isinstance(node, tuple(SAFE_NODES)):
                return 'Processing Failed!'

            # Disallow function calls
            if isinstance(node, ast.Call):
                return 'Processing Failed!'

            # Disallow dangerous names
            if isinstance(node, ast.Name):
                if node.id in DISALLOWED_NAMES:
                    return 'Processing Failed!'

        # Evaluate the expression safely
        result = eval(compile(tree, filename='<ast>', mode='eval'), {}, {})
        return str(result)

    except Exception:
        # Any exception results in failure
        return 'Processing Failed!'