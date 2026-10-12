import ast
import math
from typing import Any

# List of allowed names (functions and constants) from the math module.
_ALLOWED_NAMES = {
    name: getattr(math, name)
    for name in dir(math)
    if not name.startswith("_")
}

# Allowed binary operators
_ALLOWED_BINOPS = {
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Pow,
    ast.Mod,
    ast.FloorDiv,
}

# Allowed unary operators
_ALLOWED_UNARYOPS = {ast.UAdd, ast.USub}


def _is_safe_node(node: ast.AST) -> bool:
    """
    Recursively check if a node is safe for evaluation.
    """
    if isinstance(node, (ast.Expression, ast.Module)):
        return all(_is_safe_node(n) for n in node.body if hasattr(node, "body") else [node])

    if isinstance(node, ast.Expr):
        return _is_safe_node(node.value)

    if isinstance(node, (ast.Num, ast.Constant)):
        # Constant numeric values are allowed
        return True

    if isinstance(node, ast.BinOp):
        return (
            type(node.op) in _ALLOWED_BINOPS
            and _is_safe_node(node.left)
            and _is_safe_node(node.right)
        )

    if isinstance(node, ast.UnaryOp):
        return (
            type(node.op) in _ALLOWED_UNARYOPS
            and _is_safe_node(node.operand)
        )

    if isinstance(node, ast.Call):
        # Only allow calls to functions from the math module
        if not isinstance(node.func, ast.Name):
            return False
        func_name = node.func.id
        if func_name not in _ALLOWED_NAMES:
            return False
        # Ensure all arguments are safe
        return all(_is_safe_node(arg) for arg in node.args)

    if isinstance(node, ast.Name):
        # Allow constants like pi, e etc.
        return node.id in _ALLOWED_NAMES

    # Any other node types are disallowed
    return False


def evaluate_expression_securely(input_code: str) -> str:
    """
    Safely evaluate a mathematical expression supplied as a string.

    Parameters
    ----------
    input_code : str
        The user-supplied Python expression to evaluate.

    Returns
    -------
    str
        The result of the evaluation as a string, or 'Unsafe Code Detected!'
        if the expression contains disallowed code or evaluation fails.
    """
    try:
        # Parse the input into an AST
        parsed = ast.parse(input_code, mode="eval")

        # Validate that the entire expression is safe
        if not _is_safe_node(parsed):
            return "Unsafe Code Detected!"

        # Compile the AST into a code object
        compiled = compile(parsed, filename="<ast>", mode="eval")

        # Evaluate the expression with a restricted namespace
        result: Any = eval(compiled, {"__builtins__": {}}, _ALLOWED_NAMES)

        return str(result)
    except Exception:
        # Any parsing or evaluation error is treated as unsafe
        return "Unsafe Code Detected!"