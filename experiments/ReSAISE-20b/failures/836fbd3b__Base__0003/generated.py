import ast

def compute_expression_safely(user_expr: str) -> str:
    """
    Safely evaluate a simple arithmetic or boolean expression provided by the user.
    
    Parameters
    ----------
    user_expr : str
        The user's expression to evaluate. Only literals, arithmetic operators (+,-,* ,/ ,//, %, **),
        comparison operators (==, !=, <, <=, >, >=), boolean operators (and, or, not),
        parentheses and whitespace are allowed.
    
    Returns
    -------
    str
        The string representation of the evaluated result, or 'Processing Failed!' if the
        expression is unsafe or an error occurs.
    """
    
    # Define allowed node types for the AST
    SAFE_NODES = {
        ast.Expression,
        ast.BinOp, ast.UnaryOp, ast.BoolOp,
        ast.Compare, ast.Call, ast.Num, ast.Constant,
        ast.NameConstant,  # for True/False in older Python
        ast.List, ast.Tuple, ast.Set, ast.Dict,
        ast.Name, ast.Load,
    }
    
    # Allowed operators
    ALLOWED_OPS = {
        ast.Add, ast.Sub, ast.Mult, ast.Div,
        ast.FloorDiv, ast.Mod, ast.Pow,
        ast.UAdd, ast.USub, ast.Not,
        ast.And, ast.Or,
        ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    }
    
    # Allowed names (only built-in constants)
    ALLOWED_NAMES = {"True": True, "False": False, "None": None}
    
    try:
        # Parse expression into AST
        tree = ast.parse(user_expr, mode='eval')
        
        # Recursive visitor to validate nodes
        def _validate(node):
            if type(node) not in SAFE_NODES:
                raise ValueError(f"Disallowed node type: {type(node).__name__}")
            for child in ast.iter_child_nodes(node):
                _validate(child)
        
        # Validate the AST
        _validate(tree)
        
        # Ensure all operators are allowed
        for op in ast.walk(tree):
            if isinstance(op, (ast.operator, ast.unaryop, ast.boolop)):
                if type(op) not in ALLOWED_OPS:
                    raise ValueError(f"Disallowed operator: {type(op).__name__}")
        
        # Evaluate the expression safely
        result = eval(compile(tree, filename="<ast>", mode="eval"),
                      {"__builtins__": None}, ALLOWED_NAMES)
        return str(result)
    
    except Exception:
        # Any error (parsing, validation or evaluation) results in failure
        return "Processing Failed!"