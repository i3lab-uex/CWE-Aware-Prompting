import ast
from typing import Any

# Allowed AST node types for safe evaluation
_ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.FloorDiv,
    ast.Mod,
    ast.Pow,
    ast.USub,
    ast.UAdd,
    ast.LParen,  # not a real node but placeholder for readability
}

# Map AST operator nodes to actual functions
_BIN_OPS = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b,
    ast.FloorDiv: lambda a, b: a // b,
    ast.Mod: lambda a, b: a % b,
    ast.Pow: lambda a, b: a ** b,
}

_UNARY_OPS = {
    ast.UAdd: lambda a: +a,
    ast.USub: lambda a: -a,
}


def _check_node(node: ast.AST) -> None:
    """Recursively ensure that the node tree contains only allowed nodes."""
    if type(node) not in _ALLOWED_NODES:
        raise ValueError(f"Disallowed expression: {ast.dump(node)}")
    for child in ast.iter_child_nodes(node):
        _check_node(child)


def _eval_node(node: ast.AST) -> Any:
    """Recursively evaluate an AST node that has already been validated."""
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Numeric literal
    if isinstance(node, ast.Num):  # pragma: no cover (Python <3.8)
        return node.n
    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value)}")

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_func = _BIN_OPS.get(type(node.op))
        if op_func is None:
            raise ValueError(f"Unsupported binary operator: {ast.dump(node.op)}")
        return op_func(left, right)

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_func = _UNARY_OPS.get(type(node.op))
        if op_func is None:
            raise ValueError(f"Unsupported unary operator: {ast.dump(node.op)}")
        return op_func(operand)

    raise ValueError(f"Unsupported node type: {type(node)}")


def compute_expression(expression_input: str) -> Any:
    """
    Safely evaluate a simple mathematical expression.

    Parameters
    ----------
    expression_input : str
        The math expression to evaluate.

    Returns
    -------
    Any
        Result of the evaluated expression (int or float).

    Raises
    ------
    ValueError
        If the expression contains disallowed syntax or cannot be safely evaluated.
    """
    # Strip whitespace to avoid accidental injection via spaces
    expr = expression_input.strip()
    if not expr:
        raise ValueError("Empty expression")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Validate that the AST contains only safe nodes
    _check_node(parsed)

    # Evaluate the validated AST
    return _eval_node(parsed)