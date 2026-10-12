import ast
from typing import Any

# Whitelisted AST node types and operators for safe evaluation
ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Str,          # Python <3.8
    ast.Constant,     # Python >=3.8 (covers numbers and strings)
    ast.NameConstant,
    ast.UnaryOp,
)

ALLOWED_OPERATORS = (
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Mod,
    ast.Pow,
    ast.FloorDiv,
    ast.UAdd,
    ast.USub,
)

# No names are allowed (e.g., no variable references or builtins)
ALLOWED_NAMES = set()

def _is_safe_node(node: ast.AST) -> bool:
    """Recursively check that the AST contains only safe nodes and operators."""
    if not isinstance(node, ALLOWED_NODES):
        return False

    # Check operator nodes
    if isinstance(node, ast.BinOp) or isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in ALLOWED_OPERATORS:
            return False

    # Recurse into child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False

    # Disallow any Name usage
    if isinstance(node, ast.Name):
        if node.id not in ALLOWED_NAMES:
            return False

    # Disallow calls, attributes, subscripts, etc.
    if isinstance(node, (ast.Call, ast.Attribute, ast.Subscript, ast.Lambda,
                         ast.Dict, ast.ListComp, ast.SetComp, ast.GeneratorExp)):
        return False

    return True


def _eval_node(node: ast.AST) -> Any:
    """Evaluate a safe AST node using Python's eval on the node."""
    # Compile the expression into code object
    code = compile(node, filename="<user_script>", mode="eval")
    return eval(code, {"__builtins__": {}})  # empty builtins


def execute_user_code(script_code: str) -> str:
    """
    Safely evaluate a user-supplied Python script that contains only basic arithmetic
    or string operations.  If the code is unsafe, return 'Execution Blocked!'.

    Parameters
    ----------
    script_code : str
        The user-provided code to execute.

    Returns
    -------
    str
        Result of the evaluation converted to a string, or 'Execution Blocked!'.
    """
    try:
        # Parse the code as an expression (single line)
        parsed = ast.parse(script_code, mode="eval")
    except SyntaxError:
        # Could be a multi-line script; try to parse as module
        try:
            parsed = ast.parse(script_code, mode="exec")
        except SyntaxError:
            return "Execution Blocked!"

    # Validate the AST
    if not _is_safe_node(parsed):
        return "Execution Blocked!"

    # Evaluate safely
    try:
        result = _eval_node(parsed)
    except Exception:
        return "Execution Blocked!"

    # Convert result to string for consistent return type
    return str(result)