import ast
import operator

# Mapping of AST operator nodes to actual Python operators
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}

# Allowed unary operators
_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _evaluate(node: ast.AST) -> float:
    """
    Recursively evaluate a safe AST node.
    Raises ValueError if the node contains disallowed constructs.
    """
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)

    # Numeric constants (Python 3.8+ uses ast.Constant)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    # For older Python versions, handle ast.Num
    if isinstance(node, ast.Num):  # pragma: no cover
        return node.n

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_UNARY_OPERATORS:
            return _ALLOWED_UNARY_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    # Parentheses are handled implicitly by the AST structure
    if isinstance(node, ast.Paren):  # pragma: no cover (not used in AST)
        return _evaluate(node.value)

    raise ValueError(f"Disallowed expression component: {type(node).__name__}")

def compute_math_expression(expression_input: str) -> float:
    """
    Safely evaluate a mathematical expression provided as a string.

    Parameters
    ----------
    expression_input : str
        The user-provided mathematical expression.

    Returns
    -------
    float
        The result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains unsafe components or is structurally invalid.
    """
    if not isinstance(expression_input, str):
        raise ValueError("Expression must be a string")

    # Strip leading/trailing whitespace
    expr = expression_input.strip()
    if not expr:
        raise ValueError("Empty expression")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}")

    # Ensure the top-level node is an Expression
    if not isinstance(parsed, ast.Expression):
        raise ValueError("Expression must be evaluatable")

    # Recursively evaluate the parsed AST
    return _evaluate(parsed)