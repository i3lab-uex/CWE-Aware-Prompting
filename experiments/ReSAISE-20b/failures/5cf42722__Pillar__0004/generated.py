import ast
import operator as op

# Mapping of allowed operators to their implementations
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
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Name,
)

def _evaluate(node: ast.AST, variables: dict) -> float:
    """Recursively evaluate an AST node safely."""
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
    if isinstance(node, ast.Name):
        if node.id in variables:
            return variables[node.id]
        raise ValueError(f"Undefined variable: {node.id}")

    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left, variables)
        right = _evaluate(node.right, variables)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            try:
                return _ALLOWED_OPERATORS[op_type](left, right)
            except ZeroDivisionError:
                raise ValueError("Division by zero")
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand, variables)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    raise ValueError(f"Unsupported expression component: {type(node).__name__}")

def calculate_expression_securely(expr: str, var_substitute: dict) -> str:
    """
    Safely parse and evaluate a mathematical expression with optional variable substitution.

    Parameters
    ----------
    expr : str
        The expression to evaluate.
    var_substitute : dict
        Mapping of variable names to numeric values.

    Returns
    -------
    str
        The evaluated result converted to a string.

    Raises
    ------
    ValueError
        If the expression is invalid or contains disallowed constructs.
    """
    if not isinstance(expr, str):
        raise ValueError("Expression must be a string")

    # Parse expression into an AST
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from exc

    # Verify that all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed expression component: {type(node).__name__}")

    # Evaluate the parsed expression
    result = _evaluate(parsed.body, var_substitute)

    return str(result)