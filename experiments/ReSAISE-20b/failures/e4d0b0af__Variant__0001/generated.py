import ast
import operator as op

# Supported operators mapping from AST node to actual Python function
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}

# Allowed node types for the AST
_ALLOWED_NODES = (
    ast.Expression,   # top level expression
    ast.BinOp,        # binary operations
    ast.UnaryOp,      # unary operations (+/-)
    ast.Num,          # numeric literals (Python <3.8)
    ast.Constant,     # numeric literals (Python 3.8+)
    ast.NameConstant, # True/False/None
)

def _evaluate(node):
    """
    Recursively evaluate an AST node safely.
    Raises ValueError if the node type or operator is not allowed.
    """
    if isinstance(node, (ast.Num, ast.Constant)):
        return node.n if hasattr(node, 'n') else node.value

    if isinstance(node, ast.NameConstant):
        return node.value

    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Operator {op_type} not allowed")
        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Operator {op_type} not allowed")
        return _ALLOWED_OPERATORS[op_type](operand)

    raise ValueError(f"Unsupported node type: {type(node)}")

def evaluate_expression_safely(input_expr: str) -> str:
    """
    Safely evaluates a simple arithmetic or logical expression provided as a string.
    Returns the result converted to string, or 'Processing Failed!' on any error
    or if the expression contains disallowed constructs.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(input_expr, mode='eval')

        # Ensure only allowed node types are present
        for node in ast.walk(parsed):
            if not isinstance(node, _ALLOWED_NODES):
                return 'Processing Failed!'

        # Evaluate the expression
        result = _evaluate(parsed.body)

        return str(result)
    except Exception:
        # Catch any exception (syntax errors, division by zero, etc.)
        return 'Processing Failed!'