import ast
import sys
import io
from types import SimpleNamespace

# List of AST node types that are considered safe.
SAFE_NODES = {
    ast.Module,
    ast.Expression,
    ast.Expr,
    ast.Assign,
    ast.AnnAssign,
    ast.Return,
    ast.Name,
    ast.Constant,
    ast.Num,        # for Python <3.8
    ast.Str,        # for Python <3.8
    ast.Bytes,      # for Python <3.8
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.operator,
    ast.unaryop,
    ast.boolop,
    ast.cmpop,
    # literals
    ast.Load,
    ast.Store,
}

# Names that are considered safe to use (builtins not allowed).
SAFE_NAMES = {
    'True',
    'False',
    'None',
}

class _SafeNodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.errors = []

    def generic_visit(self, node):
        if type(node) not in SAFE_NODES:
            self.errors.append(f"Disallowed node type: {type(node).__name__}")
        super().generic_visit(node)

    def visit_Call(self, node):
        # Calls are disallowed
        self.errors.append("Function calls are not allowed")
        # Don't visit further to avoid nested errors
    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load) and node.id not in SAFE_NAMES:
            self.errors.append(f"Use of undefined name '{node.id}' is not allowed")
        super().visit_Name(node)

def _validate_code(code_str: str):
    """
    Validate the AST of the supplied code. Raises ValueError if any disallowed
    constructs are found.
    """
    try:
        parsed = ast.parse(code_str, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in code: {e}") from None

    visitor = _SafeNodeVisitor()
    visitor.visit(parsed)

    if visitor.errors:
        raise ValueError("Forbidden code detected:\n" + "\n".join(visitor.errors))

def process_python_code(code_str: str):
    """
    Execute a snippet of Python code in a sandboxed environment that only
    allows safe operations (literals, arithmetic, assignments).  The function
    captures any text printed to stdout and returns it.  If the code does not
    produce output, None is returned.

    Parameters
    ----------
    code_str : str
        The user supplied Python snippet to execute.

    Returns
    -------
    str or None
        Captured stdout output, or None if nothing was printed.

    Raises
    ------
    ValueError
        If the snippet contains forbidden operations or is syntactically invalid.
    """
    _validate_code(code_str)

    # Prepare a minimal execution environment
    exec_globals = {"__builtins__": {}}
    exec_locals = {}

    # Capture stdout
    old_stdout = sys.stdout
    fake_out = io.StringIO()
    sys.stdout = fake_out

    try:
        exec(code_str, exec_globals, exec_locals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from None
    finally:
        sys.stdout = old_stdout

    output = fake_out.getvalue()
    return output if output else None