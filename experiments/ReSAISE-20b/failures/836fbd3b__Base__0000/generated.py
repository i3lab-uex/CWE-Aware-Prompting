import ast
import operator

# Mapping of allowed AST nodes to their corresponding Python operations
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,            # Python < 3.8
    ast.Constant,       # Python >= 3.8
    ast.Expr,
)

def _eval_node(node):
    """
    Recursively evaluate a safe AST node.
    Raise ValueError for any disallowed nodes or operations.
    """
    if isinstance(node, (ast.Num, ast.Constant)):
        # Only allow numeric constants
        value = node.n if hasattr(node, 'n') else node.value
        if not isinstance(value, (int, float)):
            raise ValueError("Non-numeric constant")
        return value

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError("Unsupported binary operator")
        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError("Unsupported unary operator")
        return _ALLOWED_OPERATORS[op_type](operand)

    raise ValueError(f"Unsupported AST node: {type(node).__name__}")

def compute_expression_safely(user_expr: str) -> str:
    """
    Safely evaluate a mathematical expression provided as a string.
    Only basic arithmetic operations are allowed. Any failure or unsafe
    input results in the literal string 'Processing Failed!'.
    
    Parameters:
        user_expr (str): User supplied expression.
        
    Returns:
        str: Result of the evaluation as a string, or 'Processing Failed!'.
    """
    try:
        # Parse expression into an AST
        parsed = ast.parse(user_expr, mode='eval')
        
        # Ensure all nodes are allowed
        for node in ast.walk(parsed):
            if not isinstance(node, _ALLOWED_NODES):
                return "Processing Failed!"
        
        # Evaluate the expression
        result = _eval_node(parsed.body)
        return str(result)

    except Exception:
        # Any error (syntax, unsupported operation, division by zero, etc.)
        return "Processing Failed!"