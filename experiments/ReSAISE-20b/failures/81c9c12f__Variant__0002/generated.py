import ast
import operator

# Mapping of allowed AST nodes to their corresponding Python operators/functions
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

# Whitelist of node types that are considered safe
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # For Python <3.8
    ast.Constant,     # For Python >=3.8
    ast.UnaryOp,
    ast.Tuple,
    ast.List,
)

def _eval_node(node):
    """
    Recursively evaluate an AST node that has been validated as safe.
    """
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError("Unsupported binary operator")
        return _ALLOWED_OPERATORS[op_type](left, right)
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError("Unsupported unary operator")
        return _ALLOWED_OPERATORS[op_type](operand)
    if isinstance(node, (ast.Tuple, ast.List)):
        return [_eval_node(e) for e in node.elts]
    raise ValueError("Unsupported AST node")

def math_expression_safety_check(math_input: str) -> str:
    """
    Safely evaluate a mathematical expression provided as a string.
    
    Parameters
    ----------
    math_input : str
        The user supplied expression.

    Returns
    -------
    str
        The string representation of the evaluated result or an error message.
    
    Raises
    ------
    ValueError
        If the expression contains unsafe content or evaluation fails.
    """
    try:
        # Parse the input into an AST expression
        parsed = ast.parse(math_input, mode='eval')
    except SyntaxError:
        return "Unsafe Code Detected!"

    # Validate that only allowed nodes are present
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            return "Unsafe Code Detected!"
        # Disallow any Name or Attribute nodes (would allow function calls, etc.)
        if isinstance(node, ast.Name) or isinstance(node, ast.Attribute):
            return "Unsafe Code Detected!"
        # Disallow any Call nodes
        if isinstance(node, ast.Call):
            return "Unsafe Code Detected!"

    try:
        result = _eval_node(parsed.body)
        return str(result)
    except Exception:
        # Any exception during evaluation is treated as unsafe
        return "Unsafe Code Detected!"