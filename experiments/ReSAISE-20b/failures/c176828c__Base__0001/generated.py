import ast
import operator

# Supported binary operators mapping from AST nodes to actual functions
_ALLOWED_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Supported unary operators mapping
_ALLOWED_UNOPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _eval(node):
    """
    Recursively evaluate an AST node that represents a mathematical expression.
    Only allows numbers and the operators defined in _ALLOWED_BINOPS and
    _ALLOWED_UNOPS.
    """
    if isinstance(node, ast.Num):          # For Python <3.8
        return node.n
    if isinstance(node, ast.Constant):     # For Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_BINOPS:
            raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
        left = _eval(node.left)
        right = _eval(node.right)
        return _ALLOWED_BINOPS[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_UNOPS:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        operand = _eval(node.operand)
        return _ALLOWED_UNOPS[type(node.op)](operand)

    if isinstance(node, ast.Expression):
        return _eval(node.body)

    if isinstance(node, ast.Paren):  # Not a real node type; parentheses are handled by grouping
        return _eval(node.value)

    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def calculate_expression(math_expr: str):
    """
    Evaluate a mathematical expression provided as a string.

    Parameters
    ----------
    math_expr : str
        The arithmetic expression to evaluate. Only numeric literals and the
        operators +, -, *, /, //, %, ** and parentheses are allowed.

    Returns
    -------
    result : float or int
        The computed value of the expression.

    Raises
    ------
    ValueError
        If the expression contains unsupported characters, unsafe commands,
        or is otherwise invalid.
    """
    if not isinstance(math_expr, str):
        raise ValueError("Input must be a string")

    # Strip whitespace for easier processing
    expr = math_expr.strip()

    if not expr:
        raise ValueError("Empty expression")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Walk the AST to ensure only allowed nodes are present
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Call, ast.Attribute, ast.Import, ast.ImportFrom,
                             ast.FunctionDef, ast.Lambda, ast.Dict, ast.ListComp,
                             ast.SetComp, ast.GeneratorExp)):
            raise ValueError(f"Unsupported operation: {type(node).__name__}")

    # Evaluate the expression safely
    return _eval(parsed.body)