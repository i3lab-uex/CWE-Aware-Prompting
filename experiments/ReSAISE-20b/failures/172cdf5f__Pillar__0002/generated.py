import ast
import operator

# Mapping of allowed AST operators to the actual Python functions
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

def _eval_node(node):
    """
    Recursively evaluate an AST node that has already been validated.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Literal values (int, float, str)
    if isinstance(node, ast.Constant):
        return node.value

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type not in ALLOWED_OPERATORS:
            raise ValueError("Unsupported binary operator")
        return ALLOWED_OPERATORS[op_type](left, right)

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type not in ALLOWED_OPERATORS:
            raise ValueError("Unsupported unary operator")
        return ALLOWED_OPERATORS[op_type](operand)

    # Parenthesized expressions
    if isinstance(node, ast.Paren):
        return _eval_node(node.value)

    raise ValueError("Unsupported AST node")

def _validate_ast(tree):
    """
    Walk the AST and ensure only safe nodes are present.
    Raises ValueError if an unsafe node is found.
    """
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.Expr)):
            continue
        elif isinstance(node, ast.Expression):
            continue
        elif isinstance(node, ast.Constant):
            if not isinstance(node.value, (int, float, str)):
                raise ValueError("Only int, float, and str literals are allowed")
        elif isinstance(node, ast.BinOp):
            if type(node.op) not in ALLOWED_OPERATORS:
                raise ValueError("Unsupported binary operator")
        elif isinstance(node, ast.UnaryOp):
            if type(node.op) not in ALLOWED_OPERATORS:
                raise ValueError("Unsupported unary operator")
        elif isinstance(node, (ast.Num, ast.Str)):
            # Deprecated in Python 3.8+, but handle just in case
            continue
        else:
            raise ValueError(f"Disallowed AST node type: {type(node).__name__}")

def process_user_script(code_str: str) -> str:
    """
    Safely evaluate a user-supplied Python expression that may contain
    simple arithmetic or string operations.

    Parameters:
        code_str (str): The user-provided Python script.

    Returns:
        str: Result of the evaluation as a string, or 'Execution Blocked!'
             if the script contains unsafe content.
    """
    try:
        # Parse into an AST
        tree = ast.parse(code_str, mode="eval")

        # Validate the AST for safety
        _validate_ast(tree)

        # Evaluate the expression
        result = _eval_node(tree)
        return str(result)

    except Exception:
        # Any exception (parsing, validation or evaluation) leads to blocking
        return "Execution Blocked!"