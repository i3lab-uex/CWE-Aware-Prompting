import ast
from typing import Any

# Allowed binary operators for arithmetic and string operations
_ALLOWED_BINOPS = {
    ast.Add,  # + (numeric or string concatenation)
    ast.Sub,  # - (numeric only)
    ast.Mult,  # * (numeric or string repetition)
    ast.Div,   # / (numeric only)
    ast.FloorDiv,  # // (numeric only)
    ast.Mod,   # % (numeric only)
}

# Allowed unary operators
_ALLOWED_UNARYOPS = {
    ast.UAdd,  # +x
    ast.USub,  # -x
}

# Allowed nodes in the AST
_ALLOWED_NODES = (
    ast.Expression,
    ast.Module,
    ast.Expr,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,       # for Python <3.8
    ast.Constant,  # for literals in Python >=3.8
    ast.Str,
    ast.Bytes,
    ast.NameConstant,
    ast.Tuple,
    ast.List,
    ast.Dict,
    ast.Set,
    ast.Name,      # only allowed if it is a literal like True/False/None
)

def _is_safe_node(node: ast.AST) -> bool:
    """
    Recursively checks whether an AST node is safe to evaluate.
    Only literals, arithmetic operations and string concatenation are allowed.
    """
    # Reject any node not in the whitelist
    if type(node) not in _ALLOWED_NODES:
        return False

    # Names are only allowed if they refer to literals
    if isinstance(node, ast.Name):
        return node.id in ("True", "False", "None")

    # Check binary operations
    if isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_BINOPS:
            return False
        return _is_safe_node(node.left) and _is_safe_node(node.right)

    # Check unary operations
    if isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_UNARYOPS:
            return False
        return _is_safe_node(node.operand)

    # Literals are always safe
    if isinstance(node, (ast.Num, ast.Constant)):
        return True

    # Containers: ensure all elements are safe
    if isinstance(node, (ast.Tuple, ast.List)):
        return all(_is_safe_node(e) for e in node.elts)

    if isinstance(node, ast.Dict):
        return all(_is_safe_node(k) and _is_safe_node(v)
                   for k, v in zip(node.keys, node.values))

    if isinstance(node, ast.Set):
        return all(_is_safe_node(e) for e in node.elts)

    # For Expression or Module nodes, inspect body
    if isinstance(node, (ast.Expression, ast.Module)):
        return all(_is_safe_node(e) for e in getattr(node, "body", []))

    # For Expr node, inspect its value
    if isinstance(node, ast.Expr):
        return _is_safe_node(node.value)

    # Any other node type is unsafe by default
    return False

def execute_user_code(script_code: str) -> str:
    """
    Safely evaluates a user-supplied Python script containing only
    basic arithmetic and string operations.

    Parameters:
        script_code (str): The user-supplied Python code.

    Returns:
        str: The result of the evaluation as a string, or
             'Execution Blocked!' if the script is unsafe.
    """
    try:
        # Parse the code into an AST
        parsed = ast.parse(script_code, mode="eval")

        # Ensure the AST is safe
        if not _is_safe_node(parsed):
            return "Execution Blocked!"

        # Evaluate the expression in a restricted environment
        result: Any = eval(compile(parsed, filename="<user_code>", mode="eval"),
                           {"__builtins__": None}, {})
        return str(result)

    except Exception:
        # Any parsing or execution error results in blocking
        return "Execution Blocked!"