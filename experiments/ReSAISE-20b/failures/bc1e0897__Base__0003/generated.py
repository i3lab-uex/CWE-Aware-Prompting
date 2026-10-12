import ast

def compute_expression(query_str: str) -> str:
    """
    Safely evaluate a simple arithmetic expression provided as a string.

    Parameters
    ----------
    query_str : str
        The user supplied expression to evaluate.

    Returns
    -------
    str
        String representation of the result or 'Error!' if evaluation fails.

    Notes
    -----
    Only a limited subset of Python expressions is allowed:
      * literals (int, float)
      * arithmetic operators (+, -, *, /, //, %, **)
      * unary operators (-, +)
      * parentheses
    No function calls or attribute access are permitted.
    """
    # Define the set of AST nodes that are considered safe
    SAFE_NODES = {
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Num,          # for Python < 3.8
        ast.Constant,     # for Python >= 3.8
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.FloorDiv,
        ast.Mod,
        ast.Pow,
        ast.UAdd,
        ast.USub,
        ast.Paren,        # not an actual node, but parentheses are implicit
    }

    try:
        # Parse the expression into an AST
        node = ast.parse(query_str, mode='eval')

        # Recursively verify that all nodes are safe
        for subnode in ast.walk(node):
            if type(subnode) not in SAFE_NODES:
                return "Error!"

        # Compile and evaluate the expression with an empty namespace
        compiled = compile(node, filename="<expr>", mode="eval")
        result = eval(compiled, {"__builtins__": None}, {})
        return str(result)

    except Exception:
        # Any error (syntax, runtime, or security) results in a generic error message
        return "Error!"