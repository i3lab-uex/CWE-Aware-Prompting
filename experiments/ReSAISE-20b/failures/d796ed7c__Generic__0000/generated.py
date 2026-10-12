import ast
import operator

# Mapping of allowed AST operators to their corresponding functions
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

# Allowed AST node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Name,
    ast.Load,
    ast.Call,         # disallowed but we allow only built-in safe functions
)

# Allowed names (functions) that can be used in expressions
_ALLOWED_NAMES = {
    "abs": abs,
    "round": round,
    "pow": pow,
}

def _eval_node(node):
    """
    Recursively evaluate an AST node. Only allowed nodes are processed.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Numbers
    if isinstance(node, (ast.Num, ast.Constant)):
        return node.n

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported operator: {op_type.__name__}")
        return _ALLOWED_OPERATORS[op_type](left, right)

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return _ALLOWED_OPERATORS[op_type](operand)

    # Names (allowed functions)
    if isinstance(node, ast.Name):
        if node.id not in _ALLOWED_NAMES:
            raise ValueError(f"Use of name '{node.id}' is not allowed")
        return _ALLOWED_NAMES[node.id]

    # Function calls (only allowed names)
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name) or node.func.id not in _ALLOWED_NAMES:
            raise ValueError("Only safe built-in functions are allowed")
        args = [_eval_node(arg) for arg in node.args]
        return _ALLOWED_NAMES[node.func.id](*args)

    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def secure_math_eval(exp_str: str):
    """
    Evaluate a mathematical expression safely.

    Parameters
    ----------
    exp_str : str
        The user-provided expression string.

    Returns
    -------
    result
        The evaluated numerical result.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters, operators,
        or functions.
    """
    if not isinstance(exp_str, str):
        raise ValueError("Input must be a string")

    # Strip whitespace
    exp_str = exp_str.strip()
    if not exp_str:
        raise ValueError("Empty expression")

    try:
        parsed = ast.parse(exp_str, mode="eval")
    except SyntaxError as e:
        raise ValueError(f"Syntax error in expression: {e}") from None

    # Ensure all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed syntax element: {type(node).__name__}")

    return _eval_node(parsed)

# Example usage
if __name__ == "__main__":
    tests = [
        "2 + 3 * 4",
        "(5 - 2) ** 3",
        "abs(-10)",
        "round(3.14159, 2)",
        "__import__('os').system('echo unsafe')",   # should raise
    ]
    for expr in tests:
        try:
            print(f"{expr} => {secure_math_eval(expr)}")
        except Exception as e:
            print(f"{expr} => Error: {e}")