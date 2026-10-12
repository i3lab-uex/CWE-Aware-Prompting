import ast

def evaluate_input_expression(expression: str) -> str:
    """
    Safely evaluates a simple arithmetic or logical expression supplied by the user.
    
    Allowed elements:
        - Numbers (int, float)
        - Booleans: True, False
        - None
        - Arithmetic operators: + - * / // % ** 
        - Unary operators: + -
        - Boolean operators: and, or, not
        - Comparisons: < > <= >= == !=
    
    Any other syntax or names will cause the evaluation to fail.
    """
    try:
        # Parse expression into an AST
        tree = ast.parse(expression, mode='eval')
        
        # Define allowed node types and operators
        allowed_nodes = (
            ast.Expression,
            ast.BinOp,
            ast.UnaryOp,
            ast.BoolOp,
            ast.Compare,
            ast.NameConstant,  # True, False, None in older Python
            ast.Constant,      # Numbers, bools, None in newer Python
            ast.Num,
            ast.Str,
            ast.Bytes,
            ast.Tuple,
            ast.List,
            ast.Set,
            ast.Dict,
        )
        
        allowed_ops = (
            # Binary operators
            ast.Add, ast.Sub, ast.Mult, ast.Div,
            ast.FloorDiv, ast.Mod, ast.Pow,
            # Unary operators
            ast.UAdd, ast.USub, ast.Not,
            # Boolean operators
            ast.And, ast.Or,
            # Comparisons
            ast.Eq, ast.NotEq, ast.Lt, ast.LtE,
            ast.Gt, ast.GtE,
        )
        
        # Recursively walk the AST to ensure safety
        for node in ast.walk(tree):
            if not isinstance(node, allowed_nodes):
                raise ValueError(f"Disallowed node type: {type(node).__name__}")
            
            # Check operator types
            if isinstance(node, (ast.BinOp, ast.BoolOp, ast.UnaryOp, ast.Compare)):
                for op in (node.op if hasattr(node, 'op') else []):
                    if not isinstance(op, allowed_ops):
                        raise ValueError(f"Disallowed operator: {type(op).__name__}")
            
            # Disallow any Name nodes (variables)
            if isinstance(node, ast.Name):
                raise ValueError(f"Disallowed name: {node.id}")
        
        # Evaluate safely with empty globals/locals
        result = eval(compile(tree, filename="<ast>", mode="eval"), {}, {})
        
        return str(result)
    
    except Exception:
        # Any exception (parsing, security check, runtime) results in failure
        return "Processing Failed!"