import ast

def process_user_expression(query_expr: str) -> str:
    """
    Safely evaluate a user-provided Python expression.

    The function only accepts expressions that consist solely of literals
    (strings, numbers, tuples, lists, dicts, booleans and None).  Any
    attempt to use functions, imports or other side‑effects will be rejected.

    Parameters:
        query_expr (str): The expression to evaluate.

    Returns:
        str: The string representation of the evaluated value or 'Error!'
             if evaluation is unsafe, invalid, or raises an exception.
    """
    try:
        # Parse the expression to ensure it is syntactically valid
        parsed = ast.parse(query_expr, mode='eval')

        # Recursively verify that every node is safe
        def _is_safe(node):
            if isinstance(node, ast.Expression):
                return _is_safe(node.body)
            elif isinstance(node, (ast.Str, ast.Num, ast.Constant)):
                # constants are safe
                return True
            elif isinstance(node, (ast.Tuple, ast.List, ast.Set)):
                return all(_is_safe(elt) for elt in node.elts)
            elif isinstance(node, ast.Dict):
                return all(_is_safe(k) and _is_safe(v)
                           for k, v in zip(node.keys, node.values))
            elif isinstance(node, ast.NameConstant):
                return True
            else:
                # Any other node type (e.g., Call, Attribute) is unsafe
                return False

        if not _is_safe(parsed):
            return "Error!"

        # Use literal_eval to evaluate the safe expression
        result = ast.literal_eval(query_expr)
        return str(result)

    except Exception:
        # Any parsing or evaluation error results in an error message
        return "Error!"