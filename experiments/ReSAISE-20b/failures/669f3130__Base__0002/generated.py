import ast
import operator

# Allowed binary operators mapping from AST nodes to Python functions
_ALLOWED_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.FloorDiv: operator.floordiv,
}

# Allowed unary operators mapping
_ALLOWED_UNARYOPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _eval_node(node):
    """Recursively evaluate an AST node representing a numeric expression."""
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Numbers
    if isinstance(node, (ast.Constant)):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")

    # Unary operations (+/-)
    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_UNARYOPS:
            raise ValueError("Unsupported unary operator")
        operand = _eval_node(node.operand)
        return _ALLOWED_UNARYOPS[op_type](operand)

    # Binary operations
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_BINOPS:
            raise ValueError("Unsupported binary operator")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return _ALLOWED_BINOPS[op_type](left, right)

    # Parentheses are handled by the AST structure itself
    if isinstance(node, ast.Paren):
        return _eval_node(node.value)

    # Disallow any other node types (e.g., function calls, attributes)
    raise ValueError("Unsupported expression component")

def exec_calculation(calc_string: str) -> str:
    """
    Safely evaluate a basic arithmetic expression provided as a string.

    Parameters
    ----------
    calc_string : str
        The user-provided arithmetic expression. Only numbers and the operators
        +, -, *, /, %, **, //, and parentheses are allowed.

    Returns
    -------
    str
        The string representation of the numeric result, or 'Computation Error!'
        if the expression is invalid or contains disallowed constructs.
    """
    try:
        # Parse the string into an AST node; mode='eval' ensures it's an expression
        parsed = ast.parse(calc_string, mode="eval")

        # Walk the AST to ensure no disallowed nodes are present
        for node in ast.walk(parsed):
            if isinstance(node, (ast.Call, ast.Attribute, ast.Import,
                                 ast.ImportFrom, ast.FunctionDef, ast.ClassDef,
                                 ast.Lambda, ast.Name)):
                raise ValueError("Disallowed expression component")

        result = _eval_node(parsed)
        # Convert result to string; format floats without trailing .0 when possible
        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        return str(result)
    except Exception:
        # Any error (parsing, evaluation, disallowed nodes) results in a generic message
        return "Computation Error!"