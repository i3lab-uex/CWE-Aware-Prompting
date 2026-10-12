import ast
import operator as _op

# Mapping of allowed AST operator nodes to actual Python functions.
_ALLOWED_OPERATORS = {
    ast.Add: _op.add,
    ast.Sub: _op.sub,
    ast.Mult: _op.mul,
    ast.Div: _op.truediv,
    ast.FloorDiv: _op.floordiv,
    ast.Mod: _op.mod,
    ast.Pow: _op.pow,
    ast.UAdd: lambda x: +x,
    ast.USub: lambda x: -x,
}

# Nodes that are considered safe and will be evaluated.
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # For Python <3.8
    ast.Constant,     # For Python >=3.8
)

def _evaluate(node: ast.AST):
    """
    Recursively evaluate an AST node that has already been validated.
    """
    if isinstance(node, (ast.Num, ast.Constant)):
        # `Constant` may contain various types; only allow numbers.
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)

        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

        try:
            result = _ALLOWED_OPERATORS[op_type](left, right)
        except ZeroDivisionError as exc:
            raise ValueError("Division by zero") from exc
        return result

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return _ALLOWED_OPERATORS[op_type](operand)

    raise ValueError(f"Unsupported expression component: {type(node).__name__}")

def _validate_ast(tree: ast.AST):
    """
    Walk the AST and ensure that every node is of an allowed type.
    """
    for node in ast.walk(tree):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed expression element: {type(node).__name__}")

        # Ensure operators are allowed
        if isinstance(node, (ast.BinOp, ast.UnaryOp)):
            op_type = type(node.op)
            if op_type not in _ALLOWED_OPERATORS:
                raise ValueError(f"Disallowed operator: {op_type.__name__}")

def compute_expression(expr_input: str):
    """
    Safely evaluate a simple arithmetic expression.

    Parameters
    ----------
    expr_input : str
        The mathematical expression to evaluate. Only numeric literals and the
        operators + - * / // % ** (parentheses) are permitted.

    Returns
    -------
    int | float
        The result of the expression.

    Raises
    ------
    ValueError
        If the input contains illegal characters, unsupported operations,
        or if evaluation fails for any reason.
    """
    # Strip whitespace to avoid accidental leading/trailing characters
    expr = expr_input.strip()
    if not expr:
        raise ValueError("Empty expression")

    try:
        # Parse the expression in 'eval' mode to get an Expression node.
        tree = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in expression: {exc}") from exc

    # Validate the parsed AST
    _validate_ast(tree)

    # Evaluate safely
    try:
        result = _evaluate(tree.body)
    except Exception as exc:  # Catch any unexpected errors during evaluation
        raise ValueError(f"Failed to evaluate expression: {exc}") from exc

    return result