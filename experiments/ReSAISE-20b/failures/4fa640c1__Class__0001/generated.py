import ast
import operator as op

# Mapping of allowed operators to their corresponding functions
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,  # root node
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python < 3.8
    ast.Constant,     # Python >= 3.8
    ast.Tuple,
    ast.List,
    ast.Subscript,    # for list indexing (optional)
    ast.Index,        # for Python < 3.9
    ast.Slice,
)

def _eval_node(node):
    """
    Recursively evaluate an AST node after validating it.
    Raises ValueError on any disallowed construct.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Constants / numbers
    if isinstance(node, (ast.Num, ast.Constant)):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        return _ALLOWED_OPERATORS[op_type](left, right)

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return _ALLOWED_OPERATORS[op_type](operand)

    # Disallow any other node types
    raise ValueError(f"Disallowed expression component: {type(node).__name__}")

def perform_safe_math(expression: str):
    """
    Safely evaluate a mathematical expression string.

    Parameters
    ----------
    expression : str
        A string containing the mathematical expression to evaluate.

    Returns
    -------
    result : int | float
        The numerical result of the expression.

    Raises
    ------
    ValueError
        If the expression contains unsafe characters, unsupported operations,
        or is otherwise malformed.
    """
    if not isinstance(expression, str):
        raise ValueError("Expression must be a string")

    # Strip whitespace to prevent accidental injection of comments
    expr = expression.strip()

    if not expr:
        raise ValueError("Empty expression")

    try:
        # Parse the expression into an AST
        tree = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Verify that the tree contains only allowed node types
    for node in ast.walk(tree):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Evaluate the parsed tree
    return _eval_node(tree)

# Example usage (for testing purposes)
if __name__ == "__main__":
    test_expressions = [
        "2 + 3 * (7 - 4) / 5",
        "-(1+2)**3",
        "10 // 3",
        "4 % 3",
    ]
    for expr in test_expressions:
        print(f"{expr} = {perform_safe_math(expr)}")