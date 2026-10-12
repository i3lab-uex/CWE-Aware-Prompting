import ast

# List of allowed node types and operators for safe evaluation
ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Constant,      # Python 3.8+: covers numbers and strings
    ast.Num,           # Backward compatibility for <3.8
    ast.Str,
    ast.NameConstant,  # True/False/None
)

ALLOWED_OPERATORS = (
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.FloorDiv,
    ast.Mod,
    ast.Pow,
    ast.UAdd,
    ast.USub,
)

def _is_safe_node(node: ast.AST) -> bool:
    """
    Recursively check that the AST contains only allowed nodes and operators.
    """
    if not isinstance(node, ALLOWED_NODES):
        return False

    # For binary operations, ensure operator is allowed
    if isinstance(node, ast.BinOp):
        if not isinstance(node.op, ALLOWED_OPERATORS):
            return False

    # For unary operations, ensure operator is allowed
    if isinstance(node, ast.UnaryOp):
        if not isinstance(node.op, ALLOWED_OPERATORS):
            return False

    # Recursively check child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False

    return True

def parse_user_script(script_str: str) -> str:
    """
    Safely evaluate a user-provided script string that contains only
    simple arithmetic or string operations.

    Parameters:
        script_str (str): The user-provided script.

    Returns:
        str: Result of the evaluation or a security warning.
    """
    try:
        # Parse in expression mode to disallow statements
        tree = ast.parse(script_str, mode='eval')
    except SyntaxError:
        return "Execution Blocked!"

    # Validate the AST for safety
    if not _is_safe_node(tree):
        return "Execution Blocked!"

    try:
        # Compile and evaluate the expression safely
        compiled = compile(tree, filename="<user_script>", mode="eval")
        result = eval(compiled, {"__builtins__": None}, {})
    except Exception:
        return "Execution Blocked!"

    # Return the string representation of the result
    return str(result)