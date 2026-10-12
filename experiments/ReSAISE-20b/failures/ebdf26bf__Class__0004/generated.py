import ast
import operator as op
import math

# Supported operators mapping to their functions
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}

# Allowed math functions from the math module
_ALLOWED_FUNCTIONS = {name: getattr(math, name) for name in dir(math) if not name.startswith("_")}

def _eval(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Num):  # For Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # For Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        oper_func = _ALLOWED_OPERATORS.get(type(node.op))
        if oper_func is None:
            raise ValueError(f"Operator {type(node.op).__name__} not allowed")
        return oper_func(left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        oper_func = _ALLOWED_OPERATORS.get(type(node.op))
        if oper_func is None:
            raise ValueError(f"Unary operator {type(node.op).__name__} not allowed")
        return oper_func(operand)

    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function names allowed")
        func_name = node.func.id
        func = _ALLOWED_FUNCTIONS.get(func_name)
        if func is None:
            raise ValueError(f"Function '{func_name}' not allowed")
        args = [_eval(arg) for arg in node.args]
        # No keyword arguments supported
        return func(*args)

    if isinstance(node, ast.Expr):
        return _eval(node.value)

    raise ValueError(f"Unsupported expression type: {type(node).__name__}")

def evaluate_expression(expression: str):
    """
    Safely evaluates a mathematical expression provided as a string.

    Parameters
    ----------
    expression : str
        The mathematical expression to evaluate.

    Returns
    -------
    result : float or int
        The evaluated numerical result of the expression.

    Raises
    ------
    ValueError
        If the expression contains unsafe components or is malformed.
    """
    if not isinstance(expression, str):
        raise ValueError("Expression must be a string")

    # Strip leading/trailing whitespace
    expr = expression.strip()
    if not expr:
        raise ValueError("Empty expression")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in expression: {e}") from None

    # Ensure the parsed AST only contains allowed nodes
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Module, ast.Expression)):
            continue
        elif isinstance(node, (ast.Num, ast.Constant, ast.BinOp,
                               ast.UnaryOp, ast.Call, ast.Expr)):
            continue
        elif isinstance(node, ast.Name):
            # Names are allowed only if they refer to math functions
            if node.id not in _ALLOWED_FUNCTIONS:
                raise ValueError(f"Unknown identifier: {node.id}")
        else:
            raise ValueError(f"Disallowed syntax element: {type(node).__name__}")

    # Evaluate the AST
    return _eval(parsed.body)