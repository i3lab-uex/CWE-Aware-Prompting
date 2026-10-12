import ast
import operator

# Map AST operator nodes to safe Python functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Map AST unary operators to safe Python functions
_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed nodes in the AST
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,        # Python <3.8
    ast.Constant,   # Python >=3.8
    ast.Call,
    ast.Name,
    ast.Load,
)

def _evaluate(node: ast.AST) -> float:
    """
    Recursively evaluate an AST node.
    Raises ValueError if the node is not allowed or evaluation fails.
    """
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)

    # Numbers
    if isinstance(node, (ast.Num, ast.Constant)):
        value = node.n if hasattr(node, 'n') else node.value
        if not isinstance(value, (int, float)):
            raise ValueError(f"Unsupported numeric type: {type(value).__name__}")
        return value

    # Binary operations
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Disallowed binary operator: {op_type.__name__}")
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        return _ALLOWED_OPERATORS[op_type](left, right)

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_UNARY_OPERATORS:
            raise ValueError(f"Disallowed unary operator: {op_type.__name__}")
        operand = _evaluate(node.operand)
        return _ALLOWED_UNARY_OPERATORS[op_type](operand)

    # Disallow function calls, names, etc.
    raise ValueError(f"Disallowed expression: {ast.dump(node)}")

def compute_expression(expr_input: str) -> float:
    """
    Safely evaluate a mathematical expression provided as a string.

    Parameters
    ----------
    expr_input : str
        The arithmetic expression to evaluate. Allowed characters are digits,
        whitespace, parentheses and the operators + - * / // % **.

    Returns
    -------
    float
        The result of the evaluated expression.

    Raises
    ------
    ValueError
        If the input contains disallowed characters, malformed syntax,
        or evaluation fails.
    """
    if not isinstance(expr_input, str):
        raise ValueError("Input must be a string")

    # Strip whitespace to avoid accidental leading/trailing spaces
    expr = expr_input.strip()

    if not expr:
        raise ValueError("Empty expression")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in expression: {exc}") from exc

    # Verify all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node in expression: {type(node).__name__}")

    # Evaluate the parsed AST safely
    try:
        result = _evaluate(parsed)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Failed to evaluate expression: {exc}") from exc

    return result