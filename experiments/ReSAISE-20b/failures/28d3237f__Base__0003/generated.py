import ast
import operator as op

# Allowed operators mapping
_allowed_ops = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}

# Allowed unary operators
_allowed_unary_ops = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed node types
_allowed_nodes = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.UnaryOp,
    ast.BinOp,
    ast.Call,         # to reject function calls
)

def _eval(node):
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    elif isinstance(node, ast.Constant):  # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")
    elif isinstance(node, ast.Num):  # Python <3.8
        return node.n
    elif isinstance(node, ast.BinOp):
        if type(node.op) not in _allowed_ops:
            raise ValueError("Unsupported binary operator")
        left = _eval(node.left)
        right = _eval(node.right)
        return _allowed_ops[type(node.op)](left, right)
    elif isinstance(node, ast.UnaryOp):
        if type(node.op) not in _allowed_unary_ops:
            raise ValueError("Unsupported unary operator")
        operand = _eval(node.operand)
        return _allowed_unary_ops[type(node.op)](operand)
    else:
        raise ValueError("Unsupported expression")

def compute_expression(expression: str) -> str:
    """
    Safely evaluate a simple arithmetic expression containing numbers
    and the operators +, -, *, /, //, %, **.
    
    Parameters:
        expression (str): The arithmetic expression to evaluate.
    
    Returns:
        str: Result of evaluation or 'Computation Error!' on failure.
    """
    try:
        # Parse expression into AST
        node = ast.parse(expression, mode='eval')
        
        # Ensure no disallowed nodes (e.g., function calls)
        for sub in ast.walk(node):
            if isinstance(sub, ast.Call):
                raise ValueError("Function calls not allowed")
            if not isinstance(sub, _allowed_nodes):
                raise ValueError(f"Disallowed node type: {type(sub).__name__}")
        
        result = _eval(node)
        return str(result)
    except Exception:
        # Any error (parsing, disallowed syntax, division by zero, etc.)
        return "Computation Error!"