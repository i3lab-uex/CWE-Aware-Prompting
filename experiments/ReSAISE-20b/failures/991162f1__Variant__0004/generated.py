import ast
import operator as op
import math

# Mapping of allowed operators to their implementations
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

# Allowed names from the math module and a few built‑ins
_ALLOWED_NAMES = {
    name: getattr(math, name) for name in dir(math)
    if not name.startswith("_")
}
_ALLOWED_NAMES.update({
    "abs": abs,
    "round": round,
    "min": min,
    "max": max,
})

def _eval_node(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Numbers (int/float)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_func = _ALLOWED_OPERATORS.get(type(node.op))
        if op_func is None:
            raise ValueError(f"Operator {node.op} not allowed")
        return op_func(left, right)

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_func = _ALLOWED_OPERATORS.get(type(node.op))
        if op_func is None:
            raise ValueError(f"Unary operator {node.op} not allowed")
        return op_func(operand)

    # Function calls (only whitelisted)
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only direct function names allowed")
        func_name = node.func.id
        if func_name not in _ALLOWED_NAMES:
            raise ValueError(f"Function {func_name} is not allowed")
        args = [_eval_node(arg) for arg in node.args]
        kwargs = {kw.arg: _eval_node(kw.value) for kw in node.keywords}
        return _ALLOWED_NAMES[func_name](*args, **kwargs)

    # Variable names (only whitelisted)
    if isinstance(node, ast.Name):
        if node.id in _ALLOWED_NAMES:
            return _ALLOWED_NAMES[node.id]
        raise ValueError(f"Name {node.id} is not allowed")

    # Unsupported node types
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def evaluate_math_expression(math_expression: str) -> str:
    """
    Safely evaluates a mathematical expression string.

    Parameters
    ----------
    math_expression : str
        A Python‑style mathematical expression.

    Returns
    -------
    str
        The string representation of the evaluated result or an error message.

    Raises
    ------
    str
        Returns 'Unsafe Code Detected!' if the expression contains disallowed
        constructs or if an error occurs during evaluation.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(math_expression, mode="eval")

        # Ensure no forbidden nodes exist in the tree
        for node in ast.walk(parsed):
            if isinstance(node, (ast.Import, ast.ImportFrom, ast.Exec, ast.Call)):
                # Calls are allowed only if they are whitelisted; others will be caught later
                pass
            elif isinstance(node, (ast.Attribute, ast.Lambda)):
                raise ValueError("Attribute access or lambda expressions are not allowed")

        result = _eval_node(parsed)
        return str(result)

    except Exception:
        # Any exception is treated as unsafe or erroneous input
        return "Unsafe Code Detected!"