import ast
import operator as op

# Mapping of AST operators to actual functions
_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}

# Allowed unary operators
_UNARY_OPERATORS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

def _eval(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    if isinstance(node, ast.Num):          # Python <3.8
        return node.n

    if isinstance(node, ast.Constant):     # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        operator_func = _OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError(f"Unsupported binary operator: {ast.dump(node.op)}")
        return operator_func(left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        operator_func = _UNARY_OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError(f"Unsupported unary operator: {ast.dump(node.op)}")
        return operator_func(operand)

    if isinstance(node, ast.Paren):  # Not needed; parentheses are handled by AST grouping
        return _eval(node.value)

    raise ValueError(f"Unsupported expression element: {ast.dump(node)}")

def calculate_expression(math_expr: str):
    """
    Evaluate a simple arithmetic expression provided as a string.

    Parameters
    ----------
    math_expr : str
        A mathematical expression containing numbers and the operators
        +, -, *, /, //, %, **.  Parentheses are allowed.

    Returns
    -------
    float or int
        The result of evaluating the expression.

    Raises
    ------
    ValueError
        If the input contains unsupported characters, unsafe commands,
        or invalid operations.
    """
    if not isinstance(math_expr, str):
        raise ValueError("Input must be a string")

    # Strip whitespace to avoid accidental leading/trailing characters
    expr = math_expr.strip()

    if not expr:
        raise ValueError("Empty expression")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Ensure the parsed AST contains only allowed nodes
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Call, ast.Attribute, ast.Import,
                             ast.ImportFrom, ast.FunctionDef, ast.Lambda)):
            raise ValueError(f"Disallowed construct: {ast.dump(node)}")

    return _eval(parsed)