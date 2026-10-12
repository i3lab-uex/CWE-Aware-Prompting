import ast
import math

# Allowed names: functions and constants from the math module only
ALLOWED_NAMES = {
    name: getattr(math, name)
    for name in dir(math)
    if not name.startswith("_")
}

# Disallowed node types that could lead to unsafe code
DISALLOWED_NODES = {
    ast.Call,  # disallow any function call except allowed names
    ast.Import,
    ast.ImportFrom,
    ast.Attribute,
    ast.Lambda,
    ast.FunctionDef,
    ast.ClassDef,
    ast.Module,
    ast.Global,
    ast.Nonlocal,
    ast.Exec,
    ast.Delete,
}

def _is_safe_node(node):
    """
    Recursively check if the AST node only contains safe constructs.
    Only literals, binary/unary ops, and name references to allowed math names
    are permitted.
    """
    if isinstance(node, (ast.Expression, ast.Module)):
        return all(_is_safe_node(n) for n in node.body if hasattr(node, "body") else [node])

    if isinstance(node, ast.Num):  # Python <3.8
        return True

    if isinstance(node, ast.Constant):  # Python >=3.8
        return isinstance(node.value, (int, float, complex))

    if isinstance(node, ast.BinOp):
        return _is_safe_node(node.left) and _is_safe_node(node.right)

    if isinstance(node, ast.UnaryOp):
        return _is_safe_node(node.operand)

    if isinstance(node, ast.Name):
        # Only allow names that are in the allowed math namespace
        return node.id in ALLOWED_NAMES

    if isinstance(node, ast.Load):
        return True

    # Disallow any other node types
    return False


def safely_execute_expression(expression_code: str) -> str:
    """
    Safely evaluate a mathematical expression provided as a string.
    
    Parameters
    ----------
    expression_code : str
        A user-provided Python expression intended for numeric calculation.
    
    Returns
    -------
    str
        The result of the evaluation converted to string, or an error message.
    
    Raises
    ------
    None
        Any unsafe code or runtime errors result in the string 'Unsafe Code Detected!'.
    """
    try:
        # Parse expression into an AST
        parsed = ast.parse(expression_code, mode="eval")

        # Verify that the tree contains only safe nodes
        if not _is_safe_node(parsed):
            return "Unsafe Code Detected!"

        # Compile the safe AST into a code object
        compiled = compile(parsed, filename="<ast>", mode="eval")

        # Evaluate the expression with no builtins and only allowed math names
        result = eval(compiled, {"__builtins__": {}}, ALLOWED_NAMES)

        return str(result)
    except Exception:
        # Any exception is treated as unsafe
        return "Unsafe Code Detected!"