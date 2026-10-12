import ast
from typing import Any, Dict, Optional

# --------------------------------------------------------------------------- #
# Safe Python snippet executor
#
# The function below evaluates a user supplied code string in a tightly
# controlled environment.  It performs the following safety checks:
#
#   * No import statements (Import / ImportFrom)
#   * No calls to built‑ins that can access the file system or run shell
#     commands (open, eval, exec, __import__, os.system, subprocess.*)
#   * No attribute access that could reach unsafe objects
#
# The snippet is executed with a minimal set of safe built‑ins.  If the
# snippet contains a top‑level expression it is evaluated and its result
# returned; otherwise the function returns None.
#
# This implementation attempts to mitigate CWE‑707 by ensuring that
# all nodes are inspected before execution and that only well‑formed
# code reaches the interpreter.
# --------------------------------------------------------------------------- #

SAFE_BUILTINS: Dict[str, Any] = {
    'abs': abs,
    'all': all,
    'any': any,
    'bool': bool,
    'chr': chr,
    'dict': dict,
    'enumerate': enumerate,
    'filter': filter,
    'float': float,
    'int': int,
    'len': len,
    'list': list,
    'map': map,
    'max': max,
    'min': min,
    'pow': pow,
    'range': range,
    'reversed': reversed,
    'round': round,
    'sorted': sorted,
    'str': str,
    'sum': sum,
    'tuple': tuple,
}

# Prohibited node types
FORBIDDEN_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Exec,          # only in Python 2; kept for completeness
)

# Prohibited call names (including dotted forms)
FORBIDDEN_CALLS = {
    'open',
    'eval',
    'exec',
    '__import__',
    'os.system',
    'subprocess.Popen',
    'subprocess.call',
    'subprocess.run',
}

def _is_call_prohibited(node: ast.Call) -> bool:
    """
    Determine if a Call node is to a forbidden function.
    Handles both simple names and dotted attribute chains.
    """
    # Handle Name: eval(x)
    if isinstance(node.func, ast.Name):
        return node.func.id in FORBIDDEN_CALLS
    # Handle Attribute: os.system(...)
    if isinstance(node.func, ast.Attribute):
        parts = []
        cur = node.func
        while isinstance(cur, ast.Attribute):
            parts.append(cur.attr)
            cur = cur.value
        if isinstance(cur, ast.Name):
            parts.append(cur.id)
            full_name = '.'.join(reversed(parts))
            return full_name in FORBIDDEN_CALLS
    return False

def _check_safety(tree: ast.AST) -> None:
    """
    Walk the AST and raise ValueError if any forbidden construct is found.
    """
    for node in ast.walk(tree):
        # Prohibit import statements
        if isinstance(node, FORBIDDEN_NODES):
            raise ValueError(f"Import statements are not allowed: {ast.dump(node)}")
        # Prohibit forbidden calls
        if isinstance(node, ast.Call) and _is_call_prohibited(node):
            raise ValueError(f"Call to forbidden function: {ast.dump(node)}")
        # Prohibit attribute access that may reach unsafe objects
        if isinstance(node, ast.Attribute):
            # If the root is a Name that resolves to an unsafe module
            if isinstance(node.value, ast.Name) and node.value.id in ('os', 'subprocess'):
                raise ValueError(f"Attribute access to unsafe module '{node.value.id}' is forbidden.")
        # Prohibit use of globals or locals in eval context
        if isinstance(node, ast.Name):
            if node.id in ('__builtins__', 'globals', 'locals'):
                raise ValueError(f"Access to '{node.id}' is forbidden.")
    # Additional high-level checks can be added here

def run_python_snippet(python_snippet: str) -> Optional[Any]:
    """
    Execute a Python code snippet in a restricted environment.

    Parameters
    ----------
    python_snippet : str
        The user supplied Python code to be executed.

    Returns
    -------
    Optional[Any]
        The result of the last expression in the snippet, or None if
        there is no evaluable expression.

    Raises
    ------
    ValueError
        If the snippet contains prohibited actions.
    """
    if not isinstance(python_snippet, str):
        raise ValueError("python_snippet must be a string")

    # Parse the code into an AST
    try:
        tree = ast.parse(python_snippet, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in snippet: {exc}") from exc

    # Safety checks
    _check_safety(tree)

    # Separate the last expression if it exists
    expr_result: Optional[Any] = None
    body = tree.body

    if body and isinstance(body[-1], ast.Expr):
        # Compile the expression separately for evaluation
        expr_code = compile(ast.Expression(body[-1].value), '<string>', mode='eval')
    else:
        expr_code = None

    # Compile the rest of the statements
    stmt_body = body[:-1] if expr_code else body
    if stmt_body:
        stmt_tree = ast.Module(body=stmt_body, type_ignores=[])
        stmt_code = compile(stmt_tree, '<string>', mode='exec')
    else:
        stmt_code = None

    # Prepare the execution environment
    safe_globals: Dict[str, Any] = {'__builtins__': SAFE_BUILTINS}
    local_vars: Dict[str, Any] = {}

    # Execute statements
    if stmt_code:
        exec(stmt_code, safe_globals, local_vars)

    # Evaluate the last expression
    if expr_code:
        expr_result = eval(expr_code, safe_globals, local_vars)

    return expr_result

# Example usage (commented out)
# if __name__ == "__main__":
#     print(run_python_snippet("x = 2 + 3\nx * 5"))
#     print(run_python_snippet("abs(-10)"))   # should return 10