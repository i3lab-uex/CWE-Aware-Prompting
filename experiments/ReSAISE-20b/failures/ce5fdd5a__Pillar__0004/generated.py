import ast
import operator

# Mapping of allowed AST nodes to Python operators or functions
ALLOWED_OPERATORS = {
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

ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.NameConstant, # True/False/None for older versions
    ast.Tuple,
    ast.List,
    ast.Dict,
)

def _eval(node):
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    elif isinstance(node, (ast.Num, ast.Constant)):
        return node.n if hasattr(node, 'n') else node.value
    elif isinstance(node, ast.Tuple):
        return tuple(_eval(elt) for elt in node.elts)
    elif isinstance(node, ast.List):
        return [_eval(elt) for elt in node.elts]
    elif isinstance(node, ast.Dict):
        return {_eval(k): _eval(v) for k, v in zip(node.keys, node.values)}
    elif isinstance(node, ast.BinOp):
        if type(node.op) not in ALLOWED_OPERATORS:
            raise ValueError("Unsupported operator")
        left = _eval(node.left)
        right = _eval(node.right)
        return ALLOWED_OPERATORS[type(node.op)](left, right)
    elif isinstance(node, ast.UnaryOp):
        if type(node.op) not in ALLOWED_OPERATORS:
            raise ValueError("Unsupported unary operator")
        operand = _eval(node.operand)
        return ALLOWED_OPERATORS[type(node.op)](operand)
    else:
        raise ValueError("Unsupported expression type")

def evaluate_expression(expr: str) -> str:
    """
    Safely evaluates a mathematical expression provided as a string.
    
    Parameters
    ----------
    expr : str
        User supplied expression to evaluate.

    Returns
    -------
    str
        String representation of the result or 'Error!' on failure.
    """
    try:
        # Parse expression; disallow statements
        parsed = ast.parse(expr, mode='eval')
        
        # Ensure only allowed node types appear
        for node in ast.walk(parsed):
            if not isinstance(node, ALLOWED_NODES):
                return 'Error!'
        
        result = _eval(parsed)
        return str(result)
    except Exception:
        # Any error leads to a generic error message
        return 'Error!'