import ast

# List of disallowed AST node types and names that can lead to unsafe execution
DISALLOWED_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Exec,          # Py2 legacy
    ast.Call,         # disallow function calls entirely
    ast.Attribute,
    ast.Subscript,
}
DISALLOWED_NAMES = {
    "__import__",
    "eval",
    "exec",
    "open",
    "compile",
    "input",
    "__import__",
}

def _is_safe(node: ast.AST) -> bool:
    """
    Recursively check that a node tree contains only safe nodes.
    Allowed nodes: literals, arithmetic ops, comparisons, boolean ops,
    and simple names that are not in DISALLOWED_NAMES.
    """
    if type(node) in DISALLOWED_NODES:
        return False

    # Names that are allowed: simple identifiers
    if isinstance(node, ast.Name):
        return node.id not in DISALLOWED_NAMES

    # For literals and constants, always safe
    if isinstance(node, (ast.Constant, ast.Num, ast.Str)):
        return True

    # Allow simple operators and expressions
    if isinstance(node, (
            ast.BinOp,
            ast.UnaryOp,
            ast.BoolOp,
            ast.Compare,
            ast.IfExp,
            ast.Tuple,
            ast.List,
            ast.Dict,
            ast.Set,
        )):
        for child in ast.iter_child_nodes(node):
            if not _is_safe(child):
                return False
        return True

    # Any other node type is disallowed
    return False


def evaluate_user_code(code_string: str) -> str:
    """
    Safely evaluate a user provided Python expression.
    Returns the string representation of the result or an error message.

    Raises:
        None – errors are returned as a string.
    """
    try:
        # Parse the code into an AST
        tree = ast.parse(code_string, mode="eval")

        # Validate the tree for safety
        if not _is_safe(tree.body):
            return "Unsafe Code Detected!"

        # Compile the AST into a code object with restricted globals
        compiled = compile(tree, filename="<user>", mode="eval")

        # Execute with an empty globals dict and a safe locals dict
        result = eval(compiled, {"__builtins__": {}}, {})
        return str(result)

    except Exception:
        # Any error (syntax, runtime, etc.) is treated as unsafe
        return "Unsafe Code Detected!"