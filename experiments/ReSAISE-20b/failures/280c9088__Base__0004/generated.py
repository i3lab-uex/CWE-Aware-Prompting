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

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,            # Python <3.8
    ast.Constant,       # Python >=3.8
    ast.Name,
    ast.Load,
)

# Allowed variable names (none, but we allow "pi" and "e")
_ALLOWED_NAMES = {
    'pi': 3.141592653589793,
    'e' : 2.718281828459045,
}

def _evaluate(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")
    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Operator {op_type} not allowed")
    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unary operator {op_type} not allowed")
    if isinstance(node, ast.Name):
        if node.id in _ALLOWED_NAMES:
            return _ALLOWED_NAMES[node.id]
        raise ValueError(f"Name {node.id} not allowed")
    raise ValueError("Unsupported expression structure")

def calculate_expression(expr_input: str) -> str:
    """
    Safely evaluate a basic mathematical expression provided as a string.
    
    Parameters
    ----------
    expr_input : str
        The user-provided mathematical expression in Python syntax.
    
    Returns
    -------
    str
        The result of the evaluation as a string, or an error message.
    
    Raises
    ------
    None.  The function returns a string indicating an error if evaluation fails.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr_input, mode='eval')
        
        # Validate that only allowed node types are present
        for node in ast.walk(parsed):
            if not isinstance(node, _ALLOWED_NODES):
                return 'Computation Error!'
        
        # Evaluate the parsed expression
        result = _evaluate(parsed.body)
        
        return str(result)
    except Exception:
        # Any exception (syntax error, disallowed operation, etc.) results in a generic error
        return 'Computation Error!'