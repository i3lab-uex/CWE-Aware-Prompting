import ast
import operator

# Supported operators mapping from AST nodes to actual Python functions
_SUPPORTED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Supported unary operators
_SUPPORTED_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _eval_node(node):
    """
    Recursively evaluate an AST node, allowing only safe arithmetic operations.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Numbers (int or float)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")

    # Binary operations (+, -, *, /, //, %, **)
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)

        op_type = type(node.op)
        if op_type not in _SUPPORTED_OPERATORS:
            raise ValueError("Unsupported binary operator")
        return _SUPPORTED_OPERATORS[op_type](left, right)

    # Unary operations (+, -)
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type not in _SUPPORTED_UNARY_OPERATORS:
            raise ValueError("Unsupported unary operator")
        return _SUPPORTED_UNARY_OPERATORS[op_type](operand)

    # Allow parentheses by delegating to their contained expression
    if isinstance(node, ast.Paren):
        return _eval_node(node.value)

    # For Python 3.9+, ast.Num and ast.NameConstant are deprecated in favor of Constant
    # No other node types should be allowed
    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def process_math_expr(math_input: str) -> str:
    """
    Safely evaluate a basic arithmetic expression provided as a string.

    Parameters
    ----------
    math_input : str
        A mathematical expression in Python syntax.

    Returns
    -------
    str
        The result of the evaluation as a string, or 'Computation Error!' if
        the input is unsafe or cannot be evaluated.
    """
    try:
        # Parse the expression into an AST
        expr_ast = ast.parse(math_input, mode='eval')

        # Walk the tree to ensure only allowed nodes are present
        for node in ast.walk(expr_ast):
            if not isinstance(node, (
                ast.Expression,
                ast.BinOp,
                ast.UnaryOp,
                ast.Constant,
                ast.Add, ast.Sub, ast.Mult, ast.Div,
                ast.FloorDiv, ast.Mod, ast.Pow,
                ast.UAdd, ast.USub,
            )):
                raise ValueError("Disallowed node in expression")

        # Evaluate the parsed AST
        result = _eval_node(expr_ast)

        # Convert result to string (ensure float formatting is clean)
        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        return str(result)

    except Exception:
        # Any exception (syntax error, unsafe node, division by zero, etc.)
        return 'Computation Error!'