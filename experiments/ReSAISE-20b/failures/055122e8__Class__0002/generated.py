import ast
import math
from typing import Any, Optional

# Define a minimal safe namespace that can be used for evaluation.
SAFE_BUILTINS = {
    'abs': abs,
    'round': round,
    'min': min,
    'max': max,
    'sum': sum,
    'len': len,
    'range': range,
    # Add more safe builtins if required.
}

# Allow a limited set of math functions/attributes.
SAFE_MATH = {k: getattr(math, k) for k in dir(math) if not k.startswith('_')}


class UnsafeCodeError(ValueError):
    """Raised when the submitted code contains disallowed constructs."""
    pass


def _is_safe_node(node: ast.AST) -> bool:
    """
    Recursively check whether the AST node is safe.
    Prohibit imports, exec/eval, attribute access, function definitions,
    lambda, comprehensions with unsafe elements, etc.
    """
    # Disallowed node types
    disallowed = (
        ast.Import,
        ast.ImportFrom,
        ast.Exec,          # Python 2 only; kept for completeness
        ast.Call,         # We will inspect calls separately
        ast.Attribute,
        ast.Global,
        ast.Nonlocal,
        ast.Lambda,
        ast.FunctionDef,
        ast.AsyncFunctionDef,
        ast.ClassDef,
        ast.With,
        ast.AsyncWith,
        ast.For,
        ast.While,
        ast.Try,
    )

    if isinstance(node, disallowed):
        return False

    # For Call nodes we allow only whitelisted functions
    if isinstance(node, ast.Call):
        # Function name must be a simple Name (no attribute access)
        if not isinstance(node.func, ast.Name):
            return False
        # Disallow calling builtins that are not in SAFE_BUILTINS
        if node.func.id not in SAFE_BUILTINS:
            return False

    # Recurse into child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True


def execute_python_script(python_code: str) -> Optional[Any]:
    """
    Execute a user-provided Python script in a restricted environment.

    Parameters
    ----------
    python_code : str
        The Python code to execute.

    Returns
    -------
    Any | None
        The result of the last expression in the script, or None if there is no
        explicit result.

    Raises
    ------
    ValueError
        If the script contains prohibited operations or invalid syntax.
    """
    try:
        # Parse the code to an AST
        tree = ast.parse(python_code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python syntax: {exc}") from exc

    # Ensure the entire tree is safe
    if not _is_safe_node(tree):
        raise UnsafeCodeError("Script contains disallowed operations")

    # Prepare a restricted globals dictionary
    safe_globals = {
        '__builtins__': SAFE_BUILTINS,
        'math': SAFE_MATH,
    }

    # Execute the script
    exec(compile(tree, filename="<user_script>", mode="exec"), safe_globals)

    # Attempt to evaluate the last expression if it exists
    # We look for an Expr node at the end of the body.
    last_expr = None
    for node in reversed(tree.body):
        if isinstance(node, ast.Expr):
            last_expr = node
            break

    if last_expr is not None:
        try:
            # Compile the expression node separately
            expr_code = compile(ast.Expression(last_expr.value), filename="<user_script>", mode="eval")
            return eval(expr_code, safe_globals)
        except Exception as exc:
            # If evaluation fails, treat it as no result
            return None

    return None