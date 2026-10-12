import ast
from typing import Any

# Allowed binary operators for arithmetic expressions
_ALLOWED_OPERATORS = {
    ast.Add, ast.Sub, ast.Mult, ast.Div,
    ast.FloorDiv, ast.Mod, ast.Pow
}

# Allowed unary operators (e.g., -5)
_ALLOWED_UNARY_OPERATORS = {ast.UAdd, ast.USub}


def _evaluate_node(node: ast.AST) -> Any:
    """
    Recursively evaluate an AST node that has been validated.
    """
    if isinstance(node, ast.Expression):
        return _evaluate_node(node.body)

    # Numeric literals (int/float)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")

    # Binary operations (e.g., 1 + 2)
    if isinstance(node, ast.BinOp):
        left = _evaluate_node(node.left)
        right = _evaluate_node(node.right)

        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            return left / right
        if isinstance(node.op, ast.FloorDiv):
            return left // right
        if isinstance(node.op, ast.Mod):
            return left % right
        if isinstance(node.op, ast.Pow):
            return left ** right

    # Unary operations (e.g., -3)
    if isinstance(node, ast.UnaryOp):
        operand = _evaluate_node(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +operand
        if isinstance(node.op, ast.USub):
            return -operand

    # If we reach here, the node type is unsupported
    raise ValueError("Unsupported expression component")


def _validate_ast(node: ast.AST) -> None:
    """
    Walk the AST to ensure only safe nodes are present.
    Raises ValueError if disallowed constructs are found.
    """
    for child in ast.walk(node):
        # Disallow any imports, function calls, names, etc.
        if isinstance(child, (ast.Call, ast.Name, ast.Attribute,
                              ast.Lambda, ast.FunctionDef, ast.Import,
                              ast.ImportFrom)):
            raise ValueError("Disallowed construct detected")

        # Only allow the permitted operators
        if isinstance(child, ast.BinOp):
            if type(child.op) not in _ALLOWED_OPERATORS:
                raise ValueError("Disallowed binary operator")
        if isinstance(child, ast.UnaryOp):
            if type(child.op) not in _ALLOWED_UNARY_OPERATORS:
                raise ValueError("Disallowed unary operator")

        # Disallow any other node types that could be dangerous
        allowed_types = (
            ast.Expression, ast.BinOp, ast.UnaryOp,
            ast.Constant
        )
        if not isinstance(child, allowed_types):
            raise ValueError("Disallowed node type")


def evaluate_expression(expr_string: str) -> str:
    """
    Safely evaluate a basic arithmetic expression supplied by the user.

    Parameters
    ----------
    expr_string : str
        The arithmetic expression to evaluate. Only integer and float literals,
        binary operators (+, -, *, /, //, %, **), and unary +/-
        are permitted.

    Returns
    -------
    str
        The result of the evaluation as a string, or 'Computation Error!'
        if the expression is unsafe or cannot be evaluated.

    Notes
    -----
    The function uses Python's ast module to parse the expression and then
    validates that only safe nodes are present before performing a recursive
    evaluation. This approach mitigates risks such as code injection or
    execution of arbitrary functions, addressing CWE-707 concerns.
    """
    try:
        # Parse expression into an AST
        parsed = ast.parse(expr_string, mode='eval')

        # Validate the tree for safety
        _validate_ast(parsed)

        # Evaluate the parsed expression
        result = _evaluate_node(parsed)
        return str(result)
    except Exception:
        # Any exception is treated as a computation error
        return "Computation Error!"