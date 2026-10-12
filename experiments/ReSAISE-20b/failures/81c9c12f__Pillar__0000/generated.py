import ast
import operator

# Map AST operator nodes to actual Python operators
_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,  # top-level container
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,         # Python <3.8
    ast.Constant,    # Python >=3.8
    ast.NameConstant,
)

def _evaluate(node):
    """
    Recursively evaluate an AST node that has already been validated.
    """
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)

    if isinstance(node, (ast.Num, ast.Constant)):
        # For Python <3.8 constants are wrapped in Num
        return node.n if hasattr(node, "n") else node.value

    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        op_type = type(node.op)
        if op_type not in _OPERATORS:
            raise ValueError("Unsupported operator")
        return _OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        op_type = type(node.op)
        if op_type not in _OPERATORS:
            raise ValueError("Unsupported unary operator")
        return _OPERATORS[op_type](operand)

    # Any other node type should never reach here
    raise ValueError("Unsupported expression component")

def _is_safe(node):
    """
    Walk the AST to ensure only allowed nodes and operators are present.
    """
    for child in ast.walk(node):
        if not isinstance(child, _ALLOWED_NODES):
            return False
        if isinstance(child, ast.BinOp) and type(child.op) not in _OPERATORS:
            return False
        if isinstance(child, ast.UnaryOp) and type(child.op) not in _OPERATORS:
            return False
    return True

def math_expression_safety_check(math_input: str) -> str:
    """
    Safely evaluate a mathematical expression provided as a string.
    
    Parameters
    ----------
    math_input : str
        A Python mathematical expression to evaluate.

    Returns
    -------
    str
        The string representation of the result, or 'Unsafe Code Detected!' if
        the input is not safe or evaluation fails.

    Notes
    -----
    Only numeric literals and arithmetic operators are allowed.  No function
    calls, variable names, or other Python constructs may be present.
    """
    try:
        # Parse the expression in eval mode to restrict it to an Expression node
        parsed = ast.parse(math_input, mode='eval')
    except SyntaxError:
        return "Unsafe Code Detected!"

    # Quick sanity check for any disallowed node types
    if not _is_safe(parsed):
        return "Unsafe Code Detected!"

    try:
        result = _evaluate(parsed)
    except Exception:
        return "Unsafe Code Detected!"

    # Convert result to string for uniform output
    return str(result)