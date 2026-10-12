import ast
import operator

# Mapping of allowed AST operators to their corresponding functions
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

# Allowed literal node types
ALLOWED_LITERALS = (ast.Constant, ast.Num, ast.Str)


def _eval_node(node):
    """
    Recursively evaluate an AST node that has already been validated.
    """
    if isinstance(node, ast.Constant):  # Python 3.8+
        return node.value

    if isinstance(node, ast.Num):      # Python <3.8
        return node.n

    if isinstance(node, ast.Str):      # Python <3.8
        return node.s

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type not in ALLOWED_OPERATORS:
            raise ValueError("Unsupported binary operator")
        return ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type not in ALLOWED_OPERATORS:
            raise ValueError("Unsupported unary operator")
        return ALLOWED_OPERATORS[op_type](operand)

    # Should never reach here because of validation
    raise ValueError("Unsupported node type")


def _is_safe_node(node):
    """
    Recursively verify that the AST node contains only safe constructs.
    """
    if isinstance(node, ALLOWED_LITERALS):
        return True

    if isinstance(node, ast.BinOp) or isinstance(node, ast.UnaryOp):
        return _is_safe_node(node.left if hasattr(node, "left") else node.operand) \
               and _is_safe_node(node.right if hasattr(node, "right") else node.operand) \
               and type(node.op) in ALLOWED_OPERATORS

    # Disallow any other node types (e.g., Call, Name, Attribute)
    return False


def evaluate_user_code(code_str: str) -> str:
    """
    Safely evaluates a user-supplied Python script that contains only
    basic arithmetic and string operations.

    Parameters:
        code_str (str): The user-provided Python expression or script.

    Returns:
        str: The result of the evaluation converted to a string, or
             'Execution Blocked!' if the script is unsafe.
    """
    try:
        # Parse the code into an AST.  We only accept a single expression.
        parsed = ast.parse(code_str, mode="eval")
    except SyntaxError:
        return "Execution Blocked!"

    # Validate the AST
    if not all(_is_safe_node(node) for node in ast.walk(parsed)):
        return "Execution Blocked!"

    try:
        # Evaluate the expression in a completely empty environment
        result = _eval_node(parsed.body)
    except Exception:
        # Any runtime error (e.g., ZeroDivisionError) results in blocking
        return "Execution Blocked!"

    # Convert the result to string for consistent return type
    return str(result)