import ast
import operator

# Mapping of supported binary operators to their functions
_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Mapping of supported unary operators to their functions
_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _evaluate(node, variables):
    """
    Recursively evaluate an AST node if it contains only constants.
    Returns the numeric value or raises ValueError for unsupported nodes.
    """
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.Name):
        # Variables are not evaluated at this stage; raise to indicate incomplete
        if node.id in variables:
            val = variables[node.id]
            if isinstance(val, (int, float)):
                return val
        raise ValueError(f"Cannot evaluate variable: {node.id}")

    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left, variables)
        right = _evaluate(node.right, variables)
        op_type = type(node.op)
        if op_type in _BIN_OPS:
            return _BIN_OPS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand, variables)
        op_type = type(node.op)
        if op_type in _UNARY_OPS:
            return _UNARY_OPS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    # Disallow function calls, attribute access, etc.
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def _substitute_and_rebuild(node, variables):
    """
    Walk the AST and replace variable names with their values (if available).
    Return a new node suitable for unparsing.
    """
    if isinstance(node, ast.Name):
        if node.id in variables:
            val = variables[node.id]
            if isinstance(val, (int, float)):
                return ast.copy_location(ast.Constant(value=val), node)
        # Leave the variable as is
        return node

    for field, old_value in ast.iter_fields(node):
        if isinstance(old_value, list):
            new_list = []
            for item in old_value:
                if isinstance(item, ast.AST):
                    new_list.append(_substitute_and_rebuild(item, variables))
                else:
                    new_list.append(item)
            setattr(node, field, new_list)
        elif isinstance(old_value, ast.AST):
            setattr(node, field, _substitute_and_rebuild(old_value, variables))
    return node

def process_math_expression(expression: str, variables: dict) -> str:
    """
    Simplify a mathematical expression string by substituting known variable values
    and evaluating any fully numeric sub‑expressions.

    Parameters:
        expression (str): The mathematical expression to process.
        variables  (dict): Mapping of variable names to numeric values.

    Returns:
        str: The simplified expression as a string.

    Raises:
        ValueError: If the expression is invalid or contains unsupported constructs.
    """
    try:
        # Parse into an AST
        expr_ast = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from exc

    # Ensure the top node is an Expression
    if not isinstance(expr_ast, ast.Expression):
        raise ValueError("Expression must be a single evaluatable expression")

    # First, attempt to evaluate the entire expression
    try:
        value = _evaluate(expr_ast.body, variables)
        # If evaluation succeeded, return the numeric result as string
        if isinstance(value, float) and value.is_integer():
            value = int(value)
        return str(value)
    except ValueError:
        # Not fully evaluable; proceed to substitute known variables
        pass

    # Substitute variables where possible
    substituted_ast = _substitute_and_rebuild(expr_ast, variables)

    # Attempt to evaluate again after substitution
    try:
        value = _evaluate(substituted_ast.body, variables)
        if isinstance(value, float) and value.is_integer():
            value = int(value)
        return str(value)
    except ValueError:
        # Return the partially substituted expression
        pass

    # Use ast.unparse to convert AST back to string (Python 3.9+)
    try:
        simplified = ast.unparse(substituted_ast).strip()
    except AttributeError as exc:
        # For older Python versions, provide a minimal fallback
        raise ValueError("ast.unparse is unavailable; requires Python 3.9+") from exc

    if not simplified:
        raise ValueError("Failed to produce a simplified expression")

    return simplified