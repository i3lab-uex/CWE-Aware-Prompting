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
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # For Python <3.8
    ast.Constant,     # For Python >=3.8
    ast.Pow,
    ast.Sub,
    ast.Add,
    ast.Mult,
    ast.Div,
    ast.FloorDiv,
    ast.Mod,
    ast.UAdd,
    ast.USub,
    ast.Paren,        # Not a real node; parentheses are handled by the AST structure
)

def _validate_node(node: ast.AST):
    """
    Recursively validate that the AST node only contains allowed nodes and operators.
    Raise ValueError if an unexpected node is found.
    """
    if not isinstance(node, _ALLOWED_NODES):
        raise ValueError(f"Disallowed expression element: {type(node).__name__}")

    # For binary operations, validate left and right operands
    if isinstance(node, ast.BinOp):
        _validate_node(node.left)
        _validate_node(node.right)

        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError(f"Disallowed binary operator: {type(node.op).__name__}")

    # For unary operations, validate operand
    elif isinstance(node, ast.UnaryOp):
        _validate_node(node.operand)

        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError(f"Disallowed unary operator: {type(node.op).__name__}")

    # For numeric constants
    elif isinstance(node, (ast.Num, ast.Constant)):
        if not isinstance(getattr(node, 'n', getattr(node, 'value', None)), (int, float)):
            raise ValueError("Only integer and floating point constants are allowed.")

    # Recurse into any child nodes (for completeness)
    for child in ast.iter_child_nodes(node):
        _validate_node(child)


def _evaluate_ast(node: ast.AST) -> float:
    """
    Evaluate a validated AST node recursively.
    """
    if isinstance(node, (ast.Num, ast.Constant)):
        return getattr(node, 'n', getattr(node, 'value'))

    if isinstance(node, ast.BinOp):
        left = _evaluate_ast(node.left)
        right = _evaluate_ast(node.right)
        op_func = _ALLOWED_OPERATORS[type(node.op)]
        return op_func(left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate_ast(node.operand)
        op_func = _ALLOWED_OPERATORS[type(node.op)]
        return op_func(operand)

    raise ValueError(f"Unhandled AST node type: {type(node).__name__}")


def evaluate_expression_safely(expr: str):
    """
    Safely evaluate a mathematical expression provided as a string.

    Parameters
    ----------
    expr : str
        The mathematical expression to evaluate. Allowed characters are digits,
        decimal points, whitespace, parentheses and the operators + - * / % ** //.

    Returns
    -------
    float or int
        The result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters, unsupported operations,
        or is otherwise malformed.
    """
    if not isinstance(expr, str):
        raise ValueError("Expression must be a string.")

    # Strip whitespace for easier handling
    expr = expr.strip()
    if not expr:
        raise ValueError("Empty expression.")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid expression syntax: {e}")

    # Validate the AST
    _validate_node(parsed)

    # Evaluate the validated AST
    result = _evaluate_ast(parsed.body)
    return result