import ast

# Define a whitelist of safe AST node types
SAFE_NODES = {
    'Module', 'Expr', 'Assign', 'Name', 'Load',
    'Store', 'Tuple', 'List', 'Constant',
    'BinOp', 'UnaryOp', 'BoolOp', 'Compare',
    'Add', 'Sub', 'Mult', 'Div', 'FloorDiv', 'Mod', 'Pow',
    'UAdd', 'USub', 'Not', 'And', 'Or',
    'Eq', 'NotEq', 'Lt', 'LtE', 'Gt', 'GtE',
    'IfExp',  # ternary
    'Call',   # limited to safe functions
}

# Whitelisted built-in functions and constants
SAFE_BUILTINS = {
    'abs': abs,
    'round': round,
    'min': min,
    'max': max,
    'sum': sum,
    'len': len,
    'str': str,
    'int': int,
    'float': float,
    'bool': bool,
}

def _is_safe(node):
    """Recursively check that all nodes are in the whitelist."""
    if type(node).__name__ not in SAFE_NODES:
        return False
    for child in ast.iter_child_nodes(node):
        if not _is_safe(child):
            return False
    return True

def execute_user_code(user_code: str) -> str:
    """
    Safely evaluate simple arithmetic or string expressions submitted by the user.
    
    Parameters
    ----------
    user_code : str
        The Python code submitted by the user. Only safe expressions are allowed.
    
    Returns
    -------
    str
        The string representation of the evaluated result, or 'Execution Blocked!' if
        unsafe operations are detected.
    """
    try:
        # Parse the code into an AST
        tree = ast.parse(user_code, mode='exec')
        
        # Ensure the entire tree is safe
        if not _is_safe(tree):
            return 'Execution Blocked!'
        
        # Compile the tree
        compiled = compile(tree, '<user_code>', 'exec')
        
        # Prepare a safe namespace
        safe_globals = {'__builtins__': SAFE_BUILTINS}
        safe_locals = {}
        
        # Execute the compiled code
        exec(compiled, safe_globals, safe_locals)
        
        # Retrieve the result from local variables
        # If a variable named 'result' is set, use it; otherwise, try the last expression
        if 'result' in safe_locals:
            return str(safe_locals['result'])
        
        # If the script was just an expression, evaluate it directly
        expr_tree = ast.parse(user_code, mode='eval')
        if not _is_safe(expr_tree):
            return 'Execution Blocked!'
        expr_compiled = compile(expr_tree, '<user_code>', 'eval')
        result = eval(expr_compiled, safe_globals, {})
        return str(result)
        
    except Exception:
        # Any exception (including syntax errors) leads to blocking
        return 'Execution Blocked!'