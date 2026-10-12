import ast

def execute_user_input(user_input: str) -> str:
    """
    Safely evaluate a simple arithmetic or literal expression supplied by the user.
    
    Parameters
    ----------
    user_input : str
        The user-provided expression to evaluate.
    
    Returns
    -------
    str
        String representation of the evaluated result or 'Processing Failed!' on error.
    
    Notes
    -----
    Only Python expressions that are syntactically valid and consist of literals,
    arithmetic operations, comparisons, boolean logic, and simple function calls
    to a whitelisted set of built-in functions are allowed. All other constructs
    (attribute access, imports, etc.) will raise a ValueError and result in the
    failure message.
    """
    # Strip whitespace to avoid accidental leading/trailing spaces
    expr = user_input.strip()
    
    if not expr:
        return "Processing Failed!"
    
    # Define a whitelist of safe built-in functions
    SAFE_BUILTINS = {
        "abs": abs,
        "round": round,
        "min": min,
        "max": max,
        "sum": sum,
    }
    
    # Helper to recursively validate AST nodes
    def _validate(node: ast.AST) -> bool:
        """
        Recursively walk the AST and ensure only allowed node types are present.
        Returns True if safe, False otherwise.
        """
        # Allowed literal nodes
        allowed_nodes = (
            ast.Expression,
            ast.BinOp,
            ast.UnaryOp,
            ast.Num,  # Python <3.8
            ast.Constant,  # Python >=3.8
            ast.BoolOp,
            ast.Compare,
            ast.Name,
            ast.Call,
            ast.Load,
        )
        
        if not isinstance(node, allowed_nodes):
            return False
        
        # For Name nodes, only allow safe built-ins
        if isinstance(node, ast.Name):
            return node.id in SAFE_BUILTINS
        
        # For Call nodes, ensure the function is a safe builtin
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                return False
            if node.func.id not in SAFE_BUILTINS:
                return False
        
        # Recursively validate child nodes
        for child in ast.iter_child_nodes(node):
            if not _validate(child):
                return False
        return True
    
    try:
        # Parse the expression into an AST node
        parsed = ast.parse(expr, mode="eval")
        
        # Validate the AST for safety
        if not _validate(parsed):
            return "Processing Failed!"
        
        # Compile the AST into a code object
        compiled = compile(parsed, "<string>", "eval")
        
        # Evaluate in a restricted environment
        result = eval(compiled, {"__builtins__": None}, SAFE_BUILTINS)
        
        return str(result)
    
    except Exception:
        # Any parsing, validation, or evaluation error results in failure
        return "Processing Failed!"