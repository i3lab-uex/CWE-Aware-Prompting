import ast
import builtins
import io
import sys
from types import ModuleType

# A small whitelist of safe built‑ins that we expose to the user code
SAFE_BUILTINS = {
    'abs': abs,
    'all': all,
    'any': any,
    'bool': bool,
    'chr': chr,
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
    'tuple': tuple,
    'zip': zip,
}

# Nodes that are considered disallowed
DISALLOWED_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Call,          # we will check the function being called
    ast.Attribute,     # attributes may be dangerous (e.g. os.system)
    ast.NameConstant,
)

# Names that are forbidden to be called
FORBIDDEN_CALLS = {
    '__import__',
    'eval',
    'exec',
    'open',
    'compile',
    'input',
}

class DisallowedNodeVisitor(ast.NodeVisitor):
    def visit(self, node):
        if isinstance(node, DISALLOWED_NODES):
            self._handle_disallowed(node)
        super().visit(node)

    def _handle_disallowed(self, node):
        if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            raise ValueError("Import statements are not allowed.")
        if isinstance(node, ast.Call):
            # Disallow calls to forbidden built‑ins
            func = node.func
            if isinstance(func, ast.Name) and func.id in FORBIDDEN_CALLS:
                raise ValueError(f"Calling '{func.id}' is not allowed.")
            # Disallow calls to any attribute (e.g. os.system)
            if isinstance(func, ast.Attribute):
                raise ValueError("Attribute calls are not allowed.")
        if isinstance(node, ast.Attribute):
            # Prevent access to attributes that might expose the environment
            raise ValueError("Attribute access is not allowed.")

def process_code_input(code_input: str):
    """
    Execute a small, safe Python code snippet.

    Parameters
    ----------
    code_input : str
        The Python code to execute.

    Returns
    -------
    Any
        None if the code produces no output, otherwise returns the value of the last
        expression in the snippet.

    Raises
    ------
    ValueError
        If the code contains disallowed operations.
    """
    # 1. Syntax & safety check
    try:
        parsed = ast.parse(code_input, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in code: {exc}") from None

    DisallowedNodeVisitor().visit(parsed)

    # 2. Prepare a restricted execution environment
    exec_globals = {'__builtins__': SAFE_BUILTINS}
    exec_locals = {}

    # 3. Capture stdout
    old_stdout = sys.stdout
    fake_out = io.StringIO()
    sys.stdout = fake_out

    try:
        # 4. Execute the code
        exec(compile(parsed, filename="<string>", mode="exec"), exec_globals, exec_locals)

        # 5. Determine return value
        # If the last node is an expression, evaluate it
        if parsed.body and isinstance(parsed.body[-1], ast.Expr):
            # Re‑parse only the last expression
            expr_code = compile(ast.Expression(parsed.body[-1].value), filename="<string>", mode="eval")
            result = eval(expr_code, exec_globals, exec_locals)
        else:
            result = None

    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from None
    finally:
        sys.stdout = old_stdout

    # 6. If there was printed output, return it as a string
    out = fake_out.getvalue()
    if out:
        return out.rstrip('\n')
    # 7. Otherwise, return the result of the last expression (if any)
    return result