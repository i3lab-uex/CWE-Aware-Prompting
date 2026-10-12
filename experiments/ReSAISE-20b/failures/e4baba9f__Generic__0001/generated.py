import ast
import operator

# Mapping of allowed AST nodes to their corresponding Python operations
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed node types for the expression
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Expr,
)

def _eval_node(node):
    """
    Recursively evaluate an AST node ensuring only allowed operations are used.
    """
    if isinstance(node, (ast.Num, ast.Constant)):
        # Ensure the value is a number
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numeric constants are allowed")

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)

        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

        return _ALLOWED_OPERATORS[op_type](operand)

    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def compute_math_expression(expression_input: str):
    """
    Safely evaluate a mathematical expression provided by the user.

    Parameters
    ----------
    expression_input : str
        The mathematical expression to evaluate.

    Returns
    -------
    int | float
        The result of the evaluated expression.

    Raises
    ------
    ValueError
        If the input contains unsafe components or has an incorrect structure.
    """
    if not isinstance(expression_input, str):
        raise ValueError("Input must be a string")

    # Strip whitespace to avoid accidental parsing of hidden characters
    expression_input = expression_input.strip()

    if not expression_input:
        raise ValueError("Empty expression")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expression_input, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Ensure the parsed AST contains only allowed nodes
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed expression element: {type(node).__name__}")

    # Evaluate the parsed AST
    return _eval_node(parsed.body)