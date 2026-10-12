import ast
import operator

# Mapping of allowed AST operator nodes to corresponding functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
}

# Allowed unary operators
_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _eval_node(node):
    """
    Recursively evaluate an AST node, only allowing a limited set of operations.
    Raises ValueError if the node is not permitted.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Numbers (int/float) - allow only literal constants
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError("Unsupported binary operator")

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_UNARY_OPERATORS:
            return _ALLOWED_UNARY_OPERATORS[op_type](operand)
        raise ValueError("Unsupported unary operator")

    # Parentheses are handled implicitly by AST grouping

    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def process_math_expr(math_input: str) -> str:
    """
    Safely evaluate a simple mathematical expression provided as a string.
    Only integers, floats, and the operators + - * / ** % // are allowed.

    Parameters:
        math_input (str): The expression to evaluate.

    Returns:
        str: The result of the evaluation or 'Computation Error!' if invalid.
    """
    try:
        # Strip whitespace and parse expression
        parsed = ast.parse(math_input, mode='eval')

        # Validate that the top-level node is an Expression
        if not isinstance(parsed, ast.Expression):
            return 'Computation Error!'

        result = _eval_node(parsed)
        # Convert result to string, preserving integer formatting when possible
        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        return str(result)

    except Exception:
        # Any parsing or evaluation error results in a generic error message
        return 'Computation Error!'