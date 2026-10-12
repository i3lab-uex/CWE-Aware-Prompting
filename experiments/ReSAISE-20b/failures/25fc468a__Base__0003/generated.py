import ast

# Whitelist of safe built‑in functions that may be called by the user script
SAFE_FUNCTIONS = {"str", "int", "float", "len"}

def _is_safe_node(node: ast.AST) -> bool:
    """
    Recursively check whether a node and all its children are safe.
    """
    # Allowed container nodes
    if isinstance(node, (ast.Expression, ast.Module)):
        return all(_is_safe_node(n) for n in node.body)

    # Literal values
    if isinstance(node, (ast.Constant, ast.Num, ast.Str, ast.Bytes)):
        return True

    # Unary operations like -5
    if isinstance(node, ast.UnaryOp):
        return _is_safe_node(node.operand)

    # Binary operations like 2 + 3
    if isinstance(node, ast.BinOp):
        return _is_safe_node(node.left) and _is_safe_node(node.right)

    # Function calls
    if isinstance(node, ast.Call):
        # Only allow calls to whitelisted functions with no arguments that are themselves safe
        if isinstance(node.func, ast.Name) and node.func.id in SAFE_FUNCTIONS:
            return all(_is_safe_node(arg) for arg in node.args)
        return False

    # Names are only allowed if they refer to the whitelisted functions
    if isinstance(node, ast.Name):
        return node.id in SAFE_FUNCTIONS

    # All other nodes are disallowed
    return False


def run_user_script(script_input: str) -> str:
    """
    Safely evaluate a small Python expression submitted by the user.
    The function permits only basic arithmetic and string operations.
    If the script contains any unsafe constructs, it returns 'Execution Blocked!'.

    Parameters
    ----------
    script_input : str
        The user supplied Python code.

    Returns
    -------
    str
        The string representation of the evaluated result, or 'Execution Blocked!'
        if the script is unsafe.
    """
    try:
        # Parse the input into an AST
        tree = ast.parse(script_input, mode="eval")

        # Validate the entire tree
        if not _is_safe_node(tree):
            return "Execution Blocked!"

        # Evaluate the expression in a restricted environment
        safe_globals = {"__builtins__": None}
        safe_locals = {}
        result = eval(compile(tree, "<user_script>", mode="eval"), safe_globals, safe_locals)

        return str(result)
    except Exception:
        # Any exception (including syntax errors) results in blocking
        return "Execution Blocked!"