import ast
import operator as op

# Allowed binary operators mapping
_BIN_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}

# Allowed unary operators mapping
_UNARY_OPS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

def _validate_node(node):
    """
    Recursively validate that the AST node only contains
    literals and permitted operators.
    Raises ValueError on any disallowed construct.
    """
    if isinstance(node, ast.Expression):
        return _validate_node(node.body)

    if isinstance(node, (ast.Num, ast.Constant)):
        # Only numeric constants are allowed
        if not isinstance(node.value, (int, float)):
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
        return

    if isinstance(node, ast.BinOp):
        if type(node.op) not in _BIN_OPS:
            raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
        _validate_node(node.left)
        _validate_node(node.right)
        return

    if isinstance(node, ast.UnaryOp):
        if type(node.op) not in _UNARY_OPS:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        _validate_node(node.operand)
        return

    if isinstance(node, ast.Expr):
        return _validate_node(node.value)

    # Allow parentheses via grouping
    if isinstance(node, ast.Paren):
        return _validate_node(node.value)

    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def _evaluate_node(node):
    """
    Recursively evaluate the validated AST node.
    Assumes validation has already been performed.
    """
    if isinstance(node, (ast.Num, ast.Constant)):
        return node.value

    if isinstance(node, ast.BinOp):
        left = _evaluate_node(node.left)
        right = _evaluate_node(node.right)
        return _BIN_OPS[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate_node(node.operand)
        return _UNARY_OPS[type(node.op)](operand)

    # Should never reach here due to prior validation
    raise ValueError(f"Unexpected node type during evaluation: {type(node).__name__}")

def safe_execute_operation(operation: str):
    """
    Safely evaluate a mathematical operation provided as a string.

    Parameters
    ----------
    operation : str
        The mathematical expression to evaluate. Only numeric literals and the
        operators +, -, *, /, //, %, ** are permitted. Parentheses may be used.

    Returns
    -------
    int | float
        The result of the evaluated expression.

    Raises
    ------
    ValueError
        If the input contains disallowed characters, syntax errors, or any
        unsupported construct.
    """
    if not isinstance(operation, str):
        raise ValueError("Operation must be a string")

    # Strip whitespace to avoid accidental injection via hidden characters
    stripped = operation.strip()
    if not stripped:
        raise ValueError("Empty operation")

    try:
        # Parse the expression into an AST
        tree = ast.parse(stripped, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Validate the AST recursively
    _validate_node(tree)

    # Evaluate safely
    try:
        result = _evaluate_node(tree.body)
    except ZeroDivisionError as exc:
        raise ValueError("Division by zero") from None
    except Exception as exc:  # Catch any unexpected math errors
        raise ValueError(f"Evaluation error: {exc}") from None

    return result