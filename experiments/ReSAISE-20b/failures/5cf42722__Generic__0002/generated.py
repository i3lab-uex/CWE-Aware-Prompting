import ast
import operator
import re

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

# Regular expression to validate variable names (letters, digits, underscore, but not starting with digit)
_VAR_RE = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')


def _eval_node(node: ast.AST, vars_: dict) -> float:
    """
    Recursively evaluate an AST node safely.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body, vars_)

    elif isinstance(node, ast.Constant):          # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    elif isinstance(node, ast.Num):              # Python <3.8
        return node.n

    elif isinstance(node, ast.BinOp):
        left = _eval_node(node.left, vars_)
        right = _eval_node(node.right, vars_)
        op_type = type(node.op)
        if op_type in _BIN_OPS:
            try:
                return _BIN_OPS[op_type](left, right)
            except ZeroDivisionError as exc:
                raise ValueError("division by zero") from exc
        else:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    elif isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand, vars_)
        op_type = type(node.op)
        if op_type in _UNARY_OPS:
            return _UNARY_OPS[op_type](operand)
        else:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    elif isinstance(node, ast.Name):
        if node.id not in vars_:
            raise ValueError(f"Variable '{node.id}' is not provided")
        val = vars_[node.id]
        if not isinstance(val, (int, float)):
            raise ValueError(f"Variable '{node.id}' must be a number")
        return val

    elif isinstance(node, ast.Paren):  # Not actually needed; parentheses are handled by AST grouping
        return _eval_node(node.value, vars_)

    else:
        raise ValueError(f"Unsupported expression element: {type(node).__name__}")


def calculate_expression_securely(expr: str, var_substitute: dict) -> str:
    """
    Evaluate a mathematical expression safely with variable substitution.

    Parameters
    ----------
    expr : str
        The expression to evaluate.
    var_substitute : dict
        Mapping of variable names to numeric values.

    Returns
    -------
    str
        The computed result as a string.

    Raises
    ------
    ValueError
        If the expression is invalid, contains unsupported nodes,
        or a variable is missing/invalid.
    """
    if not isinstance(expr, str):
        raise ValueError("Expression must be a string")

    # Validate variable names
    for name in var_substitute:
        if not isinstance(name, str) or not _VAR_RE.match(name):
            raise ValueError(f"Invalid variable name: '{name}'")
        if not isinstance(var_substitute[name], (int, float)):
            raise ValueError(f"Variable '{name}' must be numeric")

    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from exc

    # Ensure the parsed AST contains only allowed nodes
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Call, ast.Import, ast.ImportFrom,
                            ast.Attribute, ast.Subscript, ast.ListComp,
                            ast.DictComp, ast.SetComp, ast.GeneratorExp)):
            raise ValueError(f"Disallowed expression component: {type(node).__name__}")

    result = _eval_node(parsed, var_substitute)

    # Convert to string; preserve integer format if no fractional part
    if isinstance(result, float) and result.is_integer():
        return str(int(result))
    return str(result)