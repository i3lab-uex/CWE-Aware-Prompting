import ast
from typing import Any

# Allowed AST node types for safe evaluation
SAFE_NODES = {
    ast.Expression,
    ast.Module,
    ast.Expr,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Str,
    ast.NameConstant,
    ast.BoolOp,
    ast.Compare,
    ast.Load,
    ast.operator,
    ast.unaryop,
    ast.cmpop,
}

# Whitelist of allowed names (basic arithmetic and string operations)
ALLOWED_NAMES = {
    "True": True,
    "False": False,
    "None": None,
}

def _is_safe(node: ast.AST) -> bool:
    """Recursively check that a node and its children are allowed."""
    if type(node) not in SAFE_NODES:
        return False
    for child in ast.iter_child_nodes(node):
        if not _is_safe(child):
            return False
    return True

def run_user_script(script_input: str) -> str:
    """
    Safely evaluate a user supplied Python script that contains simple arithmetic
    or string operations.

    Parameters:
        script_input (str): The user submitted Python code.

    Returns:
        str: The evaluated result as a string, or 'Execution Blocked!' if the
             script contains unsafe constructs.
    """
    try:
        # Parse the input into an AST
        parsed = ast.parse(script_input, mode="eval")
    except SyntaxError:
        # If the script cannot be parsed as an expression, block execution
        return "Execution Blocked!"

    # Verify that the AST only contains safe nodes
    if not _is_safe(parsed):
        return "Execution Blocked!"

    # Prepare a restricted global namespace
    safe_globals = {"__builtins__": None, **ALLOWED_NAMES}

    try:
        # Compile and evaluate the expression
        compiled = compile(parsed, "<user_script>", mode="eval")
        result: Any = eval(compiled, safe_globals)
    except Exception:
        # Any runtime error is treated as unsafe
        return "Execution Blocked!"

    # Convert the result to string for consistent output
    return str(result)