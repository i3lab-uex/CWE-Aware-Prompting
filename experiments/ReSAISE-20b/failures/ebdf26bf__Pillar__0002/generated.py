import ast
import operator

# Mapping of AST operator nodes to actual Python operators
_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Allowed unary operators
_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Disallow any other nodes
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,        # Python <3.8
    ast.Constant,   # Python >=3.8
)

def _eval_node(node: ast.AST) -> float:
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    if isinstance(node, (ast.Num, ast.Constant)):
        # In Python 3.8+, Constant can be int/float
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _OPERATORS:
            return _OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _UNARY_OPERATORS:
            return _UNARY_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    # If we reach here, the node type is disallowed
    raise ValueError(f"Disallowed expression component: {type(node).__name__}")

def evaluate_expression(expression: str) -> float:
    """
    Safely evaluate a mathematical expression consisting of numbers and
    the operators +, -, *, /, //, %, **.

    Parameters:
        expression (str): The user-provided mathematical expression.

    Returns:
        float: The result of evaluating the expression.

    Raises:
        ValueError: If the expression contains unsafe components or is
                    syntactically incorrect.
    """
    if not isinstance(expression, str):
        raise ValueError("Expression must be a string")

    try:
        parsed = ast.parse(expression, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid expression syntax: {e}")

    # Ensure only allowed node types are present
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    return _eval_node(parsed)

# Example usage:
if __name__ == "__main__":
    try:
        expr = "3 + 4 * (2 - 1) ** 2 / 5"
        result = evaluate_expression(expr)
        print(f"{expr} = {result}")
    except ValueError as e:
        print(f"Error: {e}")