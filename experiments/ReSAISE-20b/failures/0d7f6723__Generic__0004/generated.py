import ast
from typing import Any

# Allowed node types for a safe evaluation
ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,        # Python <3.8
    ast.Constant,   # Python >=3.8
    ast.Str,        # Python <3.8 string constant
    ast.NameConstant,
    ast.operator,
    ast.unaryop,
}

# Allowed operators (binary and unary)
ALLOWED_BINOPS = {
    ast.Add, ast.Sub, ast.Mult, ast.Div,
    ast.FloorDiv, ast.Mod, ast.Pow
}
ALLOWED_UNARYOPS = {
    ast.UAdd, ast.USub
}

def _is_safe_node(node: ast.AST) -> bool:
    """Recursively check that a node and all its children are safe."""
    # Basic node type check
    if type(node) not in ALLOWED_NODES:
        return False

    # Specific checks for operator nodes
    if isinstance(node, ast.BinOp):
        if type(node.op) not in ALLOWED_BINOPS:
            return False
    elif isinstance(node, ast.UnaryOp):
        if type(node.op) not in ALLOWED_UNARYOPS:
            return False

    # Recurse into child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def parse_user_script(script_str: str) -> str:
    """
    Safely evaluate a tiny Python script containing only basic arithmetic
    or string operations.

    Parameters:
        script_str (str): The user-provided Python code.

    Returns:
        str: Result of the evaluation as a string, or 'Execution Blocked!'
             if the script is unsafe or an error occurs.
    """
    try:
        # Parse the code into an AST expression
        tree = ast.parse(script_str, mode='eval')
    except SyntaxError:
        return 'Execution Blocked!'

    # Validate the AST for safety
    if not _is_safe_node(tree):
        return 'Execution Blocked!'

    try:
        # Evaluate the expression in a sandboxed environment
        result = eval(compile(tree, filename="<user_script>", mode="eval"),
                      {"__builtins__": None}, {})
        return str(result)
    except Exception:
        # Any exception during evaluation is treated as unsafe
        return 'Execution Blocked!'