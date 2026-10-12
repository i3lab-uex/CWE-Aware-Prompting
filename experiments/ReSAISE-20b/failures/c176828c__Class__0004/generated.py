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
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed names (e.g., math functions) – empty for a purely arithmetic calculator
_ALLOWED_NAMES = {}

def _eval_node(node):
    """
    Recursively evaluate an AST node, allowing only safe operations.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

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
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    if isinstance(node, ast.Call):
        # Prevent function calls – only allow names from _ALLOWED_NAMES if desired
        raise ValueError("Function calls are not allowed")

    if isinstance(node, ast.Name):
        id_ = node.id
        if id_ in _ALLOWED_NAMES:
            return _ALLOWED_NAMES[id_]
        raise ValueError(f"Use of undefined name: {id_}")

    if isinstance(node, ast.Tuple) or isinstance(node, ast.List):
        # Prevent tuples/lists
        raise ValueError("Sequences are not allowed")

    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def calculate_expression(math_expr: str):
    """
    Safely evaluate a simple arithmetic expression provided as a string.

    Parameters
    ----------
    math_expr : str
        The mathematical expression to evaluate.

    Returns
    -------
    result : float or int
        The computed value of the expression.

    Raises
    ------
    ValueError
        If the input contains unsupported characters, unsafe commands,
        or invalid operations.
    """
    if not isinstance(math_expr, str):
        raise ValueError("Input must be a string")

    # Strip whitespace and check for empty input
    expr = math_expr.strip()
    if not expr:
        raise ValueError("Empty expression")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Walk the AST to ensure no disallowed nodes are present
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.Exec,
                            ast.Call, ast.Attribute, ast.Lambda,
                            ast.Dict, ast.Set, ast.ListComp,
                            ast.GeneratorExp, ast.Await)):
            raise ValueError(f"Disallowed expression element: {type(node).__name__}")

    # Evaluate the parsed AST
    return _eval_node(parsed)

# Example usage (uncomment to test):
# if __name__ == "__main__":
#     expr = "2 + 3 * (4 - 1) / 5 ** 2"
#     print(f"{expr} = {calculate_expression(expr)}")