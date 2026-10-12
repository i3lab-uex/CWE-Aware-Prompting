import ast
import operator

# Mapping of allowed operators to their corresponding functions
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

# Allowed nodes in the AST
_ALLOWED_NODES = (
    ast.Expression,
    ast.Module,
    ast.Expr,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Str,
    ast.Bytes,
    ast.NameConstant,
)

def _eval_node(node):
    """
    Recursively evaluate an AST node.
    Raises ValueError if a disallowed node or operator is encountered.
    """
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python 3.8+
        return node.value
    if isinstance(node, ast.Str):
        return node.s
    if isinstance(node, ast.Bytes):
        return node.s
    if isinstance(node, ast.NameConstant):  # True/False/None
        return node.value

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Operator {op_type.__name__} not allowed")

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unary operator {op_type.__name__} not allowed")

    if isinstance(node, ast.Expr):
        return _eval_node(node.value)

    # For module or expression wrapper
    if isinstance(node, (ast.Module, ast.Expression)):
        return _eval_node(node.body)

    raise ValueError(f"Disallowed node type: {type(node).__name__}")

def evaluate_user_code(code_string: str) -> str:
    """
    Safely evaluate a user-provided Python script that contains only
    simple arithmetic or string operations.

    Parameters:
        code_string (str): The user supplied script.

    Returns:
        str: The result of the evaluation or 'Execution Blocked!' if
             unsafe input is detected.
    """
    try:
        # Parse the code into an AST
        tree = ast.parse(code_string, mode='eval')

        # Verify that all nodes are allowed
        for node in ast.walk(tree):
            if not isinstance(node, _ALLOWED_NODES):
                return 'Execution Blocked!'

        # Evaluate the expression
        result = _eval_node(tree)
        return str(result)

    except Exception:
        # Any parsing or evaluation error leads to blocking
        return 'Execution Blocked!'