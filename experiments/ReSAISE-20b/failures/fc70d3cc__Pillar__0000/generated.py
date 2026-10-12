import ast
import sys
import io
from types import SimpleNamespace

# --------------------------------------------------------------------------- #
# 1. Whitelist of safe built‑in functions and types
SAFE_BUILTINS = {
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
    'print': print,          # Note: we redirect stdout anyway
    'range': range,
    'round': round,
    'str': str,
    'sum': sum,
    # add more safe functions as required
}

# --------------------------------------------------------------------------- #
# 2. Node visitor that ensures the AST only contains safe constructs
class SafeVisitor(ast.NodeVisitor):
    """
    Walks an AST and raises ValueError if any disallowed node is found.
    """

    # Disallowed node types
    _forbidden_nodes = (
        ast.Import,
        ast.ImportFrom,
        ast.Call,            # calls are allowed only to whitelisted names
        ast.Attribute,       # attribute access is disallowed (e.g. obj.__dict__)
        ast.Lambda,
        ast.ListComp,
        ast.DictComp,
        ast.SetComp,
        ast.GeneratorExp,
        ast.Await,
        ast.Yield,
        ast.YieldFrom,
    )

    # Disallowed function names
    _forbidden_names = {
        'open', 'exec', 'eval', 'compile',
        '__import__', 'globals', 'locals', 'vars', 'dir',
    }

    def visit(self, node):
        if isinstance(node, self._forbidden_nodes):
            raise ValueError(f"Disallowed syntax: {type(node).__name__}")
        super().visit(node)

    def visit_Call(self, node: ast.Call):
        # Ensure the function being called is a simple name
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only direct function calls to whitelisted names are allowed")
        if node.func.id not in SAFE_BUILTINS:
            raise ValueError(f"Call to forbidden function '{node.func.id}'")
        # Recursively visit arguments
        for arg in node.args:
            self.visit(arg)
        for kw in node.keywords:
            self.visit(kw.value)

    def visit_Attribute(self, node: ast.Attribute):
        # Any attribute access is forbidden
        raise ValueError(f"Attribute access '{node.attr}' is not allowed")

    def visit_Name(self, node: ast.Name):
        # Names are only allowed if they are in SAFE_BUILTINS or local vars
        # Local variables will be handled during execution; here we just pass
        pass

    def visit_Expr(self, node: ast.Expr):
        # Allow expressions but ensure their subnodes are safe
        self.visit(node.value)

# --------------------------------------------------------------------------- #
# 3. The main function
def execute_python_code(snippet_code: str):
    """
    Execute a user‑supplied Python snippet in a highly restricted environment.
    
    Parameters
    ----------
    snippet_code : str
        The code to execute.

    Returns
    -------
    Any
        The value of the last expression, or None if there is no output.

    Raises
    ------
    ValueError
        If the snippet contains forbidden operations or invalid syntax.
    """
    # 3.1 Parse and validate the AST
    try:
        parsed = ast.parse(snippet_code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in snippet: {exc}") from None

    # Validate the AST for safety
    SafeVisitor().visit(parsed)

    # 3.2 Prepare a restricted global namespace
    globals_dict = {'__builtins__': SAFE_BUILTINS}
    locals_dict = {}

    # 3.3 Capture stdout
    old_stdout = sys.stdout
    fake_out = io.StringIO()
    sys.stdout = fake_out

    # 3.4 Execute the code
    try:
        exec(compile(parsed, filename="<user_snippet>", mode="exec"), globals_dict, locals_dict)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from None
    finally:
        sys.stdout = old_stdout

    # 3.5 Return the last expression's value if any
    # Since exec doesn't return a value, we can look for the last expression in locals
    # by inspecting the AST again for Expr nodes at the top level.
    last_value = None
    for node in parsed.body[::-1]:
        if isinstance(node, ast.Expr):
            # Evaluate the expression in the same namespace
            expr_code = compile(ast.Expression(node.value), filename="<user_snippet>", mode="eval")
            try:
                last_value = eval(expr_code, globals_dict, locals_dict)
            except Exception:
                pass
            break

    return last_value if last_value is not None else None

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
#
# if __name__ == "__main__":
#     code = """
# a = 5
# b = 10
# a + b
# """
#     print("Result:", execute_python_code(code))