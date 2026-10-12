import ast
import math

# Allowed names from the math module (you can extend this list if needed)
_ALLOWED_NAMES = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}

def _is_safe_node(node: ast.AST) -> bool:
    """
    Recursively verify that the AST node only contains safe expression constructs.
    Allowed nodes: Expression, BinOp, UnaryOp, BoolOp, Compare,
                   Call (only to allowed names), Name (only allowed),
                   Num/Constant, Subscript, Index, Slice,
                   Attribute (restricted to allowed names)
    """
    if isinstance(node, ast.Expression):
        return _is_safe_node(node.body)

    # Literals
    if isinstance(node, (ast.Constant, ast.Num)):
        return True

    # Unary and binary operations
    if isinstance(node, (ast.UnaryOp, ast.BinOp, ast.BoolOp)):
        return all(_is_safe_node(child) for child in ast.iter_child_nodes(node))

    # Comparisons
    if isinstance(node, ast.Compare):
        return all(_is_safe_node(child) for child in ast.iter_child_nodes(node))

    # Function calls
    if isinstance(node, ast.Call):
        # Only allow calls to allowed names (no keyword arguments)
        if isinstance(node.func, ast.Name) and node.func.id in _ALLOWED_NAMES:
            return all(_is_safe_node(arg) for arg in node.args)
        return False

    # Variable names
    if isinstance(node, ast.Name):
        return node.id in _ALLOWED_NAMES

    # Subscript / slice
    if isinstance(node, (ast.Subscript, ast.Index, ast.Slice)):
        return all(_is_safe_node(child) for child in ast.iter_child_nodes(node))

    # Attribute access (e.g., math.sqrt)
    if isinstance(node, ast.Attribute):
        return (
            isinstance(node.value, ast.Name) and
            node.value.id in _ALLOWED_NAMES and
            hasattr(_ALLOWED_NAMES[node.value.id], node.attr)
        )

    # Anything else is disallowed
    return False

def evaluate_expression(expr: str) -> str:
    """
    Safely evaluates a Python expression provided as a string.
    Returns the string representation of the result or 'Error!' on failure.
    """
    try:
        # Parse expression to AST
        parsed = ast.parse(expr, mode="eval")

        # Verify safety of the AST
        if not _is_safe_node(parsed):
            return "Error!"

        # Prepare evaluation environment: only allowed names
        safe_globals = {"__builtins__": None}
        safe_locals = _ALLOWED_NAMES.copy()

        result = eval(compile(parsed, filename="<expr>", mode="eval"),
                      safe_globals, safe_locals)
        return str(result)
    except Exception:
        return "Error!"