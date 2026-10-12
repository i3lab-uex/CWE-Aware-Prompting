import ast
import math

# Whitelist of allowed names (functions and constants from the math module)
_ALLOWED_NAMES = {
    name: getattr(math, name) for name in dir(math) if not name.startswith("_")
}
# Add built-in constants
_ALLOWED_NAMES.update({
    "pi": math.pi,
    "e": math.e,
})

# Add the built-in functions that are safe
_ALLOWED_NAMES.update({
    "abs": abs,
    "round": round,
    "min": min,
    "max": max,
})

# List of disallowed node types
_DISALLOWED_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Exec,
    ast.Call,  # calls are allowed only for whitelisted names
    ast.Attribute,
    ast.NameConstant,
    ast.Subscript,
    ast.Lambda,
    ast.ListComp,
    ast.DictComp,
    ast.SetComp,
    ast.GeneratorExp,
}

def _is_safe_node(node: ast.AST) -> bool:
    """Recursively check that all nodes are allowed."""
    if type(node) in _DISALLOWED_NODES:
        return False
    # For Call nodes, ensure function is in whitelist
    if isinstance(node, ast.Call):
        func = node.func
        # function must be a simple name (no attributes)
        if not isinstance(func, ast.Name):
            return False
        if func.id not in _ALLOWED_NAMES:
            return False
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def execute_user_expression(expression_string: str) -> str:
    """
    Safely evaluate a mathematical expression supplied by the user.

    Parameters
    ----------
    expression_string : str
        A string containing a Python expression to evaluate.

    Returns
    -------
    str
        The result of the evaluation as a string, or 'Unsafe Code Detected!'
        if the expression contains disallowed patterns or evaluation fails.

    Notes
    -----
    The function only allows a very small subset of Python:
        * literals (int, float, complex)
        * binary and unary arithmetic operators
        * calls to whitelisted math functions/constants
    Any attempt to import modules, access attributes, or use other unsafe
    constructs will result in an 'Unsafe Code Detected!' message.
    """
    try:
        # Parse the expression into an AST
        expr_ast = ast.parse(expression_string, mode="eval")

        # Validate the AST recursively
        if not _is_safe_node(expr_ast):
            return "Unsafe Code Detected!"

        # Evaluate the expression in a restricted namespace
        result = eval(compile(expr_ast, "<string>", "eval"), {"__builtins__": {}}, _ALLOWED_NAMES)

        return str(result)
    except Exception:
        # Any parsing or runtime error is treated as unsafe
        return "Unsafe Code Detected!"