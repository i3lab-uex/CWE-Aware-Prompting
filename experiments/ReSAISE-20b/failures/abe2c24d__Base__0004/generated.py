import ast
import operator

# Supported operators mapped to their corresponding functions
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Allowed node types in the abstract syntax tree
ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,            # For Python <3.8
    ast.Constant,       # For numbers in Python >=3.8
    ast.UnaryOp,
    ast.UAdd,
    ast.USub,
)

def _eval_node(node):
    """
    Recursively evaluate an AST node, ensuring only safe operations are performed.
    """
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)

        op_type = type(node.op)
        if op_type not in OPERATORS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

        try:
            return OPERATORS[op_type](left, right)
        except ZeroDivisionError as exc:
            raise ValueError("Division by zero") from exc

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +operand
        elif isinstance(node.op, ast.USub):
            return -operand
        else:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")

    raise ValueError(f"Unsupported expression element: {type(node).__name__}")


def calculate_from_input(user_input: str):
    """
    Safely evaluate a mathematical expression provided by the user.

    Parameters
    ----------
    user_input : str
        The mathematical expression entered by the user.

    Returns
    -------
    float | int
        Numerical result of evaluating the expression.

    Raises
    ------
    ValueError
        If the input contains unsafe or malformed expressions.
    """
    if not isinstance(user_input, str):
        raise ValueError("Input must be a string")

    # Strip whitespace to avoid accidental leading/trailing characters
    expr = user_input.strip()
    if not expr:
        raise ValueError("Empty expression")

    try:
        # Parse the expression into an AST
        tree = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError("Malformed expression") from exc

    # Verify that only allowed node types are present
    for node in ast.walk(tree):
        if not isinstance(node, ALLOWED_NODES):
            raise ValueError(f"Disallowed expression element: {type(node).__name__}")

    # Evaluate the tree safely
    return _eval_node(tree.body)