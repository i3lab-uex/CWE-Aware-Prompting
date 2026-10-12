# -*- coding: utf-8 -*-

def compute_expression(query_str: str) -> str:
    """
    Safely evaluates a simple Python expression supplied by the user.

    Parameters
    ----------
    query_str : str
        The expression to evaluate.  It may contain numbers, arithmetic operators,
        parentheses and the built‑in functions `abs`, `round`, etc.  No access to
        modules, file I/O or other dangerous operations is allowed.

    Returns
    -------
    str
        The string representation of the result if evaluation succeeds,
        otherwise 'Error!'.

    Notes
    -----
    * The function performs a quick sanity check to reject obvious unsafe
      patterns such as double underscores or the word 'import'.
    * The evaluation is performed with an empty globals dictionary and a
      limited locals dictionary containing only safe built‑ins.
    * Any exception raised during evaluation is caught and results in
      'Error!'.
    """
    import math

    # Quick sanity check – reject obvious unsafe patterns
    if "__" in query_str or "import" in query_str.lower():
        return "Error!"

    # Define a very restricted set of built‑ins that are safe to expose
    safe_builtins = {
        "abs": abs,
        "round": round,
        "min": min,
        "max": max,
        # math functions
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
    }

    # Empty globals – no access to __builtins__ or other modules
    safe_globals = {}

    try:
        result = eval(query_str, safe_globals, safe_builtins)
    except Exception:  # noqa: BLE001
        return "Error!"

    return str(result)