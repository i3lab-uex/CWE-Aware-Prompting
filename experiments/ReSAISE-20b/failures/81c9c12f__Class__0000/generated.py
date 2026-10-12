import ast
import math

# Allowed nodes for the AST (numbers, unary/binary ops, function calls)
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,            # Python <3.8
    ast.Constant,       # Python >=3.8
    ast.Name,
    ast.Call,
)

# Allowed operators mapped to actual functions
_ALLOWED_OPERATORS = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b,
    ast.Pow: lambda a, b: a ** b,
    ast.Mod: lambda a, b: a % b,
    ast.FloorDiv: lambda a, b: a // b,
    ast.UAdd: lambda a: +a,
    ast.USub: lambda a: -a,
}

# Allowed math functions (subset of the math module)
_ALLOWED_FUNCTIONS = {
    name: getattr(math, name) for name in [
        'sqrt', 'sin', 'cos', 'tan', 'log', 'exp', 'fabs',
        'floor', 'ceil', 'factorial', 'degrees', 'radians'
    ]
}

def _eval_node(node):
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numeric constants are allowed")
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_func = _ALLOWED_OPERATORS.get(type(node.op))
        if op_func is None:
            raise ValueError("Operator not allowed")
        return op_func(left, right)
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_func = _ALLOWED_OPERATORS.get(type(node.op))
        if op_func is None:
            raise ValueError("Unary operator not allowed")
        return op_func(operand)
    if isinstance(node, ast.Call):
        func_name = getattr(node.func, 'id', None)
        if func_name not in _ALLOWED_FUNCTIONS:
            raise ValueError("Function not allowed")
        args = [_eval_node(arg) for arg in node.args]
        return _ALLOWED_FUNCTIONS[func_name](*args)
    if isinstance(node, ast.Name):
        # Allow only constants from math module (e.g., pi, e)
        if node.id in {'pi', 'e'}:
            return getattr(math, node.id)
        raise ValueError("Name not allowed")
    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def math_expression_safety_check(math_input: str) -> str:
    """
    Safely evaluate a mathematical expression provided as a string.
    
    Parameters
    ----------
    math_input : str
        A user supplied Python expression involving numbers, basic arithmetic,
        and a whitelist of math functions/constants.
    
    Returns
    -------
    str
        The result of the expression as a string, or 'Unsafe Code Detected!'
        if any disallowed content is found or evaluation fails.
    """
    try:
        # Parse the expression into an AST
        expr = ast.parse(math_input, mode='eval')
        
        # Ensure only allowed node types are present
        for node in ast.walk(expr):
            if not isinstance(node, _ALLOWED_NODES):
                return 'Unsafe Code Detected!'
        
        # Evaluate the expression
        result = _eval_node(expr.body)
        return str(result)
    except Exception:
        # Any error in parsing or evaluation is treated as unsafe
        return 'Unsafe Code Detected!'