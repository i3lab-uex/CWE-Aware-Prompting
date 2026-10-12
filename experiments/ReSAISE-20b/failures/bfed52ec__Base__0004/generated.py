import ast
import operator

# Mapping of allowed AST node types to their corresponding functions or values
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

_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Expr,
    ast.Load,
)

def _eval_node(node):
    """
    Recursively evaluate an AST node while ensuring only safe operations are performed.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    if isinstance(node, (ast.Num, ast.Constant)):
        # Accept only numeric constants
        value = node.n if isinstance(node, ast.Num) else node.value
        if not isinstance(value, (int, float)):
            raise ValueError("Non-numeric constant")
        return value

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {op_type}")
        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_UNARY_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type}")
        return _ALLOWED_UNARY_OPERATORS[op_type](operand)

    raise ValueError(f"Unsupported AST node: {type(node)}")

def securely_compute_expression(formula: str) -> str:
    """
    Safely evaluate a simple arithmetic expression provided as a string.

    Parameters
    ----------
    formula : str
        The user-supplied expression to evaluate.

    Returns
    -------
    str
        String representation of the computed result, or 'Processing Failed!' if
        the expression is unsafe or evaluation fails.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(formula, mode='eval')

        # Verify that only allowed nodes are present
        for node in ast.walk(parsed):
            if not isinstance(node, _ALLOWED_NODES):
                raise ValueError(f"Disallowed node type: {type(node)}")

        # Evaluate the parsed AST
        result = _eval_node(parsed)
        return str(result)

    except Exception:
        # Any exception (syntax error, unsafe node, runtime error) results in failure
        return "Processing Failed!"