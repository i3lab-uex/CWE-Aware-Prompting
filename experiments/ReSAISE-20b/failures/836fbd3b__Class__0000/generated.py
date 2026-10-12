import ast
import operator as op

# Allowed operators mapping
_allowed_operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.FloorDiv: op.floordiv,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed functions (optional)
_allowed_functions = {
    'abs': abs,
    'round': round,
    # add more safe math functions if needed
}

def _eval(node):
    """
    Recursively evaluate an AST node ensuring only safe operations are performed.
    """
    if isinstance(node, ast.Num):          # <number>
        return node.n
    elif isinstance(node, ast.Constant):   # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")
    elif isinstance(node, ast.BinOp):      # <left> <op> <right>
        if type(node.op) not in _allowed_operators:
            raise ValueError("Unsupported binary operator")
        left = _eval(node.left)
        right = _eval(node.right)
        return _allowed_operators[type(node.op)](left, right)
    elif isinstance(node, ast.UnaryOp):    # <op> <operand>
        if type(node.op) not in _allowed_operators:
            raise ValueError("Unsupported unary operator")
        operand = _eval(node.operand)
        return _allowed_operators[type(node.op)](operand)
    elif isinstance(node, ast.Call):       # <func>(...)
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function calls allowed")
        func_name = node.func.id
        if func_name not in _allowed_functions:
            raise ValueError(f"Function '{func_name}' is not allowed")
        args = [_eval(arg) for arg in node.args]
        return _allowed_functions[func_name](*args)
    elif isinstance(node, ast.Expr):
        return _eval(node.value)
    else:
        raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def compute_expression_safely(user_expr: str) -> str:
    """
    Safely evaluate a simple mathematical expression provided by the user.
    
    Parameters
    ----------
    user_expr : str
        The user's expression to evaluate.

    Returns
    -------
    str
        String representation of the computed result, or 'Processing Failed!'
        if evaluation fails or input is unsafe.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(user_expr, mode='eval')
        # Ensure the top node is an expression
        if not isinstance(parsed.body, (ast.Expression, ast.Expr)):
            return 'Processing Failed!'
        # Evaluate the parsed expression safely
        result = _eval(parsed.body)
        return str(result)
    except Exception:
        # Any error (syntax, unsafe operation, division by zero, etc.)
        return 'Processing Failed!'