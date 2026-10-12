import ast
import operator

# Supported operators mapping to their functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
}

# Supported unary operators
_ALLOWED_UNARY = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed constants (e.g., math.pi, math.e) if desired
_ALLOWED_CONSTANTS = {
    'pi': 3.141592653589793,
    'e' : 2.718281828459045,
}

def _eval(node):
    """
    Recursively evaluate an AST node, only allowing safe operations.
    Raises ValueError on any disallowed construct.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    # Numbers
    if isinstance(node, (ast.Num, ast.Constant)):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")

    # Binary operations
    if isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError("Disallowed binary operator")
        left = _eval(node.left)
        right = _eval(node.right)
        return _ALLOWED_OPERATORS[type(node.op)](left, right)

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_UNARY:
            raise ValueError("Disallowed unary operator")
        operand = _eval(node.operand)
        return _ALLOWED_UNARY[type(node.op)](operand)

    # Parentheses are handled by grouping; no explicit node needed

    # Names (constants)
    if isinstance(node, ast.Name):
        if node.id in _ALLOWED_CONSTANTS:
            return _ALLOWED_CONSTANTS[node.id]
        raise ValueError(f"Unknown identifier: {node.id}")

    # Disallow any other node types
    raise ValueError(f"Disallowed expression: {ast.dump(node)}")

def process_expression(expression_str: str) -> str:
    """
    Safely evaluate a mathematical expression provided as a string.
    Returns the result as a string or 'Computation Error!' on failure.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(expression_str, mode='eval')

        # Evaluate the expression recursively
        result = _eval(parsed)

        # Convert the numeric result to string (handle floats with precision)
        if isinstance(result, float):
            # Remove trailing .0 for integers
            return str(int(result)) if result.is_integer() else f"{result:.10g}"
        return str(result)
    except Exception:
        # Any error (syntax, disallowed op, division by zero, etc.)
        return "Computation Error!"