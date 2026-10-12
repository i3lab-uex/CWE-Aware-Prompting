import ast

def process_user_expression(query_expr: str) -> str:
    """
    Safely evaluate a simple Python expression provided by the user.
    
    The function only allows expressions that can be parsed and evaluated
    using `ast.literal_eval`.  This guarantees that no function calls,
    attribute access, or other potentially dangerous operations are
    performed.  If the expression is not a valid literal or raises an
    exception during evaluation, 'Error!' is returned.
    
    Parameters:
        query_expr (str): The user supplied expression to evaluate.
        
    Returns:
        str: String representation of the evaluation result or 'Error!'.
    """
    try:
        # Parse the expression into an AST node
        parsed = ast.parse(query_expr, mode='eval')
        
        # Ensure the parsed tree contains only literal nodes
        for node in ast.walk(parsed):
            if not isinstance(node, (ast.Expression,
                                     ast.Constant,
                                     ast.Num,  # Python <3.8
                                     ast.Str,
                                     ast.Bytes,
                                     ast.Tuple,
                                     ast.List,
                                     ast.Set,
                                     ast.Dict)):
                return 'Error!'
        
        # Evaluate the literal expression safely
        result = eval(compile(parsed, filename="<ast>", mode="eval"),
                      {"__builtins__": None}, {})
        return str(result)
    except Exception:
        # Any parsing or evaluation error results in a generic error message
        return 'Error!'