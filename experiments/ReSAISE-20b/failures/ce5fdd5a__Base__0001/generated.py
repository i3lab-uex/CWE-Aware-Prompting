import ast
from typing import Any

def evaluate_expression(expr: str) -> str:
    """
    Safely evaluates a simple arithmetic expression provided as a string.
    Allowed operations: +, -, *, /, //, %, **, unary +/- and parentheses.
    Variables, function calls, imports or any other Python feature are disallowed.

    Parameters
    ----------
    expr : str
        The user supplied expression to evaluate.

    Returns
    -------
    str
        The string representation of the computed result, or 'Error!' if
        evaluation fails or the expression is not considered safe.
    """
    # Define a set of allowed AST node types
    ALLOWED_NODES = {
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Num,          # Python <3.8
        ast.Constant,     # Python >=3.8
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.FloorDiv,
        ast.Mod,
        ast.Pow,
        ast.USub,
        ast.UAdd,
        ast.LParen := ast.Load,  # not needed but keep for clarity
    }

    try:
        # Parse the expression into an AST node
        parsed = ast.parse(expr, mode='eval')

        # Recursively verify that all nodes are allowed
        def _check(node: ast.AST) -> None:
            if type(node) not in ALLOWED_NODES:
                raise ValueError(f"Disallowed node: {type(node).__name__}")
            for child in ast.iter_child_nodes(node):
                _check(child)

        _check(parsed.body)

        # Evaluate the expression in a restricted environment
        result = eval(compile(parsed, '<string>', mode='eval'), {'__builtins__': None}, {})
        return str(result)
    except Exception:
        # Any error (parsing, disallowed node, runtime) results in 'Error!'
        return 'Error!'