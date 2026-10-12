import ast

# List of AST node types that are considered safe.
SAFE_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # < 3.8
    ast.Constant,     # 3.8+
    ast.NameConstant,
    ast.Tuple,
    ast.List,
    ast.Dict,
    ast.Set,
)

# Operators that are allowed.
SAFE_OPERATORS = (
    ast.Add, ast.Sub, ast.Mult, ast.Div,
    ast.Mod, ast.Pow, ast.FloorDiv,
    ast.LShift, ast.RShift, ast.BitOr,
    ast.BitAnd, ast.BitXor, ast.UAdd, ast.USub
)

def _is_safe(node: ast.AST) -> bool:
    """
    Recursively check that all nodes in the AST are safe.
    """
    if not isinstance(node, SAFE_NODES):
        return False

    # For Binary and Unary operations, check operator type
    if isinstance(node, (ast.BinOp, ast.UnaryOp)):
        if not isinstance(node.op, SAFE_OPERATORS):
            return False

    # Recurse into child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe(child):
            return False

    # Ensure no names (variables) are used
    if isinstance(node, ast.Name):
        return False

    return True

def run_user_script(script_input: str) -> str:
    """
    Safely evaluate a user-provided Python script containing simple arithmetic
    or string operations. If the script contains unsafe code, return
    'Execution Blocked!'.

    Parameters:
        script_input (str): The user-submitted Python expression.

    Returns:
        str: The result of the evaluation or 'Execution Blocked!'.
    """
    try:
        # Parse the script into an AST
        parsed = ast.parse(script_input, mode='eval')
    except SyntaxError:
        return 'Execution Blocked!'

    # Validate the AST
    if not _is_safe(parsed):
        return 'Execution Blocked!'

    try:
        # Evaluate the expression in a restricted environment
        result = eval(compile(parsed, '<string>', mode='eval'), {}, {})
    except Exception:
        return 'Execution Blocked!'

    return str(result)