import ast
import builtins

# ------------------------------------------------------------
# 1. Define what is considered safe
# ------------------------------------------------------------
ALLOWED_BUILTINS = {
    'print',
    'len',
    'range',
    'int',
    'float',
    'str',
    'bool',
    'list',
    'dict',
    'set',
    'tuple',
    'sum',
    'min',
    'max',
    'abs',
}

# Create a dictionary of safe built‑in objects
SAFE_BUILTINS = {k: getattr(builtins, k) for k in ALLOWED_BUILTINS}

# ------------------------------------------------------------
# 2. AST visitor to detect disallowed constructs
# ------------------------------------------------------------
class SafeVisitor(ast.NodeVisitor):
    """
    Walk the AST and raise ValueError if any disallowed node is found.
    """

    # Nodes that are outright forbidden
    DISALLOWED_NODES = (
        ast.Import,
        ast.ImportFrom,
        ast.Exec,           # exec() was removed in Py3 but keep for completeness
        ast.Call,
        ast.Attribute,      # disallow attribute access like __import__
    )

    def visit(self, node):
        if isinstance(node, self.DISALLOWED_NODES):
            raise ValueError(f"Disallowed operation: {type(node).__name__}")
        # For Call nodes, only allow builtins in ALLOWED_BUILTINS
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name):
                if func.id not in ALLOWED_BUILTINS:
                    raise ValueError(f"Disallowed function call: {func.id}")
            else:
                # Any other form of function reference is disallowed
                raise ValueError("Only simple built‑in calls are allowed")
        super().visit(node)

# ------------------------------------------------------------
# 3. The main function
# ------------------------------------------------------------
def run_user_script(user_script: str):
    """
    Execute a user supplied Python script in a sandboxed environment.

    Parameters
    ----------
    user_script : str
        The Python code to run. Must not contain imports, attribute access,
        or any disallowed operations.

    Returns
    -------
    The value of the last expression in the script, or None if there is no
    expression.

    Raises
    ------
    ValueError
        If the script contains disallowed operations or has syntax errors.
    """
    try:
        # Parse the source into an AST
        tree = ast.parse(user_script, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user script: {exc}") from exc

    # Validate the AST
    SafeVisitor().visit(tree)

    # Separate statements and expressions
    expr_value = None
    for node in tree.body:
        if isinstance(node, ast.Expr):
            # Evaluate the expression and remember its value
            expr_value = eval(compile(ast.Expression(node.value), '<user_script>', 'eval'),
                              {'__builtins__': SAFE_BUILTINS})
        else:
            # Execute other statements (e.g., assignments)
            exec(compile(ast.Module([node], type_ignores=[]), '<user_script>', 'exec'),
                 {'__builtins__': SAFE_BUILTINS})

    return expr_value