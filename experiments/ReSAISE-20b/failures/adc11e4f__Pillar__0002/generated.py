import ast
import operator

# Mapping of allowed operators to their corresponding functions
ALLOWED_OPERATORS = {
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

def _eval(node):
    """
    Recursively evaluate an AST node that represents a mathematical expression.
    Only nodes listed in ALLOWED_OPERATORS or literals are permitted.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    if isinstance(node, ast.Num):  # Python <3.8
        return node.n

    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in ALLOWED_OPERATORS:
            return ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError("Unsupported binary operator")

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in ALLOWED_OPERATORS:
            return ALLOWED_OPERATORS[op_type](operand)
        raise ValueError("Unsupported unary operator")

    # Disallow any other node types (e.g., function calls, attribute access)
    raise ValueError("Disallowed expression component")

def process_expression(expression_str: str) -> str:
    """
    Safely evaluate a user-provided arithmetic expression.
    
    Parameters
    ----------
    expression_str : str
        The mathematical expression supplied by the user.
    
    Returns
    -------
    str
        Result of the computation as a string, or 'Computation Error!'
        if the expression is unsafe or evaluation fails.
    """
    try:
        # Parse the string into an AST node; fail if syntax is invalid
        parsed = ast.parse(expression_str, mode='eval')
        
        # Ensure the AST contains only allowed nodes
        for node in ast.walk(parsed):
            if isinstance(node, (ast.Call, ast.Attribute, ast.Import,
                                 ast.ImportFrom, ast.Lambda, ast.FunctionDef,
                                 ast.ClassDef, ast.Module, ast.Exec)):
                raise ValueError("Unsafe construct detected")

        result = _eval(parsed)
        return str(result)

    except Exception:
        # Any exception (syntax error, unsafe node, division by zero, etc.)
        return 'Computation Error!'