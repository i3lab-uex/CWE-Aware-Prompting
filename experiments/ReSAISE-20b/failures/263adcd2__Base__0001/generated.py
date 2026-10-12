import ast
import operator as op

# Mapping of allowed operators to their functions
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

# Allowed names (you can extend this list as needed)
_ALLOWED_NAMES = {
    "abs": abs,
    "round": round,
    "min": min,
    "max": max,
}

def _eval(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    elif isinstance(node, ast.Num):  # Python <3.8
        return node.n
    elif isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
    elif isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
    elif isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
    elif isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id in _ALLOWED_NAMES:
            func = _ALLOWED_NAMES[node.func.id]
            args = [_eval(arg) for arg in node.args]
            return func(*args)
    raise ValueError("Unsupported expression")

def evaluate_student_response(student_query: str) -> str:
    """
    Safely evaluates a simple arithmetic or function expression provided by the student.
    Returns the result as a string, or 'Error!' on any failure.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(student_query, mode="eval")

        # Ensure the AST contains only allowed nodes
        for node in ast.walk(parsed):
            if isinstance(node, (ast.Import, ast.ImportFrom, ast.Exec, ast.Call)):
                # Allow calls only if the function name is in _ALLOWED_NAMES
                if isinstance(node, ast.Call):
                    if not (isinstance(node.func, ast.Name) and node.func.id in _ALLOWED_NAMES):
                        raise ValueError("Disallowed function call")
                else:
                    raise ValueError("Disallowed node type")

            if isinstance(node, ast.Name):
                # Names must be in the allowed names
                if node.id not in _ALLOWED_NAMES:
                    raise ValueError(f"Disallowed name: {node.id}")

        result = _eval(parsed)
        return str(result)
    except Exception:
        return "Error!"