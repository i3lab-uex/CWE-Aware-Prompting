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
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed names (math functions/constants) can be added here if needed
_ALLOWED_NAMES = {}

def _eval_node(node):
    """
    Recursively evaluate an AST node, ensuring only allowed nodes are used.
    """
    if isinstance(node, ast.Num):  # < Python 3.8
        return node.n
    elif isinstance(node, ast.Constant):  # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
    elif isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
    elif isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
    elif isinstance(node, ast.Expression):
        return _eval_node(node.body)
    elif isinstance(node, ast.Call):
        # Disallow function calls
        raise ValueError("Function calls are not allowed.")
    elif isinstance(node, ast.Name):
        if node.id in _ALLOWED_NAMES:
            return _ALLOWED_NAMES[node.id]
        raise ValueError(f"Use of unknown identifier: {node.id}")
    else:
        raise ValueError(f"Unsupported expression component: {type(node).__name__}")

def compute_expression(expression_input: str):
    """
    Safely evaluate a simple mathematical expression provided as a string.

    Parameters:
        expression_input (str): The user-provided math expression.

    Returns:
        The numeric result of evaluating the expression.

    Raises:
        ValueError: If the expression contains disallowed syntax or cannot be evaluated.
    """
    if not isinstance(expression_input, str):
        raise ValueError("Input must be a string.")

    # Strip leading/trailing whitespace
    expr = expression_input.strip()
    if not expr:
        raise ValueError("Empty expression.")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in expression: {e}")

    # Walk the AST to ensure no disallowed nodes are present
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.Exec,
                             ast.Global, ast.Nonlocal, ast.Lambda,
                             ast.ClassDef, ast.FunctionDef)):
            raise ValueError("Disallowed statement or construct detected.")

    # Evaluate the parsed AST
    return _eval_node(parsed)

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(compute_expression("2 + 3 * (4 - 1) / 5 ** 2"))