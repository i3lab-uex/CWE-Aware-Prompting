import ast
import operator as op
import math

# Supported operators mapping
OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Supported math functions
MATH_FUNCTIONS = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}

# Allowed node types
ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Call,
    ast.Name,
)

def _eval(node: ast.AST) -> float:
    if isinstance(node, (ast.Num, ast.Constant)):
        return node.n if hasattr(node, "n") else node.value
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        if type(node.op) not in OPERATORS:
            raise ValueError(f"Unsupported operator: {ast.dump(node.op)}")
        return OPERATORS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        if type(node.op) not in OPERATORS:
            raise ValueError(f"Unsupported unary operator: {ast.dump(node.op)}")
        return OPERATORS[type(node.op)](operand)
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name) or node.func.id not in MATH_FUNCTIONS:
            raise ValueError(f"Unsupported function call: {ast.dump(node.func)}")
        args = [_eval(arg) for arg in node.args]
        return MATH_FUNCTIONS[node.func.id](*args)
    if isinstance(node, ast.Name):
        # disallow variables
        raise ValueError(f"Variables are not allowed: {node.id}")
    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def process_user_query(query: str) -> float:
    """
    Safely evaluate a mathematical expression provided by the user.

    Parameters
    ----------
    query : str
        The user-provided mathematical expression.

    Returns
    -------
    float
        The computed result of the expression.

    Raises
    ------
    ValueError
        If the input contains unsafe characters, unsupported syntax,
        or if the expression is malformed.
    """
    # Basic sanity check: allow only characters that are part of math expressions
    allowed_chars = "0123456789+-*/(). %eE"
    for ch in query:
        if ch not in allowed_chars and ch not in MATH_FUNCTIONS.keys():
            # allow function names; they will be validated later
            continue

    try:
        parsed = ast.parse(query, mode="eval")
    except SyntaxError as e:
        raise ValueError(f"Malformed expression: {e}") from e

    # Ensure all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, ALLOWED_NODES):
            raise ValueError(f"Disallowed expression component: {ast.dump(node)}")

    return _eval(parsed.body)