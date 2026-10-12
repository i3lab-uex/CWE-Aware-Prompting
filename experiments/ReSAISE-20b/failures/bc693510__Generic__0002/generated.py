import ast
from types import SimpleNamespace

# --------------------------------------------------------------------------- #
# Safe Python snippet executor
# --------------------------------------------------------------------------- #

class _SafeVisitor(ast.NodeVisitor):
    """
    AST visitor that raises ValueError if the code contains any prohibited nodes.
    """
    # Nodes that are disallowed for safety reasons
    _prohibited = (
        ast.Import,
        ast.ImportFrom,
        ast.Call,          # calls are allowed only to whitelisted functions
        ast.Attribute,     # disallow attribute access (e.g., __import__, os.system)
        ast.Lambda,
        ast.ListComp,
        ast.DictComp,
        ast.SetComp,
        ast.GeneratorExp,
        ast.FormattedValue,
    )

    # Allowed built-in functions
    _allowed_builtins = {
        'abs', 'all', 'any', 'bool', 'chr', 'divmod', 'float',
        'int', 'len', 'max', 'min', 'pow', 'range', 'round',
        'sum', 'str', 'tuple'
    }

    def __init__(self):
        self._calls = []

    def visit(self, node):
        if isinstance(node, ast.Call):
            self._calls.append(node)
        super().visit(node)

    def generic_visit(self, node):
        if isinstance(node, self._prohibited):
            raise ValueError(f"Prohibited syntax: {type(node).__name__}")
        super().generic_visit(node)

    def check_calls(self):
        for call in self._calls:
            # Only allow calls to whitelisted builtins
            if isinstance(call.func, ast.Name):
                func_name = call.func.id
                if func_name not in self._allowed_builtins:
                    raise ValueError(f"Disallowed function call: {func_name}")
            else:
                # Any other kind of call (attribute access, lambda, etc.) is disallowed
                raise ValueError("Only simple builtin function calls are allowed")


def run_python_snippet(python_snippet: str):
    """
    Execute a small Python snippet safely.

    Parameters
    ----------
    python_snippet : str
        The code to run. It may contain a single expression or multiple statements.

    Returns
    -------
    Any
        The value of the last evaluated expression, or None if no result.

    Raises
    ------
    ValueError
        If the snippet contains disallowed syntax or calls.
    """
    if not isinstance(python_snippet, str):
        raise TypeError("python_snippet must be a string")

    # Parse the snippet into an AST
    try:
        parsed = ast.parse(python_snippet, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in snippet: {exc}") from None

    # Check for prohibited nodes
    visitor = _SafeVisitor()
    visitor.visit(parsed)
    visitor.check_calls()

    # Prepare a restricted execution environment
    safe_builtins = {k: __builtins__[k] for k in _SafeVisitor._allowed_builtins if k in __builtins__}
    globals_dict = {"__builtins__": safe_builtins}

    # Execute the code
    exec(compile(parsed, filename="<snippet>", mode="exec"), globals_dict)

    # If the snippet ends with an expression, evaluate it
    if parsed.body and isinstance(parsed.body[-1], ast.Expr):
        expr_code = compile(ast.Expression(body=parsed.body[-1].value), filename="<expr>", mode="eval")
        return eval(expr_code, globals_dict)

    return None

# --------------------------------------------------------------------------- #
# Example usage (commented out – remove comments to test)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     print(run_python_snippet("2 + 3"))          # Output: 5
#     run_python_snippet("""
#         a = 10
#         b = 20
#         a + b
#     """)                                       # Output: 30