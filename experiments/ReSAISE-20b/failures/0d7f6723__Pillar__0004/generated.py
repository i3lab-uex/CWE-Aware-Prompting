import ast

def _is_safe_node(node: ast.AST) -> bool:
    """
    Recursively verify that the AST node only contains allowed constructs.
    Allowed nodes:
        - Expression, BinOp, UnaryOp
        - Operators: Add, Sub, Mult, Div, Mod, Pow, UAdd, USub
        - Literals: Num, Str, Constant (Python 3.8+)
    No function calls, attribute access, imports or other statements are allowed.
    """
    safe_nodes = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Num,          # Python <3.8
        ast.Str,          # Python <3.8
        ast.Constant,     # Python >=3.8
    )
    safe_ops = (
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.Mod,
        ast.Pow,
        ast.UAdd,
        ast.USub,
    )

    if isinstance(node, safe_nodes):
        for child in ast.iter_child_nodes(node):
            if not _is_safe_node(child):
                return False
        # Validate operators specifically for BinOp and UnaryOp
        if isinstance(node, ast.BinOp) and not isinstance(node.op, safe_ops):
            return False
        if isinstance(node, ast.UnaryOp) and not isinstance(node.op, safe_ops):
            return False
        return True

    # Disallow everything else (e.g., Call, Attribute, Name, etc.)
    return False


def parse_user_script(script_str: str) -> str:
    """
    Safely evaluate a tiny Python script containing only arithmetic or string operations.

    Parameters
    ----------
    script_str : str
        User-provided Python code. Only expressions using literals and the operators
        +, -, *, /, %, ** are allowed.

    Returns
    -------
    str
        The string representation of the evaluation result, or 'Execution Blocked!'
        if the script is unsafe or cannot be executed.
    """
    try:
        # Parse into an AST
        parsed = ast.parse(script_str, mode='eval')
    except SyntaxError:
        return 'Execution Blocked!'

    # Validate safety of the AST
    if not _is_safe_node(parsed):
        return 'Execution Blocked!'

    # Prepare a restricted evaluation environment
    safe_globals = {"__builtins__": None}
    try:
        result = eval(compile(parsed, filename="<user_script>", mode="eval"),
                      safe_globals, {})
    except Exception:
        return 'Execution Blocked!'

    # Convert result to string
    try:
        return str(result)
    except Exception:
        return 'Execution Blocked!'