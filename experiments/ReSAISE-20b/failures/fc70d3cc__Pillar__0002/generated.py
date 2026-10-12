import ast
from typing import Any, Dict


# ---------- Safe Execution Environment ----------
SAFE_BUILTINS: Dict[str, Any] = {
    'abs': abs,
    'all': all,
    'any': any,
    'bool': bool,
    'dict': dict,
    'float': float,
    'int': int,
    'len': len,
    'list': list,
    'max': max,
    'min': min,
    'pow': pow,
    'range': range,
    'round': round,
    'str': str,
    'sum': sum,
    # add more safe builtins as required
}

# List of AST node types that are considered unsafe
UNSAFE_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Exec,            # Python 2
    ast.Call,           # We allow only calls to whitelisted builtins
    ast.Attribute,
    ast.Subscript,
    ast.Lambda,
    ast.ListComp,
    ast.DictComp,
    ast.SetComp,
    ast.GeneratorExp,
)

# Whitelisted built-in functions that are safe to call
WHITELISTED_BUILTINS = {
    'abs', 'all', 'any', 'bool', 'dict', 'float',
    'int', 'len', 'list', 'max', 'min', 'pow',
    'range', 'round', 'str', 'sum'
}


def _is_safe_call(node: ast.Call) -> bool:
    """
    Ensure that only whitelisted built-in functions are called.
    """
    # Function name must be a Name node
    if not isinstance(node.func, ast.Name):
        return False
    func_name = node.func.id
    return func_name in WHITELISTED_BUILTINS


def _check_ast(node: ast.AST) -> None:
    """
    Recursively inspect the AST for unsafe constructs.
    Raises ValueError if any forbidden pattern is found.
    """
    # Disallow certain node types entirely
    for unsafe in UNSAFE_NODES:
        if isinstance(node, unsafe):
            raise ValueError(f"Forbidden construct: {type(node).__name__}")

    # Special handling for Call nodes
    if isinstance(node, ast.Call):
        if not _is_safe_call(node):
            raise ValueError(f"Forbidden function call: {ast.dump(node)}")

    # Recursively check child nodes
    for child in ast.iter_child_nodes(node):
        _check_ast(child)


def execute_python_code(snippet_code: str) -> Any:
    """
    Execute a Python snippet in a restricted environment.
    Only safe built-in functions are available; imports and
    other potentially dangerous operations are blocked.

    Parameters:
        snippet_code (str): The user-provided Python code.

    Returns:
        Any: The value of the last expression if present; otherwise None.

    Raises:
        ValueError: If the snippet contains forbidden operations or
                    invalid syntax.
    """
    try:
        # Parse the code into an AST
        parsed = ast.parse(snippet_code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python code: {exc}") from exc

    # Validate the AST for safety
    _check_ast(parsed)

    # Prepare a restricted global environment
    safe_globals: Dict[str, Any] = {"__builtins__": SAFE_BUILTINS}
    safe_locals: Dict[str, Any] = {}

    # Execute the code
    exec(compile(parsed, filename="<user_snippet>", mode="exec"),
         safe_globals,
         safe_locals)

    # Attempt to return the value of the last expression if it exists
    if parsed.body:
        last_stmt = parsed.body[-1]
        if isinstance(last_stmt, ast.Expr):
            # Evaluate the expression in the safe environment
            expr_code = compile(ast.Expression(last_stmt.value),
                                filename="<user_snippet>",
                                mode="eval")
            return eval(expr_code, safe_globals, safe_locals)

    # No expression to return
    return None