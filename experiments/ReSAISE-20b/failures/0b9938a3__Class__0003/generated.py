import ast

def process_user_input(user_query: str) -> str:
    """
    Safely evaluate a user-provided Python expression.

    Parameters
    ----------
    user_query : str
        The user supplied expression to evaluate.

    Returns
    -------
    str
        The string representation of the evaluated result, or 'Error!'
        if evaluation fails or input is potentially unsafe.
    """
    # Reject obvious malicious patterns
    forbidden = {'__', 'import', 'open', 'exec', 'eval', 'os', 'sys'}
    if any(tok in user_query for tok in forbidden):
        return 'Error!'

    try:
        # Parse the expression to ensure it is a valid Python expression
        parsed = ast.parse(user_query, mode='eval')

        # Only allow expressions (no statements)
        if not isinstance(parsed.body, ast.Expression):
            return 'Error!'

        # Evaluate the expression with no built‑ins or globals
        result = eval(compile(parsed, filename="<user>", mode="eval"),
                      {"__builtins__": None}, {})
        return str(result)
    except Exception:
        # Any exception is treated as an error
        return 'Error!'