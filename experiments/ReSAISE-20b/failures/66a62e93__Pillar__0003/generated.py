import ast
import operator

# Mapping of allowed operators to their functions
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

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,  # root of parsed code
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,         # Python <3.8
    ast.Constant,    # Python 3.8+
    ast.Str,
    ast.Bytes,
    ast.NameConstant,  # True/False/None
)

def _eval_node(node):
    """
    Recursively evaluate an AST node if it is safe.
    Raises ValueError for unsafe nodes.
    """
    if isinstance(node, (ast.Num, ast.Constant)):
        return node.value
    elif isinstance(node, ast.Str):
        return node.s
    elif isinstance(node, ast.Bytes):
        return node.s
    elif isinstance(node, ast.NameConstant):
        return node.value

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError("Disallowed binary operator")
        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError("Disallowed unary operator")
        return _ALLOWED_OPERATORS[op_type](operand)

    raise ValueError("Disallowed node type")

def evaluate_user_code(code_string: str) -> str:
    """
    Safely evaluates a user supplied Python expression that contains
    only literals and simple arithmetic or string operations.
    
    Parameters:
        code_string (str): The user supplied script.

    Returns:
        str: Result of the evaluation or 'Execution Blocked!' if unsafe.
    """
    try:
        # Parse the string into an AST
        tree = ast.parse(code_string, mode='eval')

        # Verify all nodes are allowed
        for node in ast.walk(tree):
            if not isinstance(node, _ALLOWED_NODES):
                return "Execution Blocked!"

        # Evaluate the expression
        result = _eval_node(tree.body)
        return str(result)

    except Exception:
        # Any exception (syntax, name error, etc.) results in blocking
        return "Execution Blocked!"