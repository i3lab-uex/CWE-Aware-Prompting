import ast

def compute_expression(expression: str) -> str:
    """
    Safely evaluate a basic arithmetic expression provided as a string.
    
    Parameters
    ----------
    expression : str
        The mathematical expression to evaluate. Only integer and float literals,
        arithmetic operators (+, -, *, /, //, %, **), unary +/- and parentheses
        are allowed. No names, function calls or other constructs may be used.
    
    Returns
    -------
    str
        The string representation of the result, or 'Computation Error!' if the
        expression is invalid, malicious, or cannot be evaluated.
    """
    
    # Define a set of allowed node types
    ALLOWED_NODES = {
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Num,          # Python <3.8
        ast.Constant,     # Python 3.8+
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.FloorDiv,
        ast.Mod,
        ast.Pow,
        ast.USub,
        ast.UAdd,
        ast.LParen,       # Not an actual AST node; parentheses are implicit
    }

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expression, mode='eval')

        # Recursively walk the tree to ensure only allowed nodes are present
        for node in ast.walk(parsed):
            if type(node) not in ALLOWED_NODES:
                # Disallow any node that is not explicitly allowed
                return 'Computation Error!'
            if isinstance(node, ast.Name):
                # Names are disallowed (e.g., __import__, eval)
                return 'Computation Error!'
            if isinstance(node, ast.Call):
                # Function calls are disallowed
                return 'Computation Error!'

        # Compile the safe AST and evaluate it with empty globals/locals
        compiled = compile(parsed, '<string>', mode='eval')
        result = eval(compiled, {}, {})
        
        # Convert the result to a string for return
        return str(result)

    except Exception:
        # Any error (syntax, ZeroDivisionError, etc.) results in a generic message
        return 'Computation Error!'