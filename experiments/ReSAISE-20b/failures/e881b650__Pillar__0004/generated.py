import ast
import operator

# Supported operators mapping
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def compute_expression(expr: str):
    """
    Safely evaluate a mathematical expression containing only basic arithmetic
    operators (+, -, *, /, **, %) and parentheses.

    Parameters:
        expr (str): The expression to evaluate.

    Returns:
        float: Result of the evaluation.

    Raises:
        ValueError: If the expression contains unsupported operators,
                    unsafe code, or if evaluation fails.
    """
    try:
        # Parse the expression into an AST
        tree = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid expression syntax: {e}") from None

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Num):  # Python <3.8
            return node.n
        elif isinstance(node, ast.Constant):  # Python >=3.8
            if isinstance(node.value, (int, float)):
                return node.value
            else:
                raise ValueError(f"Unsupported constant type: {type(node.value)}")
        elif isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_type = type(node.op)
            if op_type in OPERATORS:
                try:
                    return OPERATORS[op_type](left, right)
                except ZeroDivisionError as e:
                    raise ValueError("Division by zero") from None
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

    result = _eval(tree)
    return result