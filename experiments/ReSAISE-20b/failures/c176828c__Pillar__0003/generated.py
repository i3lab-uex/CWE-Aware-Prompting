import ast
import operator as op

# Mapping of allowed operators to their corresponding functions
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.FloorDiv: op.floordiv,
}

# Mapping of allowed unary operators
_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

def _eval_node(node):
    """
    Recursively evaluate an AST node. Only nodes that represent
    arithmetic expressions are allowed.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Numbers (int, float)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        operator_func = _ALLOWED_OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
        return operator_func(left, right)

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        operator_func = _ALLOWED_UNARY_OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        return operator_func(operand)

    # Parentheses are represented as Group nodes in newer Python versions
    if isinstance(node, ast.Paren):
        return _eval_node(node.value)

    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def calculate_expression(math_expr: str):
    """
    Evaluate a simple arithmetic expression provided as a string.

    Parameters
    ----------
    math_expr : str
        A mathematical expression containing numbers, +, -, *, /,
        **, %, // and parentheses. No other operations or function
        calls are permitted.

    Returns
    -------
    int | float
        The result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains unsupported characters, unsafe
        commands, or is otherwise invalid.
    """
    if not isinstance(math_expr, str):
        raise ValueError("Input must be a string")

    # Strip whitespace for easier validation
    expr = math_expr.strip()

    if not expr:
        raise ValueError("Empty expression")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Ensure the AST only contains allowed nodes
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Module,)):
            continue
        if not isinstance(node, (
                ast.Expression,
                ast.BinOp,
                ast.UnaryOp,
                ast.Constant,
                ast.Num,          # for Python <3.8
                ast.NameConstant, # for True/False in older versions
                ast.Expr,
                ast.Paren)):
            raise ValueError(f"Unsupported node type: {type(node).__name__}")

    # Evaluate the parsed AST
    return _eval_node(parsed)

# Example usage (commented out to avoid accidental execution)
# if __name__ == "__main__":
#     print(calculate_expression("3 + 4 * (2 - 1) / 5"))