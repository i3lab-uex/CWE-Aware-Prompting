import ast
import builtins
import sys
import io
from types import ModuleType

# ------------------------------------------------------------------
# 1. Safe builtin functions that are allowed in the sandbox
# ------------------------------------------------------------------
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
    # Add more safe builtins as needed
}

# ------------------------------------------------------------------
# 2. AST visitor that forbids dangerous nodes
# ------------------------------------------------------------------
class ForbiddenNodeVisitor(ast.NodeVisitor):
    """
    Raise ValueError if the AST contains any node that could lead to
    unsafe or forbidden operations.
    """
    # nodes that are considered dangerous
    FORBIDDEN_NODES = (
        ast.Import,          # import statements
        ast.ImportFrom,
        ast.Call,            # we will filter calls to unsafe functions separately
        ast.Attribute,       # disallow attribute access on arbitrary objects
        ast.NameConstant,    # e.g., None, True, False (allow? keep)
        ast.Global,
        ast.Nonlocal,
    )

    # names of functions that are disallowed
    FORBIDDEN_NAMES = {
        'exec', 'eval', 'compile', '__import__',
    }

    def visit(self, node):
        if isinstance(node, self.FORBIDDEN_NODES):
            raise ValueError(f"Forbidden node type: {type(node).__name__}")
        super().visit(node)

    def visit_Call(self, node):
        # disallow calls to forbidden names
        if isinstance(node.func, ast.Name) and node.func.id in self.FORBIDDEN_NAMES:
            raise ValueError(f"Call to forbidden function: {node.func.id}")
        # allow other calls only if the callee is a safe builtin
        if isinstance(node.func, ast.Name):
            if node.func.id not in SAFE_BUILTINS:
                raise ValueError(f"Call to untrusted function: {node.func.id}")
        # attribute calls are already caught by Attribute visitor
        self.generic_visit(node)

    def visit_Attribute(self, node):
        # Disallow any attribute access (e.g., os.system)
        raise ValueError(f"Attribute access is forbidden: {node.attr}")

# ------------------------------------------------------------------
# 3. The sandboxed execution function
# ------------------------------------------------------------------
def execute_python_code(snippet_code: str):
    """
    Execute a snippet of Python code in a sandboxed environment.

    Parameters
    ----------
    snippet_code : str
        The user-provided Python code to be executed.

    Returns
    -------
    Any
        The resulting value if the code produces any output, or None otherwise.

    Raises
    ------
    ValueError
        If the snippet attempts forbidden operations or contains invalid code.
    """
    # 1. Syntax check
    try:
        parsed = ast.parse(snippet_code, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in code: {e}")

    # 2. Security check
    visitor = ForbiddenNodeVisitor()
    try:
        visitor.visit(parsed)
    except ValueError as e:
        raise ValueError(f"Forbidden operation detected: {e}")

    # 3. Prepare sandboxed globals/locals
    sandbox_globals = {"__builtins__": SAFE_BUILTINS}
    sandbox_locals = {}

    # 4. Capture stdout to detect printed output
    old_stdout = sys.stdout
    captured_output = io.StringIO()
    sys.stdout = captured_output

    try:
        # Compile the code object
        code_obj = compile(parsed, filename="<sandbox>", mode="exec")
        # Execute the code
        exec(code_obj, sandbox_globals, sandbox_locals)
    except Exception as e:
        raise ValueError(f"Execution error: {e}") from None
    finally:
        sys.stdout = old_stdout

    # 5. Determine return value
    #   - If the last expression in the snippet is an Expr node, its value is returned.
    #   - Otherwise, if there was any printed output, return that string (trimmed).
    last_expr = None
    for node in parsed.body:
        if isinstance(node, ast.Expr):
            last_expr = node

    if last_expr is not None:
        # Evaluate the expression in the sandboxed environment
        try:
            expr_code = compile(ast.Expression(last_expr.value), filename="<sandbox>", mode="eval")
            result = eval(expr_code, sandbox_globals, sandbox_locals)
            return result
        except Exception as e:
            # If evaluation fails, fall back to printed output
            pass

    output = captured_output.getvalue().strip()
    return output if output else None