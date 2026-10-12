import ast
import operator

# Mapping of AST operator nodes to actual Python functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _eval_node(node):
    """
    Recursively evaluate an AST node that represents a numeric expression.
    Only allows literals and the operators defined in _ALLOWED_OPERATORS.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Numeric literal (Python 3.8+ uses Constant)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")

    # Binary operators (+, -, *, /, //, %, **)
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError("Unsupported binary operator")

    # Unary operators (+x, -x)
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError("Unsupported unary operator")

    # Parentheses are handled by grouping in the AST; no special node needed

    raise ValueError("Unsupported expression component")

def calculate_expression(expr_input: str) -> str:
    """
    Safely evaluate a simple arithmetic expression.

    Parameters
    ----------
    expr_input : str
        A string containing a mathematical expression (e.g. "2 + 3 * 4").

    Returns
    -------
    str
        The result of the evaluation as a string, or an error message.
    """
    try:
        # Parse expression into AST
        parsed = ast.parse(expr_input, mode='eval')

        # Verify that the AST contains only allowed nodes
        for node in ast.walk(parsed):
            if isinstance(node, (ast.Module,)):
                continue
            if not isinstance(node, (
                    ast.Expression,
                    ast.BinOp,
                    ast.UnaryOp,
                    ast.Constant,
            )):
                return "Computation Error!"

        result = _eval_node(parsed)
        # Convert to string for consistent return type
        return str(result)

    except Exception:
        # Any parsing or evaluation error results in a generic error message
        return "Computation Error!"