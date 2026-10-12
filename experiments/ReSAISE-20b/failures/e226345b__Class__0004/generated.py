import ast
import operator as op

# Allowed operators mapping
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed nodes
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Name,
)

def _eval_node(node, variables):
    if isinstance(node, (ast.Num, ast.Constant)):
        return node.n
    if isinstance(node, ast.Name):
        if node.id in variables:
            return variables[node.id]
        raise ValueError(f"Undefined variable: {node.id}")
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left, variables)
        right = _eval_node(node.right, variables)
        operator_func = _ALLOWED_OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError(f"Unsupported binary operator: {ast.dump(node.op)}")
        return operator_func(left, right)
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand, variables)
        operator_func = _ALLOWED_OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError(f"Unsupported unary operator: {ast.dump(node.op)}")
        return operator_func(operand)
    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def evaluate_math_expr(math_expression: str, variable_mapping: dict) -> str:
    """
    Safely evaluate a mathematical expression containing variables.

    Parameters
    ----------
    math_expression : str
        The expression to evaluate.
    variable_mapping : dict
        Mapping from variable names to numeric values.

    Returns
    -------
    str
        The evaluated result converted to a string.

    Raises
    ------
    ValueError
        If the expression contains unsupported syntax or evaluation fails.
    """
    try:
        # Parse expression into an AST
        parsed = ast.parse(math_expression, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from exc

    # Verify that all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed expression element: {ast.dump(node)}")

    # Evaluate the parsed AST
    result = _eval_node(parsed.body, variable_mapping)

    return str(result)