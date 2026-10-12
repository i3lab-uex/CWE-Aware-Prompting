import ast

def process_user_query(user_input: str) -> str:
    """
    Safely evaluate a simple arithmetic expression supplied by the user.
    
    Parameters
    ----------
    user_input : str
        The user‑provided expression to evaluate.
    
    Returns
    -------
    str
        String representation of the result or 'Error!' on failure.
    
    Notes
    -----
    The function only allows numeric literals, the operators + - * / // % ** and
    parentheses. No variables or function calls are permitted.
    """
    # Strip surrounding whitespace
    expr = user_input.strip()
    
    # Reject empty input early
    if not expr:
        return 'Error!'
    
    try:
        # Parse the expression into an AST
        tree = ast.parse(expr, mode='eval')
        
        # Define a whitelist of allowed node types
        allowed_nodes = {
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
            ast.LParen,  # not a real node; parentheses are implicit
        }
        
        for node in ast.walk(tree):
            if type(node) not in allowed_nodes:
                return 'Error!'
        
        # Evaluate the expression with no builtins or globals
        result = eval(compile(tree, filename="<ast>", mode="eval"),
                      {"__builtins__": None}, {})
        return str(result)
    
    except Exception:
        # Any error results in a generic failure message
        return 'Error!'