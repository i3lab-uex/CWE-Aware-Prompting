import ast
import operator as op

# Mapping of allowed operators to their corresponding functions
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}

# Allowed unary operators
_ALLOWED_UNARY = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Call,         # Disallow function calls
    ast.Name,         # Disallow names
    ast.Attribute,    # Disallow attributes
)

def _eval_node(node):
    """
    Recursively evaluate an AST node after validating its type and contents.
    Raises ValueError if the expression contains any disallowed elements.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Numeric literals
    if isinstance(node, (ast.Num, ast.Constant)):
        value = node.n if hasattr(node, 'n') else node.value
        if not isinstance(value, (int, float)):
            raise ValueError(f"Unsupported numeric type: {type(value).__name__}")
        return value

    # Binary operations
    if isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError(f"Operator {type(node.op).__name__} is not allowed")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return _ALLOWED_OPERATORS[type(node.op)](left, right)

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_UNARY:
            raise ValueError(f"Unary operator {type(node.op).__name__} is not allowed")
        operand = _eval_node(node.operand)
        return _ALLOWED_UNARY[type(node.op)](operand)

    # Disallow any other node types
    raise ValueError(f"Disallowed expression component: {type(node).__name__}")

def evaluate_math_expression(expression: str):
    """
    Safely evaluates a mathematical expression consisting of numbers and
    the operators +, -, *, /, //, %, **.  All other syntax elements are
    rejected to avoid unsafe execution.

    Parameters:
        expression (str): The user supplied mathematical expression.

    Returns:
        float or int: The result of the evaluated expression.

    Raises:
        ValueError: If the expression contains disallowed characters,
                    unsupported operators, or unsafe constructs.
    """
    if not isinstance(expression, str):
        raise ValueError("Expression must be a string")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(expression, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}")

    # Ensure the parsed AST contains only allowed nodes
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Evaluate the parsed AST
    return _eval_node(parsed)

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     expr = "2 + 3 * (4 - 1) ** 2 / 5"
#     print(evaluate_math_expression(expr))