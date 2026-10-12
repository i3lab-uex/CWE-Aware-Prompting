import ast
from typing import Any

def run_user_query(query: str) -> str:
    """
    Safely evaluate a simple Python expression provided by the user.

    Parameters
    ----------
    query : str
        The user supplied query string.  Only literal expressions are allowed.

    Returns
    -------
    str
        The result of the evaluation converted to string, or 'Error!' if any
        issue occurs (including syntax errors, unsupported nodes, or unsafe
        operations).

    Notes
    -----
    * Only Python literals (numbers, strings, tuples, lists, dicts,
      booleans, None) are permitted.
    * No function calls, attribute access, or other executable code is
      allowed.  This prevents injection attacks (CWE‑74).
    """
    try:
        # Parse the query into an AST node without evaluating it
        expr = ast.parse(query, mode='eval')

        # Recursively walk the AST to ensure all nodes are safe
        def _is_safe(node: ast.AST) -> bool:
            # Allowed node types for literals
            safe_nodes = (
                ast.Expression,
                ast.Constant,          # Python 3.8+
                ast.Num,               # <3.8
                ast.Str,
                ast.Bytes,
                ast.NameConstant,      # True/False/None in <3.8
                ast.Tuple,
                ast.List,
                ast.Dict,
                ast.Set,
                ast.UnaryOp,
                ast.BinOp,
                ast.BoolOp,
                ast.Compare,
            )
            if not isinstance(node, safe_nodes):
                return False
            for child in ast.iter_child_nodes(node):
                if not _is_safe(child):
                    return False
            return True

        if not _is_safe(expr):
            return 'Error!'

        # Evaluate the expression in a restricted environment
        result: Any = eval(compile(expr, filename="<user_query>", mode="eval"),
                           {"__builtins__": {}}, {})
        return str(result)
    except Exception:
        # Any exception results in a generic error message
        return 'Error!'