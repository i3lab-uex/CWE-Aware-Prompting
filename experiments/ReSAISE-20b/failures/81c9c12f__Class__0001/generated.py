import ast
import math

# Whitelist of allowed names (functions/constants from the math module)
_ALLOWED_NAMES = {
    name: getattr(math, name) for name in dir(math) if not name.startswith("_")
}
# Also allow built‑in constants True/False/None
_ALLOWED_NAMES.update({"True": True, "False": False, "None": None})


def _is_safe_node(node: ast.AST) -> bool:
    """
    Recursively check whether an AST node is safe for evaluation.
    Allowed nodes: Expression, BinOp, UnaryOp, BoolOp, Compare,
                   Call (only to whitelisted names), Name, Num/Constant,
                   Subscript (for indexing into allowed containers),
                   Attribute is disallowed.
    """
    if isinstance(node, ast.Expression):
        return _is_safe_node(node.body)

    # Literals
    if isinstance(node, (ast.Constant, ast.Num)):
        return True

    # Names must be in whitelist
    if isinstance(node, ast.Name):
        return node.id in _ALLOWED_NAMES

    # Binary operations
    if isinstance(node, (ast.BinOp, ast.BoolOp, ast.Compare)):
        return all(_is_safe_node(child) for child in ast.iter_child_nodes(node))

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        return _is_safe_node(node.operand)

    # Function calls
    if isinstance(node, ast.Call):
        # Only allow direct calls to whitelisted names (no attribute access)
        if isinstance(node.func, ast.Name) and node.func.id in _ALLOWED_NAMES:
            return all(_is_safe_node(arg) for arg in node.args)
        return False

    # Subscript (e.g., list indexing) is allowed only for whitelisted names
    if isinstance(node, ast.Subscript):
        return (
            isinstance(node.value, ast.Name)
            and node.value.id in _ALLOWED_NAMES
            and _is_safe_node(node.slice)
        )

    # Disallow everything else (attribute access, lambdas, comprehensions, etc.)
    return False


def math_expression_safety_check(math_input: str) -> str:
    """
    Safely evaluate a mathematical expression provided as a string.

    Parameters
    ----------
    math_input : str
        The user supplied mathematical expression.

    Returns
    -------
    str
        The result of the evaluation as a string, or 'Unsafe Code Detected!' if
        the input is unsafe or an error occurs during evaluation.
    """
    try:
        # Parse into AST
        parsed = ast.parse(math_input, mode="eval")

        # Verify that the entire tree is safe
        if not _is_safe_node(parsed):
            return "Unsafe Code Detected!"

        # Evaluate with restricted globals/locals
        result = eval(compile(parsed, "<string>", mode="eval"),
                      {"__builtins__": None}, _ALLOWED_NAMES)

        return str(result)
    except Exception:
        # Any exception is treated as unsafe
        return "Unsafe Code Detected!"