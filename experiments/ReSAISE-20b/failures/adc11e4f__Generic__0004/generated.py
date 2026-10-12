import ast
import operator

# Mapping of allowed AST nodes to their corresponding operations
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

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,  # root
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,
    ast.Constant,  # for Python 3.8+
    ast.Name,      # allow built-in constants like 'pi', 'e' if desired
)

# Optional: allow a few safe names (constants)
_ALLOWED_NAMES = {
    'pi': 3.141592653589793,
    'e': 2.718281828459045,
}

def _evaluate(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        else:
            raise ValueError("Unsupported constant type")
    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError("Unsupported binary operator")
    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError("Unsupported unary operator")
    if isinstance(node, ast.Name):
        name = node.id
        if name in _ALLOWED_NAMES:
            return _ALLOWED_NAMES[name]
        raise ValueError(f"Use of name '{name}' is not allowed")
    raise ValueError("Unsupported expression component")

def process_expression(expression_str: str) -> str:
    """
    Safely evaluate a simple arithmetic expression given as a string.
    
    Parameters
    ----------
    expression_str : str
        The user-submitted arithmetic expression.

    Returns
    -------
    str
        The result of the computation as a string, or 'Computation Error!' if any issue arises.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(expression_str, mode='eval')
        
        # Verify all nodes are allowed
        for node in ast.walk(parsed):
            if not isinstance(node, _ALLOWED_NODES):
                return "Computation Error!"
        
        # Evaluate the parsed expression
        result = _evaluate(parsed.body)
        return str(result)
    except Exception:
        # Catch any parsing or evaluation error
        return "Computation Error!"