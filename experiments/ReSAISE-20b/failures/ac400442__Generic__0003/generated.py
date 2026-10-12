import ast

# A whitelist of safe built-in functions that can be used in the snippet.
SAFE_BUILTINS = {
    'print': print,
    'len': len,
    'range': range,
    'abs': abs,
    'min': min,
    'max': max,
    'sum': sum,
}

class SafeNodeVisitor(ast.NodeVisitor):
    """
    Visits the AST of a code snippet and raises ValueError if it contains
    disallowed nodes or function calls.
    """
    def __init__(self):
        self.allowed_calls = set(SAFE_BUILTINS.keys())

    def generic_visit(self, node):
        # Reject any node that is not explicitly allowed.
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            raise ValueError("Import statements are not allowed.")
        if isinstance(node, (ast.Exec, ast.Global, ast.Nonlocal)):
            raise ValueError(f"Disallowed statement: {type(node).__name__}")
        if isinstance(node, ast.Call):
            # Only allow calls to whitelisted built-ins.
            if not (isinstance(node.func, ast.Name) and node.func.id in self.allowed_calls):
                raise ValueError(f"Call to untrusted function '{getattr(node.func, 'id', None)}' is not allowed.")
        super().generic_visit(node)

def execute_code_snippet(code_snippet: str):
    """
    Execute a small Python code snippet safely.

    Parameters
    ----------
    code_snippet : str
        The Python code to execute.

    Returns
    -------
    Any
        Result of the executed snippet, or None if no result.

    Raises
    ------
    ValueError
        If the snippet contains disallowed operations.
    """
    # Parse and validate the code snippet.
    try:
        parsed = ast.parse(code_snippet, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in code snippet: {exc}") from exc

    # Perform safety checks.
    SafeNodeVisitor().visit(parsed)

    # Prepare a restricted execution environment.
    exec_globals = {'__builtins__': SAFE_BUILTINS}
    exec_locals = {}

    # Execute the code.
    try:
        exec(compile(parsed, filename="<snip>", mode="exec"), exec_globals, exec_locals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from exc

    # If the snippet ends with an expression, return its value.
    if parsed.body and isinstance(parsed.body[-1], ast.Expr):
        expr_value = eval(compile(ast.Expression(parsed.body[-1].value), filename="<snip>", mode="eval"),
                          exec_globals, exec_locals)
        return expr_value

    return None