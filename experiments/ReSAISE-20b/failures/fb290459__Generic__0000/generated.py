import ast
import operator as op

# Allowed operators mapping for safe evaluation
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Expr,
    ast.Module,
)

def _eval_node(node):
    """
    Recursively evaluate an AST node, allowing only safe operations.
    """
    if isinstance(node, (ast.Num, ast.Constant)):
        # Ensure the value is numeric
        if not isinstance(node.value, (int, float)):
            raise ValueError("Non-numeric literal")
        return node.value

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator {op_type}")
        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported unary operator {op_type}")
        return _ALLOWED_OPERATORS[op_type](operand)

    raise ValueError(f"Unsupported expression component: {type(node).__name__}")

def process_math_expression(math_expr: str):
    """
    Evaluate a simple mathematical expression safely.

    Parameters
    ----------
    math_expr : str
        The input string containing the mathematical expression.

    Returns
    -------
    float or int
        Result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters, unsafe syntax,
        or cannot be evaluated safely.
    """
    if not isinstance(math_expr, str):
        raise ValueError("Input must be a string")

    # Strip whitespace and check for allowed characters
    stripped = math_expr.strip()
    if not stripped:
        raise ValueError("Empty expression")

    # Basic character whitelist: digits, operators, parentheses, dot, whitespace
    allowed_chars = "0123456789+-*/%() .\t\n\r"
    if any(c not in allowed_chars for c in stripped):
        raise ValueError("Expression contains illegal characters")

    try:
        # Parse expression into AST
        parsed = ast.parse(stripped, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Verify that all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed expression component: {type(node).__name__}")

    # Evaluate the parsed AST
    return _eval_node(parsed.body)

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(process_math_expression("2 + 3 * (4 - 1)"))   # Output: 11