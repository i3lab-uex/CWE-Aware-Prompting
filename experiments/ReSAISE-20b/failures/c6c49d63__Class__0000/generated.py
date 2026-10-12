import ast
import operator

# Supported operators mapping from AST node to actual function
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

# Supported constants (e.g., math constants can be added if needed)
_ALLOWED_CONSTANTS = {
    'pi': 3.141592653589793,
    'e': 2.718281828459045
}

def _eval_node(node):
    """
    Recursively evaluate an AST node, allowing only safe operations.
    Raises ValueError on unsupported nodes or unsafe constructs.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Numbers (int/float)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    # Binary operations (e.g., 1 + 2)
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    # Unary operations (e.g., -5)
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    # Parenthesized expressions are handled by the recursive call
    if isinstance(node, ast.Paren):
        return _eval_node(node.value)

    # Variable names for constants (e.g., pi, e)
    if isinstance(node, ast.Name):
        if node.id in _ALLOWED_CONSTANTS:
            return _ALLOWED_CONSTANTS[node.id]
        raise ValueError(f"Unknown identifier: {node.id}")

    # Disallow any other node types (e.g., function calls, imports)
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def compute_expression(input_expr: str):
    """
    Safely evaluate a simple arithmetic expression provided as a string.

    Parameters
    ----------
    input_expr : str
        The user supplied arithmetic expression (e.g., "3 + 4 * (2 - 1)").

    Returns
    -------
    float or int
        The computed result of the expression.

    Raises
    ------
    ValueError
        If the expression contains unsupported characters, unsafe constructs,
        or if it cannot be parsed.
    """
    # Strip whitespace to simplify validation
    expr = input_expr.strip()

    if not expr:
        raise ValueError("Empty expression")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}")

    # Walk the AST to ensure only allowed nodes are present
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Call, ast.Import, ast.ImportFrom,
                             ast.FunctionDef, ast.ClassDef,
                             ast.Lambda, ast.DictComp, ast.SetComp,
                             ast.ListComp, ast.GeneratorExp)):
            raise ValueError(f"Unsupported operation detected: {type(node).__name__}")

    # Evaluate the parsed AST safely
    return _eval_node(parsed)

# Example usage (commented out for module cleanliness)
# if __name__ == "__main__":
#     expr = "3 + 4 * (2 - 1) / pi"
#     print(compute_expression(expr))