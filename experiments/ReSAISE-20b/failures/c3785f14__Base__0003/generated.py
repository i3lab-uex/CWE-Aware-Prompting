import ast
import builtins
import io
import sys
from types import ModuleType

# List of safe builtin functions that can be used in the sandbox.
SAFE_BUILTINS = {
    'abs': abs,
    'all': all,
    'any': any,
    'bool': bool,
    'chr': chr,
    'complex': complex,
    'dict': dict,
    'divmod': divmod,
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
    'tuple': tuple,
}

# Disallowed AST node types.
DISALLOWED_NODES = (
    ast.Import,          # import statements
    ast.ImportFrom,
    ast.Exec,            # exec is not an AST node in Python3 but keep for clarity
    ast.Call,           # we will allow calls only to SAFE_BUILTINS
    ast.Attribute,       # disallow attribute access like os.system
    ast.Subscript,      # disallow subscript on arbitrary objects
    ast.Lambda,
    ast.FunctionDef,
    ast.ClassDef,
    ast.For,
    ast.While,
    ast.With,
    ast.Try,
    ast.Global,
    ast.Nonlocal,
)

class _SafeVisitor(ast.NodeVisitor):
    """AST visitor that checks for disallowed constructs."""
    def visit(self, node):
        if isinstance(node, DISALLOWED_NODES):
            raise ValueError(f"Disallowed construct: {type(node).__name__}")
        # For Call nodes, ensure the function is a safe builtin
        if isinstance(node, ast.Call):
            # Only allow calls to names that are in SAFE_BUILTINS
            if isinstance(node.func, ast.Name):
                func_name = node.func.id
                if func_name not in SAFE_BUILTINS:
                    raise ValueError(f"Disallowed function call: {func_name}")
            else:
                # Any other callable (e.g., attribute access) is disallowed
                raise ValueError("Only calls to safe builtin names are allowed")
        return super().visit(node)

def evaluate_code_string(code_string: str):
    """
    Safely execute a small Python code snippet.

    Parameters
    ----------
    code_string : str
        The code to execute.

    Returns
    -------
    None or any
        If the code produces output via `print`, that output is returned as a string.
        If no output but the last expression evaluates to a value, that value is returned.
        Otherwise None is returned.

    Raises
    ------
    ValueError
        If the code attempts to use disallowed constructs.
    """
    # Parse the code and validate
    try:
        tree = ast.parse(code_string, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in code: {e}")

    _SafeVisitor().visit(tree)

    # Prepare a restricted global namespace
    sandbox_globals = {"__builtins__": SAFE_BUILTINS}
    sandbox_locals = {}

    # Capture stdout
    old_stdout = sys.stdout
    fake_out = io.StringIO()
    sys.stdout = fake_out

    try:
        # Execute the code
        exec(compile(tree, filename="<sandbox>", mode="exec"),
             sandbox_globals, sandbox_locals)

        # If the last statement is an expression, evaluate it
        result = None
        if tree.body and isinstance(tree.body[-1], ast.Expr):
            # Evaluate the expression in the same namespace
            expr_code = compile(ast.Expression(tree.body[-1].value),
                                filename="<sandbox>", mode="eval")
            result = eval(expr_code, sandbox_globals, sandbox_locals)

        # If anything was printed, return that output
        output = fake_out.getvalue()
        if output:
            return output.rstrip("\n")
        # If no output but a result, return it
        if result is not None:
            return result

    finally:
        # Restore stdout regardless of what happened
        sys.stdout = old_stdout

    return None