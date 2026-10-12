import ast
import operator as op

# Supported operators mapping from AST nodes to functions
_ALLOWED_OPERATORS = {
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

# Supported functions from the math module
_ALLOWED_FUNCTIONS = {
    'sqrt': lambda x: __import__('math').sqrt(x),
    'sin': lambda x: __import__('math').sin(x),
    'cos': lambda x: __import__('math').cos(x),
    'tan': lambda x: __import__('math').tan(x),
    'log': lambda x, base=__import__('math').e: __import__('math').log(x, base),
    'exp': lambda x: __import__('math').exp(x),
    # add more functions as needed
}

def _eval(node):
    """
    Recursively evaluate an AST node in a safe manner.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    # Numbers (int or float)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        oper_type = type(node.op)
        if oper_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[oper_type](left, right)
        raise ValueError(f"Unsupported binary operator: {oper_type.__name__}")

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        oper_type = type(node.op)
        if oper_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[oper_type](operand)
        raise ValueError(f"Unsupported unary operator: {oper_type.__name__}")

    # Function calls
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function names are allowed")
        func_name = node.func.id
        if func_name not in _ALLOWED_FUNCTIONS:
            raise ValueError(f"Function '{func_name}' is not allowed")
        args = [_eval(arg) for arg in node.args]
        # No keyword arguments are allowed
        if node.keywords:
            raise ValueError("Keyword arguments are not supported")
        return _ALLOWED_FUNCTIONS[func_name](*args)

    # Parentheses are handled by the AST structure itself
    if isinstance(node, ast.Paren):
        return _eval(node.value)

    raise ValueError(f"Unsupported expression component: {ast.dump(node)}")

def compute_math_expression(expression_input: str):
    """
    Safely evaluate a mathematical expression provided as a string.

    Parameters
    ----------
    expression_input : str
        The mathematical expression to evaluate. It may contain numbers,
        binary operators (+, -, *, /, **, //, %), unary operators (+, -),
        parentheses, and calls to a restricted set of math functions.

    Returns
    -------
    float | int
        The evaluated result.

    Raises
    ------
    ValueError
        If the expression contains disallowed syntax, unsafe components,
        or is structurally incorrect.
    """
    try:
        # Parse expression into an AST node
        parsed = ast.parse(expression_input, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}")

    # Ensure the parsed AST only contains allowed nodes
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Module,)):
            continue  # module is top-level container
        if not isinstance(node, (
                ast.Expression,
                ast.Constant,
                ast.BinOp,
                ast.UnaryOp,
                ast.Call,
                ast.Name,
                ast.Load,
                ast.Expr,
        )):
            raise ValueError(f"Disallowed expression component: {type(node).__name__}")

    # Evaluate the parsed AST safely
    result = _eval(parsed)
    return result