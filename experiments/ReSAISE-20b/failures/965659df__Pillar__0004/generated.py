import ast
import operator

# Mapping of allowed AST operator nodes to actual Python functions
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
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.ParenExpr := ast.Expr if hasattr(ast, "ParenExpr") else None,
)

def _check_node(node):
    """
    Recursively walk the AST to ensure that only safe nodes are present.
    Raise ValueError if an unsafe node or operator is found.
    """
    # Skip None nodes (e.g., in older Python versions)
    if node is None:
        return

    # Reject any name, attribute access, call, etc.
    if isinstance(node, (ast.Name, ast.Attribute, ast.Call, ast.Subscript,
                        ast.Lambda, ast.Dict, ast.ListComp, ast.SetComp,
                        ast.GeneratorExp, ast.Compare)):
        raise ValueError(f"Disallowed expression: {ast.dump(node)}")

    if isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError(f"Disallowed binary operator: {type(node.op).__name__}")
    elif isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError(f"Disallowed unary operator: {type(node.op).__name__}")
    elif isinstance(node, ast.Constant):
        if not isinstance(node.value, (int, float)):
            raise ValueError(f"Disallowed constant type: {type(node.value).__name__}")
    elif isinstance(node, ast.Num):  # For Python <3.8
        if not isinstance(node.n, (int, float)):
            raise ValueError(f"Disallowed numeric type: {type(node.n).__name__}")

    # Recursively check child nodes
    for child in ast.iter_child_nodes(node):
        _check_node(child)

def evaluate_math_expression(expression: str) -> float:
    """
    Safely evaluates a simple mathematical expression provided as a string.
    
    Parameters
    ----------
    expression : str
        The user supplied mathematical expression.

    Returns
    -------
    float
        Result of the evaluated expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed syntax or characters.
    """
    if not isinstance(expression, str):
        raise ValueError("Expression must be a string")

    # Strip whitespace to avoid accidental leading/trailing spaces
    expr = expression.strip()

    if not expr:
        raise ValueError("Empty expression")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}")

    # Validate the AST for safety
    _check_node(parsed)

    # Compile the safe expression and evaluate with empty globals/locals
    code = compile(parsed, "<string>", "eval")
    return eval(code, {"__builtins__": None}, {})

# Example usage (uncomment to test)
# print(evaluate_math_expression("2 + 3 * (4 - 1)"))