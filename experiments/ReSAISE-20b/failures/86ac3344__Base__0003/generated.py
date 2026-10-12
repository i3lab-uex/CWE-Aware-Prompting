import ast
import operator

# Allowed binary operators mapped to the real Python functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Allowed unary operators
_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # for Python <3.8
    ast.Constant,     # for Python >=3.8
    ast.Expr,
    ast.Call,         # we will reject calls explicitly
    ast.Name,         # reject names
    ast.Attribute,    # reject attributes
)

def _check_node(node):
    """
    Recursively verify that the AST node contains only safe constructs.
    Raise ValueError if any disallowed node is found.
    """
    # Reject calls, names or attributes entirely
    if isinstance(node, (ast.Call, ast.Name, ast.Attribute)):
        raise ValueError(f"Disallowed construct: {type(node).__name__}")

    # Check the node type
    if not isinstance(node, _ALLOWED_NODES):
        raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Recursively check child nodes
    for child in ast.iter_child_nodes(node):
        _check_node(child)

def _eval_ast(node):
    """
    Evaluate the AST node recursively.
    """
    if isinstance(node, ast.Expression):
        return _eval_ast(node.body)

    # Numbers
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _eval_ast(node.left)
        right = _eval_ast(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        return _ALLOWED_OPERATORS[op_type](left, right)

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        operand = _eval_ast(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_UNARY_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return _ALLOWED_UNARY_OPERATORS[op_type](operand)

    # Should never reach here due to earlier checks
    raise ValueError(f"Unhandled node type: {type(node).__name__}")

def secure_eval_expression(exp: str):
    """
    Safely evaluate a mathematical expression containing only numbers
    and the operators +, -, *, /, //, %, ** and parentheses.

    Parameters:
        exp (str): The user supplied expression.

    Returns:
        int or float: The result of evaluating the expression.

    Raises:
        ValueError: If the expression contains disallowed characters or
                    unsafe constructs.
    """
    if not isinstance(exp, str):
        raise ValueError("Expression must be a string")

    # Quick regex to catch obvious non-numeric characters (optional)
    import re
    if not re.fullmatch(r"[0-9+\-*/%().\s]+", exp):
        raise ValueError("Expression contains invalid characters")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(exp, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}")

    # Ensure only safe nodes are present
    _check_node(parsed)

    # Evaluate the AST safely
    return _eval_ast(parsed)