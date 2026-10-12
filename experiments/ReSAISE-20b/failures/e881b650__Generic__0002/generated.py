import ast
import operator

# Supported operators mapping from AST nodes to Python functions
_OPERATOR_MAP = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Allowed unary operators
_UNARY_MAP = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _eval_node(node):
    """
    Recursively evaluate an AST node.
    Raises ValueError for unsupported nodes or operations.
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
        if op_type in _OPERATOR_MAP:
            return _OPERATOR_MAP[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _UNARY_MAP:
            return _UNARY_MAP[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    if isinstance(node, ast.Paren):
        return _eval_node(node.value)

    # Disallow names, calls, attributes, etc.
    if isinstance(node, (ast.Name, ast.Call, ast.Attribute, ast.Subscript)):
        raise ValueError(f"Unsupported expression element: {type(node).__name__}")

    # Disallow any other node types
    raise ValueError(f"Unsupported AST node: {type(node).__name__}")

def compute_expression(expr: str):
    """
    Safely evaluate a mathematical expression given as a string.
    
    Parameters
    ----------
    expr : str
        The expression to evaluate. Supports +, -, *, /, //, %, ** and parentheses.
    
    Returns
    -------
    int | float
        The result of the evaluated expression.
    
    Raises
    ------
    ValueError
        If the expression contains unsupported operators, unsafe code,
        or if evaluation fails.
    """
    try:
        # Parse expression into an AST
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Ensure the parsed tree contains only allowed nodes
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef,
                             ast.ClassDef, ast.Lambda, ast.Global,
                             ast.Nonlocal)):
            raise ValueError(f"Disallowed statement: {type(node).__name__}")

    return _eval_node(parsed)

# Example usage:
if __name__ == "__main__":
    examples = [
        "2 + 3 * (4 - 1)",
        "-5 ** 2",
        "10 / 3",
        "(8 + 2) // 5",
    ]
    for e in examples:
        print(f"{e} = {compute_expression(e)}")