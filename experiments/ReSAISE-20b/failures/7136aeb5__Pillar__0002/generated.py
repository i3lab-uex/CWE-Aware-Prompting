import ast
import operator

# Allowed operators mapping
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # For Python < 3.8
    ast.Constant,     # For Python >= 3.8
    ast.Pow,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Mod,
    ast.UAdd,
    ast.USub,
    ast.LParen,       # Not an actual node; handled by parser
)

def _evaluate(node):
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        return _ALLOWED_OPERATORS[op_type](left, right)
    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return _ALLOWED_OPERATORS[op_type](operand)
    raise ValueError(f"Unsupported expression node: {type(node).__name__}")

def evaluate_expression_safely(expr: str):
    """
    Safely evaluates a mathematical expression containing only numbers and
    the operators +, -, *, /, **, %, unary +/-, and parentheses.
    
    Parameters
    ----------
    expr : str
        The expression to evaluate.

    Returns
    -------
    int or float
        Result of the evaluation.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters, unsupported operators,
        or is otherwise malformed.
    """
    # Strip whitespace to prevent accidental injection
    expr = expr.strip()
    
    if not expr:
        raise ValueError("Empty expression")

    # Parse into an AST
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Ensure the parsed tree only contains allowed nodes
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed expression element: {type(node).__name__}")

    # Evaluate recursively
    return _evaluate(parsed.body)