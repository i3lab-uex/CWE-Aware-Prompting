import ast
from typing import Union

# Allowed binary operators
_ALLOWED_BINOPS = {
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.FloorDiv,
    ast.Mod,
    ast.Pow,
}

# Allowed unary operators
_ALLOWED_UNARYOPS = {
    ast.UAdd,
    ast.USub,
}

# Allowed numeric constants (Python 3.8+ uses Constant)
_ALLOWED_CONSTANTS = {ast.Num, ast.Constant}


def _eval_node(node: ast.AST) -> Union[int, float]:
    """
    Recursively evaluate an AST node that represents a numeric expression.
    Raises ValueError if the node contains unsupported syntax or types.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Numeric constants
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.Num):  # For Python <3.8
        return node.n

    # Binary operations
    if isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_BINOPS:
            raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
        left = _eval_node(node.left)
        right = _eval_node(node.right)

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

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_UNARYOPS:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        operand = _eval_node(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +operand
        if isinstance(node.op, ast.USub):
            return -operand

    # Allow parentheses (they are just grouping in the AST)
    if isinstance(node, ast.Paren):
        return _eval_node(node.value)

    raise ValueError(f"Unsupported expression element: {ast.dump(node)}")


def evaluate_expression(math_expr: str) -> Union[int, float]:
    """
    Evaluate a mathematical expression given as a string.

    Parameters
    ----------
    math_expr : str
        A string containing the expression to evaluate.

    Returns
    -------
    int | float
        The evaluated result of the expression.

    Raises
    ------
    ValueError
        If the expression contains unsupported operators, characters,
        or if evaluation fails.
    """
    try:
        # Parse expression in 'eval' mode to ensure it's an expression
        parsed = ast.parse(math_expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from exc

    # Walk the AST to ensure only allowed nodes are present
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Call, ast.Import, ast.ImportFrom,
                            ast.FunctionDef, ast.ClassDef, ast.Module)):
            raise ValueError("Expressions containing function or import calls are not allowed")

    return _eval_node(parsed)