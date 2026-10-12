import ast
import operator as op

# Supported binary operators mapping to their actual functions
_ALLOWED_BINOPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}

# Supported unary operators mapping to their actual functions
_ALLOWED_UNOPS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.Module,
    ast.Expr,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Str,
    ast.NameConstant,
    ast.Call,         # allow only specific builtins like str, int, float
)

# Allowed function names and their corresponding callables
_ALLOWED_FUNCS = {
    'str': str,
    'int': int,
    'float': float,
}

def _eval(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    if isinstance(node, ast.Module):
        # Only one expression in the module
        if len(node.body) != 1:
            raise ValueError("Only a single expression is allowed.")
        return _eval(node.body[0])

    if isinstance(node, ast.Expr):
        return _eval(node.value)

    if isinstance(node, ast.Num):  # Python <3.8
        return node.n

    if isinstance(node, ast.Constant):  # Python >=3.8
        return node.value

    if isinstance(node, ast.Str):
        return node.s

    if isinstance(node, ast.NameConstant):
        return node.value

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_BINOPS:
            return _ALLOWED_BINOPS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_UNOPS:
            return _ALLOWED_UNOPS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type}")

    if isinstance(node, ast.Call):
        # Only allow calls to whitelisted functions with no arguments
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function calls are allowed.")
        func_name = node.func.id
        if func_name not in _ALLOWED_FUNCS:
            raise ValueError(f"Function '{func_name}' is not allowed.")
        if node.args or node.keywords:
            raise ValueError("Function calls must have no arguments.")
        return _ALLOWED_FUNCS[func_name]()

    raise ValueError(f"Unsupported AST node: {type(node)}")

def execute_user_input(user_code: str) -> str:
    """
    Safely evaluate simple arithmetic or string expressions provided by a user.

    Parameters
    ----------
    user_code : str
        The script content to evaluate. Must be a single expression.

    Returns
    -------
    str
        The string representation of the evaluation result, or 'Execution Blocked!'
        if the input is unsafe.
    """
    try:
        # Parse the code into an AST
        parsed = ast.parse(user_code, mode='eval')

        # Ensure only allowed nodes are present
        for node in ast.walk(parsed):
            if not isinstance(node, _ALLOWED_NODES):
                return 'Execution Blocked!'

        result = _eval(parsed)
        return str(result)

    except Exception:
        # Any exception (syntax error, unsupported node, etc.) leads to blocking
        return 'Execution Blocked!'