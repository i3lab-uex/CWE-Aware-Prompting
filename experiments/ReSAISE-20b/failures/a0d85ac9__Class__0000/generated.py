import ast
from typing import Any

def calculate_user_input(input_expr: str) -> str:
    """
    Safely evaluate a simple arithmetic or logical expression provided by the user.
    
    Parameters
    ----------
    input_expr : str
        The expression to evaluate. Only literals, arithmetic operators,
        boolean operators and parentheses are allowed.
    
    Returns
    -------
    str
        The result of the evaluation as a string, or 'Processing Failed!' if
        any error occurs or an unsafe construct is detected.
    """
    
    # Define the set of AST node types that are considered safe
    SAFE_NODES = {
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.BoolOp,
        ast.Compare,
        ast.Call,          # disallowed, will raise
        ast.Name,          # disallowed, will raise
        ast.Attribute,     # disallowed, will raise
        ast.Subscript,     # disallowed, will raise
        ast.Index,
        ast.Slice,
        ast.Dict,
        ast.List,
        ast.Tuple,
        ast.Set,
        ast.Constant,      # Python 3.8+
        ast.Num,           # Deprecated but kept for older Python
        ast.Str,
        ast.Bytes,
        ast.NameConstant,  # True/False/None
    }
    
    # Allowed operators
    ALLOWED_OPERATORS = (
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
        ast.Mod, ast.Pow, ast.LShift, ast.RShift,
        ast.BitOr, ast.BitAnd, ast.BitXor, ast.UAdd, ast.USub,
        ast.Not, ast.And, ast.Or,
    )
    
    # Allowed comparison operators
    ALLOWED_COMPARISONS = (
        ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    )
    
    try:
        # Parse the expression into an AST
        parsed = ast.parse(input_expr, mode='eval')
        
        # Recursively walk the tree to ensure only safe nodes and operators are present
        for node in ast.walk(parsed):
            if type(node) not in SAFE_NODES:
                return "Processing Failed!"
            
            # Check operators
            if isinstance(node, ast.BinOp):
                if type(node.op) not in ALLOWED_OPERATORS:
                    return "Processing Failed!"
            elif isinstance(node, ast.UnaryOp):
                if type(node.op) not in ALLOWED_OPERATORS:
                    return "Processing Failed!"
            elif isinstance(node, ast.BoolOp):
                if type(node.op) not in ALLOWED_OPERATORS:
                    return "Processing Failed!"
            elif isinstance(node, ast.Compare):
                for op in node.ops:
                    if type(op) not in ALLOWED_COMPARISONS:
                        return "Processing Failed!"
            elif isinstance(node, ast.Call):
                # disallow any function calls
                return "Processing Failed!"
            elif isinstance(node, ast.Name):
                # disallow variable names
                return "Processing Failed!"
            elif isinstance(node, ast.Attribute):
                # disallow attribute access
                return "Processing Failed!"
        
        # Evaluate the expression safely
        result: Any = eval(compile(parsed, filename="<ast>", mode="eval"), {"__builtins__": None}, {})
        return str(result)
    
    except Exception:
        # Any exception leads to a generic failure message
        return "Processing Failed!"