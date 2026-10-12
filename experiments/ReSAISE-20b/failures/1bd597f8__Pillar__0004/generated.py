import ast
import operator
import math

# Mapping of allowed operators to their functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
    ast.USub: operator.neg,
}

# Allowed names from the math module
_ALLOWED_NAMES = {
    name: getattr(math, name) for name in dir(math) if not name.startswith("_")
}

def _eval(node):
    """
    Recursively evaluate an AST node that represents a numeric expression.
    Raises ValueError for any disallowed nodes or operations.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    elif isinstance(node, ast.Num):  # For Python <3.8
        return node.n
    elif isinstance(node, ast.Constant):  # For Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")
    elif isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError("Operator not allowed")
        left = _eval(node.left)
        right = _eval(node.right)
        return _ALLOWED_OPERATORS[type(node.op)](left, right)
    elif isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError("Unary operator not allowed")
        operand = _eval(node.operand)
        return _ALLOWED_OPERATORS[type(node.op)](operand)
    elif isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name) or node.func.id not in _ALLOWED_NAMES:
            raise ValueError("Function call not allowed")
        func = _ALLOWED_NAMES[node.func.id]
        args = [_eval(arg) for arg in node.args]
        return func(*args)
    elif isinstance(node, ast.Name):
        if node.id in _ALLOWED_NAMES:
            return _ALLOWED_NAMES[node.id]
        raise ValueError("Name not allowed")
    else:
        raise ValueError(f"Unsupported AST node: {type(node).__name__}")

def execute_user_input(user_input: str) -> str:
    """
    Safely evaluate a simple numeric expression supplied by the user.
    Returns the result as a string or 'Processing Failed!' on any error.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(user_input, mode="eval")
        # Ensure the tree contains only allowed nodes
        for node in ast.walk(parsed):
            if not isinstance(node, (
                ast.Expression,
                ast.BinOp,
                ast.UnaryOp,
                ast.Num,          # Python <3.8
                ast.Constant,     # Python >=3.8
                ast.Call,
                ast.Name,
            )):
                raise ValueError("Disallowed syntax detected")
        # Evaluate the parsed expression
        result = _eval(parsed)
        return str(result)
    except Exception:
        # Catch any parsing or evaluation error
        return "Processing Failed!"