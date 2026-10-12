import ast
import operator

# Mapping of allowed AST operator nodes to the corresponding Python functions
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

# Allowed AST node types
_ALLOWED_NODES = (
    ast.Expression,  # root
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Call,
    ast.Name,
    ast.Load,
    ast.Expr,
)

# Names that are allowed in expressions (e.g., math functions)
_ALLOWED_NAMES = {
    # No built‑in names allowed; we only allow constants if needed
}

def _eval(node):
    """Recursively evaluate an AST node, only allowing safe constructs."""
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    if isinstance(node, (ast.Num, ast.Constant)):
        # For numeric literals
        return node.n if isinstance(node, ast.Num) else node.value

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return _ALLOWED_OPERATORS[op_type](operand)

    if isinstance(node, ast.Call):
        # Disallow function calls for safety
        raise ValueError("Function calls are not allowed")

    if isinstance(node, ast.Name):
        # Only allow constants like 'pi' or 'e' if explicitly added
        name = node.id
        if name in _ALLOWED_NAMES:
            return _ALLOWED_NAMES[name]
        raise ValueError(f"Use of undefined name: {name}")

    # Any other node type is disallowed
    raise ValueError(f"Disallowed expression: {ast.dump(node)}")

def compute_expression(expression_input: str):
    """
    Safely evaluate a simple mathematical expression.

    Parameters
    ----------
    expression_input : str
        The string containing the mathematical expression to evaluate.

    Returns
    -------
    float or int
        Result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters or cannot be safely evaluated.
    """
    if not isinstance(expression_input, str):
        raise ValueError("Input must be a string")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(expression_input, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Verify that the parsed tree contains only allowed node types
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed syntax element: {type(node).__name__}")

    # Evaluate the expression
    return _eval(parsed)

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     expr = "2 * (3 + 4) ** 2 / 5 - 7"
#     print(compute_expression(expr))