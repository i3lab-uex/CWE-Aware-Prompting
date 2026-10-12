import ast
import operator as op

# Mapping of allowed AST operators to actual functions
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
    ast.Expression,  # top-level expression node
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,         # Python 3.7- (for literal numbers)
    ast.Constant,    # Python 3.8+ for literals
    ast.Call,        # we will explicitly disallow calls
)

def _eval_node(node):
    """
    Recursively evaluate an AST node, ensuring only allowed constructs are used.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Numbers
    if isinstance(node, (ast.Num, ast.Constant)):
        value = node.n if hasattr(node, 'n') else node.value
        if not isinstance(value, (int, float)):
            raise ValueError(f"Unsupported constant type: {type(value).__name__}")
        return value

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Operator {op_type.__name__} not allowed")
        return _ALLOWED_OPERATORS[op_type](left, right)

    # Unary operations (+/-)
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unary operator {op_type.__name__} not allowed")
        return _ALLOWED_OPERATORS[op_type](operand)

    # Disallow any other node types
    raise ValueError(f"Disallowed expression: {ast.dump(node)}")

def evaluate_math_expression(expr: str):
    """
    Safely evaluates a simple mathematical expression.

    Parameters
    ----------
    expr : str
        The math expression to evaluate.

    Returns
    -------
    int | float
        Result of the computation.

    Raises
    ------
    ValueError
        If expression contains illegal characters, unsafe usage, or cannot be evaluated.
    """
    # Strip whitespace
    expr = expr.strip()
    if not expr:
        raise ValueError("Empty expression")

    # Parse expression into an AST
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Ensure only allowed node types appear
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            # Additional check: disallow function calls or attribute access
            if isinstance(node, ast.Call):
                raise ValueError("Function calls are not allowed")
            if isinstance(node, ast.Attribute):
                raise ValueError("Attribute access is not allowed")
            if isinstance(node, ast.Name):
                raise ValueError(f"Unknown identifier: {node.id}")
            if isinstance(node, ast.Subscript):
                raise ValueError("Subscripts are not allowed")
            # Any other disallowed node
            raise ValueError(f"Disallowed expression component: {ast.dump(node)}")

    # Evaluate the safe AST
    return _eval_node(parsed)

# Example usage (uncomment to test):
# if __name__ == "__main__":
#     print(evaluate_math_expression("2 + 3 * (4 - 1) / 5 ** 2"))