import ast
from typing import Any, Optional

# Define a whitelist of AST node types that are considered safe.
SAFE_NODES = {
    ast.Module,
    ast.Expr,
    ast.Expression,
    ast.Load,
    ast.Store,
    ast.Name,
    ast.Constant,  # Python 3.8+: literals
    ast.Num,       # older literal nodes for compatibility
    ast.Str,
    ast.Bytes,
    ast.Tuple,
    ast.List,
    ast.Set,
    ast.Dict,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.IfExp,     # ternary expression
    ast.Call,      # function calls to whitelisted builtins only
    ast.Attribute,
    ast.Subscript,
    ast.Index,     # Python < 3.9
    ast.Slice,
    ast.NameConstant,   # True/False/None for older Python
}

# Whitelisted built‑in functions that may be called.
ALLOWED_BUILTINS = {
    'abs', 'min', 'max', 'sum', 'len',
    'sorted', 'reversed', 'range', 'enumerate',
    'list', 'tuple', 'set', 'dict', 'int', 'float',
    'str', 'bool', 'round'
}

# Whitelisted names that may appear in the code (e.g., built‑ins).
ALLOWED_NAMES = set(ALLOWED_BUILTINS)

def _is_safe_node(node: ast.AST) -> bool:
    """Recursively verify that every node in the AST is safe."""
    if type(node) not in SAFE_NODES:
        raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Special handling for Call nodes – only allow whitelisted functions.
    if isinstance(node, ast.Call):
        # The function being called must be a Name or Attribute.
        if isinstance(node.func, ast.Name):
            if node.func.id not in ALLOWED_BUILTINS:
                raise ValueError(f"Disallowed function call: {node.func.id}")
        elif isinstance(node.func, ast.Attribute):
            # Allow only built‑in functions accessed via __builtins__
            if not (isinstance(node.func.value, ast.Name) and node.func.value.id == '__builtins__'):
                raise ValueError("Only built‑in functions can be called via attributes")
        else:
            raise ValueError(f"Unsupported call target: {ast.dump(node.func)}")

    # Ensure no attribute access to dangerous modules.
    if isinstance(node, ast.Attribute):
        if isinstance(node.value, ast.Name) and node.value.id in ('os', 'sys', 'subprocess'):
            raise ValueError(f"Access to module '{node.value.id}' is forbidden")

    # Recursively check child nodes.
    for child in ast.iter_child_nodes(node):
        _is_safe_node(child)

def run_code_snippet(user_code: str) -> Optional[Any]:
    """
    Execute a user‑supplied Python code snippet in a highly restricted sandbox.

    Parameters
    ----------
    user_code : str
        The Python code to be executed. Only a single expression or simple
        statements are allowed.

    Returns
    -------
    Any | None
        The value of the last expression if one exists, otherwise ``None``.

    Raises
    ------
    ValueError
        If the code contains disallowed syntax or operations.
    """
    # Parse the code into an AST. We use mode='exec' to allow expressions
    # and simple statements but we will inspect the tree for safety.
    try:
        parsed = ast.parse(user_code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user code: {exc}")

    # Validate every node in the parsed tree.
    for node in ast.walk(parsed):
        _is_safe_node(node)

    # Prepare a restricted execution environment.
    safe_globals = {'__builtins__': {name: __builtins__[name] for name in ALLOWED_BUILTINS}}
    safe_locals = {}

    # If the user code is a single expression, compile as Expression and eval.
    if len(parsed.body) == 1 and isinstance(parsed.body[0], ast.Expr):
        expr = parsed.body[0].value
        compiled = compile(ast.Expression(expr), filename='<user_code>', mode='eval')
        return eval(compiled, safe_globals, safe_locals)

    # Otherwise compile as a module and execute. Capture the value of
    # the last expression if present.
    compiled = compile(parsed, filename='<user_code>', mode='exec')
    exec(compiled, safe_globals, safe_locals)

    # Attempt to return the value of the last expression if it exists.
    # We look for an Expr node at the end of the body.
    last_expr = None
    if parsed.body:
        last_stmt = parsed.body[-1]
        if isinstance(last_stmt, ast.Expr):
            last_expr = eval(compile(ast.Expression(last_stmt.value), filename='<user_code>', mode='eval'),
                             safe_globals, safe_locals)

    return last_expr

# Example usage (uncomment to test):
# print(run_code_snippet('2 + 3'))          # -> 5
# print(run_code_snippet('print("Hello")')) # -> None (prints Hello)