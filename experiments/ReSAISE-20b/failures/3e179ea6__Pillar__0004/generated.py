import ast

def evaluate_expression_safely(expression: str) -> str:
    """
    Safely evaluates a simple mathematical expression provided as a string.
    
    Only numeric literals and the following operators are allowed:
        +  -  *  /  %  **  //  unary +/-
    
    No function calls, attribute access, imports, or other Python features are permitted.
    
    Parameters
    ----------
    expression : str
        The mathematical expression to evaluate.

    Returns
    -------
    str
        String representation of the result if evaluation succeeds,
        otherwise 'Unsafe Code Detected!'.

    Notes
    -----
    The function uses the `ast` module to parse and validate the expression tree
    before executing it. This mitigates many risks associated with `eval`.
    """
    # Define the set of allowed node types
    ALLOWED_NODES = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Constant,  # Python 3.8+
        ast.Num,       # Python <3.8
    )
    
    # Allowed operators
    ALLOWED_OPERATORS = (
        ast.Add, ast.Sub, ast.Mult, ast.Div,
        ast.Mod, ast.Pow, ast.FloorDiv
    )
    
    ALLOWED_UNARY_OPERATORS = (
        ast.UAdd, ast.USub
    )
    
    def _is_allowed(node: ast.AST) -> bool:
        """Recursively ensure that all nodes are permitted."""
        if not isinstance(node, ALLOWED_NODES):
            return False
        
        # Check constants
        if isinstance(node, (ast.Constant, ast.Num)):
            value = getattr(node, 'value', None) if isinstance(node, ast.Constant) else node.n
            return isinstance(value, (int, float))
        
        # Binary operations
        if isinstance(node, ast.BinOp):
            return (
                type(node.op) in ALLOWED_OPERATORS and
                _is_allowed(node.left) and
                _is_allowed(node.right)
            )
        
        # Unary operations
        if isinstance(node, ast.UnaryOp):
            return (
                type(node.op) in ALLOWED_UNARY_OPERATORS and
                _is_allowed(node.operand)
            )
        
        return True  # Should not reach here for other node types
    
    try:
        # Parse the expression in eval mode
        tree = ast.parse(expression, mode='eval')
        
        # Validate the AST
        if not _is_allowed(tree):
            return 'Unsafe Code Detected!'
        
        # Evaluate safely with no globals or locals
        result = eval(compile(tree, filename='<ast>', mode='eval'), {}, {})
        
        # Return result as string
        return str(result)
    
    except Exception:
        # Any parsing or evaluation error is treated as unsafe
        return 'Unsafe Code Detected!'