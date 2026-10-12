import ast
from typing import Any

# Allowed node types and operators for a minimal safe evaluator
ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Str,
    ast.NameConstant, # True/False/None
}

ALLOWED_BINOPS = {
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Mod,
    ast.Pow,
}

ALLOWED_UNARYOPS = {
    ast.UAdd,
    ast.USub,
}


def _eval(node: ast.AST) -> Any:
    """
    Recursively evaluate an AST node, allowing only safe constructs.
    Raises ValueError for any disallowed nodes or operations.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    if isinstance(node, (ast.Num, ast.Constant)):
        # In Python 3.8+, constants include numbers and strings
        return node.value

    if isinstance(node, ast.Str):  # Python <3.8
        return node.s

    if isinstance(node, ast.NameConstant):
        return node.value

    if isinstance(node, ast.BinOp):
        if type(node.op) not in ALLOWED_BINOPS:
            raise ValueError("Disallowed binary operator")
        left = _eval(node.left)
        right = _eval(node.right)

        if isinstance(node.op, ast.Add):
            return left + right
        elif isinstance(node.op, ast.Sub):
            return left - right
        elif isinstance(node.op, ast.Mult):
            return left * right
        elif isinstance(node.op, ast.Div):
            return left / right
        elif isinstance(node.op, ast.Mod):
            return left % right
        elif isinstance(node.op, ast.Pow):
            return left ** right

    if isinstance(node, ast.UnaryOp):
        if type(node.op) not in ALLOWED_UNARYOPS:
            raise ValueError("Disallowed unary operator")
        operand = _eval(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +operand
        elif isinstance(node.op, ast.USub):
            return -operand

    raise ValueError(f"Disallowed node type: {type(node).__name__}")


def evaluate_user_code(code_string: str) -> str:
    """
    Safely evaluates a user-provided Python expression that
    contains only simple arithmetic or string operations.
    
    Parameters:
        code_string (str): The Python expression to evaluate.

    Returns:
        str: The string representation of the result, or
             'Execution Blocked!' if the code is unsafe.
    """
    # Strip whitespace and ensure we are dealing with an expression
    trimmed = code_string.strip()
    if not trimmed:
        return "Execution Blocked!"

    try:
        # Parse the code in eval mode; this will produce an Expression node
        parsed = ast.parse(trimmed, mode='eval')
    except SyntaxError:
        return "Execution Blocked!"

    # Verify that the parsed tree only contains allowed nodes
    for node in ast.walk(parsed):
        if type(node) not in ALLOWED_NODES:
            return "Execution Blocked!"

    try:
        result = _eval(parsed)
        # Convert the result to string for uniform output
        return str(result)
    except Exception:
        # Any evaluation error is treated as a blocked execution
        return "Execution Blocked!"