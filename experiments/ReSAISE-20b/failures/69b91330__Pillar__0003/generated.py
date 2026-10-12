import ast
import math

# Allowed names from the math module and some built‑ins
_ALLOWED_NAMES = {
    name: getattr(math, name)
    for name in dir(math)
    if not name.startswith("_")
}
_ALLOWED_NAMES.update({
    "abs": abs,
    "round": round,
    "min": min,
    "max": max,
})

# Allowed AST node types
_ALLOWED_NODES = {
    ast.Expression,  # top level container
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Name,
    ast.Call,
    ast.Load,
    ast.operator,
    ast.unaryop,
}

def _is_allowed_node(node):
    """Recursively verify that a node and all its children are allowed."""
    if type(node) not in _ALLOWED_NODES:
        return False
    for child in ast.iter_child_nodes(node):
        if not _is_allowed_node(child):
            return False
    return True

def evaluate_expression_securely(input_code: str) -> str:
    """
    Safely evaluates a user supplied mathematical expression.
    
    Parameters
    ----------
    input_code : str
        A Python expression intended for numeric calculation.
    
    Returns
    -------
    str
        The result converted to string, or 'Unsafe Code Detected!' if the
        expression contains disallowed nodes, references unknown names,
        or an exception occurs during evaluation.
    """
    try:
        # Parse the expression into an AST
        tree = ast.parse(input_code, mode="eval")

        # Verify that the entire tree consists only of allowed nodes
        if not _is_allowed_node(tree):
            return "Unsafe Code Detected!"

        # Ensure all names are from the allowed namespace
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                if node.id not in _ALLOWED_NAMES:
                    return "Unsafe Code Detected!"

        # Evaluate the expression with a restricted environment
        result = eval(compile(tree, filename="<ast>", mode="eval"),
                      {"__builtins__": {}},
                      _ALLOWED_NAMES)

        # Only numeric results are meaningful in this context
        if not isinstance(result, (int, float)):
            return "Unsafe Code Detected!"

        return str(result)

    except Exception:
        # Any parsing or runtime error is treated as unsafe
        return "Unsafe Code Detected!"