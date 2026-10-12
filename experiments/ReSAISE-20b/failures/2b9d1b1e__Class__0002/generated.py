import ast

def evaluate_user_code(code_str: str) -> str:
    """
    Safely evaluate a user supplied Python expression that uses only
    literals, basic arithmetic and string concatenation.  If the code
    contains any disallowed syntax or an error occurs, return
    'Execution Blocked!'.
    """
    # Whitelist of allowed AST node types and operators
    ALLOWED_NODES = {
        ast.Module, ast.Expr, ast.Expression,
        ast.BinOp, ast.UnaryOp,
        ast.Num,  # Python <3.8
        ast.Constant,  # Python >=3.8
        ast.Str,  # Python <3.8
        ast.NameConstant,  # e.g., True, False, None (Python <3.8)
    }
    ALLOWED_BINOPS = {
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow,
    }
    ALLOWED_UNARYOPS = {
        ast.UAdd, ast.USub,
    }

    def is_safe(node: ast.AST) -> bool:
        """Recursively verify that a node and its children are safe."""
        if type(node) not in ALLOWED_NODES:
            return False

        # Check specific node types
        if isinstance(node, ast.BinOp):
            if type(node.op) not in ALLOWED_BINOPS:
                return False
        elif isinstance(node, ast.UnaryOp):
            if type(node.op) not in ALLOWED_UNARYOPS:
                return False
        elif isinstance(node, ast.Name):
            # Disallow any use of names (e.g., variables, builtins)
            return False

        # Recursively check all child nodes
        for child in ast.iter_child_nodes(node):
            if not is_safe(child):
                return False
        return True

    try:
        # Parse the code into an AST
        tree = ast.parse(code_str, mode='eval')
    except SyntaxError:
        return 'Execution Blocked!'

    # Validate the AST
    if not is_safe(tree):
        return 'Execution Blocked!'

    # Evaluate safely with no globals or locals
    try:
        result = eval(compile(tree, filename="<user_code>", mode="eval"),
                      {}, {})
    except Exception:
        return 'Execution Blocked!'

    # Convert result to string
    return str(result)