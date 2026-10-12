import ast
import operator as op

# Mapping of allowed AST operator nodes to actual Python operators
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}

def _eval(node):
    """
    Recursively evaluate an AST node that represents a mathematical expression.
    Only numeric literals and allowed operators are permitted.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    if isinstance(node, ast.Num):          # For Python < 3.8
        return node.n

    if isinstance(node, ast.Constant):     # For Python >= 3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        operator_type = type(node.op)
        if operator_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[operator_type](left, right)
        raise ValueError(f"Unsupported binary operator: {operator_type.__name__}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        operator_type = type(node.op)
        if operator_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[operator_type](operand)
        raise ValueError(f"Unsupported unary operator: {operator_type.__name__}")

    if isinstance(node, ast.Paren):
        return _eval(node.value)

    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def safe_execute_operation(operation: str):
    """
    Safely evaluate a mathematical operation supplied as a string.

    Parameters
    ----------
    operation : str
        The mathematical expression to evaluate. Only numbers, parentheses,
        and the operators + - * / ** are permitted.

    Returns
    -------
    int | float
        The result of the evaluated expression.

    Raises
    ------
    ValueError
        If the input contains disallowed characters, invalid syntax,
        or if evaluation fails for any reason.
    """
    # Strip whitespace to avoid accidental injection via spaces
    expr = operation.strip()

    if not expr:
        raise ValueError("Empty expression")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Validate that the AST contains only allowed nodes
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Module,)):
            continue
        if not isinstance(node, (
                ast.Expression,
                ast.BinOp,
                ast.UnaryOp,
                ast.Num,          # Python < 3.8
                ast.Constant,     # Python >= 3.8
                ast.Add,
                ast.Sub,
                ast.Mult,
                ast.Div,
                ast.Pow,
                ast.USub,
                ast.UAdd,
                ast.Load,
                ast.Expr,
                ast.Paren,        # Not actually a node type; included for clarity
            )):
            raise ValueError(f"Disallowed expression element: {type(node).__name__}")

    # Evaluate the AST safely
    try:
        result = _eval(parsed)
    except Exception as e:
        raise ValueError(f"Evaluation error: {e}") from None

    return result