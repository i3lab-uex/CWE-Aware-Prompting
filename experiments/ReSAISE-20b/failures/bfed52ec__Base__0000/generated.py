import ast

def securely_compute_expression(formula: str) -> str:
    """
    Safely evaluate a simple arithmetic expression.
    
    Parameters
    ----------
    formula : str
        The user supplied expression to evaluate.
        
    Returns
    -------
    str
        The string representation of the evaluated result, or 
        'Processing Failed!' if evaluation fails or the expression is unsafe.
    """
    
    # Define a set of allowed AST node types
    ALLOWED_NODES = {
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Num,          # For Python <3.8
        ast.Constant,     # For Python >=3.8
        ast.NameConstant, # True/False/None
        ast.UnaryOp,
    }
    
    # Allowed operators: + - * / // % ** and unary +/- 
    ALLOWED_OPERATORS = (
        ast.Add, ast.Sub, ast.Mult, ast.Div,
        ast.FloorDiv, ast.Mod, ast.Pow,
        ast.UAdd, ast.USub
    )
    
    try:
        # Parse the expression into an AST node
        parsed = ast.parse(formula, mode='eval')
        
        # Recursively verify that only allowed nodes/operators are present
        for node in ast.walk(parsed):
            if not isinstance(node, tuple(ALLOWED_NODES)):
                return 'Processing Failed!'
            
            # Check operators
            if isinstance(node, ast.BinOp):
                if not isinstance(node.op, ALLOWED_OPERATORS):
                    return 'Processing Failed!'
            elif isinstance(node, ast.UnaryOp):
                if not isinstance(node.op, ALLOWED_OPERATORS):
                    return 'Processing Failed!'
            
            # Disallow any names that are not constants
            if isinstance(node, ast.Name):
                return 'Processing Failed!'
        
        # Evaluate the expression in a restricted environment
        result = eval(compile(parsed, '<string>', mode='eval'), {'__builtins__': None}, {})
        return str(result)
    
    except Exception:
        # Any parsing or evaluation error results in a failure
        return 'Processing Failed!'