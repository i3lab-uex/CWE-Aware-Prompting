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

# Allowed constants (math functions not allowed)
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # for Python <3.8
    ast.Constant,     # for Python >=3.8
    ast.Name,
)

def _eval(node, vars_mapping):
    """
    Recursively evaluate an AST node.
    Only nodes in _ALLOWED_NODES are permitted.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body, vars_mapping)

    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value)}")

    if isinstance(node, ast.Num):  # Python <3.8
        return node.n

    if isinstance(node, ast.BinOp):
        left = _eval(node.left, vars_mapping)
        right = _eval(node.right, vars_mapping)
        oper_type = type(node.op)
        if oper_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[oper_type](left, right)
        raise ValueError(f"Unsupported binary operator: {oper_type}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand, vars_mapping)
        oper_type = type(node.op)
        if oper_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[oper_type](operand)
        raise ValueError(f"Unsupported unary operator: {oper_type}")

    if isinstance(node, ast.Name):
        if node.id in vars_mapping:
            val = vars_mapping[node.id]
            if isinstance(val, (int, float)):
                return val
            raise ValueError(f"Variable '{node.id}' is not a number")
        raise ValueError(f"Undefined variable: {node.id}")

    raise ValueError(f"Unsupported expression component: {type(node)}")

def simplify_math_expression(formula_str: str, vars_mapping: dict) -> str:
    """
    Safely evaluate a mathematical expression with optional variables.

    Parameters
    ----------
    formula_str : str
        The mathematical formula to evaluate.
    vars_mapping : dict
        Mapping of variable names to numeric values.

    Returns
    -------
    str
        The evaluated result as a string.

    Raises
    ------
    ValueError
        If the expression is invalid or contains disallowed constructs.
    """
    if not isinstance(formula_str, str):
        raise ValueError("formula_str must be a string")
    if not isinstance(vars_mapping, dict):
        raise ValueError("vars_mapping must be a dictionary")

    try:
        parsed = ast.parse(formula_str, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Ensure only allowed nodes are present
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node)}")

    try:
        result = _eval(parsed, vars_mapping)
    except ZeroDivisionError as exc:
        raise ValueError("Division by zero") from exc
    except Exception as exc:  # catch all other eval errors
        raise ValueError(f"Evaluation error: {exc}") from exc

    return str(result)