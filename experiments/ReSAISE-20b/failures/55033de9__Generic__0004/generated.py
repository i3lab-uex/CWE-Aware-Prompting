import ast
import operator

# Mapping of supported operators to their functions
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}

def evaluate_expression(expression: str):
    """
    Safely evaluate a mathematical expression containing only numbers and
    the operators +, -, *, /, **, parentheses, and unary minus.

    Parameters:
        expression (str): The mathematical expression to evaluate.

    Returns:
        float: The result of the evaluated expression.

    Raises:
        ValueError: If the expression contains unsupported characters or
                    operators.
    """
    try:
        # Parse the expression into an AST node
        tree = ast.parse(expression, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Num):  # For Python <3.8
            return node.n
        elif isinstance(node, ast.Constant):  # For Python >=3.8
            if isinstance(node.value, (int, float)):
                return node.value
            else:
                raise ValueError(f"Unsupported constant type: {type(node.value)}")
        elif isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_type = type(node.op)
            if op_type in OPERATORS:
                return OPERATORS[op_type](left, right)
            else:
                raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        elif isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            op_type = type(node.op)
            if op_type in OPERATORS:
                return OPERATORS[op_type](operand)
            else:
                raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        elif isinstance(node, ast.Paren):
            return _eval(node.value)
        else:
            raise ValueError(f"Unsupported expression element: {type(node).__name__}")

    return _eval(tree)

# Example usage:
if __name__ == "__main__":
    expr = "2 + 3 * (4 ** 2) - 5 / 2"
    print(f"{expr} = {evaluate_expression(expr)}")