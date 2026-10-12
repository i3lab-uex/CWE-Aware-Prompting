import ast

ALLOWED_NODES = (
    ast.Expression,  # root node for eval()
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Str,
    ast.NameConstant,
)

ALLOWED_OPERATORS = (
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
    ast.Mod, ast.Pow,  # arithmetic operators
    ast.UAdd, ast.USub,  # unary plus/minus
)

def _is_safe(node: ast.AST) -> bool:
    """Recursively verify that a node and its children are safe."""
    if not isinstance(node, ALLOWED_NODES):
        return False
    # Check operators in BinOp and UnaryOp
    if isinstance(node, ast.BinOp):
        if not isinstance(node.op, ALLOWED_OPERATORS):
            return False
    elif isinstance(node, ast.UnaryOp):
        if not isinstance(node.op, ALLOWED_OPERATORS):
            return False
    # Recursively inspect child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe(child):
            return False
    return True

def execute_user_input(user_code: str) -> str:
    """
    Safely evaluate a user-supplied Python expression that contains only
    simple arithmetic or string operations. If the code is unsafe or raises
    an exception, return 'Execution Blocked!'.

    Parameters:
        user_code (str): The code to evaluate.

    Returns:
        str: Result of evaluation or 'Execution Blocked!'.
    """
    try:
        # Parse the code into an AST
        parsed = ast.parse(user_code, mode='eval')
    except SyntaxError:
        return 'Execution Blocked!'

    # Ensure the parsed tree contains only allowed nodes
    if not _is_safe(parsed):
        return 'Execution Blocked!'

    # Evaluate safely with no globals or locals
    try:
        result = eval(compile(parsed, filename="<user_input>", mode="eval"),
                      {"__builtins__": {}}, {})
    except Exception:
        return 'Execution Blocked!'

    # Convert the result to string
    return str(result)