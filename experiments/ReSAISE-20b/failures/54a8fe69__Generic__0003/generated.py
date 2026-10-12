import ast
import operator

# Map AST operators to actual Python functions
_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Map AST unary operators to functions
_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Call,
    ast.Name,
    ast.Load,
    ast.Tuple,
    ast.List,
)

# Whitelist of safe names (currently none, but can be extended)
_SAFE_NAMES = {}

def evaluate_user_expression(expression: str):
    """
    Safely evaluates a mathematical expression supplied by the user.

    Parameters
    ----------
    expression : str
        The string containing the mathematical expression to evaluate.

    Returns
    -------
    int | float
        Result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters or syntax.
    """
    # Basic sanity check: ensure only allowed characters (digits, operators, whitespace, parentheses)
    if not isinstance(expression, str):
        raise ValueError("Expression must be a string.")
    allowed_chars = "0123456789+-*/%(). "
    if any(ch not in allowed_chars for ch in expression):
        raise ValueError("Expression contains invalid characters.")

    try:
        parsed = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from None

    # Recursively validate the AST
    def _validate(node):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed expression: {ast.dump(node)}")
        for child in ast.iter_child_nodes(node):
            _validate(child)

    _validate(parsed.body)

    # Evaluate the AST safely
    def _eval(node):
        if isinstance(node, ast.Constant):  # Python >=3.8
            if isinstance(node.value, (int, float)):
                return node.value
            else:
                raise ValueError(f"Unsupported constant type: {type(node.value)}")
        if isinstance(node, ast.Num):  # Python <3.8
            return node.n

        if isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_type = type(node.op)
            if op_type not in _OPERATORS:
                raise ValueError(f"Unsupported binary operator: {op_type}")
            return _OPERATORS[op_type](left, right)

        if isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            op_type = type(node.op)
            if op_type not in _UNARY_OPERATORS:
                raise ValueError(f"Unsupported unary operator: {op_type}")
            return _UNARY_OPERATORS[op_type](operand)

        raise ValueError(f"Unsupported expression node: {ast.dump(node)}")

    return _eval(parsed.body)

# Example usage:
if __name__ == "__main__":
    try:
        print(evaluate_user_expression("2 + 3 * (4 - 1)"))  # Should output 11
    except ValueError as e:
        print(f"Error: {e}")