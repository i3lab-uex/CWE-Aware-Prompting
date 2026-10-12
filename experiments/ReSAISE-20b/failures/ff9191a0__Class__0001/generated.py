import ast
import operator as op

# Supported operators mapping
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

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Name,
)

def _eval(node: ast.AST, variables: dict) -> float:
    """Recursively evaluate an AST node safely."""
    if isinstance(node, ast.Expression):
        return _eval(node.body, variables)

    if isinstance(node, (ast.Num, ast.Constant)):
        # ast.Constant covers numbers and literals in newer Python
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value)}")

    if isinstance(node, ast.Name):
        try:
            return float(variables[node.id])
        except KeyError:
            raise ValueError(f"Unknown variable: {node.id}")

    if isinstance(node, ast.BinOp):
        left = _eval(node.left, variables)
        right = _eval(node.right, variables)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand, variables)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type}")

    raise ValueError(f"Disallowed expression: {ast.dump(node)}")

def evaluate_expression_safely(math_expression: str, variable_mapping: dict) -> str:
    """
    Safely evaluate a mathematical expression with optional variables.

    Parameters
    ----------
    math_expression : str
        The arithmetic expression to evaluate.
    variable_mapping : dict
        Mapping from variable names to numeric values.

    Returns
    -------
    str
        The simplified result of the expression as a string.

    Raises
    ------
    ValueError
        If the expression contains disallowed syntax or evaluation fails.
    """
    if not isinstance(math_expression, str):
        raise ValueError("Expression must be a string.")
    if not isinstance(variable_mapping, dict):
        raise ValueError("Variable mapping must be a dictionary.")

    try:
        parsed = ast.parse(math_expression, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from exc

    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    result = _eval(parsed, variable_mapping)

    # Return the result as a string, preserving integer formatting when possible
    if isinstance(result, float) and result.is_integer():
        return str(int(result))
    return str(result)