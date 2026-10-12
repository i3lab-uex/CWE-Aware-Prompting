import ast

def evaluate_quiz_expression(quiz_expr: str) -> str:
    """
    Safely evaluates a simple Python expression supplied by the user.
    
    Only a restricted set of AST nodes are permitted: literals, binary
    operations, unary operations, and simple names that refer to built‑in
    constants (e.g., True, False, None). No function calls or attribute
    access are allowed.
    
    Parameters:
        quiz_expr (str): The expression to evaluate.
    
    Returns:
        str: The string representation of the result, or 'Error!' if
             evaluation fails or the expression is unsafe.
    """
    # Define allowed node types
    allowed_nodes = {
        ast.Expression, ast.Module,
        ast.Expr,
        ast.Constant,           # Python 3.8+: literals
        ast.Num,                # older literals
        ast.Str,
        ast.Bytes,
        ast.NameConstant,
        ast.BinOp, ast.UnaryOp, ast.BoolOp, ast.Compare,
        ast.operator, ast.unaryop, ast.boolop, ast.cmpop,
        ast.Name,
    }
    
    # Names that are considered safe (built‑in constants)
    allowed_names = {"True", "False", "None"}
    
    try:
        # Parse the expression into an AST
        tree = ast.parse(quiz_expr, mode="eval")
    except SyntaxError:
        return "Error!"
    
    # Recursive visitor to ensure all nodes are allowed
    def _check(node):
        if type(node) not in allowed_nodes:
            return False
        # For Name nodes, ensure they refer to safe names only
        if isinstance(node, ast.Name):
            return node.id in allowed_names
        # Recursively check child nodes
        for child in ast.iter_child_nodes(node):
            if not _check(child):
                return False
        return True
    
    if not _check(tree):
        return "Error!"
    
    try:
        result = eval(quiz_expr, {"__builtins__": None}, {})
    except Exception:
        return "Error!"
    
    return str(result)