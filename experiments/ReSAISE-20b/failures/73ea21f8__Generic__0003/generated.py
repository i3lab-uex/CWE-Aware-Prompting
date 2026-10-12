import ast
from typing import Any

# A minimal set of safe built‑ins that students might need
SAFE_BUILTINS = {
    'abs': abs,
    'len': len,
    'range': range,
    'min': min,
    'max': max,
    'sum': sum,
    'sorted': sorted,
    'print': print,   # optional: allow printing
}

# Prohibited node types and names that should never appear in the snippet
PROHIBITED_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Exec,           # Python 2 only, but keep for completeness
    ast.Call,          # calls will be inspected further
)

PROHIBITED_CALL_NAMES = {
    'open', 'eval', 'exec', '__import__', 'globals', 'locals',
    'vars', 'dir', 'input', 'compile', 'execfile', 'os', 'sys',
}

def _check_node(node: ast.AST):
    """Recursively walk the AST and raise ValueError on prohibited patterns."""
    if isinstance(node, PROHIBITED_NODES):
        raise ValueError(f"Prohibited statement: {type(node).__name__}")

    # For Call nodes we need to inspect the function being called
    if isinstance(node, ast.Call):
        func = node.func
        # Handle simple names: e.g., open(...)
        if isinstance(func, ast.Name) and func.id in PROHIBITED_CALL_NAMES:
            raise ValueError(f"Prohibited function call: {func.id}()")
        # Handle attribute calls like os.system()
        if isinstance(func, ast.Attribute):
            attr_chain = []
            cur = func
            while isinstance(cur, ast.Attribute):
                attr_chain.append(cur.attr)
                cur = cur.value
            if isinstance(cur, ast.Name):
                attr_chain.append(cur.id)
                full_name = ".".join(reversed(attr_chain))
                if any(part in PROHIBITED_CALL_NAMES for part in attr_chain):
                    raise ValueError(f"Prohibited attribute call: {full_name}()")

    # Recursively check child nodes
    for child in ast.iter_child_nodes(node):
        _check_node(child)

def run_code_snippet(user_code: str) -> Any:
    """
    Execute a user supplied Python snippet in a sandboxed environment.

    Parameters
    ----------
    user_code : str
        The code snippet to execute. Only a very small subset of Python is allowed.

    Returns
    -------
    Any
        The value returned by the last expression in the snippet, or None.

    Raises
    ------
    ValueError
        If the snippet contains disallowed syntax or calls.
    """
    # Parse the code into an AST
    try:
        parsed = ast.parse(user_code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user code: {exc}") from exc

    # Perform a safety walk of the AST
    _check_node(parsed)

    # Prepare restricted globals and locals
    sandbox_globals = {'__builtins__': SAFE_BUILTINS}
    sandbox_locals: dict[str, Any] = {}

    # Execute the code. We capture the last expression if present.
    # For simplicity, we transform the AST into an Expression if it is a single Expr node
    last_expr_value = None

    # If the snippet ends with an expression, we can evaluate it separately
    if len(parsed.body) == 1 and isinstance(parsed.body[0], ast.Expr):
        # Compile as expression
        expr_code = compile(ast.Expression(parsed.body[0].value), '<string>', 'eval')
        last_expr_value = eval(expr_code, sandbox_globals, sandbox_locals)
    else:
        # Compile and execute
        exec(compile(parsed, '<string>', 'exec'), sandbox_globals, sandbox_locals)

    return last_expr_value