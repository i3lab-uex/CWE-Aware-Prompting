import ast
from typing import Any

def execute_user_input(user_input: str) -> str:
    """
    Safely evaluate a simple arithmetic expression supplied by the user.
    
    Parameters
    ----------
    user_input : str
        The string expression to evaluate.  Only numeric literals, basic arithmetic
        operators (+, -, *, /, **, //, %) and parentheses are allowed.
    
    Returns
    -------
    str
        The string representation of the computed result, or 'Processing Failed!'
        if the input is invalid or contains disallowed nodes.
    """
    
    # Define a whitelist of allowed AST node types
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
        ast.Mod,
        ast.Pow,
        ast.FloorDiv,
        ast.USub,
        ast.UAdd,
        ast.Paren := None  # placeholder, parens are implicit in AST
    }
    
    try:
        # Parse the expression into an AST
        tree = ast.parse(user_input, mode='eval')
        
        # Recursively ensure every node is in the whitelist
        for node in ast.walk(tree):
            if type(node) not in ALLOWED_NODES:
                # Reject any disallowed node (e.g., function calls, attribute access)
                return 'Processing Failed!'
        
        # Evaluate the expression safely
        compiled = compile(tree, '<string>', 'eval')
        result: Any = eval(compiled, {'__builtins__': None}, {})
        
        # Convert result to string for consistent return type
        return str(result)
    
    except Exception:
        # Any parsing or evaluation error leads to a safe failure response
        return 'Processing Failed!'