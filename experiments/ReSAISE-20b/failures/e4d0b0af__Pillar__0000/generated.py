import ast
import operator

# Mapping of allowed operators to their corresponding functions
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

# Mapping of allowed unary operators
_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed constants (e.g., math constants)
_ALLOWED_CONSTANTS = {
    'pi': 3.141592653589793,
    'e': 2.718281828459045,
}

def _evaluate(node):
    """
    Recursively evaluate an AST node that has been validated.
    """
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)

    if isinstance(node, ast.Num):          # Python <3.8
        return node.n

    if isinstance(node, ast.Constant):     # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
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
        if op_type in _ALLOWED_UNARY_OPERATORS:
            return _ALLOWED_UNARY_OPERATORS[op_type](operand)
        raise ValueError("Unsupported unary operator")

    if isinstance(node, ast.Name):
        id_ = node.id
        if id_ in _ALLOWED_CONSTANTS:
            return _ALLOWED_CONSTANTS[id_]
        raise ValueError("Undefined identifier")

    if isinstance(node, ast.Call):
        # Prevent any function calls
        raise ValueError("Function calls are not allowed")

    if isinstance(node, ast.Compare):
        # Disallow comparisons
        raise ValueError("Comparison operators are not allowed")

    if isinstance(node, ast.BoolOp):
        # Disallow boolean operations
        raise ValueError("Boolean operators are not allowed")

    if isinstance(node, ast.IfExp):
        # Disallow conditional expressions
        raise ValueError("Conditional expressions are not allowed")

    if isinstance(node, ast.Subscript):
        # Disallow subscripting
        raise ValueError("Subscripts are not allowed")

    if isinstance(node, ast.Attribute):
        # Disallow attribute access
        raise ValueError("Attribute access is not allowed")

    if isinstance(node, ast.Lambda):
        # Disallow lambda expressions
        raise ValueError("Lambda expressions are not allowed")

    if isinstance(node, ast.List):
        # Disallow lists
        raise ValueError("List literals are not allowed")

    if isinstance(node, ast.Tuple):
        # Disallow tuples
        raise ValueValueError("Tuple literals are not allowed")

    if isinstance(node, ast.Dict):
        # Disallow dictionaries
        raise ValueError("Dictionary literals are not allowed")

    if isinstance(node, ast.Set):
        # Disallow sets
        raise ValueError("Set literals are not allowed")

    if isinstance(node, ast.Slice):
        # Disallow slicing
        raise ValueError("Slicing is not allowed")

    if isinstance(node, ast.JoinedStr):
        # Disallow f-strings
        raise ValueError("f-strings are not allowed")

    # If we reach here, the node type is unsupported
    raise ValueError(f"Unsupported expression component: {type(node).__name__}")

def evaluate_expression_safely(input_expr: str) -> str:
    """
    Safely evaluates a simple arithmetic expression provided as a string.
    
    Parameters
    ----------
    input_expr : str
        The user-provided expression to evaluate.
    
    Returns
    -------
    str
        The string representation of the evaluated result if successful,
        otherwise 'Processing Failed!' in case of errors or unsafe input.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(input_expr, mode='eval')

        # Walk the tree to ensure only allowed nodes are present
        for node in ast.walk(parsed):
            if not isinstance(node, (
                ast.Expression,
                ast.BinOp,
                ast.UnaryOp,
                ast.Num,          # for Python <3.8
                ast.Constant,     # for Python >=3.8
                ast.Name,
                ast.Load,
            )):
                return 'Processing Failed!'

        # Evaluate the parsed expression
        result = _evaluate(parsed)
        return str(result)

    except Exception:
        # Any parsing or evaluation error leads to a generic failure message
        return 'Processing Failed!'