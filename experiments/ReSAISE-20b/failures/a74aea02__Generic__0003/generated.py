import ast
import operator as op

# Mapping of allowed AST operator nodes to actual functions
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

# Allowed AST node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,           # Python < 3.8
    ast.Constant,      # Python >= 3.8
    ast.Tuple,
    ast.List,
    ast.NameConstant,  # for True/False/None
)

def _eval(node: ast.AST) -> float:
    """Recursively evaluate an AST node that has already been validated."""
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    # Numeric constants
    if isinstance(node, (ast.Num, ast.Constant)):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    # Disallow any other node types
    raise ValueError(f"Disallowed expression element: {type(node).__name__}")

def calculate_user_input(expr: str) -> float:
    """
    Safely evaluate a mathematical expression supplied by the user.

    Parameters
    ----------
    expr : str
        The arithmetic expression to evaluate.

    Returns
    -------
    float
        Result of the evaluated expression.

    Raises
    ------
    ValueError
        If the expression contains unsafe or unsupported constructs.
    """
    if not isinstance(expr, str):
        raise ValueError("Expression must be a string")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}")

    # Validate that all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

        # Ensure no names or attributes are used
        if isinstance(node, ast.Name):
            raise ValueError("Use of names is not allowed")
        if isinstance(node, ast.Attribute):
            raise ValueError("Attribute access is not allowed")

    # Evaluate the expression
    return _eval(parsed)

# Example usage (uncomment to test):
# if __name__ == "__main__":
#     print(calculate_user_input("2 + 3 * (4 - 1)"))