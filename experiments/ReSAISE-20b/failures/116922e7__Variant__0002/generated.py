import ast
import operator

# Mapping of allowed AST operators to actual functions
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
    ast.Expression,   # root node
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Expr,
)

def _evaluate(node):
    """
    Recursively evaluate an AST node that represents a simple arithmetic expression.
    Raises ValueError for any disallowed construct.
    """
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)

    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {op_type}")
        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type}")
        return _ALLOWED_OPERATORS[op_type](operand)

    if isinstance(node, ast.Num):          # Python <3.8
        return node.n

    if isinstance(node, ast.Constant):     # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        else:
            raise ValueError(f"Unsupported constant type: {type(node.value)}")

    if isinstance(node, ast.Expr):
        return _evaluate(node.value)

    raise ValueError(f"Unsupported node type: {type(node)}")

def calculate_expression(ex_string: str) -> str:
    """
    Safely evaluate a basic arithmetic expression supplied as a string.
    Only integer and floating point operations (+, -, *, /, //, %, **)
    are allowed. Any other syntax or malicious code results in
    'Computation Error!'.

    Parameters:
        ex_string (str): The expression string to evaluate.

    Returns:
        str: Result of evaluation as a string, or 'Computation Error!'.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(ex_string, mode='eval')

        # Verify that all nodes in the tree are allowed
        for node in ast.walk(parsed):
            if not isinstance(node, _ALLOWED_NODES):
                raise ValueError(f"Disallowed node type: {type(node)}")

        # Evaluate the parsed AST
        result = _evaluate(parsed)

        return str(result)
    except Exception:
        # Any error (syntax, disallowed node, evaluation) results in a generic message
        return "Computation Error!"