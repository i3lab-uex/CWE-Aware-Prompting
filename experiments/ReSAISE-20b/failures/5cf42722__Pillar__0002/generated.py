import ast
import operator

# Allowed binary operators and their corresponding functions
_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Allowed unary operators
_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _eval(node, var_substitute):
    """
    Recursively evaluate an AST node using only the allowed operations.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body, var_substitute)

    if isinstance(node, ast.BinOp):
        left = _eval(node.left, var_substitute)
        right = _eval(node.right, var_substitute)
        op_type = type(node.op)
        if op_type not in _BIN_OPS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        try:
            return _BIN_OPS[op_type](left, right)
        except ZeroDivisionError as e:
            raise ValueError("Division by zero") from e

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand, var_substitute)
        op_type = type(node.op)
        if op_type not in _UNARY_OPS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return _UNARY_OPS[op_type](operand)

    if isinstance(node, ast.Num):  # For Python <3.8
        return node.n

    if isinstance(node, ast.Constant):  # For Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        else:
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.Name):
        if node.id in var_substitute:
            val = var_substitute[node.id]
            if isinstance(val, (int, float)):
                return val
            else:
                raise ValueError(f"Variable '{node.id}' has non-numeric value")
        else:
            raise ValueError(f"Unknown variable: {node.id}")

    # Any other node type is disallowed
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def calculate_expression_securely(expr: str, var_substitute: dict) -> str:
    """
    Safely parse and evaluate a mathematical expression containing
    numbers, basic arithmetic operators, parentheses, and variables.

    Parameters:
        expr (str): The expression to evaluate.
        var_substitute (dict): Mapping from variable names to numeric values.

    Returns:
        str: The evaluated result as a string.

    Raises:
        ValueError: If the expression is invalid or evaluation fails.
    """
    if not isinstance(expr, str):
        raise ValueError("Expression must be a string")

    # Strip leading/trailing whitespace
    expr = expr.strip()
    if not expr:
        raise ValueError("Expression is empty")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError("Invalid syntax in expression") from e

    # Ensure the parsed AST contains only allowed nodes
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Module,)):
            continue
        if not isinstance(
                node,
                (
                    ast.Expression,
                    ast.BinOp,
                    ast.UnaryOp,
                    ast.Num,
                    ast.Constant,
                    ast.Name,
                    ast.Add,
                    ast.Sub,
                    ast.Mult,
                    ast.Div,
                    ast.FloorDiv,
                    ast.Mod,
                    ast.Pow,
                    ast.UAdd,
                    ast.USub,
                ),
        ):
            raise ValueError(f"Disallowed expression element: {type(node).__name__}")

    # Evaluate the AST
    result = _eval(parsed, var_substitute)

    return str(result)