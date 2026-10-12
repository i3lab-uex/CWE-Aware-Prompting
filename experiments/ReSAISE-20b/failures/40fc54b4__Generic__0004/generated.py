import ast
import operator

def evaluate_arith_expression(input_expr: str) -> str:
    """
    Safely evaluates a basic arithmetic expression given as a string.
    
    Parameters
    ----------
    input_expr : str
        The arithmetic expression to evaluate. Only supports +, -, *, /, **,
        parentheses, and numeric literals (int/float).
    
    Returns
    -------
    str
        The string representation of the computed result or 'Computation Error!'
        if evaluation fails or malicious code is detected.
    """
    
    # Mapping of AST operator nodes to actual Python functions
    _OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
    }
    
    _UNARY_OPERATORS = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }
    
    # Allowed node types
    _ALLOWED_NODES = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Constant,   # Python 3.8+
        ast.Num,        # For compatibility with older Python versions
    )
    
    def _eval(node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        
        elif isinstance(node, (ast.Constant, ast.Num)):
            if isinstance(node.value, (int, float)):
                return node.value
            else:
                raise ValueError("Non-numeric constant")
        
        elif isinstance(node, ast.BinOp):
            if type(node.op) not in _OPERATORS:
                raise ValueError("Unsupported binary operator")
            left = _eval(node.left)
            right = _eval(node.right)
            return _OPERATORS[type(node.op)](left, right)
        
        elif isinstance(node, ast.UnaryOp):
            if type(node.op) not in _UNARY_OPERATORS:
                raise ValueError("Unsupported unary operator")
            operand = _eval(node.operand)
            return _UNARY_OPERATORS[type(node.op)](operand)
        
        else:
            raise ValueError("Unsupported syntax")
    
    try:
        # Parse expression into an AST
        parsed = ast.parse(input_expr, mode='eval')
        
        # Ensure all nodes are allowed
        for node in ast.walk(parsed):
            if not isinstance(node, _ALLOWED_NODES):
                raise ValueError("Disallowed node in expression")
        
        result = _eval(parsed)
        return str(result)
    
    except Exception:
        # Any parsing or evaluation error results in a generic error message
        return "Computation Error!"