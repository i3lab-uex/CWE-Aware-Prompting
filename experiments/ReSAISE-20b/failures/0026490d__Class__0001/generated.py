import ast
import operator as op

# Supported operators mapping from AST node to actual operation
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed unary and binary operator nodes
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,           # Python < 3.8
    ast.Constant,      # Python >= 3.8
    ast.Name,
    ast.Load,
)

# Whitelist of names that can be used in the expression
_ALLOWED_NAMES = {
    'pi': 3.141592653589793,
    'e' : 2.718281828459045,
}

def _eval(node):
    """
    Recursively evaluate an AST node, ensuring only safe operations are performed.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    if isinstance(node, ast.Constant):   # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.Num):        # Python < 3.8
        return node.n

    if isinstance(node, ast.Name):
        if node.id in _ALLOWED_NAMES:
            return _ALLOWED_NAMES[node.id]
        raise ValueError(f"Use of undefined name '{node.id}' is not allowed")

    if isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError(f"Operator {type(node.op).__name__} not allowed")
        left = _eval(node.left)
        right = _eval(node.right)
        return _ALLOWED_OPERATORS[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unary operator {type(node.op).__name__} not allowed")
        operand = _eval(node.operand)
        return _ALLOWED_OPERATORS[type(node.op)](operand)

    raise ValueError(f"Unsupported expression component: {type(node).__name__}")

def evaluate_expression(expr: str):
    """
    Safely evaluates a mathematical expression containing numbers,
    basic arithmetic operators, and optional constants 'pi' or 'e'.

    Parameters
    ----------
    expr : str
        The arithmetic expression to evaluate.

    Returns
    -------
    float or int
        The result of the evaluated expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters, unsafe nodes,
        or evaluation fails for any reason.
    """
    if not isinstance(expr, str):
        raise ValueError("Expression must be a string")

    # Strip whitespace to avoid accidental injection via spaces
    expr = expr.strip()
    if not expr:
        raise ValueError("Empty expression")

    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Validate node types
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed syntax element: {type(node).__name__}")

    # Evaluate safely
    try:
        result = _eval(parsed)
    except ZeroDivisionError as exc:
        raise ValueError("Division by zero") from exc
    except Exception as exc:
        # Wrap any other exception in ValueError to keep API consistent
        raise ValueError(f"Evaluation error: {exc}") from exc

    return result