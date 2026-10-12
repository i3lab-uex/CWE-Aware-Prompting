import ast
from typing import Union

# Allowed AST node types and operator types
_ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
}
_ALLOWED_OPERATORS = {
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Pow,
    ast.UAdd,
    ast.USub,
}

def _is_allowed(node: ast.AST) -> bool:
    """
    Recursively verify that the AST node tree only contains allowed
    nodes and operators.
    """
    if type(node) not in _ALLOWED_NODES:
        return False

    # Check operator nodes
    if isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            return False
    elif isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            return False

    # Recurse into child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_allowed(child):
            return False
    return True

def secure_math_eval(exp_str: str) -> Union[int, float]:
    """
    Safely evaluate a simple mathematical expression provided as a string.

    Parameters
    ----------
    exp_str : str
        User supplied mathematical expression. Only +, -, *, /, ** and parentheses
        are allowed.

    Returns
    -------
    int | float
        The numeric result of the evaluated expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters, syntax errors,
        or unsafe constructs.
    """
    # Strip whitespace to avoid hidden characters
    exp_str = exp_str.strip()
    if not exp_str:
        raise ValueError("Empty expression")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(exp_str, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Validate the AST tree
    if not _is_allowed(parsed):
        raise ValueError("Expression contains disallowed operations or characters")

    # Evaluate the expression safely
    try:
        result = eval(compile(parsed, filename="<secure_eval>", mode="eval"),
                      {"__builtins__": None}, {})
    except ZeroDivisionError:
        raise ValueError("Division by zero")
    except Exception as e:
        # Catch any unexpected runtime error
        raise ValueError(f"Evaluation error: {e}") from None

    return result