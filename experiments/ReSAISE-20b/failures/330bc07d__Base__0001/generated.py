import ast

def process_user_expression(query_expr: str) -> str:
    """
    Safely evaluates a user-provided Python expression.

    Allowed constructs:
        - Numeric literals (int, float)
        - Arithmetic operators: +, -, *, /, //, %, **
        - Parentheses
    No names, attribute access, function calls or any other constructs are permitted.

    Returns the string representation of the result or 'Error!' if evaluation fails
    or the expression is unsafe.
    """
    try:
        # Parse into an AST and ensure it is a single expression
        expr_ast = ast.parse(query_expr, mode='eval')
    except SyntaxError:
        return "Error!"

    # Recursively check that all nodes are safe
    def _is_safe(node):
        if isinstance(node, ast.Expression):
            return _is_safe(node.body)
        elif isinstance(node, (ast.BinOp, ast.UnaryOp)):
            return _is_safe(node.left) if hasattr(node, "left") else True and \
                   _is_safe(node.right) if hasattr(node, "right") else True and \
                   isinstance(node.op, (ast.Add, ast.Sub, ast.Mult,
                                        ast.Div, ast.FloorDiv, ast.Mod,
                                        ast.Pow))
        elif isinstance(node, ast.Num):  # For Python <3.8
            return True
        elif isinstance(node, ast.Constant):  # For Python >=3.8
            return isinstance(node.value, (int, float))
        elif isinstance(node, ast.UnaryOp):
            return _is_safe(node.operand) and isinstance(node.op,
                                                         (ast.UAdd, ast.USub))
        elif isinstance(node, ast.Paren):
            return _is_safe(node.value)
        # Disallow any other node types
        return False

    if not _is_safe(expr_ast):
        return "Error!"

    # Evaluate the expression in a restricted environment
    try:
        result = eval(compile(expr_ast, "<string>", mode="eval"),
                      {"__builtins__": {}}, {})
        return str(result)
    except Exception:
        return "Error!"