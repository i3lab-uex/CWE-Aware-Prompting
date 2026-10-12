import ast
import operator

# Mapping of AST operators to actual functions
_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Name,
    ast.Load,
)

def _evaluate(node, variables):
    """
    Recursively evaluate an AST node using the supplied variable mapping.
    Raises ValueError if unsupported nodes or operations are encountered.
    """
    if isinstance(node, ast.Expression):
        return _evaluate(node.body, variables)

    if isinstance(node, (ast.Num, ast.Constant)):
        # Num is used in older Python; Constant covers newer versions
        return node.n

    if isinstance(node, ast.Name):
        if node.id in variables:
            return variables[node.id]
        raise ValueError(f"Unknown variable: {node.id}")

    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left, variables)
        right = _evaluate(node.right, variables)

        op_type = type(node.op)
        if op_type in _BIN_OPS:
            try:
                return _BIN_OPS[op_type](left, right)
            except ZeroDivisionError as exc:
                raise ValueError("Division by zero") from exc
        else:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand, variables)
        op_type = type(node.op)
        if op_type in _UNARY_OPS:
            return _UNARY_OPS[op_type](operand)
        else:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    # Any other node type is disallowed
    raise ValueError(f"Disallowed expression: {ast.dump(node)}")

def calculate_expression_securely(expr: str, var_substitute: dict) -> str:
    """
    Evaluate a mathematical expression securely.

    Parameters
    ----------
    expr : str
        The arithmetic expression to evaluate.
    var_substitute : dict
        Mapping of variable names to numeric values.

    Returns
    -------
    str
        The string representation of the computed result.

    Raises
    ------
    ValueError
        If the expression is syntactically invalid, contains disallowed nodes,
        or if evaluation fails (e.g., division by zero).
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax in expression: {expr}") from exc

    # Ensure all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Evaluate the expression
    result = _evaluate(parsed, var_substitute)

    return str(result)