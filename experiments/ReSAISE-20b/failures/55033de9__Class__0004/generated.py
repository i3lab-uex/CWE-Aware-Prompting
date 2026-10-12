import ast
import operator as op

# Mapping of allowed operators to their implementations
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}

# Mapping of allowed unary operators
_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

def _eval(node):
    """
    Recursively evaluate an AST node.
    Raises ValueError if unsupported nodes or operations are encountered.
    """
    if isinstance(node, ast.Num):  # For Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # For Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_UNARY_OPERATORS:
            return _ALLOWED_UNARY_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    if isinstance(node, ast.Expression):
        return _eval(node.body)

    if isinstance(node, (ast.Paren)):
        return _eval(node.value)

    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def evaluate_expression(expression: str):
    """
    Safely evaluates a mathematical expression containing numbers and
    the operators +, -, *, /, //, %, **, parentheses, and unary +/-.
    
    Parameters:
        expression (str): The mathematical expression to evaluate.

    Returns:
        int or float: Result of the evaluated expression.

    Raises:
        ValueError: If the expression contains unsupported characters,
                    operators, or invalid syntax.
    """
    # Strip whitespace
    expr = expression.strip()
    
    if not expr:
        raise ValueError("Empty expression")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}")

    # Ensure the top-level node is an Expression
    if not isinstance(parsed, ast.Expression):
        raise ValueError("Expression must be a single evaluatable expression")

    # Recursively evaluate the parsed AST
    return _eval(parsed)

# Example usage (uncomment to test):
# print(evaluate_expression("2 + 3 * (4 - 1)"))