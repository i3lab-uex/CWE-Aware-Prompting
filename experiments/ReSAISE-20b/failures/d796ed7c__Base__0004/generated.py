import ast
import operator as op

# Supported operators mapping to their functions
OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.FloorDiv: op.floordiv,
}

# Supported unary operators
UNARY_OPERATORS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed node types
ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Pow,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Mod,
    ast.FloorDiv,
    ast.UAdd,
    ast.USub,
    ast.LParen := None,  # placeholder for readability
)

def _check_node(node):
    """Recursively ensure all nodes are safe."""
    if not isinstance(node, ALLOWED_NODES):
        raise ValueError(f"Disallowed expression: {ast.dump(node)}")

    for child in ast.iter_child_nodes(node):
        _check_node(child)

def secure_math_eval(exp_str: str) -> float:
    """
    Safely evaluate a mathematical expression string.

    Parameters
    ----------
    exp_str : str
        The user supplied arithmetic expression.

    Returns
    -------
    float
        Result of the evaluated expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed syntax or unsafe operations.
    """
    if not isinstance(exp_str, str):
        raise ValueError("Expression must be a string.")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(exp_str, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Validate the AST contains only allowed nodes
    _check_node(parsed)

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, (ast.Num, ast.Constant)):
            # In Python 3.8+, constants are represented by ast.Constant
            value = node.n if hasattr(node, 'n') else node.value
            if not isinstance(value, (int, float)):
                raise ValueError(f"Unsupported constant type: {type(value)}")
            return value
        elif isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_type = type(node.op)
            if op_type not in OPERATORS:
                raise ValueError(f"Unsupported binary operator: {op_type}")
            return OPERATORS[op_type](left, right)
        elif isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            op_type = type(node.op)
            if op_type not in UNARY_OPERATORS:
                raise ValueError(f"Unsupported unary operator: {op_type}")
            return UNARY_OPERATORS[op_type](operand)
        else:
            raise ValueError(f"Unhandled node type: {type(node)}")

    return _eval(parsed)

# Example usage (commented out to avoid accidental execution)
# if __name__ == "__main__":
#     expr = "2 * (3 + 4) ** 2 / -5"
#     print(secure_math_eval(expr))