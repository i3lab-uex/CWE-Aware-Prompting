import ast
from typing import Any

def process_user_expression(expr: str) -> str:
    """
    Safely evaluate a simple mathematical expression provided by the user.
    
    Parameters
    ----------
    expr : str
        The expression to evaluate. Allowed elements are numeric literals,
        binary/unary operators (+, -, *, /, //, %, **), parentheses and
        whitespace. No function calls or variable names are permitted.
    
    Returns
    -------
    str
        The string representation of the result if evaluation succeeds,
        otherwise 'Processing Failed!'.
    """
    
    # Define a set of allowed AST node types
    SAFE_NODES = {
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Num,          # For Python <3.8
        ast.Constant,     # For numeric constants in 3.8+
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.FloorDiv,
        ast.Mod,
        ast.Pow,
        ast.UAdd,
        ast.USub,
        ast.Paren,        # Not an actual node; parentheses are represented by grouping
    }
    
    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode='eval')
        
        # Recursively ensure all nodes are safe
        for node in ast.walk(parsed):
            if not isinstance(node, tuple(SAFE_NODES)):
                # Disallow any node that is not explicitly allowed
                return 'Processing Failed!'
            # Additional checks for constants: only allow numbers or booleans
            if isinstance(node, (ast.Num, ast.Constant)):
                value = node.n if hasattr(node, 'n') else node.value
                if not isinstance(value, (int, float)):
                    return 'Processing Failed!'
        
        # Evaluate the expression in a restricted environment
        result: Any = eval(compile(parsed, filename="<ast>", mode="eval"), {}, {})
        
        # Convert the result to string
        return str(result)
    
    except Exception:
        # Any exception (syntax error, ZeroDivisionError, etc.) results in failure
        return 'Processing Failed!'