import ast

ALLOWED_OPERATORS = {
    ast.Add, ast.Sub, ast.Mult, ast.Div,
    ast.Mod, ast.Pow, ast.FloorDiv
}
ALLOWED_UNARY_OPERATORS = {ast.UAdd, ast.USub}

def _is_safe_node(node: ast.AST) -> bool:
    """
    Recursively verify that the AST node contains only safe constructs.
    Allowed nodes: Module, Expr, Expression, BinOp, UnaryOp,
                    Num (Constant), Str (Constant), NameConstant.
    """
    if isinstance(node, ast.Module):
        return all(_is_safe_node(n) for n in node.body)
    if isinstance(node, (ast.Expr, ast.Expression)):
        return _is_safe_node(node.value)
    if isinstance(node, ast.BinOp):
        return (
            type(node.op) in ALLOWED_OPERATORS and
            _is_safe_node(node.left) and
            _is_safe_node(node.right)
        )
    if isinstance(node, ast.UnaryOp):
        return (
            type(node.op) in ALLOWED_UNARY_OPERATORS and
            _is_safe_node(node.operand)
        )
    if isinstance(node, ast.Constant):
        return isinstance(node.value, (int, float, str, bool, type(None)))
    if isinstance(node, ast.Num):  # For Python <3.8
        return True
    if isinstance(node, ast.Str):
        return True
    if isinstance(node, ast.NameConstant):
        return True
    # Disallow any other node types (e.g., Call, Attribute, Import)
    return False

def evaluate_user_code(code_string: str) -> str:
    """
    Safely evaluate a simple arithmetic or string expression.
    Returns the result as a string, or 'Execution Blocked!' if unsafe.
    """
    try:
        # Parse the code into an AST
        tree = ast.parse(code_string, mode='eval')
    except SyntaxError:
        # If parsing fails (e.g., non-expression), block execution
        return 'Execution Blocked!'

    # Verify that the AST contains only safe nodes
    if not _is_safe_node(tree):
        return 'Execution Blocked!'

    try:
        # Evaluate the expression in a restricted environment
        result = eval(compile(tree, filename="<user_script>", mode="eval"),
                      {"__builtins__": None}, {})
    except Exception:
        # Any runtime error leads to blocking
        return 'Execution Blocked!'

    # Convert result to string for consistent return type
    return str(result)