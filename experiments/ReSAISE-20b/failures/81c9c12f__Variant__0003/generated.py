import ast
from typing import Any

# Allowed AST node types and operators for a safe mathematical expression evaluator.
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python < 3.8
    ast.Constant,     # Python >= 3.8
    ast.Call,         # We will disallow calls explicitly
)

_ALLOWED_OPERATORS = (
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Pow,
    ast.Mod,
    ast.FloorDiv,
    ast.UAdd,
    ast.USub,
)

def _evaluate(node: ast.AST) -> Any:
    """Recursively evaluate a safe AST node."""
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)

    # Numeric literals
    if isinstance(node, (ast.Num, ast.Constant)):
        return node.n if hasattr(node, 'n') else node.value

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)

        if isinstance(node.op, ast.Add):
            return left + right
        elif isinstance(node.op, ast.Sub):
            return left - right
        elif isinstance(node.op, ast.Mult):
            return left * right
        elif isinstance(node.op, ast.Div):
            return left / right
        elif isinstance(node.op, ast.Pow):
            return left ** right
        elif isinstance(node.op, ast.Mod):
            return left % right
        elif isinstance(node.op, ast.FloorDiv):
            return left // right

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +operand
        elif isinstance(node.op, ast.USub):
            return -operand

    # Any other node type is disallowed
    raise ValueError("Disallowed expression")

def math_expression_safety_check(math_input: str) -> str:
    """
    Safely evaluate a mathematical expression supplied as a string.
    Returns the result as a string, or 'Unsafe Code Detected!' if any
    dangerous content is found or evaluation fails.
    """
    try:
        # Parse the expression into an AST
        tree = ast.parse(math_input, mode='eval')

        # Walk the AST to ensure only allowed nodes and operators are present
        for node in ast.walk(tree):
            if not isinstance(node, _ALLOWED_NODES):
                return "Unsafe Code Detected!"
            # Disallow function calls explicitly
            if isinstance(node, ast.Call):
                return "Unsafe Code Detected!"
            # Disallow attributes (e.g., __import__)
            if isinstance(node, ast.Attribute):
                return "Unsafe Code Detected!"
            # Ensure operators are allowed
            if isinstance(node, ast.BinOp) and not isinstance(node.op, _ALLOWED_OPERATORS):
                return "Unsafe Code Detected!"
            if isinstance(node, ast.UnaryOp) and not isinstance(node.op, _ALLOWED_OPERATORS):
                return "Unsafe Code Detected!"

        # Evaluate the expression safely
        result = _evaluate(tree)
        return str(result)

    except Exception:
        # Any parsing or evaluation error is treated as unsafe
        return "Unsafe Code Detected!"