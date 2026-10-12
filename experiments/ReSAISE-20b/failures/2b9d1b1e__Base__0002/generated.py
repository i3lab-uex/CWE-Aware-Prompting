import ast

SAFE_OPERATORS = {
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow,
    ast.FloorDiv,  # integer division
    ast.UAdd, ast.USub,  # unary + and -
}

SAFE_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,      # Python <3.8
    ast.Constant,  # Python >=3.8
    ast.Str,      # legacy string constants
)

def _is_safe_node(node: ast.AST) -> bool:
    """
    Recursively checks that the node tree only contains allowed nodes and operators.
    """
    if not isinstance(node, SAFE_NODES):
        return False

    # Check operators
    if isinstance(node, ast.BinOp) and type(node.op) not in SAFE_OPERATORS:
        return False
    if isinstance(node, ast.UnaryOp) and type(node.op) not in SAFE_OPERATORS:
        return False

    # Recurse into child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def evaluate_user_code(code_str: str) -> str:
    """
    Safely evaluates a user‑supplied Python expression that uses only basic arithmetic
    and string operations. If the code contains disallowed syntax or constructs,
    returns 'Execution Blocked!'.

    Parameters
    ----------
    code_str : str
        The user‑supplied expression to evaluate.

    Returns
    -------
    str
        String representation of the evaluated result or 'Execution Blocked!'.
    """
    try:
        # Parse into an AST expression
        tree = ast.parse(code_str, mode='eval')
    except SyntaxError:
        return 'Execution Blocked!'

    # Validate the AST
    if not _is_safe_node(tree):
        return 'Execution Blocked!'

    try:
        # Evaluate in a restricted environment
        result = eval(compile(tree, filename='<user>', mode='eval'), {}, {})
    except Exception:
        return 'Execution Blocked!'

    return str(result)