import ast
import operator as op
import math

# Mapping of allowed operators to their corresponding functions
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

# Allowed names from the math module
_ALLOWED_NAMES = {name: getattr(math, name) for name in dir(math) if not name.startswith("_")}

# Additionally allow built-in constants
_ALLOWED_NAMES.update({
    "pi": math.pi,
    "e": math.e,
})

def _eval(node: ast.AST) -> float:
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    # Numbers
    if isinstance(node, (ast.Constant, ast.Num)):
        value = node.n if hasattr(node, "n") else node.value
        if isinstance(value, (int, float)):
            return value
        raise ValueError(f"Unsupported constant type: {type(value).__name__}")

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Operator {op_type.__name__} is not allowed")

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unary operator {op_type.__name__} is not allowed")

    # Function calls
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function names are allowed")
        func_name = node.func.id
        if func_name not in _ALLOWED_NAMES:
            raise ValueError(f"Function '{func_name}' is not allowed")
        func = _ALLOWED_NAMES[func_name]
        args = [_eval(arg) for arg in node.args]
        return func(*args)

    # Variable names (constants)
    if isinstance(node, ast.Name):
        if node.id in _ALLOWED_NAMES:
            return _ALLOWED_NAMES[node.id]
        raise ValueError(f"Name '{node.id}' is not allowed")

    # Disallow any other node types
    raise ValueError(f"Unsupported expression component: {type(node).__name__}")

def compute_math_expression(expression_input: str) -> float:
    """
    Safely evaluate a mathematical expression provided by the user.

    Parameters
    ----------
    expression_input : str
        The mathematical expression to evaluate.

    Returns
    -------
    float
        The result of the evaluated expression.

    Raises
    ------
    ValueError
        If the input contains unsafe components or is structurally incorrect.
    """
    if not isinstance(expression_input, str):
        raise ValueError("Input must be a string")

    # Strip leading/trailing whitespace
    expr = expression_input.strip()
    if not expr:
        raise ValueError("Empty expression")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Walk the AST to ensure no disallowed nodes are present
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.Exec, ast.Call)):
            # Calls are allowed but only for safe names; other imports are disallowed
            if isinstance(node, ast.Call):
                # Allow calls only to safe functions; handled later
                continue
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Evaluate the parsed AST
    return _eval(parsed)

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     expr = "2 * (3 + math.sin(pi / 4))"
#     print(compute_math_expression(expr))