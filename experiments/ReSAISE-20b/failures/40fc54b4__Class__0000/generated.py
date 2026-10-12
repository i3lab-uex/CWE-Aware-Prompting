import ast
import operator as op

# Mapping of allowed AST operator nodes to actual Python operators
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed AST node types
_ALLOWED_NODES = (
    ast.Expression,  # top-level expression
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,         # Python <3.8
    ast.Constant,    # Python >=3.8
    ast.Expr,
)

def _eval(node):
    """
    Recursively evaluate an AST node that represents a mathematical expression.
    Only nodes and operators listed in _ALLOWED_NODES/_ALLOWED_OPERATORS are permitted.
    """
    if isinstance(node, ast.Num):          # <3.8
        return node.n
    if isinstance(node, ast.Constant):     # >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError("Unsupported binary operator")

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError("Unsupported unary operator")

    # If node is Expression or Expr, evaluate its body
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    if isinstance(node, ast.Expr):
        return _eval(node.value)

    raise ValueError("Unsupported AST node")

def evaluate_arith_expression(input_expr: str) -> str:
    """
    Safely evaluate a basic arithmetic expression.
    
    Parameters
    ----------
    input_expr : str
        The mathematical expression to evaluate.

    Returns
    -------
    str
        The string representation of the result, or 'Computation Error!' if evaluation fails.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(input_expr, mode='eval')

        # Ensure that only allowed node types are present
        for node in ast.walk(parsed):
            if not isinstance(node, _ALLOWED_NODES):
                raise ValueError("Disallowed AST node detected")

        # Evaluate the parsed expression
        result = _eval(parsed)

        # Return as string
        return str(result)
    except Exception:
        # Any error (syntax, type, security) results in the generic error message
        return 'Computation Error!'