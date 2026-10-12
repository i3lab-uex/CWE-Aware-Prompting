import ast
import operator

# Allowed binary operators mapping to actual functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}

# Allowed unary operators mapping
_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _eval_node(node):
    """
    Recursively evaluate an AST node ensuring only allowed operations are used.
    """
    if isinstance(node, ast.Num):  # For Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # For Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value)}")
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_UNARY_OPERATORS:
            return _ALLOWED_UNARY_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
    if isinstance(node, ast.Paren):  # Not actually a node type; parentheses are represented by grouping
        return _eval_node(node.value)
    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def safe_execute_operation(operation: str):
    """
    Evaluate a mathematical operation string safely.

    Parameters
    ----------
    operation : str
        The mathematical expression to evaluate. Allowed characters are digits,
        whitespace, and the operators + - * / ** % ().

    Returns
    -------
    float | int
        The result of the evaluated operation.

    Raises
    ------
    ValueError
        If the expression contains unsafe or unsupported constructs.
    """
    if not isinstance(operation, str):
        raise ValueError("Operation must be a string")

    # Strip whitespace to simplify parsing
    operation = operation.strip()
    if not operation:
        raise ValueError("Empty operation")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(operation, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Ensure the parsed tree contains only allowed nodes
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Module, ast.Expression)):
            continue
        elif isinstance(node, (ast.Num, ast.Constant)):
            if not isinstance(getattr(node, 'n', None) or getattr(node, 'value', None), (int, float)):
                raise ValueError(f"Unsupported constant type: {type(node)}")
        elif isinstance(node, (ast.BinOp, ast.UnaryOp)):
            if not isinstance(node.op, tuple(_ALLOWED_OPERATORS) + tuple(_ALLOWED_UNARY_OPERATORS)):
                raise ValueError(f"Unsupported operator: {node.op}")
        elif isinstance(node, ast.Call):
            raise ValueError("Function calls are not allowed")
        elif isinstance(node, (ast.Name, ast.Attribute)):
            raise ValueError("Names and attributes are not allowed")
        elif isinstance(node, (ast.Subscript, ast.ListComp, ast.DictComp, ast.SetComp, ast.GeneratorExp)):
            raise ValueError("Comprehensions and subscripts are not allowed")
        else:
            # Any other node types are disallowed
            raise ValueError(f"Disallowed expression component: {type(node).__name__}")

    # Evaluate the parsed AST
    try:
        result = _eval_node(parsed)
    except Exception as exc:
        raise ValueError(f"Error during evaluation: {exc}") from exc

    return result