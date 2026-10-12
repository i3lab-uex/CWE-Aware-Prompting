import ast
import operator as op

# Mapping of supported operators to their implementations
_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}

def _eval(node):
    """
    Recursively evaluate an AST node ensuring only safe operations are used.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    elif isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        operator_func = _OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError(f"Unsupported binary operator: {ast.dump(node.op)}")
        return operator_func(left, right)
    elif isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        operator_func = _OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError(f"Unsupported unary operator: {ast.dump(node.op)}")
        return operator_func(operand)
    elif isinstance(node, ast.Num):  # For Python <3.8
        return node.n
    elif isinstance(node, ast.Constant):  # For Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
    elif isinstance(node, ast.Paren):
        return _eval(node.value)
    else:
        raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def evaluate_expression(expression: str):
    """
    Safely evaluate a mathematical expression containing numbers and the
    operators +, -, *, /, ** and parentheses.

    Parameters:
        expression (str): The mathematical expression to evaluate.

    Returns:
        float: The evaluated result.

    Raises:
        ValueError: If the expression contains unsupported characters or
                    operators.
    """
    if not isinstance(expression, str):
        raise ValueError("Expression must be a string.")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(expression, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax in expression: {e}")

    # Evaluate the parsed AST safely
    return _eval(parsed)