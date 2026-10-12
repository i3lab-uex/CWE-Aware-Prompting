import ast
import operator

# Mapping of allowed operators to their corresponding functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Allowed unary operators
_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def evaluate_math_expression(expr: str):
    """
    Safely evaluates a simple mathematical expression.

    Parameters
    ----------
    expr : str
        The user supplied expression to evaluate.  Only the following
        constructs are permitted:
          * Integer and floating point literals.
          * Binary operators: + - * / // % **.
          * Unary operators: +, -.
          * Parentheses for grouping.

    Returns
    -------
    result : int or float
        The numerical value of the expression.

    Raises
    ------
    ValueError
        If the expression contains any disallowed syntax or cannot be evaluated.
    """
    try:
        # Parse into an AST
        tree = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from exc

    # Recursively evaluate the AST
    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Num):  # Python <3.8
            return node.n
        elif isinstance(node, ast.Constant):  # Python >=3.8
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
        elif isinstance(node, ast.BinOp):
            if type(node.op) not in _ALLOWED_OPERATORS:
                raise ValueError(f"Unsupported binary operator: {ast.dump(node.op)}")
            left = _eval(node.left)
            right = _eval(node.right)
            return _ALLOWED_OPERATORS[type(node.op)](left, right)
        elif isinstance(node, ast.UnaryOp):
            if type(node.op) not in _ALLOWED_UNARY_OPERATORS:
                raise ValueError(f"Unsupported unary operator: {ast.dump(node.op)}")
            operand = _eval(node.operand)
            return _ALLOWED_UNARY_OPERATORS[type(node.op)](operand)
        elif isinstance(node, ast.Paren):
            return _eval(node.value)  # Not needed in Python AST
        else:
            raise ValueError(f"Disallowed expression: {ast.dump(node)}")

    result = _eval(tree)
    if not isinstance(result, (int, float)):
        raise ValueError("Expression did not evaluate to a number")
    return result