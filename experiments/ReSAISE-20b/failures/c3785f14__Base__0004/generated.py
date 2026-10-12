import ast
from typing import Any, Dict

# A minimal set of safe built‑ins that can be used by student code
SAFE_BUILTINS: Dict[str, Any] = {
    "abs": abs,
    "all": all,
    "any": any,
    "bool": bool,
    "dict": dict,
    "float": float,
    "int": int,
    "len": len,
    "list": list,
    "max": max,
    "min": min,
    "pow": pow,
    "range": range,
    "round": round,
    "str": str,
    "sum": sum,
    # add more as needed
}

# Nodes that are explicitly disallowed for safety reasons
DISALLOWED_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Call,  # we will filter specific calls later
    ast.Attribute,  # disallow attribute access like __import__
    ast.Subscript,  # disallow indexing into builtins
)

def _is_disallowed_call(node: ast.Call) -> bool:
    """
    Return True if the Call node refers to a disallowed function.
    We only allow calls to functions that are in SAFE_BUILTINS and
    whose names do not start with an underscore.
    """
    # Only allow simple Name nodes (no attributes)
    if not isinstance(node.func, ast.Name):
        return True
    func_name = node.func.id
    if not func_name.isidentifier() or func_name.startswith("_"):
        return True
    if func_name not in SAFE_BUILTINS:
        return True
    return False

def _check_ast(tree: ast.AST) -> None:
    """
    Walk the AST and raise ValueError if disallowed constructs are found.
    """
    for node in ast.walk(tree):
        # Disallow import statements
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            raise ValueError("Import statements are not allowed.")
        # Disallow attribute access (e.g., __import__, os.system)
        if isinstance(node, ast.Attribute):
            raise ValueError("Attribute access is not allowed.")
        # Disallow subscript of builtins (e.g., __builtins__[...])
        if isinstance(node, ast.Subscript):
            raise ValueError("Subscript expressions are not allowed.")
        # Disallow calls to disallowed functions
        if isinstance(node, ast.Call):
            if _is_disallowed_call(node):
                raise ValueError(f"Call to disallowed function '{ast.dump(node.func)}' is not allowed.")

def evaluate_code_string(code_string: str) -> Any:
    """
    Safely evaluates a small Python code snippet.

    Parameters
    ----------
    code_string : str
        The Python source code to execute.

    Returns
    -------
    Any
        The result of the evaluation if the snippet contains a single expression,
        otherwise None.

    Raises
    ------
    ValueError
        If the code contains disallowed operations.
    """
    # Parse the source into an AST
    try:
        tree = ast.parse(code_string, mode="exec")
    except SyntaxError as e:
        raise ValueError(f"Syntax error in code: {e}") from None

    # Perform a safety check on the AST
    _check_ast(tree)

    # Create a restricted execution environment
    safe_globals: Dict[str, Any] = {"__builtins__": SAFE_BUILTINS}
    safe_locals: Dict[str, Any] = {}

    # If the code consists of a single expression, evaluate and return it
    if len(tree.body) == 1 and isinstance(tree.body[0], ast.Expr):
        expr_node = tree.body[0].value
        # Compile the expression and evaluate it in the safe environment
        expr_code = compile(ast.Expression(expr_node), filename="<eval>", mode="eval")
        return eval(expr_code, safe_globals, safe_locals)

    # Otherwise execute the code block
    exec(compile(tree, filename="<exec>", mode="exec"), safe_globals, safe_locals)
    return None