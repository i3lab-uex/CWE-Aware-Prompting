import ast
import operator

# Map AST operators to actual Python functions
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}

# Allowed unary operators
UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def calculate_user_input(user_input: str):
    """
    Safely evaluate a mathematical expression provided as a string.

    Parameters
    ----------
    user_input : str
        The user's mathematical expression.

    Returns
    -------
    float or int
        The result of the evaluated expression.

    Raises
    ------
    ValueError
        If the input contains disallowed characters, syntax errors,
        or unsupported operations.
    """
    if not isinstance(user_input, str):
        raise ValueError("Input must be a string.")

    # Parse the expression into an AST
    try:
        expr_ast = ast.parse(user_input, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Recursive evaluator
    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)

        elif isinstance(node, ast.Num):          # Python <3.8
            return node.n

        elif isinstance(node, ast.Constant):    # Python 3.8+
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

        elif isinstance(node, ast.BinOp):
            if type(node.op) not in OPERATORS:
                raise ValueError(f"Unsupported binary operator: {ast.dump(node.op)}")
            left = _eval(node.left)
            right = _eval(node.right)
            try:
                return OPERATORS[type(node.op)](left, right)
            except ZeroDivisionError as exc:
                raise ValueError("Division by zero") from None

        elif isinstance(node, ast.UnaryOp):
            if type(node.op) not in UNARY_OPERATORS:
                raise ValueError(f"Unsupported unary operator: {ast.dump(node.op)}")
            operand = _eval(node.operand)
            return UNARY_OPERATORS[type(node.op)](operand)

        elif isinstance(node, ast.Paren):
            return _eval(node.value)

        else:
            raise ValueError(f"Disallowed expression: {ast.dump(node)}")

    return _eval(expr_ast)

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     expr = "3 + 4 * (2 - 1) / 5 ** 2"
#     print(calculate_user_input(expr))