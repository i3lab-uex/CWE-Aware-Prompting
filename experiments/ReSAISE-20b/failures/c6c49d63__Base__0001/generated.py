import ast
import operator

# Mapping of allowed operators to their corresponding functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

def _eval_node(node):
    """
    Recursively evaluate an AST node, allowing only numeric literals and
    the operators defined in _ALLOWED_OPERATORS.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

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

    if isinstance(node, ast.Num):          # For Python < 3.8
        return node.n

    if isinstance(node, ast.Constant):     # For Python >= 3.8
        if isinstance(node.value, (int, float)):
            return node.value
        else:
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.Paren):
        return _eval_node(node.value)

    # Disallow any other node types (e.g., function calls, attributes)
    raise ValueError(f"Unsupported expression component: {type(node).__name__}")

def compute_expression(input_expr: str):
    """
    Safely parse and evaluate a simple arithmetic expression.

    Parameters
    ----------
    input_expr : str
        A string containing the arithmetic expression to evaluate.

    Returns
    -------
    float or int
        The result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains unsupported characters, unsafe commands,
        or invalid operations.
    """
    # Strip whitespace to simplify parsing
    expr = input_expr.strip()

    if not expr:
        raise ValueError("Empty expression")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Walk the AST to ensure only allowed nodes are present
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Call, ast.Attribute, ast.Import,
                            ast.ImportFrom, ast.Lambda, ast.FunctionDef)):
            raise ValueError("Unsupported operation detected")

    # Evaluate the parsed AST
    return _eval_node(parsed)

# Example usage:
if __name__ == "__main__":
    test_exprs = ["2 + 3 * 4", "-(5**2)", "10 / (3 - 1)", "abs(5)"]
    for expr in test_exprs:
        try:
            print(f"{expr} => {compute_expression(expr)}")
        except ValueError as e:
            print(f"{expr} => Error: {e}")